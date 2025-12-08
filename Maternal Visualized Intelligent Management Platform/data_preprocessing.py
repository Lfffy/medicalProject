"""
数据预处理和特征工程模块
为孕产妇健康风险预测提供专业的数据处理功能
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PolynomialFeatures
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
import json
import os
from datetime import datetime

class MaternalDataPreprocessor:
    """孕产妇数据预处理类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化数据预处理器
        
        Args:
            config_path: 配置文件路径
        """
        # 配置参数
        self.config = self._load_config(config_path)
        
        # 预处理器存储
        self.preprocessors = {}
        
        # 特征信息
        self.feature_info = {
            'numeric_features': ['age', 'height', 'weight', 'gestational_weeks', 
                               'systolic_pressure', 'diastolic_pressure', 'heart_rate',
                               'temperature', 'blood_sugar', 'hemoglobin', 'bmi'],
            'categorical_features': ['pregnancy_type', 'risk_factors'],
            'time_features': ['last_menstrual_date', 'created_at', 'due_date']
        }
        
        # 数据验证规则
        self.validation_rules = {
            'age': {'min': 12, 'max': 55},
            'height': {'min': 140, 'max': 200},
            'weight': {'min': 30, 'max': 200},
            'gestational_weeks': {'min': 0, 'max': 43},
            'systolic_pressure': {'min': 80, 'max': 220},
            'diastolic_pressure': {'min': 40, 'max': 140},
            'heart_rate': {'min': 50, 'max': 180},
            'temperature': {'min': 35.0, 'max': 42.0},
            'blood_sugar': {'min': 2.0, 'max': 33.3},
            'hemoglobin': {'min': 50, 'max': 200}
        }
        
        # 初始化预处理器
        self._initialize_preprocessors()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        default_config = {
            'imputation_strategy': 'knn',  # 'mean', 'median', 'most_frequent', 'knn'
            'scaling_method': 'standard',  # 'standard', 'minmax', 'robust'
            'polynomial_degree': 0,
            'feature_selection': False,
            'n_features_to_select': 20
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    return {**default_config, **user_config}
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def _initialize_preprocessors(self):
        """
        初始化预处理器
        """
        # 创建数值型特征处理管道
        numeric_steps = []
        
        # 缺失值处理
        if self.config['imputation_strategy'] == 'knn':
            numeric_steps.append(('imputer', KNNImputer(n_neighbors=5)))
        else:
            numeric_steps.append(('imputer', SimpleImputer(strategy=self.config['imputation_strategy'])))
        
        # 数据缩放
        if self.config['scaling_method'] == 'standard':
            numeric_steps.append(('scaler', StandardScaler()))
        elif self.config['scaling_method'] == 'minmax':
            numeric_steps.append(('scaler', MinMaxScaler()))
        elif self.config['scaling_method'] == 'robust':
            numeric_steps.append(('scaler', RobustScaler()))
        
        # 如果需要多项式特征
        if self.config['polynomial_degree'] > 1:
            numeric_steps.append(('poly', PolynomialFeatures(degree=self.config['polynomial_degree'], 
                                                           include_bias=False)))
        
        self.preprocessors['numeric_pipeline'] = Pipeline(steps=numeric_steps)
    
    def validate_data(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        验证输入数据的有效性
        
        Args:
            data: 输入数据字典
            
        Returns:
            (是否有效, 错误消息列表)
        """
        errors = []
        
        # 验证必填字段
        required_fields = ['age', 'gestational_weeks', 'systolic_pressure', 'diastolic_pressure']
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f'缺少必填字段: {field}')
        
        # 验证数值范围
        for field, rules in self.validation_rules.items():
            if field in data and data[field] is not None:
                try:
                    value = float(data[field])
                    if value < rules['min'] or value > rules['max']:
                        errors.append(f'{field} 值超出有效范围: {rules["min"]} - {rules["max"]}')
                except (ValueError, TypeError):
                    errors.append(f'{field} 值不是有效的数字')
        
        # 验证孕周与血压的合理性（子痫前期风险）
        if 'gestational_weeks' in data and 'systolic_pressure' in data and \
           data['gestational_weeks'] is not None and data['systolic_pressure'] is not None:
            try:
                weeks = float(data['gestational_weeks'])
                systolic = float(data['systolic_pressure'])
                # 早期妊娠血压过高需要特别标记
                if weeks <= 20 and systolic > 140:
                    errors.append('早期妊娠收缩压过高，建议立即医疗评估')
            except (ValueError, TypeError):
                pass
        
        # 验证BMI的合理性（如果可以计算）
        if 'height' in data and 'weight' in data and \
           data['height'] is not None and data['weight'] is not None:
            try:
                height = float(data['height']) / 100  # 转换为米
                weight = float(data['weight'])
                bmi = weight / (height ** 2)
                if bmi < 15 or bmi > 60:
                    errors.append(f'BMI ({bmi:.1f}) 超出合理范围')
            except (ValueError, TypeError):
                pass
        
        return len(errors) == 0, errors
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清理数据
        
        Args:
            df: 输入DataFrame
            
        Returns:
            清理后的DataFrame
        """
        df_clean = df.copy()
        
        # 删除完全重复的行
        df_clean.drop_duplicates(inplace=True)
        
        # 处理异常值
        for column, rules in self.validation_rules.items():
            if column in df_clean.columns:
                # 替换超出范围的值为NaN
                df_clean[column] = np.where(
                    (df_clean[column] < rules['min']) | (df_clean[column] > rules['max']),
                    np.nan,
                    df_clean[column]
                )
        
        # 处理逻辑矛盾（例如，舒张压大于收缩压）
        if 'systolic_pressure' in df_clean.columns and 'diastolic_pressure' in df_clean.columns:
            invalid_bp = df_clean['diastolic_pressure'] >= df_clean['systolic_pressure']
            if invalid_bp.any():
                # 将无效的血压值设为NaN
                df_clean.loc[invalid_bp, ['systolic_pressure', 'diastolic_pressure']] = np.nan
        
        return df_clean
    
    def generate_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        为单个患者数据生成特征
        
        Args:
            data: 患者数据字典
            
        Returns:
            包含生成特征的数据字典
        """
        enhanced_data = data.copy()
        
        # 计算BMI
        if 'weight' in data and 'height' in data and \
           data['weight'] is not None and data['height'] is not None:
            try:
                weight = float(data['weight'])
                height = float(data['height']) / 100  # 转换为米
                enhanced_data['bmi'] = weight / (height ** 2)
                
                # BMI分类
                bmi = enhanced_data['bmi']
                enhanced_data['bmi_category'] = 'normal'
                if bmi < 18.5:
                    enhanced_data['bmi_category'] = 'underweight'
                elif bmi >= 24 and bmi < 28:
                    enhanced_data['bmi_category'] = 'overweight'
                elif bmi >= 28:
                    enhanced_data['bmi_category'] = 'obese'
            except (ValueError, TypeError, ZeroDivisionError):
                enhanced_data['bmi'] = None
                enhanced_data['bmi_category'] = None
        
        # 计算脉压和平均动脉压
        if 'systolic_pressure' in data and 'diastolic_pressure' in data and \
           data['systolic_pressure'] is not None and data['diastolic_pressure'] is not None:
            try:
                systolic = float(data['systolic_pressure'])
                diastolic = float(data['diastolic_pressure'])
                if diastolic < systolic:  # 确保舒张压小于收缩压
                    enhanced_data['pulse_pressure'] = systolic - diastolic
                    enhanced_data['mean_arterial_pressure'] = diastolic + enhanced_data['pulse_pressure'] / 3
                    
                    # 血压分类
                    if systolic < 120 and diastolic < 80:
                        enhanced_data['bp_category'] = 'normal'
                    elif systolic < 130 and diastolic < 80:
                        enhanced_data['bp_category'] = 'elevated'
                    elif systolic < 140 or diastolic < 90:
                        enhanced_data['bp_category'] = 'stage1'
                    else:
                        enhanced_data['bp_category'] = 'stage2'
            except (ValueError, TypeError):
                enhanced_data['pulse_pressure'] = None
                enhanced_data['mean_arterial_pressure'] = None
                enhanced_data['bp_category'] = None
        
        # 孕期阶段分类
        if 'gestational_weeks' in data and data['gestational_weeks'] is not None:
            try:
                weeks = float(data['gestational_weeks'])
                if weeks <= 12:
                    enhanced_data['trimester'] = 1
                elif weeks <= 26:
                    enhanced_data['trimester'] = 2
                else:
                    enhanced_data['trimester'] = 3
            except (ValueError, TypeError):
                enhanced_data['trimester'] = None
        
        # 年龄风险分类
        if 'age' in data and data['age'] is not None:
            try:
                age = float(data['age'])
                enhanced_data['age_risk'] = 0
                if age < 18 or age > 35:
                    enhanced_data['age_risk'] = 1
            except (ValueError, TypeError):
                enhanced_data['age_risk'] = None
        
        # 风险因素解析和计数
        if 'risk_factors' in data and data['risk_factors'] is not None:
            risk_text = str(data['risk_factors'])
            # 常见风险因素列表
            common_risks = ['高血压', '糖尿病', '肥胖', '高龄', '多胎', '既往子痫前期', 
                           '既往妊娠期糖尿病', '吸烟', '家族史', '贫血', '甲状腺疾病', 
                           '自身免疫性疾病', '肾脏疾病', '肝脏疾病', '心脏病', '前置胎盘',
                           '胎盘早剥', '羊水过多', '羊水过少', '胎儿生长受限', '早产史',
                           '死胎史', '药物使用', '接触有害物质']
            
            # 风险因素计数
            risk_count = sum(1 for risk in common_risks if risk in risk_text)
            enhanced_data['risk_count'] = risk_count
            
            # 高风险标识
            enhanced_data['high_risk_combination'] = 1 if risk_count >= 2 else 0
            
            # 为每个风险因素创建布尔特征
            for risk in common_risks:
                enhanced_data[f'risk_{risk}'] = 1 if risk in risk_text else 0
        
        return enhanced_data
    
    def preprocess_for_prediction(self, data: Dict[str, Any]) -> Tuple[np.ndarray, List[str]]:
        """
        预处理单个患者数据用于预测
        
        Args:
            data: 患者数据字典
            
        Returns:
            (特征数组, 特征名称列表)
        """
        # 生成增强特征
        enhanced_data = self.generate_features(data)
        
        # 创建特征向量
        features = []
        feature_names = []
        
        # 基本特征
        basic_features = ['age', 'gestational_weeks', 'systolic_pressure', 'diastolic_pressure', 
                         'heart_rate', 'blood_sugar', 'bmi', 'risk_count', 'age_risk']
        
        for feature in basic_features:
            if feature in enhanced_data and enhanced_data[feature] is not None:
                try:
                    features.append(float(enhanced_data[feature]))
                    feature_names.append(feature)
                except (ValueError, TypeError):
                    features.append(0.0)  # 默认值
                    feature_names.append(feature)
            else:
                features.append(0.0)  # 默认值
                feature_names.append(feature)
        
        # 衍生特征
        derived_features = ['pulse_pressure', 'mean_arterial_pressure']
        
        for feature in derived_features:
            if feature in enhanced_data and enhanced_data[feature] is not None:
                try:
                    features.append(float(enhanced_data[feature]))
                    feature_names.append(feature)
                except (ValueError, TypeError):
                    features.append(0.0)  # 默认值
                    feature_names.append(feature)
            else:
                features.append(0.0)  # 默认值
                feature_names.append(feature)
        
        # 分类特征的数值编码
        if 'trimester' in enhanced_data and enhanced_data['trimester'] is not None:
            features.append(float(enhanced_data['trimester']))
            feature_names.append('trimester')
        else:
            features.append(0.0)
            feature_names.append('trimester')
        
        if 'high_risk_combination' in enhanced_data and enhanced_data['high_risk_combination'] is not None:
            features.append(float(enhanced_data['high_risk_combination']))
            feature_names.append('high_risk_combination')
        else:
            features.append(0.0)
            feature_names.append('high_risk_combination')
        
        return np.array([features]), feature_names
    
    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
        """
        拟合并转换数据
        
        Args:
            df: 输入DataFrame
            
        Returns:
            (转换后的特征数组, 特征名称列表)
        """
        # 清理数据
        df_clean = self.clean_data(df)
        
        # 生成增强特征
        enhanced_data_list = []
        for _, row in df_clean.iterrows():
            enhanced_data = self.generate_features(row.to_dict())
            enhanced_data_list.append(enhanced_data)
        
        df_enhanced = pd.DataFrame(enhanced_data_list)
        
        # 选择用于训练的特征
        features_to_use = ['age', 'gestational_weeks', 'systolic_pressure', 'diastolic_pressure',
                          'heart_rate', 'blood_sugar', 'bmi', 'pulse_pressure',
                          'mean_arterial_pressure', 'trimester', 'age_risk',
                          'risk_count', 'high_risk_combination']
        
        # 过滤出存在的特征
        available_features = [f for f in features_to_use if f in df_enhanced.columns]
        
        # 提取特征矩阵
        X = df_enhanced[available_features].copy()
        
        # 处理缺失值
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        
        # 拟合并转换数值特征
        if len(numeric_columns) > 0:
            X_numeric = X[numeric_columns]
            
            # 训练预处理器
            self.preprocessors['numeric_pipeline'].fit(X_numeric)
            
            # 转换数据
            X_numeric_transformed = self.preprocessors['numeric_pipeline'].transform(X_numeric)
            
            # 如果应用了多项式特征，需要生成新的特征名称
            if self.config['polynomial_degree'] > 1:
                # 获取多项式特征转换器
                poly = self.preprocessors['numeric_pipeline'].named_steps['poly']
                new_feature_names = poly.get_feature_names_out(numeric_columns)
            else:
                new_feature_names = numeric_columns.tolist()
            
            # 创建转换后的DataFrame
            X_transformed = pd.DataFrame(X_numeric_transformed, columns=new_feature_names)
            
            # 如果启用了特征选择
            if self.config['feature_selection'] and hasattr(self.config, 'n_features_to_select'):
                selector = SelectKBest(f_classif, k=self.config['n_features_to_select'])
                X_final = selector.fit_transform(X_transformed, df_enhanced.get('risk_label', np.zeros(len(df_enhanced))))
                selected_features = [new_feature_names[i] for i in selector.get_support(indices=True)]
                
                # 保存选择器
                self.preprocessors['feature_selector'] = selector
                
                return X_final, selected_features
            
            return X_transformed.values, new_feature_names.tolist()
        
        return np.array([]), []
    
    def transform(self, data: Dict[str, Any]) -> np.ndarray:
        """
        转换新数据用于预测
        
        Args:
            data: 患者数据字典
            
        Returns:
            转换后的特征数组
        """
        # 预处理数据
        X, feature_names = self.preprocess_for_prediction(data)
        
        # 转换数值特征
        X_df = pd.DataFrame(X, columns=feature_names)
        numeric_columns = X_df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) > 0 and 'numeric_pipeline' in self.preprocessors:
            X_transformed = self.preprocessors['numeric_pipeline'].transform(X_df[numeric_columns])
            
            # 如果有特征选择器，应用它
            if 'feature_selector' in self.preprocessors:
                X_transformed = self.preprocessors['feature_selector'].transform(X_transformed)
            
            return X_transformed
        
        return X
    
    def save_preprocessors(self, directory: str):
        """
        保存预处理器到文件
        
        Args:
            directory: 保存目录
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # 保存每个预处理器
        for name, preprocessor in self.preprocessors.items():
            try:
                path = os.path.join(directory, f'{name}.joblib')
                joblib.dump(preprocessor, path)
            except Exception as e:
                print(f"保存预处理器 {name} 失败: {e}")
        
        # 保存配置和特征信息
        metadata = {
            'config': self.config,
            'feature_info': self.feature_info,
            'validation_rules': self.validation_rules,
            'save_time': datetime.now().isoformat()
        }
        
        try:
            with open(os.path.join(directory, 'preprocessor_metadata.json'), 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存预处理器元数据失败: {e}")
    
    def load_preprocessors(self, directory: str):
        """
        从文件加载预处理器
        
        Args:
            directory: 加载目录
        """
        # 加载元数据
        metadata_path = os.path.join(directory, 'preprocessor_metadata.json')
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    self.config = metadata.get('config', self.config)
                    self.feature_info = metadata.get('feature_info', self.feature_info)
                    self.validation_rules = metadata.get('validation_rules', self.validation_rules)
            except Exception as e:
                print(f"加载预处理器元数据失败: {e}")
        
        # 加载预处理器
        preprocessor_files = [f for f in os.listdir(directory) if f.endswith('.joblib')]
        for file in preprocessor_files:
            name = file[:-7]  # 移除.joblib扩展名
            try:
                path = os.path.join(directory, file)
                self.preprocessors[name] = joblib.load(path)
            except Exception as e:
                print(f"加载预处理器 {name} 失败: {e}")

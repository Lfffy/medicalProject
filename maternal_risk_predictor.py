"""
孕产妇风险专用预测模型
针对孕产妇特有生理变化和妊娠期并发症风险设计的专用预测算法
"""

import numpy as np
import pandas as pd
import os
import json
import joblib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.utils.class_weight import compute_class_weight

import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical


class MaternalRiskPredictor:
    """孕产妇风险专用预测器"""
    
    def __init__(self, model_dir: str = "models"):
        """
        初始化孕产妇风险预测器
        
        Args:
            model_dir: 模型保存目录
        """
        self.model_dir = model_dir
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            
        # 预测器模型
        self.preeclampsia_model = None  # 子痫前期预测模型
        self.gestational_diabetes_model = None  # 妊娠期糖尿病预测模型
        self.preterm_birth_model = None  # 早产预测模型
        self.general_risk_model = None  # 综合风险评估模型
        
        # 预处理器
        self.scaler = None
        self.label_encoders = {}
        
        # 特征名称
        self.feature_names = []
        
        # 孕产妇特定风险阈值
        self.risk_thresholds = {
            'preeclampsia': {
                'early_pregnancy': {'systolic': 130, 'diastolic': 80},  # 早期妊娠
                'mid_pregnancy': {'systolic': 135, 'diastolic': 85},   # 中期妊娠
                'late_pregnancy': {'systolic': 140, 'diastolic': 90}    # 晚期妊娠
            },
            'gestational_diabetes': {
                'fasting_glucose': 5.1,  # mmol/L
                'ogtt_1h': 10.0,         # mmol/L
                'ogtt_2h': 8.5           # mmol/L
            },
            'preterm_birth': {
                'cervical_length': 25,  # mm
                'fetal_fibronectin': 50  # ng/mL
            }
        }
    
    def load_maternal_data(self, data_path: str = "data/maternal_data.csv") -> pd.DataFrame:
        """
        加载孕产妇数据
        
        Args:
            data_path: 数据文件路径
            
        Returns:
            孕产妇数据DataFrame
        """
        try:
            # 如果是CSV文件
            if data_path.endswith('.csv'):
                df = pd.read_csv(data_path)
            # 如果是JSON文件
            elif data_path.endswith('.json'):
                df = pd.read_json(data_path)
            # 如果是数据库文件
            elif data_path.endswith('.db') or data_path.endswith('.sqlite'):
                import sqlite3
                conn = sqlite3.connect(data_path)
                df = pd.read_sql_query("SELECT * FROM maternal_info", conn)
                conn.close()
            else:
                raise ValueError("不支持的数据格式")
                
            # 数据预处理
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
            if 'last_menstrual_date' in df.columns:
                df['last_menstrual_date'] = pd.to_datetime(df['last_menstrual_date'])
            if 'due_date' in df.columns:
                df['due_date'] = pd.to_datetime(df['due_date'])
                
            return df
            
        except Exception as e:
            print(f"加载孕产妇数据错误: {e}")
            return None
    
    def extract_maternal_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
        """
        提取孕产妇特征
        
        Args:
            df: 孕产妇数据DataFrame
            
        Returns:
            特征数组和特征名称列表
        """
        features = []
        feature_names = []
        
        # 1. 基本特征
        basic_features = ['age', 'height', 'weight', 'bmi', 'parity', 'pregnancy_count']
        for feature in basic_features:
            if feature in df.columns:
                features.append(df[feature].values)
                feature_names.append(feature)
        
        # 2. 孕周相关特征
        if 'gestational_weeks' in df.columns:
            gest_weeks = df['gestational_weeks'].values
            features.append(gest_weeks)
            feature_names.append('gestational_weeks')
            
            # 孕期阶段分类
            pregnancy_stage = np.where(
                gest_weeks < 13, 0,  # 早期妊娠
                np.where(gest_weeks < 28, 1, 2)  # 中期/晚期妊娠
            )
            features.append(pregnancy_stage)
            feature_names.append('pregnancy_stage')
        
        # 3. 生命体征特征
        vital_features = ['systolic_pressure', 'diastolic_pressure', 'heart_rate', 
                         'temperature', 'blood_sugar', 'hemoglobin']
        for feature in vital_features:
            if feature in df.columns:
                features.append(df[feature].values)
                feature_names.append(feature)
        
        # 4. 衍生特征
        if 'systolic_pressure' in df.columns and 'diastolic_pressure' in df.columns:
            # 脉压
            pulse_pressure = df['systolic_pressure'] - df['diastolic_pressure']
            features.append(pulse_pressure.values)
            feature_names.append('pulse_pressure')
            
            # 平均动脉压
            map_pressure = df['diastolic_pressure'] + pulse_pressure / 3
            features.append(map_pressure.values)
            feature_names.append('mean_arterial_pressure')
            
            # 血压分类
            bp_category = np.where(
                (df['systolic_pressure'] >= 140) | (df['diastolic_pressure'] >= 90), 2,  # 高血压
                np.where(
                    (df['systolic_pressure'] >= 130) | (df['diastolic_pressure'] >= 80), 1,  # 正常高值
                    0  # 正常
                )
            )
            features.append(bp_category)
            feature_names.append('bp_category')
        
        # 5. 孕产妇特异性风险因素
        if 'risk_factors' in df.columns:
            # 解析风险因素
            risk_factors = df['risk_factors'].fillna('').astype(str)
            
            # 常见风险因素
            common_risks = ['高血压', '糖尿病', '肥胖', '高龄', '多胎', '既往子痫前期', 
                           '既往妊娠期糖尿病', '吸烟', '家族史']
            
            for risk in common_risks:
                risk_present = risk_factors.str.contains(risk).astype(int).values
                features.append(risk_present)
                feature_names.append(f'risk_{risk}')
        
        # 6. 妊娠类型编码
        if 'pregnancy_type' in df.columns:
            le = LabelEncoder()
            pregnancy_type_encoded = le.fit_transform(df['pregnancy_type'].fillna('单胎'))
            features.append(pregnancy_type_encoded)
            feature_names.append('pregnancy_type_encoded')
            self.label_encoders['pregnancy_type'] = le
        
        # 7. 时间特征
        if 'last_menstrual_date' in df.columns:
            # 季节因素
            lmp_month = pd.to_datetime(df['last_menstrual_date']).dt.month
            features.append(lmp_month.values)
            feature_names.append('lmp_month')
            
            # 季节分类
            season = np.where(
                lmp_month.isin([3, 4, 5]), 0,  # 春季
                np.where(
                    lmp_month.isin([6, 7, 8]), 1,  # 夏季
                    np.where(
                        lmp_month.isin([9, 10, 11]), 2,  # 秋季
                        3  # 冬季
                    )
                )
            )
            features.append(season)
            feature_names.append('conception_season')
        
        # 转换为numpy数组
        X = np.column_stack(features)
        
        # 保存特征名称
        self.feature_names = feature_names
        
        return X, feature_names
    
    def prepare_preeclampsia_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        准备子痫前期预测数据
        
        Args:
            df: 孕产妇数据DataFrame
            
        Returns:
            特征数组和标签数组
        """
        # 提取特征
        X, _ = self.extract_maternal_features(df)
        
        # 创建标签 - 基于血压和尿蛋白
        if 'preeclampsia' in df.columns:
            y = df['preeclampsia'].values
        else:
            # 如果没有标签，基于血压创建伪标签
            systolic = df.get('systolic_pressure', 120)
            diastolic = df.get('diastolic_pressure', 80)
            
            # 根据孕周调整血压阈值
            gest_weeks = df.get('gestational_weeks', 20)
            
            # 早期妊娠阈值较低
            early_mask = gest_weeks < 13
            mid_mask = (gest_weeks >= 13) & (gest_weeks < 28)
            late_mask = gest_weeks >= 28
            
            # 应用不同孕期的阈值
            y = np.zeros(len(df), dtype=int)
            y[early_mask & ((systolic >= 130) | (diastolic >= 80))] = 1
            y[mid_mask & ((systolic >= 135) | (diastolic >= 85))] = 1
            y[late_mask & ((systolic >= 140) | (diastolic >= 90))] = 1
        
        return X, y
    
    def prepare_gestational_diabetes_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        准备妊娠期糖尿病预测数据
        
        Args:
            df: 孕产妇数据DataFrame
            
        Returns:
            特征数组和标签数组
        """
        # 提取特征
        X, _ = self.extract_maternal_features(df)
        
        # 创建标签
        if 'gestational_diabetes' in df.columns:
            y = df['gestational_diabetes'].values
        else:
            # 如果没有标签，基于血糖值创建伪标签
            fasting_glucose = df.get('fasting_glucose', 4.5)
            ogtt_1h = df.get('ogtt_1h', 7.0)
            ogtt_2h = df.get('ogtt_2h', 6.0)
            
            # 根据诊断标准
            y = ((fasting_glucose >= 5.1) | 
                 (ogtt_1h >= 10.0) | 
                 (ogtt_2h >= 8.5)).astype(int)
        
        return X, y
    
    def prepare_preterm_birth_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        准备早产预测数据
        
        Args:
            df: 孕产妇数据DataFrame
            
        Returns:
            特征数组和标签数组
        """
        # 提取特征
        X, _ = self.extract_maternal_features(df)
        
        # 创建标签
        if 'preterm_birth' in df.columns:
            y = df['preterm_birth'].values
        else:
            # 如果没有标签，基于孕周创建伪标签
            gest_weeks = df.get('gestational_weeks', 38)
            y = (gest_weeks < 37).astype(int)
        
        return X, y
    
    def train_preeclampsia_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        训练子痫前期预测模型
        
        Args:
            df: 孕产妇数据DataFrame
            
        Returns:
            训练结果字典
        """
        try:
            print("开始训练子痫前期预测模型...")
            
            # 准备数据
            X, y = self.prepare_preeclampsia_data(df)
            
            # 特征标准化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # 分割数据
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # 处理类别不平衡
            class_weights = compute_class_weight(
                class_weight='balanced',
                classes=np.unique(y_train),
                y=y_train
            )
            class_weight_dict = dict(enumerate(class_weights))
            
            # 训练多个模型并选择最佳
            models = {
                'random_forest': RandomForestClassifier(
                    n_estimators=100, 
                    class_weight=class_weight_dict,
                    random_state=42
                ),
                'gradient_boosting': GradientBoostingClassifier(random_state=42),
                'logistic_regression': LogisticRegression(
                    class_weight=class_weight_dict,
                    random_state=42,
                    max_iter=1000
                )
            }
            
            best_model = None
            best_score = 0
            best_model_name = ""
            
            for name, model in models.items():
                # 交叉验证
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
                mean_score = cv_scores.mean()
                
                print(f"{name} - 交叉验证AUC: {mean_score:.4f}")
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_model = model
                    best_model_name = name
            
            # 训练最佳模型
            best_model.fit(X_train, y_train)
            
            # 评估模型
            y_pred = best_model.predict(X_test)
            y_pred_proba = best_model.predict_proba(X_test)[:, 1]
            
            accuracy = best_model.score(X_test, y_test)
            auc = roc_auc_score(y_test, y_pred_proba)
            
            print(f"最佳模型: {best_model_name}")
            print(f"测试集准确率: {accuracy:.4f}")
            print(f"测试集AUC: {auc:.4f}")
            print("分类报告:")
            print(classification_report(y_test, y_pred))
            
            # 保存模型和预处理器
            self.preeclampsia_model = best_model
            self.scaler = scaler
            
            self.save_model(best_model, 'preeclampsia_model', best_model_name)
            self.save_preprocessor(scaler, 'preeclampsia_scaler')
            
            return {
                'model_name': best_model_name,
                'accuracy': accuracy,
                'auc': auc,
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
            
        except Exception as e:
            print(f"子痫前期模型训练错误: {e}")
            return None
    
    def train_gestational_diabetes_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        训练妊娠期糖尿病预测模型
        
        Args:
            df: 孕产妇数据DataFrame
            
        Returns:
            训练结果字典
        """
        try:
            print("开始训练妊娠期糖尿病预测模型...")
            
            # 准备数据
            X, y = self.prepare_gestational_diabetes_data(df)
            
            # 特征标准化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # 分割数据
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # 处理类别不平衡
            class_weights = compute_class_weight(
                class_weight='balanced',
                classes=np.unique(y_train),
                y=y_train
            )
            class_weight_dict = dict(enumerate(class_weights))
            
            # 训练多个模型并选择最佳
            models = {
                'random_forest': RandomForestClassifier(
                    n_estimators=100, 
                    class_weight=class_weight_dict,
                    random_state=42
                ),
                'gradient_boosting': GradientBoostingClassifier(random_state=42),
                'logistic_regression': LogisticRegression(
                    class_weight=class_weight_dict,
                    random_state=42,
                    max_iter=1000
                )
            }
            
            best_model = None
            best_score = 0
            best_model_name = ""
            
            for name, model in models.items():
                # 交叉验证
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
                mean_score = cv_scores.mean()
                
                print(f"{name} - 交叉验证AUC: {mean_score:.4f}")
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_model = model
                    best_model_name = name
            
            # 训练最佳模型
            best_model.fit(X_train, y_train)
            
            # 评估模型
            y_pred = best_model.predict(X_test)
            y_pred_proba = best_model.predict_proba(X_test)[:, 1]
            
            accuracy = best_model.score(X_test, y_test)
            auc = roc_auc_score(y_test, y_pred_proba)
            
            print(f"最佳模型: {best_model_name}")
            print(f"测试集准确率: {accuracy:.4f}")
            print(f"测试集AUC: {auc:.4f}")
            print("分类报告:")
            print(classification_report(y_test, y_pred))
            
            # 保存模型和预处理器
            self.gestational_diabetes_model = best_model
            
            self.save_model(best_model, 'gestational_diabetes_model', best_model_name)
            
            return {
                'model_name': best_model_name,
                'accuracy': accuracy,
                'auc': auc,
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
            
        except Exception as e:
            print(f"妊娠期糖尿病模型训练错误: {e}")
            return None
    
    def train_preterm_birth_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        训练早产预测模型
        
        Args:
            df: 孕产妇数据DataFrame
            
        Returns:
            训练结果字典
        """
        try:
            print("开始训练早产预测模型...")
            
            # 准备数据
            X, y = self.prepare_preterm_birth_data(df)
            
            # 特征标准化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # 分割数据
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # 处理类别不平衡
            class_weights = compute_class_weight(
                class_weight='balanced',
                classes=np.unique(y_train),
                y=y_train
            )
            class_weight_dict = dict(enumerate(class_weights))
            
            # 训练多个模型并选择最佳
            models = {
                'random_forest': RandomForestClassifier(
                    n_estimators=100, 
                    class_weight=class_weight_dict,
                    random_state=42
                ),
                'gradient_boosting': GradientBoostingClassifier(random_state=42),
                'logistic_regression': LogisticRegression(
                    class_weight=class_weight_dict,
                    random_state=42,
                    max_iter=1000
                )
            }
            
            best_model = None
            best_score = 0
            best_model_name = ""
            
            for name, model in models.items():
                # 交叉验证
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
                mean_score = cv_scores.mean()
                
                print(f"{name} - 交叉验证AUC: {mean_score:.4f}")
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_model = model
                    best_model_name = name
            
            # 训练最佳模型
            best_model.fit(X_train, y_train)
            
            # 评估模型
            y_pred = best_model.predict(X_test)
            y_pred_proba = best_model.predict_proba(X_test)[:, 1]
            
            accuracy = best_model.score(X_test, y_test)
            auc = roc_auc_score(y_test, y_pred_proba)
            
            print(f"最佳模型: {best_model_name}")
            print(f"测试集准确率: {accuracy:.4f}")
            print(f"测试集AUC: {auc:.4f}")
            print("分类报告:")
            print(classification_report(y_test, y_pred))
            
            # 保存模型和预处理器
            self.preterm_birth_model = best_model
            
            self.save_model(best_model, 'preterm_birth_model', best_model_name)
            
            return {
                'model_name': best_model_name,
                'accuracy': accuracy,
                'auc': auc,
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
            
        except Exception as e:
            print(f"早产模型训练错误: {e}")
            return None
    
    def predict_preeclampsia_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        预测子痫前期风险
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            预测结果字典
        """
        try:
            # 加载模型和预处理器
            if self.preeclampsia_model is None:
                self.preeclampsia_model = self.load_model('preeclampsia_model')
                self.scaler = self.load_preprocessor('preeclampsia_scaler')
            
            if self.preeclampsia_model is None or self.scaler is None:
                return None
            
            # 准备特征
            df = pd.DataFrame([patient_data])
            X, _ = self.extract_maternal_features(df)
            
            # 标准化特征
            X_scaled = self.scaler.transform(X)
            
            # 预测
            if hasattr(self.preeclampsia_model, 'predict_proba'):
                probabilities = self.preeclampsia_model.predict_proba(X_scaled)[0]
                prediction = self.preeclampsia_model.predict(X_scaled)[0]
            else:
                # 神经网络
                predictions = self.preeclampsia_model.predict(X_scaled)[0]
                probabilities = predictions
                prediction = np.argmax(predictions)
            
            # 获取特征重要性
            if hasattr(self.preeclampsia_model, 'feature_importances_'):
                feature_importance = self.preeclampsia_model.feature_importances_
                top_features_idx = np.argsort(feature_importance)[-5:][::-1]
                top_features = [
                    {
                        'name': self.feature_names[i],
                        'importance': float(feature_importance[i]),
                        'value': float(patient_data.get(self.feature_names[i], 0))
                    }
                    for i in top_features_idx
                ]
            else:
                top_features = []
            
            # 创建结果
            result = {
                'risk_type': '子痫前期',
                'risk_level': '高风险' if prediction == 1 else '低风险',
                'risk_probability': float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0]),
                'top_risk_factors': top_features,
                'recommendations': self.get_preeclampsia_recommendations(prediction, probabilities[1] if len(probabilities) > 1 else probabilities[0])
            }
            
            return result
            
        except Exception as e:
            print(f"子痫前期风险预测错误: {e}")
            return None
    
    def predict_gestational_diabetes_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        预测妊娠期糖尿病风险
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            预测结果字典
        """
        try:
            # 加载模型
            if self.gestational_diabetes_model is None:
                self.gestational_diabetes_model = self.load_model('gestational_diabetes_model')
            
            if self.gestational_diabetes_model is None:
                return None
            
            # 准备特征
            df = pd.DataFrame([patient_data])
            X, _ = self.extract_maternal_features(df)
            
            # 标准化特征
            if self.scaler is None:
                self.scaler = self.load_preprocessor('preeclampsia_scaler')
            X_scaled = self.scaler.transform(X)
            
            # 预测
            if hasattr(self.gestational_diabetes_model, 'predict_proba'):
                probabilities = self.gestational_diabetes_model.predict_proba(X_scaled)[0]
                prediction = self.gestational_diabetes_model.predict(X_scaled)[0]
            else:
                # 神经网络
                predictions = self.gestational_diabetes_model.predict(X_scaled)[0]
                probabilities = predictions
                prediction = np.argmax(predictions)
            
            # 获取特征重要性
            if hasattr(self.gestational_diabetes_model, 'feature_importances_'):
                feature_importance = self.gestational_diabetes_model.feature_importances_
                top_features_idx = np.argsort(feature_importance)[-5:][::-1]
                top_features = [
                    {
                        'name': self.feature_names[i],
                        'importance': float(feature_importance[i]),
                        'value': float(patient_data.get(self.feature_names[i], 0))
                    }
                    for i in top_features_idx
                ]
            else:
                top_features = []
            
            # 创建结果
            result = {
                'risk_type': '妊娠期糖尿病',
                'risk_level': '高风险' if prediction == 1 else '低风险',
                'risk_probability': float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0]),
                'top_risk_factors': top_features,
                'recommendations': self.get_gestational_diabetes_recommendations(prediction, probabilities[1] if len(probabilities) > 1 else probabilities[0])
            }
            
            return result
            
        except Exception as e:
            print(f"妊娠期糖尿病风险预测错误: {e}")
            return None
    
    def predict_preterm_birth_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        预测早产风险
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            预测结果字典
        """
        try:
            # 加载模型
            if self.preterm_birth_model is None:
                self.preterm_birth_model = self.load_model('preterm_birth_model')
            
            if self.preterm_birth_model is None:
                return None
            
            # 准备特征
            df = pd.DataFrame([patient_data])
            X, _ = self.extract_maternal_features(df)
            
            # 标准化特征
            if self.scaler is None:
                self.scaler = self.load_preprocessor('preeclampsia_scaler')
            X_scaled = self.scaler.transform(X)
            
            # 预测
            if hasattr(self.preterm_birth_model, 'predict_proba'):
                probabilities = self.preterm_birth_model.predict_proba(X_scaled)[0]
                prediction = self.preterm_birth_model.predict(X_scaled)[0]
            else:
                # 神经网络
                predictions = self.preterm_birth_model.predict(X_scaled)[0]
                probabilities = predictions
                prediction = np.argmax(predictions)
            
            # 获取特征重要性
            if hasattr(self.preterm_birth_model, 'feature_importances_'):
                feature_importance = self.preterm_birth_model.feature_importances_
                top_features_idx = np.argsort(feature_importance)[-5:][::-1]
                top_features = [
                    {
                        'name': self.feature_names[i],
                        'importance': float(feature_importance[i]),
                        'value': float(patient_data.get(self.feature_names[i], 0))
                    }
                    for i in top_features_idx
                ]
            else:
                top_features = []
            
            # 创建结果
            result = {
                'risk_type': '早产',
                'risk_level': '高风险' if prediction == 1 else '低风险',
                'risk_probability': float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0]),
                'top_risk_factors': top_features,
                'recommendations': self.get_preterm_birth_recommendations(prediction, probabilities[1] if len(probabilities) > 1 else probabilities[0])
            }
            
            return result
            
        except Exception as e:
            print(f"早产风险预测错误: {e}")
            return None
    
    def predict_comprehensive_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合风险评估
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            综合风险预测结果字典
        """
        try:
            # 预测各类风险
            preeclampsia_result = self.predict_preeclampsia_risk(patient_data)
            gestational_diabetes_result = self.predict_gestational_diabetes_risk(patient_data)
            preterm_birth_result = self.predict_preterm_birth_risk(patient_data)
            
            # 计算综合风险评分
            risk_scores = []
            risk_factors = []
            
            if preeclampsia_result:
                risk_scores.append(preeclampsia_result['risk_probability'])
                risk_factors.extend(preeclampsia_result['top_risk_factors'])
            
            if gestational_diabetes_result:
                risk_scores.append(gestational_diabetes_result['risk_probability'])
                risk_factors.extend(gestational_diabetes_result['top_risk_factors'])
            
            if preterm_birth_result:
                risk_scores.append(preterm_birth_result['risk_probability'])
                risk_factors.extend(preterm_birth_result['top_risk_factors'])
            
            # 计算平均风险
            if risk_scores:
                overall_risk = np.mean(risk_scores)
            else:
                overall_risk = 0.0
            
            # 确定风险等级
            if overall_risk >= 0.7:
                risk_level = '高风险'
            elif overall_risk >= 0.4:
                risk_level = '中风险'
            else:
                risk_level = '低风险'
            
            # 合并风险因素（去重）
            unique_factors = {}
            for factor in risk_factors:
                name = factor['name']
                if name not in unique_factors or factor['importance'] > unique_factors[name]['importance']:
                    unique_factors[name] = factor
            
            # 按重要性排序
            sorted_factors = sorted(unique_factors.values(), key=lambda x: x['importance'], reverse=True)[:5]
            
            # 创建综合结果
            result = {
                'overall_risk_level': risk_level,
                'overall_risk_score': float(overall_risk),
                'individual_risks': {
                    'preeclampsia': preeclampsia_result,
                    'gestational_diabetes': gestational_diabetes_result,
                    'preterm_birth': preterm_birth_result
                },
                'top_risk_factors': sorted_factors,
                'recommendations': self.get_comprehensive_recommendations(risk_level, overall_risk)
            }
            
            return result
            
        except Exception as e:
            print(f"综合风险评估错误: {e}")
            return None
    
    def get_preeclampsia_recommendations(self, prediction: int, probability: float) -> List[str]:
        """
        获取子痫前期预防建议
        
        Args:
            prediction: 预测结果 (0: 低风险, 1: 高风险)
            probability: 风险概率
            
        Returns:
            建议列表
        """
        if prediction == 1 or probability > 0.5:
            return [
                "增加产检频率，每周监测血压",
                "低盐饮食，每日盐摄入量不超过5克",
                "保证充足休息，每天至少8小时睡眠",
                "每日监测尿蛋白，注意水肿情况",
                "遵医嘱服用降压药物或钙剂",
                "避免过度劳累和精神紧张"
            ]
        else:
            return [
                "保持规律产检，每2-4周检查一次",
                "均衡饮食，控制体重增长",
                "适度运动，如散步、孕妇瑜伽",
                "注意休息，避免过度劳累",
                "自我监测血压变化，如有异常及时就医"
            ]
    
    def get_gestational_diabetes_recommendations(self, prediction: int, probability: float) -> List[str]:
        """
        获取妊娠期糖尿病预防建议
        
        Args:
            prediction: 预测结果 (0: 低风险, 1: 高风险)
            probability: 风险概率
            
        Returns:
            建议列表
        """
        if prediction == 1 or probability > 0.5:
            return [
                "控制碳水化合物摄入，选择低GI食物",
                "少食多餐，每日5-6餐",
                "餐后30分钟适度运动",
                "定期监测血糖，空腹和餐后2小时",
                "必要时遵医嘱使用胰岛素",
                "增加膳食纤维摄入，多吃蔬菜"
            ]
        else:
            return [
                "均衡饮食，控制糖分摄入",
                "保持适当体重增长",
                "规律运动，每周至少150分钟中等强度运动",
                "定期进行血糖筛查",
                "避免高糖高脂食物",
                "保证充足睡眠"
            ]
    
    def get_preterm_birth_recommendations(self, prediction: int, probability: float) -> List[str]:
        """
        获取早产预防建议
        
        Args:
            prediction: 预测结果 (0: 低风险, 1: 高风险)
            probability: 风险概率
            
        Returns:
            建议列表
        """
        if prediction == 1 or probability > 0.5:
            return [
                "卧床休息，避免剧烈活动",
                "禁止性生活",
                "定期监测宫颈长度",
                "遵医嘱使用宫缩抑制剂",
                "注意观察宫缩频率和强度",
                "避免精神刺激和情绪波动"
            ]
        else:
            return [
                "避免过度劳累和重体力活动",
                "注意个人卫生，预防感染",
                "保持情绪稳定，避免压力",
                "规律产检，监测宫颈情况",
                "注意腹痛、阴道流血等早产征兆",
                "健康饮食，戒烟戒酒"
            ]
    
    def get_comprehensive_recommendations(self, risk_level: str, risk_score: float) -> List[str]:
        """
        获取综合风险预防建议
        
        Args:
            risk_level: 风险等级
            risk_score: 风险评分
            
        Returns:
            建议列表
        """
        if risk_level == '高风险':
            return [
                "增加产检频率，每周一次",
                "严格遵医嘱进行治疗和监测",
                "卧床休息，避免一切可能诱发早产的因素",
                "家庭成员密切观察孕妇情况",
                "随时做好住院准备",
                "保持24小时联系方式畅通"
            ]
        elif risk_level == '中风险':
            return [
                "每1-2周进行一次产检",
                "注意监测各项生理指标变化",
                "调整生活方式，减少风险因素",
                "遵医嘱进行必要的检查和治疗",
                "注意休息，避免过度劳累",
                "学习识别异常征兆的知识"
            ]
        else:
            return [
                "保持规律产检，每4周一次",
                "健康饮食，适度运动",
                "保持良好心态，避免焦虑",
                "学习孕期保健知识",
                "注意个人卫生，预防感染",
                "为分娩做好准备"
            ]
    
    def save_model(self, model, model_name: str, model_type: str):
        """
        保存模型
        
        Args:
            model: 模型对象
            model_name: 模型名称
            model_type: 模型类型
        """
        try:
            if model_type == 'neural_network':
                model_path = os.path.join(self.model_dir, f"{model_name}.h5")
                model.save(model_path)
            else:
                model_path = os.path.join(self.model_dir, f"{model_name}.joblib")
                joblib.dump(model, model_path)
            
            # 保存模型类型信息
            info_path = os.path.join(self.model_dir, f"{model_name}_info.json")
            with open(info_path, 'w') as f:
                json.dump({'type': model_type}, f)
                
        except Exception as e:
            print(f"模型保存错误: {e}")
    
    def load_model(self, model_name: str):
        """
        加载模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            加载的模型对象
        """
        try:
            info_path = os.path.join(self.model_dir, f"{model_name}_info.json")
            if not os.path.exists(info_path):
                return None
            
            with open(info_path, 'r') as f:
                info = json.load(f)
            
            model_type = info['type']
            
            if model_type == 'neural_network':
                model_path = os.path.join(self.model_dir, f"{model_name}.h5")
                if os.path.exists(model_path):
                    return load_model(model_path)
            else:
                model_path = os.path.join(self.model_dir, f"{model_name}.joblib")
                if os.path.exists(model_path):
                    return joblib.load(model_path)
            
            return None
            
        except Exception as e:
            print(f"模型加载错误: {e}")
            return None
    
    def save_preprocessor(self, preprocessor, name: str):
        """
        保存预处理器
        
        Args:
            preprocessor: 预处理器对象
            name: 预处理器名称
        """
        try:
            path = os.path.join(self.model_dir, f"{name}.joblib")
            joblib.dump(preprocessor, path)
        except Exception as e:
            print(f"预处理器保存错误: {e}")
    
    def load_preprocessor(self, name: str):
        """
        加载预处理器
        
        Args:
            name: 预处理器名称
            
        Returns:
            加载的预处理器对象
        """
        try:
            path = os.path.join(self.model_dir, f"{name}.joblib")
            if os.path.exists(path):
                return joblib.load(path)
            return None
        except Exception as e:
            print(f"预处理器加载错误: {e}")
            return None
    
    def train_all_models(self, data_path: str = "data/maternal_data.csv") -> Dict[str, Any]:
        """
        训练所有孕产妇风险预测模型
        
        Args:
            data_path: 数据文件路径
            
        Returns:
            所有模型的训练结果
        """
        print("开始训练所有孕产妇风险预测模型...")
        
        # 加载数据
        df = self.load_maternal_data(data_path)
        if df is None:
            print("无法加载数据，训练终止")
            return None
        
        results = {}
        
        # 训练子痫前期模型
        preeclampsia_result = self.train_preeclampsia_model(df)
        results['preeclampsia'] = preeclampsia_result
        
        # 训练妊娠期糖尿病模型
        gestational_diabetes_result = self.train_gestational_diabetes_model(df)
        results['gestational_diabetes'] = gestational_diabetes_result
        
        # 训练早产模型
        preterm_birth_result = self.train_preterm_birth_model(df)
        results['preterm_birth'] = preterm_birth_result
        
        print("所有孕产妇风险预测模型训练完成！")
        return results


# 使用示例
if __name__ == "__main__":
    # 创建预测器
    predictor = MaternalRiskPredictor()
    
    # 训练所有模型
    results = predictor.train_all_models()
    
    # 示例患者数据
    patient_data = {
        'age': 32,
        'height': 165,
        'weight': 70,
        'gestational_weeks': 28,
        'parity': 1,
        'pregnancy_count': 2,
        'systolic_pressure': 135,
        'diastolic_pressure': 85,
        'blood_sugar': 6.5,
        'pregnancy_type': '单胎',
        'risk_factors': '高龄,肥胖'
    }
    
    # 预测综合风险
    risk_result = predictor.predict_comprehensive_risk(patient_data)
    print("综合风险评估结果:")
    print(json.dumps(risk_result, indent=2, ensure_ascii=False))
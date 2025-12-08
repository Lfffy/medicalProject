"""
模型训练和评估模块
为孕产妇健康风险预测提供专业的模型训练功能
"""

import numpy as np
import pandas as pd
import os
import json
import joblib
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union

# 机器学习模型
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    precision_recall_curve, roc_curve
)
from sklearn.model_selection import (
    train_test_split, cross_val_score, StratifiedKFold,
    GridSearchCV, RandomizedSearchCV
)
from sklearn.preprocessing import LabelEncoder

# 尝试导入XGBoost和LightGBM
try:
    import xgboost as xgb
    has_xgboost = True
except ImportError:
    has_xgboost = False
    print("警告: XGBoost未安装")

try:
    import lightgbm as lgb
    has_lightgbm = True
except ImportError:
    has_lightgbm = False
    print("警告: LightGBM未安装")

from data_preprocessing import MaternalDataPreprocessor

class MaternalRiskModelTrainer:
    """
    孕产妇风险预测模型训练器
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化模型训练器
        
        Args:
            config_path: 配置文件路径
        """
        # 配置参数
        self.config = self._load_config(config_path)
        
        # 模型存储
        self.models = {}
        self.best_models = {}
        self.model_history = {}
        
        # 性能指标
        self.performance_metrics = {}
        
        # 数据预处理器
        self.preprocessor = None
        
        # 目标变量映射
        self.target_mappers = {}
        
        # 初始化
        self._initialize()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        default_config = {
            'test_size': 0.2,
            'random_state': 42,
            'cv_folds': 5,
            'scoring': 'roc_auc',
            'hyperparameter_search': 'grid',  # 'grid', 'random', 'none'
            'n_iter_random_search': 50,
            'performance_thresholds': {
                'accuracy': 0.75,
                'recall': 0.70,  # 对风险预测，召回率更重要
                'precision': 0.60,
                'f1_score': 0.70,
                'roc_auc': 0.80
            },
            'models_to_train': ['random_forest', 'logistic_regression', 'gradient_boosting'],
            'use_ensemble': True,
            'ensemble_method': 'majority_vote',  # 'majority_vote', 'weighted_average'
            'model_params': {
                'random_forest': {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4],
                    'class_weight': ['balanced']
                },
                'logistic_regression': {
                    'C': [0.01, 0.1, 1.0, 10.0],
                    'solver': ['liblinear', 'lbfgs'],
                    'class_weight': ['balanced']
                },
                'gradient_boosting': {
                    'n_estimators': [100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                }
            }
        }
        
        # 如果XGBoost可用，添加其参数
        if has_xgboost:
            default_config['model_params']['xgboost'] = {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0],
                'scale_pos_weight': [1, 10, 20]
            }
        
        # 如果LightGBM可用，添加其参数
        if has_lightgbm:
            default_config['model_params']['lightgbm'] = {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0],
                'class_weight': ['balanced']
            }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    return self._merge_configs(default_config, user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并默认配置和用户配置
        
        Args:
            default: 默认配置
            user: 用户配置
            
        Returns:
            合并后的配置
        """
        merged = default.copy()
        
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # 递归合并嵌套字典
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def _initialize(self):
        """
        初始化训练器
        """
        # 初始化数据预处理器
        self.preprocessor = MaternalDataPreprocessor()
    
    def load_data(self, file_path: str, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        加载训练数据
        
        Args:
            file_path: 数据文件路径
            target_column: 目标列名称
            
        Returns:
            (特征数据, 目标数据)
        """
        try:
            # 支持多种文件格式
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path, encoding='utf-8')
            else:
                raise ValueError(f"不支持的文件格式: {file_path}")
            
            print(f"成功加载数据: {len(df)} 行")
            
            # 检查目标列是否存在
            if target_column not in df.columns:
                raise ValueError(f"目标列 '{target_column}' 不存在")
            
            # 分离特征和目标
            X = df.drop(columns=[target_column])
            y = df[target_column]
            
            # 处理分类目标变量
            if y.dtype == 'object' or y.nunique() < len(y) // 10:
                # 编码目标变量
                le = LabelEncoder()
                y_encoded = le.fit_transform(y)
                self.target_mappers[target_column] = le
                return X, y_encoded
            
            return X, y
        
        except Exception as e:
            print(f"加载数据失败: {e}")
            raise
    
    def create_model(self, model_name: str) -> Any:
        """
        创建指定的模型
        
        Args:
            model_name: 模型名称
            
        Returns:
            模型对象
        """
        models = {
            'random_forest': RandomForestClassifier(random_state=self.config['random_state']),
            'logistic_regression': LogisticRegression(random_state=self.config['random_state']),
            'gradient_boosting': GradientBoostingClassifier(random_state=self.config['random_state']),
            'decision_tree': DecisionTreeClassifier(random_state=self.config['random_state']),
            'svm': SVC(probability=True, random_state=self.config['random_state']),
            'knn': KNeighborsClassifier()
        }
        
        # 添加XGBoost模型
        if has_xgboost:
            models['xgboost'] = xgb.XGBClassifier(random_state=self.config['random_state'])
        
        # 添加LightGBM模型
        if has_lightgbm:
            models['lightgbm'] = lgb.LGBMClassifier(random_state=self.config['random_state'])
        
        if model_name not in models:
            raise ValueError(f"不支持的模型: {model_name}")
        
        return models[model_name]
    
    def train_single_model(self, model_name: str, X: np.ndarray, y: np.ndarray) -> Tuple[Any, Dict[str, float]]:
        """
        训练单个模型
        
        Args:
            model_name: 模型名称
            X: 特征数据
            y: 目标数据
            
        Returns:
            (训练好的模型, 评估指标)
        """
        print(f"\n开始训练模型: {model_name}")
        
        # 创建模型
        model = self.create_model(model_name)
        
        # 分割训练集和验证集
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, 
            test_size=self.config['test_size'],
            random_state=self.config['random_state'],
            stratify=y if len(np.unique(y)) > 1 else None
        )
        
        # 超参数搜索
        if self.config['hyperparameter_search'] != 'none' and model_name in self.config['model_params']:
            params = self.config['model_params'][model_name]
            
            if self.config['hyperparameter_search'] == 'grid':
                search = GridSearchCV(
                    model,
                    params,
                    cv=StratifiedKFold(n_splits=self.config['cv_folds'], shuffle=True, random_state=self.config['random_state']),
                    scoring=self.config['scoring'],
                    n_jobs=-1,
                    verbose=1
                )
            else:  # random search
                search = RandomizedSearchCV(
                    model,
                    params,
                    n_iter=self.config['n_iter_random_search'],
                    cv=StratifiedKFold(n_splits=self.config['cv_folds'], shuffle=True, random_state=self.config['random_state']),
                    scoring=self.config['scoring'],
                    n_jobs=-1,
                    random_state=self.config['random_state'],
                    verbose=1
                )
            
            # 执行搜索
            search.fit(X_train, y_train)
            best_model = search.best_estimator_
            print(f"最佳参数: {search.best_params_}")
            print(f"最佳交叉验证分数: {search.best_score_:.4f}")
        else:
            # 直接训练模型
            best_model = model
            best_model.fit(X_train, y_train)
            
            # 交叉验证
            cv_scores = cross_val_score(
                best_model,
                X_train,
                y_train,
                cv=StratifiedKFold(n_splits=self.config['cv_folds'], shuffle=True, random_state=self.config['random_state']),
                scoring=self.config['scoring'],
                n_jobs=-1
            )
            print(f"交叉验证分数: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        
        # 在验证集上评估
        metrics = self.evaluate_model(best_model, X_val, y_val)
        print(f"验证集性能:")
        for metric_name, value in metrics.items():
            print(f"  {metric_name}: {value:.4f}")
        
        # 检查是否达到性能阈值
        meets_thresholds = self._check_performance_thresholds(metrics)
        print(f"模型是否达到性能阈值: {meets_thresholds}")
        
        return best_model, metrics
    
    def evaluate_model(self, model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        评估模型性能
        
        Args:
            model: 模型对象
            X: 特征数据
            y: 目标数据
            
        Returns:
            性能指标字典
        """
        # 预测
        y_pred = model.predict(X)
        y_pred_proba = model.predict_proba(X)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # 计算基本指标
        metrics = {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, average='weighted' if len(np.unique(y)) > 2 else 'binary', zero_division=0),
            'recall': recall_score(y, y_pred, average='weighted' if len(np.unique(y)) > 2 else 'binary', zero_division=0),
            'f1_score': f1_score(y, y_pred, average='weighted' if len(np.unique(y)) > 2 else 'binary', zero_division=0)
        }
        
        # 计算ROC AUC（如果可能）
        if y_pred_proba is not None and len(np.unique(y)) > 1:
            try:
                metrics['roc_auc'] = roc_auc_score(y, y_pred_proba, average='weighted' if len(np.unique(y)) > 2 else 'macro')
            except ValueError:
                metrics['roc_auc'] = 0.0
        else:
            metrics['roc_auc'] = 0.0
        
        return metrics
    
    def _check_performance_thresholds(self, metrics: Dict[str, float]) -> bool:
        """
        检查模型性能是否达到阈值
        
        Args:
            metrics: 性能指标字典
            
        Returns:
            是否达到阈值
        """
        thresholds = self.config['performance_thresholds']
        
        # 对每个阈值进行检查
        for metric_name, threshold in thresholds.items():
            if metric_name in metrics and metrics[metric_name] < threshold:
                print(f"警告: {metric_name} ({metrics[metric_name]:.4f}) 低于阈值 ({threshold})")
                # 对于风险预测，召回率是关键指标，必须满足
                if metric_name == 'recall' or metric_name == 'roc_auc':
                    return False
        
        return True
    
    def train_all_models(self, X: np.ndarray, y: np.ndarray, model_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        训练所有指定的模型
        
        Args:
            X: 特征数据
            y: 目标数据
            model_names: 要训练的模型名称列表，如果为None则使用配置中的列表
            
        Returns:
            训练结果字典
        """
        # 使用配置中的模型列表或传入的列表
        if model_names is None:
            model_names = self.config['models_to_train']
        
        results = {
            'models': {},
            'metrics': {},
            'best_model_name': None,
            'best_model': None
        }
        
        best_score = -1
        best_model_name = None
        
        # 训练每个模型
        for model_name in model_names:
            try:
                print(f"\n===== 训练模型: {model_name} =====")
                model, metrics = self.train_single_model(model_name, X, y)
                
                # 保存模型和指标
                self.models[model_name] = model
                self.performance_metrics[model_name] = metrics
                
                results['models'][model_name] = model
                results['metrics'][model_name] = metrics
                
                # 更新最佳模型（使用ROC AUC作为主要指标）
                current_score = metrics.get('roc_auc', 0)
                if current_score > best_score:
                    best_score = current_score
                    best_model_name = model_name
                    self.best_models[model_name.split('_')[0]] = model  # 按风险类型保存最佳模型
                
                # 记录训练历史
                self.model_history[model_name] = {
                    'timestamp': datetime.now().isoformat(),
                    'metrics': metrics,
                    'config': self.config,
                    'data_shape': X.shape
                }
                
            except Exception as e:
                print(f"训练模型 {model_name} 失败: {e}")
        
        # 设置最佳模型
        if best_model_name:
            results['best_model_name'] = best_model_name
            results['best_model'] = results['models'][best_model_name]
            print(f"\n最佳模型: {best_model_name} (ROC AUC: {best_score:.4f})")
        
        return results
    
    def train_risk_specific_models(self, data_path: str, risk_types: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        训练特定风险类型的模型
        
        Args:
            data_path: 数据目录路径
            risk_types: 风险类型列表，如 ['preeclampsia', 'gestational_diabetes', 'preterm_birth']
            
        Returns:
            各风险类型的训练结果
        """
        all_results = {}
        
        # 训练每种风险类型的模型
        for risk_type in risk_types:
            print(f"\n========== 训练 {risk_type} 风险预测模型 ==========")
            
            # 构建数据文件路径
            file_name = f"{risk_type}_training_data.csv"
            file_path = os.path.join(data_path, file_name)
            
            if not os.path.exists(file_path):
                print(f"警告: 未找到 {risk_type} 的训练数据文件: {file_path}")
                # 尝试查找其他可能的文件名
                alternative_files = []
                for f in os.listdir(data_path):
                    if risk_type in f and (f.endswith('.csv') or f.endswith('.xlsx') or f.endswith('.json')):
                        alternative_files.append(f)
                
                if alternative_files:
                    file_path = os.path.join(data_path, alternative_files[0])
                    print(f"使用替代文件: {file_path}")
                else:
                    print(f"跳过 {risk_type} 模型训练")
                    continue
            
            try:
                # 加载数据
                X, y = self.load_data(file_path, f'{risk_type}_label')
                
                # 使用预处理器转换数据
                X_transformed, feature_names = self.preprocessor.fit_transform(X)
                
                # 训练所有模型
                results = self.train_all_models(X_transformed, y)
                
                # 保存结果
                all_results[risk_type] = {
                    'results': results,
                    'feature_names': feature_names,
                    'n_samples': len(y)
                }
                
                print(f"{risk_type} 模型训练完成")
                
            except Exception as e:
                print(f"训练 {risk_type} 模型失败: {e}")
                all_results[risk_type] = {'error': str(e)}
        
        return all_results
    
    def create_ensemble_model(self, models: Dict[str, Any], method: str = 'majority_vote') -> Any:
        """
        创建集成模型
        
        Args:
            models: 模型字典
            method: 集成方法 ('majority_vote', 'weighted_average')
            
        Returns:
            集成模型对象
        """
        class EnsembleModel:
            def __init__(self, models, method, weights=None):
                self.models = models
                self.method = method
                self.weights = weights if weights else {name: 1.0 for name in models.keys()}
                
                # 归一化权重
                total_weight = sum(self.weights.values())
                self.normalized_weights = {name: w/total_weight for name, w in self.weights.items()}
            
            def predict(self, X):
                predictions = {name: model.predict(X) for name, model in self.models.items()}
                
                if self.method == 'majority_vote':
                    # 多数投票
                    all_preds = np.array([pred for pred in predictions.values()])
                    return np.apply_along_axis(lambda x: np.bincount(x.astype(int)).argmax(), axis=0, arr=all_preds)
                else:
                    # 使用概率预测的加权平均
                    probas = {name: model.predict_proba(X) for name, model in self.models.items()}
                    avg_probas = np.zeros_like(next(iter(probas.values())))
                    
                    for name, prob in probas.items():
                        avg_probas += prob * self.normalized_weights[name]
                    
                    return np.argmax(avg_probas, axis=1)
            
            def predict_proba(self, X):
                probas = {name: model.predict_proba(X) for name, model in self.models.items()}
                avg_probas = np.zeros_like(next(iter(probas.values())))
                
                for name, prob in probas.items():
                    avg_probas += prob * self.normalized_weights[name]
                
                return avg_probas
        
        # 如果是加权平均，使用模型性能作为权重
        weights = None
        if method == 'weighted_average':
            weights = {}
            for name, model in models.items():
                if name in self.performance_metrics:
                    # 使用ROC AUC作为权重
                    weights[name] = self.performance_metrics[name].get('roc_auc', 0.5)
                else:
                    weights[name] = 0.5
        
        return EnsembleModel(models, method, weights)
    
    def generate_performance_report(self, risk_type: str) -> Dict[str, Any]:
        """
        生成性能报告
        
        Args:
            risk_type: 风险类型
            
        Returns:
            性能报告字典
        """
        report = {
            'risk_type': risk_type,
            'timestamp': datetime.now().isoformat(),
            'models': {},
            'thresholds': self.config['performance_thresholds']
        }
        
        # 收集每个模型的性能
        for model_name, metrics in self.performance_metrics.items():
            report['models'][model_name] = {
                'metrics': metrics,
                'meets_thresholds': self._check_performance_thresholds(metrics)
            }
        
        # 添加最佳模型信息
        if risk_type in self.best_models:
            # 找到对应的模型名称
            best_model_name = None
            for name, model in self.models.items():
                if model == self.best_models[risk_type]:
                    best_model_name = name
                    break
            
            if best_model_name and best_model_name in self.performance_metrics:
                report['best_model'] = {
                    'name': best_model_name,
                    'metrics': self.performance_metrics[best_model_name]
                }
        
        return report
    
    def save_models(self, directory: str):
        """
        保存模型和相关信息
        
        Args:
            directory: 保存目录
        """
        # 创建目录
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # 保存每个模型
        for name, model in self.models.items():
            try:
                path = os.path.join(directory, f'{name}.joblib')
                joblib.dump(model, path)
                print(f"保存模型 {name} 到 {path}")
            except Exception as e:
                print(f"保存模型 {name} 失败: {e}")
        
        # 保存最佳模型
        for risk_type, model in self.best_models.items():
            try:
                path = os.path.join(directory, f'best_{risk_type}.joblib')
                joblib.dump(model, path)
                print(f"保存最佳 {risk_type} 模型到 {path}")
            except Exception as e:
                print(f"保存最佳 {risk_type} 模型失败: {e}")
        
        # 保存预处理器
        self.preprocessor.save_preprocessors(os.path.join(directory, 'preprocessor'))
        
        # 保存配置和性能指标
        metadata = {
            'config': self.config,
            'performance_metrics': self.performance_metrics,
            'model_history': self.model_history,
            'target_mappers': {k: {'classes': v.classes_.tolist()} for k, v in self.target_mappers.items()},
            'save_time': datetime.now().isoformat(),
            'model_version': self._generate_model_version()
        }
        
        try:
            with open(os.path.join(directory, 'model_metadata.json'), 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            print("保存模型元数据成功")
        except Exception as e:
            print(f"保存模型元数据失败: {e}")
    
    def _generate_model_version(self) -> str:
        """
        生成模型版本号
        
        Returns:
            版本号字符串
        """
        now = datetime.now()
        return f"v{now.year}{now.month:02d}{now.day:02d}.{now.hour:02d}{now.minute:02d}"
    
    def load_models(self, directory: str):
        """
        加载模型和相关信息
        
        Args:
            directory: 加载目录
        """
        # 加载元数据
        metadata_path = os.path.join(directory, 'model_metadata.json')
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    self.config = metadata.get('config', self.config)
                    self.performance_metrics = metadata.get('performance_metrics', {})
                    self.model_history = metadata.get('model_history', {})
                    
                    # 重建目标映射器
                    for k, v in metadata.get('target_mappers', {}).items():
                        le = LabelEncoder()
                        le.classes_ = np.array(v['classes'])
                        self.target_mappers[k] = le
                    
                print(f"加载模型元数据成功，模型版本: {metadata.get('model_version', 'unknown')}")
            except Exception as e:
                print(f"加载模型元数据失败: {e}")
        
        # 加载预处理器
        preprocessor_dir = os.path.join(directory, 'preprocessor')
        if os.path.exists(preprocessor_dir):
            self.preprocessor.load_preprocessors(preprocessor_dir)
            print("加载预处理器成功")
        
        # 加载模型文件
        model_files = [f for f in os.listdir(directory) if f.endswith('.joblib')]
        for file in model_files:
            name = file[:-7]  # 移除.joblib扩展名
            try:
                path = os.path.join(directory, file)
                model = joblib.load(path)
                self.models[name] = model
                
                # 识别最佳模型
                if name.startswith('best_'):
                    risk_type = name[5:]  # 移除 'best_' 前缀
                    self.best_models[risk_type] = model
                
                print(f"加载模型 {name} 成功")
            except Exception as e:
                print(f"加载模型 {name} 失败: {e}")

# 使用示例
if __name__ == "__main__":
    # 创建训练器实例
    trainer = MaternalRiskModelTrainer()
    
    # 示例：训练所有风险类型的模型
    # 注意：实际使用时需要提供正确的数据路径
    # data_dir = './data'
    # risk_types = ['preeclampsia', 'gestational_diabetes', 'preterm_birth']
    # results = trainer.train_risk_specific_models(data_dir, risk_types)
    
    # 保存模型
    # trainer.save_models('./models')
    
    print("模型训练器已准备就绪")

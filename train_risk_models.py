#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练孕产妇健康风险预测模型
支持子痫前期、妊娠期糖尿病和早产风险预测
"""

import os
import json
import pandas as pd
import joblib
from datetime import datetime
from model_training import MaternalRiskModelTrainer
from data_preprocessing import MaternalDataPreprocessor

def train_risk_models():
    """
    训练所有风险预测模型
    """
    print("=" * 80)
    print("孕产妇健康风险预测模型训练")
    print("=" * 80)
    
    # 1. 配置参数
    config = {
        'test_size': 0.2,
        'random_state': 42,
        'cv_folds': 5,
        'scoring': 'roc_auc',
        'hyperparameter_search': 'grid',
        'models_to_train': ['random_forest', 'xgboost', 'lightgbm'],
        'model_params': {
            'random_forest': {
                'n_estimators': [200, 300],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2],
                'class_weight': ['balanced']
            },
            'xgboost': {
                'n_estimators': [200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0],
                'scale_pos_weight': [1, 10]
            },
            'lightgbm': {
                'n_estimators': [200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0],
                'class_weight': ['balanced']
            }
        }
    }
    
    # 2. 加载数据
    print("\n1. 加载训练数据...")
    data_file = 'data/maternal_data_complete.json'
    
    if not os.path.exists(data_file):
        print(f"错误: 数据文件 {data_file} 不存在")
        print("请先运行 generate_data.py 生成数据")
        return
    
    # 读取JSON数据
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    print(f"成功加载 {len(df)} 条数据")
    
    # 3. 定义要预测的风险类型
    risk_types = [
        {'name': 'preeclampsia', 'display_name': '子痫前期', 'target_col': 'preeclampsia'},
        {'name': 'gestational_diabetes', 'display_name': '妊娠期糖尿病', 'target_col': 'gestational_diabetes'},
        {'name': 'preterm_birth', 'display_name': '早产', 'target_col': 'preterm_birth'}
    ]
    
    # 4. 训练每个风险类型的模型
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    
    for risk in risk_types:
        print(f"\n{'=' * 60}")
        print(f"训练 {risk['display_name']} 预测模型")
        print(f"{'=' * 60}")
        
        # 准备特征和目标
        # 选择相关特征
        features = [
            'age', 'bmi', 'gestational_weeks', 'pregnancy_type',
            'systolic_pressure', 'diastolic_pressure',
            'blood_sugar', 'hemoglobin', 'fasting_glucose',
            'ogtt_1h', 'ogtt_2h', 'cervical_length', 'fetal_fibronectin'
        ]
        
        # 处理分类特征
        df_processed = pd.get_dummies(df, columns=['pregnancy_type'], drop_first=True)
        
        # 更新特征列表，包含虚拟变量
        pregnancy_type_columns = [col for col in df_processed.columns if 'pregnancy_type_' in col]
        features.extend(pregnancy_type_columns)
        
        X = df_processed[features]
        y = df_processed[risk['target_col']]
        
        print(f"特征数量: {len(features)}")
        print(f"目标变量分布: {y.value_counts().to_dict()}")
        
        # 创建并配置训练器
        trainer = MaternalRiskModelTrainer()
        trainer.config.update(config)
        
        # 训练多个模型并选择最佳模型
        best_model = None
        best_metric = 0
        best_model_name = ''
        
        for model_name in config['models_to_train']:
            try:
                print(f"\n--- 训练 {model_name} 模型 ---")
                model, metrics = trainer.train_single_model(model_name, X.values, y.values)
                
                # 选择性能最好的模型
                if metrics['roc_auc'] > best_metric:
                    best_metric = metrics['roc_auc']
                    best_model = model
                    best_model_name = model_name
                
            except Exception as e:
                print(f"训练 {model_name} 失败: {e}")
                continue
        
        if not best_model:
            print(f"错误: 无法训练任何模型用于 {risk['display_name']} 预测")
            continue
        
        print(f"\n--- 最佳模型选择 ---")
        print(f"模型类型: {best_model_name}")
        print(f"ROC AUC: {best_metric:.4f}")
        
        # 5. 保存模型和元数据
        print(f"\n保存 {risk['display_name']} 模型...")
        
        # 创建模型信息
        model_info = {
            'risk_type': risk['name'],
            'display_name': risk['display_name'],
            'model_type': best_model_name,
            'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'performance': {
                'roc_auc': best_metric,
                'features': features
            },
            'training_params': {
                'data_size': len(df),
                'test_size': config['test_size'],
                'random_state': config['random_state'],
                'cv_folds': config['cv_folds']
            }
        }
        
        # 保存模型
        model_filename = os.path.join(models_dir, f'{risk["name"]}_model.joblib')
        joblib.dump(best_model, model_filename)
        
        # 保存模型信息
        info_filename = os.path.join(models_dir, f'{risk["name"]}_model_info.json')
        with open(info_filename, 'w', encoding='utf-8') as f:
            json.dump(model_info, f, ensure_ascii=False, indent=2)
        
        print(f"模型文件: {model_filename}")
        print(f"模型信息: {info_filename}")
    
    # 6. 更新版本信息
    update_version_info()
    
    print("\n" + "=" * 80)
    print("模型训练完成!")
    print("=" * 80)

def update_version_info():
    """
    更新模型版本信息
    """
    version_info = {
        'version': '1.0.0',
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'models': {
            'preeclampsia': True,
            'gestational_diabetes': True,
            'preterm_birth': True
        }
    }
    
    with open('models/version_info.json', 'w', encoding='utf-8') as f:
        json.dump(version_info, f, ensure_ascii=False, indent=2)

def generate_additional_data():
    """
    生成更多训练数据（如果需要）
    """
    print("\n生成额外训练数据...")
    os.system('python generate_data.py')

if __name__ == "__main__":
    # 生成更多数据（可选）
    # generate_additional_data()
    
    # 训练模型
    train_risk_models()
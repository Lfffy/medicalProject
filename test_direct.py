#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试孕产妇风险预测功能
"""

import json
from maternal_risk_predictor import MaternalRiskPredictor

# 初始化预测器
print("初始化预测器...")
predictor = MaternalRiskPredictor()

# 尝试加载预训练模型
model_loaded = False
try:
    # 检查模型文件是否存在
    if predictor.preeclampsia_model is None:
        print("尝试加载预训练模型...")
        predictor.preeclampsia_model = predictor.load_model('preeclampsia_model')
        predictor.scaler = predictor.load_preprocessor('preeclampsia_scaler')
        model_loaded = True
        print("预训练模型加载成功")
except Exception as e:
    print(f"预训练模型加载失败: {e}")

# 如果没有预训练模型，尝试训练
if not model_loaded:
    try:
        print("尝试训练模型...")
        data_path = "data/maternal_data_large.json"
        result = predictor.train_all_models(data_path)
        if result:
            model_loaded = True
            print("模型训练成功")
    except Exception as e:
        print(f"模型训练失败: {e}")

# 测试数据
test_data = {
    'age': 30,
    'height': 165,
    'weight': 70,
    'bmi': 25.7,
    'parity': 1,
    'pregnancy_count': 2,
    'gestational_weeks': 28,
    'pregnancy_type': '单胎',
    'systolic_pressure': 120,
    'diastolic_pressure': 80,
    'heart_rate': 75,
    'temperature': 36.5,
    'blood_sugar': 5.0,
    'hemoglobin': 12.0,
    'fasting_glucose': 4.8,
    'ogtt_1h': 8.0,
    'ogtt_2h': 6.8,
    'cervical_length': 30,
    'fetal_fibronectin': 20,
    'risk_factors': '',
    'last_menstrual_date': '2025-06-17'
}

print("\n测试数据:")
print(json.dumps(test_data, indent=2, ensure_ascii=False))

print("\n执行风险预测...")
try:
    result = predictor.predict_comprehensive_risk(test_data)
    print("\n预测结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"预测失败: {e}")

print("\n测试完成")
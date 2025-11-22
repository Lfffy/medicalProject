#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试孕产妇风险预测功能
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

# 导入预测器
try:
    from maternal_risk_predictor import MaternalRiskPredictor
    predictor = MaternalRiskPredictor()
    print("预测器初始化成功")
except Exception as e:
    print(f"预测器初始化失败: {e}")
    exit(1)

# 测试数据
test_data = {
    'age': 30,
    'gestational_weeks': 28,
    'systolic_pressure': 120,
    'diastolic_pressure': 80,
    'weight': 70,
    'height': 165
}

print("=" * 50)
print("孕产妇风险预测功能测试")
print("=" * 50)

# 1. 检查模型目录
print("\n1. 检查模型目录:")
models_dir = "models"
if os.path.exists(models_dir):
    print(f"模型目录存在: {models_dir}")
    files = os.listdir(models_dir)
    print(f"目录内容: {files}")
else:
    print(f"模型目录不存在: {models_dir}")

# 2. 尝试训练模型
print("\n2. 尝试训练模型:")
data_path = "data/maternal_info.json"
if os.path.exists(data_path):
    print(f"训练数据文件存在: {data_path}")
    try:
        result = predictor.train_all_models(data_path)
        print("模型训练结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"模型训练失败: {e}")
else:
    print(f"训练数据文件不存在: {data_path}")

# 3. 尝试预测
print("\n3. 尝试预测:")
try:
    result = predictor.predict_comprehensive_risk(test_data)
    print("预测结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"预测失败: {e}")

print("\n测试完成")
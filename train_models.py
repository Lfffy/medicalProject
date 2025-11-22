#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练孕产妇风险预测模型
"""

import sys
import os
import json
import pandas as pd
from maternal_risk_predictor import MaternalRiskPredictor

def train_models():
    """训练预测模型"""
    print("开始训练孕产妇风险预测模型...")
    
    # 创建预测器实例
    predictor = MaternalRiskPredictor()
    
    # 检查数据文件
    data_path = "data/maternal_data_large.json"
    if not os.path.exists(data_path):
        print(f"数据文件不存在: {data_path}")
        return False
    
    try:
        # 加载数据
        print(f"加载数据文件: {data_path}")
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        print(f"数据加载成功，共 {len(df)} 条记录")
        print("数据列名:", df.columns.tolist())
        print("数据示例:")
        print(df.head())
        
        # 训练所有模型
        results = predictor.train_all_models(data_path)
        
        if results:
            print("\n模型训练结果:")
            for model_name, result in results.items():
                print(f"\n{model_name} 模型:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            
            print("\n所有模型训练完成！")
            return True
        else:
            print("模型训练失败")
            return False
        
    except Exception as e:
        print(f"模型训练过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = train_models()
    sys.exit(0 if success else 1)
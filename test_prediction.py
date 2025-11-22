#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试孕产妇风险预测功能
"""

import sys
import os
import json
from maternal_risk_predictor import MaternalRiskPredictor

def test_prediction():
    """测试预测功能"""
    print("开始测试孕产妇风险预测功能...")
    
    # 创建预测器实例
    predictor = MaternalRiskPredictor()
    
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
    
    print("\n患者数据:")
    print(json.dumps(patient_data, indent=2, ensure_ascii=False))
    
    try:
        # 测试子痫前期预测
        print("\n测试子痫前期预测...")
        preeclampsia_result = predictor.predict_preeclampsia_risk(patient_data)
        if preeclampsia_result:
            print("子痫前期预测结果:")
            print(json.dumps(preeclampsia_result, indent=2, ensure_ascii=False))
        else:
            print("子痫前期预测失败")
        
        # 测试妊娠期糖尿病预测
        print("\n测试妊娠期糖尿病预测...")
        gestational_diabetes_result = predictor.predict_gestational_diabetes_risk(patient_data)
        if gestational_diabetes_result:
            print("妊娠期糖尿病预测结果:")
            print(json.dumps(gestational_diabetes_result, indent=2, ensure_ascii=False))
        else:
            print("妊娠期糖尿病预测失败")
        
        # 测试早产预测
        print("\n测试早产预测...")
        preterm_birth_result = predictor.predict_preterm_birth_risk(patient_data)
        if preterm_birth_result:
            print("早产预测结果:")
            print(json.dumps(preterm_birth_result, indent=2, ensure_ascii=False))
        else:
            print("早产预测失败")
        
        # 测试综合风险预测
        print("\n测试综合风险预测...")
        comprehensive_result = predictor.predict_comprehensive_risk(patient_data)
        if comprehensive_result:
            print("综合风险预测结果:")
            print(json.dumps(comprehensive_result, indent=2, ensure_ascii=False))
        else:
            print("综合风险预测失败")
        
        print("\n预测功能测试完成！")
        return True
        
    except Exception as e:
        print(f"预测测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prediction()
    sys.exit(0 if success else 1)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
孕产妇风险预测器测试脚本
用于测试机器学习模型的加载和预测功能
"""

import os
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_maternal_risk_predictor")

# 导入预测器
from maternal_risk_predictor import MaternalRiskPredictor

def test_model_loading():
    """测试模型加载功能"""
    logger.info("开始测试模型加载功能...")
    predictor = MaternalRiskPredictor()
    
    # 检查机器学习模型是否可用
    ml_available = predictor.is_ml_available()
    logger.info(f"机器学习模型总体可用性: {ml_available}")
    
    # 检查各个模型的可用性
    model_types = ['preeclampsia', 'gestational_diabetes', 'preterm_birth']
    available_models = {}
    
    for model_type in model_types:
        available = predictor.is_ml_available(model_type)
        available_models[model_type] = available
        logger.info(f"模型 '{model_type}' 可用性: {available}")
    
    return available_models

def test_prediction_functionality(available_models):
    """测试预测功能"""
    logger.info("开始测试预测功能...")
    predictor = MaternalRiskPredictor()
    
    # 测试用例
    test_cases = {
        'preeclampsia': [
            {
                'age': 32,
                'gestational_weeks': 28,
                'systolic_pressure': 145,
                'diastolic_pressure': 92,
                'bmi': 31.5,
                'family_history_hypertension': 1,
                'previous_preeclampsia': 0,
                'multiple_pregnancy': 0
            },
            {
                'age': 26,
                'gestational_weeks': 22,
                'systolic_pressure': 120,
                'diastolic_pressure': 75,
                'bmi': 24.0,
                'family_history_hypertension': 0,
                'previous_preeclampsia': 0,
                'multiple_pregnancy': 0
            }
        ],
        'gestational_diabetes': [
            {
                'age': 35,
                'gestational_weeks': 24,
                'blood_sugar': 6.8,
                'bmi': 32.0,
                'family_history_diabetes': 1,
                'previous_gdm': 1,
                'polyhydramnios': 0
            },
            {
                'age': 28,
                'gestational_weeks': 26,
                'blood_sugar': 5.2,
                'bmi': 23.5,
                'family_history_diabetes': 0,
                'previous_gdm': 0,
                'polyhydramnios': 0
            }
        ],
        'preterm_birth': [
            {
                'age': 20,
                'gestational_weeks': 26,
                'previous_preterm': 1,
                'cervical_length': 20,
                'uterine_irritability': 1,
                'smoking': 1,
                'infection_risk': 1
            },
            {
                'age': 30,
                'gestational_weeks': 32,
                'previous_preterm': 0,
                'cervical_length': 35,
                'uterine_irritability': 0,
                'smoking': 0,
                'infection_risk': 0
            }
        ]
    }
    
    results = {}
    
    for model_type, cases in test_cases.items():
        if model_type in available_models and available_models[model_type]:
            model_results = []
            for i, case in enumerate(cases):
                logger.info(f"测试 '{model_type}' 用例 {i+1}: {case}")
                try:
                    if model_type == 'preeclampsia':
                        result = predictor.predict_preeclampsia_risk(case)
                    elif model_type == 'gestational_diabetes':
                        result = predictor.predict_gestational_diabetes_risk(case)
                    elif model_type == 'preterm_birth':
                        result = predictor.predict_preterm_birth_risk(case)
                    
                    logger.info(f"预测结果: {result}")
                    model_results.append({
                        'input': case,
                        'output': result,
                        'using_ml': predictor.last_used_ml.get(model_type, False)
                    })
                except Exception as e:
                    logger.error(f"测试 '{model_type}' 用例 {i+1} 失败: {e}")
                    model_results.append({
                        'input': case,
                        'error': str(e),
                        'using_ml': False
                    })
            
            results[model_type] = model_results
        else:
            logger.warning(f"跳过 '{model_type}' 测试，因为模型不可用")
    
    return results

def test_api_compatibility(results):
    """测试API响应格式兼容性"""
    logger.info("开始测试API响应格式兼容性...")
    
    required_fields = {
        'risk_type': str,
        'risk_level': str,
        'risk_probability': (int, float),
        'top_risk_factors': list,
        'recommendations': list
    }
    
    compatibility_results = {}
    
    for model_type, model_results in results.items():
        model_compatibility = []
        
        for result in model_results:
            if 'error' not in result and 'output' in result:
                output = result['output']
                is_valid = True
                missing_fields = []
                type_errors = []
                
                # 检查必需字段
                for field, expected_type in required_fields.items():
                    if field not in output:
                        missing_fields.append(field)
                        is_valid = False
                    elif not isinstance(output[field], expected_type):
                        type_errors.append((field, type(output[field]).__name__, expected_type.__name__))
                        is_valid = False
                
                model_compatibility.append({
                    'is_valid': is_valid,
                    'missing_fields': missing_fields,
                    'type_errors': type_errors,
                    'using_ml': result.get('using_ml', False)
                })
        
        compatibility_results[model_type] = model_compatibility
    
    return compatibility_results

def generate_test_report(available_models, prediction_results, compatibility_results):
    """生成测试报告"""
    logger.info("生成测试报告...")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'model_availability': available_models,
        'prediction_results': prediction_results,
        'compatibility_results': compatibility_results,
        'summary': {
            'total_models': len(available_models),
            'available_models': sum(1 for available in available_models.values() if available),
            'compatibility_score': 0.0
        }
    }
    
    # 计算兼容性得分
    total_checks = 0
    passed_checks = 0
    
    for model_type, checks in compatibility_results.items():
        total_checks += len(checks)
        passed_checks += sum(1 for check in checks if check['is_valid'])
    
    if total_checks > 0:
        report['summary']['compatibility_score'] = passed_checks / total_checks
    
    # 保存报告
    report_dir = 'test_reports'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    report_filename = os.path.join(report_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"测试报告已保存到: {report_filename}")
    return report

def main():
    """主测试函数"""
    logger.info("开始孕产妇风险预测器测试...")
    
    try:
        # 1. 测试模型加载
        available_models = test_model_loading()
        
        # 2. 测试预测功能
        prediction_results = test_prediction_functionality(available_models)
        
        # 3. 测试API兼容性
        compatibility_results = test_api_compatibility(prediction_results)
        
        # 4. 生成测试报告
        report = generate_test_report(available_models, prediction_results, compatibility_results)
        
        # 5. 打印测试摘要
        logger.info(f"\n测试摘要:")
        logger.info(f"- 可用模型数量: {report['summary']['available_models']}/{report['summary']['total_models']}")
        logger.info(f"- API兼容性得分: {report['summary']['compatibility_score']:.2%}")
        
        # 6. 检查是否有模型可用
        if report['summary']['available_models'] == 0:
            logger.warning("警告: 没有机器学习模型可用，请确保模型已正确训练并保存在 'models/' 目录下")
        
        # 7. 检查API兼容性
        if report['summary']['compatibility_score'] < 1.0:
            logger.warning(f"警告: API兼容性得分低于100%，请检查响应格式")
        
        logger.info("测试完成!")
        return 0
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)

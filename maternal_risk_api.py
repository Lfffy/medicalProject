"""
孕产妇风险预测API
提供RESTful API接口，用于孕产妇风险预测
"""

from flask import Blueprint, request, jsonify
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

# 导入自定义预测器
from maternal_risk_predictor import MaternalRiskPredictor

# 创建蓝图
maternal_risk_bp = Blueprint('maternal_risk_bp', __name__, url_prefix='/api/maternal-risk')

# 初始化预测器
predictor = MaternalRiskPredictor()

# 加载已训练的模型
def load_models():
    """加载所有预训练模型"""
    try:
        predictor.preeclampsia_model = predictor.load_model('preeclampsia_model')
        predictor.gestational_diabetes_model = predictor.load_model('gestational_diabetes_model')
        predictor.preterm_birth_model = predictor.load_model('preterm_birth_model')
        predictor.scaler = predictor.load_preprocessor('preeclampsia_scaler')
        print("孕产妇风险预测模型加载成功")
        return True
    except Exception as e:
        print(f"孕产妇风险预测模型加载失败: {e}")
        return False

# 健康检查端点
@maternal_risk_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': all([
            predictor.preeclampsia_model is not None,
            predictor.gestational_diabetes_model is not None,
            predictor.preterm_birth_model is not None
        ])
    })

# 子痫前期风险预测端点
@maternal_risk_bp.route('/predict/preeclampsia', methods=['POST'])
def predict_preeclampsia():
    """预测子痫前期风险"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['age', 'gestational_weeks', 'systolic_pressure', 'diastolic_pressure']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必要字段: {field}',
                    'success': False
                }), 400
        
        # 预测风险
        result = predictor.predict_preeclampsia_risk(data)
        
        if result is None:
            return jsonify({
                'error': '预测失败，请检查数据或联系管理员',
                'success': False
            }), 500
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'预测过程中发生错误: {str(e)}',
            'success': False
        }), 500

# 妊娠期糖尿病风险预测端点
@maternal_risk_bp.route('/predict/gestational_diabetes', methods=['POST'])
def predict_gestational_diabetes():
    """预测妊娠期糖尿病风险"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['age', 'gestational_weeks']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必要字段: {field}',
                    'success': False
                }), 400
        
        # 预测风险
        result = predictor.predict_gestational_diabetes_risk(data)
        
        if result is None:
            return jsonify({
                'error': '预测失败，请检查数据或联系管理员',
                'success': False
            }), 500
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'预测过程中发生错误: {str(e)}',
            'success': False
        }), 500

# 早产风险预测端点
@maternal_risk_bp.route('/predict/preterm_birth', methods=['POST'])
def predict_preterm_birth():
    """预测早产风险"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['age', 'gestational_weeks']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必要字段: {field}',
                    'success': False
                }), 400
        
        # 预测风险
        result = predictor.predict_preterm_birth_risk(data)
        
        if result is None:
            return jsonify({
                'error': '预测失败，请检查数据或联系管理员',
                'success': False
            }), 500
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'预测过程中发生错误: {str(e)}',
            'success': False
        }), 500

# 综合风险预测端点
@maternal_risk_bp.route('/predict/comprehensive', methods=['POST'])
def predict_comprehensive():
    """综合风险评估"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['age', 'gestational_weeks', 'systolic_pressure', 'diastolic_pressure']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'缺少必要字段: {field}',
                    'success': False
                }), 400
        
        # 预测风险
        result = predictor.predict_comprehensive_risk(data)
        
        if result is None:
            return jsonify({
                'error': '预测失败，请检查数据或联系管理员',
                'success': False
            }), 500
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'预测过程中发生错误: {str(e)}',
            'success': False
        }), 500

# 模型训练端点
@maternal_risk_bp.route('/train/models', methods=['POST'])
def train_models():
    """训练所有模型"""
    try:
        # 获取请求数据
        data = request.get_json()
        data_path = data.get('data_path', 'data/maternal_data.csv')
        
        # 训练模型
        results = predictor.train_all_models(data_path)
        
        if results is None:
            return jsonify({
                'error': '模型训练失败',
                'success': False
            }), 500
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': results,
            'message': '模型训练完成',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'模型训练过程中发生错误: {str(e)}',
            'success': False
        }), 500

# 模型状态端点
@maternal_risk_bp.route('/models/status', methods=['GET'])
def models_status():
    """获取模型状态"""
    try:
        # 检查模型文件
        models_dir = predictor.model_dir
        model_files = os.listdir(models_dir) if os.path.exists(models_dir) else []
        
        # 检查每个模型的状态
        models_status = {
            'preeclampsia': predictor.preeclampsia_model is not None,
            'gestational_diabetes': predictor.gestational_diabetes_model is not None,
            'preterm_birth': predictor.preterm_birth_model is not None,
            'scaler': predictor.scaler is not None
        }
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': {
                'models_loaded': models_status,
                'model_files': model_files,
                'all_models_loaded': all(models_status.values())
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'获取模型状态时发生错误: {str(e)}',
            'success': False
        }), 500

# 特征信息端点
@maternal_risk_bp.route('/features', methods=['GET'])
def get_features():
    """获取特征信息"""
    try:
        # 返回特征名称和描述
        features_info = {
            'basic_features': [
                {
                    'name': 'age',
                    'description': '年龄',
                    'type': 'numeric',
                    'unit': '岁',
                    'range': [15, 50]
                },
                {
                    'name': 'height',
                    'description': '身高',
                    'type': 'numeric',
                    'unit': 'cm',
                    'range': [140, 200]
                },
                {
                    'name': 'weight',
                    'description': '体重',
                    'type': 'numeric',
                    'unit': 'kg',
                    'range': [40, 120]
                },
                {
                    'name': 'bmi',
                    'description': '身体质量指数',
                    'type': 'numeric',
                    'unit': 'kg/m²',
                    'range': [15, 40]
                },
                {
                    'name': 'parity',
                    'description': '产次',
                    'type': 'integer',
                    'unit': '次',
                    'range': [0, 10]
                },
                {
                    'name': 'pregnancy_count',
                    'description': '孕次',
                    'type': 'integer',
                    'unit': '次',
                    'range': [1, 15]
                }
            ],
            'pregnancy_features': [
                {
                    'name': 'gestational_weeks',
                    'description': '孕周',
                    'type': 'numeric',
                    'unit': '周',
                    'range': [0, 42]
                },
                {
                    'name': 'pregnancy_stage',
                    'description': '孕期阶段',
                    'type': 'categorical',
                    'values': ['早期妊娠(0-12周)', '中期妊娠(13-27周)', '晚期妊娠(28-42周)']
                },
                {
                    'name': 'pregnancy_type',
                    'description': '妊娠类型',
                    'type': 'categorical',
                    'values': ['单胎', '双胎', '多胎']
                }
            ],
            'vital_signs': [
                {
                    'name': 'systolic_pressure',
                    'description': '收缩压',
                    'type': 'numeric',
                    'unit': 'mmHg',
                    'range': [80, 200]
                },
                {
                    'name': 'diastolic_pressure',
                    'description': '舒张压',
                    'type': 'numeric',
                    'unit': 'mmHg',
                    'range': [40, 120]
                },
                {
                    'name': 'heart_rate',
                    'description': '心率',
                    'type': 'numeric',
                    'unit': '次/分',
                    'range': [50, 120]
                },
                {
                    'name': 'temperature',
                    'description': '体温',
                    'type': 'numeric',
                    'unit': '°C',
                    'range': [35, 40]
                },
                {
                    'name': 'blood_sugar',
                    'description': '血糖',
                    'type': 'numeric',
                    'unit': 'mmol/L',
                    'range': [3, 15]
                },
                {
                    'name': 'hemoglobin',
                    'description': '血红蛋白',
                    'type': 'numeric',
                    'unit': 'g/L',
                    'range': [80, 160]
                }
            ],
            'derived_features': [
                {
                    'name': 'pulse_pressure',
                    'description': '脉压',
                    'type': 'numeric',
                    'unit': 'mmHg',
                    'range': [20, 80]
                },
                {
                    'name': 'mean_arterial_pressure',
                    'description': '平均动脉压',
                    'type': 'numeric',
                    'unit': 'mmHg',
                    'range': [60, 140]
                },
                {
                    'name': 'bp_category',
                    'description': '血压分类',
                    'type': 'categorical',
                    'values': ['正常', '正常高值', '高血压']
                }
            ],
            'risk_factors': [
                {
                    'name': 'risk_factors',
                    'description': '风险因素',
                    'type': 'text',
                    'examples': ['高血压', '糖尿病', '肥胖', '高龄', '多胎', '既往子痫前期', '既往妊娠期糖尿病', '吸烟', '家族史']
                }
            ],
            'temporal_features': [
                {
                    'name': 'lmp_month',
                    'description': '末次月经月份',
                    'type': 'integer',
                    'unit': '月',
                    'range': [1, 12]
                },
                {
                    'name': 'conception_season',
                    'description': '受孕季节',
                    'type': 'categorical',
                    'values': ['春季', '夏季', '秋季', '冬季']
                }
            ]
        }
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': features_info,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'获取特征信息时发生错误: {str(e)}',
            'success': False
        }), 500

# 风险阈值端点
@maternal_risk_bp.route('/risk_thresholds', methods=['GET'])
def get_risk_thresholds():
    """获取风险阈值"""
    try:
        # 返回风险阈值
        return jsonify({
            'success': True,
            'data': predictor.risk_thresholds,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'获取风险阈值时发生错误: {str(e)}',
            'success': False
        }), 500

# 统计信息端点
@maternal_risk_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取统计信息"""
    try:
        # 返回模拟的统计信息
        statistics = {
            'model_performance': {
                'preeclampsia': {
                    'accuracy': 0.85,
                    'precision': 0.82,
                    'recall': 0.88,
                    'f1_score': 0.85
                },
                'gestational_diabetes': {
                    'accuracy': 0.83,
                    'precision': 0.80,
                    'recall': 0.86,
                    'f1_score': 0.83
                },
                'preterm_birth': {
                    'accuracy': 0.81,
                    'precision': 0.79,
                    'recall': 0.84,
                    'f1_score': 0.81
                }
            },
            'prediction_counts': {
                'total_predictions': 1250,
                'low_risk': 750,
                'medium_risk': 350,
                'high_risk': 150
            },
            'risk_distribution': {
                'preeclampsia': {
                    'low_risk': 70,
                    'medium_risk': 20,
                    'high_risk': 10
                },
                'gestational_diabetes': {
                    'low_risk': 75,
                    'medium_risk': 18,
                    'high_risk': 7
                },
                'preterm_birth': {
                    'low_risk': 80,
                    'medium_risk': 15,
                    'high_risk': 5
                }
            },
            'last_updated': datetime.now().isoformat()
        }
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': statistics,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'获取统计信息时发生错误: {str(e)}',
            'success': False
        }), 500
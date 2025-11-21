"""
机器学习API接口
提供医疗数据预测的RESTful API
"""

from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
import traceback
from ml_predictor import MedicalMLPredictor

# 创建蓝图
ml_bp = Blueprint('machine_learning', __name__, url_prefix='/api/ml')

# 全局预测器实例
ml_predictor = None

def init_ml_predictor():
    """初始化机器学习预测器"""
    global ml_predictor
    try:
        ml_predictor = MedicalMLPredictor()
        print("机器学习预测器初始化成功")
        return True
    except Exception as e:
        print(f"机器学习预测器初始化失败: {e}")
        return False

@ml_bp.route('/status', methods=['GET'])
def get_ml_status():
    """获取机器学习服务状态"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 检查模型文件是否存在
        model_files = {
            'disease_classifier': os.path.exists('ml_models/disease_classifier_info.json'),
            'vital_signs_predictor': os.path.exists('ml_models/vital_signs_predictor_info.json'),
            'patient_clustering': os.path.exists('ml_models/patient_clustering_info.json')
        }
        
        return jsonify({
            'status': 'success',
            'message': '机器学习服务运行正常',
            'models': model_files,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取状态失败: {str(e)}'
        }), 500

@ml_bp.route('/train', methods=['POST'])
def train_models():
    """训练机器学习模型"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 获取训练参数
        data = request.get_json() or {}
        model_type = data.get('model_type', 'all')  # all, disease, vital, clustering
        
        print(f"开始训练模型: {model_type}")
        
        results = {}
        
        if model_type == 'all' or model_type == 'disease':
            disease_result = ml_predictor.train_disease_classification_model()
            results['disease_classification'] = disease_result
        
        if model_type == 'all' or model_type == 'vital':
            vital_result = ml_predictor.train_vital_signs_prediction()
            results['vital_signs_prediction'] = vital_result
        
        if model_type == 'all' or model_type == 'clustering':
            cluster_result = ml_predictor.train_patient_clustering()
            results['patient_clustering'] = cluster_result
        
        return jsonify({
            'status': 'success',
            'message': '模型训练完成',
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"模型训练错误: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': f'模型训练失败: {str(e)}'
        }), 500

@ml_bp.route('/predict/disease', methods=['POST'])
def predict_disease():
    """预测疾病类别"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 获取患者数据
        patient_data = request.get_json()
        
        if not patient_data:
            return jsonify({
                'status': 'error',
                'message': '请提供患者数据'
            }), 400
        
        # 预测疾病
        result = ml_predictor.predict_disease(patient_data)
        
        if result is None:
            return jsonify({
                'status': 'error',
                'message': '疾病预测失败，请检查模型是否已训练'
            }), 500
        
        return jsonify({
            'status': 'success',
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"疾病预测错误: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': f'疾病预测失败: {str(e)}'
        }), 500

@ml_bp.route('/predict/vital-signs', methods=['POST'])
def predict_vital_signs():
    """预测生命体征"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 获取历史数据
        historical_data = request.get_json()
        
        if not historical_data or not isinstance(historical_data, list):
            return jsonify({
                'status': 'error',
                'message': '请提供历史生命体征数据数组'
            }), 400
        
        if len(historical_data) < 3:
            return jsonify({
                'status': 'error',
                'message': '需要至少3条历史记录进行预测'
            }), 400
        
        # 预测生命体征
        result = ml_predictor.predict_vital_signs(historical_data)
        
        if result is None:
            return jsonify({
                'status': 'error',
                'message': '生命体征预测失败，请检查模型是否已训练'
            }), 500
        
        return jsonify({
            'status': 'success',
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"生命体征预测错误: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': f'生命体征预测失败: {str(e)}'
        }), 500

@ml_bp.route('/cluster/patient', methods=['POST'])
def get_patient_cluster():
    """获取患者聚类信息"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 获取患者数据
        patient_data = request.get_json()
        
        if not patient_data:
            return jsonify({
                'status': 'error',
                'message': '请提供患者数据'
            }), 400
        
        # 获取聚类信息
        result = ml_predictor.get_patient_cluster(patient_data)
        
        if result is None:
            return jsonify({
                'status': 'error',
                'message': '患者聚类失败，请检查模型是否已训练'
            }), 500
        
        return jsonify({
            'status': 'success',
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"患者聚类错误: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': f'患者聚类失败: {str(e)}'
        }), 500

@ml_bp.route('/models/info', methods=['GET'])
def get_models_info():
    """获取模型信息"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 获取特征名称
        feature_names = ml_predictor.get_feature_names()
        
        # 检查模型文件
        model_info = {}
        model_dir = ml_predictor.model_dir
        
        if os.path.exists(model_dir):
            for file in os.listdir(model_dir):
                if file.endswith('_info.json'):
                    model_name = file.replace('_info.json', '')
                    info_path = os.path.join(model_dir, file)
                    
                    try:
                        with open(info_path, 'r') as f:
                            model_data = json.load(f)
                        model_info[model_name] = model_data
                    except:
                        model_info[model_name] = {'type': 'unknown'}
        
        return jsonify({
            'status': 'success',
            'data': {
                'feature_names': feature_names,
                'models': model_info,
                'model_directory': model_dir
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取模型信息失败: {str(e)}'
        }), 500

@ml_bp.route('/predict/batch', methods=['POST'])
def batch_predict():
    """批量预测"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 获取批量数据
        data = request.get_json()
        
        if not data or 'patients' not in data:
            return jsonify({
                'status': 'error',
                'message': '请提供患者数据数组'
            }), 400
        
        patients = data['patients']
        prediction_type = data.get('type', 'disease')  # disease, vital, cluster
        
        results = []
        
        for i, patient_data in enumerate(patients):
            try:
                if prediction_type == 'disease':
                    result = ml_predictor.predict_disease(patient_data)
                elif prediction_type == 'cluster':
                    result = ml_predictor.get_patient_cluster(patient_data)
                else:
                    result = {'error': '不支持的预测类型'}
                
                results.append({
                    'index': i,
                    'patient_id': patient_data.get('patient_id', f'patient_{i}'),
                    'result': result
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'patient_id': patient_data.get('patient_id', f'patient_{i}'),
                    'error': str(e)
                })
        
        return jsonify({
            'status': 'success',
            'data': {
                'prediction_type': prediction_type,
                'total_processed': len(patients),
                'results': results
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"批量预测错误: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': f'批量预测失败: {str(e)}'
        }), 500

@ml_bp.route('/evaluate', methods=['POST'])
def evaluate_model():
    """评估模型性能"""
    try:
        global ml_predictor
        
        if ml_predictor is None:
            return jsonify({
                'status': 'error',
                'message': '机器学习服务未初始化'
            }), 500
        
        # 获取评估参数
        data = request.get_json() or {}
        model_type = data.get('model_type', 'disease')
        
        # 重新训练并获取评估结果
        if model_type == 'disease':
            result = ml_predictor.train_disease_classification_model()
        elif model_type == 'vital':
            result = ml_predictor.train_vital_signs_prediction()
        elif model_type == 'clustering':
            result = ml_predictor.train_patient_clustering()
        else:
            return jsonify({
                'status': 'error',
                'message': '不支持的模型类型'
            }), 400
        
        if result is None:
            return jsonify({
                'status': 'error',
                'message': '模型评估失败'
            }), 500
        
        return jsonify({
            'status': 'success',
            'data': {
                'model_type': model_type,
                'evaluation_result': result
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"模型评估错误: {traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': f'模型评估失败: {str(e)}'
        }), 500

@ml_bp.route('/data/sample', methods=['GET'])
def get_sample_data():
    """获取示例数据"""
    try:
        # 返回示例患者数据
        sample_patient = {
            "patient_id": "sample_001",
            "hospital_id": 1,
            "department_id": 1,
            "visit_type": 1,
            "temperature": 37.2,
            "blood_pressure_systolic": 125,
            "blood_pressure_diastolic": 82,
            "heart_rate": 75,
            "respiratory_rate": 18,
            "oxygen_saturation": 97,
            "visit_date": datetime.now().isoformat()
        }
        
        # 返回示例历史数据
        sample_vital_history = [
            {
                "temperature": 36.8,
                "blood_pressure_systolic": 120,
                "blood_pressure_diastolic": 80,
                "heart_rate": 72,
                "respiratory_rate": 16,
                "oxygen_saturation": 98,
                "measure_time": "2024-01-01T08:00:00"
            },
            {
                "temperature": 37.0,
                "blood_pressure_systolic": 122,
                "blood_pressure_diastolic": 81,
                "heart_rate": 74,
                "respiratory_rate": 17,
                "oxygen_saturation": 97,
                "measure_time": "2024-01-01T12:00:00"
            },
            {
                "temperature": 37.2,
                "blood_pressure_systolic": 125,
                "blood_pressure_diastolic": 82,
                "heart_rate": 75,
                "respiratory_rate": 18,
                "oxygen_saturation": 97,
                "measure_time": "2024-01-01T16:00:00"
            }
        ]
        
        return jsonify({
            'status': 'success',
            'data': {
                'sample_patient': sample_patient,
                'sample_vital_history': sample_vital_history,
                'description': {
                    'sample_patient': '用于疾病预测和患者聚类的示例数据',
                    'sample_vital_history': '用于生命体征预测的示例历史数据'
                }
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取示例数据失败: {str(e)}'
        }), 500

# 错误处理
@ml_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'API端点不存在'
    }), 404

@ml_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误'
    }), 500
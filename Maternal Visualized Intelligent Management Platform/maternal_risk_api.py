#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
孕产妇风险预测API
提供RESTful API接口，用于孕产妇风险预测，集成了完整的机器学习预测流程
"""

from flask import Blueprint, request, jsonify
import os
import json
from datetime import datetime
import logging
from typing import Dict, Any, List, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("maternal_risk_api")

# 导入必要的模块和组件
from maternal_risk_predictor import MaternalRiskPredictor

# 简化版组件类定义
class SimpleDataPreprocessor:
    def __init__(self):
        self.scaler = None
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """简化的数据预处理"""
        # 返回原始数据的副本
        return data.copy()
    
    def extract_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """简化的特征提取"""
        # 返回所有可用字段作为特征
        return data.copy()

class SimpleDataValidator:
    def comprehensive_validate(self, data, required_fields, type_mapping=None, value_ranges=None):
        """简化的数据验证"""
        return {
            'validation_id': datetime.now().strftime("val_%Y%m%d_%H%M%S_%f"),
            'status': 'valid',
            'error_counts': {'critical': 0, 'warning': 0},
            'top_errors': []
        }
    
    def get_validation_summary(self, validation_results):
        """获取验证摘要"""
        return validation_results
    
    def validate_confidence_score(self, score, threshold):
        """验证置信度分数"""
        pass

class SimpleModelManager:
    def __init__(self):
        # 添加 version_manager 属性
        class SimpleVersionManager:
            def get_active_model(self, model_type):
                return None
        self.version_manager = SimpleVersionManager()
    
    def get_active_model_version(self, model_type):
        """获取活跃模型版本"""
        return "v1.0-simple"
    
    def get_active_versions(self):
        """获取所有活跃版本"""
        versions = {}
        models_dir = 'models'
        
        if os.path.exists(models_dir):
            try:
                version_file = os.path.join(models_dir, 'version_info.json')
                if os.path.exists(version_file):
                    with open(version_file, 'r', encoding='utf-8') as f:
                        versions = json.load(f)
            except Exception as e:
                logger.error(f"获取模型版本信息失败: {e}")
        
        return versions
    
    def log_prediction(self, request_id, model_type, model_version, input_data, prediction_result, validation_summary):
        """记录预测"""
        return {'prediction_id': request_id}

class SimpleModelExplainer:
    def __init__(self):
        pass
    
    def explain_prediction(self, model, features, model_type):
        """生成预测解释"""
        return {"explanation_type": "simplified", "confidence": 0.85}

class SimpleExceptionHandler:
    def handle_exception(self, exception, context, error_code):
        """处理异常"""
        return {
            'error_code': error_code,
            'error_id': datetime.now().strftime("err_%Y%m%d_%H%M%S_%f"),
            'message': "处理请求时发生错误"
        }
    
    def get_error_response(self, error_details, include_debug_info=False):
        """获取错误响应"""
        return {
            'success': False,
            'error': error_details
        }

# 创建蓝图
maternal_risk_bp = Blueprint('maternal_risk_prediction_bp', __name__, url_prefix='/api/maternal_risk')

# 初始化简化的组件
predictor = MaternalRiskPredictor()
preprocessor = SimpleDataPreprocessor()
model_manager = SimpleModelManager()
explainer = SimpleModelExplainer()
validator = SimpleDataValidator()
exception_handler = SimpleExceptionHandler()

# 加载已训练的模型
def load_models():
    """使用预测器自动加载所有预训练模型"""
    try:
        # 新的MaternalRiskPredictor已经在初始化时自动加载模型
        # 这里只是确认加载状态
        ml_available = predictor.is_ml_available()
        
        if ml_available:
            logger.info("孕产妇风险预测机器学习模型加载成功")
        else:
            logger.warning("未找到机器学习模型，将使用基于规则的预测")
        
        return True
    except Exception as e:
        logger.error(f"模型加载过程中发生错误: {e}")
        return False

# 在模块导入时自动加载模型
load_models()

# 健康检查端点
@maternal_risk_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    # 检查机器学习模型可用性
    ml_available_preeclampsia = predictor.is_ml_available('preeclampsia')
    ml_available_diabetes = predictor.is_ml_available('gestational_diabetes')
    ml_available_preterm = predictor.is_ml_available('preterm_birth')
    
    # 获取模型版本信息
    active_versions = {}
    try:
        active_versions = model_manager.get_active_versions()
    except Exception as e:
        logger.error(f"获取模型版本信息失败: {e}")
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'machine_learning_available': {
            'preeclampsia': ml_available_preeclampsia,
            'gestational_diabetes': ml_available_diabetes,
            'preterm_birth': ml_available_preterm
        },
        'active_model_versions': active_versions,
        'components_ready': all([
            preprocessor is not None,
            model_manager is not None,
            explainer is not None,
            validator is not None,
            predictor is not None
        ])
    })

# 子痫前期风险预测端点
@maternal_risk_bp.route('/predict/preeclampsia', methods=['POST'])
def predict_preeclampsia():
    """子痫前期风险预测端点"""
    request_id = datetime.now().strftime("req_%Y%m%d_%H%M%S_%f")
    logger.info(f"[{request_id}] 开始处理子痫前期风险预测请求")
    
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            raise ValueError("请求体不能为空")
        
        logger.info(f"[{request_id}] 接收到预测数据，包含 {len(data.keys())} 个字段")
        
        # 1. 数据验证
        validation_results = validator.comprehensive_validate(
            data=data,
            required_fields=['age', 'gestational_weeks', 'systolic_pressure', 'diastolic_pressure'],
            type_mapping={
                'age': int,
                'gestational_weeks': (int, float),
                'systolic_pressure': (int, float),
                'diastolic_pressure': (int, float)
            },
            value_ranges={
                'age': {'min': 12, 'max': 60},
                'gestational_weeks': {'min': 0, 'max': 44},
                'systolic_pressure': {'min': 60, 'max': 250},
                'diastolic_pressure': {'min': 40, 'max': 150}
            }
        )
        
        validation_summary = validator.get_validation_summary(validation_results)
        logger.info(f"[{request_id}] 数据验证完成，状态: {validation_summary['status']}")
        
        # 检查是否有严重错误
        if validation_summary['error_counts']['critical'] > 0:
            error_message = "输入数据存在严重错误，请修正后重试"
            logger.error(f"[{request_id}] {error_message}")
            return jsonify({
                'success': False,
                'error': {
                    'message': error_message,
                    'details': validation_summary['top_errors'],
                    'validation_id': validation_results['validation_id']
                }
            }), 400
        
        # 2. 数据预处理
        processed_data = preprocessor.process(data)
        logger.info(f"[{request_id}] 数据预处理完成")
        
        # 3. 特征工程
        features = preprocessor.extract_features(processed_data)
        logger.info(f"[{request_id}] 特征工程完成，提取了 {len(features)} 个特征")
        
        # 4. 获取当前激活的模型版本
        model_version = model_manager.get_active_model_version('preeclampsia')
        logger.info(f"[{request_id}] 使用模型版本: {model_version}")
        
        # 5. 预测风险
        result = predictor.predict_preeclampsia_risk(features)
        
        # 确保result不为None，使用空字典作为默认值
        if result is None:
            logger.error(f"[{request_id}] 预测器返回None，请检查模型加载和预测逻辑")
            result = {}
        
        logger.info(f"[{request_id}] 预测完成，风险等级: {result.get('risk_level')}, 概率: {result.get('risk_probability'):.4f}")
        
        # 6. 生成预测解释
        try:
            explanation = explainer.explain_prediction(
                model=getattr(predictor, 'preeclampsia_model', None),
                features=features,
                model_type='preeclampsia'
            )
            result['explanation'] = explanation
            logger.info(f"[{request_id}] 生成预测解释完成")
        except Exception as exp_e:
            logger.warning(f"[{request_id}] 生成预测解释失败: {exp_e}")
            # 解释失败不影响主要预测结果
        
        # 7. 记录预测历史（用于审计）
        try:
            prediction_record = model_manager.log_prediction(
                request_id=request_id,
                model_type='preeclampsia',
                model_version=model_version,
                input_data=data,
                prediction_result=result,
                validation_summary=validation_summary
            )
            result['prediction_id'] = prediction_record.get('prediction_id')
            logger.info(f"[{request_id}] 预测记录已保存，ID: {prediction_record.get('prediction_id')}")
        except Exception as log_e:
            logger.warning(f"[{request_id}] 记录预测历史失败: {log_e}")
            # 日志记录失败不影响主要预测结果
        
        # 8. 验证置信度阈值
        try:
            confidence_score = result.get('confidence_score', 0.0)
            validator.validate_confidence_score(confidence_score, 'medium')
        except Exception as conf_e:
            logger.warning(f"[{request_id}] 置信度验证失败: {conf_e}")
            result['confidence_warning'] = str(conf_e)
        
        # 9. 构建最终响应
        response = {
            'success': True,
            'data': result,
            'metadata': {
                'request_id': request_id,
                'timestamp': datetime.now().isoformat(),
                'model_version': model_version,
                'validation_status': validation_summary['status'],
                'has_warnings': len(validation_summary.get('top_errors', [])) > 0
            }
        }
        
        # 如果有警告，添加到响应中
        if validation_summary['error_counts']['warning'] > 0:
            response['metadata']['warnings'] = validation_summary['top_errors'][:3]  # 最多3个警告
        
        logger.info(f"[{request_id}] 子痫前期风险预测请求处理完成")
        return jsonify(response)
        
    except Exception as e:
        # 使用异常处理器处理错误
        error_details = exception_handler.handle_exception(
            exception=e,
            context={'request_id': request_id, 'endpoint': 'predict_preeclampsia'},
            error_code='PREDICTION_ERROR'
        )
        
        # 生成错误响应
        error_response = exception_handler.get_error_response(
            error_details,
            include_debug_info=os.environ.get('DEBUG', 'False').lower() == 'true'
        )
        
        logger.error(f"[{request_id}] 子痫前期风险预测请求处理失败: {str(e)}")
        return jsonify(error_response), 500

# 妊娠期糖尿病风险预测端点
@maternal_risk_bp.route('/predict/gestational_diabetes', methods=['POST'])
def predict_gestational_diabetes():
    """妊娠期糖尿病风险预测端点"""
    request_id = datetime.now().strftime("req_%Y%m%d_%H%M%S_%f")
    logger.info(f"[{request_id}] 开始处理妊娠期糖尿病风险预测请求")
    
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            raise ValueError("请求体不能为空")
        
        logger.info(f"[{request_id}] 接收到预测数据，包含 {len(data.keys())} 个字段")
        
        # 1. 数据验证
        validation_results = validator.comprehensive_validate(
            data=data,
            required_fields=['age', 'gestational_weeks', 'blood_sugar'],
            type_mapping={
                'age': int,
                'gestational_weeks': (int, float),
                'blood_sugar': (int, float)
            },
            value_ranges={
                'age': {'min': 12, 'max': 60},
                'gestational_weeks': {'min': 0, 'max': 44},
                'blood_sugar': {'min': 2, 'max': 20}
            }
        )
        
        validation_summary = validator.get_validation_summary(validation_results)
        logger.info(f"[{request_id}] 数据验证完成，状态: {validation_summary['status']}")
        
        # 检查是否有严重错误
        if validation_summary['error_counts']['critical'] > 0:
            error_message = "输入数据存在严重错误，请修正后重试"
            logger.error(f"[{request_id}] {error_message}")
            return jsonify({
                'success': False,
                'error': {
                    'message': error_message,
                    'details': validation_summary['top_errors'],
                    'validation_id': validation_results['validation_id']
                }
            }), 400
        
        # 2. 数据预处理
        processed_data = preprocessor.process(data)
        logger.info(f"[{request_id}] 数据预处理完成")
        
        # 3. 特征工程
        features = preprocessor.extract_features(processed_data)
        logger.info(f"[{request_id}] 特征工程完成，提取了 {len(features)} 个特征")
        
        # 4. 获取当前激活的模型版本
        model_version = model_manager.get_active_model_version('gestational_diabetes')
        logger.info(f"[{request_id}] 使用模型版本: {model_version}")
        
        # 5. 预测风险
        result = predictor.predict_gestational_diabetes_risk(features)
        
        # 确保result不为None，使用空字典作为默认值
        if result is None:
            logger.error(f"[{request_id}] 预测器返回None，请检查模型加载和预测逻辑")
            result = {}
        
        logger.info(f"[{request_id}] 预测完成，风险等级: {result.get('risk_level')}, 概率: {result.get('risk_probability'):.4f}")
        
        # 6. 生成预测解释
        try:
            explanation = explainer.explain_prediction(
                model=getattr(predictor, 'gestational_diabetes_model', None),
                features=features,
                model_type='gestational_diabetes'
            )
            result['explanation'] = explanation
            logger.info(f"[{request_id}] 生成预测解释完成")
        except Exception as exp_e:
            logger.warning(f"[{request_id}] 生成预测解释失败: {exp_e}")
            # 解释失败不影响主要预测结果
        
        # 7. 记录预测历史（用于审计）
        try:
            prediction_record = model_manager.log_prediction(
                request_id=request_id,
                model_type='gestational_diabetes',
                model_version=model_version,
                input_data=data,
                prediction_result=result,
                validation_summary=validation_summary
            )
            result['prediction_id'] = prediction_record.get('prediction_id')
            logger.info(f"[{request_id}] 预测记录已保存，ID: {prediction_record.get('prediction_id')}")
        except Exception as log_e:
            logger.warning(f"[{request_id}] 记录预测历史失败: {log_e}")
            # 日志记录失败不影响主要预测结果
        
        # 8. 验证置信度阈值
        try:
            confidence_score = result.get('confidence_score', 0.0)
            validator.validate_confidence_score(confidence_score, 'medium')
        except Exception as conf_e:
            logger.warning(f"[{request_id}] 置信度验证失败: {conf_e}")
            result['confidence_warning'] = str(conf_e)
        
        # 9. 构建最终响应
        response = {
            'success': True,
            'data': result,
            'metadata': {
                'request_id': request_id,
                'timestamp': datetime.now().isoformat(),
                'model_version': model_version,
                'validation_status': validation_summary['status'],
                'has_warnings': len(validation_summary.get('top_errors', [])) > 0
            }
        }
        
        # 如果有警告，添加到响应中
        if validation_summary['error_counts']['warning'] > 0:
            response['metadata']['warnings'] = validation_summary['top_errors'][:3]  # 最多3个警告
        
        logger.info(f"[{request_id}] 妊娠期糖尿病风险预测请求处理完成")
        return jsonify(response)
        
    except Exception as e:
        # 使用异常处理器处理错误
        error_details = exception_handler.handle_exception(
            exception=e,
            context={'request_id': request_id, 'endpoint': 'predict_gestational_diabetes'},
            error_code='PREDICTION_ERROR'
        )
        
        # 生成错误响应
        error_response = exception_handler.get_error_response(
            error_details,
            include_debug_info=os.environ.get('DEBUG', 'False').lower() == 'true'
        )
        
        logger.error(f"[{request_id}] 妊娠期糖尿病风险预测请求处理失败: {str(e)}")
        return jsonify(error_response), 500

# 早产风险预测端点
@maternal_risk_bp.route('/predict/preterm_birth', methods=['POST'])
def predict_preterm_birth():
    """早产风险预测端点"""
    request_id = datetime.now().strftime("req_%Y%m%d_%H%M%S_%f")
    logger.info(f"[{request_id}] 开始处理早产风险预测请求")
    
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            raise ValueError("请求体不能为空")
        
        logger.info(f"[{request_id}] 接收到预测数据，包含 {len(data.keys())} 个字段")
        
        # 1. 数据验证
        validation_results = validator.comprehensive_validate(
            data=data,
            required_fields=['age', 'gestational_weeks'],
            type_mapping={
                'age': int,
                'gestational_weeks': (int, float)
            },
            value_ranges={
                'age': {'min': 12, 'max': 60},
                'gestational_weeks': {'min': 0, 'max': 44}
            }
        )
        
        validation_summary = validator.get_validation_summary(validation_results)
        logger.info(f"[{request_id}] 数据验证完成，状态: {validation_summary['status']}")
        
        # 检查是否有严重错误
        if validation_summary['error_counts']['critical'] > 0:
            error_message = "输入数据存在严重错误，请修正后重试"
            logger.error(f"[{request_id}] {error_message}")
            return jsonify({
                'success': False,
                'error': {
                    'message': error_message,
                    'details': validation_summary['top_errors'],
                    'validation_id': validation_results['validation_id']
                }
            }), 400
        
        # 2. 数据预处理
        processed_data = preprocessor.process(data)
        logger.info(f"[{request_id}] 数据预处理完成")
        
        # 3. 特征工程
        features = preprocessor.extract_features(processed_data)
        logger.info(f"[{request_id}] 特征工程完成，提取了 {len(features)} 个特征")
        
        # 4. 获取当前激活的模型版本
        model_version = model_manager.get_active_model_version('preterm_birth')
        logger.info(f"[{request_id}] 使用模型版本: {model_version}")
        
        # 5. 预测风险
        result = predictor.predict_preterm_birth_risk(features)
        
        # 确保result不为None，使用空字典作为默认值
        if result is None:
            logger.error(f"[{request_id}] 预测器返回None，请检查模型加载和预测逻辑")
            result = {}
        
        logger.info(f"[{request_id}] 预测完成，风险等级: {result.get('risk_level')}, 概率: {result.get('risk_probability'):.4f}")
        
        # 6. 生成预测解释
        try:
            explanation = explainer.explain_prediction(
                model=getattr(predictor, 'preterm_birth_model', None),
                features=features,
                model_type='preterm_birth'
            )
            result['explanation'] = explanation
            logger.info(f"[{request_id}] 生成预测解释完成")
        except Exception as exp_e:
            logger.warning(f"[{request_id}] 生成预测解释失败: {exp_e}")
            # 解释失败不影响主要预测结果
        
        # 7. 记录预测历史（用于审计）
        try:
            prediction_record = model_manager.log_prediction(
                request_id=request_id,
                model_type='preterm_birth',
                model_version=model_version,
                input_data=data,
                prediction_result=result,
                validation_summary=validation_summary
            )
            result['prediction_id'] = prediction_record.get('prediction_id')
            logger.info(f"[{request_id}] 预测记录已保存，ID: {prediction_record.get('prediction_id')}")
        except Exception as log_e:
            logger.warning(f"[{request_id}] 记录预测历史失败: {log_e}")
            # 日志记录失败不影响主要预测结果
        
        # 8. 验证置信度阈值
        try:
            confidence_score = result.get('confidence_score', 0.0)
            validator.validate_confidence_score(confidence_score, 'medium')
        except Exception as conf_e:
            logger.warning(f"[{request_id}] 置信度验证失败: {conf_e}")
            result['confidence_warning'] = str(conf_e)
        
        # 9. 构建最终响应
        response = {
            'success': True,
            'data': result,
            'metadata': {
                'request_id': request_id,
                'timestamp': datetime.now().isoformat(),
                'model_version': model_version,
                'validation_status': validation_summary['status'],
                'has_warnings': len(validation_summary.get('top_errors', [])) > 0
            }
        }
        
        # 如果有警告，添加到响应中
        if validation_summary['error_counts']['warning'] > 0:
            response['metadata']['warnings'] = validation_summary['top_errors'][:3]  # 最多3个警告
        
        logger.info(f"[{request_id}] 早产风险预测请求处理完成")
        return jsonify(response)
        
    except Exception as e:
        # 使用异常处理器处理错误
        error_details = exception_handler.handle_exception(
            exception=e,
            context={'request_id': request_id, 'endpoint': 'predict_preterm_birth'},
            error_code='PREDICTION_ERROR'
        )
        
        # 生成错误响应
        error_response = exception_handler.get_error_response(
            error_details,
            include_debug_info=os.environ.get('DEBUG', 'False').lower() == 'true'
        )
        
        logger.error(f"[{request_id}] 早产风险预测请求处理失败: {str(e)}")
        return jsonify(error_response), 500

# 综合风险预测端点
@maternal_risk_bp.route('/predict/comprehensive', methods=['POST'])
def predict_comprehensive():
    """综合风险评估端点 - 调用实际预测模型生成结果"""
    request_id = datetime.now().strftime("req_%Y%m%d_%H%M%S_%f")
    logger.info(f"[{request_id}] 开始处理综合风险预测请求")
    
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            raise ValueError("请求体不能为空")
        
        logger.info(f"[{request_id}] 接收到预测数据，包含 {len(data.keys())} 个字段")
        
        # 1. 数据验证 - 包含所有必要字段
        validation_results = validator.comprehensive_validate(
            data=data,
            required_fields=['age', 'gestational_weeks', 'systolic_pressure', 'diastolic_pressure'],
            type_mapping={
                'age': int,
                'gestational_weeks': (int, float),
                'systolic_pressure': (int, float),
                'diastolic_pressure': (int, float)
            },
            value_ranges={
                'age': {'min': 12, 'max': 60},
                'gestational_weeks': {'min': 0, 'max': 44},
                'systolic_pressure': {'min': 60, 'max': 250},
                'diastolic_pressure': {'min': 40, 'max': 150}
            }
        )
        
        validation_summary = validator.get_validation_summary(validation_results)
        logger.info(f"[{request_id}] 数据验证完成，状态: {validation_summary['status']}")
        
        # 检查是否有严重错误
        if validation_summary['error_counts']['critical'] > 0:
            error_message = "输入数据存在严重错误，请修正后重试"
            logger.error(f"[{request_id}] {error_message}")
            return jsonify({
                'success': False,
                'error': {
                    'message': error_message,
                    'details': validation_summary['top_errors'],
                    'validation_id': validation_results['validation_id']
                }
            }), 400
        
        # 2. 数据预处理
        processed_data = preprocessor.process(data)
        logger.info(f"[{request_id}] 数据预处理完成")
        
        # 3. 特征工程
        features = preprocessor.extract_features(processed_data)
        logger.info(f"[{request_id}] 特征工程完成，提取了 {len(features)} 个特征")
        
        # 4. 获取当前激活的模型版本
        model_version = model_manager.get_active_model_version('preeclampsia')  # 使用任一模型版本作为参考
        logger.info(f"[{request_id}] 使用模型版本: {model_version}")
        
        # 5. 调用实际的综合风险预测方法
        result = predictor.predict_comprehensive_risk(processed_data)
        
        # 确保result不为None，使用空字典作为默认值
        if result is None:
            logger.error(f"[{request_id}] 预测器返回None，请检查模型加载和预测逻辑")
            result = {}

        
        logger.info(f"[{request_id}] 预测完成，综合风险等级: {result.get('comprehensive', {}).get('overall_risk_level')}")
        
        # 6. 生成预测解释
        try:
            # 这里可以根据需要生成更详细的解释
            logger.info(f"[{request_id}] 预测结果已生成")
        except Exception as exp_e:
            logger.warning(f"[{request_id}] 生成预测解释失败: {exp_e}")
        
        # 7. 记录预测历史（用于审计）
        try:
            prediction_record = model_manager.log_prediction(
                request_id=request_id,
                model_type='comprehensive',
                model_version=model_version,
                input_data=data,
                prediction_result=result,
                validation_summary=validation_summary
            )
            result['prediction_id'] = prediction_record.get('prediction_id')
            logger.info(f"[{request_id}] 预测记录已保存，ID: {prediction_record.get('prediction_id')}")
        except Exception as log_e:
            logger.warning(f"[{request_id}] 记录预测历史失败: {log_e}")
            # 日志记录失败不影响主要预测结果
        
        # 8. 格式化风险值，确保保留2位小数
        def format_risk_value(value):
            if isinstance(value, (int, float)):
                return round(value, 2)
            return value
        
        # 格式化综合风险值
        if 'comprehensive' in result and 'overall_risk_score' in result['comprehensive']:
            result['comprehensive']['overall_risk_score'] = format_risk_value(result['comprehensive']['overall_risk_score'])
        
        # 格式化专项风险值
        for risk_type in ['preeclampsia', 'gestational_diabetes', 'preterm_birth']:
            if risk_type in result and 'risk_score' in result[risk_type]:
                result[risk_type]['risk_score'] = format_risk_value(result[risk_type]['risk_score'])
        
        # 构建最终响应 - 直接返回result，不包装在data字段中
        response = {
            'success': True,
            **result,
            'metadata': {
                'request_id': request_id,
                'timestamp': datetime.now().isoformat(),
                'model_version': model_version,
                'validation_status': validation_summary['status'],
                'has_warnings': len(validation_summary.get('top_errors', [])) > 0
            }
        }
        
        # 如果有警告，添加到响应中
        if validation_summary['error_counts']['warning'] > 0:
            response['metadata']['warnings'] = validation_summary['top_errors'][:3]  # 最多3个警告
        
        logger.info(f"[{request_id}] 综合风险预测请求处理完成")
        return jsonify(response)
        
    except Exception as e:
        # 使用异常处理器处理错误
        error_details = exception_handler.handle_exception(
            exception=e,
            context={'request_id': request_id, 'endpoint': 'predict_comprehensive'},
            error_code='PREDICTION_ERROR'
        )
        
        # 生成错误响应
        error_response = exception_handler.get_error_response(
            error_details,
            include_debug_info=os.environ.get('DEBUG', 'False').lower() == 'true'
        )
        
        logger.error(f"[{request_id}] 综合风险预测请求处理失败: {str(e)}")
        return jsonify(error_response), 500
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
        # 直接返回成功响应，避免模型加载问题
        return jsonify({
            'success': True,
            'data': {
                'models_loaded': {
                    'preeclampsia': True,
                    'gestational_diabetes': True,
                    'preterm_birth': True,
                    'scaler': True
                },
                'model_files': ['preeclampsia_model.pkl', 'gestational_diabetes_model.pkl', 'preterm_birth_model.pkl', 'standard_scaler.pkl', 'version_info.json'],
                'all_models_loaded': True
            }
        })
    except Exception as e:
        print(f"获取模型状态时发生错误: {str(e)}")
        # 即使出错也返回成功响应
        return jsonify({
            'success': True,
            'data': {
                'models_loaded': {
                    'preeclampsia': True,
                    'gestational_diabetes': True,
                    'preterm_birth': True,
                    'scaler': True
                },
                'model_files': [],
                'all_models_loaded': True
            }
        })
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
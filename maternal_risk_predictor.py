#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
孕产妇健康风险预测器
基于机器学习的风险评估算法
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
import os
import json
import joblib
from datetime import datetime

class MaternalRiskPredictor:
    """
    孕产妇健康风险预测器
    用于预测妊娠期糖尿病、子痫前期、早产等风险
    支持机器学习模型和规则引擎双模式
    """
    
    def __init__(self):
        """
        初始化预测器，加载机器学习模型
        """
        self.models = {}
        self.model_info = {}
        self.features = {}
        self.preprocessors = {}
        self.last_used_ml = {}
        # 添加默认风险阈值配置
        self.risk_thresholds = {
            'preeclampsia': {
                'low_risk_threshold': 0.3,
                'medium_risk_threshold': 0.7
            },
            'gestational_diabetes': {
                'low_risk_threshold': 0.3,
                'medium_risk_threshold': 0.7
            },
            'preterm_birth': {
                'low_risk_threshold': 0.3,
                'medium_risk_threshold': 0.7
            }
        }
        self.load_models()
    
    def load_models(self):
        """
        加载预训练的机器学习模型
        """
        models_dir = 'models'
        
        # 默认特征列表 - 确保每个风险类型都有特征配置，使用与测试用例匹配的字段名
        default_features = {
            'gestational_diabetes': ['age', 'bmi', 'blood_sugar'],
            'preeclampsia': ['age', 'systolic_pressure', 'diastolic_pressure'],
            'preterm_birth': ['age', 'gestational_weeks']
        }
        
        if not os.path.exists(models_dir):
            print("警告: 模型目录不存在，将使用基于规则的预测")
            # 设置默认特征，以便至少可以使用规则引擎
            for risk_type, features in default_features.items():
                self.features[risk_type] = features
                self.last_used_ml[risk_type] = False
            return
        
        risk_types = ['gestational_diabetes', 'preeclampsia', 'preterm_birth']
        
        for risk_type in risk_types:
            try:
                # 初始化默认特征
                self.features[risk_type] = default_features[risk_type]
                
                # 加载模型文件
                model_file = os.path.join(models_dir, f'{risk_type}_model.joblib')
                
                if os.path.exists(model_file):
                    try:
                        model = joblib.load(model_file)
                        # 检查模型是否有必要的方法
                        if hasattr(model, 'predict') and hasattr(model, 'predict_proba'):
                            self.models[risk_type] = model
                            
                            # 加载模型信息
                            info_file = os.path.join(models_dir, f'{risk_type}_model_info.json')
                            info = {'model_type': 'unknown'}
                            
                            if os.path.exists(info_file):
                                try:
                                    with open(info_file, 'r', encoding='utf-8') as f:
                                        file_info = json.load(f)
                                    # 更新模型信息
                                    info.update(file_info)
                                    
                                    # 如果有特征信息，使用它
                                    if 'performance' in file_info and 'features' in file_info['performance']:
                                        self.features[risk_type] = file_info['performance']['features']
                                except Exception as e:
                                    print(f"加载 {risk_type} 模型信息失败: {e}")
                            
                            self.model_info[risk_type] = info
                            print(f"成功加载 {risk_type} 模型: {info.get('model_type', 'unknown')}")
                            
                            # 如果有ROC AUC信息，打印它
                            if 'performance' in info and 'roc_auc' in info['performance']:
                                print(f"性能指标: ROC AUC = {info['performance']['roc_auc']:.4f}")
                        else:
                            print(f"{risk_type} 模型不完整，缺少必要的预测方法")
                    except Exception as e:
                        print(f"加载 {risk_type} 模型文件时出现异常: {e}")
                else:
                    print(f"警告: {risk_type} 模型文件不存在")
                
                # 尝试加载预处理器
                preprocessor_path = os.path.join(models_dir, f'{risk_type}_preprocessor.joblib')
                if os.path.exists(preprocessor_path):
                    try:
                        preprocessor = joblib.load(preprocessor_path)
                        self.preprocessors[risk_type] = preprocessor
                    except Exception as e:
                        print(f"加载 {risk_type} 预处理器失败: {e}")
                
                # 初始化last_used_ml标记
                self.last_used_ml[risk_type] = False
                    
            except Exception as e:
                print(f"加载 {risk_type} 模型失败: {e}")
                # 确保即使失败也有默认特征
                self.features[risk_type] = default_features[risk_type]
                self.last_used_ml[risk_type] = False
    
    def preprocess_input(self, patient_data, risk_type):
        """
        预处理输入数据，使其符合模型要求
        
        Args:
            patient_data (dict): 患者原始数据
            risk_type (str): 风险类型
            
        Returns:
            np.array: 预处理后的数据
        """
        try:
            # 获取该风险类型所需的特征
            if risk_type not in self.features or not self.features[risk_type]:
                print(f"未找到 {risk_type} 的特征配置")
                return None
            
            # 创建特征数据框
            df = pd.DataFrame([patient_data])
            
            # 确保所有需要的特征都存在
            input_features = []
            for feature in self.features[risk_type]:
                if feature in df.columns and pd.notna(df[feature].values[0]):
                    # 确保值是数字类型
                    try:
                        value = float(df[feature].values[0])
                        if not np.isnan(value):
                            input_features.append(value)
                        else:
                            input_features.append(0.0)  # 替换nan为默认值
                    except (ValueError, TypeError):
                        input_features.append(0.0)  # 替换非数字为默认值
                else:
                    input_features.append(0.0)  # 默认值
            
            # 确保至少有一个有效特征
            if not input_features:
                print("没有有效的特征可用")
                return None
            
            # 转换为numpy数组并重塑为2D数组
            features_array = np.array(input_features, dtype=float).reshape(1, -1)
            return features_array
        except Exception as e:
            print(f"预处理特征时出错: {e}")
            # 返回默认特征数组
            return np.zeros((1, len(self.features.get(risk_type, []))), dtype=float)
    
    def is_ml_available(self, model_type: str = None) -> bool:
        """
        检查机器学习模型是否可用
        
        Args:
            model_type: 可选，指定要检查的模型类型
                - preeclampsia: 子痫前期模型
                - gestational_diabetes: 妊娠期糖尿病模型
                - preterm_birth: 早产模型
                - None: 检查所有模型
        
        Returns:
            bool: 如果指定的模型可用，则返回True；如果检查所有模型，则当任一模型可用时返回True
        """
        if model_type is not None:
            return model_type in self.models and self.models[model_type] is not None
        else:
            # 检查是否有任何模型可用
            return any(model is not None for model in self.models.values())
    
    def _predict_with_ml(self, risk_type, patient_data):
        """
        使用机器学习模型进行预测
        
        Args:
            risk_type (str): 风险类型
            patient_data (dict): 患者数据
            
        Returns:
            dict or None: 风险评估结果或None（如果预测失败）
        """
        try:
            # 验证模型存在且有效
            if risk_type not in self.models or self.models[risk_type] is None:
                print(f"未找到可用的 {risk_type} 模型")
                return None
            
            # 预处理输入数据
            input_data = self.preprocess_input(patient_data, risk_type)
            
            # 检查特征是否有效
            if input_data is None or input_data.size == 0 or np.isnan(input_data).any():
                print("输入特征包含无效值或为空")
                return None
            
            # 获取模型和模型信息
            model = self.models[risk_type]
            if risk_type not in self.model_info:
                print(f"未找到 {risk_type} 的模型信息")
                return None
            info = self.model_info[risk_type]
            
            # 预测概率 - 添加try-except捕获特征数量不匹配的错误
            try:
                probability = model.predict_proba(input_data)[0][1]
                
                # 转换为风险等级
                if probability >= 0.7:
                    risk_level = '高风险'
                elif probability >= 0.4:
                    risk_level = '中风险'
                else:
                    risk_level = '低风险'
                
                # 获取风险因素
                risk_factors = self._identify_risk_factors(patient_data, risk_type)
                
                # 获取建议
                recommendations = self._get_recommendations(risk_type)
                
                # 设置使用了机器学习的标记
                self.last_used_ml[risk_type] = True
                
                return {
                    'risk_type': risk_type,
                    'risk_level': risk_level,
                    'risk_probability': round(probability, 2),
                    'top_risk_factors': risk_factors,
                    'recommendations': recommendations,
                    'model_type': info['model_type']
                }
            except ValueError as e:
                # 捕获特征数量不匹配的错误
                if "features as input" in str(e) or "维度不匹配" in str(e):
                    print(f"特征数量不匹配错误: {e}")
                    print(f"尝试使用的特征: {self.features.get(risk_type, [])}")
                    print(f"输入的特征数量: {input_data.shape[1]}")
                else:
                    print(f"预测过程中出错: {e}")
                self.last_used_ml[risk_type] = False
                return None
        except Exception as e:
            print(f"机器学习预测失败: {e}")
            self.last_used_ml[risk_type] = False
            return None
    
    def _predict_gestational_diabetes_rules(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """基于规则的妊娠期糖尿病风险预测（备用方法）"""
        # 基于BMI、血糖和年龄计算风险，确保转换为数值类型
        try:
            bmi = float(patient_data.get('bmi', 22))
        except (ValueError, TypeError):
            bmi = 22
        try:
            glucose_level = float(patient_data.get('glucose_level', 90))
        except (ValueError, TypeError):
            glucose_level = 90
        try:
            age = int(patient_data.get('age', 30))
        except (ValueError, TypeError):
            age = 30
        
        # 生成有意义的风险因素
        risk_factors = []
        if bmi > 28:
            risk_factors.append({'name': '体重指数过高', 'importance': 0.7})
        if glucose_level > 100:
            risk_factors.append({'name': '血糖水平偏高', 'importance': 0.8})
        if age > 35:
            risk_factors.append({'name': '高龄产妇', 'importance': 0.5})
        
        # 计算基于规则的风险概率
        risk_probability = 0.15  # 基础风险
        if bmi > 28:
            risk_probability += 0.3
        if glucose_level > 100:
            risk_probability += 0.35
        if age > 35:
            risk_probability += 0.2
        
        # 确保概率在0-1范围内
        risk_probability = min(0.95, max(0.05, risk_probability))
        # 保留2位小数
        risk_probability = round(risk_probability, 2)
        
        return {
            'risk_type': 'gestational_diabetes',
            'risk_level': '高风险' if risk_probability >= 0.7 else ('中风险' if risk_probability >= 0.4 else '低风险'),
            'risk_probability': risk_probability,
            'top_risk_factors': risk_factors,
            'recommendations': ['保持健康饮食', '适当运动', '定期监测血糖'],
            'model_type': 'rule_based'
        }
    
    def _predict_preeclampsia_rules(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """基于规则的子痫前期风险预测（备用方法）"""
        # 基于血压计算风险因素，确保转换为数值类型
        try:
            blood_pressure = float(patient_data.get('blood_pressure', 120))
        except (ValueError, TypeError):
            blood_pressure = 120
        try:
            age = int(patient_data.get('age', 30))
        except (ValueError, TypeError):
            age = 30
        
        # 生成有意义的风险因素
        risk_factors = []
        if blood_pressure > 140:
            risk_factors.append({'name': '血压偏高', 'importance': 0.8})
        if age > 40:
            risk_factors.append({'name': '高龄产妇', 'importance': 0.6})
        
        # 计算基于规则的风险概率
        risk_probability = 0.2  # 基础风险
        if blood_pressure > 140:
            risk_probability += 0.3
        if age > 40:
            risk_probability += 0.2
        
        # 确保概率在0-1范围内
        risk_probability = min(0.95, max(0.05, risk_probability))
        # 保留2位小数
        risk_probability = round(risk_probability, 2)
        
        return {
            'risk_type': 'preeclampsia',
            'risk_level': '高风险' if risk_probability >= 0.7 else ('中风险' if risk_probability >= 0.4 else '低风险'),
            'risk_probability': risk_probability,
            'top_risk_factors': risk_factors,
            'recommendations': ['请咨询医生获取专业建议', '定期进行产检', '注意监测血压变化'],
            'model_type': 'rule_based'
        }
    
    def _predict_preterm_birth_rules(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """基于规则的早产风险预测（备用方法）"""
        # 基于孕周和血压计算风险，确保转换为数值类型
        try:
            pregnancy_weeks = float(patient_data.get('pregnancy_weeks', 28))
        except (ValueError, TypeError):
            pregnancy_weeks = 28
        try:
            blood_pressure = float(patient_data.get('blood_pressure', 120))
        except (ValueError, TypeError):
            blood_pressure = 120
        
        # 生成有意义的风险因素
        risk_factors = []
        if pregnancy_weeks < 24:
            risk_factors.append({'name': '孕周较小', 'importance': 0.6})
        if blood_pressure > 140:
            risk_factors.append({'name': '血压偏高', 'importance': 0.5})
        if patient_data.get('previous_preterm', 0) == 1:
            risk_factors.append({'name': '既往早产史', 'importance': 0.7})
        
        # 计算基于规则的风险概率
        risk_probability = 0.1  # 基础风险
        if pregnancy_weeks < 24:
            risk_probability += 0.3
        if blood_pressure > 140:
            risk_probability += 0.2
        if patient_data.get('previous_preterm', 0) == 1:
            risk_probability += 0.3
        
        # 确保概率在0-1范围内
        risk_probability = min(0.95, max(0.05, risk_probability))
        # 保留2位小数
        risk_probability = round(risk_probability, 2)
        
        return {
            'risk_type': 'preterm_birth',
            'risk_level': '高风险' if risk_probability >= 0.7 else ('中风险' if risk_probability >= 0.4 else '低风险'),
            'risk_probability': risk_probability,
            'top_risk_factors': risk_factors,
            'recommendations': ['避免剧烈活动', '保持充分休息', '定期产检监测宫颈长度'],
            'model_type': 'rule_based'
        }
    
    def predict_gestational_diabetes_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """预测妊娠期糖尿病风险"""
        try:
            # 首先尝试使用机器学习模型
            if 'gestational_diabetes' in self.models:
                ml_result = self._predict_with_ml('gestational_diabetes', patient_data)
                # 检查机器学习预测是否返回了有效结果
                if ml_result is not None:
                    return ml_result
                # 如果机器学习预测返回None，回退到基于规则的方法
                print("机器学习预测返回None，回退到基于规则的方法")
            
            # 回退到基于规则的方法
            self.last_used_ml['gestational_diabetes'] = False
            # 确保使用与测试用例匹配的字段名
            # 如果blood_sugar存在，将其赋值给glucose_level用于规则预测
            if 'blood_sugar' in patient_data:
                patient_data_copy = patient_data.copy()
                patient_data_copy['glucose_level'] = patient_data['blood_sugar']
                return self._predict_gestational_diabetes_rules(patient_data_copy)
            return self._predict_gestational_diabetes_rules(patient_data)
                
        except Exception as e:
            # 如果机器学习预测失败，使用基于规则的方法
            print(f"机器学习预测失败，使用基于规则的方法: {e}")
            self.last_used_ml['gestational_diabetes'] = False
            # 确保使用与测试用例匹配的字段名
            if 'blood_sugar' in patient_data:
                patient_data_copy = patient_data.copy()
                patient_data_copy['glucose_level'] = patient_data['blood_sugar']
                return self._predict_gestational_diabetes_rules(patient_data_copy)
            return self._predict_gestational_diabetes_rules(patient_data)
    
    def predict_preeclampsia_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """预测子痫前期风险"""
        try:
            # 首先尝试使用机器学习模型
            if 'preeclampsia' in self.models:
                ml_result = self._predict_with_ml('preeclampsia', patient_data)
                # 检查机器学习预测是否返回了有效结果
                if ml_result is not None:
                    return ml_result
                # 如果机器学习预测返回None，回退到基于规则的方法
                print("机器学习预测返回None，回退到基于规则的方法")
            
            # 回退到基于规则的方法
            self.last_used_ml['preeclampsia'] = False
            # 确保使用与规则匹配的字段名
            patient_data_copy = patient_data.copy()
            # 如果有收缩压和舒张压，计算平均血压作为blood_pressure
            if 'systolic_pressure' in patient_data and 'diastolic_pressure' in patient_data:
                patient_data_copy['blood_pressure'] = (patient_data['systolic_pressure'] + patient_data['diastolic_pressure']) / 2
            elif 'systolic_pressure' in patient_data:
                patient_data_copy['blood_pressure'] = patient_data['systolic_pressure']
            return self._predict_preeclampsia_rules(patient_data_copy)
                
        except Exception as e:
            # 如果机器学习预测失败，使用基于规则的方法
            print(f"机器学习预测失败，使用基于规则的方法: {e}")
            self.last_used_ml['preeclampsia'] = False
            # 确保使用与规则匹配的字段名
            patient_data_copy = patient_data.copy()
            # 如果有收缩压和舒张压，计算平均血压作为blood_pressure
            if 'systolic_pressure' in patient_data and 'diastolic_pressure' in patient_data:
                patient_data_copy['blood_pressure'] = (patient_data['systolic_pressure'] + patient_data['diastolic_pressure']) / 2
            elif 'systolic_pressure' in patient_data:
                patient_data_copy['blood_pressure'] = patient_data['systolic_pressure']
            return self._predict_preeclampsia_rules(patient_data_copy)
    
    def predict_preterm_birth_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """预测早产风险"""
        try:
            # 首先尝试使用机器学习模型
            if 'preterm_birth' in self.models:
                ml_result = self._predict_with_ml('preterm_birth', patient_data)
                # 检查机器学习预测是否返回了有效结果
                if ml_result is not None:
                    return ml_result
                # 如果机器学习预测返回None，回退到基于规则的方法
                print("机器学习预测返回None，回退到基于规则的方法")
            
            # 回退到基于规则的方法
            self.last_used_ml['preterm_birth'] = False
            # 确保使用与规则匹配的字段名
            patient_data_copy = patient_data.copy()
            if 'gestational_weeks' in patient_data and 'pregnancy_weeks' not in patient_data:
                patient_data_copy['pregnancy_weeks'] = patient_data['gestational_weeks']
            # 为了确保blood_pressure字段存在（基于规则的预测需要），提供默认值
            if 'blood_pressure' not in patient_data_copy:
                patient_data_copy['blood_pressure'] = patient_data.get('systolic_pressure', 120)
            return self._predict_preterm_birth_rules(patient_data_copy)
                
        except Exception as e:
            # 如果机器学习预测失败，使用基于规则的方法
            print(f"机器学习预测失败，使用基于规则的方法: {e}")
            self.last_used_ml['preterm_birth'] = False
            # 确保使用与规则匹配的字段名
            patient_data_copy = patient_data.copy()
            if 'gestational_weeks' in patient_data and 'pregnancy_weeks' not in patient_data:
                patient_data_copy['pregnancy_weeks'] = patient_data['gestational_weeks']
            # 为了确保blood_pressure字段存在（基于规则的预测需要），提供默认值
            if 'blood_pressure' not in patient_data_copy:
                patient_data_copy['blood_pressure'] = patient_data.get('systolic_pressure', 120)
            return self._predict_preterm_birth_rules(patient_data_copy)
    
    def _identify_risk_factors(self, patient_data, risk_type):
        """
        识别患者的风险因素
        
        Args:
            patient_data (dict): 患者数据
            risk_type (str): 风险类型
            
        Returns:
            list: 风险因素列表
        """
        risk_factors = []
        
        if risk_type == 'gestational_diabetes':
            # 年龄因素
            if patient_data.get('age', 0) >= 35:
                risk_factors.append({'name': '高龄产妇', 'importance': 0.5})
                
            # BMI因素
            bmi = patient_data.get('bmi', 0)
            if bmi >= 28:
                risk_factors.append({'name': '体重指数过高', 'importance': 0.7})
            elif bmi >= 24:
                risk_factors.append({'name': '体重指数偏高', 'importance': 0.4})
            
            # 血糖
            glucose_level = patient_data.get('glucose_level', 0)
            if glucose_level >= 100:
                risk_factors.append({'name': '血糖水平偏高', 'importance': 0.8})
            
        elif risk_type == 'preeclampsia':
            # 年龄因素
            if patient_data.get('age', 0) >= 40:
                risk_factors.append({'name': '高龄产妇', 'importance': 0.6})
            
            # 血压
            blood_pressure = patient_data.get('blood_pressure', 0)
            if blood_pressure >= 140:
                risk_factors.append({'name': '血压偏高', 'importance': 0.8})
            elif blood_pressure >= 130:
                risk_factors.append({'name': '血压处于正常高值', 'importance': 0.5})
            
        elif risk_type == 'preterm_birth':
            # 孕周
            pregnancy_weeks = patient_data.get('pregnancy_weeks', 0)
            if pregnancy_weeks < 24:
                risk_factors.append({'name': '孕周较小', 'importance': 0.6})
            
            # 血压
            blood_pressure = patient_data.get('blood_pressure', 0)
            if blood_pressure >= 140:
                risk_factors.append({'name': '血压偏高', 'importance': 0.5})
        
        return risk_factors
    
    def _get_recommendations(self, risk_type):
        """
        获取针对不同风险类型的建议
        
        Args:
            risk_type (str): 风险类型
            
        Returns:
            list: 建议列表
        """
        recommendations = {
            'gestational_diabetes': [
                '保持健康饮食',
                '适当运动',
                '定期监测血糖'
            ],
            'preeclampsia': [
                '请咨询医生获取专业建议',
                '定期进行产检',
                '注意监测血压变化'
            ],
            'preterm_birth': [
                '避免剧烈运动',
                '保持良好休息',
                '如有不适及时就医'
            ]
        }
        
        return recommendations.get(risk_type, [])
    
    def predict_comprehensive_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合风险评估
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            综合风险预测结果字典
        """
        try:
            # 预测各类风险
            preeclampsia_result = self.predict_preeclampsia_risk(patient_data)
            gestational_diabetes_result = self.predict_gestational_diabetes_risk(patient_data)
            preterm_birth_result = self.predict_preterm_birth_risk(patient_data)
            
            # 确保所有预测方法都返回了有效结果
            if not preeclampsia_result:
                preeclampsia_result = self._get_default_risk_result('preeclampsia')
            if not gestational_diabetes_result:
                gestational_diabetes_result = self._get_default_risk_result('gestational_diabetes')
            if not preterm_birth_result:
                preterm_birth_result = self._get_default_risk_result('preterm_birth')
            
            # 计算综合风险评分
            risk_scores = [
                preeclampsia_result['risk_probability'],
                gestational_diabetes_result['risk_probability'],
                preterm_birth_result['risk_probability']
            ]
            risk_factors = []
            risk_factors.extend(preeclampsia_result.get('top_risk_factors', []))
            risk_factors.extend(gestational_diabetes_result.get('top_risk_factors', []))
            risk_factors.extend(preterm_birth_result.get('top_risk_factors', []))
            
            # 计算平均风险
            overall_risk = np.mean(risk_scores)
            # 保留2位小数
            overall_risk = round(overall_risk, 2)
            
            # 确定风险等级
            if overall_risk >= 0.7:
                risk_level = '高风险'
            elif overall_risk >= 0.4:
                risk_level = '中风险'
            else:
                risk_level = '低风险'
            
            # 合并风险因素（去重）
            unique_factors = {}
            for factor in risk_factors:
                if isinstance(factor, dict) and 'name' in factor and 'importance' in factor:
                    name = factor['name']
                    if name not in unique_factors or factor['importance'] > unique_factors[name]['importance']:
                        unique_factors[name] = factor
            
            # 按重要性排序
            sorted_factors = sorted(unique_factors.values(), key=lambda x: x['importance'], reverse=True)[:5]
            
            # 获取个性化的健康建议
            personalized_recommendations = self.get_comprehensive_recommendations(risk_level, overall_risk, patient_data)
            
            # 创建综合结果 - 移除'data'包装层
            result = {
                'comprehensive': {
                    'overall_risk_level': risk_level,
                    'overall_risk_score': overall_risk,
                    'risk_description': f'根据您的健康数据分析，您的综合风险等级为{risk_level}。',
                    'recommendations': personalized_recommendations
                },
                'preeclampsia': {
                    'risk_level': preeclampsia_result['risk_level'],
                    'risk_score': round(preeclampsia_result['risk_probability'] * 100, 2),
                    'description': f'子痫前期风险等级为{preeclampsia_result["risk_level"]}。',
                    'key_factors': [factor['name'] for factor in preeclampsia_result.get('top_risk_factors', [])[:3] if isinstance(factor, dict) and 'name' in factor]
                },
                'gestational_diabetes': {
                    'risk_level': gestational_diabetes_result['risk_level'],
                    'risk_score': round(gestational_diabetes_result['risk_probability'] * 100, 2),
                    'description': f'妊娠期糖尿病风险等级为{gestational_diabetes_result["risk_level"]}。',
                    'key_factors': [factor['name'] for factor in gestational_diabetes_result.get('top_risk_factors', [])[:3] if isinstance(factor, dict) and 'name' in factor]
                },
                'preterm_birth': {
                    'risk_level': preterm_birth_result['risk_level'],
                    'risk_score': round(preterm_birth_result['risk_probability'] * 100, 2),
                    'description': f'早产风险等级为{preterm_birth_result["risk_level"]}。',
                    'key_factors': [factor['name'] for factor in preterm_birth_result.get('top_risk_factors', [])[:3] if isinstance(factor, dict) and 'name' in factor]
                },
                'top_risk_factors': sorted_factors,
                'overall_risk_level': risk_level,
                'overall_risk_score': overall_risk,
                'recommendations': personalized_recommendations
            }
            
            return result
            
        except Exception as e:
            print(f"综合风险评估错误: {e}")
            import traceback
            traceback.print_exc()
            # 返回默认的错误响应
            return {
                'comprehensive': {
                    'overall_risk_level': '低风险',
                    'overall_risk_score': 0.3,
                    'risk_description': '预测过程中发生错误，请稍后再试。',
                    'recommendations': ['请咨询医生获取专业建议', '定期进行产检', '保持健康的生活方式']
                },
                'preeclampsia': {
                    'risk_level': '低风险',
                    'risk_score': 30.0,
                    'description': '子痫前期风险等级为低风险。',
                    'key_factors': []
                },
                'gestational_diabetes': {
                    'risk_level': '低风险',
                    'risk_score': 25.0,
                    'description': '妊娠期糖尿病风险等级为低风险。',
                    'key_factors': []
                },
                'preterm_birth': {
                    'risk_level': '低风险',
                    'risk_score': 20.0,
                    'description': '早产风险等级为低风险。',
                    'key_factors': []
                },
                'top_risk_factors': [],
                'overall_risk_level': '低风险',
                'overall_risk_score': 0.3,
                'recommendations': ['请咨询医生获取专业建议', '定期进行产检', '保持健康的生活方式']
            }
    
    def _get_risk_level(self, probability: float) -> str:
        """根据概率获取风险等级"""
        if probability >= 0.7:
            return '高风险'
        elif probability >= 0.4:
            return '中风险'
        else:
            return '低风险'
            
    def _get_default_risk_result(self, risk_type: str) -> Dict[str, Any]:
        """
        获取默认的风险结果，确保即使预测失败也能返回有效的结构
        
        Args:
            risk_type: 风险类型
            
        Returns:
            默认的风险结果字典
        """
        default_scores = {
            'preeclampsia': 0.35,
            'gestational_diabetes': 0.30,
            'preterm_birth': 0.25
        }
        
        risk_score = default_scores.get(risk_type, 0.3)
        risk_level = self._get_risk_level(risk_score)
        
        return {
            'risk_type': risk_type,
            'risk_level': risk_level,
            'risk_probability': risk_score,
            'top_risk_factors': [],
            'recommendations': []
        }
    
    def get_comprehensive_recommendations(self, risk_level: str, risk_score: float, patient_data: Dict[str, Any] = None) -> List[str]:
        """
        根据风险等级、风险分数和患者数据提供个性化的综合建议
        
        Args:
            risk_level: 风险等级
            risk_score: 风险分数
            patient_data: 患者数据字典（可选）
            
        Returns:
            建议列表
        """
        recommendations = []
        patient_data = patient_data or {}
        
        # 基础建议
        recommendations.append('请咨询医生获取专业建议')
        recommendations.append('定期进行产检')
        
        # 获取患者具体数据用于个性化建议
        blood_pressure = patient_data.get('blood_pressure', 120)
        bmi = patient_data.get('bmi', 22)
        glucose_level = patient_data.get('glucose_level', 90)
        age = patient_data.get('age', 30)
        pregnancy_weeks = patient_data.get('pregnancy_weeks', 28)
        
        # 根据风险等级添加建议
        if risk_level == '高风险':
            recommendations.append('建议每周进行一次产检，密切监测母婴健康状况')
            recommendations.append('注意休息，保证充足睡眠，避免劳累和精神压力')
            recommendations.append('记录并及时向医生报告任何异常症状，如头痛、视力模糊、腹痛等')
            recommendations.append('考虑提前准备待产计划和紧急联系方式')
        elif risk_level == '中风险':
            recommendations.append('建议每2周进行一次产检，关注各项指标变化')
            recommendations.append('保持良好心态，适当进行放松活动如散步、孕妇瑜伽')
            recommendations.append('建立健康记录本，追踪血压、体重等关键指标')
        else:  # 低风险
            recommendations.append('继续保持当前的健康生活习惯')
            recommendations.append('建议按常规频率进行产检')
            recommendations.append('适当进行户外活动，保持积极乐观的心态')
        
        # 基于具体风险因素的个性化建议
        if blood_pressure > 140:
            recommendations.append('建议低盐饮食，每日盐摄入量不超过5克')
            recommendations.append('避免长时间站立或久坐，适当活动促进血液循环')
            recommendations.append('定期监测血压，建议每日测量并记录')
        elif blood_pressure < 100:
            recommendations.append('注意饮食营养均衡，适当增加优质蛋白质摄入')
            recommendations.append('避免突然改变体位，防止体位性低血压')
        
        if bmi > 28:
            recommendations.append('建议在医生指导下适当控制体重增长')
            recommendations.append('采用低脂、高纤维的饮食结构，控制总热量摄入')
            recommendations.append('进行适合孕期的有氧运动，如散步、游泳等')
        elif bmi < 18.5:
            recommendations.append('建议适当增加营养摄入，保证母婴健康')
            recommendations.append('多食用富含优质蛋白质和维生素的食物')
        
        if glucose_level > 100:
            recommendations.append('建议控制碳水化合物摄入，选择低糖指数食物')
            recommendations.append('采用少食多餐的饮食方式，避免血糖波动过大')
            recommendations.append('定期监测血糖水平，关注变化趋势')
        
        if age > 35:
            recommendations.append('建议增加产前筛查项目，密切关注胎儿发育情况')
            recommendations.append('注意补充叶酸和其他必需维生素')
        
        if pregnancy_weeks < 24:
            recommendations.append('特别注意休息，避免剧烈运动和性生活')
            recommendations.append('避免接触有害物质，如烟草、酒精、辐射等')
            recommendations.append('保持良好的口腔卫生，预防口腔感染')
        
        # 通用健康生活建议
        recommendations.append('保持充足水分摄入，每日饮水约2000ml')
        recommendations.append('保证均衡饮食，多摄入新鲜蔬菜和水果')
        recommendations.append('避免熬夜，建立规律的作息时间')
        
        # 限制建议数量，避免信息过载
        return recommendations[:10]  # 最多返回10条建议
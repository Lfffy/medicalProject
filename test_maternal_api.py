#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的孕产妇风险预测API测试应用
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'maternal_risk_test_key'
CORS(app)

# 导入预测器
try:
    from maternal_risk_predictor import MaternalRiskPredictor
    predictor = MaternalRiskPredictor()
    print("预测器初始化成功")
except Exception as e:
    print(f"预测器初始化失败: {e}")
    predictor = None

# 健康检查端点
@app.route('/api/maternal-risk/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': predictor is not None
    })

# 模型训练端点
@app.route('/api/maternal-risk/train/models', methods=['POST'])
def train_models():
    """训练模型"""
    try:
        if predictor is None:
            return jsonify({
                'error': '预测器未初始化',
                'success': False
            }), 500
            
        # 获取请求数据
        data = request.get_json() or {}
        data_path = data.get('data_path', 'data/maternal_data.csv')
        
        # 检查数据文件是否存在
        if not os.path.exists(data_path):
            return jsonify({
                'error': f'数据文件不存在: {data_path}',
                'success': False
            }), 400
        
        # 训练模型
        result = predictor.train_all_models(data_path)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'训练过程中发生错误: {str(e)}',
            'success': False
        }), 500

# 综合风险预测端点
@app.route('/api/maternal-risk/predict/comprehensive', methods=['POST'])
def predict_comprehensive():
    """综合风险评估"""
    try:
        if predictor is None:
            return jsonify({
                'error': '预测器未初始化',
                'success': False
            }), 500
            
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

# 根路径
@app.route('/')
def home():
    return jsonify({
        'message': '孕产妇风险预测API测试服务',
        'version': '1.0.0',
        'endpoints': [
            '/api/maternal-risk/health',
            '/api/maternal-risk/train/models',
            '/api/maternal-risk/predict/comprehensive'
        ]
    })

if __name__ == '__main__':
    print("孕产妇风险预测API测试服务启动中...")
    print("请访问: http://localhost:8083")
    app.run(debug=True, host='0.0.0.0', port=8083)
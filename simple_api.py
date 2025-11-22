#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版孕产妇风险预测API
"""

from flask import Flask, request, jsonify
import json
import os
from maternal_risk_predictor import MaternalRiskPredictor

# 创建Flask应用
app = Flask(__name__)

# 初始化预测器
predictor = MaternalRiskPredictor()

# 尝试加载预训练模型
model_loaded = False
try:
    # 检查模型文件是否存在
    if os.path.exists("models/preeclampsia_model_info.json"):
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
        if os.path.exists(data_path):
            predictor.train_all_models(data_path)
            model_loaded = True
            print("模型训练成功")
        else:
            print("训练数据不存在")
    except Exception as e:
        print(f"模型训练失败: {e}")

@app.route('/api/maternal-risk/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'service': '孕产妇风险预测API'
    })

@app.route('/api/maternal-risk/predict', methods=['POST'])
def predict_risk():
    """风险预测端点"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '未提供数据'}), 400
        
        # 预测风险
        result = predictor.predict_comprehensive_risk(data)
        
        if result is None:
            return jsonify({'error': '预测失败'}), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/maternal-risk/train', methods=['POST'])
def train_models():
    """模型训练端点"""
    try:
        # 获取请求数据
        data = request.get_json()
        data_path = data.get('data_path', 'data/maternal_data_large.json')
        
        # 训练模型
        result = predictor.train_all_models(data_path)
        
        if result is None:
            return jsonify({'error': '训练失败'}), 500
        
        return jsonify({
            'status': 'success',
            'results': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("孕产妇风险预测API启动中...")
    print("请访问: http://localhost:8084")
    app.run(debug=True, host='0.0.0.0', port=8084)
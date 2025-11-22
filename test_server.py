#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试服务启动脚本
"""

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'test_secret_key'
CORS(app)

@app.route('/')
def home():
    return "测试服务正在运行"

@app.route('/test')
def test():
    return {"status": "success", "message": "测试端点正常工作"}

if __name__ == '__main__':
    print("测试服务启动中...")
    print("请访问: http://localhost:8082")
    app.run(debug=True, host='0.0.0.0', port=8082)
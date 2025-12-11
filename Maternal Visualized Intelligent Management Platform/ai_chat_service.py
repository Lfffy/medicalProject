from flask import request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import time
import threading
import requests
import hashlib
import os
from datetime import datetime
import os
from openai import OpenAI

# 启用火山方舟大模型依赖
builtin_available = True
openai_available = True

class AIChatService:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.active_connections = {}
        self.user_sessions = {}
        
        # AI助手API配置
        self.api_key = os.environ.get('ARK_API_KEY', 'ceadb27c-39e4-4527-924d-a8bb5e81758e')  # 从环境变量获取或使用提供的密钥
        
        # 初始化火山方舟OpenAI兼容客户端
        self.client = OpenAI(
            # 火山方舟API地址
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            # 使用API密钥
            api_key=self.api_key,
        )
        print("已初始化火山方舟大模型客户端")
        
        # AI助手模型配置
        self.ai_model = "ep-20250514110428-r589j"  # 使用用户提供的火山方舟推理接入点ID
        
        # 注册WebSocket事件处理器
        self.register_handlers()
    
    def register_handlers(self):
        """注册WebSocket事件处理器"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """客户端连接事件"""
            client_id = request.sid
            print(f'客户端连接: {client_id}')
            
            # 发送欢迎消息
            emit('assistant_response', {
                'type': 'assistant_response',
                'content': '您好！我是AI智能助手，很高兴为您服务。我可以为您提供医疗健康相关的咨询和建议。请问有什么可以帮助您的吗？',
                'timestamp': time.time()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """客户端断开连接事件"""
            client_id = request.sid
            print(f'客户端断开连接: {client_id}')
            
            # 清理连接信息
            if client_id in self.active_connections:
                del self.active_connections[client_id]
        
        @self.socketio.on('user_message')
        def handle_user_message(data):
            """处理用户消息"""
            try:
                client_id = request.sid
                message = data.get('content', '').strip()
                settings = data.get('settings', {})
                
                if not message:
                    emit('error', {'message': '消息不能为空'})
                    return
                
                print(f'收到用户消息 ({client_id}): {message}')
                
                # 发送正在输入状态
                emit('typing', {'isTyping': True})
                
                # 异步处理AI响应
                def process_ai_response():
                    try:
                        response = self.generate_ai_response(message, settings)
                        
                        # 发送AI响应
                        self.socketio.emit('assistant_response', {
                            'type': 'assistant_response',
                            'content': response,
                            'timestamp': time.time()
                        }, room=client_id)
                        
                    except Exception as e:
                        print(f'AI响应生成失败: {str(e)}')
                        self.socketio.emit('error', {
                            'type': 'error',
                            'message': '抱歉，AI服务暂时不可用，请稍后再试'
                        }, room=client_id)
                    finally:
                        # 停止输入状态
                        self.socketio.emit('typing', {'isTyping': False}, room=client_id)
                
                # 启动异步处理
                thread = threading.Thread(target=process_ai_response)
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                print(f'处理用户消息失败: {str(e)}')
                emit('error', {'message': '消息处理失败'})
    
    def generate_ai_response(self, message, settings):
        """生成AI响应"""
        try:
            # 调用AI助手API
            response = self.call_ai_api(message)
            # 确保响应内容也经过清理和长度限制
            cleaned_response = self.clean_response_text(response)
            return self.limit_response_length(cleaned_response, 500)
            
        except Exception as e:
            print(f'生成AI响应失败: {str(e)}')
            # 如果API调用失败，使用模拟响应作为备选
            mock_response = self.generate_mock_response(message)
            cleaned_mock = self.clean_response_text(mock_response)
            return self.limit_response_length(cleaned_mock, 500)
    
    def call_ai_api(self, message):
        """调用OpenAI API生成自然语言响应"""
        try:
            # 导入预测器，用于专业医疗数据的处理
            from maternal_risk_predictor import MaternalRiskPredictor
            import re
            
            # 初始化预测器
            predictor = MaternalRiskPredictor()
            
            # 检查是否包含医疗风险评估相关的关键词
            medical_keywords = ['子痫前期', '子痫', '高血压', '早产', '提前分娩', 'BMI', '血压', '年龄']
            has_medical_keyword = any(keyword in message for keyword in medical_keywords)
            
            # 如果包含医疗关键词，先获取专业的医疗评估结果
            medical_analysis = ""
            if has_medical_keyword:
                # 解析用户输入，提取关键信息
                age_match = re.search(r'(?:今年)?(?:年龄)?(\d+)岁', message)
                age = int(age_match.group(1)) if age_match else 30
                
                # 处理血压格式
                blood_pressure_match = re.search(r'(?:血压)?(\d+)/(\d+)', message)
                if blood_pressure_match:
                    systolic = int(blood_pressure_match.group(1))
                    diastolic = int(blood_pressure_match.group(2))
                else:
                    systolic_match = re.search(r'收缩压(\d+)', message)
                    diastolic_match = re.search(r'舒张压(\d+)', message)
                    systolic = int(systolic_match.group(1)) if systolic_match else 120
                    diastolic = int(diastolic_match.group(1)) if diastolic_match else 80
                
                # 处理BMI格式
                bmi_match = re.search(r'BMI\s*(\d+(?:\.\d+)?)', message)
                bmi = float(bmi_match.group(1)) if bmi_match else 25.0
                
                # 创建患者数据
                patient_data = {
                    'age': age,
                    'systolic_pressure': systolic,
                    'diastolic_pressure': diastolic,
                    'bmi': bmi
                }
                
                # 进行专业医疗评估
                if '子痫前期' in message or '子痫' in message or '高血压' in message:
                    result = predictor.predict_preeclampsia_risk(patient_data)
                    risk_level = result.get('risk_level', '未知')
                    confidence = result.get('confidence', 0.0)
                    medical_analysis = f"子痫前期风险评估：等级为{risk_level}，置信度为{confidence:.2f}。"
                elif '早产' in message or '提前分娩' in message:
                    result = predictor.predict_preterm_birth_risk(patient_data)
                    risk_level = result.get('risk_level', '未知')
                    confidence = result.get('confidence', 0.0)
                    medical_analysis = f"早产风险评估：等级为{risk_level}，置信度为{confidence:.2f}。"
                else:
                    # 调用综合风险评估
                    result = predictor.predict_comprehensive_risk(patient_data)
                    if result:
                        preeclampsia_risk = result.get('preeclampsia', {}).get('risk_level', '未知')
                        preterm_risk = result.get('preterm_birth', {}).get('risk_level', '未知')
                        medical_analysis = f"综合风险评估：子痫前期风险等级为{preeclampsia_risk}，早产风险等级为{preterm_risk}。"
                    else:
                        medical_analysis = "无法提供准确的风险评估，请提供更多详细信息。"
            
            # 调用火山方舟大模型API生成自然语言响应
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "您是一位专业的医疗健康助手，基于以下医疗分析结果（如果有），用自然、友好的语言回答用户的问题。请避免使用过于专业的术语，确保回答通俗易懂。"
                    },
                    {
                        "role": "user",
                        "content": f"医疗分析结果：{medical_analysis}\n\n用户问题：{message}"
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # 获取AI生成的响应
            ai_response = response.choices[0].message.content.strip()
            return ai_response
            
        except Exception as e:
            print(f'调用OpenAI API失败: {str(e)}')
            # 如果OpenAI调用失败，使用内置的专业医疗评估作为备选
            if has_medical_keyword and medical_analysis:
                return f"{medical_analysis}建议您保持健康的生活方式，定期进行产检。"
            else:
                return "抱歉，AI服务暂时不可用，请稍后再试。"
    
    def clean_response_text(self, text):
        """清理响应文本中的乱码符号"""
        if not text:
            return text
            
        # 移除常见的乱码符号和不必要的字符
        import re
        
        # 移除特殊Unicode字符和乱码
        text = re.sub(r'[\u0000-\u001F\u007F-\u009F]', '', text)  # 控制字符
        text = re.sub(r'[\uFFFD]', '', text)  # 替换字符
        text = re.sub(r'[\uFEFF]', '', text)  # BOM字符
        
        # 移除多余的空格和换行
        text = re.sub(r'\n\s*\n', '\n\n', text)  # 多个空行
        text = re.sub(r' +', ' ', text)  # 多个空格
        text = re.sub(r'\s+$', '', text)  # 行尾空格
        
        # 移除Markdown格式符号（保留基本的换行）
        text = re.sub(r'#{1,6}\s*', '', text)  # 标题符号
        text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)  # 粗体斜体
        text = re.sub(r'`([^`]+)`', r'\1', text)  # 代码标记
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # 链接
        
        # 移除emoji（保留基本的表情符号）
        text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '', text)
        
        return text.strip()
    
    def limit_response_length(self, text, max_length=500):
        """限制响应文本长度"""
        if not text:
            return text
            
        if len(text) <= max_length:
            return text
            
        # 在合适的位置截断，避免在句子中间截断
        truncated = text[:max_length]
        
        # 寻找最近的句号、感叹号或问号
        for i in range(len(truncated) - 1, max(0, len(truncated) - 50), -1):
            if truncated[i] in ['。', '！', '？', '.', '!', '?']:
                return truncated[:i + 1]
        
        # 如果没有找到合适的标点，在逗号或分号处截断
        for i in range(len(truncated) - 1, max(0, len(truncated) - 30), -1):
            if truncated[i] in ['，', '；', ',', ';']:
                return truncated[:i + 1]
        
        # 最后直接截断并添加省略号
        return truncated + '...'
    
    def generate_mock_response(self, message):
        """移除模拟响应生成函数，仅保留接口以避免调用错误"""
        return "请通过系统的预测功能获取专业的健康风险评估。"
    
    def get_connection_stats(self):
        """获取连接统计信息"""
        return {
            'active_connections': len(self.active_connections),
            'user_sessions': len(self.user_sessions)
        }

# 初始化AI聊天服务
def init_ai_chat_service(socketio):
    """初始化AI聊天服务"""
    return AIChatService(socketio)
from flask import request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import time
import threading
import requests
import hashlib
import os
from datetime import datetime
from openai import OpenAI

class AIChatService:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.active_connections = {}
        self.user_sessions = {}
        
        # 豆包API配置 - 使用环境变量获取API Key
        api_key = os.getenv('ARK_API_KEY')
        if not api_key:
            print("警告: 未设置ARK_API_KEY环境变量，将使用模拟响应")
            api_key = "your-doubao-api-key-here"  # 占位符
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key
        )
        
        # 豆包模型配置
        self.doubao_model = "doubao-seed-1-6-251015"  # 使用您提供的模型ID
        
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
            # 调用豆包API
            response = self.call_doubao_api(message)
            # 确保响应内容也经过清理和长度限制
            cleaned_response = self.clean_response_text(response)
            return self.limit_response_length(cleaned_response, 500)
            
        except Exception as e:
            print(f'生成AI响应失败: {str(e)}')
            # 如果API调用失败，使用模拟响应作为备选
            mock_response = self.generate_mock_response(message)
            cleaned_mock = self.clean_response_text(mock_response)
            return self.limit_response_length(cleaned_mock, 500)
    
    def call_doubao_api(self, message):
        """调用豆包API - 使用OpenAI客户端格式"""
        try:
            # 检查API Key是否已配置
            if not hasattr(self.client, 'api_key') or self.client.api_key == "your-doubao-api-key-here":
                print("豆包API Key未正确配置，使用模拟响应")
                return self.generate_mock_response(message)
            
            # 构建消息，添加医疗健康系统人设
            messages = [
                {
                    "role": "system",
                    "content": """你是一个专业的医疗健康AI助手，具有以下特点：
1. 专业性：具备丰富的医疗健康知识，能够提供准确的健康建议
2. 责任感：始终提醒用户重要症状需要就医，不替代专业医生诊断
3. 关怀性：以温和、专业的语调与用户交流
4. 实用性：提供实用的健康建议和生活指导
5. 安全性：对于严重症状，始终建议及时就医
6. 简洁性：回答控制在500字以内，简洁明了，避免冗长

请根据用户的问题，提供专业、准确、安全且简洁的医疗健康建议，确保回答不超过500字。"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
            
            # 使用OpenAI客户端调用豆包API
            response = self.client.chat.completions.create(
                model=self.doubao_model,
                messages=messages,
                temperature=0.7,
                max_tokens=800  # 限制token数量，确保输出在500字以内
            )
            
            # 提取响应内容
            if response.choices and len(response.choices) > 0:
                raw_response = response.choices[0].message.content
                # 清理和限制响应内容
                cleaned_response = self.clean_response_text(raw_response)
                return self.limit_response_length(cleaned_response, 500)
            else:
                print('豆包API返回格式异常')
                return self.generate_mock_response(message)
                
        except Exception as e:
            print(f'调用豆包API异常: {str(e)}')
            # 如果是认证错误，提示检查API Key
            if "AuthenticationError" in str(e) or "401" in str(e):
                print("API Key认证失败，请检查ARK_API_KEY环境变量是否正确设置")
            return self.generate_mock_response(message)
    
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
        """生成模拟AI响应"""
        message_lower = message.lower()
        
        # 医疗相关关键词检测
        if any(keyword in message_lower for keyword in ['头痛', '发烧', '感冒', '咳嗽', '症状']):
            response = (
                '我理解您对身体症状的关注。请注意，我是一个AI助手，不能替代专业医生的诊断。'
                '一般建议：1. 如果症状轻微，可以多休息、多喝水 2. 观察症状变化，如有加重请及时就医 '
                '3. 保持良好的生活习惯和作息 4. 如有疑问，建议咨询专业医生。请问您还有其他需要了解的吗？'
            )
            return self.limit_response_length(response, 500)
        
        elif any(keyword in message_lower for keyword in ['健康', '预防', '保健', '运动']):
            response = (
                '健康的生活方式对预防疾病非常重要。运动建议：每周至少150分钟中等强度运动，包括有氧运动和力量训练。'
                '饮食建议：均衡饮食，多吃蔬菜水果，控制油盐糖的摄入。作息建议：保证7-8小时充足睡眠，规律作息，避免熬夜。'
                '适当放松，减轻压力。希望这些建议对您有帮助！'
            )
            return self.limit_response_length(response, 500)
        
        elif any(keyword in message_lower for keyword in ['你好', 'hello', 'hi', '您好']):
            response = (
                '您好！我是您的AI健康助手。我可以为您提供健康咨询、数据分析、用药指导、运动建议和营养指导。'
                '请告诉我您需要什么帮助，我会尽力为您提供专业、准确的建议。'
            )
            return self.limit_response_length(response, 500)
        
        elif any(keyword in message_lower for keyword in ['谢谢', '感谢', 'thank']):
            response = (
                '不客气！很高兴能帮助到您。如果您还有其他问题，随时可以问我。祝您身体健康，生活愉快！'
            )
            return self.limit_response_length(response, 500)
        
        else:
            response = (
                '感谢您的提问。作为AI健康助手，我会尽力为您提供有用的信息。'
                '如果您有具体的健康问题，建议详细描述您的症状或问题，提供相关的背景信息。'
                '如有严重症状，请及时就医。我还可以帮您分析健康数据趋势、提供生活方式建议、解答基本医疗常识。'
                '请问还有什么我可以帮助您的吗？'
            )
            return self.limit_response_length(response, 500)
    
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
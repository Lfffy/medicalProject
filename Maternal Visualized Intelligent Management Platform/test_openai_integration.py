import socketio
import time
import json

# 创建Socket.IO客户端
sio = socketio.Client()

# 连接事件处理
def on_connect():
    print('成功连接到服务器')
    # 发送一个包含医疗关键词的测试消息
    test_message = {
        'type': 'user_message',
        'content': '我今年35岁，血压140/90，BMI 28，请问我的子痫前期风险高吗？',
        'timestamp': time.time()
    }
    sio.emit('send_message', test_message)
    print(f'发送测试消息: {test_message["content"]}')

# 接收消息事件处理
def on_receive_message(data):
    print(f'收到助手响应: {json.dumps(data, ensure_ascii=False)}')
    # 断开连接
    sio.disconnect()

# 连接到服务器
print('正在连接到服务器...')
sio.on('connect', on_connect)
sio.on('receive_message', on_receive_message)

# 连接到后端服务
try:
    sio.connect('http://localhost:8081', wait_timeout=10)
    # 保持连接，直到收到响应
    sio.wait()
except Exception as e:
    print(f'连接失败: {e}')

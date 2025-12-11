import socketio
import time

# 创建Socket.IO客户端
sio = socketio.Client()

# 连接事件
@sio.event
def connect():
    print('成功连接到服务器')
    # 发送测试消息
    test_message = "我今年35岁，血压140/90，BMI 28，请问我的子痫前期风险高吗？"
    print(f"发送测试消息: {test_message}")
    sio.emit('ai_chat_query', {'message': test_message})

# 断开连接事件
@sio.event
def disconnect():
    print('与服务器断开连接')

# 接收AI响应事件
@sio.event
def ai_chat_response(data):
    print(f"收到AI响应: {data['response']}")
    # 断开连接
    sio.disconnect()

# 连接到服务器
try:
    sio.connect('http://localhost:8081')
    # 等待响应
    sio.wait()
except Exception as e:
    print(f"连接失败: {e}")

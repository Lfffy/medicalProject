import socketio
import time

# 创建Socket.IO客户端
sio = socketio.Client()

# 连接事件处理函数
@sio.event
def connect():
    print('成功连接到服务器')
    # 发送测试消息
    sio.emit('user_message', {'content': '我今年35岁，血压140/90，BMI 28，有什么风险吗？', 'timestamp': time.time()})

# 助手响应事件处理函数
@sio.event
def assistant_response(data):
    print(f'收到助手响应: {data}')
    # 断开连接
    sio.disconnect()

# 输入事件处理函数
@sio.event
def typing(data):
    print(f'助手正在输入...')

# 连接到服务器
try:
    sio.connect('http://localhost:8081')
    # 等待响应
    sio.wait()
except Exception as e:
    print(f'连接失败: {str(e)}')

<template>
  <div class="ai-chat-container">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <div class="header-left">
        <i class="el-icon-chat-dot-round"></i>
        <span>AI智能助手</span>
      </div>
      <div class="header-right">
        <el-button 
          size="small" 
          type="text" 
          @click="clearHistory"
          :disabled="messages.length === 0"
        >
          <i class="el-icon-delete"></i>
          清空记录
        </el-button>
        <el-button 
          size="small" 
          type="text" 
          @click="reconnect"
          :disabled="connectionStatus === 'connected'"
        >
          <i class="el-icon-refresh"></i>
          重连
        </el-button>
      </div>
    </div>

    <!-- 连接状态指示器 -->
    <div class="connection-status" :class="connectionStatus">
      <div class="status-indicator"></div>
      <span>{{ getStatusText() }}</span>
    </div>

    <!-- 消息列表 -->
    <div class="messages-container" ref="messagesContainer">
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        class="message-wrapper"
        :class="message.type"
      >
        <div class="message">
          <div class="message-content">{{ message.content }}</div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>
      
      <!-- 正在输入指示器 -->
      <div v-if="isTyping" class="typing-indicator">
        <div class="message">
          <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-container">
      <div class="input-wrapper">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="2"
          placeholder="请输入您的问题..."
          @keydown.enter.native="handleEnter"
          :disabled="connectionStatus !== 'connected' || isTyping"
          resize="none"
        ></el-input>
        <el-button 
          type="primary" 
          @click="sendMessage"
          :disabled="!inputMessage.trim() || connectionStatus !== 'connected' || isTyping"
          :loading="isTyping"
          class="send-button"
        >
          <i class="el-icon-s-promotion"></i>
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from 'socket.io-client'

export default {
  name: 'AIChat',
  data() {
    return {
      inputMessage: '',
      messages: [],
      isTyping: false,
      connectionStatus: 'disconnected', // disconnected, connecting, connected, error
      socket: null,
      reconnectAttempts: 0,
      maxReconnectAttempts: 5
    }
  },
  mounted() {
    this.initSocket()
  },
  beforeDestroy() {
    this.disconnect()
  },
  methods: {
    initSocket() {
      try {
        this.connectionStatus = 'connecting'
        
        // 连接到Socket.IO服务器
        this.socket = io('http://localhost:8081', {
          transports: ['websocket', 'polling'],
          timeout: 10000,
          forceNew: true,
          reconnection: true,
          reconnectionAttempts: 5,
          reconnectionDelay: 1000,
          reconnectionDelayMax: 5000,
          autoConnect: true,
          upgrade: true,
          rememberUpgrade: true,
          forceJSONP: false,
          jsonp: false,
          transportsOptions: {
            websocket: {
              extraHeaders: {
                'Origin': window.location.origin
              }
            }
          }
        })
        
        this.socket.on('connect', () => {
          console.log('Socket.IO连接已建立')
          this.connectionStatus = 'connected'
          this.reconnectAttempts = 0
        })
        
        this.socket.on('assistant_response', (data) => {
          this.isTyping = false
          this.addMessage(data.content, 'assistant')
        })
        
        this.socket.on('typing', (data) => {
          this.isTyping = data.isTyping
        })
        
        this.socket.on('error', (data) => {
          this.isTyping = false
          this.$message.error(data.message || '发生错误')
        })
        
        this.socket.on('disconnect', () => {
          console.log('Socket.IO连接已断开')
          this.connectionStatus = 'disconnected'
          this.handleReconnect()
        })
        
        this.socket.on('connect_error', (error) => {
          console.error('Socket.IO连接错误:', error)
          this.connectionStatus = 'error'
          this.handleReconnect()
        })
        
      } catch (error) {
        console.error('初始化Socket.IO失败:', error)
        this.connectionStatus = 'error'
        this.handleReconnect()
      }
    },
    
    sendMessage() {
      if (!this.inputMessage.trim() || this.connectionStatus !== 'connected' || this.isTyping) {
        return
      }
      
      const message = this.inputMessage.trim()
      this.addMessage(message, 'user')
      this.inputMessage = ''
      
      // 发送消息到服务器
      this.socket.emit('user_message', {
        content: message,
        timestamp: Date.now()
      })
    },
    
    addMessage(content, type) {
      this.messages.push({
        type,
        content,
        timestamp: Date.now()
      })
      this.scrollToBottom()
    },
    
    clearHistory() {
      this.$confirm('确定要清空所有对话记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.messages = []
        this.$message.success('对话记录已清空')
      }).catch(() => {})
    },
    
    reconnect() {
      this.disconnect()
      this.initSocket()
    },
    
    disconnect() {
      if (this.socket) {
        this.socket.disconnect()
        this.socket = null
      }
      this.connectionStatus = 'disconnected'
    },
    
    handleReconnect() {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000)
        
        setTimeout(() => {
          console.log(`尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
          this.initSocket()
        }, delay)
      } else {
        this.$message.error('连接失败，请检查网络后重试')
      }
    },
    
    getStatusText() {
      switch (this.connectionStatus) {
        case 'connecting':
          return '连接中...'
        case 'connected':
          return '已连接'
        case 'disconnected':
          return '连接断开'
        case 'error':
          return '连接错误'
        default:
          return '未知状态'
      }
    },
    
    handleEnter(event) {
      if (!event.shiftKey) {
        event.preventDefault()
        this.sendMessage()
      }
    },
    
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    },
    
    formatTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    }
  }
}
</script>

<style scoped>
.ai-chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
}

.header-left i {
  font-size: 20px;
}

.header-right {
  display: flex;
  gap: 10px;
}

.connection-status {
  background: white;
  padding: 8px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid #e4e7ed;
  font-size: 14px;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #909399;
}

.connection-status.connecting .status-indicator {
  background: #e6a23c;
  animation: pulse 1.5s infinite;
}

.connection-status.connected .status-indicator {
  background: #67c23a;
}

.connection-status.error .status-indicator {
  background: #f56c6c;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

.message-wrapper {
  margin-bottom: 20px;
  display: flex;
}

.message-wrapper.user {
  justify-content: flex-end;
}

.message-wrapper.assistant {
  justify-content: flex-start;
}

.message {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
}

.message-wrapper.user .message {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-left: auto;
}

.message-wrapper.assistant .message {
  background: white;
  color: #303133;
  border: 1px solid #e4e7ed;
  margin-right: auto;
}

.message-content {
  word-wrap: break-word;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 5px;
  text-align: right;
}

.typing-indicator {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.typing-dots {
  display: flex;
  gap: 4px;
  padding: 16px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #909399;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.input-container {
  background: white;
  border-top: 1px solid #e4e7ed;
  padding: 20px;
}

.input-wrapper {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-wrapper .el-textarea {
  flex: 1;
}

.send-button {
  height: 80px;
  min-width: 80px;
  border-radius: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .message {
    max-width: 85%;
  }
  
  .chat-header {
    padding: 12px 15px;
  }
  
  .messages-container {
    padding: 15px;
  }
  
  .input-container {
    padding: 15px;
  }
}

/* 滚动条样式 */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
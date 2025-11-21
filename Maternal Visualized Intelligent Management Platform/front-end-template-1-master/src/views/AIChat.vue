<template>
  <div class="ai-chat-page">
    <div class="page-header">
      <h2>
        <i class="fas fa-robot"></i>
        AI智能助手
      </h2>
      <p>基于大语言模型的智能对话助手，为您提供专业的医疗健康咨询服务</p>
    </div>
    
    <div class="chat-wrapper">
      <AIChat />
    </div>
  </div>
</template>

<script>
import AIChat from '../components/AIChat.vue'

export default {
  name: 'AIChatPage',
  components: {
    AIChat
  }
}
</script>

<style lang="less" scoped>
.ai-chat-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--background-color, #f5f7fa);
  
  .page-header {
    padding: 20px 30px;
    background: white;
    border-bottom: 1px solid #e4e7ed;
    
    h2 {
      margin: 0 0 8px 0;
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      
      i {
        margin-right: 12px;
        color: #409eff;
      }
    }
    
    p {
      margin: 0;
      color: #606266;
      font-size: 14px;
    }
  }
  
  .chat-wrapper {
    flex: 1;
    padding: 20px;
    height: calc(100vh - 120px);
    min-height: 600px;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .ai-chat-page {
    .page-header {
      padding: 15px 20px;
      
      h2 {
        font-size: 20px;
      }
    }
    
    .chat-wrapper {
      padding: 10px;
      height: calc(100vh - 100px);
    }
  }
}
</style>
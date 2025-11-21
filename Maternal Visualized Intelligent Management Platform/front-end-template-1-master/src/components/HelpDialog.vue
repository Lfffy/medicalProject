<template>
  <div class="help-dialog-overlay" v-if="visible" @click="closeDialog">
    <div class="help-dialog" @click.stop>
      <div class="help-header">
        <h3>帮助文档</h3>
        <button class="close-btn" @click="closeDialog">✕</button>
      </div>
      
      <div class="help-content">
        <div class="help-sidebar">
          <div class="sidebar-title">文档目录</div>
          <div 
            v-for="(doc, key) in helpData" 
            :key="key"
            class="sidebar-item"
            :class="{ active: activeTab === key }"
            @click="switchTab(key)"
          >
            {{ doc.title }}
          </div>
        </div>
        
        <div class="help-main">
          <div class="help-toolbar">
            <div class="toolbar-left">
              <h4>{{ currentDoc?.title }}</h4>
            </div>
            <div class="toolbar-right">
              <el-button size="mini" @click="copyContent">复制内容</el-button>
              <el-button size="mini" @click="printContent">打印</el-button>
            </div>
          </div>
          
          <div class="markdown-content" ref="markdownContent">
            <div v-if="loading" class="loading-content">
              正在加载文档...
            </div>
            <div v-else-if="error" class="error-content">
              {{ error }}
            </div>
            <div v-else v-html="renderedMarkdown" class="markdown-body"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelpDialog',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      helpData: {},
      activeTab: 'guide',
      loading: false,
      error: null
    }
  },
  computed: {
    currentDoc() {
      return this.helpData[this.activeTab]
    },
    renderedMarkdown() {
      if (!this.currentDoc?.content) return ''
      return this.markdownToHtml(this.currentDoc.content)
    }
  },
  watch: {
    visible(newVal) {
      console.log('HelpDialog visible变化:', newVal);
      if (newVal) {
        this.loadHelpDocs()
      }
    }
  },
  methods: {
    async loadHelpDocs() {
      this.loading = true
      this.error = null
      
      try {
        const response = await fetch('/api/help/docs')
        const result = await response.json()
        
        if (result.code === 200) {
          this.helpData = result.data
        } else {
          this.error = result.message || '加载帮助文档失败'
        }
      } catch (error) {
        console.error('加载帮助文档时出错:', error)
        this.error = '网络错误，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    
    switchTab(key) {
      this.activeTab = key
    },
    
    markdownToHtml(markdown) {
      if (!markdown) return ''
      
      return markdown
        // 标题
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        // 粗体
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // 斜体
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        // 代码块
        .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
        // 行内代码
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // 链接
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
        // 列表
        .replace(/^\* (.+)$/gim, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        // 数字列表
        .replace(/^\d+\. (.+)$/gim, '<li>$1</li>')
        // 段落
        .replace(/\n\n/g, '</p><p>')
        .replace(/^/, '<p>')
        .replace(/$/, '</p>')
        // 换行
        .replace(/\n/g, '<br>')
    },
    
    closeDialog() {
      this.$emit('update:visible', false)
    },
    
    copyContent() {
      if (!this.currentDoc?.content) return
      
      navigator.clipboard.writeText(this.currentDoc.content).then(() => {
        this.$message.success('内容已复制到剪贴板')
      }).catch(() => {
        this.$message.error('复制失败')
      })
    },
    
    printContent() {
      if (!this.currentDoc?.content) return
      
      const printWindow = window.open('', '_blank')
      printWindow.document.write(`
        <html>
          <head>
            <title>${this.currentDoc.title}</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 20px; }
              h1, h2, h3 { color: #333; }
              pre { background: #f5f5f5; padding: 10px; border-radius: 4px; }
              code { background: #f0f0f0; padding: 2px 4px; border-radius: 2px; }
              ul, ol { margin-left: 20px; }
            </style>
          </head>
          <body>
            <h1>${this.currentDoc.title}</h1>
            <pre>${this.currentDoc.content}</pre>
          </body>
        </html>
      `)
      printWindow.document.close()
      printWindow.print()
    }
  }
}
</script>

<style scoped>
.help-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.help-dialog {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 1200px;
  height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.help-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
  background: #f8f9fa;
  border-radius: 8px 8px 0 0;
}

.help-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #909399;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.3s;
}

.close-btn:hover {
  background: #f0f0f0;
  color: #303133;
}

.help-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.help-sidebar {
  width: 250px;
  background: #fafbfc;
  border-right: 1px solid #e4e7ed;
  overflow-y: auto;
}

.sidebar-title {
  padding: 15px 20px;
  font-weight: bold;
  color: #303133;
  border-bottom: 1px solid #e4e7ed;
  background: #f8f9fa;
}

.sidebar-item {
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 3px solid transparent;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
}

.sidebar-item:hover {
  background: #ecf5ff;
  color: #409eff;
}

.sidebar-item.active {
  background: #ecf5ff;
  color: #409eff;
  border-left-color: #409eff;
  font-weight: 500;
}

.help-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.help-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e4e7ed;
  background: #fff;
}

.help-toolbar h4 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.toolbar-right {
  display: flex;
  gap: 8px;
}

.markdown-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #fff;
}

.loading-content,
.error-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #909399;
  font-size: 14px;
  gap: 8px;
}

.error-content {
  color: #f56c6c;
}

.markdown-body {
  line-height: 1.6;
  color: #303133;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body h1 {
  font-size: 2em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
  color: #303133;
}

.markdown-body h2 {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
  color: #303133;
}

.markdown-body h3 {
  font-size: 1.25em;
  color: #303133;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 2em;
  margin-bottom: 16px;
}

.markdown-body li {
  margin-bottom: 4px;
}

.markdown-body code {
  background: #f6f8fa;
  border-radius: 3px;
  font-size: 85%;
  margin: 0;
  padding: 0.2em 0.4em;
  color: #e74c3c;
}

.markdown-body pre {
  background: #f6f8fa;
  border-radius: 6px;
  overflow: auto;
  padding: 16px;
  margin-bottom: 16px;
}

.markdown-body pre code {
  background: transparent;
  border: 0;
  display: inline;
  line-height: inherit;
  margin: 0;
  max-width: auto;
  overflow: visible;
  padding: 0;
  color: #303133;
}

.markdown-body a {
  color: #409eff;
  text-decoration: none;
}

.markdown-body a:hover {
  text-decoration: underline;
}

.markdown-body p {
  margin-bottom: 16px;
}

.markdown-body strong {
  font-weight: 600;
  color: #303133;
}

.markdown-body em {
  font-style: italic;
  color: #606266;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .help-dialog {
    width: 95%;
    height: 90vh;
  }
  
  .help-sidebar {
    width: 200px;
  }
  
  .help-toolbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
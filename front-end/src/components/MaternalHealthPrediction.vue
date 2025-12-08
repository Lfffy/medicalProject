<template>
  <div class="maternal-health-prediction">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="container">
        <div class="header-title">
          <i class="fas fa-heartbeat"></i>
          <h1>孕产妇健康风险预测中心</h1>
        </div>
        <p class="header-subtitle">
          基于AI技术的个人健康风险评估系统，为您提供专业、精准的孕期健康管理指导
        </p>
      </div>
    </header>

    <!-- 通知消息 -->
    <div v-if="notification.show" class="notification" :class="notification.type">
      <i :class="notification.icon"></i>
      <span class="notification-message">{{ notification.message }}</span>
      <button class="notification-close" @click="clearNotification" aria-label="关闭通知">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <!-- 主要内容区域 -->
    <main class="container">
      <!-- 统计卡片区域 -->
      <section class="stats-section" v-if="!showResult">
        <div class="stats-card">
          <div class="stats-icon primary">
            <i class="fas fa-users"></i>
          </div>
          <div class="stats-content">
            <h3 class="stats-title">已服务用户</h3>
            <p class="stats-number">{{ stats.totalUsers }}</p>
          </div>
        </div>
        <div class="stats-card">
          <div class="stats-icon success">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stats-content">
            <h3 class="stats-title">成功预测</h3>
            <p class="stats-number">{{ stats.successfulPredictions }}</p>
          </div>
        </div>
        <div class="stats-card">
          <div class="stats-icon warning">
            <i class="fas fa-heart-rate"></i>
          </div>
          <div class="stats-content">
            <h3 class="stats-title">风险预警</h3>
            <p class="stats-number">{{ stats.riskAlerts }}</p>
          </div>
        </div>
        <div class="stats-card">
          <div class="stats-icon info">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stats-content">
            <h3 class="stats-title">平均评估时间</h3>
            <p class="stats-number">{{ stats.avgPredictionTime }}秒</p>
          </div>
        </div>
      </section>

      <!-- 表单和结果区域 -->
      <div class="prediction-container">
        <!-- 预测表单 -->
        <div v-if="!showResult" class="prediction-form-wrapper">
          <EnhancedMaternalPredictionForm @submit-form="handleFormSubmit" />
        </div>

        <!-- 预测结果 -->
        <div v-else class="prediction-result-wrapper">
          <MaternalPredictionResult 
            :prediction-data="predictionData" 
            @back-to-form="backToForm"
            @save-result="handleSaveResult"
            @share-result="handleShareResult"
          />
        </div>
      </div>

      <!-- 健康知识卡片 -->
      <section class="health-info-section" v-if="!showResult">
        <h2 class="section-title">孕期健康小贴士</h2>
        <div class="health-info-cards">
          <div class="health-info-card">
            <div class="info-card-icon">
              <i class="fas fa-apple-alt"></i>
            </div>
            <h3 class="info-card-title">均衡饮食</h3>
            <p class="info-card-content">
              孕期应保持均衡的营养摄入，多食用富含蛋白质、叶酸、铁和钙的食物，避免过多摄入高糖、高盐和高脂肪食物。
            </p>
          </div>
          <div class="health-info-card">
            <div class="info-card-icon">
              <i class="fas fa-running"></i>
            </div>
            <h3 class="info-card-title">适量运动</h3>
            <p class="info-card-content">
              每天进行30分钟的中等强度有氧运动，如散步、游泳或孕妇瑜伽，有助于维持健康体重和促进分娩顺利。
            </p>
          </div>
          <div class="health-info-card">
            <div class="info-card-icon">
              <i class="fas fa-sync-alt"></i>
            </div>
            <h3 class="info-card-title">定期产检</h3>
            <p class="info-card-content">
              遵循医生建议进行定期产检，及时发现和处理可能出现的健康问题，确保母婴安全。
            </p>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="page-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-info">
            <p>&copy; 2024 孕产妇健康风险预测中心 | 专业、精准的孕期健康管理平台</p>
          </div>
          <div class="footer-links">
            <a href="#" class="footer-link">使用指南</a>
            <a href="#" class="footer-link">隐私政策</a>
            <a href="#" class="footer-link">关于我们</a>
            <a href="#" class="footer-link">联系客服</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import EnhancedMaternalPredictionForm from './EnhancedMaternalPredictionForm.vue';
import MaternalPredictionResult from './MaternalPredictionResult.vue';
import '../assets/responsive-maternal-styles.css';

export default {
  name: 'MaternalHealthPrediction',
  components: {
    EnhancedMaternalPredictionForm,
    MaternalPredictionResult
  },
  data() {
    return {
      showResult: false,
      predictionData: null,
      notification: {
        show: false,
        type: 'success',
        message: '',
        icon: ''
      },
      stats: {
        totalUsers: 12580,
        successfulPredictions: 11920,
        riskAlerts: 856,
        avgPredictionTime: 2.8
      }
    };
  },
  methods: {
    // 处理表单提交
    handleFormSubmit(formData) {
      // 模拟预测结果
      this.predictionData = {
        riskLevel: '低风险',
        riskScore: 72,
        riskItems: [
          { name: '血压异常', level: '正常', value: '118/76 mmHg' },
          { name: '血糖偏高', level: '低风险', value: '4.8 mmol/L' },
          { name: 'BMI指数', level: '正常', value: '22.8' },
          { name: '年龄风险', level: '低风险', value: '28岁' }
        ],
        recommendations: [
          '保持现有的健康生活方式，继续均衡饮食和适量运动',
          '定期进行产检，密切关注血压和血糖变化',
          '保持充足的睡眠，建议每晚睡眠时间不少于8小时',
          '避免接触有害物质，如吸烟、饮酒和二手烟'
        ],
        indicators: [
          { name: '心率', value: '76 次/分', unit: '次/分', status: 'normal' },
          { name: '血红蛋白', value: '13.5', unit: 'g/dL', status: 'normal' },
          { name: '铁蛋白', value: '42', unit: 'ng/mL', status: 'normal' },
          { name: '维生素D', value: '38', unit: 'ng/mL', status: 'normal' }
        ],
        predictionDate: new Date().toLocaleString()
      };
      
      // 显示结果页面
      this.showResult = true;
      
      // 滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    
    // 返回表单
    backToForm() {
      this.showResult = false;
      this.predictionData = null;
      // 滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    
    // 保存结果
    handleSaveResult() {
      this.showNotification('success', '预测结果已保存', 'fas fa-check-circle');
    },
    
    // 分享结果
    handleShareResult() {
      this.showNotification('info', '分享链接已复制到剪贴板', 'fas fa-share-alt');
    },
    
    // 显示通知
    showNotification(type, message, icon) {
      this.notification = {
        show: true,
        type,
        message,
        icon
      };
      
      // 3秒后自动关闭
      setTimeout(() => {
        this.clearNotification();
      }, 3000);
    },
    
    // 清除通知
    clearNotification() {
      this.notification.show = false;
    }
  }
};
</script>

<style>
/* 基础样式 */
.maternal-health-prediction {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
  min-height: 100vh;
  padding-bottom: 60px;
}

/* 容器样式 */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  padding: 40px 0;
  text-align: center;
  margin-bottom: 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
}

.header-title i {
  font-size: 2.8rem;
}

.header-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  max-width: 800px;
  margin: 0 auto;
}

/* 预测容器 */
.prediction-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 40px;
  overflow: hidden;
}

.prediction-form-wrapper,
.prediction-result-wrapper {
  padding: 20px;
}

/* 统计卡片区域 */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stats-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  color: white;
}

.stats-icon.primary {
  background-color: #3498db;
}

.stats-icon.success {
  background-color: #2ecc71;
}

.stats-icon.warning {
  background-color: #f39c12;
}

.stats-icon.info {
  background-color: #1abc9c;
}

.stats-content h3 {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0 0 5px 0;
  font-weight: 500;
}

.stats-number {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  color: #2c3e50;
}

/* 健康知识区域 */
.health-info-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 25px;
  text-align: center;
}

.health-info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 25px;
}

.health-info-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  border-top: 4px solid #3498db;
}

.health-info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.info-card-icon {
  font-size: 2.5rem;
  color: #3498db;
  margin-bottom: 20px;
}

.info-card-title {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 15px;
  font-weight: 600;
}

.info-card-content {
  color: #7f8c8d;
  line-height: 1.6;
}

/* 页脚 */
.page-footer {
  background-color: #2c3e50;
  color: white;
  padding: 30px 0;
  margin-top: 60px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-info p {
  margin: 0;
  opacity: 0.8;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-link {
  color: white;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.footer-link:hover {
  opacity: 1;
  text-decoration: underline;
}

/* 通知样式 */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease-out;
  max-width: 400px;
}

.notification.success {
  background-color: #2ecc71;
  color: white;
}

.notification.error {
  background-color: #e74c3c;
  color: white;
}

.notification.warning {
  background-color: #f39c12;
  color: white;
}

.notification.info {
  background-color: #3498db;
  color: white;
}

.notification-message {
  font-size: 1rem;
  margin: 0;
}

/* 动画 */
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 加载状态 */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #7f8c8d;
  font-size: 1.1rem;
}

/* 错误状态 */
.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  color: #e74c3c;
  margin-bottom: 20px;
}

.error-message {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

/* 无障碍支持 */
@media (prefers-reduced-motion: reduce) {
  .stats-card,
  .health-info-card,
  .notification {
    animation: none;
  }
  
  .loading-spinner {
    animation-duration: 2s;
  }
}

/* 高对比度模式 */
@media (prefers-contrast: high) {
  .stats-card,
  .health-info-card,
  .prediction-container {
    border: 2px solid #000;
  }
}
</style>
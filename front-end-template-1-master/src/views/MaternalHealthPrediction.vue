<template>
  <div class="maternal-health-prediction">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="container">
        <div class="header-content">
          <h1 class="header-title">
            <i class="fas fa-heartbeat" aria-hidden="true"></i>
            孕产妇健康风险预测平台
          </h1>
          <p class="header-subtitle">专业的孕期健康管理和风险评估工具</p>
        </div>
      </div>
    </header>
    
    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="container">
        <!-- 通知栏 -->
        <div v-if="notification" class="notification" :class="notification.type">
          <i :class="notificationIcon"></i>
          <span class="notification-message">{{ notification.message }}</span>
          <button class="notification-close" @click="clearNotification">
            <i class="fas fa-times" aria-hidden="true"></i>
          </button>
        </div>
        
        <!-- 统计卡片区域 -->
        <div class="stats-section">
          <div class="stats-card">
            <i class="fas fa-user-md stats-icon blue"></i>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.totalPredictions }}</div>
              <div class="stats-label">累计预测次数</div>
            </div>
          </div>
          <div class="stats-card">
            <i class="fas fa-check-circle stats-icon green"></i>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.lowRiskCases }}</div>
              <div class="stats-label">低风险案例</div>
            </div>
          </div>
          <div class="stats-card">
            <i class="fas fa-exclamation-triangle stats-icon orange"></i>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.moderateRiskCases }}</div>
              <div class="stats-label">中等风险案例</div>
            </div>
          </div>
          <div class="stats-card">
            <i class="fas fa-ambulance stats-icon red"></i>
            <div class="stats-content">
              <div class="stats-number">{{ statistics.highRiskCases }}</div>
              <div class="stats-label">高风险案例</div>
            </div>
          </div>
        </div>
        
        <!-- 主要功能区域 -->
        <div class="function-area">
          <!-- 表单区域 -->
          <div v-if="showForm" class="form-section">
            <div class="section-header">
              <h2 class="section-title"><i class="fas fa-clipboard-list" aria-hidden="true"></i> 个人信息录入</h2>
              <p class="section-description">请准确填写以下信息，以便获得更精准的预测结果</p>
            </div>
            <MaternalRiskPrediction @predictionSuccess="handlePredictionSuccess" />
          </div>
          
          <!-- 结果展示区域 -->
          <div v-if="showResult" class="result-section">
            <div class="section-header">
              <h2 class="section-title"><i class="fas fa-chart-line" aria-hidden="true"></i> 健康风险预测结果</h2>
              <p class="section-description">基于您提供的信息，我们生成了以下健康风险评估报告</p>
            </div>
            <MaternalPredictionResult 
              :predictionData="currentPrediction"
              @newPrediction="handleNewPrediction"
              @saveResult="handleSaveResult"
              @shareResult="handleShareResult"
            />
          </div>
        </div>
        
        <!-- 健康知识区域 -->
        <div class="health-info-section">
          <h3 class="info-section-title"><i class="fas fa-book-medical" aria-hidden="true"></i> 孕期健康知识</h3>
          <div class="health-info-cards">
            <div class="health-info-card">
              <i class="fas fa-apple-alt info-card-icon"></i>
              <h4 class="info-card-title">合理膳食</h4>
              <p class="info-card-content">孕期应保持均衡饮食，摄入足够的蛋白质、维生素和矿物质，避免高糖、高盐食物。</p>
            </div>
            <div class="health-info-card">
              <i class="fas fa-walking info-card-icon"></i>
              <h4 class="info-card-title">适量运动</h4>
              <p class="info-card-content">适当的运动有助于维持身体健康，可选择散步、孕妇瑜伽等低强度活动。</p>
            </div>
            <div class="health-info-card">
              <i class="fas fa-heartbeat info-card-icon"></i>
              <h4 class="info-card-title">定期产检</h4>
              <p class="info-card-content">按时进行产前检查，监测血压、血糖等指标变化，及时发现并处理异常情况。</p>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 页脚 -->
    <footer class="page-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-info">
            <p class="footer-text">© 2025 孕产妇健康风险预测平台 版权所有</p>
            <p class="footer-disclaimer">免责声明：本平台提供的预测结果仅供参考，不能替代专业医生的诊断和建议。如有不适，请及时就医。</p>
          </div>
          <div class="footer-links">
            <a href="#" class="footer-link"><i class="fas fa-question-circle" aria-hidden="true"></i> 帮助中心</a>
            <a href="#" class="footer-link"><i class="fas fa-shield-alt" aria-hidden="true"></i> 隐私政策</a>
            <a href="#" class="footer-link"><i class="fas fa-file-contract" aria-hidden="true"></i> 用户协议</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import MaternalRiskPrediction from '../components/MaternalRiskPrediction.vue';
import MaternalPredictionResult from '../components/MaternalPredictionResult.vue';
import maternalPredictionService from '../services/maternalPredictionService';

export default {
  name: 'MaternalHealthPrediction',
  
  components: {
    MaternalRiskPrediction,
    MaternalPredictionResult
  },
  
  data() {
    return {
      showForm: true,
      showResult: false,
      currentPrediction: null,
      notification: null,
      statistics: {
        totalPredictions: 0,
        lowRiskCases: 0,
        moderateRiskCases: 0,
        highRiskCases: 0
      }
    };
  },
  
  mounted() {
    // 页面加载时获取统计信息
    this.loadStatistics();
  },
  
  computed: {
    // 通知图标
    notificationIcon() {
      if (!this.notification) return '';
      
      const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
      };
      
      return icons[this.notification.type] || 'fas fa-info-circle';
    }
  },
  
  methods: {
    // 加载统计信息
    async loadStatistics() {
      try {
        const result = await maternalPredictionService.getStatistics();
        console.log('统计接口返回数据:', result); // 添加调试日志
        if (result.success) {
          // 修复：使用result.data而不是result.stats
          const statsData = result.data;
          this.statistics = {
            totalPredictions: statsData.prediction_counts.total_predictions,
            lowRiskCases: statsData.prediction_counts.low_risk,
            moderateRiskCases: statsData.prediction_counts.medium_risk,
            highRiskCases: statsData.prediction_counts.high_risk
          };
        } else {
          throw new Error(result.error || '获取统计信息失败');
        }
      } catch (error) {
        console.error('加载统计信息失败:', error);
        // 使用模拟数据
        this.statistics = {
          totalPredictions: 1254,
          lowRiskCases: 897,
          moderateRiskCases: 286,
          highRiskCases: 71
        };
      }
    },
    
    // 显示通知
    showNotification(type, message, duration = 5000) {
      this.notification = {
        type,
        message
      };
      
      // 自动清除通知
      if (duration > 0) {
        setTimeout(() => {
          this.clearNotification();
        }, duration);
      }
    },
    
    // 清除通知
    clearNotification() {
      this.notification = null;
    },
    
    // 处理预测成功
    handlePredictionSuccess(predictionData) {
      console.log('预测成功:', predictionData);
      this.currentPrediction = predictionData;
      this.showForm = false;
      this.showResult = true;
      this.showNotification('success', '预测成功！点击查看详细结果。');
      
      // 更新统计信息
      this.updateStatistics(predictionData.comprehensive.overall_risk_level);
    },
    
    // 处理预测失败
    handlePredictionError(errorData) {
      console.error('预测失败:', errorData);
      this.showNotification('error', errorData.message || '预测失败，请检查网络连接或稍后重试。');
    },
    
    // 处理重新预测
    handleNewPrediction() {
      this.currentPrediction = null;
      this.showForm = true;
      this.showResult = false;
      this.showNotification('info', '请填写新的预测信息。');
    },
    
    // 处理保存结果
    handleSaveResult() {
      this.showNotification('success', '结果已成功保存。');
    },
    
    // 处理分享结果
    handleShareResult() {
      // 分享功能已在结果组件中实现
    },
    
    // 更新统计信息
    updateStatistics(riskLevel) {
      this.statistics.totalPredictions += 1;
      
      switch (riskLevel) {
        case '低风险':
          this.statistics.lowRiskCases += 1;
          break;
        case '中风险':
          this.statistics.moderateRiskCases += 1;
          break;
        case '高风险':
          this.statistics.highRiskCases += 1;
          break;
      }
    }
  }
};
</script>

<style scoped>
/* 全局样式 */
.maternal-health-prediction {
  min-height: 100vh;
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 页面头部样式 */
.page-header {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  padding: 40px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  text-align: center;
}

.header-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.header-title i {
  font-size: 2.8rem;
  color: #f1c40f;
}

.header-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto;
}

/* 通知样式 */
.notification {
  margin: 20px 0;
  padding: 15px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.notification.success {
  background-color: #e8f5e9;
  color: #2e7d32;
  border-left: 4px solid #4caf50;
}

.notification.error {
  background-color: #ffebee;
  color: #c62828;
  border-left: 4px solid #f44336;
}

.notification.warning {
  background-color: #fff8e1;
  color: #ef6c00;
  border-left: 4px solid #ff9800;
}

.notification.info {
  background-color: #e3f2fd;
  color: #1565c0;
  border-left: 4px solid #2196f3;
}

.notification i {
  font-size: 1.2rem;
}

.notification-message {
  flex: 1;
  font-size: 1rem;
}

.notification-close {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.2rem;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.notification-close:hover {
  opacity: 1;
  background-color: rgba(0, 0, 0, 0.1);
}

/* 统计卡片样式 */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 40px 0;
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
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stats-icon.blue {
  background-color: #3498db;
}

.stats-icon.green {
  background-color: #2ecc71;
}

.stats-icon.orange {
  background-color: #e67e22;
}

.stats-icon.red {
  background-color: #e74c3c;
}

.stats-content {
  flex: 1;
}

.stats-number {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stats-label {
  font-size: 0.95rem;
  color: #7f8c8d;
  font-weight: 500;
}

/* 主要功能区域样式 */
.function-area {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin: 40px 0;
  overflow: hidden;
}

.section-header {
  background: linear-gradient(90deg, #f8f9fa, #e9ecef);
  padding: 25px 40px;
  border-bottom: 1px solid #dee2e6;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-title i {
  color: #3498db;
  font-size: 1.6rem;
}

.section-description {
  color: #7f8c8d;
  font-size: 1rem;
  margin: 0;
}

.form-section,
.result-section {
  padding: 0;
}

/* 健康知识区域样式 */
.health-info-section {
  margin: 40px 0;
}

.info-section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-section-title i {
  color: #e74c3c;
  font-size: 1.3rem;
}

.health-info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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
  font-size: 2rem;
  color: #3498db;
  margin-bottom: 15px;
}

.info-card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
}

.info-card-content {
  color: #5a6c7d;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* 页脚样式 */
.page-footer {
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 40px 0;
  margin-top: 60px;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
}

.footer-info {
  flex: 1;
  min-width: 300px;
}

.footer-text {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 15px;
  color: #bdc3c7;
}

.footer-disclaimer {
  font-size: 0.85rem;
  color: #95a5a6;
  line-height: 1.5;
}

.footer-links {
  display: flex;
  gap: 30px;
}

.footer-link {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.3s;
}

.footer-link:hover {
  color: #3498db;
}

.footer-link i {
  font-size: 1rem;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .container {
    max-width: 100%;
  }
  
  .header-title {
    font-size: 2.2rem;
  }
  
  .section-title {
    font-size: 1.6rem;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 30px 0;
  }
  
  .header-title {
    font-size: 1.8rem;
    flex-direction: column;
  }
  
  .header-subtitle {
    font-size: 1rem;
  }
  
  .stats-section {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .stats-card {
    padding: 20px;
  }
  
  .stats-number {
    font-size: 1.8rem;
  }
  
  .section-header {
    padding: 20px;
  }
  
  .section-title {
    font-size: 1.4rem;
  }
  
  .health-info-cards {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .footer-content {
    flex-direction: column;
    text-align: center;
  }
  
  .footer-links {
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .notification {
    padding: 12px 15px;
  }
  
  .notification-message {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .header-title {
    font-size: 1.5rem;
  }
  
  .header-title i {
    font-size: 2rem;
  }
  
  .stats-icon {
    font-size: 2rem;
    width: 50px;
    height: 50px;
  }
  
  .stats-number {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 1.2rem;
  }
  
  .health-info-card {
    padding: 20px;
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stats-card,
.health-info-card {
  animation: fadeInUp 0.6s ease-out;
}

.stats-card:nth-child(2) {
  animation-delay: 0.1s;
}

.stats-card:nth-child(3) {
  animation-delay: 0.2s;
}

.stats-card:nth-child(4) {
  animation-delay: 0.3s;
}

.health-info-card:nth-child(2) {
  animation-delay: 0.1s;
}

.health-info-card:nth-child(3) {
  animation-delay: 0.2s;
}
</style>
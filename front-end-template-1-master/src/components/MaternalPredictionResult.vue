<template>
  <div class="maternal-prediction-result">
    <div class="result-header">
      <h3 class="result-title">风险评估结果</h3>
      <p class="result-subtitle">基于您提供的信息，我们为您生成了以下健康风险评估报告</p>
    </div>
    
    <!-- 综合风险评估 -->
    <div class="result-section comprehensive-risk">
      <h4 class="section-title">
        <i class="fas fa-chart-pie" aria-hidden="true"></i>
        综合风险评估
      </h4>
      <div class="risk-gauge-container">
        <div class="risk-gauge">
          <div class="gauge-circle" :class="getRiskClass(predictionData.comprehensive.overall_risk_level)">
            <div class="gauge-value">{{ predictionData.comprehensive.overall_risk_score }}%</div>
            <div class="gauge-label">{{ predictionData.comprehensive.overall_risk_level }}</div>
          </div>
        </div>
        <div class="risk-description">
          <p>{{ predictionData.comprehensive.risk_description }}</p>
        </div>
      </div>
    </div>
    
    <!-- 专项风险预测 -->
    <div class="result-section specific-risks">
      <h4 class="section-title">
        <i class="fas fa-microscope" aria-hidden="true"></i>
        专项风险预测
      </h4>
      <div class="risks-grid">
        <!-- 子痫前期风险 -->
        <div class="risk-card">
          <div class="risk-card-header">
            <h5 class="risk-card-title">子痫前期风险</h5>
            <div class="risk-score" :class="getRiskClass(predictionData.preeclampsia.risk_level)">
              {{ predictionData.preeclampsia.risk_score }}%
            </div>
          </div>
          <div class="risk-card-body">
            <div class="risk-level">{{ predictionData.preeclampsia.risk_level }}</div>
            <p class="risk-description">{{ predictionData.preeclampsia.description }}</p>
            <div class="risk-factors">
              <h6>主要风险因素：</h6>
              <ul>
                <li v-for="factor in predictionData.preeclampsia.key_factors" :key="factor">
                  {{ factor }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <!-- 妊娠期糖尿病风险 -->
        <div class="risk-card">
          <div class="risk-card-header">
            <h5 class="risk-card-title">妊娠期糖尿病风险</h5>
            <div class="risk-score" :class="getRiskClass(predictionData.gestational_diabetes.risk_level)">
              {{ predictionData.gestational_diabetes.risk_score }}%
            </div>
          </div>
          <div class="risk-card-body">
            <div class="risk-level">{{ predictionData.gestational_diabetes.risk_level }}</div>
            <p class="risk-description">{{ predictionData.gestational_diabetes.description }}</p>
            <div class="risk-factors">
              <h6>主要风险因素：</h6>
              <ul>
                <li v-for="factor in predictionData.gestational_diabetes.key_factors" :key="factor">
                  {{ factor }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <!-- 早产风险 -->
        <div class="risk-card">
          <div class="risk-card-header">
            <h5 class="risk-card-title">早产风险</h5>
            <div class="risk-score" :class="getRiskClass(predictionData.preterm_birth.risk_level)">
              {{ predictionData.preterm_birth.risk_score }}%
            </div>
          </div>
          <div class="risk-card-body">
            <div class="risk-level">{{ predictionData.preterm_birth.risk_level }}</div>
            <p class="risk-description">{{ predictionData.preterm_birth.description }}</p>
            <div class="risk-factors">
              <h6>主要风险因素：</h6>
              <ul>
                <li v-for="factor in predictionData.preterm_birth.key_factors" :key="factor">
                  {{ factor }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 健康建议 -->
    <div class="result-section recommendations">
      <h4 class="section-title">
        <i class="fas fa-lightbulb" aria-hidden="true"></i>
        健康建议
      </h4>
      <div class="recommendations-list">
        <div v-for="(recommendation, index) in predictionData.comprehensive.recommendations" :key="index" class="recommendation-item">
          <div class="recommendation-icon">
            <i class="fas fa-check-circle" aria-hidden="true"></i>
          </div>
          <div class="recommendation-text">{{ recommendation }}</div>
        </div>
      </div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="result-actions">
      <button class="btn btn-primary" @click="handleNewPrediction">
        <i class="fas fa-redo" aria-hidden="true"></i>
        重新预测
      </button>
      <button class="btn btn-success" @click="handleSaveResult">
        <i class="fas fa-save" aria-hidden="true"></i>
        保存结果
      </button>
      <button class="btn btn-info" @click="handleShareResult">
        <i class="fas fa-share-alt" aria-hidden="true"></i>
        分享结果
      </button>
      <button class="btn btn-secondary" @click="handleExportResult">
        <i class="fas fa-download" aria-hidden="true"></i>
        导出报告
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MaternalPredictionResult',
  
  props: {
    predictionData: {
      type: Object,
      required: true
    }
  },
  
  methods: {
    // 获取风险级别对应的CSS类
    getRiskClass(riskLevel) {
      switch (riskLevel) {
        case '低风险':
          return 'risk-low';
        case '中风险':
          return 'risk-moderate';
        case '高风险':
          return 'risk-high';
        default:
          return 'risk-unknown';
      }
    },
    
    // 处理重新预测
    handleNewPrediction() {
      this.$emit('newPrediction');
    },
    
    // 处理保存结果
    handleSaveResult() {
      this.$emit('saveResult');
    },
    
    // 处理分享结果
    handleShareResult() {
      // 创建分享链接
      const shareUrl = window.location.href;
      
      // 检查是否支持Web Share API
      if (navigator.share) {
        navigator.share({
          title: '孕产妇健康风险评估报告',
          text: '我刚刚完成了孕产妇健康风险评估，查看我的结果。',
          url: shareUrl
        })
        .then(() => {
          console.log('分享成功');
        })
        .catch((error) => {
          console.error('分享失败:', error);
          this.fallbackShare(shareUrl);
        });
      } else {
        this.fallbackShare(shareUrl);
      }
    },
    
    // 备用分享方法
    fallbackShare(url) {
      // 复制到剪贴板
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url)
          .then(() => {
            this.$emit('showNotification', 'success', '分享链接已复制到剪贴板');
          })
          .catch(() => {
            this.$emit('showNotification', 'error', '复制失败，请手动复制链接');
          });
      } else {
        // 旧浏览器备用方法
        const textArea = document.createElement('textarea');
        textArea.value = url;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        this.$emit('showNotification', 'success', '分享链接已复制到剪贴板');
      }
    },
    
    // 处理导出结果
    handleExportResult() {
      // 创建导出数据
      const exportData = {
        predictionData: this.predictionData,
        exportDate: new Date().toISOString()
      };
      
      // 转换为JSON字符串
      const dataStr = JSON.stringify(exportData, null, 2);
      
      // 创建Blob对象
      const blob = new Blob([dataStr], { type: 'application/json' });
      
      // 创建下载链接
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `maternal-risk-assessment-${new Date().toISOString().split('T')[0]}.json`;
      
      // 触发下载
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // 释放URL对象
      URL.revokeObjectURL(url);
      
      this.$emit('showNotification', 'success', '报告已导出');
    }
  }
};
</script>

<style scoped>
.maternal-prediction-result {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.result-header {
  text-align: center;
  margin-bottom: 30px;
}

.result-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
}

.result-subtitle {
  font-size: 1rem;
  color: #7f8c8d;
  max-width: 700px;
  margin: 0 auto;
}

.result-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title i {
  color: #3498db;
  font-size: 1.2rem;
}

/* 综合风险评估样式 */
.comprehensive-risk {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 10px;
  border-left: 4px solid #3498db;
}

.risk-gauge-container {
  display: flex;
  align-items: center;
  gap: 30px;
}

.risk-gauge {
  flex: 0 0 200px;
}

.gauge-circle {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  border: 10px solid #e9ecef;
  transition: all 0.3s ease;
}

.gauge-circle.risk-low {
  border-color: #2ecc71;
  background-color: rgba(46, 204, 113, 0.1);
}

.gauge-circle.risk-moderate {
  border-color: #f39c12;
  background-color: rgba(243, 156, 18, 0.1);
}

.gauge-circle.risk-high {
  border-color: #e74c3c;
  background-color: rgba(231, 76, 60, 0.1);
}

.gauge-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.gauge-label {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 5px;
}

.risk-description {
  flex: 1;
}

.risk-description p {
  font-size: 1rem;
  line-height: 1.6;
  color: #5a6c7d;
  margin: 0;
}

/* 专项风险预测样式 */
.specific-risks {
  margin-bottom: 30px;
}

.risks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.risk-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.risk-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.risk-card-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e9ecef;
}

.risk-card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.risk-score {
  font-size: 1.3rem;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 20px;
  color: white;
}

.risk-score.risk-low {
  background-color: #2ecc71;
}

.risk-score.risk-moderate {
  background-color: #f39c12;
}

.risk-score.risk-high {
  background-color: #e74c3c;
}

.risk-card-body {
  padding: 20px;
}

.risk-level {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #2c3e50;
}

.risk-description {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #5a6c7d;
  margin-bottom: 15px;
}

.risk-factors h6 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.risk-factors ul {
  padding-left: 20px;
  margin: 0;
}

.risk-factors li {
  font-size: 0.85rem;
  line-height: 1.4;
  color: #5a6c7d;
  margin-bottom: 5px;
}

/* 健康建议样式 */
.recommendations {
  background: #e8f4fd;
  padding: 25px;
  border-radius: 10px;
  border-left: 4px solid #3498db;
}

.recommendations-list {
  display: grid;
  gap: 15px;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.recommendation-icon {
  flex: 0 0 24px;
  height: 24px;
  color: #2ecc71;
  font-size: 1.2rem;
  margin-top: 2px;
}

.recommendation-text {
  flex: 1;
  font-size: 1rem;
  line-height: 1.6;
  color: #5a6c7d;
}

/* 操作按钮样式 */
.result-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-success {
  background-color: #2ecc71;
  color: white;
}

.btn-success:hover {
  background-color: #27ae60;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
}

.btn-info:hover {
  background-color: #138496;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .maternal-prediction-result {
    padding: 20px;
  }
  
  .result-title {
    font-size: 1.5rem;
  }
  
  .risk-gauge-container {
    flex-direction: column;
    text-align: center;
  }
  
  .risk-gauge {
    margin: 0 auto;
  }
  
  .risks-grid {
    grid-template-columns: 1fr;
  }
  
  .result-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 250px;
    justify-content: center;
  }
}
</style>
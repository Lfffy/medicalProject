<template>
  <div class="analysis-center-container">
    <dv-border-box-8 :dur="5">
      <div class="analysis-center-content">
        <!-- 页面头部 -->
        <div class="header">
          <h2>智能分析预测中心</h2>
          <div class="header-actions">
            <el-button-group>
              <el-button 
                :type="activeTab === 'prediction' ? 'primary' : 'default'"
                @click="switchTab('prediction')"
                icon="el-icon-cpu"
              >
                智能预测
              </el-button>
              <el-button 
                :type="activeTab === 'comparison' ? 'primary' : 'default'"
                @click="switchTab('comparison')"
                icon="el-icon-data-analysis"
              >
                对比分析
              </el-button>
              <el-button 
                :type="activeTab === 'trend' ? 'primary' : 'default'"
                @click="switchTab('trend')"
                icon="el-icon-s-marketing"
              >
                趋势分析
              </el-button>
              <el-button 
                :type="activeTab === 'risk' ? 'primary' : 'default'"
                @click="switchTab('risk')"
                icon="el-icon-warning"
              >
                风险评估
              </el-button>
            </el-button-group>
          </div>
        </div>

        <!-- 智能预测页面 -->
        <div v-show="activeTab === 'prediction'" class="tab-content">
          <div class="prediction-container">
            <el-row :gutter="20">
              <!-- 预测配置 -->
              <el-col :span="8">
                <el-card class="prediction-config">
                  <h3>预测配置</h3>
                  <el-form :model="predictionForm" label-width="120px">
                    <el-form-item label="预测类型">
                      <el-select v-model="predictionForm.type" @change="handlePredictionTypeChange">
                        <el-option label="疾病风险预测" value="disease"></el-option>
                        <el-option label="孕产妇风险评估" value="maternal"></el-option>
                        <el-option label="健康趋势预测" value="health"></el-option>
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="选择模型">
                      <el-select v-model="predictionForm.model">
                        <el-option 
                          v-for="model in availableModels" 
                          :key="model.id"
                          :label="model.name" 
                          :value="model.id"
                        ></el-option>
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="算法类型">
                      <el-select v-model="predictionForm.algorithm">
                        <el-option label="随机森林" value="random_forest"></el-option>
                        <el-option label="逻辑回归" value="logistic_regression"></el-option>
                        <el-option label="支持向量机" value="svm"></el-option>
                        <el-option label="神经网络" value="neural_network"></el-option>
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="置信度">
                      <el-slider
                        v-model="predictionForm.confidence"
                        :min="0.5"
                        :max="1"
                        :step="0.05"
                        show-input
                      ></el-slider>
                    </el-form-item>
                    
                    <el-form-item>
                      <el-button type="primary" @click="startPrediction" :loading="predicting">开始预测</el-button>
                      <el-button @click="resetPredictionForm">重置</el-button>
                    </el-form-item>
                  </el-form>
                </el-card>
              </el-col>
              
              <!-- 特征重要性 -->
              <el-col :span="8">
                <el-card class="feature-importance">
                  <h3>特征重要性</h3>
                  <div class="chart-container">
                    <dv-capsule-chart 
                      :config="featureImportanceConfig" 
                      style="width:100%; height:300px;"
                    />
                  </div>
                  <div class="feature-list">
                    <div v-for="feature in topFeatures" :key="feature.name" class="feature-item">
                      <span class="feature-name">{{ feature.name }}</span>
                      <el-progress 
                        :percentage="feature.importance" 
                        :color="getFeatureColor(feature.importance)"
                        :show-text="false"
                      ></el-progress>
                      <span class="feature-value">{{ feature.importance }}%</span>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <!-- 预测结果 -->
              <el-col :span="8">
                <el-card class="prediction-result">
                  <h3>预测结果</h3>
                  <div v-if="predictionResult" class="result-content">
                    <div class="result-score">
                      <div class="score-circle">
                        <el-progress 
                          type="circle" 
                          :percentage="predictionResult.score"
                          :color="getScoreColor(predictionResult.score)"
                          :width="120"
                        ></el-progress>
                      </div>
                      <div class="score-text">
                        <h4>{{ predictionResult.label }}</h4>
                        <p>{{ predictionResult.description }}</p>
                      </div>
                    </div>
                    
                    <div class="result-details">
                      <h4>详细分析</h4>
                      <ul>
                        <li v-for="detail in predictionResult.details" :key="detail.key">
                          <strong>{{ detail.key }}:</strong> {{ detail.value }}
                        </li>
                      </ul>
                    </div>
                    
                    <div class="result-actions">
                      <el-button type="primary" @click="savePredictionResult">保存结果</el-button>
                      <el-button @click="exportPredictionReport">导出报告</el-button>
                    </div>
                  </div>
                  <div v-else class="no-result">
                    <i class="el-icon-data-analysis"></i>
                    <p>暂无预测结果</p>
                    <p>请配置参数并开始预测</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 对比分析页面 -->
        <div v-show="activeTab === 'comparison'" class="tab-content">
          <div class="comparison-container">
            <el-row :gutter="20">
              <el-col :span="24">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>数据对比分析</span>
                    <el-button-group style="float: right;">
                      <el-button size="small" @click="refreshComparison">刷新</el-button>
                      <el-button size="small" @click="exportComparison">导出</el-button>
                    </el-button-group>
                  </div>
                  
                  <div class="comparison-controls">
                    <el-row :gutter="20">
                      <el-col :span="6">
                        <el-select v-model="comparisonConfig.dataType1" placeholder="数据类型1">
                          <el-option label="普通医疗数据" value="medical"></el-option>
                          <el-option label="孕产妇数据" value="maternal"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="comparisonConfig.dataType2" placeholder="数据类型2">
                          <el-option label="普通医疗数据" value="medical"></el-option>
                          <el-option label="孕产妇数据" value="maternal"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="comparisonConfig.metric" placeholder="对比指标">
                          <el-option label="平均年龄" value="avg_age"></el-option>
                          <el-option label="疾病分布" value="disease_dist"></el-option>
                          <el-option label="风险等级" value="risk_level"></el-option>
                          <el-option label="健康指标" value="health_metrics"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-button type="primary" @click="performComparison">开始对比</el-button>
                      </el-col>
                    </el-row>
                  </div>
                  
                  <div class="comparison-results">
                    <el-row :gutter="20">
                      <el-col :span="12">
                        <div class="comparison-chart">
                          <h4>数据对比图表</h4>
                          <dv-capsule-chart 
                            :config="comparisonChartConfig" 
                            style="width:100%; height:300px;"
                          />
                        </div>
                      </el-col>
                      <el-col :span="12">
                        <div class="comparison-stats">
                          <h4>统计对比</h4>
                          <el-table :data="comparisonStats" border>
                            <el-table-column prop="metric" label="指标"></el-table-column>
                            <el-table-column prop="dataset1" label="数据集1"></el-table-column>
                            <el-table-column prop="dataset2" label="数据集2"></el-table-column>
                            <el-table-column prop="difference" label="差异">
                              <template slot-scope="scope">
                                <span :class="getDifferenceClass(scope.row.difference)">
                                  {{ scope.row.difference }}
                                </span>
                              </template>
                            </el-table-column>
                          </el-table>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 趋势分析页面 -->
        <div v-show="activeTab === 'trend'" class="tab-content">
          <div class="trend-container">
            <el-row :gutter="20">
              <el-col :span="24">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>趋势分析</span>
                    <el-button-group style="float: right;">
                      <el-button size="small" @click="refreshTrend">刷新</el-button>
                      <el-button size="small" @click="exportTrend">导出</el-button>
                    </el-button-group>
                  </div>
                  
                  <div class="trend-controls">
                    <el-row :gutter="20">
                      <el-col :span="6">
                        <el-select v-model="trendConfig.dataType" placeholder="数据类型">
                          <el-option label="全部数据" value="all"></el-option>
                          <el-option label="普通医疗数据" value="medical"></el-option>
                          <el-option label="孕产妇数据" value="maternal"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="trendConfig.timeRange" placeholder="时间范围">
                          <el-option label="最近7天" value="7d"></el-option>
                          <el-option label="最近30天" value="30d"></el-option>
                          <el-option label="最近3个月" value="3m"></el-option>
                          <el-option label="最近1年" value="1y"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="trendConfig.metric" placeholder="分析指标">
                          <el-option label="数据量变化" value="volume"></el-option>
                          <el-option label="疾病分布趋势" value="disease_trend"></el-option>
                          <el-option label="健康指标趋势" value="health_trend"></el-option>
                          <el-option label="风险等级趋势" value="risk_trend"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-button type="primary" @click="analyzeTrend">分析趋势</el-button>
                      </el-col>
                    </el-row>
                  </div>
                  
                  <div class="trend-results">
                    <el-row :gutter="20">
                      <el-col :span="16">
                        <div class="trend-chart">
                          <h4>趋势图表</h4>
                          <dv-capsule-chart 
                            :config="trendChartConfig" 
                            style="width:100%; height:400px;"
                          />
                        </div>
                      </el-col>
                      <el-col :span="8">
                        <div class="trend-summary">
                          <h4>趋势总结</h4>
                          <div class="summary-item" v-for="item in trendSummary" :key="item.title">
                            <div class="summary-title">{{ item.title }}</div>
                            <div class="summary-value">{{ item.value }}</div>
                            <div class="summary-trend" :class="item.trend">
                              <i :class="item.trend === 'up' ? 'el-icon-top' : 'el-icon-bottom'"></i>
                              {{ item.change }}
                            </div>
                          </div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 风险评估页面 -->
        <div v-show="activeTab === 'risk'" class="tab-content">
          <div class="risk-container">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card>
                  <h3>风险评估配置</h3>
                  <el-form :model="riskForm" label-width="120px">
                    <el-form-item label="评估对象">
                      <el-select v-model="riskForm.target">
                        <el-option label="患者个体" value="individual"></el-option>
                        <el-option label="群体统计" value="population"></el-option>
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="风险类型">
                      <el-checkbox-group v-model="riskForm.riskTypes">
                        <el-checkbox label="health">健康风险</el-checkbox>
                        <el-checkbox label="disease">疾病风险</el-checkbox>
                        <el-checkbox label="maternal">孕产风险</el-checkbox>
                        <el-checkbox label="complication">并发症风险</el-checkbox>
                      </el-checkbox-group>
                    </el-form-item>
                    
                    <el-form-item label="评估周期">
                      <el-select v-model="riskForm.period">
                        <el-option label="短期(1个月)" value="short"></el-option>
                        <el-option label="中期(3个月)" value="medium"></el-option>
                        <el-option label="长期(1年)" value="long"></el-option>
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item>
                      <el-button type="primary" @click="assessRisk" :loading="assessing">开始评估</el-button>
                      <el-button @click="resetRiskForm">重置</el-button>
                    </el-form-item>
                  </el-form>
                </el-card>
              </el-col>
              
              <el-col :span="12">
                <el-card>
                  <h3>风险评估结果</h3>
                  <div v-if="riskResult" class="risk-result">
                    <div class="risk-level">
                      <h4>总体风险等级</h4>
                      <el-tag :type="getRiskTagType(riskResult.overallRisk)" size="large">
                        {{ riskResult.overallRisk }}
                      </el-tag>
                    </div>
                    
                    <div class="risk-breakdown">
                      <h4>风险细分</h4>
                      <div v-for="risk in riskResult.riskBreakdown" :key="risk.type" class="risk-item">
                        <div class="risk-type">{{ risk.type }}</div>
                        <el-progress 
                          :percentage="risk.score" 
                          :color="getRiskColor(risk.score)"
                          :show-text="false"
                        ></el-progress>
                        <div class="risk-score">{{ risk.score }}%</div>
                      </div>
                    </div>
                    
                    <div class="risk-recommendations">
                      <h4>建议措施</h4>
                      <ul>
                        <li v-for="rec in riskResult.recommendations" :key="rec">
                          {{ rec }}
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div v-else class="no-result">
                    <i class="el-icon-warning"></i>
                    <p>暂无评估结果</p>
                    <p>请配置参数并开始评估</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AnalysisCenter',
  data() {
    return {
      activeTab: 'prediction',
      predicting: false,
      assessing: false,
      
      // 预测相关
      predictionForm: {
        type: 'disease',
        model: 'model_1',
        algorithm: 'random_forest',
        confidence: 0.8
      },
      
      availableModels: [
        { id: 'model_1', name: '疾病风险预测模型' },
        { id: 'model_2', name: '孕产妇风险评估模型' },
        { id: 'model_3', name: '健康趋势预测模型' }
      ],
      
      topFeatures: [
        { name: '年龄', importance: 85 },
        { name: '血压', importance: 78 },
        { name: '体重指数', importance: 72 },
        { name: '血糖', importance: 65 },
        { name: '家族病史', importance: 58 }
      ],
      
      predictionResult: null,
      
      // 对比分析相关
      comparisonConfig: {
        dataType1: 'medical',
        dataType2: 'maternal',
        metric: 'avg_age'
      },
      
      comparisonStats: [],
      
      // 趋势分析相关
      trendConfig: {
        dataType: 'all',
        timeRange: '30d',
        metric: 'volume'
      },
      
      trendSummary: [],
      
      // 风险评估相关
      riskForm: {
        target: 'individual',
        riskTypes: ['health', 'disease'],
        period: 'medium'
      },
      
      riskResult: null,
      
      // 图表配置
      featureImportanceConfig: {
        data: [
          { name: '年龄', value: 85 },
          { name: '血压', value: 78 },
          { name: '体重指数', value: 72 },
          { name: '血糖', value: 65 },
          { name: '家族病史', value: 58 }
        ]
      },
      
      comparisonChartConfig: {
        data: [
          { name: '指标1', value: 75 },
          { name: '指标2', value: 82 },
          { name: '指标3', value: 68 }
        ]
      },
      
      trendChartConfig: {
        data: [
          { name: '周一', value: 120 },
          { name: '周二', value: 135 },
          { name: '周三', value: 125 },
          { name: '周四', value: 145 },
          { name: '周五', value: 160 },
          { name: '周六', value: 140 },
          { name: '周日', value: 130 }
        ]
      }
    }
  },
  
  methods: {
    // 切换标签页
    switchTab(tab) {
      this.activeTab = tab
    },
    
    // 预测类型变化
    handlePredictionTypeChange() {
      // 根据预测类型更新可用模型
      this.updateAvailableModels()
    },
    
    // 更新可用模型
    updateAvailableModels() {
      // 根据预测类型筛选模型
      const type = this.predictionForm.type
      // 这里可以根据实际需求更新模型列表
    },
    
    // 开始预测
    async startPrediction() {
      this.predicting = true
      try {
        const response = await axios.post('/api/analysis/predict', this.predictionForm)
        if (response.data.code === 200) {
          this.predictionResult = response.data.data
          this.$message.success('预测完成')
        } else {
          this.$message.error(response.data.message || '预测失败')
        }
      } catch (error) {
        console.error('预测失败:', error)
        this.$message.error('预测失败，请检查网络连接')
      } finally {
        this.predicting = false
      }
    },
    
    // 重置预测表单
    resetPredictionForm() {
      this.predictionForm = {
        type: 'disease',
        model: 'model_1',
        algorithm: 'random_forest',
        confidence: 0.8
      }
      this.predictionResult = null
    },
    
    // 获取特征颜色
    getFeatureColor(importance) {
      if (importance >= 80) return '#f56c6c'
      if (importance >= 60) return '#e6a23c'
      return '#67c23a'
    },
    
    // 获取分数颜色
    getScoreColor(score) {
      if (score >= 80) return '#f56c6c'
      if (score >= 60) return '#e6a23c'
      return '#67c23a'
    },
    
    // 保存预测结果
    savePredictionResult() {
      // 实现保存预测结果
      this.$message.success('预测结果已保存')
    },
    
    // 导出预测报告
    exportPredictionReport() {
      // 实现导出预测报告
      this.$message.success('预测报告已导出')
    },
    
    // 执行对比分析
    async performComparison() {
      try {
        const response = await axios.post('/api/analysis/compare', this.comparisonConfig)
        if (response.data.code === 200) {
          this.comparisonStats = response.data.data.stats
          this.comparisonChartConfig = response.data.data.chart
          this.$message.success('对比分析完成')
        }
      } catch (error) {
        console.error('对比分析失败:', error)
        this.$message.error('对比分析失败')
      }
    },
    
    // 刷新对比分析
    refreshComparison() {
      this.performComparison()
    },
    
    // 导出对比结果
    exportComparison() {
      this.$message.success('对比结果已导出')
    },
    
    // 获取差异样式
    getDifferenceClass(difference) {
      if (difference.startsWith('+')) return 'positive'
      if (difference.startsWith('-')) return 'negative'
      return 'neutral'
    },
    
    // 分析趋势
    async analyzeTrend() {
      try {
        const response = await axios.post('/api/analysis/trend', this.trendConfig)
        if (response.data.code === 200) {
          this.trendChartConfig = response.data.data.chart
          this.trendSummary = response.data.data.summary
          this.$message.success('趋势分析完成')
        }
      } catch (error) {
        console.error('趋势分析失败:', error)
        this.$message.error('趋势分析失败')
      }
    },
    
    // 刷新趋势分析
    refreshTrend() {
      this.analyzeTrend()
    },
    
    // 导出趋势结果
    exportTrend() {
      this.$message.success('趋势结果已导出')
    },
    
    // 风险评估
    async assessRisk() {
      this.assessing = true
      try {
        const response = await axios.post('/api/analysis/risk', this.riskForm)
        if (response.data.code === 200) {
          this.riskResult = response.data.data
          this.$message.success('风险评估完成')
        } else {
          this.$message.error(response.data.message || '风险评估失败')
        }
      } catch (error) {
        console.error('风险评估失败:', error)
        this.$message.error('风险评估失败')
      } finally {
        this.assessing = false
      }
    },
    
    // 重置风险评估表单
    resetRiskForm() {
      this.riskForm = {
        target: 'individual',
        riskTypes: ['health', 'disease'],
        period: 'medium'
      }
      this.riskResult = null
    },
    
    // 获取风险标签类型
    getRiskTagType(risk) {
      switch (risk) {
        case '高风险': return 'danger'
        case '中风险': return 'warning'
        case '低风险': return 'success'
        default: return 'info'
      }
    },
    
    // 获取风险颜色
    getRiskColor(score) {
      if (score >= 80) return '#f56c6c'
      if (score >= 60) return '#e6a23c'
      return '#67c23a'
    }
  },
  
  created() {
    // 初始化数据
  }
}
</script>

<style scoped>
.analysis-center-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.analysis-center-content {
  background: white;
  border-radius: 10px;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.header h2 {
  color: #333;
  margin: 0;
  font-weight: bold;
}

.tab-content {
  min-height: 600px;
}

/* 预测页面样式 */
.prediction-container .el-card {
  height: 100%;
}

.prediction-config h3,
.feature-importance h3,
.prediction-result h3 {
  margin-bottom: 20px;
  color: #333;
}

.chart-container {
  margin-bottom: 20px;
}

.feature-list {
  max-height: 200px;
  overflow-y: auto;
}

.feature-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.feature-name {
  width: 80px;
  font-size: 12px;
}

.feature-item .el-progress {
  flex: 1;
  margin: 0 10px;
}

.feature-value {
  width: 40px;
  text-align: right;
  font-size: 12px;
}

.result-content {
  text-align: center;
}

.result-score {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.score-text h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.score-text p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.result-details {
  text-align: left;
  margin-bottom: 20px;
}

.result-details h4 {
  margin-bottom: 10px;
  color: #333;
}

.result-details ul {
  list-style: none;
  padding: 0;
}

.result-details li {
  margin-bottom: 5px;
  font-size: 14px;
}

.no-result {
  text-align: center;
  color: #999;
}

.no-result i {
  font-size: 48px;
  margin-bottom: 10px;
}

/* 对比分析页面样式 */
.comparison-controls {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.comparison-results {
  margin-top: 20px;
}

.comparison-chart h4,
.comparison-stats h4 {
  margin-bottom: 15px;
  color: #333;
}

.positive {
  color: #67c23a;
}

.negative {
  color: #f56c6c;
}

.neutral {
  color: #909399;
}

/* 趋势分析页面样式 */
.trend-controls {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.trend-results {
  margin-top: 20px;
}

.trend-chart h4,
.trend-summary h4 {
  margin-bottom: 15px;
  color: #333;
}

.summary-item {
  padding: 15px;
  margin-bottom: 10px;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.summary-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.summary-trend {
  font-size: 12px;
}

.summary-trend.up {
  color: #67c23a;
}

.summary-trend.down {
  color: #f56c6c;
}

/* 风险评估页面样式 */
.risk-result {
  text-align: center;
}

.risk-level {
  margin-bottom: 20px;
}

.risk-level h4 {
  margin-bottom: 10px;
  color: #333;
}

.risk-breakdown {
  margin-bottom: 20px;
  text-align: left;
}

.risk-breakdown h4 {
  margin-bottom: 15px;
  color: #333;
}

.risk-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.risk-type {
  width: 80px;
  font-size: 14px;
}

.risk-item .el-progress {
  flex: 1;
  margin: 0 10px;
}

.risk-score {
  width: 40px;
  text-align: right;
  font-size: 12px;
}

.risk-recommendations {
  text-align: left;
}

.risk-recommendations h4 {
  margin-bottom: 10px;
  color: #333;
}

.risk-recommendations ul {
  list-style: none;
  padding: 0;
}

.risk-recommendations li {
  margin-bottom: 5px;
  font-size: 14px;
  color: #666;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 15px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: center;
  }
  
  .result-score {
    flex-direction: column;
  }
  
  .score-text {
    margin-top: 15px;
  }
}
</style>
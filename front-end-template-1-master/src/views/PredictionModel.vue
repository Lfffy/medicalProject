<template>
  <div class="prediction-model-container">
    <dv-border-box-8 :dur="5">
      <div class="prediction-model-content">
        <div class="header">
          <h2>预测模型</h2>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-refresh" @click="refreshData">刷新数据</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportReport">导出报告</el-button>
          </div>
        </div>

        <div class="filter-section">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-select v-model="filters.modelType" placeholder="模型类型" @change="handleFilterChange">
                <el-option label="疾病风险预测" value="disease_risk"></el-option>
                <el-option label="住院时长预测" value="hospitalization_duration"></el-option>
                <el-option label="费用预测" value="cost_prediction"></el-option>
                <el-option label="孕产妇并发症预测" value="maternal_complications"></el-option>
                <el-option label="新生儿健康预测" value="neonatal_health"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.dataType" placeholder="数据类型" @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="普通医疗数据" value="medical"></el-option>
                <el-option label="孕产妇数据" value="maternal"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.algorithm" placeholder="算法选择" @change="handleFilterChange">
                <el-option label="随机森林" value="random_forest"></el-option>
                <el-option label="逻辑回归" value="logistic_regression"></el-option>
                <el-option label="支持向量机" value="svm"></el-option>
                <el-option label="神经网络" value="neural_network"></el-option>
                <el-option label="XGBoost" value="xgboost"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-button type="primary" @click="trainModel">训练模型</el-button>
              <el-button @click="resetFilters">重置</el-button>
            </el-col>
          </el-row>
        </div>

        <!-- 模型训练状态 -->
        <div class="training-status" v-if="trainingStatus.isTraining">
          <el-progress 
            :percentage="trainingStatus.progress" 
            :status="trainingStatus.status"
            :stroke-width="20"
          >
            <template #default="{ percentage }">
              <span class="percentage-value">{{ percentage }}%</span>
            </template>
          </el-progress>
          <p class="training-message">{{ trainingStatus.message }}</p>
        </div>

        <div class="model-info-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="model-info-content">
                  <h3>模型信息</h3>
                  <el-descriptions :column="2" border>
                    <el-descriptions-item label="模型类型">
                      {{ getModelTypeLabel(filters.modelType) }}
                    </el-descriptions-item>
                    <el-descriptions-item label="算法">
                      {{ getAlgorithmLabel(filters.algorithm) }}
                    </el-descriptions-item>
                    <el-descriptions-item label="准确率">
                      <el-tag type="success">{{ modelInfo.accuracy }}%</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="精确率">
                      <el-tag type="primary">{{ modelInfo.precision }}%</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="召回率">
                      <el-tag type="warning">{{ modelInfo.recall }}%</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="F1分数">
                      <el-tag type="info">{{ modelInfo.f1_score }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="训练时间" :span="2">
                      {{ modelInfo.training_time }}
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="feature-importance-content">
                  <h3>特征重要性</h3>
                  <div ref="featureChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <div class="charts-grid">
          <!-- 混淆矩阵 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>混淆矩阵</h3>
                <div ref="confusionChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- ROC曲线 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>ROC曲线</h3>
                <div ref="rocChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 学习曲线 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>学习曲线</h3>
                <div ref="learningChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 预测结果分布 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>预测结果分布</h3>
                <div ref="predictionChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>
        </div>

        <!-- 预测输入表单 -->
        <div class="prediction-form-section">
          <dv-border-box-10>
            <div class="form-content">
              <h3>实时预测</h3>
              <el-form 
                ref="predictionForm" 
                :model="predictionForm" 
                :rules="predictionRules"
                label-width="120px"
              >
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="患者姓名" prop="name">
                      <el-input v-model="predictionForm.name" placeholder="请输入患者姓名"></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="年龄" prop="age">
                      <el-input-number 
                        v-model="predictionForm.age" 
                        :min="0" 
                        :max="120"
                        style="width: 100%"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="性别" prop="gender">
                      <el-select v-model="predictionForm.gender" style="width: 100%">
                        <el-option label="男" value="male"></el-option>
                        <el-option label="女" value="female"></el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="收缩压" prop="systolic">
                      <el-input-number 
                        v-model="predictionForm.systolic" 
                        :min="50" 
                        :max="250"
                        style="width: 100%"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="舒张压" prop="diastolic">
                      <el-input-number 
                        v-model="predictionForm.diastolic" 
                        :min="30" 
                        :max="150"
                        style="width: 100%"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="体重(kg)" prop="weight">
                      <el-input-number 
                        v-model="predictionForm.weight" 
                        :min="10" 
                        :max="200"
                        style="width: 100%"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20" v-if="filters.modelType === 'maternal_complications'">
                  <el-col :span="8">
                    <el-form-item label="孕周" prop="gestational_weeks">
                      <el-input-number 
                        v-model="predictionForm.gestational_weeks" 
                        :min="1" 
                        :max="42"
                        style="width: 100%"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="产次" prop="parity">
                      <el-input-number 
                        v-model="predictionForm.parity" 
                        :min="0" 
                        :max="10"
                        style="width: 100%"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="既往病史" prop="medical_history">
                      <el-input 
                        v-model="predictionForm.medical_history" 
                        placeholder="请输入既往病史"
                      ></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-form-item>
                  <el-button type="primary" @click="makePrediction" :loading="predicting">
                    开始预测
                  </el-button>
                  <el-button @click="resetForm">重置表单</el-button>
                </el-form-item>
              </el-form>
            </div>
          </dv-border-box-10>
        </div>

        <!-- 预测结果 -->
        <div class="prediction-result-section" v-if="predictionResult">
          <dv-border-box-10>
            <div class="result-content">
              <h3>预测结果</h3>
              <el-row :gutter="20">
                <el-col :span="12">
                  <div class="result-card">
                    <h4>风险评估</h4>
                    <div class="risk-level" :class="predictionResult.risk_level.toLowerCase()">
                      {{ getRiskLevelLabel(predictionResult.risk_level) }}
                    </div>
                    <div class="confidence">
                      置信度: {{ predictionResult.confidence }}%
                    </div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="result-card">
                    <h4>详细预测</h4>
                    <el-descriptions :column="1" border>
                      <el-descriptions-item 
                        v-for="(value, key) in predictionResult.details" 
                        :key="key"
                        :label="getDetailLabel(key)"
                      >
                        {{ value }}
                      </el-descriptions-item>
                    </el-descriptions>
                  </div>
                </el-col>
              </el-row>
            </div>
          </dv-border-box-10>
        </div>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'PredictionModel',
  data() {
    return {
      loading: false,
      predicting: false,
      charts: {},
      
      // 筛选条件
      filters: {
        modelType: 'disease_risk',
        dataType: '',
        algorithm: 'random_forest'
      },
      
      // 训练状态
      trainingStatus: {
        isTraining: false,
        progress: 0,
        status: '',
        message: ''
      },
      
      // 模型信息
      modelInfo: {
        accuracy: 0,
        precision: 0,
        recall: 0,
        f1_score: 0,
        training_time: ''
      },
      
      // 预测表单
      predictionForm: {
        name: '',
        age: null,
        gender: '',
        systolic: null,
        diastolic: null,
        weight: null,
        gestational_weeks: null,
        parity: null,
        medical_history: ''
      },
      
      // 表单验证规则
      predictionRules: {
        name: [
          { required: true, message: '请输入患者姓名', trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        systolic: [
          { required: true, message: '请输入收缩压', trigger: 'blur' }
        ],
        diastolic: [
          { required: true, message: '请输入舒张压', trigger: 'blur' }
        ],
        weight: [
          { required: true, message: '请输入体重', trigger: 'blur' }
        ]
      },
      
      // 预测结果
      predictionResult: null
    }
  },
  
  mounted() {
    this.initCharts()
    this.loadModelData()
  },
  
  beforeDestroy() {
    // 销毁图表实例
    Object.values(this.charts).forEach(chart => {
      if (chart) {
        chart.dispose()
      }
    })
    window.removeEventListener('resize', this.handleResize)
  },
  
  methods: {
    initCharts() {
      // 初始化特征重要性图表
      this.charts.feature = echarts.init(this.$refs.featureChart)
      
      // 初始化混淆矩阵图表
      this.charts.confusion = echarts.init(this.$refs.confusionChart)
      
      // 初始化ROC曲线图表
      this.charts.roc = echarts.init(this.$refs.rocChart)
      
      // 初始化学习曲线图表
      this.charts.learning = echarts.init(this.$refs.learningChart)
      
      // 初始化预测结果分布图表
      this.charts.prediction = echarts.init(this.$refs.predictionChart)
      
      // 监听窗口大小变化
      window.addEventListener('resize', this.handleResize)
    },
    
    handleResize() {
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.resize()
        }
      })
    },
    
    loadModelData() {
      this.loading = true
      
      const params = {
        model_type: this.filters.modelType,
        data_type: this.filters.dataType,
        algorithm: this.filters.algorithm
      }
      
      this.$http.get('/api/analysis/model-info', { params })
        .then(response => {
          const data = response.data.data
          this.modelInfo = data.model_info || {}
          
          // 更新图表
          this.updateFeatureChart(data.feature_importance || {})
          this.updateConfusionChart(data.confusion_matrix || {})
          this.updateRocChart(data.roc_curve || {})
          this.updateLearningChart(data.learning_curve || {})
          this.updatePredictionChart(data.prediction_distribution || {})
        })
        .catch(error => {
          this.$message.error('加载模型数据失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    updateFeatureChart(data) {
      const option = {
        title: {
          text: '特征重要性排序',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'value',
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'category',
          data: data.features || [],
          axisLabel: {
            color: '#666'
          }
        },
        series: [
          {
            name: '重要性',
            type: 'bar',
            data: data.importance || [],
            itemStyle: {
              color: '#409EFF'
            }
          }
        ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      this.charts.feature.setOption(option)
    },
    
    updateConfusionChart(data) {
      const option = {
        title: {
          text: '混淆矩阵',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          position: 'top'
        },
        grid: {
          height: '50%',
          top: '10%'
        },
        xAxis: {
          type: 'category',
          data: data.xAxis || [],
          splitArea: {
            show: true
          }
        },
        yAxis: {
          type: 'category',
          data: data.yAxis || [],
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 100,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '15%'
        },
        series: [
          {
            name: '混淆矩阵',
            type: 'heatmap',
            data: data.data || [],
            label: {
              show: true
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      
      this.charts.confusion.setOption(option)
    },
    
    updateRocChart(data) {
      const option = {
        title: {
          text: 'ROC曲线',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: ['ROC曲线', '随机猜测'],
          top: 30
        },
        xAxis: {
          type: 'value',
          name: '假阳性率',
          nameLocation: 'middle',
          nameGap: 30,
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'value',
          name: '真阳性率',
          nameLocation: 'middle',
          nameGap: 30,
          axisLabel: {
            color: '#666'
          }
        },
        series: [
          {
            name: 'ROC曲线',
            type: 'line',
            data: data.roc_data || [],
            itemStyle: {
              color: '#409EFF'
            }
          },
          {
            name: '随机猜测',
            type: 'line',
            data: [[0, 0], [1, 1]],
            lineStyle: {
              type: 'dashed',
              color: '#909399'
            }
          }
        ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      this.charts.roc.setOption(option)
    },
    
    updateLearningChart(data) {
      const option = {
        title: {
          text: '学习曲线',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['训练集', '验证集'],
          top: 30
        },
        xAxis: {
          type: 'category',
          data: data.xAxis || [],
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'value',
          name: '准确率',
          nameLocation: 'middle',
          nameGap: 30,
          axisLabel: {
            color: '#666'
          }
        },
        series: data.series || [],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      this.charts.learning.setOption(option)
    },
    
    updatePredictionChart(data) {
      const option = {
        title: {
          text: '预测结果分布',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 30
        },
        series: [
          {
            name: '预测结果',
            type: 'pie',
            radius: '50%',
            data: data.data || [],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      
      this.charts.prediction.setOption(option)
    },
    
    getModelTypeLabel(type) {
      const labels = {
        disease_risk: '疾病风险预测',
        hospitalization_duration: '住院时长预测',
        cost_prediction: '费用预测',
        maternal_complications: '孕产妇并发症预测',
        neonatal_health: '新生儿健康预测'
      }
      return labels[type] || type
    },
    
    getAlgorithmLabel(algorithm) {
      const labels = {
        random_forest: '随机森林',
        logistic_regression: '逻辑回归',
        svm: '支持向量机',
        neural_network: '神经网络',
        xgboost: 'XGBoost'
      }
      return labels[algorithm] || algorithm
    },
    
    getRiskLevelLabel(level) {
      const labels = {
        low: '低风险',
        medium: '中风险',
        high: '高风险'
      }
      return labels[level] || level
    },
    
    getDetailLabel(key) {
      const labels = {
        probability: '概率',
        risk_factors: '风险因素',
        recommendations: '建议',
        next_steps: '下一步'
      }
      return labels[key] || key
    },
    
    trainModel() {
      this.trainingStatus.isTraining = true
      this.trainingStatus.progress = 0
      this.trainingStatus.status = ''
      this.trainingStatus.message = '开始训练模型...'
      
      const params = {
        model_type: this.filters.modelType,
        data_type: this.filters.dataType,
        algorithm: this.filters.algorithm
      }
      
      // 模拟训练进度
      const progressInterval = setInterval(() => {
        if (this.trainingStatus.progress < 90) {
          this.trainingStatus.progress += 10
          this.trainingStatus.message = `训练中... ${this.trainingStatus.progress}%`
        }
      }, 500)
      
      this.$http.post('/api/analysis/train-model', params)
        .then(response => {
          clearInterval(progressInterval)
          this.trainingStatus.progress = 100
          this.trainingStatus.status = 'success'
          this.trainingStatus.message = '模型训练完成！'
          
          // 重新加载模型数据
          this.loadModelData()
          
          setTimeout(() => {
            this.trainingStatus.isTraining = false
          }, 2000)
        })
        .catch(error => {
          clearInterval(progressInterval)
          this.trainingStatus.status = 'exception'
          this.trainingStatus.message = '模型训练失败：' + error.message
          
          setTimeout(() => {
            this.trainingStatus.isTraining = false
          }, 3000)
        })
    },
    
    makePrediction() {
      this.$refs.predictionForm.validate((valid) => {
        if (!valid) {
          return false
        }
        
        this.predicting = true
        
        const params = {
          model_type: this.filters.modelType,
          algorithm: this.filters.algorithm,
          input_data: this.predictionForm
        }
        
        this.$http.post('/api/analysis/predict', params)
          .then(response => {
            this.predictionResult = response.data.data
            this.$message.success('预测完成！')
          })
          .catch(error => {
            this.$message.error('预测失败：' + error.message)
          })
          .finally(() => {
            this.predicting = false
          })
      })
    },
    
    resetForm() {
      this.$refs.predictionForm.resetFields()
      this.predictionResult = null
    },
    
    handleFilterChange() {
      this.loadModelData()
    },
    
    resetFilters() {
      this.filters = {
        modelType: 'disease_risk',
        dataType: '',
        algorithm: 'random_forest'
      }
      this.loadModelData()
    },
    
    refreshData() {
      this.loadModelData()
      this.$message.success('数据已刷新')
    },
    
    exportReport() {
      const params = {
        model_type: this.filters.modelType,
        algorithm: this.filters.algorithm
      }
      
      this.$http.get('/api/analysis/export-model-report', { 
        params,
        responseType: 'blob'
      })
      .then(response => {
        const blob = new Blob([response.data])
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = `模型分析报告_${new Date().toISOString().slice(0, 10)}.pdf`
        link.click()
      })
      .catch(error => {
        this.$message.error('导出报告失败：' + error.message)
      })
    }
  }
}
</script>

<style lang="less" scoped>
.prediction-model-container {
  padding: 20px;
  height: 100%;
  
  .prediction-model-content {
    padding: 20px;
    height: 100%;
    
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      
      h2 {
        color: #409EFF;
        margin: 0;
        font-size: 24px;
      }
    }
    
    .filter-section {
      margin-bottom: 20px;
      padding: 20px;
      background: rgba(64, 158, 255, 0.05);
      border-radius: 8px;
      border: 1px solid rgba(64, 158, 255, 0.2);
    }
    
    .training-status {
      margin-bottom: 20px;
      padding: 20px;
      background: rgba(64, 158, 255, 0.05);
      border-radius: 8px;
      border: 1px solid rgba(64, 158, 255, 0.2);
      
      .percentage-value {
        font-weight: bold;
        color: #409EFF;
      }
      
      .training-message {
        text-align: center;
        margin-top: 10px;
        color: #666;
      }
    }
    
    .model-info-section {
      margin-bottom: 20px;
      
      .model-info-content,
      .feature-importance-content {
        padding: 20px;
        height: 100%;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
        
        .chart {
          width: 100%;
          height: 300px;
        }
      }
    }
    
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-bottom: 20px;
      
      .chart-item {
        min-height: 400px;
        
        .chart-content {
          padding: 20px;
          height: 100%;
          
          h3 {
            color: #409EFF;
            margin-bottom: 15px;
            text-align: center;
          }
          
          .chart {
            width: 100%;
            height: 320px;
          }
        }
      }
    }
    
    .prediction-form-section {
      margin-bottom: 20px;
      
      .form-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
      }
    }
    
    .prediction-result-section {
      .result-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
        
        .result-card {
          padding: 20px;
          background: rgba(64, 158, 255, 0.05);
          border-radius: 8px;
          border: 1px solid rgba(64, 158, 255, 0.2);
          height: 100%;
          
          h4 {
            color: #409EFF;
            margin-bottom: 15px;
          }
          
          .risk-level {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            
            &.low {
              color: #67C23A;
            }
            
            &.medium {
              color: #E6A23C;
            }
            
            &.high {
              color: #F56C6C;
            }
          }
          
          .confidence {
            color: #666;
            font-size: 14px;
          }
        }
      }
    }
  }
}

@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
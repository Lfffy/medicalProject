<template>
  <div class="ml-prediction-center">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="fas fa-brain"></i>
            智能医疗预测中心
          </h1>
          <p class="page-subtitle">AI驱动的疾病预测与健康分析平台</p>
        </div>
        <div class="header-right">
          <div class="system-status">
            <div class="status-indicator" :class="systemStatus.status">
              <span class="status-dot"></span>
              <span class="status-text">{{ systemStatus.text }}</span>
            </div>
            <div class="last-update">
              <i class="fas fa-clock"></i>
              <span>最后更新: {{ lastUpdateTime }}</span>
            </div>
          </div>
          <button class="refresh-btn" @click="refreshData" :disabled="isRefreshing">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': isRefreshing }"></i>
            刷新数据
          </button>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 快速统计卡片 -->
      <section class="stats-section">
        <div class="stats-grid">
          <div class="stat-card" v-for="stat in statsData" :key="stat.id">
            <div class="stat-icon" :style="{ backgroundColor: stat.color }">
              <i :class="stat.icon"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-value">{{ stat.value }}</h3>
              <p class="stat-label">{{ stat.label }}</p>
              <div class="stat-trend" :class="stat.trend">
                <i :class="stat.trendIcon"></i>
                <span>{{ stat.trendValue }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能区域 -->
      <section class="features-section">
        <div class="features-tabs">
          <button 
            v-for="tab in featureTabs" 
            :key="tab.id"
            class="tab-button"
            :class="{ active: activeTab === tab.id }"
            @click="switchTab(tab.id)"
          >
            <i :class="tab.icon"></i>
            {{ tab.name }}
          </button>
        </div>

        <!-- 疾病预测面板 -->
        <div v-show="activeTab === 'disease'" class="tab-panel disease-prediction">
          <div class="panel-content">
            <div class="prediction-form">
              <h3 class="form-title">疾病智能预测</h3>
              <form @submit.prevent="predictDisease" class="disease-form">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">患者姓名</label>
                    <input 
                      v-model="diseaseForm.patientName" 
                      type="text" 
                      class="form-input"
                      placeholder="请输入患者姓名"
                      required
                    >
                  </div>
                  <div class="form-group">
                    <label class="form-label">年龄</label>
                    <input 
                      v-model.number="diseaseForm.age" 
                      type="number" 
                      class="form-input"
                      placeholder="请输入年龄"
                      min="0" 
                      max="150"
                      required
                    >
                  </div>
                </div>
                
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">性别</label>
                    <select v-model="diseaseForm.gender" class="form-select" required>
                      <option value="">请选择性别</option>
                      <option value="男">男</option>
                      <option value="女">女</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label class="form-label">症状描述</label>
                    <input 
                      v-model="diseaseForm.symptoms" 
                      type="text" 
                      class="form-input"
                      placeholder="请描述主要症状"
                      required
                    >
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">体温 (°C)</label>
                    <input 
                      v-model.number="diseaseForm.temperature" 
                      type="number" 
                      step="0.1"
                      class="form-input"
                      placeholder="36.5"
                      min="35" 
                      max="42"
                      required
                    >
                  </div>
                  <div class="form-group">
                    <label class="form-label">血压 (mmHg)</label>
                    <input 
                      v-model="diseaseForm.bloodPressure" 
                      type="text" 
                      class="form-input"
                      placeholder="120/80"
                      pattern="\d{2,3}\/\d{2,3}"
                      required
                    >
                  </div>
                </div>

                <div class="form-actions">
                  <button type="submit" class="btn-primary" :disabled="isPredicting">
                    <i class="fas fa-microscope"></i>
                    {{ isPredicting ? '预测中...' : '开始预测' }}
                  </button>
                  <button type="button" class="btn-secondary" @click="resetDiseaseForm">
                    <i class="fas fa-redo"></i>
                    重置表单
                  </button>
                </div>
              </form>
            </div>

            <div class="prediction-result" v-if="diseaseResult">
              <h3 class="result-title">预测结果</h3>
              <div class="result-content">
                <div class="result-header">
                  <div class="patient-info">
                    <h4>{{ diseaseResult.patientName }}</h4>
                    <p>{{ diseaseResult.age }}岁 / {{ diseaseResult.gender }}</p>
                  </div>
                  <div class="risk-level" :class="diseaseResult.riskLevel">
                    <span class="risk-label">风险等级</span>
                    <span class="risk-value">{{ diseaseResult.riskText }}</span>
                  </div>
                </div>
                
                <div class="prediction-details">
                  <div class="detail-item">
                    <span class="detail-label">可能疾病</span>
                    <span class="detail-value">{{ diseaseResult.disease }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">置信度</span>
                    <div class="confidence-bar">
                      <div class="confidence-fill" :style="{ width: diseaseResult.confidence + '%' }"></div>
                      <span class="confidence-text">{{ diseaseResult.confidence }}%</span>
                    </div>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">建议措施</span>
                    <span class="detail-value suggestion">{{ diseaseResult.suggestion }}</span>
                  </div>
                </div>

                <div class="result-actions">
                  <button class="btn-outline" @click="shareResult('disease')">
                    <i class="fas fa-share"></i>
                    分享结果
                  </button>
                  <button class="btn-outline" @click="printResult('disease')">
                    <i class="fas fa-print"></i>
                    打印报告
                  </button>
                  <button class="btn-outline" @click="saveResult('disease')">
                    <i class="fas fa-save"></i>
                    保存记录
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 生命体征预测面板 -->
        <div v-show="activeTab === 'vital'" class="tab-panel vital-prediction">
          <div class="panel-content">
            <div class="prediction-form">
              <h3 class="form-title">生命体征趋势预测</h3>
              <form @submit.prevent="predictVitalSigns" class="vital-form">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">患者ID</label>
                    <input 
                      v-model="vitalForm.patientId" 
                      type="text" 
                      class="form-input"
                      placeholder="请输入患者ID"
                      required
                    >
                  </div>
                  <div class="form-group">
                    <label class="form-label">预测天数</label>
                    <select v-model.number="vitalForm.days" class="form-select">
                      <option value="1">1天</option>
                      <option value="3">3天</option>
                      <option value="7">7天</option>
                      <option value="14">14天</option>
                      <option value="30">30天</option>
                    </select>
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">当前心率</label>
                    <input 
                      v-model.number="vitalForm.heartRate" 
                      type="number" 
                      class="form-input"
                      placeholder="72"
                      min="40" 
                      max="200"
                      required
                    >
                  </div>
                  <div class="form-group">
                    <label class="form-label">当前血压</label>
                    <input 
                      v-model="vitalForm.bloodPressure" 
                      type="text" 
                      class="form-input"
                      placeholder="120/80"
                      required
                    >
                  </div>
                </div>

                <div class="form-actions">
                  <button type="submit" class="btn-primary" :disabled="isPredicting">
                    <i class="fas fa-chart-line"></i>
                    {{ isPredicting ? '预测中...' : '开始预测' }}
                  </button>
                  <button type="button" class="btn-secondary" @click="resetVitalForm">
                    <i class="fas fa-redo"></i>
                    重置表单
                  </button>
                </div>
              </form>
            </div>

            <div class="vital-charts" v-if="vitalResult">
              <h3 class="charts-title">趋势预测图表</h3>
              <div class="charts-grid">
                <div class="chart-container">
                  <h4>心率趋势</h4>
                  <div class="chart-placeholder">
                    <canvas ref="heartRateChart"></canvas>
                  </div>
                </div>
                <div class="chart-container">
                  <h4>血压趋势</h4>
                  <div class="chart-placeholder">
                    <canvas ref="bloodPressureChart"></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 患者聚类分析面板 -->
        <div v-show="activeTab === 'clustering'" class="tab-panel clustering-analysis">
          <div class="panel-content">
            <div class="clustering-controls">
              <h3 class="form-title">患者聚类分析</h3>
              <div class="control-row">
                <div class="form-group">
                  <label class="form-label">聚类数量</label>
                  <select v-model.number="clusteringForm.clusters" class="form-select">
                    <option value="3">3类</option>
                    <option value="4">4类</option>
                    <option value="5">5类</option>
                    <option value="6">6类</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">分析维度</label>
                  <select v-model="clusteringForm.dimensions" class="form-select">
                    <option value="basic">基础信息</option>
                    <option value="vital">生命体征</option>
                    <option value="comprehensive">综合分析</option>
                  </select>
                </div>
                <button class="btn-primary" @click="performClustering" :disabled="isAnalyzing">
                  <i class="fas fa-project-diagram"></i>
                  {{ isAnalyzing ? '分析中...' : '开始分析' }}
                </button>
              </div>
            </div>

            <div class="clustering-results" v-if="clusteringResult">
              <h3 class="results-title">聚类分析结果</h3>
              <div class="results-grid">
                <div 
                  v-for="(cluster, index) in clusteringResult.clusters" 
                  :key="index"
                  class="cluster-card"
                >
                  <div class="cluster-header">
                    <div class="cluster-icon" :style="{ backgroundColor: cluster.color }">
                      {{ index + 1 }}
                    </div>
                    <div class="cluster-info">
                      <h4>聚类 {{ index + 1 }}</h4>
                      <p>{{ cluster.count }} 名患者</p>
                    </div>
                  </div>
                  <div class="cluster-characteristics">
                    <h5>特征描述</h5>
                    <ul>
                      <li v-for="char in cluster.characteristics" :key="char">
                        {{ char }}
                      </li>
                    </ul>
                  </div>
                  <div class="cluster-stats">
                    <div class="stat-item">
                      <span class="stat-label">平均年龄</span>
                      <span class="stat-value">{{ cluster.avgAge }}岁</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">风险等级</span>
                      <span class="stat-value" :class="cluster.riskLevel">
                        {{ cluster.riskText }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 历史记录面板 -->
        <div v-show="activeTab === 'history'" class="tab-panel history-records">
          <div class="panel-content">
            <div class="history-header">
              <h3 class="form-title">预测历史记录</h3>
              <div class="history-controls">
                <input 
                  v-model="historySearch" 
                  type="text" 
                  class="search-input"
                  placeholder="搜索患者姓名或ID..."
                >
                <button class="btn-outline" @click="exportHistory">
                  <i class="fas fa-download"></i>
                  导出记录
                </button>
              </div>
            </div>

            <div class="history-table">
              <table>
                <thead>
                  <tr>
                    <th>时间</th>
                    <th>患者信息</th>
                    <th>预测类型</th>
                    <th>结果</th>
                    <th>置信度</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in filteredHistory" :key="record.id">
                    <td>{{ formatTime(record.time) }}</td>
                    <td>{{ record.patientName }} ({{ record.patientId }})</td>
                    <td>{{ record.type }}</td>
                    <td>{{ record.result }}</td>
                    <td>
                      <div class="confidence-small">
                        <div class="confidence-fill-small" :style="{ width: record.confidence + '%' }"></div>
                        <span>{{ record.confidence }}%</span>
                      </div>
                    </td>
                    <td>
                      <button class="btn-small" @click="viewRecord(record)">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button class="btn-small" @click="deleteRecord(record.id)">
                        <i class="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 模态框 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button class="modal-close" @click="closeModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div v-html="modalContent"></div>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" @click="closeModal">确定</button>
        </div>
      </div>
    </div>

    <!-- 通知提示 -->
    <div v-if="notification.show" class="notification" :class="notification.type">
      <div class="notification-content">
        <i :class="notification.icon"></i>
        <span>{{ notification.message }}</span>
      </div>
      <button class="notification-close" @click="hideNotification">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MLPredictionCenter',
  data() {
    return {
      // 系统状态
      systemStatus: {
        status: 'online',
        text: '系统正常运行'
      },
      lastUpdateTime: '',
      isRefreshing: false,
      
      // 统计数据
      statsData: [
        {
          id: 1,
          icon: 'fas fa-users',
          value: '1,234',
          label: '总患者数',
          color: '#4CAF50',
          trend: 'up',
          trendIcon: 'fas fa-arrow-up',
          trendValue: '+12%'
        },
        {
          id: 2,
          icon: 'fas fa-microscope',
          value: '5,678',
          label: '预测次数',
          color: '#2196F3',
          trend: 'up',
          trendIcon: 'fas fa-arrow-up',
          trendValue: '+23%'
        },
        {
          id: 3,
          icon: 'fas fa-chart-line',
          value: '94.5%',
          label: '预测准确率',
          color: '#FF9800',
          trend: 'stable',
          trendIcon: 'fas fa-minus',
          trendValue: '0%'
        },
        {
          id: 4,
          icon: 'fas fa-clock',
          value: '1.2s',
          label: '平均响应时间',
          color: '#9C27B0',
          trend: 'down',
          trendIcon: 'fas fa-arrow-down',
          trendValue: '-15%'
        }
      ],
      
      // 功能标签
      featureTabs: [
        { id: 'disease', name: '疾病预测', icon: 'fas fa-virus' },
        { id: 'vital', name: '生命体征', icon: 'fas fa-heartbeat' },
        { id: 'clustering', name: '聚类分析', icon: 'fas fa-project-diagram' },
        { id: 'history', name: '历史记录', icon: 'fas fa-history' }
      ],
      activeTab: 'disease',
      
      // 疾病预测
      diseaseForm: {
        patientName: '',
        age: '',
        gender: '',
        symptoms: '',
        temperature: '',
        bloodPressure: ''
      },
      diseaseResult: null,
      
      // 生命体征预测
      vitalForm: {
        patientId: '',
        days: 7,
        heartRate: '',
        bloodPressure: ''
      },
      vitalResult: null,
      
      // 聚类分析
      clusteringForm: {
        clusters: 4,
        dimensions: 'comprehensive'
      },
      clusteringResult: null,
      
      // 历史记录
      historySearch: '',
      historyRecords: [],
      
      // 通用状态
      isPredicting: false,
      isAnalyzing: false,
      
      // 模态框
      showModal: false,
      modalTitle: '',
      modalContent: '',
      
      // 通知
      notification: {
        show: false,
        type: 'info',
        message: '',
        icon: 'fas fa-info-circle'
      }
    }
  },
  
  computed: {
    filteredHistory() {
      if (!this.historySearch) return this.historyRecords;
      return this.historyRecords.filter(record => 
        record.patientName.includes(this.historySearch) ||
        record.patientId.includes(this.historySearch)
      );
    }
  },
  
  mounted() {
    this.updateLastTime();
    this.loadHistoryRecords();
    this.initCharts();
  },
  
  methods: {
    // 更新最后更新时间
    updateLastTime() {
      const now = new Date();
      this.lastUpdateTime = now.toLocaleString('zh-CN');
    },
    
    // 刷新数据
    async refreshData() {
      this.isRefreshing = true;
      try {
        await this.fetchSystemStatus();
        await this.fetchStatsData();
        this.updateLastTime();
        this.showNotification('数据刷新成功', 'success');
      } catch (error) {
        this.showNotification('数据刷新失败', 'error');
      } finally {
        this.isRefreshing = false;
      }
    },
    
    // 获取系统状态
    async fetchSystemStatus() {
      try {
        const response = await fetch('/api/ml/status');
        const data = await response.json();
        this.systemStatus = {
          status: data.status === 'healthy' ? 'online' : 'warning',
          text: data.message || '系统运行正常'
        };
      } catch (error) {
        this.systemStatus = {
          status: 'offline',
          text: '连接失败'
        };
      }
    },
    
    // 获取统计数据
    async fetchStatsData() {
      // 模拟数据更新
      this.statsData.forEach(stat => {
        const change = Math.random() * 10 - 5;
        if (stat.id === 1) {
          stat.value = (1234 + Math.floor(change * 10)).toLocaleString();
        } else if (stat.id === 2) {
          stat.value = (5678 + Math.floor(change * 50)).toLocaleString();
        }
      });
    },
    
    // 切换标签
    switchTab(tabId) {
      this.activeTab = tabId;
    },
    
    // 疾病预测
    async predictDisease() {
      this.isPredicting = true;
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 模拟预测结果
        this.diseaseResult = {
          patientName: this.diseaseForm.patientName,
          age: this.diseaseForm.age,
          gender: this.diseaseForm.gender,
          disease: '上呼吸道感染',
          confidence: 85,
          riskLevel: 'medium',
          riskText: '中等风险',
          suggestion: '建议进行血常规检查，注意休息，多饮水'
        };
        
        this.showNotification('疾病预测完成', 'success');
        this.saveToHistory('疾病预测', this.diseaseForm.patientName, this.diseaseResult.disease, this.diseaseResult.confidence);
      } catch (error) {
        this.showNotification('预测失败，请重试', 'error');
      } finally {
        this.isPredicting = false;
      }
    },
    
    // 重置疾病表单
    resetDiseaseForm() {
      this.diseaseForm = {
        patientName: '',
        age: '',
        gender: '',
        symptoms: '',
        temperature: '',
        bloodPressure: ''
      };
      this.diseaseResult = null;
    },
    
    // 生命体征预测
    async predictVitalSigns() {
      this.isPredicting = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 模拟预测数据
        this.vitalResult = {
          heartRate: this.generateTrendData(this.vitalForm.heartRate, this.vitalForm.days),
          bloodPressure: this.generateTrendData(this.vitalForm.bloodPressure, this.vitalForm.days)
        };
        
        this.showNotification('生命体征预测完成', 'success');
        this.updateCharts();
        this.saveToHistory('生命体征预测', this.vitalForm.patientId, '趋势预测', 92);
      } catch (error) {
        this.showNotification('预测失败，请重试', 'error');
      } finally {
        this.isPredicting = false;
      }
    },
    
    // 生成趋势数据
    generateTrendData(currentValue, days) {
      const data = [];
      const baseValue = typeof currentValue === 'string' ? 
        parseInt(currentValue.split('/')[0]) : currentValue;
      
      for (let i = 0; i <= days; i++) {
        const variation = (Math.random() - 0.5) * 10;
        data.push(baseValue + variation);
      }
      return data;
    },
    
    // 重置生命体征表单
    resetVitalForm() {
      this.vitalForm = {
        patientId: '',
        days: 7,
        heartRate: '',
        bloodPressure: ''
      };
      this.vitalResult = null;
    },
    
    // 聚类分析
    async performClustering() {
      this.isAnalyzing = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // 模拟聚类结果
        this.clusteringResult = {
          clusters: [
            {
              count: 234,
              color: '#4CAF50',
              characteristics: ['年龄较大', '慢性疾病', '需要定期随访'],
              avgAge: 65,
              riskLevel: 'high',
              riskText: '高风险'
            },
            {
              count: 456,
              color: '#2196F3',
              characteristics: ['中年群体', '轻度症状', '预防性治疗'],
              avgAge: 45,
              riskLevel: 'medium',
              riskText: '中等风险'
            },
            {
              count: 544,
              color: '#FF9800',
              characteristics: ['年轻健康', '偶发症状', '健康指导'],
              avgAge: 28,
              riskLevel: 'low',
              riskText: '低风险'
            },
            {
              count: 123,
              color: '#9C27B0',
              characteristics: ['儿童患者', '发育阶段', '专科治疗'],
              avgAge: 12,
              riskLevel: 'medium',
              riskText: '中等风险'
            }
          ]
        };
        
        this.showNotification('聚类分析完成', 'success');
        this.saveToHistory('聚类分析', '批量分析', `${this.clusteringForm.clusters}个聚类`, 88);
      } catch (error) {
        this.showNotification('分析失败，请重试', 'error');
      } finally {
        this.isAnalyzing = false;
      }
    },
    
    // 初始化图表
    initCharts() {
      // 这里可以初始化Chart.js或其他图表库
    },
    
    // 更新图表
    updateCharts() {
      // 更新图表数据
      this.$nextTick(() => {
        if (this.vitalResult) {
          this.drawHeartRateChart();
          this.drawBloodPressureChart();
        }
      });
    },
    
    // 绘制心率图表
    drawHeartRateChart() {
      // 实现心率图表绘制
    },
    
    // 绘制血压图表
    drawBloodPressureChart() {
      // 实现血压图表绘制
    },
    
    // 保存到历史记录
    saveToHistory(type, patientName, result, confidence) {
      const record = {
        id: Date.now(),
        time: new Date().toISOString(),
        type: type,
        patientName: patientName,
        patientId: this.diseaseForm.patientName || this.vitalForm.patientId || 'N/A',
        result: result,
        confidence: confidence
      };
      
      this.historyRecords.unshift(record);
      if (this.historyRecords.length > 100) {
        this.historyRecords = this.historyRecords.slice(0, 100);
      }
      
      // 保存到本地存储
      localStorage.setItem('mlPredictionHistory', JSON.stringify(this.historyRecords));
    },
    
    // 加载历史记录
    loadHistoryRecords() {
      const saved = localStorage.getItem('mlPredictionHistory');
      if (saved) {
        this.historyRecords = JSON.parse(saved);
      }
    },
    
    // 格式化时间
    formatTime(timeString) {
      const date = new Date(timeString);
      return date.toLocaleString('zh-CN');
    },
    
    // 查看记录
    viewRecord(record) {
      this.modalTitle = '预测记录详情';
      this.modalContent = `
        <p><strong>时间:</strong> ${this.formatTime(record.time)}</p>
        <p><strong>患者:</strong> ${record.patientName}</p>
        <p><strong>类型:</strong> ${record.type}</p>
        <p><strong>结果:</strong> ${record.result}</p>
        <p><strong>置信度:</strong> ${record.confidence}%</p>
      `;
      this.showModal = true;
    },
    
    // 删除记录
    deleteRecord(id) {
      this.historyRecords = this.historyRecords.filter(record => record.id !== id);
      localStorage.setItem('mlPredictionHistory', JSON.stringify(this.historyRecords));
      this.showNotification('记录已删除', 'success');
    },
    
    // 导出历史记录
    exportHistory() {
      const csv = this.convertToCSV(this.historyRecords);
      this.downloadCSV(csv, 'prediction_history.csv');
      this.showNotification('历史记录已导出', 'success');
    },
    
    // 转换为CSV
    convertToCSV(data) {
      const headers = ['时间', '患者姓名', '患者ID', '预测类型', '结果', '置信度'];
      const rows = data.map(record => [
        this.formatTime(record.time),
        record.patientName,
        record.patientId,
        record.type,
        record.result,
        record.confidence + '%'
      ]);
      
      return [headers, ...rows].map(row => row.join(',')).join('\n');
    },
    
    // 下载CSV
    downloadCSV(csv, filename) {
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      link.click();
    },
    
    // 分享结果
    shareResult(type) {
      const result = type === 'disease' ? this.diseaseResult : this.vitalResult;
      const text = `预测结果: ${result.disease || '生命体征趋势'}, 置信度: ${result.confidence || 92}%`;
      
      if (navigator.share) {
        navigator.share({
          title: '医疗预测结果',
          text: text
        });
      } else {
        navigator.clipboard.writeText(text);
        this.showNotification('结果已复制到剪贴板', 'success');
      }
    },
    
    // 打印结果
    printResult(type) {
      window.print();
    },
    
    // 保存结果
    saveResult(type) {
      this.showNotification('结果已保存', 'success');
    },
    
    // 显示通知
    showNotification(message, type = 'info') {
      const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
      };
      
      this.notification = {
        show: true,
        type: type,
        message: message,
        icon: icons[type]
      };
      
      setTimeout(() => {
        this.hideNotification();
      }, 3000);
    },
    
    // 隐藏通知
    hideNotification() {
      this.notification.show = false;
    },
    
    // 关闭模态框
    closeModal() {
      this.showModal = false;
    }
  }
}
</script>

<style scoped>
/* 页面整体布局 */
.ml-prediction-center {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 页面头部 */
.page-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1.5rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.page-title i {
  color: #667eea;
}

.page-subtitle {
  color: #6c757d;
  margin: 0;
  font-size: 1rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.system-status {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4CAF50;
  animation: pulse 2s infinite;
}

.status-indicator.warning .status-dot {
  background: #FF9800;
}

.status-indicator.offline .status-dot {
  background: #f44336;
}

.last-update {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6c757d;
  font-size: 0.875rem;
}

.refresh-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.refresh-btn:hover {
  background: #5a6fd8;
  transform: translateY(-2px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 主要内容 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* 统计卡片 */
.stats-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 45px;
  height: 45px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 0.125rem 0;
}

.stat-label {
  color: #6c757d;
  margin: 0 0 0.25rem 0;
  font-size: 0.75rem;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
  font-weight: 500;
}

.stat-trend.up {
  color: #4CAF50;
}

.stat-trend.down {
  color: #f44336;
}

.stat-trend.stable {
  color: #FF9800;
}

/* 功能区域 */
.features-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

.features-tabs {
  display: flex;
  background: rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.tab-button {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: none;
  background: transparent;
  color: #6c757d;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  font-size: 0.8rem;
}

.tab-button i {
  font-size: 0.8rem;
}

.tab-button:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.tab-button.active {
  background: #667eea;
  color: white;
}

.tab-panel {
  padding: 2rem;
  min-height: 500px;
}

.panel-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

/* 表单样式 */
.prediction-form {
  background: rgba(248, 249, 250, 0.8);
  border-radius: 16px;
  padding: 2rem;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.form-input,
.form-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-primary {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background: #5a6fd8;
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
  padding: 0.625rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.btn-small {
  background: transparent;
  color: #6c757d;
  border: 1px solid #dee2e6;
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 0.5rem;
}

.btn-small:hover {
  background: #f8f9fa;
  color: #495057;
}

/* 结果展示 */
.prediction-result {
  background: rgba(248, 249, 250, 0.8);
  border-radius: 16px;
  padding: 2rem;
}

.result-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.patient-info h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.patient-info p {
  margin: 0;
  color: #6c757d;
  font-size: 0.875rem;
}

.risk-level {
  text-align: center;
  padding: 1rem;
  border-radius: 8px;
  min-width: 120px;
}

.risk-level.high {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.risk-level.medium {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

.risk-level.low {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.risk-label {
  display: block;
  font-size: 0.75rem;
  margin-bottom: 0.25rem;
}

.risk-value {
  font-size: 1.25rem;
  font-weight: 600;
}

.prediction-details {
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
}

.detail-label {
  font-weight: 500;
  color: #495057;
}

.detail-value {
  color: #2c3e50;
  font-weight: 500;
}

.detail-value.suggestion {
  color: #667eea;
  text-align: right;
  max-width: 60%;
}

.confidence-bar {
  position: relative;
  width: 150px;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  transition: width 0.3s ease;
}

.confidence-text {
  position: absolute;
  right: -40px;
  top: -8px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #495057;
}

.result-actions {
  display: flex;
  gap: 1rem;
}

/* 图表区域 */
.vital-charts {
  grid-column: 1 / -1;
  background: rgba(248, 249, 250, 0.8);
  border-radius: 16px;
  padding: 2rem;
}

.charts-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.chart-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.chart-container h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-weight: 500;
}

.chart-placeholder {
  height: 200px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

/* 聚类分析 */
.clustering-controls {
  background: rgba(248, 249, 250, 0.8);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.control-row {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.clustering-results {
  grid-column: 1 / -1;
}

.results-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.cluster-card {
  background: rgba(248, 249, 250, 0.8);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.cluster-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.cluster-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.cluster-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1.25rem;
}

.cluster-info h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.cluster-info p {
  margin: 0;
  color: #6c757d;
  font-size: 0.875rem;
}

.cluster-characteristics {
  margin-bottom: 1rem;
}

.cluster-characteristics h5 {
  margin: 0 0 0.5rem 0;
  color: #495057;
  font-size: 0.875rem;
}

.cluster-characteristics ul {
  margin: 0;
  padding-left: 1.25rem;
  color: #6c757d;
  font-size: 0.875rem;
}

.cluster-characteristics li {
  margin-bottom: 0.25rem;
}

.cluster-stats {
  display: flex;
  justify-content: space-between;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-weight: 600;
  color: #2c3e50;
}

.stat-value.high {
  color: #f44336;
}

.stat-value.medium {
  color: #FF9800;
}

.stat-value.low {
  color: #4CAF50;
}

/* 历史记录 */
.history-records {
  grid-column: 1 / -1;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.history-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  padding: 0.5rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 0.875rem;
  width: 250px;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.history-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.history-table table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #495057;
  border-bottom: 1px solid #dee2e6;
}

.history-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f3f4;
}

.history-table tr:hover {
  background: #f8f9fa;
}

.confidence-small {
  position: relative;
  width: 80px;
  height: 6px;
  background: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
  display: inline-block;
}

.confidence-fill-small {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
}

.confidence-small span {
  position: absolute;
  right: -30px;
  top: -8px;
  font-size: 0.75rem;
  color: #6c757d;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #6c757d;
  cursor: pointer;
  padding: 0.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
}

/* 通知提示 */
.notification {
  position: fixed;
  top: 2rem;
  right: 2rem;
  background: white;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 300px;
  animation: slideIn 0.3s ease;
}

.notification.success {
  border-left: 4px solid #4CAF50;
}

.notification.error {
  border-left: 4px solid #f44336;
}

.notification.warning {
  border-left: 4px solid #FF9800;
}

.notification.info {
  border-left: 4px solid #2196F3;
}

.notification-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.notification-close {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem;
}

/* 动画 */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}

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

/* 响应式设计 */
@media (max-width: 1200px) {
  .panel-content {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header-right {
    flex-direction: column;
    gap: 1rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .features-tabs {
    flex-wrap: wrap;
  }
  
  .tab-button {
    flex: 1 1 50%;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .control-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
  
  .history-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .history-controls {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
  
  .result-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .result-actions {
    flex-wrap: wrap;
  }
  
  .notification {
    right: 1rem;
    left: 1rem;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .tab-button {
    flex: 1 1 100%;
  }
  
  .tab-panel {
    padding: 1rem;
  }
  
  .prediction-form,
  .prediction-result,
  .clustering-controls,
  .vital-charts {
    padding: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}

/* 打印样式 */
@media print {
  .page-header,
  .features-tabs,
  .form-actions,
  .result-actions,
  .notification {
    display: none;
  }
  
  .ml-prediction-center {
    background: white;
  }
  
  .tab-panel {
    padding: 0;
  }
  
  .prediction-result {
    box-shadow: none;
    border: 1px solid #dee2e6;
  }
}
</style>
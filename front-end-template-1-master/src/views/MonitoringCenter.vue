<template>
  <div class="monitoring-center-container">
    <dv-border-box-8 :dur="5">
      <div class="monitoring-center-content">
        <!-- 页面头部 -->
        <div class="header">
          <h2>医疗监测中心</h2>
          <div class="header-actions">
            <el-button-group>
              <el-button 
                :type="activeTab === 'realtime' ? 'primary' : 'default'"
                @click="switchTab('realtime')"
                icon="el-icon-video-camera"
              >
                实时监测
              </el-button>
              <el-button 
                :type="activeTab === 'vitals' ? 'primary' : 'default'"
                @click="switchTab('vitals')"
                icon="el-icon-first-aid-kit"
              >
                生命体征
              </el-button>
              <el-button 
                :type="activeTab === 'maternal' ? 'primary' : 'default'"
                @click="switchTab('maternal')"
                icon="el-icon-user"
              >
                孕产监测
              </el-button>
              <el-button 
                :type="activeTab === 'alerts' ? 'primary' : 'default'"
                @click="switchTab('alerts')"
                icon="el-icon-bell"
              >
                预警管理
              </el-button>
            </el-button-group>
          </div>
        </div>

        <!-- 实时监测页面 -->
        <div v-show="activeTab === 'realtime'" class="tab-content">
          <div class="realtime-container">
            <el-row :gutter="20">
              <!-- 监测概览 -->
              <el-col :span="24">
                <el-card class="overview-card">
                  <h3>实时监测概览</h3>
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <div class="stat-card">
                        <div class="stat-icon">
                          <i class="el-icon-user"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ overviewData.totalPatients }}</div>
                          <div class="stat-label">监测患者</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="stat-card">
                        <div class="stat-icon normal">
                          <i class="el-icon-circle-check"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ overviewData.normalPatients }}</div>
                          <div class="stat-label">正常状态</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="stat-card">
                        <div class="stat-icon warning">
                          <i class="el-icon-warning"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ overviewData.warningPatients }}</div>
                          <div class="stat-label">预警状态</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="stat-card">
                        <div class="stat-icon danger">
                          <i class="el-icon-error"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ overviewData.criticalPatients }}</div>
                          <div class="stat-label">危急状态</div>
                        </div>
                      </div>
                    </el-col>
                  </el-row>
                </el-card>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <!-- 实时数据流 -->
              <el-col :span="16">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>实时数据流</span>
                    <el-button-group style="float: right;">
                      <el-button size="small" @click="refreshRealtime">刷新</el-button>
                      <el-button size="small" @click="toggleAutoRefresh">
                        {{ autoRefresh ? '停止' : '开始' }}自动刷新
                      </el-button>
                    </el-button-group>
                  </div>
                  
                  <div class="realtime-data">
                    <div class="data-stream">
                      <div v-for="data in realtimeData" :key="data.id" class="data-item" :class="data.status">
                        <div class="patient-info">
                          <span class="patient-name">{{ data.patientName }}</span>
                          <el-tag :type="getStatusTagType(data.status)" size="mini">
                            {{ data.status }}
                          </el-tag>
                        </div>
                        <div class="vitals-info">
                          <span>血压: {{ data.bloodPressure }}</span>
                          <span>心率: {{ data.heartRate }}</span>
                          <span>体温: {{ data.temperature }}</span>
                        </div>
                        <div class="time-info">{{ formatTime(data.timestamp) }}</div>
                      </div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <!-- 预警信息 -->
              <el-col :span="8">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>预警信息</span>
                    <el-badge :value="alertCount" class="alert-badge" style="float: right;">
                      <el-button size="small" type="danger" @click="viewAllAlerts">查看全部</el-button>
                    </el-badge>
                  </div>
                  
                  <div class="alert-list">
                    <div v-for="alert in recentAlerts" :key="alert.id" class="alert-item" :class="alert.level">
                      <div class="alert-header">
                        <i class="el-icon-warning"></i>
                        <span class="alert-title">{{ alert.title }}</span>
                        <el-tag :type="getAlertTagType(alert.level)" size="mini">
                          {{ alert.level }}
                        </el-tag>
                      </div>
                      <div class="alert-content">{{ alert.content }}</div>
                      <div class="alert-time">{{ formatTime(alert.timestamp) }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 生命体征页面 -->
        <div v-show="activeTab === 'vitals'" class="tab-content">
          <div class="vitals-container">
            <el-row :gutter="20">
              <!-- 患者选择 -->
              <el-col :span="24">
                <el-card>
                  <div class="patient-selector">
                    <el-row :gutter="20">
                      <el-col :span="8">
                        <el-select v-model="selectedPatient" placeholder="选择患者" @change="handlePatientChange">
                          <el-option 
                            v-for="patient in patientList" 
                            :key="patient.id"
                            :label="patient.name" 
                            :value="patient.id"
                          ></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="8">
                        <el-date-picker
                          v-model="vitalsDateRange"
                          type="datetimerange"
                          range-separator="至"
                          start-placeholder="开始时间"
                          end-placeholder="结束时间"
                          @change="handleDateRangeChange"
                        ></el-date-picker>
                      </el-col>
                      <el-col :span="8">
                        <el-button type="primary" @click="loadVitalsData">查询</el-button>
                        <el-button @click="exportVitalsData">导出</el-button>
                      </el-col>
                    </el-row>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <!-- 生命体征图表 -->
              <el-col :span="12">
                <el-card>
                  <h4>血压趋势</h4>
                  <dv-capsule-chart 
                    :config="bloodPressureConfig" 
                    style="width:100%; height:300px;"
                  />
                </el-card>
              </el-col>
              
              <el-col :span="12">
                <el-card>
                  <h4>心率趋势</h4>
                  <dv-capsule-chart 
                    :config="heartRateConfig" 
                    style="width:100%; height:300px;"
                  />
                </el-card>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card>
                  <h4>体温趋势</h4>
                  <dv-capsule-chart 
                    :config="temperatureConfig" 
                    style="width:100%; height:300px;"
                  />
                </el-card>
              </el-col>
              
              <el-col :span="12">
                <el-card>
                  <h4>血氧饱和度</h4>
                  <dv-capsule-chart 
                    :config="oxygenConfig" 
                    style="width:100%; height:300px;"
                  />
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 孕产监测页面 -->
        <div v-show="activeTab === 'maternal'" class="tab-content">
          <div class="maternal-container">
            <el-row :gutter="20">
              <!-- 孕产妇概览 -->
              <el-col :span="24">
                <el-card>
                  <h3>孕产妇监测概览</h3>
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <div class="maternal-stat-card">
                        <div class="stat-icon maternal">
                          <i class="el-icon-user"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ maternalOverview.total }}</div>
                          <div class="stat-label">监测孕产妇</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="maternal-stat-card">
                        <div class="stat-icon first-trimester">
                          <i class="el-icon-time"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ maternalOverview.firstTrimester }}</div>
                          <div class="stat-label">早期妊娠</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="maternal-stat-card">
                        <div class="stat-icon second-trimester">
                          <i class="el-icon-time"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ maternalOverview.secondTrimester }}</div>
                          <div class="stat-label">中期妊娠</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="maternal-stat-card">
                        <div class="stat-icon third-trimester">
                          <i class="el-icon-time"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ maternalOverview.thirdTrimester }}</div>
                          <div class="stat-label">晚期妊娠</div>
                        </div>
                      </div>
                    </el-col>
                  </el-row>
                </el-card>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <!-- 孕产妇列表 -->
              <el-col :span="16">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>孕产妇列表</span>
                    <el-button-group style="float: right;">
                      <el-button size="small" @click="refreshMaternalList">刷新</el-button>
                      <el-button size="small" @click="addMaternalPatient">添加</el-button>
                    </el-button-group>
                  </div>
                  
                  <el-table :data="maternalList" border>
                    <el-table-column prop="name" label="姓名" width="100"></el-table-column>
                    <el-table-column prop="age" label="年龄" width="80"></el-table-column>
                    <el-table-column prop="gestationalWeeks" label="孕周" width="80"></el-table-column>
                    <el-table-column prop="riskLevel" label="风险等级" width="100">
                      <template slot-scope="scope">
                        <el-tag :type="getRiskTagType(scope.row.riskLevel)">
                          {{ scope.row.riskLevel }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="lastCheckup" label="末次检查" width="150">
                      <template slot-scope="scope">
                        {{ formatDate(scope.row.lastCheckup) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="nextCheckup" label="下次检查" width="150">
                      <template slot-scope="scope">
                        {{ formatDate(scope.row.nextCheckup) }}
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="200">
                      <template slot-scope="scope">
                        <el-button size="mini" @click="viewMaternalDetails(scope.row)">详情</el-button>
                        <el-button size="mini" type="primary" @click="recordCheckup(scope.row)">记录</el-button>
                        <el-button size="mini" type="warning" @click="updateRisk(scope.row)">评估</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-card>
              </el-col>
              
              <!-- 检查提醒 -->
              <el-col :span="8">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>检查提醒</span>
                    <el-badge :value="reminderCount" class="reminder-badge" style="float: right;">
                      <el-button size="small" type="primary">全部提醒</el-button>
                    </el-badge>
                  </div>
                  
                  <div class="reminder-list">
                    <div v-for="reminder in checkupReminders" :key="reminder.id" class="reminder-item">
                      <div class="reminder-header">
                        <i class="el-icon-bell"></i>
                        <span class="reminder-patient">{{ reminder.patientName }}</span>
                        <el-tag :type="getReminderTagType(reminder.urgency)" size="mini">
                          {{ reminder.urgency }}
                        </el-tag>
                      </div>
                      <div class="reminder-content">{{ reminder.checkupType }}</div>
                      <div class="reminder-time">{{ formatDate(reminder.scheduledDate) }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 预警管理页面 -->
        <div v-show="activeTab === 'alerts'" class="tab-content">
          <div class="alerts-container">
            <el-row :gutter="20">
              <!-- 预警统计 -->
              <el-col :span="24">
                <el-card>
                  <h3>预警统计</h3>
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <div class="alert-stat-card">
                        <div class="stat-icon low">
                          <i class="el-icon-info"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ alertStats.low }}</div>
                          <div class="stat-label">低级预警</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="alert-stat-card">
                        <div class="stat-icon medium">
                          <i class="el-icon-warning"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ alertStats.medium }}</div>
                          <div class="stat-label">中级预警</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="alert-stat-card">
                        <div class="stat-icon high">
                          <i class="el-icon-warning-outline"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ alertStats.high }}</div>
                          <div class="stat-label">高级预警</div>
                        </div>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="alert-stat-card">
                        <div class="stat-icon critical">
                          <i class="el-icon-error"></i>
                        </div>
                        <div class="stat-content">
                          <div class="stat-number">{{ alertStats.critical }}</div>
                          <div class="stat-label">危急预警</div>
                        </div>
                      </div>
                    </el-col>
                  </el-row>
                </el-card>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <!-- 预警列表 -->
              <el-col :span="24">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>预警列表</span>
                    <el-button-group style="float: right;">
                      <el-button size="small" @click="refreshAlerts">刷新</el-button>
                      <el-button size="small" @click="exportAlerts">导出</el-button>
                    </el-button-group>
                  </div>
                  
                  <div class="alert-filters">
                    <el-row :gutter="20">
                      <el-col :span="6">
                        <el-select v-model="alertFilters.level" placeholder="预警级别" @change="filterAlerts">
                          <el-option label="全部" value=""></el-option>
                          <el-option label="低级" value="low"></el-option>
                          <el-option label="中级" value="medium"></el-option>
                          <el-option label="高级" value="high"></el-option>
                          <el-option label="危急" value="critical"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="alertFilters.status" placeholder="处理状态" @change="filterAlerts">
                          <el-option label="全部" value=""></el-option>
                          <el-option label="待处理" value="pending"></el-option>
                          <el-option label="处理中" value="processing"></el-option>
                          <el-option label="已处理" value="resolved"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-date-picker
                          v-model="alertFilters.dateRange"
                          type="daterange"
                          range-separator="至"
                          start-placeholder="开始日期"
                          end-placeholder="结束日期"
                          @change="filterAlerts"
                        ></el-date-picker>
                      </el-col>
                      <el-col :span="6">
                        <el-button type="primary" @click="filterAlerts">筛选</el-button>
                        <el-button @click="resetAlertFilters">重置</el-button>
                      </el-col>
                    </el-row>
                  </div>
                  
                  <el-table :data="filteredAlerts" border>
                    <el-table-column prop="id" label="ID" width="80"></el-table-column>
                    <el-table-column prop="patientName" label="患者姓名" width="120"></el-table-column>
                    <el-table-column prop="type" label="预警类型" width="120"></el-table-column>
                    <el-table-column prop="level" label="级别" width="80">
                      <template slot-scope="scope">
                        <el-tag :type="getAlertTagType(scope.row.level)">
                          {{ scope.row.level }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="content" label="预警内容" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="status" label="状态" width="100">
                      <template slot-scope="scope">
                        <el-tag :type="getStatusTagType(scope.row.status)">
                          {{ scope.row.status }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="createdAt" label="创建时间" width="150">
                      <template slot-scope="scope">
                        {{ formatDateTime(scope.row.createdAt) }}
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="200">
                      <template slot-scope="scope">
                        <el-button size="mini" @click="viewAlertDetails(scope.row)">详情</el-button>
                        <el-button size="mini" type="primary" @click="handleAlert(scope.row)">处理</el-button>
                        <el-button size="mini" type="success" @click="resolveAlert(scope.row)">解决</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
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
  name: 'MonitoringCenter',
  data() {
    return {
      activeTab: 'realtime',
      autoRefresh: false,
      refreshTimer: null,
      
      // 实时监测数据
      overviewData: {
        totalPatients: 156,
        normalPatients: 120,
        warningPatients: 28,
        criticalPatients: 8
      },
      
      realtimeData: [],
      recentAlerts: [],
      alertCount: 5,
      
      // 生命体征数据
      selectedPatient: '',
      patientList: [],
      vitalsDateRange: null,
      
      bloodPressureConfig: {
        data: []
      },
      
      heartRateConfig: {
        data: []
      },
      
      temperatureConfig: {
        data: []
      },
      
      oxygenConfig: {
        data: []
      },
      
      // 孕产妇数据
      maternalOverview: {
        total: 45,
        firstTrimester: 12,
        secondTrimester: 18,
        thirdTrimester: 15
      },
      
      maternalList: [],
      checkupReminders: [],
      reminderCount: 8,
      
      // 预警管理数据
      alertStats: {
        low: 12,
        medium: 8,
        high: 5,
        critical: 2
      },
      
      alertFilters: {
        level: '',
        status: '',
        dateRange: null
      },
      
      allAlerts: [],
      filteredAlerts: []
    }
  },
  
  methods: {
    // 切换标签页
    switchTab(tab) {
      this.activeTab = tab
      if (tab === 'realtime') {
        this.startAutoRefresh()
      } else {
        this.stopAutoRefresh()
      }
    },
    
    // 开始自动刷新
    startAutoRefresh() {
      this.autoRefresh = true
      this.refreshTimer = setInterval(() => {
        this.refreshRealtime()
      }, 5000)
    },
    
    // 停止自动刷新
    stopAutoRefresh() {
      this.autoRefresh = false
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer)
        this.refreshTimer = null
      }
    },
    
    // 切换自动刷新
    toggleAutoRefresh() {
      if (this.autoRefresh) {
        this.stopAutoRefresh()
      } else {
        this.startAutoRefresh()
      }
    },
    
    // 刷新实时数据
    async refreshRealtime() {
      try {
        const response = await axios.get('/api/monitoring/realtime')
        if (response.data.code === 200) {
          this.realtimeData = response.data.data.realtimeData
          this.recentAlerts = response.data.data.recentAlerts
          this.alertCount = response.data.data.alertCount
        }
      } catch (error) {
        console.error('刷新实时数据失败:', error)
      }
    },
    
    // 查看所有预警
    viewAllAlerts() {
      this.activeTab = 'alerts'
    },
    
    // 格式化时间
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString('zh-CN')
    },
    
    formatDateTime(timestamp) {
      return new Date(timestamp).toLocaleString('zh-CN')
    },
    
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('zh-CN')
    },
    
    // 获取状态标签类型
    getStatusTagType(status) {
      switch (status) {
        case 'normal': return 'success'
        case 'warning': return 'warning'
        case 'critical': return 'danger'
        case 'pending': return 'warning'
        case 'processing': return 'primary'
        case 'resolved': return 'success'
        default: return 'info'
      }
    },
    
    // 获取预警标签类型
    getAlertTagType(level) {
      switch (level) {
        case 'low': return 'info'
        case 'medium': return 'warning'
        case 'high': return 'danger'
        case 'critical': return 'danger'
        default: return 'info'
      }
    },
    
    // 获取风险标签类型
    getRiskTagType(risk) {
      switch (risk) {
        case '低风险': return 'success'
        case '中风险': return 'warning'
        case '高风险': return 'danger'
        default: return 'info'
      }
    },
    
    // 获取提醒标签类型
    getReminderTagType(urgency) {
      switch (urgency) {
        case '普通': return 'info'
        case '重要': return 'warning'
        case '紧急': return 'danger'
        default: return 'info'
      }
    },
    
    // 患者变化处理
    handlePatientChange() {
      this.loadVitalsData()
    },
    
    // 日期范围变化处理
    handleDateRangeChange() {
      this.loadVitalsData()
    },
    
    // 加载生命体征数据
    async loadVitalsData() {
      if (!this.selectedPatient) return
      
      try {
        const response = await axios.get('/api/monitoring/vitals', {
          params: {
            patientId: this.selectedPatient,
            startDate: this.vitalsDateRange?.[0],
            endDate: this.vitalsDateRange?.[1]
          }
        })
        
        if (response.data.code === 200) {
          const data = response.data.data
          this.bloodPressureConfig = { data: data.bloodPressure }
          this.heartRateConfig = { data: data.heartRate }
          this.temperatureConfig = { data: data.temperature }
          this.oxygenConfig = { data: data.oxygen }
        }
      } catch (error) {
        console.error('加载生命体征数据失败:', error)
      }
    },
    
    // 导出生命体征数据
    exportVitalsData() {
      this.$message.success('生命体征数据已导出')
    },
    
    // 刷新孕产妇列表
    async refreshMaternalList() {
      try {
        const response = await axios.get('/api/monitoring/maternal')
        if (response.data.code === 200) {
          this.maternalList = response.data.data.maternalList
          this.checkupReminders = response.data.data.reminders
          this.reminderCount = response.data.data.reminders.length
        }
      } catch (error) {
        console.error('刷新孕产妇列表失败:', error)
      }
    },
    
    // 添加孕产妇
    addMaternalPatient() {
      this.$message.info('添加孕产妇功能')
    },
    
    // 查看孕产妇详情
    viewMaternalDetails(patient) {
      console.log('查看孕产妇详情:', patient)
    },
    
    // 记录检查
    recordCheckup(patient) {
      console.log('记录检查:', patient)
    },
    
    // 更新风险评估
    updateRisk(patient) {
      console.log('更新风险评估:', patient)
    },
    
    // 刷新预警列表
    async refreshAlerts() {
      try {
        const response = await axios.get('/api/monitoring/alerts')
        if (response.data.code === 200) {
          this.allAlerts = response.data.data
          this.filteredAlerts = [...this.allAlerts]
        }
      } catch (error) {
        console.error('刷新预警列表失败:', error)
      }
    },
    
    // 筛选预警
    filterAlerts() {
      this.filteredAlerts = this.allAlerts.filter(alert => {
        if (this.alertFilters.level && alert.level !== this.alertFilters.level) {
          return false
        }
        if (this.alertFilters.status && alert.status !== this.alertFilters.status) {
          return false
        }
        if (this.alertFilters.dateRange) {
          const alertDate = new Date(alert.createdAt)
          if (alertDate < this.alertFilters.dateRange[0] || alertDate > this.alertFilters.dateRange[1]) {
            return false
          }
        }
        return true
      })
    },
    
    // 重置预警筛选
    resetAlertFilters() {
      this.alertFilters = {
        level: '',
        status: '',
        dateRange: null
      }
      this.filteredAlerts = [...this.allAlerts]
    },
    
    // 导出预警数据
    exportAlerts() {
      this.$message.success('预警数据已导出')
    },
    
    // 查看预警详情
    viewAlertDetails(alert) {
      console.log('查看预警详情:', alert)
    },
    
    // 处理预警
    handleAlert(alert) {
      console.log('处理预警:', alert)
    },
    
    // 解决预警
    async resolveAlert(alert) {
      try {
        const response = await axios.put(`/api/monitoring/alerts/${alert.id}/resolve`)
        if (response.data.code === 200) {
          this.$message.success('预警已解决')
          this.refreshAlerts()
        }
      } catch (error) {
        console.error('解决预警失败:', error)
        this.$message.error('解决预警失败')
      }
    }
  },
  
  created() {
    // 初始化数据
    this.refreshRealtime()
    this.refreshMaternalList()
    this.refreshAlerts()
    
    // 初始化患者列表
    this.patientList = [
      { id: 1, name: '张三' },
      { id: 2, name: '李四' },
      { id: 3, name: '王五' }
    ]
    
    // 初始化模拟数据
    this.realtimeData = [
      {
        id: 1,
        patientName: '张三',
        status: 'normal',
        bloodPressure: '120/80',
        heartRate: '72',
        temperature: '36.5°C',
        timestamp: new Date()
      },
      {
        id: 2,
        patientName: '李四',
        status: 'warning',
        bloodPressure: '140/90',
        heartRate: '85',
        temperature: '37.2°C',
        timestamp: new Date()
      }
    ]
    
    this.recentAlerts = [
      {
        id: 1,
        title: '血压异常',
        content: '患者李四血压偏高，需要关注',
        level: 'medium',
        timestamp: new Date()
      }
    ]
    
    this.maternalList = [
      {
        id: 1,
        name: '赵六',
        age: 28,
        gestationalWeeks: 24,
        riskLevel: '低风险',
        lastCheckup: new Date(),
        nextCheckup: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    ]
    
    this.checkupReminders = [
      {
        id: 1,
        patientName: '赵六',
        checkupType: '常规产检',
        urgency: '重要',
        scheduledDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    ]
    
    this.allAlerts = [
      {
        id: 1,
        patientName: '张三',
        type: '血压异常',
        level: 'medium',
        content: '血压持续偏高，建议进一步检查',
        status: 'pending',
        createdAt: new Date()
      }
    ]
    
    this.filteredAlerts = [...this.allAlerts]
  },
  
  beforeDestroy() {
    this.stopAutoRefresh()
  }
}
</script>

<style scoped>
.monitoring-center-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.monitoring-center-content {
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

/* 统计卡片样式 */
.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #409eff;
  color: white;
  margin-right: 15px;
}

.stat-icon.normal {
  background: #67c23a;
}

.stat-icon.warning {
  background: #e6a23c;
}

.stat-icon.danger {
  background: #f56c6c;
}

.stat-icon.maternal {
  background: #ff6b9d;
}

.stat-icon.first-trimester {
  background: #66d9ef;
}

.stat-icon.second-trimester {
  background: #a29bfe;
}

.stat-icon.third-trimester {
  background: #fd79a8;
}

.stat-icon.low {
  background: #909399;
}

.stat-icon.medium {
  background: #e6a23c;
}

.stat-icon.high {
  background: #ff6b6b;
}

.stat-icon.critical {
  background: #ff3838;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

/* 实时数据样式 */
.data-stream {
  max-height: 400px;
  overflow-y: auto;
}

.data-item {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  border-left: 4px solid;
}

.data-item.normal {
  background: #f0f9ff;
  border-left-color: #67c23a;
}

.data-item.warning {
  background: #fdf6ec;
  border-left-color: #e6a23c;
}

.data-item.critical {
  background: #fef0f0;
  border-left-color: #f56c6c;
}

.patient-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.patient-name {
  font-weight: bold;
  color: #333;
}

.vitals-info {
  display: flex;
  gap: 15px;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.time-info {
  font-size: 12px;
  color: #999;
}

/* 预警列表样式 */
.alert-list {
  max-height: 400px;
  overflow-y: auto;
}

.alert-item {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  border-left: 4px solid;
}

.alert-item.low {
  background: #f4f4f5;
  border-left-color: #909399;
}

.alert-item.medium {
  background: #fdf6ec;
  border-left-color: #e6a23c;
}

.alert-item.high {
  background: #fef0f0;
  border-left-color: #f56c6c;
}

.alert-item.critical {
  background: #fef0f0;
  border-left-color: #ff3838;
}

.alert-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.alert-title {
  flex: 1;
  margin: 0 10px;
  font-weight: bold;
  color: #333;
}

.alert-content {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.alert-time {
  font-size: 12px;
  color: #999;
}

/* 患者选择器样式 */
.patient-selector {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

/* 孕产妇列表样式 */
.maternal-stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 提醒列表样式 */
.reminder-list {
  max-height: 400px;
  overflow-y: auto;
}

.reminder-item {
  padding: 15px;
  margin-bottom: 10px;
  background: #f8f9fa;
  border-radius: 8px;
}

.reminder-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.reminder-patient {
  flex: 1;
  margin: 0 10px;
  font-weight: bold;
  color: #333;
}

.reminder-content {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.reminder-time {
  font-size: 12px;
  color: #999;
}

/* 预警筛选样式 */
.alert-filters {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
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
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    margin-right: 0;
    margin-bottom: 10px;
  }
  
  .vitals-info {
    flex-direction: column;
    gap: 5px;
  }
  
  .alert-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .alert-title {
    margin: 5px 0;
  }
}
</style>
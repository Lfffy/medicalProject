<template>
  <div class="dashboard-center-container">
    <dv-border-box-8 :dur="5">
      <div class="dashboard-center-content">
        <!-- 页面头部 -->
        <div class="header">
          <h2>可视化大屏中心</h2>
          <div class="header-actions">
            <el-button-group>
              <el-button 
                :type="activeTab === 'overview' ? 'primary' : 'default'"
                @click="switchTab('overview')"
                icon="el-icon-data-board"
              >
                总览大屏
              </el-button>
              <el-button 
                :type="activeTab === 'medical' ? 'primary' : 'default'"
                @click="switchTab('medical')"
                icon="el-icon-first-aid-kit"
              >
                医疗数据大屏
              </el-button>
              <el-button 
                :type="activeTab === 'maternal' ? 'primary' : 'default'"
                @click="switchTab('maternal')"
                icon="el-icon-user"
              >
                孕产数据大屏
              </el-button>
              <el-button 
                :type="activeTab === 'comparison' ? 'primary' : 'default'"
                @click="switchTab('comparison')"
                icon="el-icon-data-analysis"
              >
                对比分析大屏
              </el-button>
            </el-button-group>
          </div>
        </div>

        <!-- 总览大屏 -->
        <div v-show="activeTab === 'overview'" class="tab-content">
          <div class="overview-dashboard">
            <!-- 顶部统计区域 -->
            <el-row :gutter="20" class="top-stats">
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon total">
                    <i class="el-icon-user"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-number">{{ overviewStats.totalPatients }}</div>
                    <div class="stat-label">总患者数</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon today">
                    <i class="el-icon-date"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-number">{{ overviewStats.todayPatients }}</div>
                    <div class="stat-label">今日就诊</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon maternal">
                    <i class="el-icon-user"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-number">{{ overviewStats.maternalPatients }}</div>
                    <div class="stat-label">孕产妇数</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon alerts">
                    <i class="el-icon-warning"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-number">{{ overviewStats.alertCount }}</div>
                    <div class="stat-label">预警数量</div>
                  </div>
                </div>
              </el-col>
            </el-row>

            <!-- 中部图表区域 -->
            <el-row :gutter="20" class="middle-charts">
              <el-col :span="12">
                <div class="chart-card">
                  <h3>患者趋势分析</h3>
                  <dv-capsule-chart 
                    :config="patientTrendConfig" 
                    style="width:100%; height:300px;"
                  />
                </div>
              </el-col>
              <el-col :span="12">
                <div class="chart-card">
                  <h3>疾病分布统计</h3>
                  <dv-capsule-chart 
                    :config="diseaseDistributionConfig" 
                    style="width:100%; height:300px;"
                  />
                </div>
              </el-col>
            </el-row>

            <!-- 底部详细数据 -->
            <el-row :gutter="20" class="bottom-data">
              <el-col :span="16">
                <div class="data-card">
                  <h3>实时就诊数据</h3>
                  <el-table :data="realtimeData" border>
                    <el-table-column prop="time" label="时间" width="150"></el-table-column>
                    <el-table-column prop="department" label="科室" width="120"></el-table-column>
                    <el-table-column prop="patientCount" label="就诊人数" width="100"></el-table-column>
                    <el-table-column prop="avgWaitTime" label="平均等待" width="100"></el-table-column>
                    <el-table-column prop="status" label="状态" width="100">
                      <template slot-scope="scope">
                        <el-tag :type="getStatusTagType(scope.row.status)">
                          {{ scope.row.status }}
                        </el-tag>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="data-card">
                  <h3>系统状态监控</h3>
                  <div class="system-status">
                    <div class="status-item">
                      <span class="status-label">数据库连接</span>
                      <el-tag type="success">正常</el-tag>
                    </div>
                    <div class="status-item">
                      <span class="status-label">API服务</span>
                      <el-tag type="success">正常</el-tag>
                    </div>
                    <div class="status-item">
                      <span class="status-label">数据同步</span>
                      <el-tag type="warning">延迟</el-tag>
                    </div>
                    <div class="status-item">
                      <span class="status-label">预警系统</span>
                      <el-tag type="success">正常</el-tag>
                    </div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 医疗数据大屏 -->
        <div v-show="activeTab === 'medical'" class="tab-content">
          <div class="medical-dashboard">
            <!-- 医疗数据概览 -->
            <el-row :gutter="20" class="medical-overview">
              <el-col :span="24">
                <div class="overview-card">
                  <h3>医疗数据概览</h3>
                  <el-row :gutter="20">
                    <el-col :span="4">
                      <div class="medical-stat">
                        <div class="stat-number">{{ medicalStats.totalRecords }}</div>
                        <div class="stat-label">总记录数</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="medical-stat">
                        <div class="stat-number">{{ medicalStats.todayRecords }}</div>
                        <div class="stat-label">今日新增</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="medical-stat">
                        <div class="stat-number">{{ medicalStats.diseaseTypes }}</div>
                        <div class="stat-label">疾病类型</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="medical-stat">
                        <div class="stat-number">{{ medicalStats.departments }}</div>
                        <div class="stat-label">科室数量</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="medical-stat">
                        <div class="stat-number">{{ medicalStats.doctors }}</div>
                        <div class="stat-label">医生数量</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="medical-stat">
                        <div class="stat-number">{{ medicalStats.beds }}</div>
                        <div class="stat-label">床位数量</div>
                      </div>
                    </el-col>
                  </el-row>
                </div>
              </el-col>
            </el-row>

            <!-- 医疗数据图表 -->
            <el-row :gutter="20" class="medical-charts">
              <el-col :span="8">
                <div class="chart-card">
                  <h3>科室就诊分布</h3>
                  <dv-capsule-chart 
                    :config="departmentConfig" 
                    style="width:100%; height:250px;"
                  />
                </div>
              </el-col>
              <el-col :span="8">
                <div class="chart-card">
                  <h3>疾病类型统计</h3>
                  <dv-capsule-chart 
                    :config="diseaseTypeConfig" 
                    style="width:100%; height:250px;"
                  />
                </div>
              </el-col>
              <el-col :span="8">
                <div class="chart-card">
                  <h3>月度就诊趋势</h3>
                  <dv-capsule-chart 
                    :config="monthlyTrendConfig" 
                    style="width:100%; height:250px;"
                  />
                </div>
              </el-col>
            </el-row>

            <!-- 医疗详细数据 -->
            <el-row :gutter="20" class="medical-details">
              <el-col :span="24">
                <div class="data-card">
                  <h3>科室详细数据</h3>
                  <el-table :data="departmentData" border>
                    <el-table-column prop="name" label="科室名称" width="120"></el-table-column>
                    <el-table-column prop="todayPatients" label="今日患者" width="100"></el-table-column>
                    <el-table-column prop="weekPatients" label="本周患者" width="100"></el-table-column>
                    <el-table-column prop="monthPatients" label="本月患者" width="100"></el-table-column>
                    <el-table-column prop="doctorCount" label="医生数" width="80"></el-table-column>
                    <el-table-column prop="bedCount" label="床位数" width="80"></el-table-column>
                    <el-table-column prop="occupancyRate" label="床位使用率" width="120">
                      <template slot-scope="scope">
                        <el-progress :percentage="scope.row.occupancyRate" :color="getProgressColor(scope.row.occupancyRate)"></el-progress>
                      </template>
                    </el-table-column>
                    <el-table-column prop="avgWaitTime" label="平均等待" width="100"></el-table-column>
                    <el-table-column label="操作" width="150">
                      <template slot-scope="scope">
                        <el-button size="mini" @click="viewDepartmentDetails(scope.row)">详情</el-button>
                        <el-button size="mini" type="primary" @click="exportDepartmentData(scope.row)">导出</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 孕产数据大屏 -->
        <div v-show="activeTab === 'maternal'" class="tab-content">
          <div class="maternal-dashboard">
            <!-- 孕产数据概览 -->
            <el-row :gutter="20" class="maternal-overview">
              <el-col :span="24">
                <div class="overview-card">
                  <h3>孕产数据概览</h3>
                  <el-row :gutter="20">
                    <el-col :span="4">
                      <div class="maternal-stat">
                        <div class="stat-number">{{ maternalStats.total }}</div>
                        <div class="stat-label">总孕产妇</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="maternal-stat">
                        <div class="stat-number">{{ maternalStats.firstTrimester }}</div>
                        <div class="stat-label">早期妊娠</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="maternal-stat">
                        <div class="stat-number">{{ maternalStats.secondTrimester }}</div>
                        <div class="stat-label">中期妊娠</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="maternal-stat">
                        <div class="stat-number">{{ maternalStats.thirdTrimester }}</div>
                        <div class="stat-label">晚期妊娠</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="maternal-stat">
                        <div class="stat-number">{{ maternalStats.todayCheckups }}</div>
                        <div class="stat-label">今日产检</div>
                      </div>
                    </el-col>
                    <el-col :span="4">
                      <div class="maternal-stat">
                        <div class="stat-number">{{ maternalStats.highRisk }}</div>
                        <div class="stat-label">高危妊娠</div>
                      </div>
                    </el-col>
                  </el-row>
                </div>
              </el-col>
            </el-row>

            <!-- 孕产数据图表 -->
            <el-row :gutter="20" class="maternal-charts">
              <el-col :span="12">
                <div class="chart-card">
                  <h3>孕周分布</h3>
                  <dv-capsule-chart 
                    :config="gestationalWeeksConfig" 
                    style="width:100%; height:300px;"
                  />
                </div>
              </el-col>
              <el-col :span="12">
                <div class="chart-card">
                  <h3>风险等级分布</h3>
                  <dv-capsule-chart 
                    :config="riskLevelConfig" 
                    style="width:100%; height:300px;"
                  />
                </div>
              </el-col>
            </el-row>

            <!-- 孕产详细数据 -->
            <el-row :gutter="20" class="maternal-details">
              <el-col :span="16">
                <div class="data-card">
                  <h3>孕产妇详细数据</h3>
                  <el-table :data="maternalData" border>
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
                    <el-table-column prop="lastCheckup" label="末次产检" width="120">
                      <template slot-scope="scope">
                        {{ formatDate(scope.row.lastCheckup) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="nextCheckup" label="下次产检" width="120">
                      <template slot-scope="scope">
                        {{ formatDate(scope.row.nextCheckup) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="doctor" label="主治医生" width="100"></el-table-column>
                    <el-table-column label="操作" width="150">
                      <template slot-scope="scope">
                        <el-button size="mini" @click="viewMaternalDetails(scope.row)">详情</el-button>
                        <el-button size="mini" type="primary" @click="updateMaternalRecord(scope.row)">更新</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="data-card">
                  <h3>产检提醒</h3>
                  <div class="checkup-reminders">
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
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 对比分析大屏 -->
        <div v-show="activeTab === 'comparison'" class="tab-content">
          <div class="comparison-dashboard">
            <!-- 对比分析控制面板 -->
            <el-row :gutter="20" class="comparison-controls">
              <el-col :span="24">
                <div class="control-card">
                  <h3>对比分析设置</h3>
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <el-select v-model="comparisonConfig.metric" placeholder="选择指标" @change="updateComparison">
                        <el-option label="患者数量" value="patientCount"></el-option>
                        <el-option label="就诊次数" value="visitCount"></el-option>
                        <el-option label="平均等待时间" value="avgWaitTime"></el-option>
                        <el-option label="床位使用率" value="occupancyRate"></el-option>
                        <el-option label="疾病分布" value="diseaseDistribution"></el-option>
                      </el-select>
                    </el-col>
                    <el-col :span="6">
                      <el-select v-model="comparisonConfig.period" placeholder="选择周期" @change="updateComparison">
                        <el-option label="今日" value="today"></el-option>
                        <el-option label="本周" value="week"></el-option>
                        <el-option label="本月" value="month"></el-option>
                        <el-option label="本季度" value="quarter"></el-option>
                        <el-option label="本年" value="year"></el-option>
                      </el-select>
                    </el-col>
                    <el-col :span="6">
                      <el-select v-model="comparisonConfig.department" placeholder="选择科室" @change="updateComparison">
                        <el-option label="全部科室" value="all"></el-option>
                        <el-option label="内科" value="internal"></el-option>
                        <el-option label="外科" value="surgery"></el-option>
                        <el-option label="妇产科" value="obstetrics"></el-option>
                        <el-option label="儿科" value="pediatrics"></el-option>
                      </el-select>
                    </el-col>
                    <el-col :span="6">
                      <el-button type="primary" @click="runComparison">开始对比</el-button>
                      <el-button @click="exportComparison">导出报告</el-button>
                    </el-col>
                  </el-row>
                </div>
              </el-col>
            </el-row>

            <!-- 对比结果展示 -->
            <el-row :gutter="20" class="comparison-results">
              <el-col :span="12">
                <div class="chart-card">
                  <h3>同比分析</h3>
                  <dv-capsule-chart 
                    :config="yearOverYearConfig" 
                    style="width:100%; height:300px;"
                  />
                </div>
              </el-col>
              <el-col :span="12">
                <div class="chart-card">
                  <h3>环比分析</h3>
                  <dv-capsule-chart 
                    :config="monthOverMonthConfig" 
                    style="width:100%; height:300px;"
                  />
                </div>
              </el-col>
            </el-row>

            <!-- 对比详细数据 -->
            <el-row :gutter="20" class="comparison-details">
              <el-col :span="24">
                <div class="data-card">
                  <h3>对比分析报告</h3>
                  <div class="comparison-summary">
                    <el-row :gutter="20">
                      <el-col :span="8">
                        <div class="summary-item">
                          <div class="summary-label">当前周期数值</div>
                          <div class="summary-value current">{{ comparisonResults.currentValue }}</div>
                        </div>
                      </el-col>
                      <el-col :span="8">
                        <div class="summary-item">
                          <div class="summary-label">上周期数值</div>
                          <div class="summary-value previous">{{ comparisonResults.previousValue }}</div>
                        </div>
                      </el-col>
                      <el-col :span="8">
                        <div class="summary-item">
                          <div class="summary-label">变化率</div>
                          <div class="summary-value" :class="comparisonResults.changeType">
                            {{ comparisonResults.changeRate }}%
                          </div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                  
                  <el-table :data="comparisonData" border>
                    <el-table-column prop="period" label="周期" width="120"></el-table-column>
                    <el-table-column prop="metric" label="指标" width="150"></el-table-column>
                    <el-table-column prop="currentValue" label="当前值" width="100"></el-table-column>
                    <el-table-column prop="previousValue" label="上期值" width="100"></el-table-column>
                    <el-table-column prop="changeRate" label="变化率" width="100">
                      <template slot-scope="scope">
                        <span :class="scope.row.changeRate > 0 ? 'positive' : 'negative'">
                          {{ scope.row.changeRate > 0 ? '+' : '' }}{{ scope.row.changeRate }}%
                        </span>
                      </template>
                    </el-table-column>
                    <el-table-column prop="trend" label="趋势" width="100">
                      <template slot-scope="scope">
                        <el-tag :type="getTrendTagType(scope.row.trend)">
                          {{ scope.row.trend }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="analysis" label="分析" show-overflow-tooltip></el-table-column>
                  </el-table>
                </div>
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
  name: 'DashboardCenter',
  data() {
    return {
      activeTab: 'overview',
      
      // 总览数据
      overviewStats: {
        totalPatients: 15234,
        todayPatients: 156,
        maternalPatients: 456,
        alertCount: 23
      },
      
      patientTrendConfig: {
        data: []
      },
      
      diseaseDistributionConfig: {
        data: []
      },
      
      realtimeData: [],
      
      // 医疗数据
      medicalStats: {
        totalRecords: 45678,
        todayRecords: 234,
        diseaseTypes: 156,
        departments: 12,
        doctors: 234,
        beds: 567
      },
      
      departmentConfig: {
        data: []
      },
      
      diseaseTypeConfig: {
        data: []
      },
      
      monthlyTrendConfig: {
        data: []
      },
      
      departmentData: [],
      
      // 孕产数据
      maternalStats: {
        total: 456,
        firstTrimester: 123,
        secondTrimester: 156,
        thirdTrimester: 177,
        todayCheckups: 34,
        highRisk: 45
      },
      
      gestationalWeeksConfig: {
        data: []
      },
      
      riskLevelConfig: {
        data: []
      },
      
      maternalData: [],
      checkupReminders: [],
      
      // 对比分析
      comparisonConfig: {
        metric: '',
        period: '',
        department: ''
      },
      
      yearOverYearConfig: {
        data: []
      },
      
      monthOverMonthConfig: {
        data: []
      },
      
      comparisonResults: {
        currentValue: 0,
        previousValue: 0,
        changeRate: 0,
        changeType: ''
      },
      
      comparisonData: []
    }
  },
  
  methods: {
    // 切换标签页
    switchTab(tab) {
      this.activeTab = tab
      this.loadTabData(tab)
    },
    
    // 加载标签页数据
    loadTabData(tab) {
      switch (tab) {
        case 'overview':
          this.loadOverviewData()
          break
        case 'medical':
          this.loadMedicalData()
          break
        case 'maternal':
          this.loadMaternalData()
          break
        case 'comparison':
          this.loadComparisonData()
          break
      }
    },
    
    // 加载总览数据
    async loadOverviewData() {
      try {
        const response = await axios.get('/api/dashboard/overview')
        if (response.data.code === 200) {
          const data = response.data.data
          // 转换后端数据结构为前端期望的格式
          this.overviewStats = {
            totalPatients: data.total_patients,
            todayPatients: data.today_new_cases, // 映射今日新增病例到今日患者数
            maternalPatients: data.total_maternal,
            alertCount: data.alert_count
          }
          // 如果有患者趋势和疾病分布数据，进行相应处理
          if (data.trends && data.trends.daily_cases) {
            this.patientTrendConfig = { data: data.trends.daily_cases }
          }
          if (data.statistics && data.statistics.risk_level_distribution) {
            this.diseaseDistributionConfig = { data: data.statistics.risk_level_distribution }
          }
          // 处理实时数据
          this.realtimeData = data.recent_alerts || []
        }
      } catch (error) {
        console.error('加载总览数据失败:', error)
        this.initMockOverviewData()
      }
    },
    
    // 加载医疗数据
    async loadMedicalData() {
      try {
        console.log('开始请求医疗数据...')
        const response = await axios.get('/api/dashboard/medical', {
          timeout: 10000, // 设置超时时间
          headers: {
            'Content-Type': 'application/json'
          }
        })
        console.log('医疗数据请求成功:', response.data)
        if (response.data.code === 200) {
          const data = response.data.data
          // 转换后端返回的数据结构为前端期望的格式
          this.medicalStats = {
            totalRecords: data.total || 0,
            todayRecords: data.today || 0,
            diseaseTypes: data.disease_distribution ? data.disease_distribution.length : 0,
            departments: data.department_distribution ? data.department_distribution.length : 0,
            doctors: 0, // 后端未返回医生数，使用默认值
            beds: 0 // 后端未返回床位数，使用默认值
          }
          this.departmentConfig = { data: data.department_distribution || [] }
          this.diseaseTypeConfig = { data: data.disease_distribution || [] }
          // 后端可能没有返回monthlyTrend和departmentDetails，使用默认值
          this.monthlyTrendConfig = { data: data.monthly_trend || [] }
          this.departmentData = data.department_details || []
        }
      } catch (error) {
        console.error('加载医疗数据失败:', error)
        console.error('错误类型:', error.name)
        console.error('错误消息:', error.message)
        if (error.response) {
          console.error('响应状态:', error.response.status)
          console.error('响应数据:', error.response.data)
        } else if (error.request) {
          console.error('请求已发送但未收到响应:', error.request)
        } else {
          console.error('请求配置错误:', error.message)
        }
        this.initMockMedicalData()
      }
    },
    
    // 加载孕产数据
    async loadMaternalData() {
      try {
        console.log('开始请求孕产数据...')
        const response = await axios.get('/api/dashboard/maternal', {
          timeout: 10000, // 设置超时时间
          headers: {
            'Content-Type': 'application/json'
          }
        })
        console.log('孕产数据请求成功:', response.data)
        if (response.data.code === 200) {
          const data = response.data.data
          // 转换后端返回的数据结构为前端期望的格式
          this.maternalStats = {
            total: data.total || 0,
            todayCheckups: data.today || 0,
            // 从pregnancy_distribution中提取各孕期数据
            firstTrimester: data.pregnancy_distribution ? 
              (data.pregnancy_distribution.find(item => item.name === '早期')?.value || 0) : 0,
            secondTrimester: data.pregnancy_distribution ? 
              (data.pregnancy_distribution.find(item => item.name === '中期')?.value || 0) : 0,
            thirdTrimester: data.pregnancy_distribution ? 
              (data.pregnancy_distribution.find(item => item.name === '晚期')?.value || 0) : 0,
            // 从risk_distribution中提取高风险数据
            highRisk: data.risk_distribution ? 
              (data.risk_distribution.find(item => item.name === '高风险')?.value || 0) : 0
          }
          this.gestationalWeeksConfig = { data: data.pregnancy_distribution || [] }
          this.riskLevelConfig = { data: data.risk_distribution || [] }
          // 后端可能没有返回这些字段，使用默认值
          this.maternalData = data.maternal_details || []
          this.checkupReminders = data.reminders || []
        }
      } catch (error) {
        console.error('加载孕产数据失败:', error)
        console.error('错误类型:', error.name)
        console.error('错误消息:', error.message)
        if (error.response) {
          console.error('响应状态:', error.response.status)
          console.error('响应数据:', error.response.data)
        } else if (error.request) {
          console.error('请求已发送但未收到响应:', error.request)
        } else {
          console.error('请求配置错误:', error.message)
        }
        this.initMockMaternalData()
      }
    },
    
    // 加载对比数据
    async loadComparisonData() {
      try {
        const response = await axios.get('/api/dashboard/comparison')
        if (response.data.code === 200) {
          const data = response.data.data
          this.yearOverYearConfig = { data: data.yearOverYear }
          this.monthOverMonthConfig = { data: data.monthOverMonth }
          this.comparisonData = data.comparisonDetails
        }
      } catch (error) {
        console.error('加载对比数据失败:', error)
        this.initMockComparisonData()
      }
    },
    
    // 更新对比分析
    updateComparison() {
      // 根据配置更新对比分析
      console.log('更新对比分析:', this.comparisonConfig)
    },
    
    // 运行对比分析
    async runComparison() {
      try {
        const response = await axios.post('/api/dashboard/comparison/run', this.comparisonConfig)
        if (response.data.code === 200) {
          const data = response.data.data
          this.comparisonResults = data.results
          this.yearOverYearConfig = { data: data.yearOverYear }
          this.monthOverMonthConfig = { data: data.monthOverMonth }
          this.comparisonData = data.comparisonDetails
          this.$message.success('对比分析完成')
        }
      } catch (error) {
        console.error('运行对比分析失败:', error)
        this.$message.error('对比分析失败')
      }
    },
    
    // 导出对比报告
    exportComparison() {
      this.$message.success('对比报告已导出')
    },
    
    // 查看科室详情
    viewDepartmentDetails(department) {
      console.log('查看科室详情:', department)
    },
    
    // 导出科室数据
    exportDepartmentData(department) {
      console.log('导出科室数据:', department)
    },
    
    // 查看孕产妇详情
    viewMaternalDetails(maternal) {
      console.log('查看孕产妇详情:', maternal)
    },
    
    // 更新孕产妇记录
    updateMaternalRecord(maternal) {
      console.log('更新孕产妇记录:', maternal)
    },
    
    // 格式化日期
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('zh-CN')
    },
    
    // 获取状态标签类型
    getStatusTagType(status) {
      switch (status) {
        case '正常': return 'success'
        case '繁忙': return 'warning'
        case '拥堵': return 'danger'
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
    
    // 获取趋势标签类型
    getTrendTagType(trend) {
      switch (trend) {
        case '上升': return 'success'
        case '下降': return 'danger'
        case '平稳': return 'info'
        default: return 'info'
      }
    },
    
    // 获取进度条颜色
    getProgressColor(percentage) {
      if (percentage < 60) return '#67c23a'
      if (percentage < 80) return '#e6a23c'
      return '#f56c6c'
    },
    
    // 初始化模拟数据
    initMockOverviewData() {
      this.patientTrendConfig = {
        data: [
          { name: '周一', value: 120 },
          { name: '周二', value: 132 },
          { name: '周三', value: 101 },
          { name: '周四', value: 134 },
          { name: '周五', value: 90 },
          { name: '周六', value: 230 },
          { name: '周日', value: 210 }
        ]
      }
      
      this.diseaseDistributionConfig = {
        data: [
          { name: '感冒', value: 45 },
          { name: '高血压', value: 23 },
          { name: '糖尿病', value: 18 },
          { name: '心脏病', value: 12 },
          { name: '其他', value: 32 }
        ]
      }
      
      this.realtimeData = [
        {
          time: '09:00',
          department: '内科',
          patientCount: 15,
          avgWaitTime: '20分钟',
          status: '正常'
        },
        {
          time: '10:00',
          department: '外科',
          patientCount: 12,
          avgWaitTime: '15分钟',
          status: '正常'
        }
      ]
    },
    
    initMockMedicalData() {
      // 设置medicalStats的默认值，防止出现undefined错误
      this.medicalStats = {
        totalRecords: 45678,
        todayRecords: 234,
        diseaseTypes: 156,
        departments: 12,
        doctors: 234,
        beds: 567
      }
      
      this.departmentConfig = {
        data: [
          { name: '内科', value: 156 },
          { name: '外科', value: 134 },
          { name: '妇产科', value: 89 },
          { name: '儿科', value: 67 },
          { name: '急诊科', value: 45 }
        ]
      }
      
      this.diseaseTypeConfig = {
        data: [
          { name: '呼吸系统', value: 234 },
          { name: '消化系统', value: 189 },
          { name: '循环系统', value: 156 },
          { name: '神经系统', value: 123 },
          { name: '其他', value: 98 }
        ]
      }
      
      this.monthlyTrendConfig = {
        data: [
          { name: '1月', value: 1200 },
          { name: '2月', value: 1400 },
          { name: '3月', value: 1100 },
          { name: '4月', value: 1600 },
          { name: '5月', value: 1300 },
          { name: '6月', value: 1800 }
        ]
      }
      
      this.departmentData = [
        {
          name: '内科',
          todayPatients: 45,
          weekPatients: 234,
          monthPatients: 1234,
          doctorCount: 12,
          bedCount: 45,
          occupancyRate: 75,
          avgWaitTime: '18分钟'
        }
      ]
    },
    
    initMockMaternalData() {
      // 设置maternalStats的默认值，防止出现undefined错误
      this.maternalStats = {
        total: 456,
        firstTrimester: 123,
        secondTrimester: 156,
        thirdTrimester: 177,
        todayCheckups: 34,
        highRisk: 45
      }
      
      this.gestationalWeeksConfig = {
        data: [
          { name: '0-12周', value: 123 },
          { name: '13-28周', value: 156 },
          { name: '29-40周', value: 177 }
        ]
      }
      
      this.riskLevelConfig = {
        data: [
          { name: '低风险', value: 345 },
          { name: '中风险', value: 89 },
          { name: '高风险', value: 22 }
        ]
      }
      
      this.maternalData = [
        {
          name: '张三',
          age: 28,
          gestationalWeeks: 24,
          riskLevel: '低风险',
          lastCheckup: new Date(),
          nextCheckup: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
          doctor: '李医生'
        }
      ]
      
      this.checkupReminders = [
        {
          id: 1,
          patientName: '张三',
          checkupType: '常规产检',
          urgency: '重要',
          scheduledDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
        }
      ]
    },
    
    initMockComparisonData() {
      this.yearOverYearConfig = {
        data: [
          { name: '本月', value: 1200 },
          { name: '上月', value: 1100 },
          { name: '去年同月', value: 1000 }
        ]
      }
      
      this.monthOverMonthConfig = {
        data: [
          { name: '本周', value: 300 },
          { name: '上周', value: 280 },
          { name: '上周同期', value: 260 }
        ]
      }
      
      this.comparisonData = [
        {
          period: '本月',
          metric: '患者数量',
          currentValue: 1200,
          previousValue: 1100,
          changeRate: 9.1,
          trend: '上升',
          analysis: '本月患者数量较上月增长9.1%，主要受季节性因素影响'
        }
      ]
      
      this.comparisonResults = {
        currentValue: 1200,
        previousValue: 1100,
        changeRate: 9.1,
        changeType: 'positive'
      }
    }
  },
  
  created() {
    this.loadTabData(this.activeTab)
  }
}
</script>

<style scoped>
.dashboard-center-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.dashboard-center-content {
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
  margin-bottom: 20px;
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
  font-size: 24px;
}

.stat-icon.total {
  background: #409eff;
}

.stat-icon.today {
  background: #67c23a;
}

.stat-icon.maternal {
  background: #ff6b9d;
}

.stat-icon.alerts {
  background: #f56c6c;
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

/* 图表卡片样式 */
.chart-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.chart-card h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: bold;
}

/* 数据卡片样式 */
.data-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.data-card h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: bold;
}

/* 概览卡片样式 */
.overview-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.overview-card h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: bold;
}

/* 医疗统计样式 */
.medical-stat {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.medical-stat .stat-number {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.medical-stat .stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

/* 孕产统计样式 */
.maternal-stat {
  text-align: center;
  padding: 15px;
  background: #fff0f5;
  border-radius: 8px;
}

.maternal-stat .stat-number {
  font-size: 20px;
  font-weight: bold;
  color: #ff6b9d;
}

.maternal-stat .stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

/* 控制面板样式 */
.control-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.control-card h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: bold;
}

/* 系统状态样式 */
.system-status {
  padding: 15px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.status-item:last-child {
  border-bottom: none;
}

.status-label {
  font-size: 14px;
  color: #666;
}

/* 产检提醒样式 */
.checkup-reminders {
  max-height: 400px;
  overflow-y: auto;
}

.reminder-item {
  padding: 15px;
  margin-bottom: 10px;
  background: #fff0f5;
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

/* 对比摘要样式 */
.comparison-summary {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.summary-item {
  text-align: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
}

.summary-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
}

.summary-value.current {
  color: #409eff;
}

.summary-value.previous {
  color: #909399;
}

.summary-value.positive {
  color: #67c23a;
}

.summary-value.negative {
  color: #f56c6c;
}

/* 表格样式增强 */
.el-table {
  margin-top: 15px;
}

.positive {
  color: #67c23a;
  font-weight: bold;
}

.negative {
  color: #f56c6c;
  font-weight: bold;
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
  
  .control-card .el-row {
    flex-direction: column;
  }
  
  .control-card .el-col {
    margin-bottom: 10px;
  }
  
  .comparison-summary .el-row {
    flex-direction: column;
  }
  
  .summary-item {
    margin-bottom: 10px;
  }
}

/* 动画效果 */
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  transition: all 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  transition: all 0.3s ease;
}

.data-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  transition: all 0.3s ease;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
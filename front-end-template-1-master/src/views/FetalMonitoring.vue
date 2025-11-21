<template>
  <div class="fetal-monitoring-container">
    <dv-border-box-8 :dur="5">
      <div class="fetal-monitoring-content">
        <div class="header">
          <h2>胎心监测</h2>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-plus" @click="startMonitoring">开始监测</el-button>
            <el-button type="warning" icon="el-icon-video-camera" @click="showRealtimeMonitor">实时监测</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportReport">导出报告</el-button>
            <el-button type="info" icon="el-icon-refresh" @click="refreshData">刷新</el-button>
          </div>
        </div>

        <!-- 筛选区域 -->
        <div class="filter-section">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-input
                v-model="filters.patientName"
                placeholder="孕妇姓名"
                prefix-icon="el-icon-search"
                clearable
                @change="handleFilterChange"
              ></el-input>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.hospital" placeholder="医院" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="北京妇产医院" value="北京妇产医院"></el-option>
                <el-option label="上海第一妇婴保健院" value="上海第一妇婴保健院"></el-option>
                <el-option label="广州妇女儿童医疗中心" value="广州妇女儿童医疗中心"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-date-picker
                v-model="filters.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                @change="handleFilterChange"
                style="width: 100%"
              ></el-date-picker>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.monitoringStatus" placeholder="监测状态" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="正常" value="normal"></el-option>
                <el-option label="异常" value="abnormal"></el-option>
                <el-option label="监测中" value="monitoring"></el-option>
              </el-select>
            </el-col>
          </el-row>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-section">
          <el-row :gutter="20">
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="el-icon-user"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.totalPatients }}</h3>
                    <p>监测孕妇数</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="el-icon-time"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.totalSessions }}</h3>
                    <p>监测次数</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="el-icon-warning"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.abnormalCount }}</h3>
                    <p>异常次数</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="el-icon-video-play"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.activeMonitoring }}</h3>
                    <p>实时监测中</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 胎心监测图表 -->
        <div class="charts-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>实时胎心率曲线</h3>
                  <div ref="fetalHeartRateChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>胎心率分布统计</h3>
                  <div ref="heartRateDistributionChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>宫缩压力监测</h3>
                  <div ref="contractionChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>胎动频率分析</h3>
                  <div ref="fetalMovementChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 监测记录表格 -->
        <div class="table-section">
          <dv-border-box-10>
            <div class="table-content">
              <el-table
                :data="monitoringRecords"
                border
                stripe
                style="width: 100%"
                v-loading="loading"
                @selection-change="handleSelectionChange"
              >
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="id" label="ID" width="80"></el-table-column>
                <el-table-column prop="patient_name" label="孕妇姓名" width="120"></el-table-column>
                <el-table-column prop="gestational_week" label="孕周" width="100">
                  <template slot-scope="scope">
                    {{ scope.row.gestational_week }}周
                  </template>
                </el-table-column>
                <el-table-column prop="monitoring_date" label="监测日期" width="120">
                  <template slot-scope="scope">
                    {{ formatDate(scope.row.monitoring_date) }}
                  </template>
                </el-table-column>
                <el-table-column prop="monitoring_duration" label="监测时长" width="100">
                  <template slot-scope="scope">
                    {{ scope.row.monitoring_duration }}分钟
                  </template>
                </el-table-column>
                <el-table-column prop="baseline_heart_rate" label="基础心率" width="100">
                  <template slot-scope="scope">
                    {{ scope.row.baseline_heart_rate }}bpm
                  </template>
                </el-table-column>
                <el-table-column prop="variability" label="变异性" width="100">
                  <template slot-scope="scope">
                    {{ scope.row.variability }}bpm
                  </template>
                </el-table-column>
                <el-table-column prop="accelerations" label="加速次数" width="100"></el-table-column>
                <el-table-column prop="decelerations" label="减速次数" width="100"></el-table-column>
                <el-table-column prop="monitoring_status" label="监测状态" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getStatusTagType(scope.row.monitoring_status)">
                      {{ getStatusText(scope.row.monitoring_status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="viewDetails(scope.row)">查看</el-button>
                    <el-button size="mini" type="primary" @click="viewChart(scope.row)">图表</el-button>
                    <el-button size="mini" type="success" @click="generateReport(scope.row)">报告</el-button>
                  </template>
                </el-table-column>
              </el-table>
              
              <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="pagination.currentPage"
                :page-sizes="[10, 20, 50, 100]"
                :page-size="pagination.pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="pagination.total"
                style="margin-top: 20px; text-align: center"
              ></el-pagination>
            </div>
          </dv-border-box-10>
        </div>

        <!-- 批量操作 -->
        <div class="batch-actions" v-if="selectedRecords.length > 0">
          <el-button type="success" @click="batchExport">批量导出</el-button>
          <el-button type="warning" @click="batchGenerateReports">批量生成报告</el-button>
          <span class="selected-info">已选择 {{ selectedRecords.length }} 条记录</span>
        </div>

        <!-- 新增监测对话框 -->
        <el-dialog
          title="开始胎心监测"
          :visible.sync="monitoringDialogVisible"
          width="600px"
        >
          <el-form
            ref="monitoringForm"
            :model="monitoringForm"
            :rules="monitoringRules"
            label-width="120px"
          >
            <el-form-item label="孕妇姓名" prop="patient_name">
              <el-input v-model="monitoringForm.patient_name" placeholder="请输入孕妇姓名"></el-input>
            </el-form-item>
            
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="monitoringForm.age" :min="15" :max="50" style="width: 100%"></el-input-number>
            </el-form-item>
            
            <el-form-item label="孕周" prop="gestational_week">
              <el-input-number v-model="monitoringForm.gestational_week" :min="20" :max="42" style="width: 100%"></el-input-number>
            </el-form-item>
            
            <el-form-item label="医院" prop="hospital">
              <el-select v-model="monitoringForm.hospital" placeholder="选择医院" style="width: 100%">
                <el-option label="北京妇产医院" value="北京妇产医院"></el-option>
                <el-option label="上海第一妇婴保健院" value="上海第一妇婴保健院"></el-option>
                <el-option label="广州妇女儿童医疗中心" value="广州妇女儿童医疗中心"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="医生" prop="doctor">
              <el-input v-model="monitoringForm.doctor" placeholder="请输入医生姓名"></el-input>
            </el-form-item>
            
            <el-form-item label="监测时长" prop="monitoring_duration">
              <el-select v-model="monitoringForm.monitoring_duration" placeholder="选择监测时长" style="width: 100%">
                <el-option label="10分钟" :value="10"></el-option>
                <el-option label="20分钟" :value="20"></el-option>
                <el-option label="30分钟" :value="30"></el-option>
                <el-option label="40分钟" :value="40"></el-option>
                <el-option label="60分钟" :value="60"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="备注" prop="notes">
              <el-input
                v-model="monitoringForm.notes"
                type="textarea"
                :rows="3"
                placeholder="请输入备注信息"
              ></el-input>
            </el-form-item>
          </el-form>
          
          <div slot="footer" class="dialog-footer">
            <el-button @click="monitoringDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="startMonitoringSession" :loading="starting">开始监测</el-button>
          </div>
        </el-dialog>

        <!-- 实时监测对话框 -->
        <el-dialog
          title="实时胎心监测"
          :visible.sync="realtimeDialogVisible"
          width="1200px"
          :before-close="closeRealtimeMonitoring"
        >
          <div class="realtime-monitoring">
            <div class="monitoring-info">
              <el-row :gutter="20">
                <el-col :span="6">
                  <div class="info-item">
                    <label>孕妇姓名：</label>
                    <span>{{ realtimeData.patient_name }}</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="info-item">
                    <label>孕周：</label>
                    <span>{{ realtimeData.gestational_week }}周</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="info-item">
                    <label>当前心率：</label>
                    <span class="heart-rate">{{ realtimeData.current_heart_rate }}bpm</span>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="info-item">
                    <label>监测时长：</label>
                    <span>{{ realtimeData.elapsed_time }}分钟</span>
                  </div>
                </el-col>
              </el-row>
            </div>
            
            <div class="realtime-chart">
              <div ref="realtimeChart" class="chart"></div>
            </div>
            
            <div class="monitoring-controls">
              <el-button type="danger" @click="stopMonitoring">停止监测</el-button>
              <el-button type="warning" @click="pauseMonitoring" :disabled="!isMonitoring">
                {{ isPaused ? '继续监测' : '暂停监测' }}
              </el-button>
              <el-button type="success" @click="saveSnapshot">保存快照</el-button>
            </div>
          </div>
        </el-dialog>

        <!-- 详情对话框 -->
        <el-dialog
          title="监测记录详情"
          :visible.sync="detailDialogVisible"
          width="900px"
        >
          <div class="detail-content" v-if="currentRecord">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>孕妇姓名：</label>
                  <span>{{ currentRecord.patient_name }}</span>
                </div>
                <div class="detail-item">
                  <label>孕周：</label>
                  <span>{{ currentRecord.gestational_week }}周</span>
                </div>
                <div class="detail-item">
                  <label>监测日期：</label>
                  <span>{{ formatDate(currentRecord.monitoring_date) }}</span>
                </div>
                <div class="detail-item">
                  <label>监测时长：</label>
                  <span>{{ currentRecord.monitoring_duration }}分钟</span>
                </div>
                <div class="detail-item">
                  <label>基础心率：</label>
                  <span>{{ currentRecord.baseline_heart_rate }}bpm</span>
                </div>
                <div class="detail-item">
                  <label>变异性：</label>
                  <span>{{ currentRecord.variability }}bpm</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>加速次数：</label>
                  <span>{{ currentRecord.accelerations }}次</span>
                </div>
                <div class="detail-item">
                  <label>减速次数：</label>
                  <span>{{ currentRecord.decelerations }}次</span>
                </div>
                <div class="detail-item">
                  <label>宫缩次数：</label>
                  <span>{{ currentRecord.contractions }}次</span>
                </div>
                <div class="detail-item">
                  <label>胎动次数：</label>
                  <span>{{ currentRecord.fetal_movements }}次</span>
                </div>
                <div class="detail-item">
                  <label>监测状态：</label>
                  <el-tag :type="getStatusTagType(currentRecord.monitoring_status)">
                    {{ getStatusText(currentRecord.monitoring_status) }}
                  </el-tag>
                </div>
                <div class="detail-item">
                  <label>评估结果：</label>
                  <span>{{ currentRecord.assessment_result }}</span>
                </div>
              </el-col>
            </el-row>
            
            <div class="detail-section">
              <h4>监测分析</h4>
              <p>{{ currentRecord.analysis_result || '暂无分析结果' }}</p>
            </div>
            
            <div class="detail-section">
              <h4>医嘱建议</h4>
              <p>{{ currentRecord.medical_advice || '暂无医嘱建议' }}</p>
            </div>
          </div>
        </el-dialog>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'FetalMonitoring',
  data() {
    return {
      loading: false,
      starting: false,
      monitoringDialogVisible: false,
      realtimeDialogVisible: false,
      detailDialogVisible: false,
      isMonitoring: false,
      isPaused: false,
      
      // 筛选条件
      filters: {
        patientName: '',
        hospital: '',
        dateRange: [],
        monitoringStatus: ''
      },
      
      // 统计数据
      stats: {
        totalPatients: 0,
        totalSessions: 0,
        abnormalCount: 0,
        activeMonitoring: 0
      },
      
      // 监测记录
      monitoringRecords: [],
      selectedRecords: [],
      
      // 分页
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      
      // 监测表单
      monitoringForm: {
        patient_name: '',
        age: 25,
        gestational_week: 30,
        hospital: '',
        doctor: '',
        monitoring_duration: 20,
        notes: ''
      },
      
      // 表单验证规则
      monitoringRules: {
        patient_name: [
          { required: true, message: '请输入孕妇姓名', trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        gestational_week: [
          { required: true, message: '请输入孕周', trigger: 'blur' }
        ],
        hospital: [
          { required: true, message: '请选择医院', trigger: 'change' }
        ],
        doctor: [
          { required: true, message: '请输入医生姓名', trigger: 'blur' }
        ],
        monitoring_duration: [
          { required: true, message: '请选择监测时长', trigger: 'change' }
        ]
      },
      
      // 实时监测数据
      realtimeData: {
        patient_name: '',
        gestational_week: 0,
        current_heart_rate: 140,
        elapsed_time: 0
      },
      
      // 当前记录
      currentRecord: null,
      
      // 图表实例
      charts: {
        fetalHeartRate: null,
        heartRateDistribution: null,
        contraction: null,
        fetalMovement: null,
        realtime: null
      },
      
      // 定时器
      realtimeTimer: null,
      dataUpdateTimer: null
    }
  },
  
  mounted() {
    this.loadMonitoringRecords()
    this.loadStatistics()
    this.initCharts()
  },
  
  beforeDestroy() {
    this.destroyCharts()
    this.clearTimers()
  },
  
  methods: {
    loadMonitoringRecords() {
      this.loading = true
      
      const params = {
        page: this.pagination.currentPage,
        page_size: this.pagination.pageSize,
        patient_name: this.filters.patientName,
        hospital: this.filters.hospital,
        start_date: this.filters.dateRange?.[0],
        end_date: this.filters.dateRange?.[1],
        monitoring_status: this.filters.monitoringStatus
      }
      
      this.$http.get('/api/fetal-monitoring/records', { params })
        .then(response => {
          const data = response.data.data
          this.monitoringRecords = data.records || []
          this.pagination.total = data.total || 0
        })
        .catch(error => {
          this.$message.error('加载监测记录失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    loadStatistics() {
      this.$http.get('/api/fetal-monitoring/statistics')
        .then(response => {
          const data = response.data.data
          this.stats = {
            totalPatients: data.total_patients || 0,
            totalSessions: data.total_sessions || 0,
            abnormalCount: data.abnormal_count || 0,
            activeMonitoring: data.active_monitoring || 0
          }
        })
        .catch(error => {
          this.$message.error('加载统计数据失败：' + error.message)
        })
    },
    
    initCharts() {
      this.$nextTick(() => {
        this.initFetalHeartRateChart()
        this.initHeartRateDistributionChart()
        this.initContractionChart()
        this.initFetalMovementChart()
      })
    },
    
    initFetalHeartRateChart() {
      const chart = echarts.init(this.$refs.fetalHeartRateChart)
      const option = {
        title: {
          text: '实时胎心率',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: Array.from({length: 60}, (_, i) => `${i}秒`)
        },
        yAxis: {
          type: 'value',
          name: '心率(bpm)',
          min: 100,
          max: 180
        },
        series: [{
          data: Array.from({length: 60}, () => 130 + Math.random() * 20),
          type: 'line',
          smooth: true,
          lineStyle: {
            color: '#409EFF',
            width: 2
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
            ])
          }
        }]
      }
      chart.setOption(option)
      this.charts.fetalHeartRate = chart
    },
    
    initHeartRateDistributionChart() {
      const chart = echarts.init(this.$refs.heartRateDistributionChart)
      const option = {
        title: {
          text: '胎心率分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        series: [{
          name: '胎心率',
          type: 'pie',
          radius: '60%',
          data: [
            { value: 35, name: '120-130 bpm' },
            { value: 40, name: '130-140 bpm' },
            { value: 20, name: '140-150 bpm' },
            { value: 5, name: '>150 bpm' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      }
      chart.setOption(option)
      this.charts.heartRateDistribution = chart
    },
    
    initContractionChart() {
      const chart = echarts.init(this.$refs.contractionChart)
      const option = {
        title: {
          text: '宫缩压力监测',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: Array.from({length: 30}, (_, i) => `${i}分钟`)
        },
        yAxis: {
          type: 'value',
          name: '压力(mmHg)'
        },
        series: [{
          data: Array.from({length: 30}, () => Math.random() * 50),
          type: 'line',
          smooth: true,
          lineStyle: {
            color: '#E6A23C',
            width: 2
          }
        }]
      }
      chart.setOption(option)
      this.charts.contraction = chart
    },
    
    initFetalMovementChart() {
      const chart = echarts.init(this.$refs.fetalMovementChart)
      const option = {
        title: {
          text: '胎动频率分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['0-2时', '2-4时', '4-6时', '6-8时', '8-10时', '10-12时', '12-14时', '14-16时', '16-18时', '18-20时', '20-22时', '22-24时']
        },
        yAxis: {
          type: 'value',
          name: '胎动次数'
        },
        series: [{
          data: [2, 1, 3, 5, 8, 12, 15, 18, 14, 10, 6, 3],
          type: 'bar',
          itemStyle: {
            color: '#67C23A'
          }
        }]
      }
      chart.setOption(option)
      this.charts.fetalMovement = chart
    },
    
    startMonitoring() {
      this.monitoringDialogVisible = true
    },
    
    startMonitoringSession() {
      this.$refs.monitoringForm.validate(valid => {
        if (!valid) return
        
        this.starting = true
        
        this.$http.post('/api/fetal-monitoring/start', this.monitoringForm)
          .then(response => {
            this.$message.success('监测已开始')
            this.monitoringDialogVisible = false
            this.showRealtimeMonitorWithData(response.data.data)
            this.loadMonitoringRecords()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('开始监测失败：' + error.message)
          })
          .finally(() => {
            this.starting = false
          })
      })
    },
    
    showRealtimeMonitor() {
      this.realtimeDialogVisible = true
      this.$nextTick(() => {
        this.initRealtimeChart()
      })
    },
    
    showRealtimeMonitorWithData(data) {
      this.realtimeData = {
        patient_name: data.patient_name,
        gestational_week: data.gestational_week,
        current_heart_rate: 140,
        elapsed_time: 0
      }
      this.showRealtimeMonitor()
      this.startRealtimeMonitoring()
    },
    
    initRealtimeChart() {
      if (this.charts.realtime) {
        this.charts.realtime.dispose()
      }
      
      const chart = echarts.init(this.$refs.realtimeChart)
      const option = {
        title: {
          text: '实时胎心率监测',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: []
        },
        yAxis: {
          type: 'value',
          name: '心率(bpm)',
          min: 100,
          max: 180
        },
        series: [{
          data: [],
          type: 'line',
          smooth: true,
          lineStyle: {
            color: '#FF6B6B',
            width: 3
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(255, 107, 107, 0.3)' },
              { offset: 1, color: 'rgba(255, 107, 107, 0.1)' }
            ])
          }
        }]
      }
      chart.setOption(option)
      this.charts.realtime = chart
    },
    
    startRealtimeMonitoring() {
      this.isMonitoring = true
      this.isPaused = false
      let timeCounter = 0
      
      this.realtimeTimer = setInterval(() => {
        if (!this.isPaused) {
          timeCounter++
          this.realtimeData.elapsed_time = Math.floor(timeCounter / 6)
          
          // 模拟心率数据
          const heartRate = 130 + Math.random() * 20 + Math.sin(timeCounter / 10) * 5
          this.realtimeData.current_heart_rate = Math.round(heartRate)
          
          // 更新图表
          if (this.charts.realtime) {
            const option = this.charts.realtime.getOption()
            option.xAxis[0].data.push(`${timeCounter}秒`)
            option.series[0].data.push(this.realtimeData.current_heart_rate)
            
            // 保持最近60个数据点
            if (option.xAxis[0].data.length > 60) {
              option.xAxis[0].data.shift()
              option.series[0].data.shift()
            }
            
            this.charts.realtime.setOption(option)
          }
        }
      }, 1000)
    },
    
    stopMonitoring() {
      this.isMonitoring = false
      this.isPaused = false
      this.clearTimers()
      this.realtimeDialogVisible = false
      this.$message.success('监测已停止')
      this.loadMonitoringRecords()
    },
    
    pauseMonitoring() {
      this.isPaused = !this.isPaused
      this.$message.info(this.isPaused ? '监测已暂停' : '监测已继续')
    },
    
    saveSnapshot() {
      this.$message.success('快照已保存')
    },
    
    viewDetails(record) {
      this.currentRecord = record
      this.detailDialogVisible = true
    },
    
    viewChart(record) {
      // 查看详细图表
      this.$message.info('查看图表功能开发中')
    },
    
    generateReport(record) {
      this.$http.post(`/api/fetal-monitoring/report/${record.id}`, {}, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `胎心监测报告_${record.patient_name}_${new Date().toLocaleDateString()}.pdf`
          link.click()
        })
        .catch(error => {
          this.$message.error('生成报告失败：' + error.message)
        })
    },
    
    batchExport() {
      if (this.selectedRecords.length === 0) {
        this.$message.warning('请选择要导出的记录')
        return
      }
      
      const ids = this.selectedRecords.map(record => record.id)
      this.$http.post('/api/fetal-monitoring/export', { ids }, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `胎心监测记录_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    batchGenerateReports() {
      if (this.selectedRecords.length === 0) {
        this.$message.warning('请选择要生成报告的记录')
        return
      }
      
      this.$message.info('批量生成报告功能开发中')
    },
    
    exportReport() {
      this.$http.post('/api/fetal-monitoring/export', {}, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `胎心监测报告_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    handleFilterChange() {
      this.pagination.currentPage = 1
      this.loadMonitoringRecords()
    },
    
    handleSelectionChange(selection) {
      this.selectedRecords = selection
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadMonitoringRecords()
    },
    
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadMonitoringRecords()
    },
    
    closeRealtimeMonitoring() {
      if (this.isMonitoring) {
        this.$confirm('监测正在进行中，确定要关闭吗？', '确认关闭', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.stopMonitoring()
        })
      } else {
        this.realtimeDialogVisible = false
      }
    },
    
    refreshData() {
      this.loadMonitoringRecords()
      this.loadStatistics()
      this.$message.success('数据已刷新')
    },
    
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },
    
    getStatusTagType(status) {
      const types = {
        'normal': 'success',
        'abnormal': 'danger',
        'monitoring': 'warning'
      }
      return types[status] || ''
    },
    
    getStatusText(status) {
      const texts = {
        'normal': '正常',
        'abnormal': '异常',
        'monitoring': '监测中'
      }
      return texts[status] || status
    },
    
    destroyCharts() {
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.dispose()
        }
      })
    },
    
    clearTimers() {
      if (this.realtimeTimer) {
        clearInterval(this.realtimeTimer)
        this.realtimeTimer = null
      }
      if (this.dataUpdateTimer) {
        clearInterval(this.dataUpdateTimer)
        this.dataUpdateTimer = null
      }
    }
  }
}
</script>

<style lang="less" scoped>
.fetal-monitoring-container {
  padding: 20px;
  height: 100%;
  
  .fetal-monitoring-content {
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
    
    .stats-section {
      margin-bottom: 20px;
      
      .stat-card {
        display: flex;
        align-items: center;
        padding: 20px;
        
        .stat-icon {
          font-size: 32px;
          color: #409EFF;
          margin-right: 15px;
        }
        
        .stat-content {
          h3 {
            margin: 0;
            font-size: 28px;
            color: #333;
            font-weight: bold;
          }
          
          p {
            margin: 5px 0 0 0;
            color: #666;
            font-size: 14px;
          }
        }
      }
    }
    
    .charts-section {
      margin-bottom: 20px;
      
      .chart-container {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 15px;
          text-align: center;
        }
        
        .chart {
          height: 300px;
        }
      }
    }
    
    .table-section {
      margin-bottom: 20px;
      
      .table-content {
        padding: 20px;
      }
    }
    
    .batch-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 20px;
      padding: 15px;
      background: rgba(255, 193, 7, 0.1);
      border: 1px solid rgba(255, 193, 7, 0.3);
      border-radius: 8px;
      
      .selected-info {
        color: #856404;
        font-weight: bold;
        margin-left: auto;
      }
    }
    
    .realtime-monitoring {
      .monitoring-info {
        margin-bottom: 20px;
        padding: 15px;
        background: rgba(64, 158, 255, 0.05);
        border-radius: 8px;
        
        .info-item {
          display: flex;
          margin-bottom: 10px;
          
          label {
            font-weight: bold;
            color: #666;
            width: 80px;
          }
          
          span {
            color: #333;
            
            &.heart-rate {
              color: #FF6B6B;
              font-weight: bold;
              font-size: 18px;
            }
          }
        }
      }
      
      .realtime-chart {
        margin-bottom: 20px;
        
        .chart {
          height: 400px;
        }
      }
      
      .monitoring-controls {
        text-align: center;
        
        .el-button {
          margin: 0 10px;
        }
      }
    }
    
    .detail-content {
      .detail-item {
        display: flex;
        margin-bottom: 10px;
        
        label {
          font-weight: bold;
          color: #666;
          width: 100px;
        }
        
        span {
          color: #333;
        }
      }
      
      .detail-section {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        
        h4 {
          color: #409EFF;
          margin-bottom: 10px;
        }
        
        p {
          color: #666;
          line-height: 1.6;
        }
      }
    }
  }
}
</style>
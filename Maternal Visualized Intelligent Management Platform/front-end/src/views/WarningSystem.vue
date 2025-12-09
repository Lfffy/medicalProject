<template>
  <div class="warning-system-container">
    <dv-border-box-8 :dur="5">
      <div class="warning-system-content">
        <div class="header">
          <h2>预警系统</h2>
          <div class="header-actions">
            <el-button type="danger" icon="el-icon-warning" @click="createWarning">创建预警</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportWarnings">导出预警</el-button>
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
              <el-select v-model="filters.warningLevel" placeholder="预警级别" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="紧急" value="critical"></el-option>
                <el-option label="高危" value="high"></el-option>
                <el-option label="中危" value="medium"></el-option>
                <el-option label="低危" value="low"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.warningType" placeholder="预警类型" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="生命体征异常" value="vital_signs"></el-option>
                <el-option label="实验室检查异常" value="lab_results"></el-option>
                <el-option label="胎儿监测异常" value="fetal_monitoring"></el-option>
                <el-option label="并发症风险" value="complications"></el-option>
                <el-option label="营养风险" value="nutrition"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.status" placeholder="处理状态" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="待处理" value="pending"></el-option>
                <el-option label="处理中" value="processing"></el-option>
                <el-option label="已处理" value="resolved"></el-option>
                <el-option label="已忽略" value="ignored"></el-option>
              </el-select>
            </el-col>
          </el-row>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-section">
          <el-row :gutter="20">
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card critical">
                  <div class="stat-icon">
                    <i class="el-icon-warning-outline"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.criticalCount }}</h3>
                    <p>紧急预警</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card high">
                  <div class="stat-icon">
                    <i class="el-icon-warning"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.highCount }}</h3>
                    <p>高危预警</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card medium">
                  <div class="stat-icon">
                    <i class="el-icon-info"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.pendingCount }}</h3>
                    <p>待处理预警</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card resolved">
                  <div class="stat-icon">
                    <i class="el-icon-check"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.resolvedCount }}</h3>
                    <p>已处理预警</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 预警趋势图表 -->
        <div class="charts-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>预警趋势分析</h3>
                  <div ref="trendChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>预警类型分布</h3>
                  <div ref="typeChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>预警级别分布</h3>
                  <div ref="levelChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>处理时效分析</h3>
                  <div ref="responseChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 实时预警列表 -->
        <div class="realtime-section">
          <dv-border-box-10>
            <div class="realtime-content">
              <h3>实时预警</h3>
              <div class="realtime-warnings" v-loading="realtimeLoading">
                <div 
                  v-for="warning in realtimeWarnings" 
                  :key="warning.id"
                  class="realtime-warning-item"
                  :class="warning.warning_level"
                >
                  <div class="warning-header">
                    <div class="warning-level">
                      <el-tag :type="getLevelTagType(warning.warning_level)">
                        {{ getLevelText(warning.warning_level) }}
                      </el-tag>
                    </div>
                    <div class="warning-time">{{ formatTime(warning.created_time) }}</div>
                  </div>
                  <div class="warning-content">
                    <div class="patient-info">
                      <strong>{{ warning.patient_name }}</strong> 
                      ({{ warning.gestational_week }}周)
                    </div>
                    <div class="warning-message">{{ warning.warning_message }}</div>
                  </div>
                  <div class="warning-actions">
                    <el-button size="mini" @click="handleWarning(warning)">处理</el-button>
                    <el-button size="mini" @click="viewWarningDetail(warning)">详情</el-button>
                  </div>
                </div>
              </div>
            </div>
          </dv-border-box-10>
        </div>

        <!-- 预警记录表格 -->
        <div class="table-section">
          <dv-border-box-10>
            <div class="table-content">
              <el-table
                :data="warningRecords"
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
                <el-table-column prop="warning_level" label="预警级别" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getLevelTagType(scope.row.warning_level)">
                      {{ getLevelText(scope.row.warning_level) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="warning_type" label="预警类型" width="120">
                  <template slot-scope="scope">
                    <el-tag :type="getTypeTagType(scope.row.warning_type)">
                      {{ getTypeText(scope.row.warning_type) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="warning_message" label="预警信息" width="250" show-overflow-tooltip></el-table-column>
                <el-table-column prop="threshold_value" label="阈值" width="100"></el-table-column>
                <el-table-column prop="actual_value" label="实际值" width="100"></el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getStatusTagType(scope.row.status)">
                      {{ getStatusText(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="created_time" label="创建时间" width="150">
                  <template slot-scope="scope">
                    {{ formatTime(scope.row.created_time) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="viewWarningDetail(scope.row)">查看</el-button>
                    <el-button size="mini" @click="handleWarning(scope.row)">处理</el-button>
                    <el-button size="mini" type="danger" @click="deleteWarning(scope.row)">删除</el-button>
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
        <div class="batch-actions" v-if="selectedWarnings.length > 0">
          <el-button type="success" @click="batchExport">批量导出</el-button>
          <el-button type="warning" @click="batchUpdateStatus">批量更新状态</el-button>
          <span class="selected-info">已选择 {{ selectedWarnings.length }} 条预警</span>
        </div>

        <!-- 创建/编辑预警对话框 -->
        <el-dialog
          :title="dialogTitle"
          :visible.sync="warningDialogVisible"
          width="800px"
          :before-close="handleDialogClose"
        >
          <el-form
            ref="warningForm"
            :model="warningForm"
            :rules="warningRules"
            label-width="120px"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="孕妇姓名" prop="patient_name">
                  <el-input v-model="warningForm.patient_name" placeholder="请输入孕妇姓名"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="孕周" prop="gestational_week">
                  <el-input-number v-model="warningForm.gestational_week" :min="1" :max="42" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="预警级别" prop="warning_level">
                  <el-select v-model="warningForm.warning_level" placeholder="选择预警级别" style="width: 100%">
                    <el-option label="紧急" value="critical"></el-option>
                    <el-option label="高危" value="high"></el-option>
                    <el-option label="中危" value="medium"></el-option>
                    <el-option label="低危" value="low"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="预警类型" prop="warning_type">
                  <el-select v-model="warningForm.warning_type" placeholder="选择预警类型" style="width: 100%">
                    <el-option label="生命体征异常" value="vital_signs"></el-option>
                    <el-option label="实验室检查异常" value="lab_results"></el-option>
                    <el-option label="胎儿监测异常" value="fetal_monitoring"></el-option>
                    <el-option label="并发症风险" value="complications"></el-option>
                    <el-option label="营养风险" value="nutrition"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="预警信息" prop="warning_message">
              <el-input v-model="warningForm.warning_message" placeholder="请输入预警信息"></el-input>
            </el-form-item>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="阈值" prop="threshold_value">
                  <el-input v-model="warningForm.threshold_value" placeholder="请输入阈值"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="实际值" prop="actual_value">
                  <el-input v-model="warningForm.actual_value" placeholder="请输入实际值"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="详细描述" prop="description">
              <el-input
                v-model="warningForm.description"
                type="textarea"
                :rows="4"
                placeholder="请详细描述预警情况"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="处理建议" prop="handling_suggestion">
              <el-input
                v-model="warningForm.handling_suggestion"
                type="textarea"
                :rows="3"
                placeholder="请输入处理建议"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="状态" prop="status">
              <el-select v-model="warningForm.status" placeholder="选择状态" style="width: 100%">
                <el-option label="待处理" value="pending"></el-option>
                <el-option label="处理中" value="processing"></el-option>
                <el-option label="已处理" value="resolved"></el-option>
                <el-option label="已忽略" value="ignored"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          
          <div slot="footer" class="dialog-footer">
            <el-button @click="warningDialogVisible = false">取消</el-button>
            <el-button @click="saveWarning" :loading="saving">保存</el-button>
          </div>
        </el-dialog>

        <!-- 预警详情对话框 -->
        <el-dialog
          title="预警详情"
          :visible.sync="detailDialogVisible"
          width="900px"
        >
          <div class="detail-content" v-if="currentWarning">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>孕妇姓名：</label>
                  <span>{{ currentWarning.patient_name }}</span>
                </div>
                <div class="detail-item">
                  <label>孕周：</label>
                  <span>{{ currentWarning.gestational_week }}周</span>
                </div>
                <div class="detail-item">
                  <label>预警级别：</label>
                  <el-tag :type="getLevelTagType(currentWarning.warning_level)">
                    {{ getLevelText(currentWarning.warning_level) }}
                  </el-tag>
                </div>
                <div class="detail-item">
                  <label>预警类型：</label>
                  <el-tag :type="getTypeTagType(currentWarning.warning_type)">
                    {{ getTypeText(currentWarning.warning_type) }}
                  </el-tag>
                </div>
                <div class="detail-item">
                  <label>阈值：</label>
                  <span>{{ currentWarning.threshold_value }}</span>
                </div>
                <div class="detail-item">
                  <label>实际值：</label>
                  <span>{{ currentWarning.actual_value }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>状态：</label>
                  <el-tag :type="getStatusTagType(currentWarning.status)">
                    {{ getStatusText(currentWarning.status) }}
                  </el-tag>
                </div>
                <div class="detail-item">
                  <label>创建时间：</label>
                  <span>{{ formatTime(currentWarning.created_time) }}</span>
                </div>
                <div class="detail-item">
                  <label>处理时间：</label>
                  <span>{{ formatTime(currentWarning.handled_time) }}</span>
                </div>
                <div class="detail-item">
                  <label>处理人：</label>
                  <span>{{ currentWarning.handler || '未处理' }}</span>
                </div>
                <div class="detail-item">
                  <label>创建人：</label>
                  <span>{{ currentWarning.created_by }}</span>
                </div>
                <div class="detail-item">
                  <label>预警信息：</label>
                  <span>{{ currentWarning.warning_message }}</span>
                </div>
              </el-col>
            </el-row>
            
            <div class="detail-section">
              <h4>详细描述</h4>
              <p>{{ currentWarning.description }}</p>
            </div>
            
            <div class="detail-section">
              <h4>处理建议</h4>
              <p>{{ currentWarning.handling_suggestion }}</p>
            </div>
            
            <div class="detail-section" v-if="currentWarning.handling_result">
              <h4>处理结果</h4>
              <p>{{ currentWarning.handling_result }}</p>
            </div>
          </div>
        </el-dialog>

        <!-- 处理预警对话框 -->
        <el-dialog
          title="处理预警"
          :visible.sync="handleDialogVisible"
          width="600px"
        >
          <el-form
            ref="handleForm"
            :model="handleForm"
            :rules="handleRules"
            label-width="100px"
          >
            <el-form-item label="处理状态" prop="status">
              <el-select v-model="handleForm.status" placeholder="选择处理状态" style="width: 100%">
                <el-option label="处理中" value="processing"></el-option>
                <el-option label="已处理" value="resolved"></el-option>
                <el-option label="已忽略" value="ignored"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="处理结果" prop="handling_result">
              <el-input
                v-model="handleForm.handling_result"
                type="textarea"
                :rows="4"
                placeholder="请描述处理结果"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="备注" prop="remarks">
              <el-input
                v-model="handleForm.remarks"
                type="textarea"
                :rows="3"
                placeholder="请输入备注信息"
              ></el-input>
            </el-form-item>
          </el-form>
          
          <div slot="footer" class="dialog-footer">
            <el-button @click="handleDialogVisible = false">取消</el-button>
            <el-button @click="submitHandle" :loading="handling">提交</el-button>
          </div>
        </el-dialog>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'WarningSystem',
  data() {
    return {
      loading: false,
      realtimeLoading: false,
      saving: false,
      handling: false,
      warningDialogVisible: false,
      detailDialogVisible: false,
      handleDialogVisible: false,
      isEdit: false,
      
      // 筛选条件
      filters: {
        patientName: '',
        warningLevel: '',
        warningType: '',
        status: ''
      },
      
      // 统计数据
      stats: {
        criticalCount: 0,
        highCount: 0,
        pendingCount: 0,
        resolvedCount: 0
      },
      
      // 实时预警
      realtimeWarnings: [],
      
      // 预警记录
      warningRecords: [],
      selectedWarnings: [],
      
      // 分页
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      
      // 预警表单
      warningForm: {
        patient_name: '',
        gestational_week: 20,
        warning_level: 'medium',
        warning_type: 'vital_signs',
        warning_message: '',
        threshold_value: '',
        actual_value: '',
        description: '',
        handling_suggestion: '',
        status: 'pending'
      },
      
      // 表单验证规则
      warningRules: {
        patient_name: [
          { required: true, message: '请输入孕妇姓名', trigger: 'blur' }
        ],
        gestational_week: [
          { required: true, message: '请输入孕周', trigger: 'blur' }
        ],
        warning_level: [
          { required: true, message: '请选择预警级别', trigger: 'change' }
        ],
        warning_type: [
          { required: true, message: '请选择预警类型', trigger: 'change' }
        ],
        warning_message: [
          { required: true, message: '请输入预警信息', trigger: 'blur' }
        ]
      },
      
      // 处理表单
      handleForm: {
        status: 'processing',
        handling_result: '',
        remarks: ''
      },
      
      handleRules: {
        status: [
          { required: true, message: '请选择处理状态', trigger: 'change' }
        ],
        handling_result: [
          { required: true, message: '请输入处理结果', trigger: 'blur' }
        ]
      },
      
      // 当前预警
      currentWarning: null,
      
      // 图表实例
      charts: {
        trend: null,
        type: null,
        level: null,
        response: null
      }
    }
  },
  
  computed: {
    dialogTitle() {
      return this.isEdit ? '编辑预警' : '创建预警'
    }
  },
  
  mounted() {
    this.loadWarningRecords()
    this.loadRealtimeWarnings()
    this.loadStatistics()
    this.initCharts()
    
    // 启动实时更新
    this.startRealtimeUpdate()
  },
  
  beforeDestroy() {
    this.destroyCharts()
    this.stopRealtimeUpdate()
  },
  
  methods: {
    loadWarningRecords() {
      this.loading = true
      
      const params = {
        page: this.pagination.currentPage,
        page_size: this.pagination.pageSize,
        patient_name: this.filters.patientName,
        warning_level: this.filters.warningLevel,
        warning_type: this.filters.warningType,
        status: this.filters.status
      }
      
      this.$http.get('/warning/records', { params })
        .then(response => {
          const data = response.data.data
          this.warningRecords = data.warnings || []
          this.pagination.total = data.total || 0
        })
        .catch(error => {
          this.$message.error('加载预警记录失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    loadRealtimeWarnings() {
      this.realtimeLoading = true
      
      this.$http.get('/warning/realtime')
        .then(response => {
          this.realtimeWarnings = response.data.data.warnings || []
        })
        .catch(error => {
          this.$message.error('加载实时预警失败：' + error.message)
        })
        .finally(() => {
          this.realtimeLoading = false
        })
    },
    
    loadStatistics() {
      this.$http.get('/warning/statistics')
        .then(response => {
          const data = response.data.data
          this.stats = {
            criticalCount: data.critical_count || 0,
            highCount: data.high_count || 0,
            pendingCount: data.pending_count || 0,
            resolvedCount: data.resolved_count || 0
          }
        })
        .catch(error => {
          this.$message.error('加载统计数据失败：' + error.message)
        })
    },
    
    initCharts() {
      this.$nextTick(() => {
        this.initTrendChart()
        this.initTypeChart()
        this.initLevelChart()
        this.initResponseChart()
      })
    },
    
    initTrendChart() {
      const chart = echarts.init(this.$refs.trendChart)
      const option = {
        title: {
          text: '预警趋势分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['紧急', '高危', '中危', '低危'],
          top: 30
        },
        xAxis: {
          type: 'category',
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value',
          name: '预警数量'
        },
        series: [
          {
            name: '紧急',
            type: 'line',
            data: [2, 1, 3, 2, 1, 2, 1],
            lineStyle: { color: '#F56C6C' }
          },
          {
            name: '高危',
            type: 'line',
            data: [5, 6, 4, 7, 5, 6, 4],
            lineStyle: { color: '#E6A23C' }
          },
          {
            name: '中危',
            type: 'line',
            data: [8, 9, 7, 10, 8, 9, 7],
            lineStyle: { color: '#ff69b4' }
          },
          {
            name: '低危',
            type: 'line',
            data: [12, 14, 11, 13, 12, 14, 11],
            lineStyle: { color: '#67C23A' }
          }
        ]
      }
      chart.setOption(option)
      this.charts.trend = chart
    },
    
    initTypeChart() {
      const chart = echarts.init(this.$refs.typeChart)
      const option = {
        title: {
          text: '预警类型分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        series: [{
          name: '预警类型',
          type: 'pie',
          radius: '60%',
          data: [
            { value: 35, name: '生命体征异常' },
            { value: 25, name: '实验室检查异常' },
            { value: 20, name: '胎儿监测异常' },
            { value: 15, name: '并发症风险' },
            { value: 5, name: '营养风险' }
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
      this.charts.type = chart
    },
    
    initLevelChart() {
      const chart = echarts.init(this.$refs.levelChart)
      const option = {
        title: {
          text: '预警级别分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['紧急', '高危', '中危', '低危']
        },
        yAxis: {
          type: 'value',
          name: '数量'
        },
        series: [{
          data: [12, 35, 58, 82],
          type: 'bar',
          itemStyle: {
            color: function(params) {
              const colors = ['#F56C6C', '#E6A23C', '#ff69b4', '#67C23A']
              return colors[params.dataIndex]
            }
          }
        }]
      }
      chart.setOption(option)
      this.charts.level = chart
    },
    
    initResponseChart() {
      const chart = echarts.init(this.$refs.responseChart)
      const option = {
        title: {
          text: '处理时效分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['0-30分钟', '30分钟-1小时', '1-2小时', '2-4小时', '4-8小时', '8小时以上']
        },
        yAxis: {
          type: 'value',
          name: '预警数量'
        },
        series: [{
          data: [45, 32, 28, 15, 8, 3],
          type: 'bar',
          itemStyle: {
          color: '#ff69b4'
        }
        }]
      }
      chart.setOption(option)
      this.charts.response = chart
    },
    
    createWarning() {
      this.isEdit = false
      this.warningForm = {
        patient_name: '',
        gestational_week: 20,
        warning_level: 'medium',
        warning_type: 'vital_signs',
        warning_message: '',
        threshold_value: '',
        actual_value: '',
        description: '',
        handling_suggestion: '',
        status: 'pending'
      }
      this.warningDialogVisible = true
    },
    
    editWarning(warning) {
      this.isEdit = true
      this.warningForm = { ...warning }
      this.warningDialogVisible = true
    },
    
    saveWarning() {
      this.$refs.warningForm.validate(valid => {
        if (!valid) return
        
        this.saving = true
        
        const url = this.isEdit 
          ? `/warning/records/${this.warningForm.id}`
          : '/warning/records'
        const method = this.isEdit ? 'put' : 'post'
        
        this.$http[method](url, this.warningForm)
          .then(() => {
            this.$message.success(this.isEdit ? '编辑成功' : '创建成功')
            this.warningDialogVisible = false
            this.loadWarningRecords()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('保存失败：' + error.message)
          })
          .finally(() => {
            this.saving = false
          })
      })
    },
    
    deleteWarning(warning) {
      this.$confirm('确定要删除这条预警吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http.delete(`/warning/records/${warning.id}`)
          .then(() => {
            this.$message.success('删除成功')
            this.loadWarningRecords()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('删除失败：' + error.message)
          })
      })
    },
    
    viewWarningDetail(warning) {
      this.currentWarning = warning
      this.detailDialogVisible = true
    },
    
    handleWarning(warning) {
      this.currentWarning = warning
      this.handleForm = {
        status: 'processing',
        handling_result: '',
        remarks: ''
      }
      this.handleDialogVisible = true
    },
    
    submitHandle() {
      this.$refs.handleForm.validate(valid => {
        if (!valid) return
        
        this.handling = true
        
        this.$http.put(`/warning/records/${this.currentWarning.id}/handle`, this.handleForm)
          .then(() => {
            this.$message.success('处理成功')
            this.handleDialogVisible = false
            this.loadWarningRecords()
            this.loadRealtimeWarnings()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('处理失败：' + error.message)
          })
          .finally(() => {
            this.handling = false
          })
      })
    },
    
    batchExport() {
      if (this.selectedWarnings.length === 0) {
        this.$message.warning('请选择要导出的预警')
        return
      }
      
      const ids = this.selectedWarnings.map(warning => warning.id)
      this.$http.post('/warning/export', { ids }, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `预警记录_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    batchUpdateStatus() {
      if (this.selectedWarnings.length === 0) {
        this.$message.warning('请选择要更新的预警')
        return
      }
      
      this.$prompt('请选择新状态', '批量更新状态', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputType: 'select',
        inputOptions: [
          { value: 'pending', label: '待处理' },
          { value: 'processing', label: '处理中' },
          { value: 'resolved', label: '已处理' },
          { value: 'ignored', label: '已忽略' }
        ]
      }).then(({ value }) => {
        const ids = this.selectedWarnings.map(warning => warning.id)
        this.$http.put('/warning/records/batch-status', { ids, status: value })
          .then(() => {
            this.$message.success('批量更新成功')
            this.loadWarningRecords()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('批量更新失败：' + error.message)
          })
      })
    },
    
    exportWarnings() {
      this.$http.post('/warning/export', {}, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `预警记录_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    handleFilterChange() {
      this.pagination.currentPage = 1
      this.loadWarningRecords()
    },
    
    handleSelectionChange(selection) {
      this.selectedWarnings = selection
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadWarningRecords()
    },
    
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadWarningRecords()
    },
    
    handleDialogClose() {
      this.$refs.warningForm.resetFields()
      this.warningDialogVisible = false
    },
    
    refreshData() {
      this.loadWarningRecords()
      this.loadRealtimeWarnings()
      this.loadStatistics()
      this.$message.success('数据已刷新')
    },
    
    startRealtimeUpdate() {
      this.realtimeTimer = setInterval(() => {
        this.loadRealtimeWarnings()
      }, 30000) // 30秒更新一次
    },
    
    stopRealtimeUpdate() {
      if (this.realtimeTimer) {
        clearInterval(this.realtimeTimer)
      }
    },
    
    formatTime(time) {
      if (!time) return ''
      return new Date(time).toLocaleString()
    },
    
    getLevelTagType(level) {
      const types = {
        'critical': 'danger',
        'high': 'warning',
        'medium': '',
        'low': 'info'
      }
      return types[level] || ''
    },
    
    getLevelText(level) {
      const texts = {
        'critical': '紧急',
        'high': '高危',
        'medium': '中危',
        'low': '低危'
      }
      return texts[level] || level
    },
    
    getTypeTagType(type) {
      const types = {
        'vital_signs': 'danger',
        'lab_results': 'warning',
        'fetal_monitoring': '',
        'complications': 'success',
        'nutrition': 'info'
      }
      return types[type] || ''
    },
    
    getTypeText(type) {
      const texts = {
        'vital_signs': '生命体征异常',
        'lab_results': '实验室检查异常',
        'fetal_monitoring': '胎儿监测异常',
        'complications': '并发症风险',
        'nutrition': '营养风险'
      }
      return texts[type] || type
    },
    
    getStatusTagType(status) {
      const types = {
        'pending': 'info',
        'processing': 'warning',
        'resolved': 'success',
        'ignored': 'danger'
      }
      return types[status] || ''
    },
    
    getStatusText(status) {
      const texts = {
        'pending': '待处理',
        'processing': '处理中',
        'resolved': '已处理',
        'ignored': '已忽略'
      }
      return texts[status] || status
    },
    
    destroyCharts() {
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.dispose()
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.warning-system-container {
  padding: 20px;
  height: 100%;
    background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  
  .warning-system-content {
    padding: 20px;
    height: 100%;
    max-width: 1400px;
    margin: 0 auto;
    
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      padding: 25px 30px;
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
      border: 2px solid #dcdfe6;
      
      h2 {
        color: #2c3e50;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
        
        &::before {
          content: "";
          width: 4px;
          height: 30px;
          background: linear-gradient(135deg, #409eff, #66b1ff);
          border-radius: 2px;
        }
      }
    }
    
    .filter-section {
      margin-bottom: 30px;
      padding: 25px;
      background: #ffffff;
      border-radius: 12px;
      border: 2px solid #dcdfe6;
    }
    
    .stats-section {
      margin-bottom: 30px;
      
      .stat-card {
        display: flex;
        align-items: center;
        padding: 30px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 2px solid #dcdfe6;
        
        &:hover {
          transform: translateY(-8px);
          box-shadow: 0 12px 24px rgba(64, 158, 255, 0.15);
        }
        
        &.critical {
          border-color: #F56C6C;
          background: linear-gradient(135deg, #fff5f5, #fff1f0);
          
          .stat-icon {
            color: #F56C6C;
            background: linear-gradient(135deg, #F56C6C, #f78989);
          }
        }
        
        &.high {
          border-color: #E6A23C;
          background: linear-gradient(135deg, #fffbe6, #fff8e6);
          
          .stat-icon {
            color: #E6A23C;
            background: linear-gradient(135deg, #E6A23C, #ebb563);
          }
        }
        
        &.medium {
          border-color: #409eff;
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        
        .stat-icon {
          color: #409eff;
          background: linear-gradient(135deg, #409eff, #66b1ff);
          }
        }
        
        &.resolved {
          border-color: #67C23A;
          background: linear-gradient(135deg, #f6ffed, #f0fff4);
          
          .stat-icon {
            color: #67C23A;
            background: linear-gradient(135deg, #67C23A, #85ce61);
          }
        }
        
        .stat-icon {
          font-size: 36px;
          margin-right: 25px;
          width: 60px;
          height: 60px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .stat-content {
          h3 {
            margin: 0;
            font-size: 32px;
            color: #2c3e50;
            font-weight: 700;
          }
          
          p {
            margin: 8px 0 0 0;
            color: #666;
            font-size: 15px;
            font-weight: 500;
          }
        }
      }
    }
    
    .charts-section {
      margin-bottom: 30px;
      
      .chart-container {
        padding: 25px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        border: 2px solid #dcdfe6;
          background: #ffffff;
        
        h3 {
          color: #409eff;
          margin-bottom: 20px;
          text-align: center;
          font-size: 20px;
          font-weight: 600;
        }
        
        .chart {
          height: 350px;
        }
      }
      
      /* 局部覆盖dv-border-box-8和dv-border-box-10颜色 */
      .dv-border-box-8,
      .dv-border-box-10 {
        --primary-color: #409eff !important;
      --secondary-color: #66b1ff !important;
      background: white !important;
      border-radius: 16px !important;
      border: 2px solid #409eff !important;
        box-shadow: none !important;
      }
      
      .dv-border-box-8 .dv-border-svg path,
      .dv-border-box-8 .dv-border-svg polygon,
      .dv-border-box-8 .dv-border-svg circle,
      .dv-border-box-8 .dv-border-svg rect,
      .dv-border-box-8 .dv-border-svg line,
      .dv-border-box-8 .dv-border-svg polyline,
      .dv-border-box-10 .dv-border-svg path,
      .dv-border-box-10 .dv-border-svg polygon,
      .dv-border-box-10 .dv-border-svg circle {
        fill: #409eff !important;
        stroke: #409eff !important;
        stroke-dasharray: none !important;
        stroke-width: 1px !important;
      }
      
      .dv-border-box-8 text,
      .dv-border-box-10 text {
        fill: #409eff !important;
        stroke: none !important;
      }
      
      /* 确保dv-border-box-8没有蓝色阴影 */
      .dv-border-box-8::before,
      .dv-border-box-8::after {
        box-shadow: none !important;
        border-color: #409eff !important;
      }
    }
    
    .realtime-section {
      margin-bottom: 30px;
      
      .realtime-content {
        padding: 25px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 2px solid #dcdfe6;
        
        h3 {
          color: #2c3e50;
          margin-bottom: 20px;
          font-size: 20px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 10px;
          
          &::before {
            content: "";
            width: 4px;
            height: 24px;
            background: linear-gradient(135deg, #409eff, #66b1ff);
            border-radius: 2px;
          }
        }
        
        .realtime-warnings {
          max-height: 400px;
          overflow-y: auto;
          
          .realtime-warning-item {
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 12px;
            border: 2px solid #dcdfe6;
            background: #ffffff;
            transition: transform 0.2s, box-shadow 0.2s;
            
            &:hover {
              transform: translateX(5px);
              box-shadow: 0 6px 16px rgba(64, 158, 255, 0.15);
            }
            
            &.critical {
              border-color: #F56C6C;
              background: linear-gradient(135deg, #fff5f5, #fff1f0);
            }
            
            &.high {
              border-color: #E6A23C;
              background: linear-gradient(135deg, #fffbe6, #fff8e6);
            }
            
            &.medium {
              border-color: #E6A23C;
              background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            }
            
            &.low {
              border-color: #67C23A;
              background: linear-gradient(135deg, #f6ffed, #f0fff4);
            }
            
            .warning-header {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: 10px;
              
              .warning-time {
                color: #666;
                font-size: 13px;
              }
            }
            
            .warning-content {
              margin-bottom: 15px;
              
              .patient-info {
                font-weight: 600;
                margin-bottom: 5px;
                color: #2c3e50;
                font-size: 16px;
              }
              
              .warning-message {
                color: #666;
                font-size: 14px;
                line-height: 1.5;
              }
            }
            
            .warning-actions {
              display: flex;
              gap: 10px;
            }
          }
        }
      }
    }
    
    .table-section {
      margin-bottom: 30px;
      
      .table-content {
          padding: 25px;
          background: white;
          border-radius: 16px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
          border: 2px solid #dcdfe6;
        
        .el-table {
          border-radius: 12px;
          overflow: hidden;
          
          th {
            background: #f5f7fa;
            color: #2c3e50;
            font-weight: 600;
            padding: 15px;
          }
          
          td {
            padding: 15px;
            color: #666;
            border-bottom: 1px solid #f0f0f0;
          }
        }
      }
    }
    
    .batch-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 30px;
      padding: 20px;
      background: #f5f7fa;
      border-radius: 12px;
      border: 2px solid #dcdfe6;
      
      .selected-info {
        color: #409eff;
        font-weight: 600;
        margin-left: auto;
        font-size: 14px;
      }
    }
    
    .detail-content {
      .detail-item {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        
        label {
          font-weight: 600;
          color: #2c3e50;
          width: 120px;
          margin-right: 15px;
          font-size: 14px;
        }
        
        span {
          color: #666;
          font-size: 14px;
          flex: 1;
        }
      }
      
      .detail-section {
        margin-top: 25px;
        padding-top: 20px;
        border-top: 2px solid #dcdfe6;
        
        h4 {
          color: #409eff;
          margin-bottom: 15px;
          font-size: 16px;
          font-weight: 600;
        }
        
        p {
          color: #666;
          line-height: 1.7;
          font-size: 14px;
        }
      }
    }
  }
}
</style>
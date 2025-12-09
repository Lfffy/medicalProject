<template>
  <div class="nutrition-advice-container">
    <dv-border-box-8 :dur="5">
      <div class="nutrition-advice-content">
        <div class="header">
          <h2>营养建议</h2>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-plus" @click="createAdvice">创建建议</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportAdvice">导出建议</el-button>
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
              <el-select v-model="filters.gestationalStage" placeholder="孕期阶段" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="孕早期(1-12周)" value="early"></el-option>
                <el-option label="孕中期(13-28周)" value="middle"></el-option>
                <el-option label="孕晚期(29-40周)" value="late"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.adviceType" placeholder="建议类型" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="饮食建议" value="diet"></el-option>
                <el-option label="营养补充" value="supplement"></el-option>
                <el-option label="运动建议" value="exercise"></el-option>
                <el-option label="生活方式" value="lifestyle"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.priority" placeholder="优先级" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="高" value="high"></el-option>
                <el-option label="中" value="medium"></el-option>
                <el-option label="低" value="low"></el-option>
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
                    <p>管理孕妇数</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="el-icon-document"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.totalAdvice }}</h3>
                    <p>营养建议数</p>
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
                    <h3>{{ stats.highPriorityCount }}</h3>
                    <p>高优先级建议</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="el-icon-check"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.completedCount }}</h3>
                    <p>已完成建议</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 营养分析图表 -->
        <div class="charts-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>营养成分摄入分析</h3>
                  <div ref="nutritionChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>体重增长趋势</h3>
                  <div ref="weightChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>饮食结构分布</h3>
                  <div ref="dietChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="chart-container">
                  <h3>建议执行情况</h3>
                  <div ref="executionChart" class="chart"></div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 营养建议表格 -->
        <div class="table-section">
          <dv-border-box-10>
            <div class="table-content">
              <el-table
                :data="nutritionAdvice"
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
                <el-table-column prop="advice_type" label="建议类型" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getAdviceTypeTagType(scope.row.advice_type)">
                      {{ getAdviceTypeText(scope.row.advice_type) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="priority" label="优先级" width="80">
                  <template slot-scope="scope">
                    <el-tag :type="getPriorityTagType(scope.row.priority)">
                      {{ getPriorityText(scope.row.priority) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="advice_title" label="建议标题" width="200"></el-table-column>
                <el-table-column prop="target_nutrients" label="目标营养素" width="150"></el-table-column>
                <el-table-column prop="daily_intake" label="每日摄入量" width="120"></el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getStatusTagType(scope.row.status)">
                      {{ getStatusText(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="created_date" label="创建日期" width="120">
                  <template slot-scope="scope">
                    {{ formatDate(scope.row.created_date) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="viewDetails(scope.row)">查看</el-button>
                    <el-button size="mini" type="primary" @click="editAdvice(scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="deleteAdvice(scope.row)">删除</el-button>
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
        <div class="batch-actions" v-if="selectedAdvice.length > 0">
          <el-button type="success" @click="batchExport">批量导出</el-button>
          <el-button type="warning" @click="batchUpdateStatus">批量更新状态</el-button>
          <span class="selected-info">已选择 {{ selectedAdvice.length }} 条建议</span>
        </div>

        <!-- 创建/编辑建议对话框 -->
        <el-dialog
          :title="dialogTitle"
          :visible.sync="adviceDialogVisible"
          width="900px"
          :before-close="handleDialogClose"
        >
          <el-form
            ref="adviceForm"
            :model="adviceForm"
            :rules="adviceRules"
            label-width="120px"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="孕妇姓名" prop="patient_name">
                  <el-input v-model="adviceForm.patient_name" placeholder="请输入孕妇姓名"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="孕周" prop="gestational_week">
                  <el-input-number v-model="adviceForm.gestational_week" :min="1" :max="42" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="建议类型" prop="advice_type">
                  <el-select v-model="adviceForm.advice_type" placeholder="选择建议类型" style="width: 100%">
                    <el-option label="饮食建议" value="diet"></el-option>
                    <el-option label="营养补充" value="supplement"></el-option>
                    <el-option label="运动建议" value="exercise"></el-option>
                    <el-option label="生活方式" value="lifestyle"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="优先级" prop="priority">
                  <el-select v-model="adviceForm.priority" placeholder="选择优先级" style="width: 100%">
                    <el-option label="高" value="high"></el-option>
                    <el-option label="中" value="medium"></el-option>
                    <el-option label="低" value="low"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="建议标题" prop="advice_title">
              <el-input v-model="adviceForm.advice_title" placeholder="请输入建议标题"></el-input>
            </el-form-item>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="目标营养素" prop="target_nutrients">
                  <el-input v-model="adviceForm.target_nutrients" placeholder="如：叶酸、铁、钙等"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="每日摄入量" prop="daily_intake">
                  <el-input v-model="adviceForm.daily_intake" placeholder="如：400μg、30mg等"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="建议内容" prop="advice_content">
              <el-input
                v-model="adviceForm.advice_content"
                type="textarea"
                :rows="4"
                placeholder="请详细描述营养建议内容"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="食物推荐" prop="food_recommendations">
              <el-input
                v-model="adviceForm.food_recommendations"
                type="textarea"
                :rows="3"
                placeholder="请推荐相关食物"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="注意事项" prop="precautions">
              <el-input
                v-model="adviceForm.precautions"
                type="textarea"
                :rows="3"
                placeholder="请输入注意事项"
              ></el-input>
            </el-form-item>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="执行周期" prop="execution_period">
                  <el-input v-model="adviceForm.execution_period" placeholder="如：4周、整个孕期等"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="状态" prop="status">
                  <el-select v-model="adviceForm.status" placeholder="选择状态" style="width: 100%">
                    <el-option label="待执行" value="pending"></el-option>
                    <el-option label="执行中" value="executing"></el-option>
                    <el-option label="已完成" value="completed"></el-option>
                    <el-option label="已暂停" value="paused"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          
          <div slot="footer" class="dialog-footer">
            <el-button @click="adviceDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveAdvice" :loading="saving">保存</el-button>
          </div>
        </el-dialog>

        <!-- 详情对话框 -->
        <el-dialog
          title="营养建议详情"
          :visible.sync="detailDialogVisible"
          width="900px"
        >
          <div class="detail-content" v-if="currentAdvice">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>孕妇姓名：</label>
                  <span>{{ currentAdvice.patient_name }}</span>
                </div>
                <div class="detail-item">
                  <label>孕周：</label>
                  <span>{{ currentAdvice.gestational_week }}周</span>
                </div>
                <div class="detail-item">
                  <label>建议类型：</label>
                  <el-tag :type="getAdviceTypeTagType(currentAdvice.advice_type)">
                    {{ getAdviceTypeText(currentAdvice.advice_type) }}
                  </el-tag>
                </div>
                <div class="detail-item">
                  <label>优先级：</label>
                  <el-tag :type="getPriorityTagType(currentAdvice.priority)">
                    {{ getPriorityText(currentAdvice.priority) }}
                  </el-tag>
                </div>
                <div class="detail-item">
                  <label>目标营养素：</label>
                  <span>{{ currentAdvice.target_nutrients }}</span>
                </div>
                <div class="detail-item">
                  <label>每日摄入量：</label>
                  <span>{{ currentAdvice.daily_intake }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>建议标题：</label>
                  <span>{{ currentAdvice.advice_title }}</span>
                </div>
                <div class="detail-item">
                  <label>执行周期：</label>
                  <span>{{ currentAdvice.execution_period }}</span>
                </div>
                <div class="detail-item">
                  <label>状态：</label>
                  <el-tag :type="getStatusTagType(currentAdvice.status)">
                    {{ getStatusText(currentAdvice.status) }}
                  </el-tag>
                </div>
                <div class="detail-item">
                  <label>创建日期：</label>
                  <span>{{ formatDate(currentAdvice.created_date) }}</span>
                </div>
                <div class="detail-item">
                  <label>更新日期：</label>
                  <span>{{ formatDate(currentAdvice.updated_date) }}</span>
                </div>
                <div class="detail-item">
                  <label>创建人：</label>
                  <span>{{ currentAdvice.created_by }}</span>
                </div>
              </el-col>
            </el-row>
            
            <div class="detail-section">
              <h4>建议内容</h4>
              <p>{{ currentAdvice.advice_content }}</p>
            </div>
            
            <div class="detail-section">
              <h4>食物推荐</h4>
              <p>{{ currentAdvice.food_recommendations }}</p>
            </div>
            
            <div class="detail-section">
              <h4>注意事项</h4>
              <p>{{ currentAdvice.precautions }}</p>
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
  name: 'NutritionAdvice',
  data() {
    return {
      loading: false,
      saving: false,
      adviceDialogVisible: false,
      detailDialogVisible: false,
      isEdit: false,
      
      // 筛选条件
      filters: {
        patientName: '',
        gestationalStage: '',
        adviceType: '',
        priority: ''
      },
      
      // 统计数据
      stats: {
        totalPatients: 0,
        totalAdvice: 0,
        highPriorityCount: 0,
        completedCount: 0
      },
      
      // 营养建议
      nutritionAdvice: [],
      selectedAdvice: [],
      
      // 分页
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      
      // 建议表单
      adviceForm: {
        patient_name: '',
        gestational_week: 20,
        advice_type: 'diet',
        priority: 'medium',
        advice_title: '',
        target_nutrients: '',
        daily_intake: '',
        advice_content: '',
        food_recommendations: '',
        precautions: '',
        execution_period: '',
        status: 'pending'
      },
      
      // 表单验证规则
      adviceRules: {
        patient_name: [
          { required: true, message: '请输入孕妇姓名', trigger: 'blur' }
        ],
        gestational_week: [
          { required: true, message: '请输入孕周', trigger: 'blur' }
        ],
        advice_type: [
          { required: true, message: '请选择建议类型', trigger: 'change' }
        ],
        priority: [
          { required: true, message: '请选择优先级', trigger: 'change' }
        ],
        advice_title: [
          { required: true, message: '请输入建议标题', trigger: 'blur' }
        ],
        advice_content: [
          { required: true, message: '请输入建议内容', trigger: 'blur' }
        ]
      },
      
      // 当前建议
      currentAdvice: null,
      
      // 图表实例
      charts: {
        nutrition: null,
        weight: null,
        diet: null,
        execution: null
      }
    }
  },
  
  computed: {
    dialogTitle() {
      return this.isEdit ? '编辑营养建议' : '创建营养建议'
    }
  },
  
  mounted() {
    this.loadNutritionAdvice()
    this.loadStatistics()
    this.initCharts()
  },
  
  beforeDestroy() {
    this.destroyCharts()
  },
  
  methods: {
    loadNutritionAdvice() {
      this.loading = true
      
      const params = {
        page: this.pagination.currentPage,
        page_size: this.pagination.pageSize,
        patient_name: this.filters.patientName,
        gestational_stage: this.filters.gestationalStage,
        advice_type: this.filters.adviceType,
        priority: this.filters.priority
      }
      
      this.$http.get('/nutrition/advice', { params })
        .then(response => {
          const data = response.data.data
          this.nutritionAdvice = data.advice || []
          this.pagination.total = data.total || 0
        })
        .catch(error => {
          this.$message.error('加载营养建议失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    loadStatistics() {
      this.$http.get('/nutrition/statistics')
        .then(response => {
          const data = response.data.data
          this.stats = {
            totalPatients: data.total_patients || 0,
            totalAdvice: data.total_advice || 0,
            highPriorityCount: data.high_priority_count || 0,
            completedCount: data.completed_count || 0
          }
        })
        .catch(error => {
          this.$message.error('加载统计数据失败：' + error.message)
        })
    },
    
    initCharts() {
      this.$nextTick(() => {
        this.initNutritionChart()
        this.initWeightChart()
        this.initDietChart()
        this.initExecutionChart()
      })
    },
    
    initNutritionChart() {
      const chart = echarts.init(this.$refs.nutritionChart)
      const option = {
        title: {
          text: '营养成分摄入分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['推荐摄入', '实际摄入'],
          top: 30
        },
        radar: {
          indicator: [
            { name: '蛋白质', max: 100 },
            { name: '碳水化合物', max: 100 },
            { name: '脂肪', max: 100 },
            { name: '维生素', max: 100 },
            { name: '矿物质', max: 100 },
            { name: '纤维素', max: 100 }
          ]
        },
        series: [{
          type: 'radar',
          data: [
            {
              value: [85, 90, 70, 80, 75, 65],
              name: '推荐摄入',
              lineStyle: {
                color: '#ff69b4'
              },
              areaStyle: {
                color: 'rgba(255, 105, 180, 0.2)'
              }
            },
            {
              value: [75, 85, 65, 70, 80, 60],
              name: '实际摄入',
              lineStyle: {
                color: '#67C23A'
              },
              areaStyle: {
                color: 'rgba(103, 194, 58, 0.2)'
              }
            }
          ]
        }]
      }
      chart.setOption(option)
      this.charts.nutrition = chart
    },
    
    initWeightChart() {
      const chart = echarts.init(this.$refs.weightChart)
      const option = {
        title: {
          text: '体重增长趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['实际体重', '推荐体重范围'],
          top: 30
        },
        xAxis: {
          type: 'category',
          data: ['孕前', '8周', '12周', '16周', '20周', '24周', '28周', '32周', '36周', '40周']
        },
        yAxis: {
          type: 'value',
          name: '体重(kg)'
        },
        series: [
          {
            name: '实际体重',
            type: 'line',
            data: [55, 55.5, 56, 57, 58, 59.5, 61, 63, 65, 67],
            lineStyle: {
              color: '#E6A23C'
            }
          },
          {
            name: '推荐体重范围',
            type: 'line',
            data: [55, 55.8, 56.5, 57.5, 58.8, 60.2, 62, 64, 66, 68],
            lineStyle: {
              color: '#909399',
              type: 'dashed'
            }
          }
        ]
      }
      chart.setOption(option)
      this.charts.weight = chart
    },
    
    initDietChart() {
      const chart = echarts.init(this.$refs.dietChart)
      const option = {
        title: {
          text: '饮食结构分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        series: [{
          name: '饮食结构',
          type: 'pie',
          radius: '60%',
          data: [
            { value: 30, name: '谷物类' },
            { value: 25, name: '蔬菜水果' },
            { value: 20, name: '蛋白质食物' },
            { value: 15, name: '乳制品' },
            { value: 10, name: '健康脂肪' }
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
      this.charts.diet = chart
    },
    
    initExecutionChart() {
      const chart = echarts.init(this.$refs.executionChart)
      const option = {
        title: {
          text: '建议执行情况',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周', '第7周', '第8周']
        },
        yAxis: {
          type: 'value',
          name: '执行率(%)'
        },
        series: [{
          data: [85, 88, 82, 90, 87, 92, 89, 94],
          type: 'bar',
          itemStyle: {
            color: '#67C23A'
          }
        }]
      }
      chart.setOption(option)
      this.charts.execution = chart
    },
    
    createAdvice() {
      this.isEdit = false
      this.adviceForm = {
        patient_name: '',
        gestational_week: 20,
        advice_type: 'diet',
        priority: 'medium',
        advice_title: '',
        target_nutrients: '',
        daily_intake: '',
        advice_content: '',
        food_recommendations: '',
        precautions: '',
        execution_period: '',
        status: 'pending'
      }
      this.adviceDialogVisible = true
    },
    
    editAdvice(advice) {
      this.isEdit = true
      this.adviceForm = { ...advice }
      this.adviceDialogVisible = true
    },
    
    saveAdvice() {
      this.$refs.adviceForm.validate(valid => {
        if (!valid) return
        
        this.saving = true
        
        const url = this.isEdit 
          ? `/api/nutrition/advice/${this.adviceForm.id}`
          : '/api/nutrition/advice'
        const method = this.isEdit ? 'put' : 'post'
        
        this.$http[method](url, this.adviceForm)
          .then(() => {
            this.$message.success(this.isEdit ? '编辑成功' : '创建成功')
            this.adviceDialogVisible = false
            this.loadNutritionAdvice()
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
    
    deleteAdvice(advice) {
      this.$confirm('确定要删除这条营养建议吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http.delete(`/api/nutrition/advice/${advice.id}`)
          .then(() => {
            this.$message.success('删除成功')
            this.loadNutritionAdvice()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('删除失败：' + error.message)
          })
      })
    },
    
    viewDetails(advice) {
      this.currentAdvice = advice
      this.detailDialogVisible = true
    },
    
    batchExport() {
      if (this.selectedAdvice.length === 0) {
        this.$message.warning('请选择要导出的建议')
        return
      }
      
      const ids = this.selectedAdvice.map(advice => advice.id)
      this.$http.post('/api/nutrition/export', { ids }, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `营养建议_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    batchUpdateStatus() {
      if (this.selectedAdvice.length === 0) {
        this.$message.warning('请选择要更新的建议')
        return
      }
      
      this.$prompt('请选择新状态', '批量更新状态', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputType: 'select',
        inputOptions: [
          { value: 'pending', label: '待执行' },
          { value: 'executing', label: '执行中' },
          { value: 'completed', label: '已完成' },
          { value: 'paused', label: '已暂停' }
        ]
      }).then(({ value }) => {
        const ids = this.selectedAdvice.map(advice => advice.id)
        this.$http.put('/api/nutrition/advice/batch-status', { ids, status: value })
          .then(() => {
            this.$message.success('批量更新成功')
            this.loadNutritionAdvice()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('批量更新失败：' + error.message)
          })
      })
    },
    
    exportAdvice() {
      this.$http.post('/api/nutrition/export', {}, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `营养建议_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    handleFilterChange() {
      this.pagination.currentPage = 1
      this.loadNutritionAdvice()
    },
    
    handleSelectionChange(selection) {
      this.selectedAdvice = selection
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadNutritionAdvice()
    },
    
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadNutritionAdvice()
    },
    
    handleDialogClose() {
      this.$refs.adviceForm.resetFields()
      this.adviceDialogVisible = false
    },
    
    refreshData() {
      this.loadNutritionAdvice()
      this.loadStatistics()
      this.$message.success('数据已刷新')
    },
    
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },
    
    getAdviceTypeTagType(type) {
      const types = {
        'diet': 'primary',
        'supplement': 'success',
        'exercise': 'warning',
        'lifestyle': 'info'
      }
      return types[type] || ''
    },
    
    getAdviceTypeText(type) {
      const texts = {
        'diet': '饮食建议',
        'supplement': '营养补充',
        'exercise': '运动建议',
        'lifestyle': '生活方式'
      }
      return texts[type] || type
    },
    
    getPriorityTagType(priority) {
      const types = {
        'high': 'danger',
        'medium': 'warning',
        'low': 'info'
      }
      return types[priority] || ''
    },
    
    getPriorityText(priority) {
      const texts = {
        'high': '高',
        'medium': '中',
        'low': '低'
      }
      return texts[priority] || priority
    },
    
    getStatusTagType(status) {
      const types = {
        'pending': 'info',
        'executing': 'warning',
        'completed': 'success',
        'paused': 'danger'
      }
      return types[status] || ''
    },
    
    getStatusText(status) {
      const texts = {
        'pending': '待执行',
        'executing': '执行中',
        'completed': '已完成',
        'paused': '已暂停'
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

<style scoped>
/* 全局样式 */
.nutrition-advice-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  padding: 20px;
}

.nutrition-advice-content {
  max-width: 1400px;
  margin: 0 auto;
}

/* 页面头部样式 */
.header {
  background: white;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header h2::before {
  content: "";
  width: 4px;
  height: 24px;
  background: linear-gradient(135deg, #ff69b4, #ff85a2);
  border-radius: 2px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* 筛选区域样式 */
.filter-section {
  background: white;
  padding: 25px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.filter-section .el-row {
  width: 100%;
}

/* 统计卡片样式 */
.stats-section {
  margin-bottom: 30px;
}

.stats-section .el-row {
  width: 100%;
}

.stats-section .el-col {
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
  width: 100%;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  font-size: 2.2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon i {
  font-size: 1.5rem;
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 5px 0;
}

.stat-content p {
  font-size: 0.95rem;
  color: #7f8c8d;
  font-weight: 500;
  margin: 0;
}

/* 图表区域样式 */
.charts-section {
  margin-bottom: 30px;
}

.charts-section .el-row {
  width: 100%;
}

.chart-container {
  background: white;
  padding: 25px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

.chart-container h3 {
  margin: 0 0 15px 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  text-align: center;
}

.chart {
  height: 300px;
}

/* 表格区域样式 */
.table-section {
  margin-bottom: 30px;
}

.table-content {
  background: white;
  padding: 25px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.table-content .el-table {
  border-radius: 8px;
  overflow: hidden;
}

.table-content .el-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.table-content .el-table td {
  color: #34495e;
}

/* 批量操作样式 */
.batch-actions {
  background: white;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}

.batch-actions .selected-info {
  margin-left: auto;
  color: #7f8c8d;
  font-size: 14px;
}

/* 详情对话框样式 */
.detail-content {
  width: 100%;
}

.detail-content .detail-item {
  display: flex;
  margin-bottom: 10px;
}

.detail-content .detail-item label {
  font-weight: bold;
  color: #666;
  width: 100px;
}

.detail-content .detail-item span {
  color: #333;
}

.detail-content .detail-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.detail-content .detail-section h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.detail-content .detail-section p {
  margin: 0;
  color: #34495e;
  line-height: 1.6;
}

/* 对话框通用样式 */
.el-dialog {
  border-radius: 12px;
  overflow: hidden;
}

.el-dialog__header {
  background: linear-gradient(135deg, #ff69b4, #ff85a2);
  color: white;
  padding: 20px 30px;
}

.el-dialog__title {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.el-dialog__body {
  padding: 30px;
}

.el-dialog__footer {
  padding: 20px 30px;
  border-top: 1px solid #f0f0f0;
  background-color: #fafafa;
}

/* 表单样式 */
.el-form {
  width: 100%;
}

.el-form-item {
  margin-bottom: 25px;
}

.el-form-item__label {
  font-weight: 500;
  color: #2c3e50;
}

/* 按钮样式 */
.el-button--primary {
  background: linear-gradient(135deg, #ff69b4, #ff85a2);
  border: none;
}

.el-button--primary:hover,
.el-button--primary:focus {
  background: linear-gradient(135deg, #ff85a2, #ffb6c1);
}

.el-button--success {
  background: linear-gradient(135deg, #ff69b4, #ff85a2);
  border: none;
}

.el-button--success:hover,
.el-button--success:focus {
  background: linear-gradient(135deg, #ff85a2, #ffb6c1);
}

.el-button--danger {
  background: linear-gradient(135deg, #ff69b4, #ff85a2);
  border: none;
}

.el-button--danger:hover,
.el-button--danger:focus {
  background: linear-gradient(135deg, #ff85a2, #ffb6c1);
}

.el-button--info {
  background: linear-gradient(135deg, #ff69b4, #ff85a2);
  border: none;
}

.el-button--info:hover,
.el-button--info:focus {
  background: linear-gradient(135deg, #ff85a2, #ffb6c1);
}

.el-button--warning {
  background: linear-gradient(135deg, #ff69b4, #ff85a2);
  border: none;
}

.el-button--warning:hover,
.el-button--warning:focus {
  background: linear-gradient(135deg, #ff85a2, #ffb6c1);
}

/* 标签样式 */
.el-tag {
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nutrition-advice-container {
    padding: 10px;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
    padding: 15px 20px;
  }
  
  .header-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .filter-section {
    padding: 15px 20px;
  }
  
  .filter-section .el-col {
    margin-bottom: 15px;
  }
  
  .stats-section .el-col {
    margin-bottom: 15px;
  }
  
  .chart-container,
  .table-content,
  .batch-actions {
    padding: 15px 20px;
  }
  
  .chart {
    height: 250px;
  }
  
  .batch-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .batch-actions .selected-info {
    margin-left: 0;
    text-align: center;
    margin-top: 10px;
  }
  
  .el-dialog__body {
    padding: 20px;
  }
}
</style>
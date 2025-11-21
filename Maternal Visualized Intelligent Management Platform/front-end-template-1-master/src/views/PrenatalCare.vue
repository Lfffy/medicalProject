<template>
  <div class="prenatal-care-container">
    <dv-border-box-8 :dur="5">
      <div class="prenatal-care-content">
        <div class="header">
          <h2>产检记录管理</h2>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-plus" @click="showAddDialog">新增产检</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportRecords">导出记录</el-button>
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
              <el-select v-model="filters.gestationalWeek" placeholder="孕周范围" clearable @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="早期(<12周)" value="early"></el-option>
                <el-option label="中期(12-28周)" value="middle"></el-option>
                <el-option label="晚期(>28周)" value="late"></el-option>
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
                    <p>总孕妇数</p>
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
                    <h3>{{ stats.totalRecords }}</h3>
                    <p>产检记录数</p>
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
                    <h3>{{ stats.highRiskCount }}</h3>
                    <p>高危孕妇</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="6">
              <dv-border-box-10>
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="el-icon-date"></i>
                  </div>
                  <div class="stat-content">
                    <h3>{{ stats.todayCheckups }}</h3>
                    <p>今日产检</p>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 产检记录表格 -->
        <div class="table-section">
          <dv-border-box-10>
            <div class="table-content">
              <el-table
                :data="prenatalRecords"
                border
                stripe
                style="width: 100%"
                v-loading="loading"
                @selection-change="handleSelectionChange"
              >
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="id" label="ID" width="80"></el-table-column>
                <el-table-column prop="patient_name" label="孕妇姓名" width="120"></el-table-column>
                <el-table-column prop="age" label="年龄" width="80"></el-table-column>
                <el-table-column prop="gestational_week" label="孕周" width="100">
                  <template slot-scope="scope">
                    {{ scope.row.gestational_week }}周
                  </template>
                </el-table-column>
                <el-table-column prop="checkup_date" label="产检日期" width="120">
                  <template slot-scope="scope">
                    {{ formatDate(scope.row.checkup_date) }}
                  </template>
                </el-table-column>
                <el-table-column prop="hospital" label="医院" width="150"></el-table-column>
                <el-table-column prop="doctor" label="医生" width="100"></el-table-column>
                <el-table-column prop="weight" label="体重(kg)" width="100"></el-table-column>
                <el-table-column prop="blood_pressure" label="血压" width="120"></el-table-column>
                <el-table-column prop="fetal_heart_rate" label="胎心率" width="100">
                  <template slot-scope="scope">
                    {{ scope.row.fetal_heart_rate }}次/分
                  </template>
                </el-table-column>
                <el-table-column prop="risk_level" label="风险等级" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getRiskTagType(scope.row.risk_level)">
                      {{ scope.row.risk_level }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="viewDetails(scope.row)">查看</el-button>
                    <el-button size="mini" type="primary" @click="editRecord(scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="deleteRecord(scope.row)">删除</el-button>
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
          <el-button type="danger" @click="batchDelete">批量删除</el-button>
          <el-button type="success" @click="batchExport">批量导出</el-button>
          <span class="selected-info">已选择 {{ selectedRecords.length }} 条记录</span>
        </div>

        <!-- 新增/编辑对话框 -->
        <el-dialog
          :title="dialogTitle"
          :visible.sync="dialogVisible"
          width="800px"
          :before-close="handleDialogClose"
        >
          <el-form
            ref="recordForm"
            :model="recordForm"
            :rules="formRules"
            label-width="120px"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="孕妇姓名" prop="patient_name">
                  <el-input v-model="recordForm.patient_name" placeholder="请输入孕妇姓名"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="年龄" prop="age">
                  <el-input-number v-model="recordForm.age" :min="15" :max="50" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="孕周" prop="gestational_week">
                  <el-input-number v-model="recordForm.gestational_week" :min="1" :max="42" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="产检日期" prop="checkup_date">
                  <el-date-picker
                    v-model="recordForm.checkup_date"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                  ></el-date-picker>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="医院" prop="hospital">
                  <el-select v-model="recordForm.hospital" placeholder="选择医院" style="width: 100%">
                    <el-option label="北京妇产医院" value="北京妇产医院"></el-option>
                    <el-option label="上海第一妇婴保健院" value="上海第一妇婴保健院"></el-option>
                    <el-option label="广州妇女儿童医疗中心" value="广州妇女儿童医疗中心"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="医生" prop="doctor">
                  <el-input v-model="recordForm.doctor" placeholder="请输入医生姓名"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="体重(kg)" prop="weight">
                  <el-input-number v-model="recordForm.weight" :min="30" :max="150" :precision="1" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="血压" prop="blood_pressure">
                  <el-input v-model="recordForm.blood_pressure" placeholder="120/80"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="胎心率" prop="fetal_heart_rate">
                  <el-input-number v-model="recordForm.fetal_heart_rate" :min="100" :max="180" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="宫高(cm)" prop="uterine_height">
                  <el-input-number v-model="recordForm.uterine_height" :min="10" :max="40" :precision="1" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="腹围(cm)" prop="abdominal_circumference">
                  <el-input-number v-model="recordForm.abdominal_circumference" :min="50" :max="150" :precision="1" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="风险等级" prop="risk_level">
              <el-radio-group v-model="recordForm.risk_level">
                <el-radio label="低风险">低风险</el-radio>
                <el-radio label="中风险">中风险</el-radio>
                <el-radio label="高风险">高风险</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="检查结果" prop="checkup_result">
              <el-input
                v-model="recordForm.checkup_result"
                type="textarea"
                :rows="3"
                placeholder="请输入检查结果"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="医嘱建议" prop="medical_advice">
              <el-input
                v-model="recordForm.medical_advice"
                type="textarea"
                :rows="3"
                placeholder="请输入医嘱建议"
              ></el-input>
            </el-form-item>
          </el-form>
          
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveRecord" :loading="saving">保存</el-button>
          </div>
        </el-dialog>

        <!-- 详情对话框 -->
        <el-dialog
          title="产检记录详情"
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
                  <label>年龄：</label>
                  <span>{{ currentRecord.age }}岁</span>
                </div>
                <div class="detail-item">
                  <label>孕周：</label>
                  <span>{{ currentRecord.gestational_week }}周</span>
                </div>
                <div class="detail-item">
                  <label>产检日期：</label>
                  <span>{{ formatDate(currentRecord.checkup_date) }}</span>
                </div>
                <div class="detail-item">
                  <label>医院：</label>
                  <span>{{ currentRecord.hospital }}</span>
                </div>
                <div class="detail-item">
                  <label>医生：</label>
                  <span>{{ currentRecord.doctor }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>体重：</label>
                  <span>{{ currentRecord.weight }}kg</span>
                </div>
                <div class="detail-item">
                  <label>血压：</label>
                  <span>{{ currentRecord.blood_pressure }}</span>
                </div>
                <div class="detail-item">
                  <label>胎心率：</label>
                  <span>{{ currentRecord.fetal_heart_rate }}次/分</span>
                </div>
                <div class="detail-item">
                  <label>宫高：</label>
                  <span>{{ currentRecord.uterine_height }}cm</span>
                </div>
                <div class="detail-item">
                  <label>腹围：</label>
                  <span>{{ currentRecord.abdominal_circumference }}cm</span>
                </div>
                <div class="detail-item">
                  <label>风险等级：</label>
                  <el-tag :type="getRiskTagType(currentRecord.risk_level)">
                    {{ currentRecord.risk_level }}
                  </el-tag>
                </div>
              </el-col>
            </el-row>
            
            <div class="detail-section">
              <h4>检查结果</h4>
              <p>{{ currentRecord.checkup_result || '暂无记录' }}</p>
            </div>
            
            <div class="detail-section">
              <h4>医嘱建议</h4>
              <p>{{ currentRecord.medical_advice || '暂无记录' }}</p>
            </div>
          </div>
        </el-dialog>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
export default {
  name: 'PrenatalCare',
  data() {
    return {
      loading: false,
      saving: false,
      dialogVisible: false,
      detailDialogVisible: false,
      isEdit: false,
      
      // 筛选条件
      filters: {
        patientName: '',
        hospital: '',
        dateRange: [],
        gestationalWeek: ''
      },
      
      // 统计数据
      stats: {
        totalPatients: 0,
        totalRecords: 0,
        highRiskCount: 0,
        todayCheckups: 0
      },
      
      // 产检记录
      prenatalRecords: [],
      selectedRecords: [],
      
      // 分页
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      
      // 表单数据
      recordForm: {
        patient_name: '',
        age: 25,
        gestational_week: 20,
        checkup_date: new Date(),
        hospital: '',
        doctor: '',
        weight: 60.0,
        blood_pressure: '120/80',
        fetal_heart_rate: 140,
        uterine_height: 20.0,
        abdominal_circumference: 85.0,
        risk_level: '低风险',
        checkup_result: '',
        medical_advice: ''
      },
      
      // 表单验证规则
      formRules: {
        patient_name: [
          { required: true, message: '请输入孕妇姓名', trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        gestational_week: [
          { required: true, message: '请输入孕周', trigger: 'blur' }
        ],
        checkup_date: [
          { required: true, message: '请选择产检日期', trigger: 'change' }
        ],
        hospital: [
          { required: true, message: '请选择医院', trigger: 'change' }
        ],
        doctor: [
          { required: true, message: '请输入医生姓名', trigger: 'blur' }
        ]
      },
      
      // 当前记录
      currentRecord: null
    }
  },
  
  computed: {
    dialogTitle() {
      return this.isEdit ? '编辑产检记录' : '新增产检记录'
    }
  },
  
  mounted() {
    this.loadPrenatalRecords()
    this.loadStatistics()
  },
  
  methods: {
    loadPrenatalRecords() {
      this.loading = true
      
      const params = {
        page: this.pagination.currentPage,
        page_size: this.pagination.pageSize,
        patient_name: this.filters.patientName,
        hospital: this.filters.hospital,
        start_date: this.filters.dateRange?.[0],
        end_date: this.filters.dateRange?.[1],
        gestational_week: this.filters.gestationalWeek
      }
      
      this.$http.get('/api/prenatal/records', { params })
        .then(response => {
          const data = response.data.data
          this.prenatalRecords = data.records || []
          this.pagination.total = data.total || 0
        })
        .catch(error => {
          this.$message.error('加载产检记录失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    loadStatistics() {
      this.$http.get('/api/prenatal/statistics')
        .then(response => {
          const data = response.data.data
          this.stats = {
            totalPatients: data.total_patients || 0,
            totalRecords: data.total_records || 0,
            highRiskCount: data.high_risk_count || 0,
            todayCheckups: data.today_checkups || 0
          }
        })
        .catch(error => {
          this.$message.error('加载统计数据失败：' + error.message)
        })
    },
    
    showAddDialog() {
      this.isEdit = false
      this.recordForm = {
        patient_name: '',
        age: 25,
        gestational_week: 20,
        checkup_date: new Date(),
        hospital: '',
        doctor: '',
        weight: 60.0,
        blood_pressure: '120/80',
        fetal_heart_rate: 140,
        uterine_height: 20.0,
        abdominal_circumference: 85.0,
        risk_level: '低风险',
        checkup_result: '',
        medical_advice: ''
      }
      this.dialogVisible = true
    },
    
    editRecord(record) {
      this.isEdit = true
      this.recordForm = { ...record }
      this.dialogVisible = true
    },
    
    saveRecord() {
      this.$refs.recordForm.validate(valid => {
        if (!valid) return
        
        this.saving = true
        
        const url = this.isEdit 
          ? `/api/prenatal/records/${this.recordForm.id}`
          : '/api/prenatal/records'
        const method = this.isEdit ? 'put' : 'post'
        
        this.$http[method](url, this.recordForm)
          .then(() => {
            this.$message.success(this.isEdit ? '编辑成功' : '新增成功')
            this.dialogVisible = false
            this.loadPrenatalRecords()
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
    
    deleteRecord(record) {
      this.$confirm('确定要删除这条产检记录吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http.delete(`/api/prenatal/records/${record.id}`)
          .then(() => {
            this.$message.success('删除成功')
            this.loadPrenatalRecords()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('删除失败：' + error.message)
          })
      })
    },
    
    viewDetails(record) {
      this.currentRecord = record
      this.detailDialogVisible = true
    },
    
    batchDelete() {
      if (this.selectedRecords.length === 0) {
        this.$message.warning('请选择要删除的记录')
        return
      }
      
      this.$confirm(`确定要删除选中的 ${this.selectedRecords.length} 条记录吗？`, '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const ids = this.selectedRecords.map(record => record.id)
        this.$http.delete('/api/prenatal/records/batch', { data: { ids } })
          .then(() => {
            this.$message.success('批量删除成功')
            this.loadPrenatalRecords()
            this.loadStatistics()
          })
          .catch(error => {
            this.$message.error('批量删除失败：' + error.message)
          })
      })
    },
    
    batchExport() {
      if (this.selectedRecords.length === 0) {
        this.$message.warning('请选择要导出的记录')
        return
      }
      
      const ids = this.selectedRecords.map(record => record.id)
      this.$http.post('/api/prenatal/export', { ids }, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `产检记录_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    exportRecords() {
      this.$http.post('/api/prenatal/export', {}, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data])
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = `产检记录_${new Date().toLocaleDateString()}.xlsx`
          link.click()
        })
        .catch(error => {
          this.$message.error('导出失败：' + error.message)
        })
    },
    
    handleFilterChange() {
      this.pagination.currentPage = 1
      this.loadPrenatalRecords()
    },
    
    handleSelectionChange(selection) {
      this.selectedRecords = selection
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadPrenatalRecords()
    },
    
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadPrenatalRecords()
    },
    
    handleDialogClose() {
      this.$refs.recordForm.resetFields()
      this.dialogVisible = false
    },
    
    refreshData() {
      this.loadPrenatalRecords()
      this.loadStatistics()
      this.$message.success('数据已刷新')
    },
    
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },
    
    getRiskTagType(riskLevel) {
      const types = {
        '低风险': 'success',
        '中风险': 'warning',
        '高风险': 'danger'
      }
      return types[riskLevel] || ''
    }
  }
}
</script>

<style lang="less" scoped>
.prenatal-care-container {
  padding: 20px;
  height: 100%;
  
  .prenatal-care-content {
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
    
    .detail-content {
      .detail-item {
        display: flex;
        margin-bottom: 10px;
        
        label {
          font-weight: bold;
          color: #666;
          width: 80px;
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
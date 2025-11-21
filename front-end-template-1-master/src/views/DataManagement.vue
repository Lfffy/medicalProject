<template>
  <div class="data-management-container">
    <dv-border-box-8 :dur="5">
      <div class="data-management-content">
        <!-- 页面头部 -->
        <div class="page-header">
          <div class="header-left">
            <div class="page-title">
              <i class="fas fa-database"></i>
              <h2>数据管理中心</h2>
            </div>
            <div class="page-description">
              统一管理医疗数据和孕产妇数据，支持数据的增删改查、批量操作和导出功能
            </div>
          </div>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-plus" @click="showAddDialog">
              新增数据
            </el-button>
            <el-button type="success" icon="el-icon-download" @click="exportData">
              导出数据
            </el-button>
          </div>
        </div>

        <!-- 数据统计卡片 -->
        <div class="stats-cards">
          <div class="stat-card medical">
            <div class="stat-icon">
              <i class="fas fa-heartbeat"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.medicalCount }}</div>
              <div class="stat-label">医疗数据</div>
            </div>
          </div>
          <div class="stat-card maternal">
            <div class="stat-icon">
              <i class="fas fa-baby"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.maternalCount }}</div>
              <div class="stat-label">孕产妇数据</div>
            </div>
          </div>
          <div class="stat-card total">
            <div class="stat-icon">
              <i class="fas fa-chart-bar"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalCount }}</div>
              <div class="stat-label">数据总量</div>
            </div>
          </div>
          <div class="stat-card today">
            <div class="stat-icon">
              <i class="fas fa-calendar-day"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.todayCount }}</div>
              <div class="stat-label">今日新增</div>
            </div>
          </div>
        </div>

        <!-- 筛选区域 -->
        <div class="filter-section">
          <div class="filter-header">
            <h3><i class="fas fa-filter"></i> 数据筛选</h3>
            <el-button type="text" @click="resetFilters">重置筛选</el-button>
          </div>
          <div class="filter-content">
            <el-row :gutter="20">
              <el-col :span="6">
                <el-select v-model="filters.dataType" placeholder="选择数据类型" clearable @change="handleFilterChange">
                  <el-option label="全部类型" value=""></el-option>
                  <el-option label="医疗数据" value="medical"></el-option>
                  <el-option label="孕产妇数据" value="maternal"></el-option>
                </el-select>
              </el-col>
              <el-col :span="8">
                <el-input v-model="filters.keyword" placeholder="搜索姓名、疾病类型等..." clearable @input="handleSearchChange">
                  <i slot="prefix" class="el-input__icon el-icon-search"></i>
                </el-input>
              </el-col>
              <el-col :span="10">
                <el-date-picker
                  v-model="filters.dateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  format="yyyy-MM-dd"
                  value-format="yyyy-MM-dd"
                  @change="handleFilterChange">
                </el-date-picker>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 数据表格区域 -->
        <div class="table-section">
          <div class="table-header">
            <div class="table-title">
              <h3><i class="fas fa-table"></i> 数据列表</h3>
              <span class="record-count">共 {{ pagination.total }} 条记录</span>
            </div>
            <div class="table-actions">
              <el-button-group>
                <el-button size="small" icon="el-icon-refresh" @click="loadData">刷新</el-button>
                <el-button size="small" icon="el-icon-s-grid" @click="toggleTableSize">调整列宽</el-button>
              </el-button-group>
            </div>
          </div>
          
          <el-table
            :data="tableData"
            style="width: 100%"
            v-loading="loading"
            element-loading-text="正在加载数据..."
            @row-click="handleRowClick"
            @selection-change="handleSelectionChange"
            :row-class-name="tableRowClassName"
            :default-sort="{ prop: 'created_at', order: 'descending' }"
            stripe>
            
            <el-table-column type="selection" width="55" align="center"></el-table-column>
            
            <el-table-column prop="id" label="ID" width="80" align="center">
              <template slot-scope="scope">
                <el-tag size="mini" type="info">{{ scope.row.id }}</el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="name" label="姓名" min-width="120" sortable>
              <template slot-scope="scope">
                <div class="name-cell">
                  <i :class="scope.row.data_type === 'medical' ? 'fas fa-user-md' : 'fas fa-pregnant'"></i>
                  <span>{{ scope.row.name }}</span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="data_type" label="数据类型" width="120" align="center">
              <template slot-scope="scope">
                <el-tag :type="scope.row.data_type === 'medical' ? 'primary' : 'success'" size="small">
                  {{ scope.row.data_type === 'medical' ? '医疗数据' : '孕产妇数据' }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="age" label="年龄" width="80" align="center" sortable>
              <template slot-scope="scope">
                <span class="age-text">{{ scope.row.age }}岁</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="gender" label="性别" width="80" align="center" v-if="showGenderColumn">
              <template slot-scope="scope">
                <i :class="scope.row.gender === '男' ? 'fas fa-mars' : 'fas fa-venus'" 
                   :style="{ color: scope.row.gender === '男' ? '#409EFF' : '#F56C6C' }"></i>
              </template>
            </el-table-column>
            
            <el-table-column prop="disease_type" label="疾病类型" min-width="120" v-if="showDiseaseColumn">
              <template slot-scope="scope">
                <el-tag size="mini" type="warning">{{ scope.row.disease_type }}</el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="gestational_weeks" label="孕周" width="80" align="center" v-if="showMaternalColumns">
              <template slot-scope="scope">
                <span class="gestational-weeks">{{ scope.row.gestational_weeks }}周</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="systolic_pressure" label="血压" width="100" align="center">
              <template slot-scope="scope">
                <div class="pressure-cell">
                  <span>{{ scope.row.systolic_pressure }}/{{ scope.row.diastolic_pressure }}</span>
                  <small>mmHg</small>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="created_at" label="创建时间" width="160" sortable>
              <template slot-scope="scope">
                <div class="time-cell">
                  <i class="fas fa-clock"></i>
                  <span>{{ formatDateTime(scope.row.created_at) }}</span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="200" align="center" fixed="right">
              <template slot-scope="scope">
                <div class="action-buttons">
                  <el-button size="mini" type="text" icon="el-icon-view" @click="showViewDialog(scope.row)">
                    查看
                  </el-button>
                  <el-button size="mini" type="text" icon="el-icon-edit" @click="editRecord(scope.row)">
                    编辑
                  </el-button>
                  <el-button size="mini" type="text" icon="el-icon-delete" @click="deleteRecord(scope.row)" 
                             style="color: #F56C6C;">
                    删除
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>

          <div class="batch-actions" v-if="selectedRecords.length > 0">
            <div class="batch-info">
              <i class="fas fa-check-circle"></i>
              <span>已选择 {{ selectedRecords.length }} 条记录</span>
            </div>
            <div class="batch-buttons">
              <el-button-group>
                <el-button size="small" type="primary" icon="el-icon-edit" @click="batchEdit">
                  批量编辑
                </el-button>
                <el-button size="small" type="success" icon="el-icon-download" @click="batchExport">
                  批量导出
                </el-button>
                <el-button size="small" type="danger" icon="el-icon-delete" @click="batchDelete">
                  批量删除
                </el-button>
              </el-button-group>
            </div>
          </div>

          <div class="pagination-section">
            <div class="pagination-info">
              <span>显示第 {{ (pagination.currentPage - 1) * pagination.pageSize + 1 }} 至 
                    {{ Math.min(pagination.currentPage * pagination.pageSize, pagination.total) }} 条记录，
                    共 {{ pagination.total }} 条</span>
            </div>
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="pagination.currentPage"
              :page-sizes="[10, 20, 50, 100]"
              :page-size="pagination.pageSize"
              layout="sizes, prev, pager, next, jumper"
              :total="pagination.total"
              background>
            </el-pagination>
          </div>
        </div>

        <!-- 新增/编辑对话框 -->
        <el-dialog
          :title="dialogTitle"
          :visible.sync="dialogVisible"
          width="80%"
          :close-on-click-modal="false"
        >
          <div class="dialog-content">
            <!-- 普通医疗数据表单 -->
            <div v-if="currentRecord.data_type === 'medical' || dialogMode === 'add'">
              <el-form :model="medicalForm" :rules="medicalRules" ref="medicalFormRef" label-width="120px">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="患者姓名" prop="name">
                      <el-input v-model="medicalForm.name" placeholder="请输入患者姓名"></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="性别" prop="gender">
                      <el-select v-model="medicalForm.gender" placeholder="请选择性别">
                        <el-option label="男" value="男"></el-option>
                        <el-option label="女" value="女"></el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="年龄" prop="age">
                      <el-input-number v-model="medicalForm.age" :min="0" :max="150" placeholder="请输入年龄"></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="疾病类型" prop="disease_type">
                      <el-select v-model="medicalForm.disease_type" placeholder="请选择疾病类型">
                        <el-option label="高血压" value="高血压"></el-option>
                        <el-option label="糖尿病" value="糖尿病"></el-option>
                        <el-option label="心脏病" value="心脏病"></el-option>
                        <el-option label="呼吸系统疾病" value="呼吸系统疾病"></el-option>
                        <el-option label="消化系统疾病" value="消化系统疾病"></el-option>
                        <el-option label="其他" value="其他"></el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="血压(收缩压)" prop="systolic_pressure">
                      <el-input-number v-model="medicalForm.systolic_pressure" :min="50" :max="250" placeholder="收缩压"></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="血压(舒张压)" prop="diastolic_pressure">
                      <el-input-number v-model="medicalForm.diastolic_pressure" :min="30" :max="150" placeholder="舒张压"></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="体重(kg)" prop="weight">
                      <el-input-number v-model="medicalForm.weight" :min="0" :max="300" :precision="1" placeholder="体重"></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="身高(cm)" prop="height">
                      <el-input-number v-model="medicalForm.height" :min="50" :max="250" placeholder="身高"></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-form-item label="症状描述" prop="symptoms">
                  <el-input type="textarea" v-model="medicalForm.symptoms" rows="3" placeholder="请描述患者症状"></el-input>
                </el-form-item>

                <el-form-item label="诊断结果" prop="diagnosis">
                  <el-input type="textarea" v-model="medicalForm.diagnosis" rows="3" placeholder="请输入诊断结果"></el-input>
                </el-form-item>

                <el-form-item label="治疗方案" prop="treatment">
                  <el-input type="textarea" v-model="medicalForm.treatment" rows="3" placeholder="请输入治疗方案"></el-input>
                </el-form-item>
              </el-form>
            </div>

            <!-- 孕产妇数据表单 -->
            <div v-if="currentRecord.data_type === 'maternal'">
              <el-form :model="maternalForm" :rules="maternalRules" ref="maternalFormRef" label-width="120px">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="孕妇姓名" prop="name">
                      <el-input v-model="maternalForm.name" placeholder="请输入孕妇姓名"></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="年龄" prop="age">
                      <el-input-number v-model="maternalForm.age" :min="15" :max="50" placeholder="请输入年龄"></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="孕周" prop="gestational_weeks">
                      <el-input-number v-model="maternalForm.gestational_weeks" :min="1" :max="42" placeholder="请输入孕周"></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="孕次" prop="pregnancy_count">
                      <el-input-number v-model="maternalForm.pregnancy_count" :min="1" :max="20" placeholder="请输入孕次"></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="产次" prop="parity">
                      <el-input-number v-model="maternalForm.parity" :min="0" :max="10" placeholder="请输入产次"></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="妊娠类型" prop="pregnancy_type">
                      <el-select v-model="maternalForm.pregnancy_type" placeholder="请选择妊娠类型">
                        <el-option label="单胎" value="单胎"></el-option>
                        <el-option label="双胎" value="双胎"></el-option>
                        <el-option label="多胎" value="多胎"></el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="体重(kg)" prop="weight">
                      <el-input-number v-model="maternalForm.weight" :min="30" :max="200" :precision="1" placeholder="体重"></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="身高(cm)" prop="height">
                      <el-input-number v-model="maternalForm.height" :min="140" :max="200" placeholder="身高"></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="收缩压" prop="systolic_pressure">
                      <el-input-number v-model="maternalForm.systolic_pressure" :min="60" :max="200" placeholder="收缩压"></el-input-number>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="舒张压" prop="diastolic_pressure">
                      <el-input-number v-model="maternalForm.diastolic_pressure" :min="40" :max="120" placeholder="舒张压"></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-form-item label="备注" prop="notes">
                  <el-input type="textarea" v-model="maternalForm.notes" rows="3" placeholder="请输入备注信息"></el-input>
                </el-form-item>
              </el-form>
            </div>
          </div>

          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveRecord" :loading="saving">保存</el-button>
          </div>
        </el-dialog>

        <!-- 查看详情对话框 -->
        <el-dialog title="数据详情" :visible.sync="viewDialogVisible" width="60%">
          <div v-if="viewRecordData" class="record-detail">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="姓名">{{ viewRecordData.name }}</el-descriptions-item>
              <el-descriptions-item label="数据类型">
                <el-tag :type="viewRecordData.data_type === 'medical' ? 'primary' : 'success'">
                  {{ viewRecordData.data_type === 'medical' ? '医疗数据' : '孕产妇数据' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="年龄">{{ viewRecordData.age }}</el-descriptions-item>
              <el-descriptions-item label="性别" v-if="viewRecordData.gender">{{ viewRecordData.gender }}</el-descriptions-item>
              <el-descriptions-item label="疾病类型" v-if="viewRecordData.disease_type">{{ viewRecordData.disease_type }}</el-descriptions-item>
              <el-descriptions-item label="孕周" v-if="viewRecordData.gestational_weeks">{{ viewRecordData.gestational_weeks }}</el-descriptions-item>
              <el-descriptions-item label="收缩压">{{ viewRecordData.systolic_pressure }}</el-descriptions-item>
              <el-descriptions-item label="舒张压">{{ viewRecordData.diastolic_pressure }}</el-descriptions-item>
              <el-descriptions-item label="体重">{{ viewRecordData.weight }}</el-descriptions-item>
              <el-descriptions-item label="身高" v-if="viewRecordData.height">{{ viewRecordData.height }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{ formatDateTime(viewRecordData.created_at) }}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{ formatDateTime(viewRecordData.updated_at) }}</el-descriptions-item>
            </el-descriptions>
            
            <div v-if="viewRecordData.symptoms" class="detail-section">
              <h4>症状描述</h4>
              <p>{{ viewRecordData.symptoms }}</p>
            </div>
            
            <div v-if="viewRecordData.diagnosis" class="detail-section">
              <h4>诊断结果</h4>
              <p>{{ viewRecordData.diagnosis }}</p>
            </div>
            
            <div v-if="viewRecordData.treatment" class="detail-section">
              <h4>治疗方案</h4>
              <p>{{ viewRecordData.treatment }}</p>
            </div>
            
            <div v-if="viewRecordData.notes" class="detail-section">
              <h4>备注</h4>
              <p>{{ viewRecordData.notes }}</p>
            </div>
          </div>
        </el-dialog>
    
    <!-- 数据详情对话框 -->
    <el-dialog title="数据详情" :visible.sync="detailDialogVisible" width="60%" class="detail-dialog">
      <div v-if="currentRecord" class="record-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="数据ID">{{ currentRecord.id }}</el-descriptions-item>
          <el-descriptions-item label="数据类型">
            <el-tag :type="currentRecord.data_type === 'medical' ? 'primary' : 'success'">
              {{ currentRecord.data_type === 'medical' ? '医疗数据' : '孕产妇数据' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="姓名">{{ currentRecord.name }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ currentRecord.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ currentRecord.age }}岁</el-descriptions-item>
          <el-descriptions-item label="记录时间">{{ currentRecord.record_time }}</el-descriptions-item>
          
          <template v-if="currentRecord.data_type === 'medical'">
            <el-descriptions-item label="疾病类型">{{ currentRecord.disease_type }}</el-descriptions-item>
            <el-descriptions-item label="收缩压">{{ currentRecord.systolic_pressure }} mmHg</el-descriptions-item>
            <el-descriptions-item label="舒张压">{{ currentRecord.diastolic_pressure }} mmHg</el-descriptions-item>
            <el-descriptions-item label="心率">{{ currentRecord.heart_rate }} bpm</el-descriptions-item>
            <el-descriptions-item label="血糖">{{ currentRecord.blood_sugar }} mmol/L</el-descriptions-item>
            <el-descriptions-item label="体温">{{ currentRecord.body_temperature }}°C</el-descriptions-item>
          </template>
          
          <template v-else>
            <el-descriptions-item label="孕周">{{ currentRecord.gestational_weeks }}周</el-descriptions-item>
            <el-descriptions-item label="产次">{{ currentRecord.parity }}</el-descriptions-item>
            <el-descriptions-item label="宫高">{{ currentRecord.fundal_height }} cm</el-descriptions-item>
            <el-descriptions-item label="腹围">{{ currentRecord.abdominal_circumference }} cm</el-descriptions-item>
            <el-descriptions-item label="胎心率">{{ currentRecord.fetal_heart_rate }} bpm</el-descriptions-item>
            <el-descriptions-item label="体重">{{ currentRecord.weight }} kg</el-descriptions-item>
          </template>
          
          <el-descriptions-item label="备注" :span="2">{{ currentRecord.notes || '无' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEdit(currentRecord)">编辑</el-button>
      </div>
    </el-dialog>
  </div>
    </dv-border-box-8>
  </div>
</template>

<script>
export default {
  name: 'DataManagement',
  data() {
    return {
      loading: false,
      saving: false,
      tableData: [],
      selectedRecords: [],
      dialogVisible: false,
      viewDialogVisible: false,
      detailDialogVisible: false,
      dialogMode: 'add', // add, edit
      currentRecord: {},
      viewRecordData: null,
      
      // 搜索防抖定时器
      searchTimer: null,
      
      // 统计数据
      stats: {
        medicalCount: 0,
        maternalCount: 0,
        totalCount: 0,
        todayCount: 0
      },
      
      // 筛选条件
      filters: {
        dataType: '',
        keyword: '',
        dateRange: []
      },
      
      // 分页
      pagination: {
        currentPage: 1,
        pageSize: 20,
        total: 0
      },
      
      // 表单数据
      medicalForm: {
        name: '',
        gender: '',
        age: null,
        disease_type: '',
        systolic_pressure: null,
        diastolic_pressure: null,
        weight: null,
        height: null,
        symptoms: '',
        diagnosis: '',
        treatment: ''
      },
      
      maternalForm: {
        name: '',
        age: null,
        gestational_weeks: null,
        pregnancy_count: null,
        parity: null,
        pregnancy_type: '',
        weight: null,
        height: null,
        systolic_pressure: null,
        diastolic_pressure: null,
        notes: ''
      },
      
      // 表单验证规则
      medicalRules: {
        name: [
          { required: true, message: '请输入患者姓名', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        disease_type: [
          { required: true, message: '请选择疾病类型', trigger: 'change' }
        ]
      },
      
      maternalRules: {
        name: [
          { required: true, message: '请输入孕妇姓名', trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        gestational_weeks: [
          { required: true, message: '请输入孕周', trigger: 'blur' }
        ],
        pregnancy_count: [
          { required: true, message: '请输入孕次', trigger: 'blur' }
        ],
        parity: [
          { required: true, message: '请输入产次', trigger: 'blur' }
        ],
        pregnancy_type: [
          { required: true, message: '请选择妊娠类型', trigger: 'change' }
        ]
      }
    }
  },
  
  computed: {
    dialogTitle() {
      return this.dialogMode === 'add' ? '新增数据' : '编辑数据';
    },
    
    showGenderColumn() {
      return this.tableData.some(record => record.data_type === 'medical');
    },
    
    showDiseaseColumn() {
      return this.tableData.some(record => record.data_type === 'medical');
    },
    
    showMaternalColumns() {
      return this.tableData.some(record => record.data_type === 'maternal');
    }
  },
  
  methods: {
    loadData() {
      this.loading = true;
      const params = {
        page: this.pagination.currentPage,
        size: this.pagination.pageSize,
        data_type: this.filters.dataType,
        keyword: this.filters.keyword,
        start_date: this.filters.dateRange?.[0],
        end_date: this.filters.dateRange?.[1]
      };
      
      this.$http.get('/api/data/list', { params })
        .then(response => {
          if (response.data && response.data.data) {
            this.tableData = response.data.data;
            this.pagination.total = response.data.total || 0;
            
            // 如果没有数据，显示友好提示
            if (this.tableData.length === 0) {
              this.$message.info('暂无符合条件的数据');
            }
          } else {
            this.tableData = [];
            this.pagination.total = 0;
            this.$message.warning('数据格式异常');
          }
        })
        .catch(error => {
          console.error('加载数据失败:', error);
          this.tableData = [];
          this.pagination.total = 0;
          
          // 根据错误类型显示不同的提示
          if (error.response) {
            if (error.response.status === 401) {
              this.$message.error('登录已过期，请重新登录');
            } else if (error.response.status === 403) {
              this.$message.error('权限不足，无法访问数据');
            } else if (error.response.status >= 500) {
              this.$message.error('服务器错误，请稍后重试');
            } else {
              this.$message.error('加载数据失败：' + (error.response.data?.message || error.message));
            }
          } else if (error.request) {
            this.$message.error('网络连接失败，请检查网络设置');
          } else {
            this.$message.error('加载数据失败：' + error.message);
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    handleFilterChange() {
      this.pagination.currentPage = 1;
      this.loadData();
    },
    
    // 带防抖的搜索
    handleSearchChange() {
      if (this.searchTimer) {
        clearTimeout(this.searchTimer);
      }
      this.searchTimer = setTimeout(() => {
        this.handleFilterChange();
      }, 500);
    },
    
    resetFilters() {
      this.filters = {
        dataType: '',
        keyword: '',
        dateRange: []
      };
      this.handleFilterChange();
    },
    
    handleSelectionChange(selection) {
      this.selectedRecords = selection;
    },
    
    // 处理表格行点击事件
    handleRowClick(row, column, event) {
      // 如果点击的是操作列，不触发详情查看
      if (column.property === 'operation') {
        return;
      }
      this.showDetailDialog(row);
    },
    
    // 显示详情对话框
    showDetailDialog(row) {
      this.currentRecord = { ...row };
      this.detailDialogVisible = true;
    },
    
    handleSizeChange(size) {
      this.pagination.pageSize = size;
      this.loadData();
    },
    
    handleCurrentChange(page) {
      this.pagination.currentPage = page;
      this.loadData();
    },
    
    showAddDialog() {
      this.dialogMode = 'add';
      this.currentRecord = { data_type: 'medical' };
      this.resetForms();
      this.dialogVisible = true;
    },
    
    showViewDialog(record) {
      this.viewRecordData = record;
      this.viewDialogVisible = true;
    },
    
    editRecord(record) {
      this.dialogMode = 'edit';
      this.currentRecord = { ...record };
      this.loadFormData();
      this.dialogVisible = true;
    },
    
    deleteRecord(record) {
      this.$confirm('确定要删除这条记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http.delete(`/api/data/${record.id}`)
          .then(response => {
            this.$message.success('删除成功');
            this.loadData();
          })
          .catch(error => {
            this.$message.error('删除失败：' + error.message);
          });
      });
    },
    
    batchDelete() {
      this.$confirm(`确定要删除选中的 ${this.selectedRecords.length} 条记录吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const ids = this.selectedRecords.map(record => record.id);
        this.$http.delete('/api/data/batch', { data: { ids } })
          .then(response => {
            this.$message.success('批量删除成功');
            this.loadData();
          })
          .catch(error => {
            this.$message.error('批量删除失败：' + error.message);
          });
      });
    },
    
    exportData() {
      const params = {
        data_type: this.filters.dataType,
        keyword: this.filters.keyword,
        start_date: this.filters.dateRange?.[0],
        end_date: this.filters.dateRange?.[1]
      };
      
      this.$http.get('/api/data/export', { 
        params,
        responseType: 'blob'
      })
      .then(response => {
        const blob = new Blob([response.data]);
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = `数据导出_${new Date().toISOString().slice(0, 10)}.xlsx`;
        link.click();
      })
      .catch(error => {
        this.$message.error('导出失败：' + error.message);
      });
    },
    
    batchExport() {
      const ids = this.selectedRecords.map(record => record.id);
      this.$http.post('/api/data/batch-export', { ids }, {
        responseType: 'blob'
      })
      .then(response => {
        const blob = new Blob([response.data]);
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = `批量导出_${new Date().toISOString().slice(0, 10)}.xlsx`;
        link.click();
      })
      .catch(error => {
        this.$message.error('批量导出失败：' + error.message);
      });
    },
    
    saveRecord() {
      const formRef = this.currentRecord.data_type === 'medical' ? 'medicalFormRef' : 'maternalFormRef';
      const formData = this.currentRecord.data_type === 'medical' ? this.medicalForm : this.maternalForm;
      
      this.$refs[formRef].validate((valid) => {
        if (valid) {
          this.saving = true;
          
          const url = this.dialogMode === 'add' 
            ? `/api/data/${this.currentRecord.data_type}/add`
            : `/api/data/${this.currentRecord.id}`;
            
          const method = this.dialogMode === 'add' ? 'post' : 'put';
          
          this.$http[method](url, formData)
            .then(response => {
              this.$message.success(this.dialogMode === 'add' ? '新增成功' : '更新成功');
              this.dialogVisible = false;
              this.loadData();
            })
            .catch(error => {
              this.$message.error('保存失败：' + (error.response?.data?.message || error.message));
            })
            .finally(() => {
              this.saving = false;
            });
        }
      });
    },
    
    loadFormData() {
      if (this.currentRecord.data_type === 'medical') {
        Object.assign(this.medicalForm, this.currentRecord);
      } else {
        Object.assign(this.maternalForm, this.currentRecord);
      }
    },
    
    resetForms() {
      this.$refs.medicalFormRef?.resetFields();
      this.$refs.maternalFormRef?.resetFields();
    },
    
    formatDateTime(dateTime) {
      if (!dateTime) return '-';
      return new Date(dateTime).toLocaleString();
    },
    
    // 新增方法
    tableRowClassName({row, rowIndex}) {
      if (row.data_type === 'medical') {
        return 'medical-row';
      } else if (row.data_type === 'maternal') {
        return 'maternal-row';
      }
      return '';
    },
    
    toggleTableSize() {
      // 这里可以实现表格列宽调整逻辑
      this.$message.info('表格列宽调整功能开发中...');
    },
    
    batchEdit() {
      if (this.selectedRecords.length === 0) {
        this.$message.warning('请先选择要编辑的记录');
        return;
      }
      // 这里可以实现批量编辑逻辑
      this.$message.info(`批量编辑 ${this.selectedRecords.length} 条记录功能开发中...`);
    },
    
    // 获取统计数据的方法
    getStatistics() {
      this.$http.get('/api/data/statistics')
        .then(response => {
          if (response.data && response.data.success) {
            const data = response.data.data;
            this.stats = {
              medicalCount: data.medical?.total || 0,
              maternalCount: data.maternal?.total || 0,
              totalCount: (data.medical?.total || 0) + (data.maternal?.total || 0),
              todayCount: (data.medical?.today || 0) + (data.maternal?.today || 0)
            };
          }
        })
        .catch(error => {
          console.error('获取统计数据失败:', error);
          // 设置默认值
          this.stats = {
            medicalCount: 0,
            maternalCount: 0,
            totalCount: 0,
            todayCount: 0
          };
        });
    },
    
    // 键盘快捷键处理
    handleKeyDown(event) {
      // Ctrl+N: 新增数据
      if (event.ctrlKey && event.key === 'n') {
        event.preventDefault();
        this.showAddDialog();
      }
      // Ctrl+F: 聚焦搜索框
      else if (event.ctrlKey && event.key === 'f') {
        event.preventDefault();
        this.$nextTick(() => {
          const searchInput = document.querySelector('.el-input__inner');
          if (searchInput) {
            searchInput.focus();
          }
        });
      }
      // F5: 刷新数据
      else if (event.key === 'F5') {
        event.preventDefault();
        this.loadData();
      }
    }
  },
  
  mounted() {
    this.loadData();
    this.getStatistics();
    // 添加键盘快捷键支持
    document.addEventListener('keydown', this.handleKeyDown);
  },
  
  beforeDestroy() {
    // 清理定时器和事件监听
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }
    document.removeEventListener('keydown', this.handleKeyDown);
  },
}
</script>

<style lang="less" scoped>
.data-management-container {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* 页面头部样式 */
.page-header {
  background: linear-gradient(135deg, #ff69b4 0%, #ff66a3 100%);
  color: white;
  padding: 24px 32px;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(255, 105, 180, 0.3);

  h1 {
    margin: 0 0 8px 0;
    font-size: 28px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 12px;

    i {
      font-size: 24px;
    }
  }

  p {
    margin: 0;
    opacity: 0.9;
    font-size: 14px;
  }
}

/* 统计卡片样式 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 4px solid transparent;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(255, 105, 180, 0.3);
  }

  &.medical {
    border-left-color: #409EFF;
  }

  &.maternal {
    border-left-color: #ff69b4;
  }

  &.total {
    border-left-color: #67C23A;
  }

  &.today {
    border-left-color: #E6A23C;
  }
}

.stat-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.stat-card-title {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.stat-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;

  .stat-card.medical & {
    background: linear-gradient(135deg, #409EFF, #66B3FF);
  }

  .stat-card.maternal & {
    background: linear-gradient(135deg, #67C23A, #85CE61);
  }

  .stat-card.total & {
    background: linear-gradient(135deg, #E6A23C, #EEBE77);
  }

  .stat-card.today & {
    background: linear-gradient(135deg, #F56C6C, #F78989);
  }
}

.stat-card-value {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 8px;
}

.stat-card-change {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;

  &.positive {
    color: #67C23A;
  }

  &.negative {
    color: #F56C6C;
  }
}

/* 筛选区域样式 */
.filter-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 105, 180, 0.2);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  h3 {
    margin: 0;
    font-size: 18px;
    color: #303133;
    display: flex;
    align-items: center;
    gap: 8px;

    i {
      color: #409EFF;
    }
  }
}

.filter-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  align-items: end;
}

.filter-actions {
  display: flex;
  gap: 8px;
}

/* 表格区域样式 */
.table-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 105, 180, 0.2);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 12px;

  h3 {
    margin: 0;
    font-size: 18px;
    color: #303133;

    i {
      color: #409EFF;
    }
  }
}

.record-count {
  font-size: 14px;
  color: #909399;
  background: #F4F4F5;
  padding: 4px 8px;
  border-radius: 4px;
}

/* 表格单元格样式 */
.name-cell {
  display: flex;
  align-items: center;
  gap: 8px;

  i {
    color: #409EFF;
  }
}

.age-text {
  font-weight: 600;
  color: #606266;
}

.gestational-weeks {
  font-weight: 600;
  color: #67C23A;
}

.pressure-cell {
  display: flex;
  flex-direction: column;
  align-items: center;

  span {
    font-weight: 600;
    color: #303133;
  }

  small {
    color: #909399;
    font-size: 10px;
  }
}

.time-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;

  i {
    color: #909399;
  }
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

/* 批量操作区域样式 */
.batch-actions {
  background: linear-gradient(135deg, #E8F4FD 0%, #F0F9FF 100%);
  border: 1px solid #B3D8FF;
  border-radius: 8px;
  padding: 16px;
  margin: 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409EFF;
  font-weight: 500;

  i {
    font-size: 16px;
  }
}

/* 分页区域样式 */
.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
}

.pagination-info {
  font-size: 14px;
  color: #606266;
}

/* 对话框样式增强 */
::v-deep .el-dialog {
  border-radius: 12px;
}

::v-deep .el-dialog__header {
  background: linear-gradient(135deg, #ff69b4 0%, #ff66a3 100%);
  color: white;
  padding: 20px 24px;
  border-radius: 12px 12px 0 0;
}

::v-deep .el-dialog__title {
  color: white;
  font-weight: 600;
}

::v-deep .el-dialog__headerbtn .el-dialog__close {
  color: white;
}

::v-deep .el-form-item__label {
  font-weight: 500;
  color: #303133;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .data-management-container {
    padding: 16px;
  }
  
  .page-header {
    padding: 20px;
    
    h1 {
      font-size: 24px;
    }
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .filter-content {
    grid-template-columns: 1fr;
  }
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .pagination-section {
    flex-direction: column;
    gap: 16px;
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 12px;
  }
}

/* 加载动画 */
::v-deep .el-loading-mask {
  background-color: rgba(255, 255, 255, 0.9);
}

::v-deep .el-loading-spinner {
  margin-top: -20px;
}

/* 表格行样式 */
::v-deep .medical-row {
  background-color: rgba(64, 158, 255, 0.02);
}

::v-deep .maternal-row {
  background-color: rgba(103, 194, 58, 0.02);
}

::v-deep .el-table__row {
  transition: all 0.3s ease;
}

::v-deep .el-table__row:hover {
  transform: scale(1.001);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 按钮悬停效果 */
::v-deep .el-button:hover {
  transform: translateY(-1px);
}

/* 表格头部样式 */
::v-deep .el-table__header-wrapper {
  background: #F8F9FA;
}

::v-deep .el-table__header th {
  background: #F8F9FA !important;
  color: #303133;
  font-weight: 600;
}

/* Element UI 组件样式覆盖 */
::v-deep .el-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

::v-deep .el-button--primary {
  background: linear-gradient(135deg, #ff69b4 0%, #ff66a3 100%);
  border: none;
}

::v-deep .el-button--success {
  background: linear-gradient(135deg, #67C23A, #85CE61);
  border: none;
}

::v-deep .el-button--danger {
  background: linear-gradient(135deg, #F56C6C, #F78989);
  border: none;
}

::v-deep .el-button--warning {
  background: linear-gradient(135deg, #E6A23C, #EEBE77);
  border: none;
}

::v-deep .el-pagination.is-background .el-pager li:not(.disabled).active {
  background: linear-gradient(135deg, #ff69b4 0%, #ff66a3 100%);
}

/* 记录详情样式 */
.record-detail {
  .el-descriptions {
    .el-descriptions__body {
      background: rgba(255, 255, 255, 0.02);
    }
    
    .el-descriptions-item__label {
      background: rgba(0, 123, 255, 0.1);
      color: #007bff;
      font-weight: 600;
    }
    
    .el-descriptions-item__content {
      color: #fff;
      font-weight: 500;
    }
  }
}

/* 详情对话框样式 */
.detail-dialog {
  .el-dialog {
    background: linear-gradient(135deg, rgba(10, 25, 47, 0.95) 0%, rgba(20, 35, 60, 0.95) 100%);
    border: 1px solid rgba(0, 123, 255, 0.3);
    
    .el-dialog__header {
      background: rgba(0, 123, 255, 0.1);
      border-bottom: 1px solid rgba(0, 123, 255, 0.2);
      
      .el-dialog__title {
        color: #fff;
        font-weight: 600;
      }
    }
    
    .el-dialog__body {
      background: transparent;
    }
  }
}
</style>
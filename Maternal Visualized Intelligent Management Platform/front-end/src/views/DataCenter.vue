<template>
  <div class="data-center-container">
    <dv-border-box-8 :dur="5">
      <div class="data-center-content">
        <!-- 页面头部 -->
        <div class="header">
          <h2>数据中心</h2>
          <div class="header-actions">
            <el-button-group>
              <el-button 
                :type="activeTab === 'management' ? 'primary' : 'default'"
                @click="switchTab('management')"
                icon="el-icon-document"
              >
                数据管理
              </el-button>
              <el-button 
                :type="activeTab === 'entry' ? 'primary' : 'default'"
                @click="switchTab('entry')"
                icon="el-icon-edit"
              >
                数据录入
              </el-button>
              <el-button 
                :type="activeTab === 'import' ? 'primary' : 'default'"
                @click="switchTab('import')"
                icon="el-icon-upload"
              >
                数据导入
              </el-button>
              <el-button 
                :type="activeTab === 'table' ? 'primary' : 'default'"
                @click="switchTab('table')"
                icon="el-icon-s-grid"
              >
                数据表格
              </el-button>
            </el-button-group>
            <el-button type="success" icon="el-icon-download" @click="exportData">导出数据</el-button>
          </div>
        </div>

        <!-- 数据管理页面 -->
        <div v-show="activeTab === 'management'" class="tab-content">
          <div class="filter-section">
            <el-row :gutter="20">
              <el-col :span="6">
                <el-select v-model="filters.dataType" placeholder="数据类型" @change="handleFilterChange">
                  <el-option label="全部" value=""></el-option>
                  <el-option label="普通医疗数据" value="medical"></el-option>
                  <el-option label="孕产妇数据" value="maternal"></el-option>
                </el-select>
              </el-col>
              <el-col :span="6">
                <el-input v-model="filters.keyword" placeholder="搜索姓名/疾病类型" @keyup.enter="handleFilterChange">
                  <i slot="prefix" class="el-input__icon el-icon-search"></i>
                </el-input>
              </el-col>
              <el-col :span="6">
                <el-date-picker
                  v-model="filters.dateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  @change="handleFilterChange"
                ></el-date-picker>
              </el-col>
              <el-col :span="6">
                <el-button type="primary" @click="handleFilterChange">搜索</el-button>
                <el-button @click="resetFilters">重置</el-button>
              </el-col>
            </el-row>
          </div>

          <div class="table-section">
            <el-table
              :data="tableData"
              border
              style="width: 100%"
              v-loading="loading"
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection" width="55"></el-table-column>
              <el-table-column prop="id" label="ID" width="80"></el-table-column>
              <el-table-column prop="name" label="姓名" width="120"></el-table-column>
              <el-table-column prop="data_type" label="数据类型" width="120">
                <template slot-scope="scope">
                  <el-tag :type="scope.row.data_type === 'medical' ? 'primary' : 'success'">
                    {{ scope.row.data_type === 'medical' ? '医疗数据' : '孕产妇数据' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="age" label="年龄" width="80"></el-table-column>
              <el-table-column prop="gender" label="性别" width="80" v-if="showGenderColumn"></el-table-column>
              <el-table-column prop="disease_type" label="疾病类型" width="120" v-if="showDiseaseColumn"></el-table-column>
              <el-table-column prop="gestational_weeks" label="孕周" width="80" v-if="showMaternalColumns"></el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template slot-scope="scope">
                  {{ formatDateTime(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template slot-scope="scope">
                  <el-button size="mini" @click="viewRecord(scope.row)">查看</el-button>
                  <el-button size="mini" type="primary" @click="editRecord(scope.row)">编辑</el-button>
                  <el-button size="mini" type="danger" @click="deleteRecord(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="pagination">
              <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="pagination.currentPage"
                :page-sizes="[10, 20, 50, 100]"
                :page-size="pagination.pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="pagination.total"
              ></el-pagination>
            </div>
          </div>
        </div>

        <!-- 数据录入页面 -->
        <div v-show="activeTab === 'entry'" class="tab-content">
          <div class="entry-form-container">
            <el-row :gutter="20">
              <!-- 数据类型选择 -->
              <el-col :span="24">
                <el-card class="data-type-selector">
                  <h3>选择数据类型</h3>
                  <el-radio-group v-model="entryForm.dataType" @change="handleDataTypeChange">
                    <el-radio-button label="medical">普通医疗数据</el-radio-button>
                    <el-radio-button label="maternal">孕产妇数据</el-radio-button>
                  </el-radio-group>
                </el-card>
              </el-col>

              <!-- 普通医疗数据表单 -->
              <el-col :span="24" v-if="entryForm.dataType === 'medical'">
                <el-card>
                  <h3>医疗数据录入</h3>
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
                        <el-form-item label="收缩压" prop="systolic_pressure">
                          <el-input-number v-model="medicalForm.systolic_pressure" :min="50" :max="250" placeholder="收缩压"></el-input-number>
                        </el-form-item>
                      </el-col>
                      <el-col :span="12">
                        <el-form-item label="舒张压" prop="diastolic_pressure">
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

                    <el-form-item>
                      <el-button type="primary" @click="submitMedicalData" :loading="submitting">提交数据</el-button>
                      <el-button @click="resetMedicalForm">重置</el-button>
                    </el-form-item>
                  </el-form>
                </el-card>
              </el-col>

              <!-- 孕产妇数据表单 -->
              <el-col :span="24" v-if="entryForm.dataType === 'maternal'">
                <el-card>
                  <h3>孕产妇数据录入</h3>
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
                          <el-input-number v-model="maternalForm.gestational_weeks" :min="1" :max="42" placeholder="孕周"></el-input-number>
                        </el-form-item>
                      </el-col>
                      <el-col :span="12">
                        <el-form-item label="风险等级" prop="risk_level">
                          <el-select v-model="maternalForm.risk_level" placeholder="请选择风险等级">
                            <el-option label="低风险" value="低风险"></el-option>
                            <el-option label="中风险" value="中风险"></el-option>
                            <el-option label="高风险" value="高风险"></el-option>
                          </el-select>
                        </el-form-item>
                      </el-col>
                    </el-row>

                    <el-row :gutter="20">
                      <el-col :span="8">
                        <el-form-item label="收缩压" prop="systolic_pressure">
                          <el-input-number v-model="maternalForm.systolic_pressure" :min="50" :max="250" placeholder="收缩压"></el-input-number>
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item label="舒张压" prop="diastolic_pressure">
                          <el-input-number v-model="maternalForm.diastolic_pressure" :min="30" :max="150" placeholder="舒张压"></el-input-number>
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item label="体重(kg)" prop="weight">
                          <el-input-number v-model="maternalForm.weight" :min="30" :max="200" :precision="1" placeholder="体重"></el-input-number>
                        </el-form-item>
                      </el-col>
                    </el-row>

                    <el-form-item label="孕期症状" prop="symptoms">
                      <el-input type="textarea" v-model="maternalForm.symptoms" rows="3" placeholder="请描述孕期症状"></el-input>
                    </el-form-item>

                    <el-form-item label="检查结果" prop="examination_result">
                      <el-input type="textarea" v-model="maternalForm.examination_result" rows="3" placeholder="请输入检查结果"></el-input>
                    </el-form-item>

                    <el-form-item>
                      <el-button type="primary" @click="submitMaternalData" :loading="submitting">提交数据</el-button>
                      <el-button @click="resetMaternalForm">重置</el-button>
                    </el-form-item>
                  </el-form>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 数据导入页面 -->
        <div v-show="activeTab === 'import'" class="tab-content">
          <div class="import-container">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card>
                  <h3>文件上传</h3>
                  <el-upload
                    class="upload-demo"
                    drag
                    action="/api/data/import"
                    :on-success="handleUploadSuccess"
                    :on-error="handleUploadError"
                    :before-upload="beforeUpload"
                    :file-list="fileList"
                  >
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">只能上传xlsx/xls/csv文件，且不超过10MB</div>
                  </el-upload>
                </el-card>
              </el-col>
              
              <el-col :span="12">
                <el-card>
                  <h3>导入说明</h3>
                  <div class="import-instructions">
                    <h4>支持的数据格式：</h4>
                    <ul>
                      <li>Excel文件 (.xlsx, .xls)</li>
                      <li>CSV文件 (.csv)</li>
                    </ul>
                    
                    <h4>数据字段要求：</h4>
                    <ul>
                      <li>普通医疗数据：姓名、性别、年龄、疾病类型、血压、体重、身高等</li>
                      <li>孕产妇数据：姓名、年龄、孕周、风险等级、血压、体重、症状等</li>
                    </ul>
                    
                    <h4>注意事项：</h4>
                    <ul>
                      <li>请确保数据格式正确</li>
                      <li>重复数据将被覆盖</li>
                      <li>导入前建议备份数据</li>
                    </ul>
                  </div>
                </el-card>
              </el-col>
            </el-row>

            <el-row v-if="importHistory.length > 0">
              <el-col :span="24">
                <el-card>
                  <h3>导入历史</h3>
                  <el-table :data="importHistory" border>
                    <el-table-column prop="filename" label="文件名"></el-table-column>
                    <el-table-column prop="upload_time" label="上传时间"></el-table-column>
                    <el-table-column prop="status" label="状态">
                      <template slot-scope="scope">
                        <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
                          {{ scope.row.status === 'success' ? '成功' : '失败' }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="records_count" label="记录数"></el-table-column>
                    <el-table-column prop="message" label="说明"></el-table-column>
                  </el-table>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 数据表格页面 -->
        <div v-show="activeTab === 'table'" class="tab-content">
          <div class="table-view-container">
            <el-row :gutter="20">
              <el-col :span="24">
                <el-card>
                  <div slot="header" class="clearfix">
                    <span>数据表格视图</span>
                    <el-button-group style="float: right;">
                      <el-button size="small" icon="el-icon-refresh" @click="refreshTableData">刷新</el-button>
                      <el-button size="small" icon="el-icon-download" @click="exportTableData">导出</el-button>
                    </el-button-group>
                  </div>
                  
                  <el-table
                    :data="tableData"
                    border
                    stripe
                    style="width: 100%"
                    height="600"
                    v-loading="loading"
                  >
                    <el-table-column prop="id" label="ID" width="80" fixed></el-table-column>
                    <el-table-column prop="name" label="姓名" width="120" fixed></el-table-column>
                    <el-table-column prop="data_type" label="数据类型" width="120">
                      <template slot-scope="scope">
                        <el-tag :type="scope.row.data_type === 'medical' ? 'primary' : 'success'">
                          {{ scope.row.data_type === 'medical' ? '医疗数据' : '孕产妇数据' }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="age" label="年龄" width="80"></el-table-column>
                    <el-table-column prop="gender" label="性别" width="80" v-if="showGenderColumn"></el-table-column>
                    <el-table-column prop="disease_type" label="疾病类型" width="120" v-if="showDiseaseColumn"></el-table-column>
                    <el-table-column prop="gestational_weeks" label="孕周" width="80" v-if="showMaternalColumns"></el-table-column>
                    <el-table-column prop="systolic_pressure" label="收缩压" width="100"></el-table-column>
                    <el-table-column prop="diastolic_pressure" label="舒张压" width="100"></el-table-column>
                    <el-table-column prop="weight" label="体重" width="80"></el-table-column>
                    <el-table-column prop="height" label="身高" width="80" v-if="showGenderColumn"></el-table-column>
                    <el-table-column prop="symptoms" label="症状描述" width="200" show-overflow-tooltip></el-table-column>
                    <el-table-column prop="diagnosis" label="诊断结果" width="200" show-overflow-tooltip v-if="showDiseaseColumn"></el-table-column>
                    <el-table-column prop="examination_result" label="检查结果" width="200" show-overflow-tooltip v-if="showMaternalColumns"></el-table-column>
                    <el-table-column prop="created_at" label="创建时间" width="180">
                      <template slot-scope="scope">
                        {{ formatDateTime(scope.row.created_at) }}
                      </template>
                    </el-table-column>
                  </el-table>

                  <div class="pagination">
                    <el-pagination
                      @size-change="handleSizeChange"
                      @current-change="handleCurrentChange"
                      :current-page="pagination.currentPage"
                      :page-sizes="[20, 50, 100, 200]"
                      :page-size="pagination.pageSize"
                      layout="total, sizes, prev, pager, next, jumper"
                      :total="pagination.total"
                    ></el-pagination>
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


export default {
  name: 'DataCenter',
  data() {
    return {
      activeTab: 'management',
      loading: false,
      submitting: false,
      
      // 筛选条件
      filters: {
        dataType: '',
        keyword: '',
        dateRange: null
      },
      
      // 分页
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      
      // 表格数据
      tableData: [],
      selectedRecords: [],
      
      // 数据录入表单
      entryForm: {
        dataType: 'medical'
      },
      
      // 医疗数据表单
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
        diagnosis: ''
      },
      
      medicalRules: {
        name: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
        gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
        age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
        disease_type: [{ required: true, message: '请选择疾病类型', trigger: 'change' }],
        systolic_pressure: [{ required: true, message: '请输入收缩压', trigger: 'blur' }],
        diastolic_pressure: [{ required: true, message: '请输入舒张压', trigger: 'blur' }],
        weight: [{ required: true, message: '请输入体重', trigger: 'blur' }],
        height: [{ required: true, message: '请输入身高', trigger: 'blur' }]
      },
      
      // 孕产妇数据表单
      maternalForm: {
        name: '',
        age: null,
        gestational_weeks: null,
        risk_level: '',
        systolic_pressure: null,
        diastolic_pressure: null,
        weight: null,
        symptoms: '',
        examination_result: ''
      },
      
      maternalRules: {
        name: [{ required: true, message: '请输入孕妇姓名', trigger: 'blur' }],
        age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
        gestational_weeks: [{ required: true, message: '请输入孕周', trigger: 'blur' }],
        risk_level: [{ required: true, message: '请选择风险等级', trigger: 'change' }],
        systolic_pressure: [{ required: true, message: '请输入收缩压', trigger: 'blur' }],
        diastolic_pressure: [{ required: true, message: '请输入舒张压', trigger: 'blur' }],
        weight: [{ required: true, message: '请输入体重', trigger: 'blur' }]
      },
      
      // 文件上传
      fileList: [],
      importHistory: []
    }
  },
  
  computed: {
    showGenderColumn() {
      return this.tableData.some(item => item.data_type === 'medical')
    },
    showDiseaseColumn() {
      return this.tableData.some(item => item.data_type === 'medical')
    },
    showMaternalColumns() {
      return this.tableData.some(item => item.data_type === 'maternal')
    }
  },
  
  methods: {
    // 获取模拟数据
    getMockData() {
      return [
        {
          id: 1,
          name: '张三',
          age: 35,
          gender: '男',
          systolic_pressure: 120,
          diastolic_pressure: 80,
          weight: 70,
          height: 175,
          disease_type: '高血压',
          symptoms: '头晕、头痛',
          diagnosis: '原发性高血压',
          treatment: '降压药物治疗',
          data_type: 'medical',
          created_at: '2024-01-15 10:30:00',
          updated_at: '2024-01-15 10:30:00'
        },
        {
          id: 2,
          name: '李四',
          age: 28,
          gender: '女',
          gestational_weeks: 24,
          pregnancy_count: 1,
          parity: 0,
          pregnancy_type: '初产妇',
          systolic_pressure: 110,
          diastolic_pressure: 70,
          weight: 65,
          height: 162,
          data_type: 'maternal',
          created_at: '2024-01-14 14:20:00',
          updated_at: '2024-01-14 14:20:00'
        },
        {
          id: 3,
          name: '王五',
          age: 42,
          gender: '男',
          systolic_pressure: 135,
          diastolic_pressure: 85,
          weight: 80,
          height: 170,
          disease_type: '糖尿病',
          symptoms: '多饮、多尿',
          diagnosis: '2型糖尿病',
          treatment: '口服降糖药',
          data_type: 'medical',
          created_at: '2024-01-13 09:15:00',
          updated_at: '2024-01-13 09:15:00'
        },
        {
          id: 4,
          name: '赵六',
          age: 32,
          gender: '女',
          gestational_weeks: 32,
          pregnancy_count: 2,
          parity: 1,
          pregnancy_type: '经产妇',
          systolic_pressure: 115,
          diastolic_pressure: 75,
          weight: 72,
          height: 165,
          data_type: 'maternal',
          created_at: '2024-01-12 16:45:00',
          updated_at: '2024-01-12 16:45:00'
        },
        {
          id: 5,
          name: '钱七',
          age: 29,
          gender: '男',
          systolic_pressure: 125,
          diastolic_pressure: 82,
          weight: 68,
          height: 178,
          disease_type: '冠心病',
          symptoms: '胸闷、心悸',
          diagnosis: '冠心病',
          treatment: '药物治疗+生活方式干预',
          data_type: 'medical',
          created_at: '2024-01-11 11:30:00',
          updated_at: '2024-01-11 11:30:00'
        }
      ]
    },
    
    // 切换标签页
    switchTab(tab) {
      this.activeTab = tab
      if (tab === 'management' || tab === 'table') {
        this.loadTableData()
      } else if (tab === 'import') {
        this.loadImportHistory()
      }
    },
    
    // 加载表格数据
    loadTableData() {
      this.loading = true
      this.$http.get('/api/data/list', {
        params: {
          page: this.currentPage,
          size: this.pageSize,
          data_type: this.currentFilter,
          keyword: this.searchKeyword
        }
      }).then(response => {
        if (response.data.success) {
          this.tableData = response.data.data
          this.total = response.data.total
        } else {
          this.$message.error('获取数据失败')
          // 使用模拟数据
          this.tableData = this.getMockData()
        }
      }).catch(error => {
        console.error('加载数据失败:', error)
        this.$message.error('加载数据失败')
        // 使用模拟数据
        this.tableData = this.getMockData()
      }).finally(() => {
        this.loading = false
      })
    },
    
    // 处理筛选变化
    handleFilterChange() {
      this.pagination.currentPage = 1
      this.loadTableData()
    },
    
    // 重置筛选
    resetFilters() {
      this.filters = {
        dataType: '',
        keyword: '',
        dateRange: null
      }
      this.handleFilterChange()
    },
    
    // 分页处理
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadTableData()
    },
    
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadTableData()
    },
    
    // 选择变化
    handleSelectionChange(val) {
      this.selectedRecords = val
    },
    
    // 格式化日期时间
    formatDateTime(dateStr) {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN')
    },
    
    // 数据类型切换
    handleDataTypeChange() {
      // 重置表单
      this.$nextTick(() => {
        if (this.$refs.medicalFormRef) this.$refs.medicalFormRef.resetFields()
        if (this.$refs.maternalFormRef) this.$refs.maternalFormRef.resetFields()
      })
    },
    
    // 提交医疗数据
    async submitMedicalData() {
      try {
        await this.$refs.medicalFormRef.validate()
        this.submitting = true
        const response = await this.$http.post('/api/data/medical', this.medicalForm)
        if (response.data.code === 200) {
          this.$message.success('数据提交成功')
          this.resetMedicalForm()
          this.loadTableData()
        } else {
          this.$message.error(response.data.message || '提交失败')
        }
      } catch (error) {
        console.error('提交医疗数据失败:', error)
        this.$message.error('提交失败，请检查网络连接')
      } finally {
        this.submitting = false
      }
    },
    
    // 提交孕产妇数据
    async submitMaternalData() {
      try {
        await this.$refs.maternalFormRef.validate()
        this.submitting = true
        const response = await this.$http.post('/api/data/maternal', this.maternalForm)
        if (response.data.code === 200) {
          this.$message.success('数据提交成功')
          this.resetMaternalForm()
          this.loadTableData()
        } else {
          this.$message.error(response.data.message || '提交失败')
        }
      } catch (error) {
        console.error('提交孕产妇数据失败:', error)
        this.$message.error('提交失败，请检查网络连接')
      } finally {
        this.submitting = false
      }
    },
    
    // 重置表单
    resetMedicalForm() {
      this.$refs.medicalFormRef.resetFields()
    },
    
    resetMaternalForm() {
      this.$refs.maternalFormRef.resetFields()
    },
    
    // 文件上传相关
    beforeUpload(file) {
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                     file.type === 'application/vnd.ms-excel' ||
                     file.type === 'text/csv'
      const isLt10M = file.size / 1024 / 1024 < 10

      if (!isExcel) {
        this.$message.error('只能上传 Excel 或 CSV 文件!')
        return false
      }
      if (!isLt10M) {
        this.$message.error('文件大小不能超过 10MB!')
        return false
      }
      return true
    },
    
    handleUploadSuccess(response, file) {
      if (response.code === 200) {
        this.$message.success('文件上传成功')
        this.loadImportHistory()
        this.loadTableData()
      } else {
        this.$message.error(response.message || '上传失败')
      }
    },
    
    handleUploadError() {
      this.$message.error('文件上传失败')
    },
    
    // 加载导入历史
    async loadImportHistory() {
      try {
        const response = await this.$http.get('/api/data/import-history')
        if (response.data.code === 200) {
          this.importHistory = response.data.data
        }
      } catch (error) {
        console.error('加载导入历史失败:', error)
      }
    },
    
    // 刷新表格数据
    refreshTableData() {
      this.loadTableData()
    },
    
    // 导出数据
    async exportData() {
      try {
        const response = await this.$http.get('/api/data/export', {
          responseType: 'blob'
        })
        
        const blob = new Blob([response.data], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `数据导出_${new Date().toLocaleDateString()}.xlsx`
        a.click()
        window.URL.revokeObjectURL(url)
        
        this.$message.success('数据导出成功')
      } catch (error) {
        console.error('导出数据失败:', error)
        this.$message.error('导出失败')
      }
    },
    
    // 导出表格数据
    async exportTableData() {
      this.exportData()
    },
    
    // 查看记录
    viewRecord(record) {
      // 实现查看记录详情
      console.log('查看记录:', record)
    },
    
    // 编辑记录
    editRecord(record) {
      // 实现编辑记录
      console.log('编辑记录:', record)
    },
    
    // 删除记录
    async deleteRecord(record) {
      try {
        await this.$confirm('确定要删除这条记录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        const response = await this.$http.delete(`/api/data/${record.id}`)
        if (response.data.code === 200) {
          this.$message.success('删除成功')
          this.loadTableData()
        } else {
          this.$message.error(response.data.message || '删除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除记录失败:', error)
          this.$message.error('删除失败')
        }
      }
    }
  },
  
  created() {
    this.loadTableData()
  }
}
</script>

<style scoped>
.data-center-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.data-center-content {
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

.header-actions {
  display: flex;
  gap: 15px;
}

.tab-content {
  min-height: 600px;
}

.filter-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.table-section {
  background: white;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.entry-form-container .el-card {
  margin-bottom: 20px;
}

.data-type-selector {
  text-align: center;
}

.data-type-selector h3 {
  margin-bottom: 20px;
  color: #333;
}

.import-container .el-card {
  margin-bottom: 20px;
}

.import-instructions h4 {
  color: #333;
  margin-bottom: 10px;
}

.import-instructions ul {
  margin-bottom: 20px;
}

.import-instructions li {
  margin-bottom: 5px;
  color: #666;
}

.upload-demo {
  width: 100%;
}

.table-view-container .el-card {
  height: 100%;
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
  
  .filter-section .el-col {
    margin-bottom: 10px;
  }
}
</style>
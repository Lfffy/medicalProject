<template>
  <div class="data-import-container">
    <dv-border-box-8 :dur="5">
      <div class="data-import-content">
        <div class="header">
          <h2>数据导入管理</h2>
          <div class="data-type-selector">
            <el-radio-group v-model="dataType" @change="handleDataTypeChange">
              <el-radio-button label="medical">普通医疗数据</el-radio-button>
              <el-radio-button label="maternal">孕产妇数据</el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <div class="import-section">
          <div class="upload-area">
            <el-upload
              class="upload-component"
              drag
              :action="uploadUrl"
              :headers="uploadHeaders"
              :before-upload="beforeUpload"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :on-progress="handleUploadProgress"
              :file-list="fileList"
              :accept="acceptTypes"
              :limit="1"
              :on-exceed="handleExceed"
              :disabled="uploading"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">
                只能上传 Excel/CSV 文件，且不超过 10MB
              </div>
            </el-upload>

            <div v-if="uploading" class="upload-progress">
              <el-progress :percentage="uploadPercentage" :status="uploadStatus"></el-progress>
              <p>正在上传文件，请稍候...</p>
            </div>
          </div>

          <div class="template-section">
            <h3>模板下载</h3>
            <p>请下载对应的数据模板，按照模板格式填写数据后上传。</p>
            <div class="template-buttons">
              <el-button type="primary" icon="el-icon-download" @click="downloadTemplate('medical')">
                下载医疗数据模板
              </el-button>
              <el-button type="success" icon="el-icon-download" @click="downloadTemplate('maternal')">
                下载孕产妇数据模板
              </el-button>
            </div>
          </div>
        </div>

        <div class="data-preview" v-if="previewData.length > 0">
          <h3>数据预览</h3>
          <el-table :data="previewData" border style="width: 100%" max-height="300">
            <el-table-column
              v-for="column in previewColumns"
              :key="column.prop"
              :prop="column.prop"
              :label="column.label"
              :width="column.width"
            ></el-table-column>
          </el-table>
          <div class="preview-actions">
            <el-button type="success" @click="confirmImport" :loading="importing">
              确认导入
            </el-button>
            <el-button @click="cancelImport">取消</el-button>
          </div>
        </div>

        <div class="import-history">
          <h3>导入历史</h3>
          <el-table :data="importHistory" border style="width: 100%">
            <el-table-column prop="file_name" label="文件名" width="200"></el-table-column>
            <el-table-column prop="data_type" label="数据类型" width="120">
              <template slot-scope="scope">
                <el-tag :type="scope.row.data_type === 'medical' ? 'primary' : 'success'">
                  {{ scope.row.data_type === 'medical' ? '医疗数据' : '孕产妇数据' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="total_records" label="总记录数" width="100"></el-table-column>
            <el-table-column prop="success_records" label="成功记录数" width="120"></el-table-column>
            <el-table-column prop="failed_records" label="失败记录数" width="120"></el-table-column>
            <el-table-column prop="import_status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.import_status)">
                  {{ getStatusText(scope.row.import_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="导入时间" width="180">
              <template slot-scope="scope">
                {{ formatDateTime(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template slot-scope="scope">
                <el-button size="mini" @click="viewDetails(scope.row)">查看详情</el-button>
                <el-button size="mini" type="danger" @click="deleteRecord(scope.row)" v-if="scope.row.import_status === 'failed'">
                  删除记录
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 导入详情对话框 -->
        <el-dialog title="导入详情" :visible.sync="detailDialogVisible" width="60%">
          <div v-if="currentRecord">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="文件名">{{ currentRecord.file_name }}</el-descriptions-item>
              <el-descriptions-item label="数据类型">
                <el-tag :type="currentRecord.data_type === 'medical' ? 'primary' : 'success'">
                  {{ currentRecord.data_type === 'medical' ? '医疗数据' : '孕产妇数据' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="总记录数">{{ currentRecord.total_records }}</el-descriptions-item>
              <el-descriptions-item label="成功记录数">{{ currentRecord.success_records }}</el-descriptions-item>
              <el-descriptions-item label="失败记录数">{{ currentRecord.failed_records }}</el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag :type="getStatusType(currentRecord.import_status)">
                  {{ getStatusText(currentRecord.import_status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="开始时间">{{ formatDateTime(currentRecord.start_time) }}</el-descriptions-item>
              <el-descriptions-item label="结束时间">{{ formatDateTime(currentRecord.end_time) }}</el-descriptions-item>
            </el-descriptions>
            
            <div v-if="currentRecord.error_details" class="error-details">
              <h4>错误详情</h4>
              <el-input
                type="textarea"
                :rows="10"
                :value="currentRecord.error_details"
                readonly
              ></el-input>
            </div>
          </div>
        </el-dialog>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
export default {
  name: 'DataImport',
  data() {
    return {
      dataType: 'medical',
      uploading: false,
      importing: false,
      uploadPercentage: 0,
      uploadStatus: '',
      fileList: [],
      previewData: [],
      previewColumns: [],
      importHistory: [],
      detailDialogVisible: false,
      currentRecord: null,
      
      // 上传相关
      uploadUrl: '',
      uploadHeaders: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      acceptTypes: '.xlsx,.xls,.csv'
    }
  },
  
  computed: {
    uploadUrl() {
      return `/api/data/${this.dataType}/import`;
    }
  },
  
  methods: {
    handleDataTypeChange() {
      this.fileList = [];
      this.previewData = [];
      this.previewColumns = [];
    },
    
    beforeUpload(file) {
      const isValidType = file.type === 'application/vnd.ms-excel' || 
                         file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                         file.type === 'text/csv';
      
      const isLt10M = file.size / 1024 / 1024 < 10;
      
      if (!isValidType) {
        this.$message.error('只能上传 Excel 或 CSV 文件!');
        return false;
      }
      
      if (!isLt10M) {
        this.$message.error('文件大小不能超过 10MB!');
        return false;
      }
      
      this.uploading = true;
      this.uploadPercentage = 0;
      return true;
    },
    
    handleUploadProgress(event, file) {
      this.uploadPercentage = Math.round(event.percent);
    },
    
    handleUploadSuccess(response, file) {
      this.uploading = false;
      this.uploadStatus = 'success';
      
      if (response.code === 200) {
        this.$message.success('文件上传成功');
        
        // 显示数据预览
        if (response.data.preview) {
          this.previewData = response.data.preview.data || [];
          this.previewColumns = response.data.preview.columns || [];
        }
        
        // 刷新导入历史
        this.loadImportHistory();
      } else {
        this.$message.error(response.message || '上传失败');
      }
    },
    
    handleUploadError(error, file) {
      this.uploading = false;
      this.uploadStatus = 'exception';
      this.$message.error('上传失败：' + (error.message || '网络错误'));
    },
    
    handleExceed(files, fileList) {
      this.$message.warning('只能上传一个文件，请先删除当前文件');
    },
    
    downloadTemplate(type) {
      const templateUrl = `/api/data/${type}/template`;
      window.open(templateUrl, '_blank');
    },
    
    confirmImport() {
      this.importing = true;
      this.$http.post('/api/data/confirm-import', {
        data_type: this.dataType,
        file_name: this.fileList[0]?.name
      })
      .then(response => {
        this.$message.success('数据导入成功');
        this.previewData = [];
        this.previewColumns = [];
        this.fileList = [];
        this.loadImportHistory();
      })
      .catch(error => {
        this.$message.error('导入失败：' + (error.response?.data?.message || error.message));
      })
      .finally(() => {
        this.importing = false;
      });
    },
    
    cancelImport() {
      this.previewData = [];
      this.previewColumns = [];
      this.fileList = [];
    },
    
    loadImportHistory() {
      this.$http.get('/api/data/import-history')
        .then(response => {
          this.importHistory = response.data || [];
        })
        .catch(error => {
          this.$message.error('加载导入历史失败：' + error.message);
        });
    },
    
    viewDetails(record) {
      this.currentRecord = record;
      this.detailDialogVisible = true;
    },
    
    deleteRecord(record) {
      this.$confirm('确定要删除这条导入记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http.delete(`/api/data/import-record/${record.id}`)
          .then(response => {
            this.$message.success('删除成功');
            this.loadImportHistory();
          })
          .catch(error => {
            this.$message.error('删除失败：' + error.message);
          });
      });
    },
    
    getStatusType(status) {
      const statusMap = {
        'processing': 'warning',
        'completed': 'success',
        'failed': 'danger'
      };
      return statusMap[status] || 'info';
    },
    
    getStatusText(status) {
      const statusMap = {
        'processing': '处理中',
        'completed': '已完成',
        'failed': '失败'
      };
      return statusMap[status] || '未知';
    },
    
    formatDateTime(dateTime) {
      if (!dateTime) return '-';
      return new Date(dateTime).toLocaleString();
    }
  },
  
  mounted() {
    this.loadImportHistory();
  }
}
</script>

<style lang="less" scoped>
.data-import-container {
  padding: 20px;
  height: 100%;
  
  .data-import-content {
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
      
      .data-type-selector {
        .el-radio-group {
          .el-radio-button__inner {
            background: rgba(64, 158, 255, 0.1);
            border-color: #409EFF;
            color: #409EFF;
            
            &:hover {
              background: rgba(64, 158, 255, 0.2);
            }
          }
          
          .el-radio-button__orig-radio:checked + .el-radio-button__inner {
            background: #409EFF;
            border-color: #409EFF;
            color: #fff;
          }
        }
      }
    }
    
    .import-section {
      display: flex;
      gap: 40px;
      margin-bottom: 30px;
      
      .upload-area {
        flex: 1;
        
        .upload-component {
          width: 100%;
          
          .el-upload-dragger {
            background: rgba(64, 158, 255, 0.05);
            border: 2px dashed #409EFF;
            
            &:hover {
              background: rgba(64, 158, 255, 0.1);
              border-color: #409EFF;
            }
          }
        }
        
        .upload-progress {
          margin-top: 20px;
          text-align: center;
          
          p {
            margin-top: 10px;
            color: #409EFF;
          }
        }
      }
      
      .template-section {
        flex: 1;
        
        h3 {
          color: #409EFF;
          margin-bottom: 10px;
        }
        
        p {
          color: #666;
          margin-bottom: 20px;
        }
        
        .template-buttons {
          display: flex;
          gap: 20px;
        }
      }
    }
    
    .data-preview {
      margin-bottom: 30px;
      
      h3 {
        color: #409EFF;
        margin-bottom: 20px;
      }
      
      .preview-actions {
        margin-top: 20px;
        text-align: center;
      }
    }
    
    .import-history {
      h3 {
        color: #409EFF;
        margin-bottom: 20px;
      }
      
      .el-table {
        .el-tag {
          &.el-tag--primary {
            background-color: rgba(64, 158, 255, 0.1);
            border-color: #409EFF;
            color: #409EFF;
          }
          
          &.el-tag--success {
            background-color: rgba(103, 194, 58, 0.1);
            border-color: #67C23A;
            color: #67C23A;
          }
          
          &.el-tag--warning {
            background-color: rgba(230, 162, 60, 0.1);
            border-color: #E6A23C;
            color: #E6A23C;
          }
          
          &.el-tag--danger {
            background-color: rgba(245, 108, 108, 0.1);
            border-color: #F56C6C;
            color: #F56C6C;
          }
        }
      }
    }
    
    .error-details {
      margin-top: 20px;
      
      h4 {
        color: #F56C6C;
        margin-bottom: 10px;
      }
    }
  }
}
</style>
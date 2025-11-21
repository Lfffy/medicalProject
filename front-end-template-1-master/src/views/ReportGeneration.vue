<template>
  <div class="report-generation-container">
    <dv-border-box-8 :dur="5">
      <div class="report-generation-content">
        <div class="header">
          <h2>报告生成</h2>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-refresh" @click="refreshData">刷新数据</el-button>
            <el-button type="success" icon="el-icon-folder-opened" @click="viewReports">报告库</el-button>
          </div>
        </div>

        <div class="filter-section">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-select v-model="filters.reportType" placeholder="报告类型" @change="handleFilterChange">
                <el-option label="综合分析报告" value="comprehensive"></el-option>
                <el-option label="趋势分析报告" value="trend"></el-option>
                <el-option label="对比分析报告" value="comparison"></el-option>
                <el-option label="预测分析报告" value="prediction"></el-option>
                <el-option label="专项分析报告" value="special"></el-option>
                <el-option label="自定义报告" value="custom"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.dataType" placeholder="数据类型" @change="handleFilterChange">
                <el-option label="全部" value=""></el-option>
                <el-option label="普通医疗数据" value="medical"></el-option>
                <el-option label="孕产妇数据" value="maternal"></el-option>
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
              <el-button type="primary" @click="generateReport">生成报告</el-button>
              <el-button @click="resetFilters">重置</el-button>
            </el-col>
          </el-row>
        </div>

        <!-- 报告配置 -->
        <div class="report-config-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <dv-border-box-10>
                <div class="config-content">
                  <h3>报告配置</h3>
                  <el-form ref="configForm" :model="reportConfig" label-width="120px">
                    <el-form-item label="报告标题">
                      <el-input v-model="reportConfig.title" placeholder="请输入报告标题"></el-input>
                    </el-form-item>
                    <el-form-item label="报告描述">
                      <el-input 
                        v-model="reportConfig.description" 
                        type="textarea" 
                        :rows="3"
                        placeholder="请输入报告描述"
                      ></el-input>
                    </el-form-item>
                    <el-form-item label="包含章节">
                      <el-checkbox-group v-model="reportConfig.sections">
                        <el-checkbox label="summary">数据概要</el-checkbox>
                        <el-checkbox label="trend">趋势分析</el-checkbox>
                        <el-checkbox label="comparison">对比分析</el-checkbox>
                        <el-checkbox label="prediction">预测分析</el-checkbox>
                        <el-checkbox label="conclusion">结论建议</el-checkbox>
                      </el-checkbox-group>
                    </el-form-item>
                    <el-form-item label="图表类型">
                      <el-checkbox-group v-model="reportConfig.chartTypes">
                        <el-checkbox label="line">折线图</el-checkbox>
                        <el-checkbox label="bar">柱状图</el-checkbox>
                        <el-checkbox label="pie">饼图</el-checkbox>
                        <el-checkbox label="radar">雷达图</el-checkbox>
                        <el-checkbox label="heatmap">热力图</el-checkbox>
                      </el-checkbox-group>
                    </el-form-item>
                    <el-form-item label="输出格式">
                      <el-radio-group v-model="reportConfig.format">
                        <el-radio label="pdf">PDF</el-radio>
                        <el-radio label="word">Word</el-radio>
                        <el-radio label="excel">Excel</el-radio>
                        <el-radio label="html">HTML</el-radio>
                      </el-radio-group>
                    </el-form-item>
                  </el-form>
                </div>
              </dv-border-box-10>
            </el-col>
            <el-col :span="12">
              <dv-border-box-10>
                <div class="template-content">
                  <h3>报告模板</h3>
                  <div class="template-list">
                    <div 
                      v-for="template in reportTemplates" 
                      :key="template.id"
                      class="template-item"
                      :class="{ active: selectedTemplate === template.id }"
                      @click="selectTemplate(template)"
                    >
                      <div class="template-icon">
                        <i :class="template.icon"></i>
                      </div>
                      <div class="template-info">
                        <h4>{{ template.name }}</h4>
                        <p>{{ template.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </dv-border-box-10>
            </el-col>
          </el-row>
        </div>

        <!-- 报告预览 -->
        <div class="report-preview-section" v-if="reportPreview">
          <dv-border-box-10>
            <div class="preview-content">
              <h3>报告预览</h3>
              <div class="preview-toolbar">
                <el-button-group>
                  <el-button size="mini" icon="el-icon-zoom-in" @click="zoomIn">放大</el-button>
                  <el-button size="mini" icon="el-icon-zoom-out" @click="zoomOut">缩小</el-button>
                  <el-button size="mini" icon="el-icon-refresh" @click="resetZoom">重置</el-button>
                </el-button-group>
                <div class="zoom-info">{{ zoomLevel }}%</div>
              </div>
              <div class="preview-container" :style="{ transform: `scale(${zoomLevel / 100})` }">
                <div class="report-preview" v-html="reportPreview"></div>
              </div>
            </div>
          </dv-border-box-10>
        </div>

        <!-- 生成历史 -->
        <div class="history-section">
          <dv-border-box-10>
            <div class="history-content">
              <h3>生成历史</h3>
              <el-table
                :data="reportHistory"
                border
                style="width: 100%"
                v-loading="loading"
              >
                <el-table-column prop="id" label="ID" width="80"></el-table-column>
                <el-table-column prop="title" label="报告标题" width="200"></el-table-column>
                <el-table-column prop="type" label="报告类型" width="120">
                  <template slot-scope="scope">
                    <el-tag :type="getReportTypeTag(scope.row.type)">
                      {{ getReportTypeLabel(scope.row.type) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="format" label="格式" width="80"></el-table-column>
                <el-table-column prop="created_at" label="生成时间" width="180"></el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getStatusTag(scope.row.status)">
                      {{ getStatusLabel(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="file_size" label="文件大小" width="100"></el-table-column>
                <el-table-column label="操作" width="200">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="previewReport(scope.row)">预览</el-button>
                    <el-button size="mini" type="primary" @click="downloadReport(scope.row)">下载</el-button>
                    <el-button size="mini" type="danger" @click="deleteReport(scope.row)">删除</el-button>
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

        <!-- 批量生成 -->
        <div class="batch-generation-section">
          <dv-border-box-10>
            <div class="batch-content">
              <h3>批量生成</h3>
              <el-form :model="batchConfig" label-width="120px">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="报告类型">
                      <el-select v-model="batchConfig.reportType" style="width: 100%">
                        <el-option label="综合分析报告" value="comprehensive"></el-option>
                        <el-option label="趋势分析报告" value="trend"></el-option>
                        <el-option label="对比分析报告" value="comparison"></el-option>
                        <el-option label="预测分析报告" value="prediction"></el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="时间周期">
                      <el-select v-model="batchConfig.period" style="width: 100%">
                        <el-option label="日报" value="daily"></el-option>
                        <el-option label="周报" value="weekly"></el-option>
                        <el-option label="月报" value="monthly"></el-option>
                        <el-option label="季报" value="quarterly"></el-option>
                        <el-option label="年报" value="yearly"></el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="生成数量">
                      <el-input-number 
                        v-model="batchConfig.count" 
                        :min="1" 
                        :max="100"
                        style="width: 100%"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item>
                  <el-button type="primary" @click="batchGenerate" :loading="batchGenerating">
                    批量生成
                  </el-button>
                  <el-button @click="resetBatchConfig">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
          </dv-border-box-10>
        </div>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
export default {
  name: 'ReportGeneration',
  data() {
    return {
      loading: false,
      batchGenerating: false,
      
      // 筛选条件
      filters: {
        reportType: 'comprehensive',
        dataType: '',
        dateRange: []
      },
      
      // 报告配置
      reportConfig: {
        title: '',
        description: '',
        sections: ['summary', 'trend', 'conclusion'],
        chartTypes: ['line', 'bar'],
        format: 'pdf'
      },
      
      // 选中的模板
      selectedTemplate: null,
      
      // 报告模板
      reportTemplates: [
        {
          id: 1,
          name: '标准医疗报告',
          description: '包含基础数据分析和可视化图表',
          icon: 'el-icon-document'
        },
        {
          id: 2,
          name: '孕产妇专项报告',
          description: '针对孕产妇数据的专项分析报告',
          icon: 'el-icon-document'
        },
        {
          id: 3,
          name: '科研分析报告',
          description: '适用于科研项目的详细分析报告',
          icon: 'el-icon-document'
        },
        {
          id: 4,
          name: '管理决策报告',
          description: '面向管理层的决策支持报告',
          icon: 'el-icon-document'
        }
      ],
      
      // 报告预览
      reportPreview: null,
      zoomLevel: 100,
      
      // 报告历史
      reportHistory: [],
      
      // 分页
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      
      // 批量生成配置
      batchConfig: {
        reportType: 'comprehensive',
        period: 'monthly',
        count: 1
      }
    }
  },
  
  mounted() {
    this.loadReportHistory()
  },
  
  methods: {
    loadReportHistory() {
      this.loading = true
      
      const params = {
        page: this.pagination.currentPage,
        page_size: this.pagination.pageSize,
        report_type: this.filters.reportType,
        data_type: this.filters.dataType,
        start_date: this.filters.dateRange?.[0],
        end_date: this.filters.dateRange?.[1]
      }
      
      this.$http.get('/api/reports/history', { params })
        .then(response => {
          const data = response.data.data
          this.reportHistory = data.reports || []
          this.pagination.total = data.total || 0
        })
        .catch(error => {
          this.$message.error('加载报告历史失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    selectTemplate(template) {
      this.selectedTemplate = template.id
      this.reportConfig.title = template.name
      this.reportConfig.description = template.description
    },
    
    generateReport() {
      if (!this.reportConfig.title) {
        this.$message.warning('请输入报告标题')
        return
      }
      
      const params = {
        report_type: this.filters.reportType,
        data_type: this.filters.dataType,
        date_range: this.filters.dateRange,
        config: this.reportConfig,
        template_id: this.selectedTemplate
      }
      
      this.$http.post('/api/reports/generate', params)
        .then(response => {
          const data = response.data.data
          this.reportPreview = data.preview_html
          this.$message.success('报告生成成功！')
          
          // 刷新历史记录
          this.loadReportHistory()
        })
        .catch(error => {
          this.$message.error('生成报告失败：' + error.message)
        })
    },
    
    batchGenerate() {
      this.batchGenerating = true
      
      const params = {
        report_type: this.batchConfig.reportType,
        period: this.batchConfig.period,
        count: this.batchConfig.count
      }
      
      this.$http.post('/api/reports/batch-generate', params)
        .then(response => {
          this.$message.success(`成功生成 ${this.batchConfig.count} 个报告！`)
          this.loadReportHistory()
        })
        .catch(error => {
          this.$message.error('批量生成失败：' + error.message)
        })
        .finally(() => {
          this.batchGenerating = false
        })
    },
    
    previewReport(report) {
      this.$http.get(`/api/reports/preview/${report.id}`)
        .then(response => {
          this.reportPreview = response.data.data.preview_html
        })
        .catch(error => {
          this.$message.error('预览报告失败：' + error.message)
        })
    },
    
    downloadReport(report) {
      this.$http.get(`/api/reports/download/${report.id}`, {
        responseType: 'blob'
      })
      .then(response => {
        const blob = new Blob([response.data])
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = report.title + '.' + report.format
        link.click()
      })
      .catch(error => {
        this.$message.error('下载报告失败：' + error.message)
      })
    },
    
    deleteReport(report) {
      this.$confirm('确定要删除这个报告吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http.delete(`/api/reports/${report.id}`)
          .then(() => {
            this.$message.success('删除成功')
            this.loadReportHistory()
          })
          .catch(error => {
            this.$message.error('删除失败：' + error.message)
          })
      })
    },
    
    viewReports() {
      this.loadReportHistory()
    },
    
    handleFilterChange() {
      this.loadReportHistory()
    },
    
    resetFilters() {
      this.filters = {
        reportType: 'comprehensive',
        dataType: '',
        dateRange: []
      }
      this.loadReportHistory()
    },
    
    resetBatchConfig() {
      this.batchConfig = {
        reportType: 'comprehensive',
        period: 'monthly',
        count: 1
      }
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadReportHistory()
    },
    
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadReportHistory()
    },
    
    refreshData() {
      this.loadReportHistory()
      this.$message.success('数据已刷新')
    },
    
    zoomIn() {
      if (this.zoomLevel < 200) {
        this.zoomLevel += 10
      }
    },
    
    zoomOut() {
      if (this.zoomLevel > 50) {
        this.zoomLevel -= 10
      }
    },
    
    resetZoom() {
      this.zoomLevel = 100
    },
    
    getReportTypeLabel(type) {
      const labels = {
        comprehensive: '综合分析',
        trend: '趋势分析',
        comparison: '对比分析',
        prediction: '预测分析',
        special: '专项分析',
        custom: '自定义'
      }
      return labels[type] || type
    },
    
    getReportTypeTag(type) {
      const tags = {
        comprehensive: 'primary',
        trend: 'success',
        comparison: 'warning',
        prediction: 'danger',
        special: 'info',
        custom: ''
      }
      return tags[type] || ''
    },
    
    getStatusLabel(status) {
      const labels = {
        generating: '生成中',
        completed: '已完成',
        failed: '失败',
        deleted: '已删除'
      }
      return labels[status] || status
    },
    
    getStatusTag(status) {
      const tags = {
        generating: 'warning',
        completed: 'success',
        failed: 'danger',
        deleted: 'info'
      }
      return tags[status] || ''
    }
  }
}
</script>

<style lang="less" scoped>
.report-generation-container {
  padding: 20px;
  height: 100%;
  
  .report-generation-content {
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
    
    .report-config-section {
      margin-bottom: 20px;
      
      .config-content,
      .template-content {
        padding: 20px;
        height: 100%;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
      }
      
      .template-list {
        .template-item {
          display: flex;
          align-items: center;
          padding: 15px;
          margin-bottom: 10px;
          background: rgba(64, 158, 255, 0.05);
          border: 1px solid rgba(64, 158, 255, 0.2);
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s;
          
          &:hover {
            background: rgba(64, 158, 255, 0.1);
          }
          
          &.active {
            background: rgba(64, 158, 255, 0.2);
            border-color: #409EFF;
          }
          
          .template-icon {
            margin-right: 15px;
            font-size: 24px;
            color: #409EFF;
          }
          
          .template-info {
            flex: 1;
            
            h4 {
              margin: 0 0 5px 0;
              color: #333;
            }
            
            p {
              margin: 0;
              color: #666;
              font-size: 12px;
            }
          }
        }
      }
    }
    
    .report-preview-section {
      margin-bottom: 20px;
      
      .preview-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
        
        .preview-toolbar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          padding: 10px;
          background: rgba(64, 158, 255, 0.05);
          border-radius: 8px;
          
          .zoom-info {
            color: #666;
            font-weight: bold;
          }
        }
        
        .preview-container {
          transition: transform 0.3s;
          transform-origin: top left;
          max-height: 600px;
          overflow: auto;
          
          .report-preview {
            background: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            min-height: 400px;
          }
        }
      }
    }
    
    .history-section {
      margin-bottom: 20px;
      
      .history-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
      }
    }
    
    .batch-generation-section {
      .batch-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
      }
    }
  }
}
</style>
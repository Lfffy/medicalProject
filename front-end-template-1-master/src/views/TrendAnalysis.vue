<template>
  <div class="trend-analysis-container">
    <dv-border-box-8 :dur="5">
      <div class="trend-analysis-content">
        <div class="header">
          <h2>趋势分析</h2>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-refresh" @click="refreshData">刷新数据</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportReport">导出报告</el-button>
          </div>
        </div>

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
              <el-select v-model="filters.timeRange" placeholder="时间范围" @change="handleFilterChange">
                <el-option label="最近7天" value="7d"></el-option>
                <el-option label="最近30天" value="30d"></el-option>
                <el-option label="最近3个月" value="3m"></el-option>
                <el-option label="最近6个月" value="6m"></el-option>
                <el-option label="最近1年" value="1y"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-select v-model="filters.metric" placeholder="分析指标" @change="handleFilterChange">
                <el-option label="患者数量" value="patient_count"></el-option>
                <el-option label="平均年龄" value="avg_age"></el-option>
                <el-option label="血压趋势" value="blood_pressure"></el-option>
                <el-option label="体重趋势" value="weight"></el-option>
                <el-option label="疾病分布" value="disease_distribution"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-button type="primary" @click="handleFilterChange">分析</el-button>
              <el-button @click="resetFilters">重置</el-button>
            </el-col>
          </el-row>
        </div>

        <div class="charts-grid">
          <!-- 趋势图 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>{{ getChartTitle('trend') }}</h3>
                <div ref="trendChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 分布图 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>{{ getChartTitle('distribution') }}</h3>
                <div ref="distributionChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 对比图 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>{{ getChartTitle('comparison') }}</h3>
                <div ref="comparisonChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 预测图 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>{{ getChartTitle('prediction') }}</h3>
                <div ref="predictionChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>
        </div>

        <!-- 统计摘要 -->
        <div class="summary-section">
          <dv-border-box-10>
            <div class="summary-content">
              <h3>统计摘要</h3>
              <el-row :gutter="20">
                <el-col :span="6" v-for="stat in summaryStats" :key="stat.label">
                  <div class="stat-card">
                    <div class="stat-label">{{ stat.label }}</div>
                    <div class="stat-value">{{ stat.value }}</div>
                    <div class="stat-trend" :class="stat.trend">
                      <i :class="getTrendIcon(stat.trend)"></i>
                      {{ stat.change }}
                    </div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </dv-border-box-10>
        </div>

        <!-- 详细数据表格 -->
        <div class="data-table-section">
          <dv-border-box-10>
            <div class="table-content">
              <h3>详细数据</h3>
              <el-table
                :data="trendData"
                border
                style="width: 100%"
                v-loading="loading"
              >
                <el-table-column prop="date" label="日期" width="120"></el-table-column>
                <el-table-column prop="patient_count" label="患者数量" width="100"></el-table-column>
                <el-table-column prop="avg_age" label="平均年龄" width="100"></el-table-column>
                <el-table-column prop="avg_systolic" label="平均收缩压" width="120"></el-table-column>
                <el-table-column prop="avg_diastolic" label="平均舒张压" width="120"></el-table-column>
                <el-table-column prop="avg_weight" label="平均体重" width="100"></el-table-column>
                <el-table-column prop="disease_types" label="主要疾病类型" width="150"></el-table-column>
                <el-table-column prop="risk_level" label="风险等级" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="getRiskTagType(scope.row.risk_level)">
                      {{ scope.row.risk_level }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </dv-border-box-10>
        </div>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'TrendAnalysis',
  data() {
    return {
      loading: false,
      charts: {},
      
      // 筛选条件
      filters: {
        dataType: '',
        timeRange: '30d',
        metric: 'patient_count'
      },
      
      // 趋势数据
      trendData: [],
      
      // 统计摘要
      summaryStats: [],
      
      // 图表配置
      chartOptions: {
        trend: null,
        distribution: null,
        comparison: null,
        prediction: null
      }
    }
  },
  
  mounted() {
    this.initCharts()
    this.loadData()
  },
  
  beforeDestroy() {
    // 销毁图表实例
    Object.values(this.charts).forEach(chart => {
      if (chart) {
        chart.dispose()
      }
    })
  },
  
  methods: {
    initCharts() {
      // 初始化趋势图
      this.charts.trend = echarts.init(this.$refs.trendChart)
      
      // 初始化分布图
      this.charts.distribution = echarts.init(this.$refs.distributionChart)
      
      // 初始化对比图
      this.charts.comparison = echarts.init(this.$refs.comparisonChart)
      
      // 初始化预测图
      this.charts.prediction = echarts.init(this.$refs.predictionChart)
      
      // 监听窗口大小变化
      window.addEventListener('resize', this.handleResize)
    },
    
    handleResize() {
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.resize()
        }
      })
    },
    
    loadData() {
      this.loading = true
      
      const params = {
        data_type: this.filters.dataType,
        time_range: this.filters.timeRange,
        metric: this.filters.metric
      }
      
      this.$http.get('/api/analysis/trend', { params })
        .then(response => {
          const data = response.data.data
          this.trendData = data.trend_data || []
          this.summaryStats = data.summary_stats || []
          
          // 更新图表
          this.updateTrendChart(data.trend_chart || {})
          this.updateDistributionChart(data.distribution_chart || {})
          this.updateComparisonChart(data.comparison_chart || {})
          this.updatePredictionChart(data.prediction_chart || {})
        })
        .catch(error => {
          this.$message.error('加载趋势数据失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    updateTrendChart(data) {
      const option = {
        title: {
          text: '趋势变化',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: data.series?.map(s => s.name) || [],
          top: 30
        },
        xAxis: {
          type: 'category',
          data: data.xAxis?.data || [],
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            color: '#666'
          }
        },
        series: data.series || [],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      this.charts.trend.setOption(option)
    },
    
    updateDistributionChart(data) {
      const option = {
        title: {
          text: '分布情况',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 30
        },
        series: [
          {
            name: '分布',
            type: 'pie',
            radius: '50%',
            data: data.data || [],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      
      this.charts.distribution.setOption(option)
    },
    
    updateComparisonChart(data) {
      const option = {
        title: {
          text: '对比分析',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: data.series?.map(s => s.name) || [],
          top: 30
        },
        xAxis: {
          type: 'category',
          data: data.xAxis?.data || [],
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            color: '#666'
          }
        },
        series: data.series || [],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      this.charts.comparison.setOption(option)
    },
    
    updatePredictionChart(data) {
      const option = {
        title: {
          text: '预测趋势',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: data.series?.map(s => s.name) || [],
          top: 30
        },
        xAxis: {
          type: 'category',
          data: data.xAxis?.data || [],
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            color: '#666'
          }
        },
        series: data.series || [],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      this.charts.prediction.setOption(option)
    },
    
    getChartTitle(type) {
      const titles = {
        trend: '趋势分析',
        distribution: '分布分析',
        comparison: '对比分析',
        prediction: '预测分析'
      }
      return titles[type] || '图表'
    },
    
    getRiskTagType(riskLevel) {
      const types = {
        '低风险': 'success',
        '中风险': 'warning',
        '高风险': 'danger',
        '未知': 'info'
      }
      return types[riskLevel] || 'info'
    },
    
    getTrendIcon(trend) {
      const icons = {
        up: 'el-icon-top',
        down: 'el-icon-bottom',
        stable: 'el-icon-minus'
      }
      return icons[trend] || 'el-icon-minus'
    },
    
    handleFilterChange() {
      this.loadData()
    },
    
    resetFilters() {
      this.filters = {
        dataType: '',
        timeRange: '30d',
        metric: 'patient_count'
      }
      this.loadData()
    },
    
    refreshData() {
      this.loadData()
      this.$message.success('数据已刷新')
    },
    
    exportReport() {
      const params = {
        data_type: this.filters.dataType,
        time_range: this.filters.timeRange,
        metric: this.filters.metric
      }
      
      this.$http.get('/api/analysis/export-report', { 
        params,
        responseType: 'blob'
      })
      .then(response => {
        const blob = new Blob([response.data])
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = `趋势分析报告_${new Date().toISOString().slice(0, 10)}.pdf`
        link.click()
      })
      .catch(error => {
        this.$message.error('导出报告失败：' + error.message)
      })
    }
  }
}
</script>

<style lang="less" scoped>
.trend-analysis-container {
  padding: 20px;
  height: 100%;
  
  .trend-analysis-content {
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
    
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-bottom: 20px;
      
      .chart-item {
        min-height: 400px;
        
        .chart-content {
          padding: 20px;
          height: 100%;
          
          h3 {
            color: #409EFF;
            margin-bottom: 15px;
            text-align: center;
          }
          
          .chart {
            width: 100%;
            height: 320px;
          }
        }
      }
    }
    
    .summary-section {
      margin-bottom: 20px;
      
      .summary-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
        
        .stat-card {
          text-align: center;
          padding: 20px;
          background: rgba(64, 158, 255, 0.05);
          border-radius: 8px;
          border: 1px solid rgba(64, 158, 255, 0.2);
          
          .stat-label {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
          }
          
          .stat-value {
            color: #409EFF;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
          }
          
          .stat-trend {
            font-size: 12px;
            
            &.up {
              color: #67C23A;
            }
            
            &.down {
              color: #F56C6C;
            }
            
            &.stable {
              color: #909399;
            }
          }
        }
      }
    }
    
    .data-table-section {
      .table-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
      }
    }
  }
}

@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
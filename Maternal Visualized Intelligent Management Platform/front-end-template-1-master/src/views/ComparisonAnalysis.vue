<template>
  <div class="comparison-analysis-container">
    <dv-border-box-8 :dur="5">
      <div class="comparison-analysis-content">
        <div class="header">
          <h2>对比分析</h2>
          <div class="header-actions">
            <el-button type="primary" icon="el-icon-refresh" @click="refreshData">刷新数据</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportReport">导出报告</el-button>
          </div>
        </div>

        <div class="filter-section">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-select v-model="filters.comparisonType" placeholder="对比类型" @change="handleFilterChange">
                <el-option label="时间对比" value="time"></el-option>
                <el-option label="科室对比" value="department"></el-option>
                <el-option label="疾病对比" value="disease"></el-option>
                <el-option label="年龄组对比" value="age_group"></el-option>
                <el-option label="性别对比" value="gender"></el-option>
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
              <el-select v-model="filters.timeRange" placeholder="时间范围" @change="handleFilterChange">
                <el-option label="最近7天" value="7d"></el-option>
                <el-option label="最近30天" value="30d"></el-option>
                <el-option label="最近3个月" value="3m"></el-option>
                <el-option label="最近6个月" value="6m"></el-option>
                <el-option label="最近1年" value="1y"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-button type="primary" @click="handleFilterChange">分析</el-button>
              <el-button @click="resetFilters">重置</el-button>
            </el-col>
          </el-row>
        </div>

        <!-- 对比维度选择 -->
        <div class="dimension-section" v-if="filters.comparisonType">
          <el-row :gutter="20">
            <el-col :span="12">
              <h4>选择对比维度</h4>
              <el-select 
                v-model="selectedDimensions" 
                multiple 
                placeholder="请选择对比维度"
                style="width: 100%"
                @change="handleDimensionChange"
              >
                <el-option 
                  v-for="item in dimensionOptions" 
                  :key="item.value" 
                  :label="item.label" 
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-col>
            <el-col :span="12">
              <h4>分析指标</h4>
              <el-select 
                v-model="selectedMetrics" 
                multiple 
                placeholder="请选择分析指标"
                style="width: 100%"
                @change="handleMetricChange"
              >
                <el-option 
                  v-for="item in metricOptions" 
                  :key="item.value" 
                  :label="item.label" 
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-col>
          </el-row>
        </div>

        <div class="charts-grid">
          <!-- 柱状对比图 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>柱状对比分析</h3>
                <div ref="barChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 雷达图对比 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>雷达图对比分析</h3>
                <div ref="radarChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 热力图对比 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>热力图对比分析</h3>
                <div ref="heatmapChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>

          <!-- 散点图对比 -->
          <div class="chart-item">
            <dv-border-box-10>
              <div class="chart-content">
                <h3>散点图对比分析</h3>
                <div ref="scatterChart" class="chart"></div>
              </div>
            </dv-border-box-10>
          </div>
        </div>

        <!-- 对比结果表格 -->
        <div class="comparison-table-section">
          <dv-border-box-10>
            <div class="table-content">
              <h3>对比结果详情</h3>
              <el-table
                :data="comparisonData"
                border
                style="width: 100%"
                v-loading="loading"
              >
                <el-table-column prop="dimension" label="对比维度" width="150"></el-table-column>
                <el-table-column prop="total_count" label="总数" width="100"></el-table-column>
                <el-table-column prop="avg_age" label="平均年龄" width="100"></el-table-column>
                <el-table-column prop="male_count" label="男性数量" width="100"></el-table-column>
                <el-table-column prop="female_count" label="女性数量" width="100"></el-table-column>
                <el-table-column prop="avg_systolic" label="平均收缩压" width="120"></el-table-column>
                <el-table-column prop="avg_diastolic" label="平均舒张压" width="120"></el-table-column>
                <el-table-column prop="avg_weight" label="平均体重" width="100"></el-table-column>
                <el-table-column prop="risk_distribution" label="风险分布" width="200">
                  <template slot-scope="scope">
                    <el-tag 
                      v-for="(count, risk) in scope.row.risk_distribution" 
                      :key="risk"
                      :type="getRiskTagType(risk)"
                      size="mini"
                      style="margin-right: 5px"
                    >
                      {{ risk }}: {{ count }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="150">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="viewDetails(scope.row)">查看详情</el-button>
                    <el-button size="mini" type="primary" @click="drillDown(scope.row)">下钻分析</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </dv-border-box-10>
        </div>

        <!-- 统计显著性检验 -->
        <div class="significance-section">
          <dv-border-box-10>
            <div class="significance-content">
              <h3>统计显著性检验</h3>
              <el-table
                :data="significanceData"
                border
                style="width: 100%"
              >
                <el-table-column prop="test_type" label="检验类型" width="150"></el-table-column>
                <el-table-column prop="groups" label="对比组" width="200"></el-table-column>
                <el-table-column prop="statistic" label="统计量" width="120"></el-table-column>
                <el-table-column prop="p_value" label="P值" width="100">
                  <template slot-scope="scope">
                    <span :class="getSignificanceClass(scope.row.p_value)">
                      {{ scope.row.p_value }}
                    </span>
                  </template>
                </el-table-column>
                <el-table-column prop="significance" label="显著性" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="scope.row.significant ? 'success' : 'info'">
                      {{ scope.row.significant ? '显著' : '不显著' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="interpretation" label="解释"></el-table-column>
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
  name: 'ComparisonAnalysis',
  data() {
    return {
      loading: false,
      charts: {},
      
      // 筛选条件
      filters: {
        comparisonType: '',
        dataType: '',
        timeRange: '30d'
      },
      
      // 选中的维度和指标
      selectedDimensions: [],
      selectedMetrics: [],
      
      // 维度选项
      dimensionOptions: [],
      
      // 指标选项
      metricOptions: [
        { label: '患者数量', value: 'patient_count' },
        { label: '平均年龄', value: 'avg_age' },
        { label: '性别比例', value: 'gender_ratio' },
        { label: '血压水平', value: 'blood_pressure' },
        { label: '体重指数', value: 'bmi' },
        { label: '风险等级', value: 'risk_level' }
      ],
      
      // 对比数据
      comparisonData: [],
      significanceData: [],
      
      // 图表配置
      chartOptions: {
        bar: null,
        radar: null,
        heatmap: null,
        scatter: null
      }
    }
  },
  
  mounted() {
    this.initCharts()
    this.loadDimensionOptions()
  },
  
  beforeDestroy() {
    // 销毁图表实例
    Object.values(this.charts).forEach(chart => {
      if (chart) {
        chart.dispose()
      }
    })
    window.removeEventListener('resize', this.handleResize)
  },
  
  watch: {
    'filters.comparisonType'() {
      this.loadDimensionOptions()
    }
  },
  
  methods: {
    initCharts() {
      // 初始化柱状图
      this.charts.bar = echarts.init(this.$refs.barChart)
      
      // 初始化雷达图
      this.charts.radar = echarts.init(this.$refs.radarChart)
      
      // 初始化热力图
      this.charts.heatmap = echarts.init(this.$refs.heatmapChart)
      
      // 初始化散点图
      this.charts.scatter = echarts.init(this.$refs.scatterChart)
      
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
    
    loadDimensionOptions() {
      if (!this.filters.comparisonType) {
        this.dimensionOptions = []
        return
      }
      
      const dimensionMap = {
        time: [
          { label: '本周', value: 'this_week' },
          { label: '上周', value: 'last_week' },
          { label: '本月', value: 'this_month' },
          { label: '上月', value: 'last_month' }
        ],
        department: [
          { label: '内科', value: 'internal' },
          { label: '外科', value: 'surgery' },
          { label: '妇产科', value: 'obstetrics' },
          { label: '儿科', value: 'pediatrics' }
        ],
        disease: [
          { label: '高血压', value: 'hypertension' },
          { label: '糖尿病', value: 'diabetes' },
          { label: '心脏病', value: 'heart_disease' },
          { label: '呼吸系统疾病', value: 'respiratory' }
        ],
        age_group: [
          { label: '0-18岁', value: '0-18' },
          { label: '19-35岁', value: '19-35' },
          { label: '36-50岁', value: '36-50' },
          { label: '51-65岁', value: '51-65' },
          { label: '65岁以上', value: '65+' }
        ],
        gender: [
          { label: '男性', value: 'male' },
          { label: '女性', value: 'female' }
        ]
      }
      
      this.dimensionOptions = dimensionMap[this.filters.comparisonType] || []
    },
    
    loadData() {
      if (!this.filters.comparisonType || this.selectedDimensions.length === 0) {
        this.$message.warning('请选择对比类型和对比维度')
        return
      }
      
      this.loading = true
      
      const params = {
        comparison_type: this.filters.comparisonType,
        data_type: this.filters.dataType,
        time_range: this.filters.timeRange,
        dimensions: this.selectedDimensions,
        metrics: this.selectedMetrics
      }
      
      this.$http.get('/api/analysis/comparison', { params })
        .then(response => {
          const data = response.data.data
          this.comparisonData = data.comparison_data || []
          this.significanceData = data.significance_data || []
          
          // 更新图表
          this.updateBarChart(data.bar_chart || {})
          this.updateRadarChart(data.radar_chart || {})
          this.updateHeatmapChart(data.heatmap_chart || {})
          this.updateScatterChart(data.scatter_chart || {})
        })
        .catch(error => {
          this.$message.error('加载对比数据失败：' + error.message)
        })
        .finally(() => {
          this.loading = false
        })
    },
    
    updateBarChart(data) {
      const option = {
        title: {
          text: '柱状对比',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
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
      
      this.charts.bar.setOption(option)
    },
    
    updateRadarChart(data) {
      const option = {
        title: {
          text: '雷达图对比',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {},
        legend: {
          data: data.series?.map(s => s.name) || [],
          top: 30
        },
        radar: {
          indicator: data.indicator || [],
          center: ['50%', '60%']
        },
        series: [
          {
            type: 'radar',
            data: data.series || []
          }
        ]
      }
      
      this.charts.radar.setOption(option)
    },
    
    updateHeatmapChart(data) {
      const option = {
        title: {
          text: '热力图对比',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        tooltip: {
          position: 'top'
        },
        grid: {
          height: '50%',
          top: '10%'
        },
        xAxis: {
          type: 'category',
          data: data.xAxis?.data || [],
          splitArea: {
            show: true
          }
        },
        yAxis: {
          type: 'category',
          data: data.yAxis?.data || [],
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 10,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '15%'
        },
        series: [
          {
            name: '热力图',
            type: 'heatmap',
            data: data.data || [],
            label: {
              show: true
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      
      this.charts.heatmap.setOption(option)
    },
    
    updateScatterChart(data) {
      const option = {
        title: {
          text: '散点图对比',
          left: 'center',
          textStyle: {
            color: '#409EFF'
          }
        },
        xAxis: {
          type: 'value',
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        yAxis: {
          type: 'value',
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        series: data.series || [],
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            return `${params.seriesName}<br/>X: ${params.value[0]}<br/>Y: ${params.value[1]}`
          }
        }
      }
      
      this.charts.scatter.setOption(option)
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
    
    getSignificanceClass(pValue) {
      if (pValue < 0.01) return 'highly-significant'
      if (pValue < 0.05) return 'significant'
      return 'not-significant'
    },
    
    handleFilterChange() {
      this.loadData()
    },
    
    handleDimensionChange() {
      if (this.selectedDimensions.length > 0) {
        this.loadData()
      }
    },
    
    handleMetricChange() {
      if (this.selectedMetrics.length > 0) {
        this.loadData()
      }
    },
    
    resetFilters() {
      this.filters = {
        comparisonType: '',
        dataType: '',
        timeRange: '30d'
      }
      this.selectedDimensions = []
      this.selectedMetrics = []
      this.comparisonData = []
      this.significanceData = []
    },
    
    refreshData() {
      this.loadData()
      this.$message.success('数据已刷新')
    },
    
    viewDetails(row) {
      this.$message.info(`查看 ${row.dimension} 的详细信息`)
    },
    
    drillDown(row) {
      this.$message.info(`对 ${row.dimension} 进行下钻分析`)
    },
    
    exportReport() {
      const params = {
        comparison_type: this.filters.comparisonType,
        data_type: this.filters.dataType,
        time_range: this.filters.timeRange,
        dimensions: this.selectedDimensions,
        metrics: this.selectedMetrics
      }
      
      this.$http.get('/api/analysis/export-comparison-report', { 
        params,
        responseType: 'blob'
      })
      .then(response => {
        const blob = new Blob([response.data])
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = `对比分析报告_${new Date().toISOString().slice(0, 10)}.pdf`
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
.comparison-analysis-container {
  padding: 20px;
  height: 100%;
  
  .comparison-analysis-content {
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
    
    .dimension-section {
      margin-bottom: 20px;
      padding: 20px;
      background: rgba(64, 158, 255, 0.05);
      border-radius: 8px;
      border: 1px solid rgba(64, 158, 255, 0.2);
      
      h4 {
        color: #409EFF;
        margin-bottom: 10px;
      }
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
    
    .comparison-table-section {
      margin-bottom: 20px;
      
      .table-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
      }
    }
    
    .significance-section {
      .significance-content {
        padding: 20px;
        
        h3 {
          color: #409EFF;
          margin-bottom: 20px;
        }
        
        .highly-significant {
          color: #F56C6C;
          font-weight: bold;
        }
        
        .significant {
          color: #E6A23C;
          font-weight: bold;
        }
        
        .not-significant {
          color: #909399;
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
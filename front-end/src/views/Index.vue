<template>
  <div class="home">
    <transition name="fade" mode="out-in">
      <div key="content">
        <dv-loading v-if="!config4.data.length">Loading...</dv-loading>
        <div class="naca">
          <!-- 页面头部 -->
          <div class="index-header">
            <dv-decoration-10 style="width: 300px; height: 1px; margin-bottom: 30px" />
            <dv-decoration-8 style="width: 180px; height: 50px" :color="['#ff85a2', '#ffb6c1']" />
            <div class="header-title">
              {{ isMaternalData ? '孕产妇健康管理' : '医疗疾病数据' }}
            </div>
            <dv-decoration-8 :reverse="true" style="width: 180px; height: 50px" :color="['#ff85a2', '#ffb6c1']" />
            <dv-decoration-10 style="width: 300px; height: 1px; transform: rotateY(180deg); margin-bottom: 30px;" />
          </div>

          <!-- 内容区域 - 采用网格布局 -->
          <div class="index-content">
            <!-- 1. 数据概览卡片区域 -->
            <div class="card-grid">
              <div class="data-card">
                <div class="card-icon">👶</div>
                <div class="card-content">
                  <div class="card-label">就诊人数</div>
                  <div class="card-value">{{ centerData.maxNum }}</div>
                </div>
              </div>
              <div class="data-card">
                <div class="card-icon">❤️</div>
                <div class="card-content">
                  <div class="card-label">常见症状</div>
                  <div class="card-value">{{ centerData.maxType }}</div>
                </div>
              </div>
              <div class="data-card">
                <div class="card-icon">🏥</div>
                <div class="card-content">
                  <div class="card-label">就诊科室</div>
                  <div class="card-value">{{ centerData.maxDep }}</div>
                </div>
              </div>
              <div class="data-card">
                <div class="card-icon">📅</div>
                <div class="card-content">
                  <div class="card-label">年龄范围</div>
                  <div class="card-value">{{ centerData.minAge }}-{{ centerData.maxAge }}岁</div>
                </div>
              </div>
              <div class="data-card">
                <div class="card-icon">🏨</div>
                <div class="card-content">
                  <div class="card-label">主要医院</div>
                  <div class="card-value">{{ centerData.maxHos }}</div>
                </div>
              </div>
            </div>

            <!-- 2. 核心图表网格 -->
            <div class="chart-grid">
              <!-- 左侧区域 -->
              <div class="chart-item chart-item-1">
                <div class="chart-header">
                  <div class="title">{{ isMaternalData ? '各孕周分布' : '各年龄段患病占比' }}</div>
                </div>
                <div class="chart-body">
                  <div id="firstChart" class="chart-container"></div>
                </div>
              </div>

              <div class="chart-item chart-item-2">
                <div class="chart-header">
                  <div class="title">{{ isMaternalData ? '风险等级分布' : '疾病类型分布' }}</div>
                </div>
                <div class="chart-body">
                  <div class="dv-chart-wrapper">
                    <dv-capsule-chart :config="config1" style="width: 100%; height: 100px" />
                  </div>
                </div>
              </div>

              <div class="chart-item chart-item-3">
                <div class="chart-header">
                  <div class="title">{{ isMaternalData ? '风险等级分析' : '医院科室分布' }}</div>
                </div>
                <div class="chart-body">
                  <div id="secondChart" class="chart-container"></div>
                </div>
              </div>

              <div class="chart-item chart-item-4">
                <div class="chart-header">
                  <div class="title">{{ isMaternalData ? '健康指标分析' : '疾病趋势分析' }}</div>
                </div>
                <div class="chart-body">
                  <div id="thirdChart" class="chart-container"></div>
                </div>
              </div>

              <div class="chart-item chart-item-5">
                <div class="chart-header">
                  <div class="title">{{ isMaternalData ? '妊娠类型统计' : '男女性别患病对比' }}</div>
                </div>
                <div class="chart-body">
                  <div class="mini-charts">
                    <div class="mini-chart-item">
                      <dv-active-ring-chart :config="config3" style="width: 100%; height: 80px" />
                    </div>
                    <div class="mini-chart-item">
                      <dv-water-level-pond :config="config4" style="width: 100%; height: 80px" />
                    </div>
                    <div class="mini-chart-item">
                      <dv-active-ring-chart :config="config3" style="width: 100%; height: 80px" />
                    </div>
                  </div>
                </div>
              </div>

              <div class="chart-item chart-item-6">
                <div class="chart-header">
                  <div class="title">{{ isMaternalData ? '孕产妇信息列表' : '病例列表' }}</div>
                </div>
                <div class="chart-body">
                  <div class="data-list">
                    <ul class="cases_list">
                      <li class="list-header">
                        <template v-if="isMaternalData">
                          <div>编号</div>
                          <div>姓名</div>
                          <div>年龄</div>
                          <div>孕周</div>
                          <div>风险等级</div>
                        </template>
                        <template v-else>
                          <div>编号</div>
                          <div>求诊类型</div>
                          <div>性别</div>
                          <div>年龄</div>
                          <div>身高</div>
                        </template>
                      </li>
                      <li v-for="(caseData, index) in casesData" :key="index" class="list-item">
                        <template v-if="isMaternalData">
                          <div>{{ caseData.id || '-' }}</div>
                          <div>{{ caseData.name || '-' }}</div>
                          <div>{{ caseData.age || '-' }}</div>
                          <div>{{ caseData.gestational_week || '-' }}</div>
                          <div>{{ caseData.risk_level || '-' }}</div>
                        </template>
                        <template v-else>
                          <div>{{ caseData[0] || '-' }}</div>
                          <div>{{ caseData[1] || '-' }}</div>
                          <div>{{ caseData[2] || '-' }}</div>
                          <div>{{ caseData[3] || '-' }}</div>
                          <div>{{ caseData[10] || '-' }}</div>
                        </template>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>


            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import $ from "jquery";
import LeftTop from "@/components/LeftTop.vue";
function formatter(number) {
  const numbers = number.toString().split("").reverse();
  const segs = [];

  while (numbers.length) segs.push(numbers.splice(0, 3).join(""));

  return segs.join(",").split("").reverse().join("");
}
export default {
  name: "Index",
  components: {
    LeftTop,
  },
  data() {
      return {
        currentIndex: 0,
        config1: {
          data: [
            {
              name: "已处理",
              value: 80,
            },
            {
              name: "未处理",
              value: 20,
            },
          ],
          color: ["#43b983", "#ff85a2"],
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          gradientColor: true,
        },
        config2: {
          data: {
            value: 70,
            name: "正常数据",
          },
          backgroundColor: ["#5cdbd3", "#43b983"],
          height: 20,
        },
        config3: {
          data: [
            {
              name: "正常",
              value: 60,
            },
            {
              name: "异常",
              value: 40,
            },
          ],
          color: ["#43b983", "#ff85a2"],
          innerRadius: 0.65,
        },
        config4: {
          data: [70],
          min: 0,
          max: 100,
          color: ["#43b983", "#ff85a2"],
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          textStyle: {
            color: "#43b983",
          },
          animation: true,
        },
        casesData: [],
        centerData: {
          maxNum: 100,
          maxType: "感冒",
          maxDep: "内科",
          maxAge: 80,
          minAge: 1,
          maxHos: "总医院",
        },
        isMaternalData: true,
        // 图表实例变量
        firstChartInstance: null,
        secondChartInstance: null,
        thirdChartInstance: null,
    };
  },
  mounted() {
      // 确保页面完全加载后初始化图表
      setTimeout(() => {
        this.initCharts();
      }, 500);
      
      this.getData();
    },
  methods: {
    initCharts() {
      // 直接调用图表初始化方法
      this.initFirstChart();
      this.initSecondChart();
      this.initThirdChart();
      
      // 添加窗口大小改变时的图表调整
      window.addEventListener('resize', this.resizeCharts);
    },
    
    // 调整图表大小
    resizeCharts() {
      // 调整所有图表大小
      if (this.firstChartInstance) this.firstChartInstance.resize();
      if (this.secondChartInstance) this.secondChartInstance.resize();
      if (this.thirdChartInstance) this.thirdChartInstance.resize();
    },
    
    // 初始化第一个图表（柱状图）
    initFirstChart() {
      console.log('初始化第一个图表');
      const chartDom = document.getElementById('firstChart');
      console.log('firstChart容器存在:', !!chartDom);
      if (chartDom && this.$echarts) {
        // 清除容器内容，确保echarts能够正常渲染
        chartDom.innerHTML = '';
        const echarts = this.$echarts;
        if (!echarts) {
          console.error('echarts未正确加载');
          return;
        }
        
        const myChart = echarts.init(chartDom);
        this.firstChartInstance = myChart;
        
        const option = {
          backgroundColor: 'transparent',
          title: {
            text: this.isMaternalData ? '各孕周分布' : '各年龄段患病占比',
            textStyle: {
              color: '#fff',
              fontSize: 14
            },
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            top: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: this.isMaternalData ? ['1-12周', '13-24周', '25-36周', '37-40周', '40周以上'] : ['0-18岁', '19-30岁', '31-45岁', '46-60岁', '60岁以上'],
            axisLine: {
              lineStyle: {
                color: 'rgba(255, 255, 255, 0.5)'
              }
            },
            axisLabel: {
              color: 'rgba(255, 255, 255, 0.7)',
              rotate: 30
            }
          },
          yAxis: {
            type: 'value',
            name: '人数',
            nameTextStyle: {
              color: 'rgba(255, 255, 255, 0.7)'
            },
            axisLine: {
              lineStyle: {
                color: 'rgba(255, 255, 255, 0.5)'
              }
            },
            axisLabel: {
              color: 'rgba(255, 255, 255, 0.7)'
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          },
          series: [
            {
              name: this.isMaternalData ? '产检人数' : '患病人数',
              type: 'bar',
              barWidth: '60%',
              data: [120, 200, 150, 80, 60],
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  {offset: 0, color: '#ff69b4'},
                  {offset: 1, color: '#ff85a2'}
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    {offset: 0, color: '#ff85a2'},
                    {offset: 1, color: '#ff69b4'}
                  ])
                }
              }
            }
          ]
        };
        myChart.setOption(option);
        // 响应式调整
        window.addEventListener('resize', () => {
          myChart.resize();
        });
      }
    },
    
    // 初始化第二个图表（环形图）
    initSecondChart() {
      console.log('初始化第二个图表');
      const chartDom = document.getElementById('secondChart');
      console.log('secondChart容器存在:', !!chartDom);
      if (chartDom && this.$echarts) {
          // 清除容器内容，确保echarts能够正常渲染
          chartDom.innerHTML = '';
          // 确保echarts可用
          const echarts = this.$echarts;
          // 确保容器尺寸正确并添加GPU加速
          chartDom.style.width = '100%';
          chartDom.style.height = '100%';
          chartDom.style.transform = 'translateZ(0)';
          chartDom.style.willChange = 'transform';
          // 创建图表实例，严格控制渲染参数
          const myChart = echarts.init(chartDom, null, {
            renderer: 'canvas',
            useDirtyRect: false
          });
          this.secondChartInstance = myChart;
          
          const option = {
          backgroundColor: 'transparent',
          title: {
            text: this.isMaternalData ? '风险等级分析' : '医院科室分布',
            textStyle: {
              color: '#fff',
              fontSize: 14
            },
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            borderColor: '#ff69b4',
            textStyle: {
              color: '#fff'
            }
          },
          legend: {
            orient: 'horizontal',
            bottom: 30,
            left: 'center',
            textStyle: {
              color: '#fff',
              fontSize: 8
            },
            itemWidth: 8,
            itemHeight: 8,
            itemGap: 10
          },
          series: [{
            name: this.isMaternalData ? '风险等级' : '科室分布',
              type: 'pie',
              radius: ['35%', '40%'],
              center: ['50%', '38%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 8,
              borderColor: 'rgba(255, 255, 255, 0.3)',
              borderWidth: 2
            },
            label: {
              show: false
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '12',
                fontWeight: 'bold',
                color: '#fff'
              },
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            labelLine: {
              show: false
            },
            data: this.isMaternalData ? [
              { value: 335, name: '低风险' },
              { value: 310, name: '中风险' },
              { value: 234, name: '高风险' },
              { value: 135, name: '极高风险' }
            ] : [
              { value: 350, name: '内科' },
              { value: 280, name: '外科' },
              { value: 220, name: '妇产科' },
              { value: 180, name: '儿科' },
              { value: 150, name: '其他' }
            ],
            color: this.isMaternalData ? 
              ['#52c41a', '#faad14', '#fa8c16', '#f5222d'] :
              ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']
          }]
        };
        myChart.setOption(option);
        window.addEventListener('resize', () => {
          myChart.resize();
        });
      }
    },
    
    // 初始化第三个图表（折线图）
    initThirdChart() {
      console.log('初始化第三个图表');
      const chartDom = document.getElementById('thirdChart');
      console.log('thirdChart容器存在:', !!chartDom);
      if (chartDom && this.$echarts) {
          // 清除容器内容，确保echarts能够正常渲染
          chartDom.innerHTML = '';
          // 确保echarts可用
          const echarts = this.$echarts;
          // 确保容器尺寸正确并添加GPU加速
          chartDom.style.width = '100%';
          chartDom.style.height = '100%';
          chartDom.style.transform = 'translateZ(0)';
          chartDom.style.willChange = 'transform';
          // 创建图表实例，严格控制渲染参数
          const myChart = echarts.init(chartDom, null, {
            renderer: 'canvas',
            useDirtyRect: false
          });
          this.thirdChartInstance = myChart;
          
          const option = {
          backgroundColor: 'transparent',
          title: {
            text: this.isMaternalData ? '健康指标分析' : '疾病趋势分析',
            textStyle: {
              color: '#fff',
              fontSize: 14
            },
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            borderColor: '#ff69b4',
            textStyle: {
              color: '#fff'
            }
          },
          legend: {
            data: this.isMaternalData ? ['血压', '血糖'] : ['新增病例', '累计病例'],
            bottom: 20,
            textStyle: {
              color: '#fff',
              fontSize: 10
            },
            itemWidth: 12,
            itemHeight: 12,
            itemGap: 15
          },
          grid: {
            left: '8%',
            right: '8%',
            bottom: '25%',
            top: '20%',
            containLabel: true
          },
          xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['1月', '2月', '3月', '4月', '5月', '6月'],
        axisLine: {
          lineStyle: {
            color: '#ff69b4',
            width: 1
          }
        },
        axisLabel: {
          color: '#fff',
          fontSize: 10,
          interval: 0,
          rotate: 0
        }
      },
          yAxis: {
        type: 'value',
        name: this.isMaternalData ? '指标值' : '病例数',
        nameTextStyle: {
          color: '#fff',
          fontSize: 10
        },
        axisLine: {
          lineStyle: {
            color: '#ff69b4',
            width: 1
          }
        },
        axisLabel: {
          color: '#fff',
          fontSize: 10
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(255, 105, 180, 0.2)',
            width: 1
          }
        }
      },
          series: [
            {
              name: this.isMaternalData ? '血压' : '新增病例',
              type: 'line',
              stack: 'Total',
              data: this.isMaternalData ? 
                [120, 132, 101, 134, 90, 230] :
                [120, 150, 180, 160, 200, 220],
              lineStyle: {
                color: '#ff69b4',
                width: 4
              },
              itemStyle: {
                color: '#ff69b4',
                borderWidth: 2
              },
              symbol: 'circle',
              symbolSize: 6,
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(255, 105, 180, 0.8)' },
                  { offset: 1, color: 'rgba(255, 105, 180, 0.1)' }
                ])
              },
              smooth: true,
              emphasis: {
                focus: 'series',
                lineStyle: {
                  width: 5
                },
                itemStyle: {
                  symbolSize: 8
                }
              }
            },
            {
              name: this.isMaternalData ? '血糖' : '累计病例',
              type: 'line',
              stack: 'Total',
              data: this.isMaternalData ? 
                [220, 182, 191, 234, 290, 330] :
                [120, 270, 450, 610, 810, 1030],
              lineStyle: {
                color: '#87cefa',
                width: 4
              },
              itemStyle: {
                color: '#87cefa',
                borderWidth: 2
              },
              symbol: 'circle',
              symbolSize: 6,
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(135, 206, 250, 0.8)' },
                  { offset: 1, color: 'rgba(135, 206, 250, 0.1)' }
                ])
              },
              smooth: true,
              emphasis: {
                focus: 'series',
                lineStyle: {
                  width: 5
                },
                itemStyle: {
                  symbolSize: 8
                }
              }
            }
          ]
        };
        myChart.setOption(option);
        window.addEventListener('resize', () => {
          myChart.resize();
        });
      }
    },
    

    
    // 所有图表初始化方法已在上方实现
    getData() {
      // 模拟数据
      const mockCases = [
        { id: "001", name: "张女士", age: 28, gestational_week: 24, risk_level: "低风险" },
        { id: "002", name: "李女士", age: 32, gestational_week: 18, risk_level: "中风险" },
        { id: "003", name: "王女士", age: 25, gestational_week: 30, risk_level: "低风险" },
        { id: "004", name: "陈女士", age: 35, gestational_week: 12, risk_level: "高风险" },
        { id: "005", name: "刘女士", age: 29, gestational_week: 26, risk_level: "低风险" },
      ];
      
      const mockCenterData = [
        { name: "低风险", value: 65 },
        { name: "中风险", value: 25 },
        { name: "高风险", value: 10 }
      ];
      
      // 初始化使用模拟数据
      this.casesData = mockCases;
      this.centerData = mockCenterData;
      
      // 实际项目中应该从API获取数据
      $.ajax({
        type: "GET",
        url: "http://localhost:8081/getHomeData",
        dataType: "json",
        success: (res) => {
          if (res.code === 200) {
            // 只有当API返回有效数据时才使用API数据
            if (res.data.casesData && res.data.casesData.length > 0) {
              this.casesData = res.data.casesData;
            }
            if (res.data.circleData && res.data.circleData.length > 0) {
              this.centerData = res.data.circleData;
            }
            // 更新图表配置
          }
        },
        error: (err) => {
          console.error("获取数据失败:", err);
          // 使用模拟数据（已在初始化时设置）
        },
      });
    },
  },
};
</script>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20px;
  overflow-x: auto;
  overflow-y: auto;
}

/* 页面过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 主容器样式 */
.naca {
  width: 100%;
  min-height: calc(100vh - 40px);
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

/* 头部样式 */
.index-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.header-title {
  width: 180px;
  color: #ff69b4;
  font-size: 20px;
  padding: 0 15px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(255, 105, 180, 0.3);
  text-align: center;
}

/* 内容区域 - 网格布局 */
.index-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: 600px;
}

/* 数据卡片网格 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 10px;
}

.data-card {
  background: linear-gradient(135deg, rgba(255, 105, 180, 0.1), rgba(255, 133, 162, 0.05));
  border: 1px solid rgba(255, 133, 162, 0.3);
  border-radius: 10px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.1);
}

.data-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.2);
  border-color: rgba(255, 133, 162, 0.5);
}

.card-icon {
  font-size: 32px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 105, 180, 0.2);
  border-radius: 50%;
}

.card-content {
  flex: 1;
}

.card-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 5px;
}

.card-value {
  font-size: 18px;
  font-weight: bold;
  color: #ff69b4;
}

/* 图表网格布局 */
.chart-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: auto auto auto;
  gap: 20px;
  min-height: calc(100vh - 250px);
  height: auto;
}

.chart-item {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  border: 1px solid rgba(255, 133, 162, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.1);
  min-height: 320px;
}

.chart-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.2);
  border-color: rgba(255, 133, 162, 0.5);
}

/* 图表位置和大小 */
.chart-item-1 {
  grid-column: 1 / 5;
  grid-row: 1 / 2;
  min-height: 320px;
}

.chart-item-2 {
  grid-column: 5 / 9;
  grid-row: 1 / 2;
  min-height: 320px;
}

.chart-item-3 {
  grid-column: 9 / 13;
  grid-row: 1 / 2;
  min-height: 320px;
}

.chart-item-4 {
  grid-column: 1 / 7;
  grid-row: 2 / 3;
  min-height: 400px;
}

.chart-item-5 {
  grid-column: 7 / 13;
  grid-row: 2 / 3;
  min-height: 320px;
}

.chart-item-6 {
    grid-column: 1 / 13;
    grid-row: 3 / 4;
    min-height: 300px;
  }

/* 图表头部 */
.chart-header {
  padding: 10px 15px;
  border-bottom: 1px solid rgba(255, 133, 162, 0.2);
  background: rgba(255, 105, 180, 0.05);
}

/* 图表标题 */
.title {
  color: #ff69b4;
  font-size: 14px;
  font-weight: bold;
  text-align: center;
  text-shadow: 0 2px 4px rgba(255, 105, 180, 0.3);
  letter-spacing: 0.5px;
}

/* 图表主体 */
.chart-body {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* ECharts容器 */
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 240px;
  background: linear-gradient(135deg, rgba(255, 105, 180, 0.1), rgba(255, 133, 162, 0.05));
  border-radius: 8px;
  border: 1px solid rgba(255, 133, 162, 0.2);
  box-shadow: 0 2px 10px rgba(255, 105, 180, 0.1);
}

/* 迷你图表容器 */
.mini-charts {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  height: 100%;
  gap: 10px;
}

.mini-chart-item {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

/* 数据列表 */
.data-list {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.cases_list {
  list-style: none;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: auto;
  border-radius: 8px;
}

/* 列表头部 */
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  background: rgba(255, 133, 162, 0.2);
  border-radius: 8px 8px 0 0;
  font-weight: bold;
  color: #ff69b4;
  font-size: 14px;
  position: sticky;
  top: 0;
  z-index: 10;
}

/* 列表项 */
.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #eeecec;
  font-size: 13px;
  transition: background-color 0.2s ease;
}

.list-item:hover {
  background: rgba(255, 133, 162, 0.05);
}

.list-header div,
.list-item div {
  flex: 1;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 0 10px;
}

/* 自定义滚动条样式 */
.cases_list::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.cases_list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.cases_list::-webkit-scrollbar-thumb {
  background: rgba(255, 133, 162, 0.5);
  border-radius: 4px;
}

.cases_list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 133, 162, 0.7);
}

/* 响应式设计 */
@media (max-width: 1400px) {
    .chart-grid {
      grid-template-columns: repeat(8, 1fr);
      grid-template-rows: auto auto auto auto;
      min-height: calc(100vh - 200px);
      height: auto;
    }
    
    .chart-item-1 {
      grid-column: 1 / 5;
      grid-row: 1 / 2;
      min-height: 300px;
    }
    
    .chart-item-2 {
      grid-column: 5 / 9;
      grid-row: 1 / 2;
      min-height: 300px;
    }
    
    .chart-item-3 {
      grid-column: 1 / 9;
      grid-row: 2 / 3;
      min-height: 380px;
    }
    
    .chart-item-4 {
      grid-column: 1 / 5;
      grid-row: 3 / 4;
      min-height: 350px;
    }
    
    .chart-item-5 {
      grid-column: 5 / 9;
      grid-row: 3 / 4;
      min-height: 300px;
    }
    
    .chart-item-6 {
      grid-column: 1 / 9;
      grid-row: 4 / 5;
      min-height: 300px;
    }
  }

@media (max-width: 1024px) {
    .chart-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(6, auto);
      height: auto;
      min-height: calc(100vh - 200px);
    }
    
    .chart-item-1,
    .chart-item-2,
    .chart-item-3,
    .chart-item-4,
    .chart-item-5,
    .chart-item-6 {
      grid-column: 1 / 2;
      grid-row: auto;
      min-height: 320px;
    }
    
    /* 线条图表增加额外高度 */
    .chart-item-3,
    .chart-item-4 {
      min-height: 400px;
    }
    
    .card-grid {
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }
  }

@media (max-width: 768px) {
  .naca {
    padding: 15px;
  }
  
  .home {
    padding: 10px;
  }
  
  .index-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .dv-decoration-10 {
    width: 200px !important;
  }
  
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
  
  .mini-charts {
    flex-direction: column;
    gap: 20px;
  }
}

/* 加载动画 */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #ff69b4;
}

/* 动画效果 */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 133, 162, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 133, 162, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 133, 162, 0);
  }
}

/* 按钮样式 */
button {
  background: linear-gradient(45deg, #ff85a2, #ff69b4);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  font-size: 14px;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
}

button:active {
  transform: translateY(0);
}
</style>
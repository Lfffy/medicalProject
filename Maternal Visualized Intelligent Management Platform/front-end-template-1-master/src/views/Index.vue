<template>
  <div class="home">
    <transition name="fade" mode="out-in">
      <div key="content">
        <dv-loading v-if="!config4.data.length">Loading...</dv-loading>
        <div class="naca">
          <div class="index-header" style="margin-top: 5px">
            <div>
              <dv-decoration-10 style="width: 450px; height: 1px; margin-bottom: 45px" />
              <dv-decoration-8 style="width: 180px; height: 50px" :color="['#ff85a2', '#ffb6c1']" />
              <div style="width: 150px; color: #ff69b4; font-size: 18px; padding: 0 15px; font-weight: bold; text-shadow: 2px 2px 4px rgba(255, 105, 180, 0.3);">
                {{ isMaternalData ? '孕产妇健康管理' : '医疗疾病数据' }}
              </div>
              <dv-decoration-8 :reverse="true" style="width: 180px; height: 50px" :color="['#ff85a2', '#ffb6c1']" />
              <dv-decoration-10 style="width: 450px; height: 1px; transform: rotateY(180deg); margin-bottom: 45px;" />
            </div>
            <dv-decoration-5 style="width: 10%; height: 20px" :color="['#ff85a2', '#ffb6c1']" />
          </div>

          <div class="index-content">
            <div class="left">
              <div class="left-1">
                <div class="chart-container">
                  <div style="padding: 5px">
                    <div class="title" style="margin-top: 5px">
                      {{ isMaternalData ? '各孕周分布' : '各年龄段患病占比' }}
                    </div>
                    <div id="firstChart" style="width: 100%; height: 200px; background: linear-gradient(135deg, rgba(255, 105, 180, 0.2), rgba(255, 133, 162, 0.1)); border: 2px solid #ff69b4; border-radius: 10px; box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);"></div>
                  </div>
                </div>
                
                <div class="chart-container">
                  <div style="padding: 5px; padding-bottom: 30px">
                    <div class="title" style="margin-top: 1px">
                      {{ isMaternalData ? '风险等级分布' : '疾病类型分布' }}
                    </div>
                    <dv-capsule-chart :config="config1" style="width: 80%; height: 110px" />
                  </div>
                </div>

                <div class="chart-container">
                  <div style="padding: 15px">
                    <div class="title" style="margin-top: 5px">{{ isMaternalData ? '孕产妇信息列表' : '病例列表' }}</div>
                    <div class="row_list">
                      <ul class="cases_list" style="width: 100%; height: 159px; overflow: auto">
                        <li style="font-size: 15px">
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
                        <li v-for="(caseData, index) in casesData" :key="index">
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
            
            <div class="cents">
              <div class="above">
                <div class="aboveOne">
                  <div style="padding: 15px">
                    <div class="title">{{ isMaternalData ? '孕产妇健康数据信息' : '疾病数据信息' }}</div>
                    <div style="display: flex; flex-direction: column; width: 100%; height: 120px; color: #eeecec;">
                      <div style="display: flex; flex: 1">
                        <dv-decoration-11 style="height: 60px; text-align: center;">
                          <div style="flex: 1; color: #ff69b4">👶 就诊人数:{{ centerData.maxNum }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height: 60px; text-align: center;">
                          <div style="flex: 1; color: #ff69b4">❤️ 常见症状:{{ centerData.maxType }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height: 60px; text-align: center;">
                          <div style="flex: 1; color: #ff69b4">🏥 就诊科室:{{ centerData.maxDep }}</div>
                        </dv-decoration-11>
                      </div>
                      <div style="display: flex; flex: 1">
                        <dv-decoration-11 style="height: 60px; text-align: center;">
                          <div style="flex: 1; color: #ff69b4">📅 最大年龄:{{ centerData.maxAge }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height: 60px; text-align: center;">
                          <div style="flex: 1; color: #ff69b4">📅 最小年龄:{{ centerData.minAge }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height: 60px; text-align: center;">
                          <div style="flex: 1; color: #ff69b4">🏥 就诊医院:{{ centerData.maxHos }}</div>
                        </dv-decoration-11>
                      </div>
                    </div>
                  </div>
                  
                  <div style="padding: 15px">
                    <div class="title" style="margin-top: -30px">
                      {{ isMaternalData ? '妊娠类型统计' : '男女性别患病对比' }}
                    </div>
                    <div class="content">
                      <dv-active-ring-chart :config="config3" style="width: 150px; height: 100px" />
                      <dv-water-level-pond :config="config4" style="width: 100px; height: 90px" />
                      <dv-active-ring-chart :config="config3" style="width: 150px; height: 100px" />
                    </div>
                  </div>
                </div>
                
                <div class="aboveTwo">
                  <div class="chart-container" style="border-color: #ff85a2;">
                    <div style="padding: 15px">
                      <div class="title" style="margin-top: 5px">
                        {{ isMaternalData ? '风险等级分析' : '医院科室环形图' }}
                      </div>
                      <div style="width: calc(100% - 20px); height: 300px; margin: 0 auto; overflow: hidden; border-radius: 10px; position: relative; clip-path: inset(5px 5px 20px 5px); border: 2px solid transparent; background-clip: padding-box;">
                        <div id="secondChart" style="width: 100%; height: 100%; padding: 15px 10px 50px 10px; background: linear-gradient(135deg, rgba(255, 105, 180, 0.2), rgba(255, 133, 162, 0.1)); border-radius: 8px; box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3); box-sizing: border-box;"></div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="chart-container">
                    <div style="padding: 5px">
                      <div class="title" style="margin-top: 5px">
                        {{ isMaternalData ? '健康指标分析' : '疾病关键词云图' }}
                      </div>
                      <div style="width: calc(100% - 20px); height: 300px; margin: 0 auto; overflow: hidden; border-radius: 10px; position: relative; clip-path: inset(5px 5px 20px 5px); border: 2px solid transparent; background-clip: padding-box;">
                        <div id="thirdChart" style="width: 100%; height: 100%; padding: 15px 10px 50px 10px; background: linear-gradient(135deg, rgba(255, 105, 180, 0.2), rgba(255, 133, 162, 0.1)); border-radius: 8px; box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3); box-sizing: border-box;"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="below">
                <div class="chart-container">
                  <div style="padding: 7px">
                    <div class="title" style="margin-top: 5px; color: #ff85a2">
                      孕期健康指标追踪
                    </div>
                    <div id="fourthChart" style="width: 100%; height: 300px; margin-top: 25px; background: linear-gradient(135deg, rgba(255, 105, 180, 0.2), rgba(255, 133, 162, 0.1)); border: 2px solid #ff69b4; border-radius: 10px; box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);"></div>
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
        fourthChartInstance: null,
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
      this.initFourthChart();
      
      // 添加窗口大小改变时的图表调整
      window.addEventListener('resize', this.resizeCharts);
    },
    
    // 调整图表大小
    resizeCharts() {
      // 调整所有图表大小
      if (this.firstChartInstance) this.firstChartInstance.resize();
      if (this.secondChartInstance) this.secondChartInstance.resize();
      if (this.thirdChartInstance) this.thirdChartInstance.resize();
      if (this.fourthChartInstance) this.fourthChartInstance.resize();
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
            bottom: 30,
            textStyle: {
              color: '#fff',
              fontSize: 8
            },
            itemWidth: 8,
            itemHeight: 8,
            itemGap: 10
          },
          grid: {
            left: '12%',
            right: '12%',
            bottom: '40%',
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
                width: 3
              },
              itemStyle: {
                color: '#ff69b4'
              },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(255, 105, 180, 0.8)' },
                  { offset: 1, color: 'rgba(255, 105, 180, 0.1)' }
                ])
              },
              smooth: true
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
                width: 3
              },
              itemStyle: {
                color: '#87cefa'
              },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(135, 206, 250, 0.8)' },
                  { offset: 1, color: 'rgba(135, 206, 250, 0.1)' }
                ])
              },
              smooth: true
            }
          ]
        };
        myChart.setOption(option);
        window.addEventListener('resize', () => {
          myChart.resize();
        });
      }
    },
    
    // 初始化第四个图表（面积图）
    initFourthChart() {
      console.log('初始化第四个图表');
      const chartDom = document.getElementById('fourthChart');
      console.log('fourthChart容器存在:', !!chartDom);
      if (chartDom && this.$echarts) {
          // 清除容器内容，确保echarts能够正常渲染
          chartDom.innerHTML = '';
          // 确保echarts可用
          const echarts = this.$echarts;
          const myChart = echarts.init(chartDom);
          this.fourthChartInstance = myChart;
          
          const option = {
          backgroundColor: 'transparent',
          title: {
            text: '孕期健康指标追踪',
            textStyle: {
              color: '#fff',
              fontSize: 16
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
            data: ['体重', '血压', '血糖'],
            bottom: 20,
            textStyle: {
              color: '#fff',
              fontSize: 14
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
            boundaryGap: false,
            data: ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周', '第7周', '第8周', '第9周', '第10周', '第11周', '第12周'],
            axisLine: {
              lineStyle: {
                color: 'rgba(255, 255, 255, 0.5)'
              }
            },
            axisLabel: {
              color: 'rgba(255, 255, 255, 0.7)',
              rotate: 45
            }
          },
          yAxis: [
            {
              type: 'value',
              name: '体重/血压',
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
            {
              type: 'value',
              name: '血糖',
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
              }
            }
          ],
          series: [
            {
              name: '体重',
              type: 'line',
              stack: '总量',
              data: [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71],
              lineStyle: {
                color: '#ff69b4',
                width: 3
              },
              itemStyle: {
                color: '#ff69b4'
              },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(255, 105, 180, 0.8)' },
                  { offset: 1, color: 'rgba(255, 105, 180, 0.1)' }
                ])
              },
              smooth: true
            },
            {
              name: '血压',
              type: 'line',
              stack: '总量',
              data: [110, 112, 115, 118, 120, 122, 125, 128, 130, 132, 135, 138],
              lineStyle: {
                color: '#87cefa',
                width: 3
              },
              itemStyle: {
                color: '#87cefa'
              },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(135, 206, 250, 0.8)' },
                  { offset: 1, color: 'rgba(135, 206, 250, 0.1)' }
                ])
              },
              smooth: true
            },
            {
              name: '血糖',
              type: 'line',
              yAxisIndex: 1,
              data: [5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1],
              lineStyle: {
                color: '#32cd32',
                width: 3
              },
              itemStyle: {
                color: '#32cd32'
              },
              smooth: true
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
      
      this.casesData = mockCases;
      
      // 实际项目中应该从API获取数据
      $.ajax({
        type: "GET",
        url: "/api/getHomeData",
        dataType: "json",
        success: (res) => {
          if (res.code === 200) {
            this.casesData = res.data.casesData || [];
            this.centerData = res.data.center || this.centerData;
            // 更新图表配置
          }
        },
        error: (err) => {
          console.error("获取数据失败:", err);
          // 使用模拟数据
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
  transition: opacity 0.5s;
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
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

/* 头部样式 */
.index-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.index-header > div:first-child {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

/* 内容区域样式 */
.index-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  min-height: 600px;
}

/* 左侧区域 */
.left {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.left-1 {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

/* 中央区域 */
.cents {
  flex: 2;
  min-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.above {
  display: flex;
  gap: 20px;
  height: 50%;
}

.aboveOne {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.aboveTwo {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.below {
  height: 50%;
}

/* 图表容器样式 */
.chart-container {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid rgba(255, 133, 162, 0.3);
  transition: all 0.3s ease;
  min-height: 150px;
  margin-bottom: 10px;
}

.chart-container:hover {
  border-color: rgba(255, 133, 162, 0.6);
  box-shadow: 0 4px 20px rgba(255, 133, 162, 0.2);
  transform: translateY(-2px);
}

/* 标题样式 */
.title {
  color: #ff69b4;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  text-shadow: 0 2px 4px rgba(255, 105, 180, 0.3);
  letter-spacing: 1px;
}

/* 内容区域样式 */
.content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100px;
}

/* 列表样式 */
.row_list {
  height: calc(100% - 40px);
  overflow: hidden;
}

.cases_list {
  list-style: none;
  width: 100%;
  max-height: 250px;
  overflow-y: auto;
  overflow-x: auto;
  border-radius: 5px;
  border: 1px solid rgba(255, 133, 162, 0.3);
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

.cases_list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #eeecec;
}

.cases_list li:first-child {
  background: rgba(255, 133, 162, 0.2);
  padding: 10px 0;
  border-radius: 5px;
  font-weight: bold;
  color: #ff69b4;
}

.cases_list li div {
  flex: 1;
  text-align: center;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 0 5px;
}

/* 滚动条样式 */
.cases_list::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.cases_list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.cases_list::-webkit-scrollbar-thumb {
  background: rgba(255, 133, 162, 0.5);
  border-radius: 3px;
}

.cases_list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 133, 162, 0.8);
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .index-content {
    flex-direction: column;
  }
  
  .above {
    flex-direction: column;
  }
  
  .chart-container {
    min-height: 200px;
  }
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

/* 加载动画 */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

/* 按钮样式 */
button {
  background: linear-gradient(45deg, #ff85a2, #ff69b4);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
}

button:active {
  transform: translateY(0);
}
</style>
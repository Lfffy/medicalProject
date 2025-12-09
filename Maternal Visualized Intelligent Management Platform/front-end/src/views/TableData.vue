<template>
  <div class="tableData-container">
      <div class="table-header">
        <h3>{{ isMaternal ? '孕产妇健康数据表' : '患者医疗数据表' }}</h3>
        <p class="record-info">共 {{ totalRecords }} 条记录</p>
      </div>
      <transition name="fade" mode="out-in">
        <dv-loading v-if="loading">
            数据加载中...
        </dv-loading>
        <div v-else class="content">
          <dv-scroll-board :config="config" style="width:100%;height:600px" />
        </div>
      </transition>
  </div>
</template>

<script>
export default {
    data(){
        return {
            config:{
                header: [],
                data: [],
                index: true,
                align: [],
                headerBGC:"#3077b1",
            },
            tableList:[],
            totalRecords: 0,
            dbFields: [],
            loading: true,
            isMaternal: false
        }
    },
    async created(){
        await this.delay(500)
        this.getTableList()
    },
    methods:{
        delay(ms){
            return new Promise(resolve => setTimeout(resolve, ms));
        },
        async getTableList() {
            console.log('开始获取表格数据...');
            try {
                this.loading = true;
                const res = await this.$http.get('/tableData');
                console.log('TableData响应:', res);
                
                // 安全地访问响应数据
                if (res && res.data && res.data.data) {
                    const data = res.data.data
                    
                    // 检查是否是孕产妇数据
                    this.isMaternal = data.isMaternal || false
                    
                    // 获取表格行数据
                    if (data.rows && Array.isArray(data.rows)) {
                        this.tableList = data.rows
                        this.totalRecords = data.rows.length
                        
                        // 直接使用rows数组（后端已转换为二维数组）
                        this.config.data = data.rows
                        
                        // 设置表头
                        if (data.headers && Array.isArray(data.headers)) {
                            this.config.header = data.headers
                        } else {
                            // 默认表头
                            this.config.header = this.isMaternal ? 
                                ['类型', '性别', '年龄', '时间', '描述', '医生', '医院', '科室', '详情链接', '体重', '血压', '风险等级', '预产期'] : 
                                ['类型', '性别', '年龄', '时间', '描述', '医生', '医院', '科室', '详情链接', '身高', '体重', '患病时长', '过敏史']
                        }
                    } else {
                        // 没有数据时显示默认内容
                        this.config.data = [['暂无数据']]
                        this.config.header = ['信息']
                        this.totalRecords = 0
                    }
                } else {
                    console.warn('响应数据结构不符合预期，使用空数据');
                    this.config.data = [['暂无数据']]
                    this.config.header = ['信息']
                    this.totalRecords = 0
                }
                
                // 设置对齐方式
                this.config.align = this.config.header.map(item => 'center')
                
                console.log('表格数据设置成功:', this.config.data);
                console.log('表头设置:', this.config.header);
            } catch (error) {
                console.error('获取表格数据失败:', error);
                // 出错时使用空数据
                this.config.data = [['获取数据失败，请刷新页面重试']]
                this.config.header = ['错误信息']
                this.config.align = ['center']
                this.totalRecords = 0
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
.content{
    display: flex;
    justify-content: center;
}
.table-header {
  margin-bottom: 20px;
  text-align: center;
}
.record-info {
  color: #666;
  margin-top: 5px;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
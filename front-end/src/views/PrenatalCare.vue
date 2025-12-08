<template>
  <div class="prenatal-care-container">
    <div class="page-header">
      <h2 class="page-title">产检记录管理</h2>
    </div>
    
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="filterForm.name"
            placeholder="孕妇姓名"
            clearable
            class="filter-input"
          ></el-input>
        </el-col>
        <el-col :span="6">
          <el-input
            v-model="filterForm.idCard"
            placeholder="身份证号"
            clearable
            class="filter-input"
          ></el-input>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="filterForm.recordDate"
            type="date"
            placeholder="产检日期"
            value-format="YYYY-MM-DD"
            class="filter-input"
          ></el-date-picker>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch" class="search-btn">
            <i class="el-icon-search"></i> 搜索
          </el-button>
          <el-button @click="resetFilter" class="reset-btn">
            <i class="el-icon-refresh-right"></i> 重置
          </el-button>
        </el-col>
      </el-row>
    </div>
    
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ totalRecords }}</div>
            <div class="stat-label">总记录数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ thisMonthRecords }}</div>
            <div class="stat-label">本月记录</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ normalCount }}</div>
            <div class="stat-label">正常</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-number">{{ abnormalCount }}</div>
            <div class="stat-label">异常</div>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <div class="table-section">
      <el-table
        :data="tableData"
        style="width: 100%"
        stripe
        class="custom-table"
      >
        <el-table-column prop="name" label="孕妇姓名" width="120"></el-table-column>
        <el-table-column prop="idCard" label="身份证号" width="180"></el-table-column>
        <el-table-column prop="age" label="年龄" width="80"></el-table-column>
        <el-table-column prop="gestationalWeek" label="孕周" width="80"></el-table-column>
        <el-table-column prop="recordDate" label="产检日期" width="120"></el-table-column>
        <el-table-column prop="weight" label="体重(kg)" width="100"></el-table-column>
        <el-table-column prop="bloodPressure" label="血压" width="120"></el-table-column>
        <el-table-column prop="fetalHeartRate" label="胎心率(bpm)" width="120"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '正常' ? 'success' : 'danger'">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="viewRecord(scope.row)">
              <i class="el-icon-view"></i> 查看
            </el-button>
            <el-button type="warning" size="small" @click="editRecord(scope.row)">
              <i class="el-icon-edit"></i> 编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteRecord(scope.row)">
              <i class="el-icon-delete"></i> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalRecords"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrenatalCare',
  data() {
    return {
      filterForm: {
        name: '',
        idCard: '',
        recordDate: ''
      },
      tableData: [],
      totalRecords: 0,
      thisMonthRecords: 0,
      normalCount: 0,
      abnormalCount: 0,
      currentPage: 1,
      pageSize: 10
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    loadData() {
      // 模拟数据加载
      this.tableData = [
        {
          id: 1,
          name: '李小红',
          idCard: '110101199001011234',
          age: 32,
          gestationalWeek: 28,
          recordDate: '2023-12-01',
          weight: 65.2,
          bloodPressure: '120/80',
          fetalHeartRate: 145,
          status: '正常'
        },
        {
          id: 2,
          name: '王小花',
          idCard: '110101199202022345',
          age: 30,
          gestationalWeek: 32,
          recordDate: '2023-12-02',
          weight: 72.5,
          bloodPressure: '130/85',
          fetalHeartRate: 150,
          status: '正常'
        },
        {
          id: 3,
          name: '张小丽',
          idCard: '110101198803033456',
          age: 34,
          gestationalWeek: 24,
          recordDate: '2023-12-03',
          weight: 68.8,
          bloodPressure: '140/90',
          fetalHeartRate: 142,
          status: '异常'
        }
      ]
      this.totalRecords = this.tableData.length
      this.thisMonthRecords = this.tableData.length
      this.normalCount = this.tableData.filter(item => item.status === '正常').length
      this.abnormalCount = this.tableData.filter(item => item.status === '异常').length
    },
    handleSearch() {
      // 搜索逻辑
      this.loadData()
    },
    resetFilter() {
      this.filterForm = {
        name: '',
        idCard: '',
        recordDate: ''
      }
      this.loadData()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadData()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadData()
    },
    viewRecord(row) {
      // 查看记录详情
      this.$message.info('查看记录：' + row.name)
    },
    editRecord(row) {
      // 编辑记录
      this.$message.info('编辑记录：' + row.name)
    },
    deleteRecord(row) {
      // 删除记录
      this.$confirm('确定要删除这条记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('删除成功')
        this.loadData()
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    }
  }
}
</script>

<style scoped>
.prenatal-care-container {
  padding: 20px;
  background-color: #fff;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #ff69b4;
}

.page-title {
  color: #ff69b4;
  font-size: 24px;
  margin: 0;
  font-weight: 600;
}

.filter-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fff5f7;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(255, 105, 180, 0.1);
}

.filter-input {
  width: 100%;
}

.search-btn {
  width: 100%;
  background-color: #ff69b4;
  border-color: #ff69b4;
}

.search-btn:hover {
  background-color: #ff85c0;
  border-color: #ff85c0;
}

.reset-btn {
  width: 100%;
  margin-top: 10px;
  border-color: #ff69b4;
  color: #ff69b4;
}

.reset-btn:hover {
  background-color: #fff5f7;
}

.stats-section {
  margin-bottom: 30px;
}

.stat-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(255, 105, 180, 0.1);
  border: 1px solid #ffd6e9;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #ff69b4;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.table-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(255, 105, 180, 0.1);
}

.custom-table {
  width: 100%;
}

.custom-table >>> .el-table__header-wrapper th {
  background-color: #fff5f7;
  color: #ff69b4;
  font-weight: 600;
  border-bottom: 2px solid #ffd6e9;
}

.custom-table >>> .el-table__body-wrapper tr:hover {
  background-color: #fff5f7;
}

.custom-table >>> .el-table__body-wrapper tr.el-table__row--striped {
  background-color: #fff8fb;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.pagination-container >>> .el-pagination.is-background .el-pager li:not(.disabled).active {
  background-color: #ff69b4;
  color: #fff;
}

.pagination-container >>> .el-pagination.is-background .el-pager li:hover {
  color: #ff69b4;
}

.pagination-container >>> .el-pagination__total {
  color: #ff69b4;
}
</style>
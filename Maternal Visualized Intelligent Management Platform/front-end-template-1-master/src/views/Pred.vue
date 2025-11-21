<template>
  <div class="pred-container">
    <div class="pred-header">
      <h2>孕期风险评估</h2>
      <p class="subtitle">智能医疗风险评估系统</p>
    </div>
    <div class="pred-content">
      <div class="left-panel">
        <div class="form-card">
          <div class="card-header">
            <i class="fas fa-user-md"></i>
            <span>基本信息</span>
          </div>
          <div class="form">
            <div class="form-group">
              <div class="form-label">
                <i class="fas fa-birthday-cake"></i>
                年龄
              </div>
              <div class="form-control">
                <input type="number" v-model.number="formSubmit.age" placeholder="请输入年龄">
              </div>
            </div>
            <div class="form-group">
              <div class="form-label">
                <i class="fas fa-baby"></i>
                孕周
              </div>
              <div class="form-control">
                <input type="number" v-model.number="formSubmit.gestational_week" placeholder="请输入孕周">
              </div>
            </div>
            <div class="form-group">
              <div class="form-label">
                <i class="fas fa-weight"></i>
                体重(kg)
              </div>
              <div class="form-control">
                <input type="number" v-model.number="formSubmit.weight" placeholder="请输入体重">
              </div>
            </div>
            <div class="form-group">
              <div class="form-label">
                <i class="fas fa-heartbeat"></i>
                血压
              </div>
              <div class="form-control">
                <input type="text" v-model="formSubmit.blood_pressure" placeholder="格式：120/80">
              </div>
            </div>
            <div class="form-group">
              <div class="form-label">
                <i class="fas fa-users"></i>
                妊娠类型
              </div>
              <div class="form-control">
                <select v-model="formSubmit.pregnancy_type">
                  <option value="单胎">单胎</option>
                  <option value="双胎">双胎</option>
                  <option value="多胎">多胎</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <div class="form-label">
                <i class="fas fa-notes-medical"></i>
                病史
              </div>
              <div class="form-control">
                <input type="text" v-model="formSubmit.medical_history" placeholder="如有高血压、糖尿病等请注明">
              </div>
            </div>
            <div class="form-group button">
              <button type="button" class="submit-btn" @click="submit">
                <i class="fas fa-stethoscope"></i>
                评估风险
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <div class="tips-card">
          <div class="card-header">
            <i class="fas fa-info-circle"></i>
            <span>温馨提示</span>
          </div>
          <div class="card-content">
            <dv-decoration-11 style="width:100%;height:40px;font-size:12px">
              小贴士：仅为初步风险评估，具体请以医生诊断为准
            </dv-decoration-11>
          </div>
        </div>
        
        <div class="result-card">
          <div class="card-header">
            <i class="fas fa-chart-line"></i>
            <span>评估结果</span>
          </div>
          <div class="card-content">
            <dv-border-box-9>
              <div class="result-display">
                {{resultDescription || '暂无信息'}}
              </div>
            </dv-border-box-9>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pred',
  data(){
    return {
      formSubmit:{
        age: 0,
        gestational_week: 0,
        weight: 0,
        blood_pressure: '',
        pregnancy_type: '单胎',
        medical_history: ''
      },
      resultData: "暂无信息",
      resultDescription: ""
    }
  },
  created(){

  },
  methods:{
   async submit(){
    try {
      console.log('提交评估请求:', this.formSubmit);
      const res = await this.$http.post('/submitModel', this.formSubmit)
      console.log('评估响应:', res);
      
      if (res && res.data && res.data.data) {
        this.resultData = res.data.data.result || '暂无信息'
        this.resultDescription = res.data.data.description || ''
      } else {
        this.resultData = '评估失败'
        this.resultDescription = '无法获取评估结果，请检查输入信息'
      }
    } catch (error) {
      console.error('评估过程中出错:', error);
      this.resultData = '评估失败'
      this.resultDescription = '系统错误，请稍后重试'
    }
   }
  },
  components: {
    
  }
}
</script>

<style lang="less" scoped>
.pred-container {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background: linear-gradient(135deg, rgba(255, 105, 180, 0.2), rgba(255, 133, 162, 0.1));
}

.pred-header {
  text-align: center;
  margin-bottom: 30px;
  
  h2 {
    color: #ff69b4;
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 0 2px 4px rgba(255, 105, 180, 0.3);
  }
  
  .subtitle {
    color: #ff69b4;
    font-size: 1.1rem;
  }
}

.pred-content {
  display: flex;
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.left-panel, .right-panel {
  flex: 1;
}

.form-card, .tips-card, .result-card {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 15px;
  box-shadow: 0 8px 32px rgba(255, 105, 180, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 133, 162, 0.3);
  margin-bottom: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.form-card:hover, .tips-card:hover, .result-card:hover {
  border-color: rgba(255, 133, 162, 0.6);
  box-shadow: 0 4px 20px rgba(255, 133, 162, 0.3);
  transform: translateY(-2px);
}

.card-header {
  background: linear-gradient(135deg, #ff85a2, #ff69b4);
  color: white;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  
  i {
    font-size: 1.2rem;
  }
  
  span {
    font-weight: 600;
    font-size: 1.1rem;
  }
}

.form {
  padding: 30px;
}

.form-group {
  margin-bottom: 25px;
  
  .form-label {
    color: #ff69b4;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    
    i {
      color: #ff85a2;
      width: 16px;
    }
  }
  
  .form-control {
    input, select {
      width: 100%;
      padding: 12px 15px;
      border: 2px solid #e1e5e9;
      border-radius: 8px;
      font-size: 1rem;
      transition: all 0.3s ease;
      background: white;
      
      &:focus {
        outline: none;
        border-color: #ff69b4;
        box-shadow: 0 0 0 3px rgba(255, 105, 180, 0.1);
      }
    }
  }
  
  &.button {
    text-align: center;
    margin-top: 30px;
  }
}

.submit-btn {
  background: linear-gradient(135deg, #ff85a2, #ff69b4);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 105, 180, 0.4);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.card-content {
  padding: 20px;
}

.result-display {
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #ff69b4;
  text-align: center;
  line-height: 1.6;
  padding: 20px;
  background: linear-gradient(135deg, rgba(255, 105, 180, 0.1), rgba(255, 133, 162, 0.05));
  border-radius: 10px;
  border: 1px solid rgba(255, 133, 162, 0.3);
}

// 响应式设计
@media (max-width: 768px) {
  .pred-content {
    flex-direction: column;
    gap: 20px;
  }
  
  .pred-header h2 {
    font-size: 2rem;
  }
  
  .form {
    padding: 20px;
  }
}
</style>

<template>
  <div class="maternal-risk-prediction">
    <el-card class="prediction-card">
      <div slot="header" class="card-header">
        <span class="card-title">孕产妇风险预测</span>
        <el-button type="primary" size="small" @click="refreshModels">刷新模型</el-button>
      </div>
      
      <!-- 模型状态 -->
      <el-alert
        v-if="!modelsLoaded"
        title="模型未加载"
        type="warning"
        description="孕产妇风险预测模型尚未加载，请先训练模型或联系管理员"
        show-icon
        :closable="false"
        class="model-status-alert">
      </el-alert>
      
      <!-- 预测表单 -->
      <el-form :model="predictionForm" :rules="formRules" ref="predictionForm" label-width="120px" class="prediction-form">
        <el-row :gutter="20">
          <!-- 基本信息 -->
          <el-col :span="24">
            <h3 class="form-section-title">基本信息</h3>
          </el-col>
          <el-col :span="8">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="predictionForm.age" :min="15" :max="50" placeholder="年龄" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="身高(cm)" prop="height">
              <el-input-number v-model="predictionForm.height" :min="140" :max="200" placeholder="身高" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="体重(kg)" prop="weight">
              <el-input-number v-model="predictionForm.weight" :min="40" :max="120" placeholder="体重" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="BMI" prop="bmi">
              <el-input-number v-model="predictionForm.bmi" :min="15" :max="40" placeholder="BMI" style="width: 100%" disabled></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="产次" prop="parity">
              <el-input-number v-model="predictionForm.parity" :min="0" :max="10" placeholder="产次" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="孕次" prop="pregnancy_count">
              <el-input-number v-model="predictionForm.pregnancy_count" :min="1" :max="15" placeholder="孕次" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          
          <!-- 妊娠信息 -->
          <el-col :span="24">
            <h3 class="form-section-title">妊娠信息</h3>
          </el-col>
          <el-col :span="8">
            <el-form-item label="孕周" prop="gestational_weeks">
              <el-input-number v-model="predictionForm.gestational_weeks" :min="0" :max="42" placeholder="孕周" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="妊娠类型" prop="pregnancy_type">
              <el-select v-model="predictionForm.pregnancy_type" placeholder="请选择妊娠类型" style="width: 100%">
                <el-option label="单胎" value="单胎"></el-option>
                <el-option label="双胎" value="双胎"></el-option>
                <el-option label="多胎" value="多胎"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="末次月经月份" prop="lmp_month">
              <el-select v-model="predictionForm.lmp_month" placeholder="请选择月份" style="width: 100%">
                <el-option v-for="month in 12" :key="month" :label="month + '月'" :value="month"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          
          <!-- 生命体征 -->
          <el-col :span="24">
            <h3 class="form-section-title">生命体征</h3>
          </el-col>
          <el-col :span="8">
            <el-form-item label="收缩压(mmHg)" prop="systolic_pressure">
              <el-input-number v-model="predictionForm.systolic_pressure" :min="80" :max="200" placeholder="收缩压" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="舒张压(mmHg)" prop="diastolic_pressure">
              <el-input-number v-model="predictionForm.diastolic_pressure" :min="40" :max="120" placeholder="舒张压" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="心率(次/分)" prop="heart_rate">
              <el-input-number v-model="predictionForm.heart_rate" :min="50" :max="120" placeholder="心率" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="体温(°C)" prop="temperature">
              <el-input-number v-model="predictionForm.temperature" :min="35" :max="40" :precision="1" placeholder="体温" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="血糖(mmol/L)" prop="blood_sugar">
              <el-input-number v-model="predictionForm.blood_sugar" :min="3" :max="15" :precision="1" placeholder="血糖" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="血红蛋白(g/L)" prop="hemoglobin">
              <el-input-number v-model="predictionForm.hemoglobin" :min="80" :max="160" placeholder="血红蛋白" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          
          <!-- 风险因素 -->
          <el-col :span="24">
            <h3 class="form-section-title">风险因素</h3>
          </el-col>
          <el-col :span="24">
            <el-form-item label="风险因素" prop="risk_factors">
              <el-checkbox-group v-model="predictionForm.risk_factors">
                <el-checkbox label="高血压">高血压</el-checkbox>
                <el-checkbox label="糖尿病">糖尿病</el-checkbox>
                <el-checkbox label="肥胖">肥胖</el-checkbox>
                <el-checkbox label="高龄">高龄</el-checkbox>
                <el-checkbox label="多胎">多胎</el-checkbox>
                <el-checkbox label="既往子痫前期">既往子痫前期</el-checkbox>
                <el-checkbox label="既往妊娠期糖尿病">既往妊娠期糖尿病</el-checkbox>
                <el-checkbox label="吸烟">吸烟</el-checkbox>
                <el-checkbox label="家族史">家族史</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 预测按钮 -->
        <el-form-item style="text-align: center; margin-top: 20px;">
          <el-button type="primary" @click="predictRisks" :loading="predicting">开始预测</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 预测结果 -->
    <el-card v-if="predictionResults" class="results-card">
      <div slot="header" class="card-header">
        <span class="card-title">预测结果</span>
        <el-button type="text" @click="exportResults">导出结果</el-button>
      </div>
      
      <el-tabs v-model="activeTab">
        <!-- 综合风险 -->
        <el-tab-pane label="综合风险评估" name="comprehensive">
          <div class="risk-summary">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="risk-item">
                  <div class="risk-label">综合风险等级</div>
                  <div class="risk-value" :class="getRiskLevelClass(predictionResults.comprehensive.overall_risk_level)">
                    {{ predictionResults.comprehensive.overall_risk_level }}
                  </div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="risk-item">
                  <div class="risk-label">综合风险评分</div>
                  <div class="risk-score">{{ predictionResults.comprehensive.overall_risk_score.toFixed(2) }}</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="risk-item">
                  <div class="risk-label">主要风险因素</div>
                  <div class="risk-factors">
                    <el-tag v-for="factor in predictionResults.comprehensive.main_risk_factors" :key="factor" type="danger" size="small" style="margin-right: 5px; margin-bottom: 5px;">
                      {{ factor }}
                    </el-tag>
                  </div>
                </div>
              </el-col>
            </el-row>
            
            <div class="risk-suggestions">
              <h4>健康建议</h4>
              <ul>
                <li v-for="(suggestion, index) in predictionResults.comprehensive.suggestions" :key="index">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </el-tab-pane>
        
        <!-- 子痫前期风险 -->
        <el-tab-pane label="子痫前期风险" name="preeclampsia">
          <div class="risk-detail">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="risk-chart-container">
                  <div class="risk-chart-title">子痫前期风险评估</div>
                  <div class="risk-gauge" :style="{ background: `conic-gradient(${getGaugeGradient(predictionResults.preeclampsia.risk_level, predictionResults.preeclampsia.risk_probability)})` }">
                    <div class="risk-gauge-center">
                      <div class="risk-gauge-value">{{ (predictionResults.preeclampsia.risk_probability * 100).toFixed(1) }}%</div>
                      <div class="risk-gauge-label">{{ predictionResults.preeclampsia.risk_level }}</div>
                    </div>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="risk-factors-detail">
                  <h4>主要风险因素</h4>
                  <ul>
                    <li v-for="(factor, index) in predictionResults.preeclampsia.main_risk_factors" :key="index">
                      {{ factor }}
                    </li>
                  </ul>
                  
                  <h4>健康建议</h4>
                  <ul>
                    <li v-for="(suggestion, index) in predictionResults.preeclampsia.suggestions" :key="index">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        
        <!-- 妊娠期糖尿病风险 -->
        <el-tab-pane label="妊娠期糖尿病风险" name="gestational_diabetes">
          <div class="risk-detail">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="risk-chart-container">
                  <div class="risk-chart-title">妊娠期糖尿病风险评估</div>
                  <div class="risk-gauge" :style="{ background: `conic-gradient(${getGaugeGradient(predictionResults.gestational_diabetes.risk_level, predictionResults.gestational_diabetes.risk_probability)})` }">
                    <div class="risk-gauge-center">
                      <div class="risk-gauge-value">{{ (predictionResults.gestational_diabetes.risk_probability * 100).toFixed(1) }}%</div>
                      <div class="risk-gauge-label">{{ predictionResults.gestational_diabetes.risk_level }}</div>
                    </div>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="risk-factors-detail">
                  <h4>主要风险因素</h4>
                  <ul>
                    <li v-for="(factor, index) in predictionResults.gestational_diabetes.main_risk_factors" :key="index">
                      {{ factor }}
                    </li>
                  </ul>
                  
                  <h4>健康建议</h4>
                  <ul>
                    <li v-for="(suggestion, index) in predictionResults.gestational_diabetes.suggestions" :key="index">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        
        <!-- 早产风险 -->
        <el-tab-pane label="早产风险" name="preterm_birth">
          <div class="risk-detail">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="risk-chart-container">
                  <div class="risk-chart-title">早产风险评估</div>
                  <div class="risk-gauge" :style="{ background: `conic-gradient(${getGaugeGradient(predictionResults.preterm_birth.risk_level, predictionResults.preterm_birth.risk_probability)})` }">
                    <div class="risk-gauge-center">
                      <div class="risk-gauge-value">{{ (predictionResults.preterm_birth.risk_probability * 100).toFixed(1) }}%</div>
                      <div class="risk-gauge-label">{{ predictionResults.preterm_birth.risk_level }}</div>
                    </div>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="risk-factors-detail">
                  <h4>主要风险因素</h4>
                  <ul>
                    <li v-for="(factor, index) in predictionResults.preterm_birth.main_risk_factors" :key="index">
                      {{ factor }}
                    </li>
                  </ul>
                  
                  <h4>健康建议</h4>
                  <ul>
                    <li v-for="(suggestion, index) in predictionResults.preterm_birth.suggestions" :key="index">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import maternalPredictionService from '../services/maternalPredictionService';

export default {
  name: 'MaternalRiskPrediction',
  data() {
    return {
      modelsLoaded: false,
      predicting: false,
      activeTab: 'comprehensive',
      predictionForm: {
        age: null,
        height: null,
        weight: null,
        bmi: null,
        parity: 0,
        pregnancy_count: 1,
        gestational_weeks: null,
        pregnancy_type: '单胎',
        lmp_month: null,
        systolic_pressure: null,
        diastolic_pressure: null,
        heart_rate: null,
        temperature: null,
        blood_sugar: null,
        hemoglobin: null,
        risk_factors: []
      },
      formRules: {
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' },
          { type: 'number', min: 15, max: 50, message: '年龄必须在15-50岁之间', trigger: 'blur' }
        ],
        height: [
          { required: true, message: '请输入身高', trigger: 'blur' },
          { type: 'number', min: 140, max: 200, message: '身高必须在140-200cm之间', trigger: 'blur' }
        ],
        weight: [
          { required: true, message: '请输入体重', trigger: 'blur' },
          { type: 'number', min: 40, max: 120, message: '体重必须在40-120kg之间', trigger: 'blur' }
        ],
        gestational_weeks: [
          { required: true, message: '请输入孕周', trigger: 'blur' },
          { type: 'number', min: 0, max: 42, message: '孕周必须在0-42周之间', trigger: 'blur' }
        ],
        pregnancy_type: [
          { required: true, message: '请选择妊娠类型', trigger: 'change' }
        ],
        systolic_pressure: [
          { required: true, message: '请输入收缩压', trigger: 'blur' },
          { type: 'number', min: 80, max: 200, message: '收缩压必须在80-200mmHg之间', trigger: 'blur' }
        ],
        diastolic_pressure: [
          { required: true, message: '请输入舒张压', trigger: 'blur' },
          { type: 'number', min: 40, max: 120, message: '舒张压必须在40-120mmHg之间', trigger: 'blur' }
        ]
      },
      predictionResults: null
    };
  },
  watch: {
    'predictionForm.height'(newVal) {
      this.calculateBMI();
    },
    'predictionForm.weight'(newVal) {
      this.calculateBMI();
    }
  },
  mounted() {
    this.checkModelsStatus();
  },
  methods: {
    calculateBMI() {
      if (this.predictionForm.height && this.predictionForm.weight) {
        const heightInMeters = this.predictionForm.height / 100;
        this.predictionForm.bmi = parseFloat((this.predictionForm.weight / (heightInMeters * heightInMeters)).toFixed(1));
      } else {
        this.predictionForm.bmi = null;
      }
    },
    checkModelsStatus() {
      maternalPredictionService.getModelStatus()
        .then(response => {
          if (response.success) {
            this.modelsLoaded = response.data.models_loaded;
          }
        })
        .catch(error => {
          console.error('获取模型状态失败:', error);
          this.$message.error('获取模型状态失败');
        });
    },
    refreshModels() {
      this.checkModelsStatus();
      this.$message.success('模型状态已刷新');
    },
    predictRisks() {
      this.$refs.predictionForm.validate((valid) => {
        if (valid) {
          this.predicting = true;
          
          // 预测综合风险
          maternalPredictionService.predictComprehensiveRisk(this.predictionForm)
            .then(response => {
              if (response.success) {
                this.predictionResults = response.data;
                this.$message.success('风险预测完成');
                // 触发预测成功事件
                this.$emit('predictionSuccess', response.data);
              } else {
                this.$message.error(response.error || '预测失败');
                // 触发预测失败事件
                this.$emit('predictionError', { message: response.error || '预测失败' });
              }
            })
            .catch(error => {
              console.error('预测失败:', error);
              this.$message.error('预测失败，请稍后重试');
              // 触发预测失败事件
              this.$emit('predictionError', { message: '预测失败，请稍后重试' });
            })
            .finally(() => {
              this.predicting = false;
            });
        }
      });
    },
    resetForm() {
      this.$refs.predictionForm.resetFields();
      this.predictionResults = null;
    },
    exportResults() {
      if (!this.predictionResults) {
        this.$message.warning('没有可导出的结果');
        return;
      }
      
      const dataStr = JSON.stringify(this.predictionResults, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `孕产妇风险预测结果_${new Date().toLocaleDateString()}.json`;
      link.click();
      URL.revokeObjectURL(url);
    },
    getRiskLevelClass(riskLevel) {
      switch (riskLevel) {
        case '低风险':
          return 'risk-low';
        case '中风险':
          return 'risk-medium';
        case '高风险':
          return 'risk-high';
        default:
          return '';
      }
    },
    getGaugeGradient(riskLevel, riskProbability) {
      const percentage = riskProbability * 100;
      
      if (riskLevel === '低风险') {
        return `green 0%, green ${percentage}%, #f0f0f0 ${percentage}%, #f0f0f0 100%`;
      } else if (riskLevel === '中风险') {
        return `orange 0%, orange ${percentage}%, #f0f0f0 ${percentage}%, #f0f0f0 100%`;
      } else {
        return `red 0%, red ${percentage}%, #f0f0f0 ${percentage}%, #f0f0f0 100%`;
      }
    }
  }
};
</script>

<style scoped>
.maternal-risk-prediction {
  padding: 20px;
}

.prediction-card, .results-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
}

.model-status-alert {
  margin-bottom: 20px;
}

.prediction-form {
  margin-top: 20px;
}

.form-section-title {
  font-size: 16px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 15px;
  padding-bottom: 5px;
  border-bottom: 1px solid #EBEEF5;
}

.risk-summary {
  padding: 20px;
}

.risk-item {
  text-align: center;
  padding: 15px;
  border-radius: 8px;
  background-color: #F5F7FA;
  margin-bottom: 20px;
}

.risk-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.risk-value {
  font-size: 24px;
  font-weight: bold;
}

.risk-score {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.risk-factors {
  margin-top: 10px;
}

.risk-suggestions {
  margin-top: 20px;
  padding: 15px;
  background-color: #F0F9FF;
  border-radius: 8px;
}

.risk-suggestions h4 {
  margin-bottom: 10px;
  color: #409EFF;
}

.risk-suggestions ul {
  padding-left: 20px;
}

.risk-suggestions li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.risk-detail {
  padding: 20px;
}

.risk-chart-container {
  text-align: center;
}

.risk-chart-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
}

.risk-gauge {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  position: relative;
  margin: 0 auto;
}

.risk-gauge-center {
  width: 150px;
  height: 150px;
  background-color: white;
  border-radius: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.risk-gauge-value {
  font-size: 28px;
  font-weight: bold;
}

.risk-gauge-label {
  font-size: 14px;
  margin-top: 5px;
}

.risk-factors-detail {
  padding: 0 20px;
}

.risk-factors-detail h4 {
  margin-bottom: 10px;
  color: #409EFF;
}

.risk-factors-detail ul {
  padding-left: 20px;
  margin-bottom: 20px;
}

.risk-factors-detail li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.risk-low {
  color: #67C23A;
}

.risk-medium {
  color: #E6A23C;
}

.risk-high {
  color: #F56C6C;
}
</style>
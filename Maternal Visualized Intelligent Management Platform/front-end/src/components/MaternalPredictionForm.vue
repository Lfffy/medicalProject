<template>
  <div class="maternal-prediction-form">
    <div class="form-container">
      <h2 class="form-title">孕产妇健康风险预测</h2>
      <p class="form-description">请填写以下信息以获取个性化的健康风险预测和建议</p>
      
      <form @submit.prevent="submitForm" class="prediction-form">
        <!-- 基本信息部分 -->
        <div class="form-section">
          <h3 class="section-title">
            <i class="fas fa-user-circle"></i>
            基本信息
          </h3>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="name">姓名 <span class="required">*</span></label>
              <input 
                id="name"
                v-model="formData.name" 
                type="text" 
                class="form-input"
                placeholder="请输入姓名"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="age">年龄（岁） <span class="required">*</span></label>
              <input 
                id="age"
                v-model.number="formData.age" 
                type="number" 
                class="form-input"
                placeholder="请输入年龄"
                min="16" 
                max="55"
                required
              >
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="gestationalWeek">孕周（周） <span class="required">*</span></label>
              <input 
                id="gestationalWeek"
                v-model.number="formData.gestationalWeek" 
                type="number" 
                class="form-input"
                placeholder="请输入当前孕周"
                min="1" 
                max="42"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="parity">产次 <span class="required">*</span></label>
              <select id="parity" v-model.number="formData.parity" class="form-select" required>
                <option value="">请选择产次</option>
                <option value="0">初产妇</option>
                <option value="1">1次</option>
                <option value="2">2次</option>
                <option value="3">3次及以上</option>
              </select>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="height">身高（cm） <span class="required">*</span></label>
              <input 
                id="height"
                v-model.number="formData.height" 
                type="number" 
                class="form-input"
                placeholder="请输入身高"
                min="140" 
                max="190"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="weight">体重（kg） <span class="required">*</span></label>
              <input 
                id="weight"
                v-model.number="formData.weight" 
                type="number" 
                class="form-input"
                placeholder="请输入当前体重"
                min="35" 
                max="150"
                required
              >
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="bmi">BMI指数 <span class="info">（系统自动计算）</span></label>
              <input 
                id="bmi"
                v-model="formData.bmi"
                type="text" 
                class="form-input disabled"
                disabled
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="bloodType">血型</label>
              <select id="bloodType" v-model="formData.bloodType" class="form-select">
                <option value="">请选择血型</option>
                <option value="A">A型</option>
                <option value="B">B型</option>
                <option value="AB">AB型</option>
                <option value="O">O型</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- 生理指标部分 -->
        <div class="form-section">
          <h3 class="section-title">
            <i class="fas fa-heartbeat"></i>
            生理指标
          </h3>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="systolic">收缩压（mmHg） <span class="required">*</span></label>
              <input 
                id="systolic"
                v-model.number="formData.systolic" 
                type="number" 
                class="form-input"
                placeholder="请输入收缩压"
                min="80" 
                max="180"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="diastolic">舒张压（mmHg） <span class="required">*</span></label>
              <input 
                id="diastolic"
                v-model.number="formData.diastolic" 
                type="number" 
                class="form-input"
                placeholder="请输入舒张压"
                min="40" 
                max="110"
                required
              >
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="heartRate">心率（次/分） <span class="required">*</span></label>
              <input 
                id="heartRate"
                v-model.number="formData.heartRate" 
                type="number" 
                class="form-input"
                placeholder="请输入心率"
                min="50" 
                max="120"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="temperature">体温（°C）</label>
              <input 
                id="temperature"
                v-model.number="formData.temperature" 
                type="number" 
                step="0.1"
                class="form-input"
                placeholder="请输入体温"
                min="35" 
                max="42"
              >
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="bloodSugar">血糖（mmol/L）</label>
              <input 
                id="bloodSugar"
                v-model.number="formData.bloodSugar" 
                type="number" 
                step="0.1"
                class="form-input"
                placeholder="请输入血糖值"
                min="2.5" 
                max="15"
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="hemoglobin">血红蛋白（g/L）</label>
              <input 
                id="hemoglobin"
                v-model.number="formData.hemoglobin" 
                type="number" 
                class="form-input"
                placeholder="请输入血红蛋白值"
                min="80" 
                max="180"
              >
            </div>
          </div>
        </div>
        
        <!-- 既往病史部分 -->
        <div class="form-section">
          <h3 class="section-title">
            <i class="fas fa-stethoscope"></i>
            既往病史
          </h3>
          
          <div class="form-row">
            <div class="form-group full-width">
              <label class="form-label">慢性疾病史</label>
              <div class="checkbox-group">
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.chronicDiseases.hypertension"
                    value="hypertension"
                  >
                  <span>高血压</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.chronicDiseases.diabetes"
                    value="diabetes"
                  >
                  <span>糖尿病</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.chronicDiseases.cardiovascular"
                    value="cardiovascular"
                  >
                  <span>心血管疾病</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.chronicDiseases.thyroid"
                    value="thyroid"
                  >
                  <span>甲状腺疾病</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.chronicDiseases.kidney"
                    value="kidney"
                  >
                  <span>肾脏疾病</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.chronicDiseases.other"
                    value="other"
                  >
                  <span>其他</span>
                </label>
              </div>
            </div>
          </div>
          
          <div class="form-row" v-if="formData.chronicDiseases.other">
            <div class="form-group full-width">
              <label class="form-label" for="otherDisease">请说明其他疾病</label>
              <textarea 
                id="otherDisease"
                v-model="formData.otherDisease" 
                class="form-textarea"
                rows="2"
                placeholder="请详细描述其他疾病情况"
              ></textarea>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group full-width">
              <label class="form-label">妊娠相关病史</label>
              <div class="checkbox-group">
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.pregnancyHistory.preeclampsia"
                    value="preeclampsia"
                  >
                  <span>子痫前期/子痫</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.pregnancyHistory.gestationalDiabetes"
                    value="gestationalDiabetes"
                  >
                  <span>妊娠期糖尿病</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.pregnancyHistory.preterm"
                    value="preterm"
                  >
                  <span>早产史</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.pregnancyHistory.miscarriage"
                    value="miscarriage"
                  >
                  <span>流产史</span>
                </label>
                <label class="checkbox-item">
                  <input 
                    type="checkbox" 
                    v-model="formData.pregnancyHistory.other"
                    value="other"
                  >
                  <span>其他</span>
                </label>
              </div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="medications">目前服用药物</label>
              <textarea 
                id="medications"
                v-model="formData.medications" 
                class="form-textarea"
                rows="2"
                placeholder="请列出目前正在服用的所有药物"
              ></textarea>
            </div>
          </div>
        </div>
        
        <!-- 生活习惯部分 -->
        <div class="form-section">
          <h3 class="section-title">
            <i class="fas fa-heart"></i>
            生活习惯
          </h3>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="exerciseFrequency">运动频率</label>
              <select id="exerciseFrequency" v-model="formData.exerciseFrequency" class="form-select">
                <option value="">请选择</option>
                <option value="daily">每天</option>
                <option value="weekly3-5">每周3-5次</option>
                <option value="weekly1-2">每周1-2次</option>
                <option value="rarely">很少</option>
                <option value="never">从不</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label" for="sleepHours">每日睡眠时间（小时）</label>
              <input 
                id="sleepHours"
                v-model.number="formData.sleepHours" 
                type="number" 
                step="0.5"
                class="form-input"
                placeholder="请输入每日平均睡眠时间"
                min="4" 
                max="12"
              >
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">饮食习惯</label>
              <select v-model="formData.diet" class="form-select">
                <option value="">请选择</option>
                <option value="balanced">均衡</option>
                <option value="highProtein">高蛋白</option>
                <option value="highCarb">高碳水</option>
                <option value="vegetarian">素食</option>
                <option value="irregular">不规律</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">吸烟情况</label>
              <select v-model="formData.smoking" class="form-select">
                <option value="">请选择</option>
                <option value="never">从不吸烟</option>
                <option value="former">曾经吸烟</option>
                <option value="current">现在吸烟</option>
              </select>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">饮酒情况</label>
              <select v-model="formData.alcohol" class="form-select">
                <option value="">请选择</option>
                <option value="never">从不饮酒</option>
                <option value="rarely">偶尔饮酒</option>
                <option value="moderate">适量饮酒</option>
                <option value="heavy">大量饮酒</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">压力水平</label>
              <select v-model="formData.stressLevel" class="form-select">
                <option value="">请选择</option>
                <option value="low">低</option>
                <option value="moderate">中等</option>
                <option value="high">高</option>
                <option value="veryHigh">非常高</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- 其他信息部分 -->
        <div class="form-section">
          <h3 class="section-title">
            <i class="fas fa-info-circle"></i>
            其他信息
          </h3>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="symptoms">当前不适症状</label>
              <textarea 
                id="symptoms"
                v-model="formData.symptoms" 
                class="form-textarea"
                rows="3"
                placeholder="请描述您目前的任何不适症状，如头痛、恶心、水肿等"
              ></textarea>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="notes">补充说明</label>
              <textarea 
                id="notes"
                v-model="formData.notes" 
                class="form-textarea"
                rows="2"
                placeholder="请提供任何您认为重要的其他信息"
              ></textarea>
            </div>
          </div>
        </div>
        
        <!-- 提交按钮 -->
        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="resetForm">
            <i class="fas fa-redo"></i>
            重置表单
          </button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            <i class="fas fa-microscope"></i>
            {{ isSubmitting ? '分析中...' : '提交分析' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MaternalPredictionForm',
  data() {
    return {
      isSubmitting: false,
      formData: {
        // 基本信息
        name: '',
        age: null,
        gestationalWeek: null,
        parity: null,
        height: null,
        weight: null,
        bmi: '',
        bloodType: '',
        
        // 生理指标
        systolic: null,
        diastolic: null,
        heartRate: null,
        temperature: null,
        bloodSugar: null,
        hemoglobin: null,
        
        // 既往病史
        chronicDiseases: {
          hypertension: false,
          diabetes: false,
          cardiovascular: false,
          thyroid: false,
          kidney: false,
          other: false
        },
        otherDisease: '',
        pregnancyHistory: {
          preeclampsia: false,
          gestationalDiabetes: false,
          preterm: false,
          miscarriage: false,
          other: false
        },
        medications: '',
        
        // 生活习惯
        exerciseFrequency: '',
        sleepHours: null,
        diet: '',
        smoking: '',
        alcohol: '',
        stressLevel: '',
        
        // 其他信息
        symptoms: '',
        notes: ''
      },
      // 验证规则
      validationRules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' },
          { type: 'number', min: 16, max: 55, message: '年龄应在16到55岁之间', trigger: 'blur' }
        ],
        gestationalWeek: [
          { required: true, message: '请输入孕周', trigger: 'blur' },
          { type: 'number', min: 4, max: 42, message: '孕周应在4到42周之间', trigger: 'blur' }
        ],
        parity: [
          { required: false },
          { type: 'number', min: 0, max: 10, message: '产次应在0到10之间', trigger: 'blur' }
        ],
        height: [
          { required: true, message: '请输入身高', trigger: 'blur' },
          { type: 'number', min: 140, max: 200, message: '身高应在140到200cm之间', trigger: 'blur' }
        ],
        weight: [
          { required: true, message: '请输入体重', trigger: 'blur' },
          { type: 'number', min: 40, max: 150, message: '体重应在40到150kg之间', trigger: 'blur' }
        ],
        systolic: [
          { required: true, message: '请输入收缩压', trigger: 'blur' },
          { type: 'number', min: 80, max: 200, message: '收缩压应在80到200mmHg之间', trigger: 'blur' }
        ],
        diastolic: [
          { required: true, message: '请输入舒张压', trigger: 'blur' },
          { type: 'number', min: 50, max: 120, message: '舒张压应在50到120mmHg之间', trigger: 'blur' }
        ],
        heartRate: [
          { required: true, message: '请输入心率', trigger: 'blur' },
          { type: 'number', min: 50, max: 120, message: '心率应在50到120次/分钟之间', trigger: 'blur' }
        ],
        temperature: [
          { required: true, message: '请输入体温', trigger: 'blur' },
          { type: 'number', min: 35, max: 42, message: '体温应在35到42℃之间', trigger: 'blur' }
        ],
        bloodSugar: [
          { required: false },
          { type: 'number', min: 2, max: 20, message: '血糖应在2到20mmol/L之间', trigger: 'blur' }
        ],
        hemoglobin: [
          { required: false },
          { type: 'number', min: 80, max: 200, message: '血红蛋白应在80到200g/L之间', trigger: 'blur' }
        ],
        sleepHours: [
          { required: false },
          { type: 'number', min: 3, max: 12, message: '睡眠时间应在3到12小时之间', trigger: 'blur' }
        ]
      },
      // 验证状态
      errors: {}
    }
  },
  
  watch: {
    // 自动计算BMI
    'formData.height': function(newHeight) {
      this.calculateBMI();
    },
    'formData.weight': function(newWeight) {
      this.calculateBMI();
    }
  },
  
  computed: {
    // 检查血压是否正常
    isBloodPressureNormal() {
      if (!this.formData.systolic || !this.formData.diastolic) return null;
      return this.formData.systolic < 140 && this.formData.diastolic < 90;
    },
    
    // 检查BMI分类
    bmiCategory() {
      if (!this.formData.bmi) return '';
      const bmi = parseFloat(this.formData.bmi);
      if (bmi < 18.5) return '偏瘦';
      if (bmi < 24) return '正常';
      if (bmi < 28) return '超重';
      return '肥胖';
    },
    
    // 检查是否有慢性疾病
    hasChronicDiseases() {
      return Object.values(this.formData.chronicDiseases).some(value => value === true);
    },
    
    // 检查是否有妊娠相关疾病史
    hasPregnancyRelatedDiseases() {
      return Object.values(this.formData.pregnancyHistory).some(value => value === true);
    },
    
    // 验证当前标签页
    isValidTab() {
      // 这里可以根据当前激活的标签页进行验证
      // 暂时返回true，后续可以扩展
      return true;
    }
  },
  
  methods: {
    // 计算BMI
    calculateBMI() {
      if (this.formData.height && this.formData.weight) {
        const heightInMeters = this.formData.height / 100;
        const bmi = (this.formData.weight / (heightInMeters * heightInMeters)).toFixed(1);
        this.formData.bmi = bmi;
      } else {
        this.formData.bmi = '';
      }
    },
    
    // 验证单个字段
    validateField(fieldName, value) {
      const rules = this.validationRules[fieldName];
      if (!rules) return '';
      
      for (const rule of rules) {
        // 检查必填
        if (rule.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
          return rule.message;
        }
        
        // 如果字段不是必填且为空，跳过其他验证
        if (!rule.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
          continue;
        }
        
        // 类型和范围验证
        if (rule.type === 'number' && value !== null && value !== '') {
          const numValue = parseFloat(value);
          if (isNaN(numValue)) {
            return '请输入有效的数字';
          }
          if (rule.min !== undefined && numValue < rule.min) {
            return rule.message;
          }
          if (rule.max !== undefined && numValue > rule.max) {
            return rule.message;
          }
        }
        
        // 长度验证
        if (rule.min !== undefined && rule.max !== undefined && typeof value === 'string') {
          if (value.length < rule.min || value.length > rule.max) {
            return rule.message;
          }
        }
      }
      
      return '';
    },
    
    // 处理输入变化和验证
    handleInput(fieldName, value) {
      this.formData[fieldName] = value;
      const error = this.validateField(fieldName, value);
      
      if (error) {
        this.$set(this.errors, fieldName, error);
      } else {
        this.$delete(this.errors, fieldName);
      }
    },
    
    // 验证整个表单
    validateForm() {
      const errors = {};
      let isValid = true;
      
      // 验证所有字段
      Object.keys(this.validationRules).forEach(field => {
        const error = this.validateField(field, this.formData[field]);
        if (error) {
          errors[field] = error;
          isValid = false;
        }
      });
      
      // 验证血压关系
      if (this.formData.systolic && this.formData.diastolic && 
          this.formData.systolic <= this.formData.diastolic) {
        errors.bloodPressure = '收缩压必须大于舒张压';
        isValid = false;
      }
      
      // 验证病史信息
      if (this.formData.chronicDiseases.other && !this.formData.otherDisease.trim()) {
        errors.otherDisease = '请说明其他慢性疾病';
        isValid = false;
      }
      
      this.errors = errors;
      return isValid;
    },
    
    // 准备提交数据
    prepareSubmitData() {
      // 转换数据格式，确保数值类型正确
      const submitData = JSON.parse(JSON.stringify(this.formData));
      
      // 处理数值字段
      const numericFields = ['age', 'gestationalWeek', 'parity', 'height', 'weight', 
                            'systolic', 'diastolic', 'heartRate', 'temperature', 
                            'bloodSugar', 'hemoglobin', 'sleepHours'];
      
      numericFields.forEach(field => {
        if (submitData[field] !== null && submitData[field] !== '') {
          submitData[field] = parseFloat(submitData[field]);
        }
      });
      
      // 转换布尔值为数值（如果后端需要）
      Object.keys(submitData.chronicDiseases).forEach(key => {
        submitData.chronicDiseases[key] = submitData.chronicDiseases[key] ? 1 : 0;
      });
      
      Object.keys(submitData.pregnancyHistory).forEach(key => {
        submitData.pregnancyHistory[key] = submitData.pregnancyHistory[key] ? 1 : 0;
      });
      
      return submitData;
    },
    
    // 重置表单
    resetForm() {
      if (confirm('确定要重置所有表单数据吗？')) {
        this.$data.formData = this.$options.data().formData;
        this.errors = {};
      }
    },
    
    // 提交表单
    async submitForm() {
      // 验证表单
      if (!this.validateForm()) {
        // 滚动到第一个错误字段
        const firstErrorField = Object.keys(this.errors)[0];
        if (firstErrorField) {
          const element = document.querySelector(`[data-field="${firstErrorField}"]`);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            element.focus();
          }
        }
        return;
      }
      
      // 准备提交数据
      const submitData = this.prepareSubmitData();
      console.log('表单数据:', submitData);
      
      // 这里将在后续步骤中与后端API交互
      this.isSubmitting = true;
      
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 模拟成功响应
        this.$emit('predictionSuccess', {
          status: 'success',
          message: '预测成功',
          data: submitData
        });
      } catch (error) {
        console.error('提交表单时出错:', error);
        this.$emit('predictionError', {
          status: 'error',
          message: '预测失败，请稍后重试'
        });
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
.maternal-prediction-form {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 20px;
}

.form-container {
  max-width: 1200px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.form-title {
  color: #2c3e50;
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
  text-align: center;
}

.form-description {
  color: #7f8c8d;
  font-size: 16px;
  text-align: center;
  margin-bottom: 30px;
}

.form-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #ff69b4;
}

.section-title {
  color: #2c3e50;
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 10px;
  color: #ff69b4;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 20px;
  gap: 20px;
}

.form-group {
  flex: 1;
  min-width: 280px;
  margin-bottom: 15px;
}

.form-group.full-width {
  flex: 100%;
  min-width: 100%;
}

.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #34495e;
  font-size: 14px;
}

.required {
  color: #e74c3c;
}

.info {
  color: #7f8c8d;
  font-weight: normal;
  font-size: 12px;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: #ff69b4;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.2);
}

.form-input.disabled {
  background-color: #f2f2f2;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 60px;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-right: 20px;
  margin-bottom: 10px;
}

.checkbox-item input {
  margin-right: 6px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
  gap: 15px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #ecf0f1;
  color: #2c3e50;
  border: 1px solid #bdc3c7;
}

.btn-secondary:hover {
  background-color: #bdc3c7;
}

.btn-primary i,
.btn-secondary i {
  margin-right: 8px;
}

@media (max-width: 768px) {
  .form-container {
    padding: 20px;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .form-group {
    min-width: 100%;
  }
  
  .checkbox-group {
    flex-direction: column;
  }
  
  .checkbox-item {
    margin-right: 0;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}
</style>
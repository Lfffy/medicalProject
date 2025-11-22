<template>
  <div class="maternal-prediction-form">
    <div class="form-container">
      <h1 class="form-title">孕产妇健康风险预测</h1>
      <p class="form-description">请填写以下信息，我们将为您提供个性化的健康风险评估和建议</p>
      
      <!-- 基本信息部分 -->
      <div class="form-section">
        <h2 class="section-title"><i class="fas fa-user"></i>基本信息</h2>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="name">姓名 <span class="required">*</span></label>
            <input
              id="name"
              type="text"
              class="form-input"
              :class="{ 'error': errors.name }"
              v-model="formData.name"
              @input="handleInput('name', $event.target.value)"
              @blur="handleInput('name', $event.target.value)"
              data-field="name"
              placeholder="请输入姓名"
            />
            <div v-if="errors.name" class="error-message">{{ errors.name }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="age">年龄 <span class="required">*</span></label>
            <input
              id="age"
              type="number"
              class="form-input"
              :class="{ 'error': errors.age }"
              v-model.number="formData.age"
              @input="handleInput('age', $event.target.value)"
              @blur="handleInput('age', $event.target.value)"
              data-field="age"
              placeholder="请输入年龄"
            />
            <div v-if="errors.age" class="error-message">{{ errors.age }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="gestationalWeek">孕周 <span class="required">*</span></label>
            <input
              id="gestationalWeek"
              type="number"
              class="form-input"
              :class="{ 'error': errors.gestationalWeek }"
              v-model.number="formData.gestationalWeek"
              @input="handleInput('gestationalWeek', $event.target.value)"
              @blur="handleInput('gestationalWeek', $event.target.value)"
              data-field="gestationalWeek"
              placeholder="请输入孕周"
            />
            <div v-if="errors.gestationalWeek" class="error-message">{{ errors.gestationalWeek }}</div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="parity">产次</label>
            <input
              id="parity"
              type="number"
              class="form-input"
              :class="{ 'error': errors.parity }"
              v-model.number="formData.parity"
              @input="handleInput('parity', $event.target.value)"
              @blur="handleInput('parity', $event.target.value)"
              data-field="parity"
              placeholder="请输入产次"
            />
            <div v-if="errors.parity" class="error-message">{{ errors.parity }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="height">身高(cm) <span class="required">*</span></label>
            <input
              id="height"
              type="number"
              class="form-input"
              :class="{ 'error': errors.height }"
              v-model.number="formData.height"
              @input="handleInput('height', $event.target.value)"
              @blur="handleInput('height', $event.target.value)"
              data-field="height"
              placeholder="请输入身高"
            />
            <div v-if="errors.height" class="error-message">{{ errors.height }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="weight">体重(kg) <span class="required">*</span></label>
            <input
              id="weight"
              type="number"
              class="form-input"
              :class="{ 'error': errors.weight }"
              v-model.number="formData.weight"
              @input="handleInput('weight', $event.target.value)"
              @blur="handleInput('weight', $event.target.value)"
              data-field="weight"
              placeholder="请输入体重"
            />
            <div v-if="errors.weight" class="error-message">{{ errors.weight }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="bmi">BMI指数</label>
            <div class="input-with-info">
              <input
                id="bmi"
                type="text"
                class="form-input disabled"
                v-model="formData.bmi"
                :disabled="true"
                placeholder="自动计算"
              />
              <span v-if="formData.bmi" class="bmi-category" :class="bmiCategory">
                {{ bmiCategory }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="bloodType">血型</label>
            <select id="bloodType" class="form-select" v-model="formData.bloodType">
              <option value="">请选择血型</option>
              <option value="A">A型</option>
              <option value="B">B型</option>
              <option value="AB">AB型</option>
              <option value="O">O型</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="rhFactor">Rh因子</label>
            <select id="rhFactor" class="form-select" v-model="formData.rhFactor">
              <option value="">请选择Rh因子</option>
              <option value="positive">Rh阳性</option>
              <option value="negative">Rh阴性</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="menstrualHistory">月经史</label>
            <select id="menstrualHistory" class="form-select" v-model="formData.menstrualHistory">
              <option value="">请选择月经史</option>
              <option value="regular">规律</option>
              <option value="irregular">不规律</option>
              <option value="unknown">不清楚</option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="lastMenstrualPeriod">末次月经日期</label>
            <input
              id="lastMenstrualPeriod"
              type="date"
              class="form-input"
              v-model="formData.lastMenstrualPeriod"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label" for="plannedDeliveryDate">计划分娩日期</label>
            <input
              id="plannedDeliveryDate"
              type="date"
              class="form-input"
              v-model="formData.plannedDeliveryDate"
            />
          </div>
        </div>
      </div>
      
      <!-- 生理指标部分 -->
      <div class="form-section">
        <h2 class="section-title"><i class="fas fa-heartbeat"></i>生理指标</h2>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="systolic">收缩压(mmHg) <span class="required">*</span></label>
            <input
              id="systolic"
              type="number"
              class="form-input"
              :class="{ 'error': errors.systolic || errors.bloodPressure }"
              v-model.number="formData.systolic"
              @input="handleInput('systolic', $event.target.value)"
              @blur="handleInput('systolic', $event.target.value)"
              data-field="systolic"
              placeholder="请输入收缩压"
            />
            <div v-if="errors.systolic" class="error-message">{{ errors.systolic }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="diastolic">舒张压(mmHg) <span class="required">*</span></label>
            <input
              id="diastolic"
              type="number"
              class="form-input"
              :class="{ 'error': errors.diastolic || errors.bloodPressure }"
              v-model.number="formData.diastolic"
              @input="handleInput('diastolic', $event.target.value)"
              @blur="handleInput('diastolic', $event.target.value)"
              data-field="diastolic"
              placeholder="请输入舒张压"
            />
            <div v-if="errors.bloodPressure" class="error-message">{{ errors.bloodPressure }}</div>
            <div v-else-if="errors.diastolic" class="error-message">{{ errors.diastolic }}</div>
            <div v-if="formData.systolic && formData.diastolic && !errors.bloodPressure" class="info-message">
              血压{{ isBloodPressureNormal ? '正常' : '偏高' }}
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="heartRate">心率(次/分钟) <span class="required">*</span></label>
            <input
              id="heartRate"
              type="number"
              class="form-input"
              :class="{ 'error': errors.heartRate }"
              v-model.number="formData.heartRate"
              @input="handleInput('heartRate', $event.target.value)"
              @blur="handleInput('heartRate', $event.target.value)"
              data-field="heartRate"
              placeholder="请输入心率"
            />
            <div v-if="errors.heartRate" class="error-message">{{ errors.heartRate }}</div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="temperature">体温(℃) <span class="required">*</span></label>
            <input
              id="temperature"
              type="number"
              step="0.1"
              class="form-input"
              :class="{ 'error': errors.temperature }"
              v-model.number="formData.temperature"
              @input="handleInput('temperature', $event.target.value)"
              @blur="handleInput('temperature', $event.target.value)"
              data-field="temperature"
              placeholder="请输入体温"
            />
            <div v-if="errors.temperature" class="error-message">{{ errors.temperature }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="bloodSugar">血糖(mmol/L)</label>
            <input
              id="bloodSugar"
              type="number"
              step="0.1"
              class="form-input"
              :class="{ 'error': errors.bloodSugar }"
              v-model.number="formData.bloodSugar"
              @input="handleInput('bloodSugar', $event.target.value)"
              @blur="handleInput('bloodSugar', $event.target.value)"
              data-field="bloodSugar"
              placeholder="请输入血糖"
            />
            <div v-if="errors.bloodSugar" class="error-message">{{ errors.bloodSugar }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="hemoglobin">血红蛋白(g/L)</label>
            <input
              id="hemoglobin"
              type="number"
              class="form-input"
              :class="{ 'error': errors.hemoglobin }"
              v-model.number="formData.hemoglobin"
              @input="handleInput('hemoglobin', $event.target.value)"
              @blur="handleInput('hemoglobin', $event.target.value)"
              data-field="hemoglobin"
              placeholder="请输入血红蛋白"
            />
            <div v-if="errors.hemoglobin" class="error-message">{{ errors.hemoglobin }}</div>
          </div>
        </div>
      </div>
      
      <!-- 既往病史部分 -->
      <div class="form-section">
        <h2 class="section-title"><i class="fas fa-history"></i>既往病史</h2>
        <div class="form-group">
          <label class="form-label">慢性疾病史</label>
          <div class="checkbox-group">
            <div class="checkbox-item" v-for="(value, key) in formData.chronicDiseases" :key="key">
              <input
                type="checkbox"
                :id="`chronic-${key}`"
                v-model="formData.chronicDiseases[key]"
              />
              <label :for="`chronic-${key}`">{{ getChronicDiseaseLabel(key) }}</label>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label" for="otherDisease">其他慢性疾病描述</label>
          <textarea
            id="otherDisease"
            class="form-textarea"
            :class="{ 'error': errors.otherDisease }"
            v-model="formData.otherDisease"
            data-field="otherDisease"
            placeholder="如有其他慢性疾病，请详细描述"
          ></textarea>
          <div v-if="errors.otherDisease" class="error-message">{{ errors.otherDisease }}</div>
        </div>
        
        <div class="form-group">
          <label class="form-label">妊娠相关病史</label>
          <div class="checkbox-group">
            <div class="checkbox-item" v-for="(value, key) in formData.pregnancyHistory" :key="key">
              <input
                type="checkbox"
                :id="`pregnancy-${key}`"
                v-model="formData.pregnancyHistory[key]"
              />
              <label :for="`pregnancy-${key}`">{{ getPregnancyHistoryLabel(key) }}</label>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label" for="medications">目前用药情况</label>
          <textarea
            id="medications"
            class="form-textarea"
            v-model="formData.medications"
            placeholder="请详细描述目前服用的药物，包括名称、剂量和频率"
          ></textarea>
        </div>
      </div>
      
      <!-- 生活习惯部分 -->
      <div class="form-section">
        <h2 class="section-title"><i class="fas fa-lifestyle"></i>生活习惯</h2>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="exerciseFrequency">运动频率</label>
            <select id="exerciseFrequency" class="form-select" v-model="formData.exerciseFrequency">
              <option value="">请选择运动频率</option>
              <option value="daily">每天</option>
              <option value="several">每周数次</option>
              <option value="rarely">很少</option>
              <option value="never">从不</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="sleepHours">平均睡眠时间(小时/天)</label>
            <input
              id="sleepHours"
              type="number"
              step="0.5"
              class="form-input"
              :class="{ 'error': errors.sleepHours }"
              v-model.number="formData.sleepHours"
              @input="handleInput('sleepHours', $event.target.value)"
              @blur="handleInput('sleepHours', $event.target.value)"
              data-field="sleepHours"
              placeholder="请输入睡眠时间"
            />
            <div v-if="errors.sleepHours" class="error-message">{{ errors.sleepHours }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="diet">饮食习惯</label>
            <select id="diet" class="form-select" v-model="formData.diet">
              <option value="">请选择饮食习惯</option>
              <option value="balanced">均衡饮食</option>
              <option value="vegetarian">素食</option>
              <option value="highProtein">高蛋白</option>
              <option value="highCarb">高碳水</option>
              <option value="irregular">不规律</option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="smoking">吸烟情况</label>
            <select id="smoking" class="form-select" v-model="formData.smoking">
              <option value="">请选择吸烟情况</option>
              <option value="never">从不吸烟</option>
              <option value="past">曾经吸烟</option>
              <option value="current">正在吸烟</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="alcohol">饮酒情况</label>
            <select id="alcohol" class="form-select" v-model="formData.alcohol">
              <option value="">请选择饮酒情况</option>
              <option value="never">从不饮酒</option>
              <option value="rarely">很少饮酒</option>
              <option value="socially">社交场合饮酒</option>
              <option value="regularly">经常饮酒</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="stressLevel">压力水平</label>
            <select id="stressLevel" class="form-select" v-model="formData.stressLevel">
              <option value="">请选择压力水平</option>
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
        <h2 class="section-title"><i class="fas fa-info-circle"></i>其他信息</h2>
        <div class="form-group full-width">
          <label class="form-label" for="symptoms">当前症状</label>
          <textarea
            id="symptoms"
            class="form-textarea"
            v-model="formData.symptoms"
            placeholder="请描述您当前的任何不适症状"
          ></textarea>
        </div>
        
        <div class="form-group full-width">
          <label class="form-label" for="notes">其他说明</label>
          <textarea
            id="notes"
            class="form-textarea"
            v-model="formData.notes"
            placeholder="如有其他需要说明的信息，请在此处填写"
          ></textarea>
        </div>
      </div>
      
      <!-- 表单操作按钮 -->
      <div class="form-actions">
        <button 
          type="button" 
          class="btn-secondary" 
          @click="resetForm"
          :disabled="isSubmitting"
        >
          <i class="fas fa-redo-alt"></i> 重置
        </button>
        <button 
          type="button" 
          class="btn-primary" 
          @click="submitForm"
          :disabled="isSubmitting"
        >
          <i v-if="!isSubmitting" class="fas fa-check"></i>
          <i v-else class="fas fa-spinner fa-spin"></i>
          {{ isSubmitting ? '提交中...' : '提交预测' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import maternalPredictionService from '../services/maternalPredictionService';

export default {
  name: 'EnhancedMaternalPredictionForm',
  
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
        rhFactor: '',
        menstrualHistory: '',
        lastMenstrualPeriod: '',
        plannedDeliveryDate: '',
        
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
    }
  },
  
  methods: {
    // 获取慢性疾病标签
    getChronicDiseaseLabel(key) {
      const labels = {
        hypertension: '高血压',
        diabetes: '糖尿病',
        cardiovascular: '心血管疾病',
        thyroid: '甲状腺疾病',
        kidney: '肾脏疾病',
        other: '其他'
      };
      return labels[key] || key;
    },
    
    // 获取妊娠历史标签
    getPregnancyHistoryLabel(key) {
      const labels = {
        preeclampsia: '子痫前期/子痫',
        gestationalDiabetes: '妊娠期糖尿病',
        preterm: '早产史',
        miscarriage: '流产史',
        other: '其他'
      };
      return labels[key] || key;
    },
    
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
      
      // 与后端API交互
      this.isSubmitting = true;
      
      try {
        // 调用预测服务
        const result = await maternalPredictionService.submitPrediction(submitData);
        
        if (result.success) {
          // 预测成功
          this.$emit('predictionSuccess', {
            status: 'success',
            message: '预测成功',
            prediction: result.prediction,
            recommendations: result.recommendations,
            confidence: result.confidence,
            timestamp: result.timestamp,
            inputData: submitData
          });
        } else {
          // 预测失败
          this.$emit('predictionError', {
            status: 'error',
            message: result.error || '预测失败，请稍后重试'
          });
        }
      } catch (error) {
        console.error('提交表单时出错:', error);
        this.$emit('predictionError', {
          status: 'error',
          message: error.message || '预测失败，请稍后重试'
        });
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
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
  border-left: 4px solid #3498db;
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
  color: #3498db;
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
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-input.disabled {
  background-color: #f2f2f2;
  cursor: not-allowed;
}

.form-input.error {
  border-color: #e74c3c;
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

.error-message {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 4px;
}

.info-message {
  color: #3498db;
  font-size: 12px;
  margin-top: 4px;
}

.input-with-info {
  position: relative;
  display: flex;
  align-items: center;
}

.bmi-category {
  position: absolute;
  right: 10px;
  font-size: 14px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
}

.bmi-category.偏瘦 {
  color: #3498db;
  background-color: #ebf5fb;
}

.bmi-category.正常 {
  color: #27ae60;
  background-color: #ebfaf2;
}

.bmi-category.超重 {
  color: #f39c12;
  background-color: #fff5eb;
}

.bmi-category.肥胖 {
  color: #e74c3c;
  background-color: #fdedec;
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
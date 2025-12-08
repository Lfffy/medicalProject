<template>
  <div class="data-entry-container">
    <dv-border-box-8 :dur="5">
      <div class="data-entry-content">
        <div class="header">
          <h2>数据录入管理</h2>
          <div class="data-type-selector">
            <el-radio-group v-model="dataType" @change="handleDataTypeChange">
              <el-radio-button label="medical">普通医疗数据</el-radio-button>
              <el-radio-button label="maternal">孕产妇数据</el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <div class="form-container">
          <!-- 普通医疗数据录入表单 -->
          <div v-if="dataType === 'medical'" class="medical-form">
            <el-form :model="medicalForm" :rules="medicalRules" ref="medicalFormRef" label-width="120px">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="患者姓名" prop="name">
                    <el-input v-model="medicalForm.name" placeholder="请输入患者姓名"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-select v-model="medicalForm.gender" placeholder="请选择性别">
                      <el-option label="男" value="男"></el-option>
                      <el-option label="女" value="女"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="年龄" prop="age">
                    <el-input-number v-model="medicalForm.age" :min="0" :max="150" placeholder="请输入年龄"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="疾病类型" prop="disease_type">
                    <el-select v-model="medicalForm.disease_type" placeholder="请选择疾病类型">
                      <el-option label="高血压" value="高血压"></el-option>
                      <el-option label="糖尿病" value="糖尿病"></el-option>
                      <el-option label="心脏病" value="心脏病"></el-option>
                      <el-option label="呼吸系统疾病" value="呼吸系统疾病"></el-option>
                      <el-option label="消化系统疾病" value="消化系统疾病"></el-option>
                      <el-option label="其他" value="其他"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="血压(收缩压)" prop="systolic_pressure">
                    <el-input-number v-model="medicalForm.systolic_pressure" :min="50" :max="250" placeholder="收缩压"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="血压(舒张压)" prop="diastolic_pressure">
                    <el-input-number v-model="medicalForm.diastolic_pressure" :min="30" :max="150" placeholder="舒张压"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="体重(kg)" prop="weight">
                    <el-input-number v-model="medicalForm.weight" :min="0" :max="300" :precision="1" placeholder="体重"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="身高(cm)" prop="height">
                    <el-input-number v-model="medicalForm.height" :min="50" :max="250" placeholder="身高"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="血糖" prop="blood_sugar">
                    <el-input-number v-model="medicalForm.blood_sugar" :min="0" :max="30" :precision="1" placeholder="血糖值"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="体温(℃)" prop="temperature">
                    <el-input-number v-model="medicalForm.temperature" :min="35" :max="42" :precision="1" placeholder="体温"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="症状描述" prop="symptoms">
                <el-input type="textarea" v-model="medicalForm.symptoms" rows="4" placeholder="请描述患者症状"></el-input>
              </el-form-item>

              <el-form-item label="诊断结果" prop="diagnosis">
                <el-input type="textarea" v-model="medicalForm.diagnosis" rows="3" placeholder="请输入诊断结果"></el-input>
              </el-form-item>

              <el-form-item label="治疗方案" prop="treatment">
                <el-input type="textarea" v-model="medicalForm.treatment" rows="3" placeholder="请输入治疗方案"></el-input>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="submitMedicalForm" :loading="submitting">提交</el-button>
                <el-button @click="resetMedicalForm">重置</el-button>
                <el-button type="info" @click="saveDraft">保存草稿</el-button>
              </el-form-item>
            </el-form>
          </div>

          <!-- 孕产妇数据录入表单 -->
          <div v-if="dataType === 'maternal'" class="maternal-form">
            <el-form :model="maternalForm" :rules="maternalRules" ref="maternalFormRef" label-width="120px">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="孕妇姓名" prop="name">
                    <el-input v-model="maternalForm.name" placeholder="请输入孕妇姓名"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="年龄" prop="age">
                    <el-input-number v-model="maternalForm.age" :min="15" :max="50" placeholder="请输入年龄"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="孕周" prop="gestational_weeks">
                    <el-input-number v-model="maternalForm.gestational_weeks" :min="1" :max="42" placeholder="请输入孕周"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="孕次" prop="pregnancy_count">
                    <el-input-number v-model="maternalForm.pregnancy_count" :min="1" :max="20" placeholder="请输入孕次"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="产次" prop="parity">
                    <el-input-number v-model="maternalForm.parity" :min="0" :max="10" placeholder="请输入产次"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="妊娠类型" prop="pregnancy_type">
                    <el-select v-model="maternalForm.pregnancy_type" placeholder="请选择妊娠类型">
                      <el-option label="单胎" value="单胎"></el-option>
                      <el-option label="双胎" value="双胎"></el-option>
                      <el-option label="多胎" value="多胎"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="体重(kg)" prop="weight">
                    <el-input-number v-model="maternalForm.weight" :min="30" :max="200" :precision="1" placeholder="体重"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="身高(cm)" prop="height">
                    <el-input-number v-model="maternalForm.height" :min="140" :max="200" placeholder="身高"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="收缩压" prop="systolic_pressure">
                    <el-input-number v-model="maternalForm.systolic_pressure" :min="60" :max="200" placeholder="收缩压"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="舒张压" prop="diastolic_pressure">
                    <el-input-number v-model="maternalForm.diastolic_pressure" :min="40" :max="120" placeholder="舒张压"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="宫高(cm)" prop="fundal_height">
                    <el-input-number v-model="maternalForm.fundal_height" :min="0" :max="50" :precision="1" placeholder="宫高"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="腹围(cm)" prop="abdominal_circumference">
                    <el-input-number v-model="maternalForm.abdominal_circumference" :min="50" :max="150" :precision="1" placeholder="腹围"></el-input-number>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="胎心率" prop="fetal_heart_rate">
                    <el-input-number v-model="maternalForm.fetal_heart_rate" :min="100" :max="200" placeholder="胎心率"></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="水肿程度" prop="edema">
                    <el-select v-model="maternalForm.edema" placeholder="请选择水肿程度">
                      <el-option label="无" value="无"></el-option>
                      <el-option label="轻度" value="轻度"></el-option>
                      <el-option label="中度" value="中度"></el-option>
                      <el-option label="重度" value="重度"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="尿蛋白" prop="urine_protein">
                    <el-select v-model="maternalForm.urine_protein" placeholder="请选择尿蛋白">
                      <el-option label="阴性" value="阴性"></el-option>
                      <el-option label="微量" value="微量"></el-option>
                      <el-option label="1+" value="1+"></el-option>
                      <el-option label="2+" value="2+"></el-option>
                      <el-option label="3+" value="3+"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="尿糖" prop="urine_glucose">
                    <el-select v-model="maternalForm.urine_glucose" placeholder="请选择尿糖">
                      <el-option label="阴性" value="阴性"></el-option>
                      <el-option label="微量" value="微量"></el-option>
                      <el-option label="1+" value="1+"></el-option>
                      <el-option label="2+" value="2+"></el-option>
                      <el-option label="3+" value="3+"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="高危因素" prop="risk_factors">
                <el-checkbox-group v-model="maternalForm.risk_factors">
                  <el-checkbox label="高龄孕妇">高龄孕妇</el-checkbox>
                  <el-checkbox label="妊娠期高血压">妊娠期高血压</el-checkbox>
                  <el-checkbox label="妊娠期糖尿病">妊娠期糖尿病</el-checkbox>
                  <el-checkbox label="贫血">贫血</el-checkbox>
                  <el-checkbox label="甲状腺疾病">甲状腺疾病</el-checkbox>
                  <el-checkbox label="心脏病">心脏病</el-checkbox>
                  <el-checkbox label="肾脏疾病">肾脏疾病</el-checkbox>
                  <el-checkbox label="其他">其他</el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item label="备注" prop="notes">
                <el-input type="textarea" v-model="maternalForm.notes" rows="3" placeholder="请输入备注信息"></el-input>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="submitMaternalForm" :loading="submitting">提交</el-button>
                <el-button @click="resetMaternalForm">重置</el-button>
                <el-button type="info" @click="saveDraft">保存草稿</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </dv-border-box-8>
  </div>
</template>

<script>
export default {
  name: 'DataEntry',
  data() {
    return {
      dataType: 'medical',
      submitting: false,
      
      // 普通医疗数据表单
      medicalForm: {
        name: '',
        gender: '',
        age: null,
        disease_type: '',
        systolic_pressure: null,
        diastolic_pressure: null,
        weight: null,
        height: null,
        blood_sugar: null,
        temperature: null,
        symptoms: '',
        diagnosis: '',
        treatment: ''
      },
      
      // 孕产妇数据表单
      maternalForm: {
        name: '',
        age: null,
        gestational_weeks: null,
        pregnancy_count: null,
        parity: null,
        pregnancy_type: '',
        weight: null,
        height: null,
        systolic_pressure: null,
        diastolic_pressure: null,
        fundal_height: null,
        abdominal_circumference: null,
        fetal_heart_rate: null,
        edema: '',
        urine_protein: '',
        urine_glucose: '',
        risk_factors: [],
        notes: ''
      },
      
      // 表单验证规则
      medicalRules: {
        name: [
          { required: true, message: '请输入患者姓名', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        disease_type: [
          { required: true, message: '请选择疾病类型', trigger: 'change' }
        ]
      },
      
      maternalRules: {
        name: [
          { required: true, message: '请输入孕妇姓名', trigger: 'blur' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        gestational_weeks: [
          { required: true, message: '请输入孕周', trigger: 'blur' }
        ],
        pregnancy_count: [
          { required: true, message: '请输入孕次', trigger: 'blur' }
        ],
        parity: [
          { required: true, message: '请输入产次', trigger: 'blur' }
        ],
        pregnancy_type: [
          { required: true, message: '请选择妊娠类型', trigger: 'change' }
        ]
      }
    }
  },
  
  methods: {
    handleDataTypeChange() {
      // 切换数据类型时重置表单
      this.resetMedicalForm();
      this.resetMaternalForm();
    },
    
    submitMedicalForm() {
      this.$refs.medicalFormRef.validate((valid) => {
        if (valid) {
          this.submitting = true;
          this.$http.post('/api/data/medical/add', this.medicalForm)
            .then(response => {
              this.$message.success('医疗数据提交成功');
              this.resetMedicalForm();
            })
            .catch(error => {
              this.$message.error('提交失败：' + (error.response?.data?.message || error.message));
            })
            .finally(() => {
              this.submitting = false;
            });
        }
      });
    },
    
    submitMaternalForm() {
      this.$refs.maternalFormRef.validate((valid) => {
        if (valid) {
          this.submitting = true;
          this.$http.post('/api/data/maternal/add', this.maternalForm)
            .then(response => {
              this.$message.success('孕产妇数据提交成功');
              this.resetMaternalForm();
            })
            .catch(error => {
              this.$message.error('提交失败：' + (error.response?.data?.message || error.message));
            })
            .finally(() => {
              this.submitting = false;
            });
        }
      });
    },
    
    resetMedicalForm() {
      this.$refs.medicalFormRef?.resetFields();
    },
    
    resetMaternalForm() {
      this.$refs.maternalFormRef?.resetFields();
    },
    
    saveDraft() {
      const draftData = this.dataType === 'medical' ? this.medicalForm : this.maternalForm;
      const draftKey = `draft_${this.dataType}`;
      localStorage.setItem(draftKey, JSON.stringify(draftData));
      this.$message.success('草稿已保存');
    },
    
    loadDraft() {
      const draftKey = `draft_${this.dataType}`;
      const draftData = localStorage.getItem(draftKey);
      if (draftData) {
        const data = JSON.parse(draftData);
        if (this.dataType === 'medical') {
          Object.assign(this.medicalForm, data);
        } else {
          Object.assign(this.maternalForm, data);
        }
      }
    }
  },
  
  mounted() {
    this.loadDraft();
  }
}
</script>

<style lang="less" scoped>
.data-entry-container {
  padding: 20px;
  height: 100%;
  
  .data-entry-content {
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
      
      .data-type-selector {
        .el-radio-group {
          .el-radio-button__inner {
            background: rgba(255, 105, 180, 0.1);
            border-color: #ff69b4;
            color: #ff69b4;
            
            &:hover {
              background: rgba(255, 105, 180, 0.2);
            }
          }
          
          .el-radio-button__orig-radio:checked + .el-radio-button__inner {
            background: #ff69b4;
            border-color: #ff69b4;
            color: #fff;
          }
        }
      }
    }
    
    .form-container {
      max-height: calc(100vh - 200px);
      overflow-y: auto;
      
      .medical-form,
      .maternal-form {
        .el-form {
          .el-form-item {
            margin-bottom: 20px;
            
            .el-form-item__label {
              color: #ff69b4;
              font-weight: bold;
            }
            
            .el-input,
            .el-select,
            .el-input-number {
              width: 100%;
            }
            
            .el-textarea {
              .el-textarea__inner {
                background: rgba(255, 105, 180, 0.05);
                border-color: #ff69b4;
                
                &:focus {
                  border-color: #ff69b4;
                  box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.2);
                }
              }
            }
          }
        }
      }
    }
  }
}

// 滚动条样式
.form-container::-webkit-scrollbar {
  width: 8px;
}

.form-container::-webkit-scrollbar-track {
  background: rgba(64, 158, 255, 0.1);
  border-radius: 4px;
}

.form-container::-webkit-scrollbar-thumb {
  background: rgba(64, 158, 255, 0.3);
  border-radius: 4px;
  
  &:hover {
    background: rgba(64, 158, 255, 0.5);
  }
}
</style>
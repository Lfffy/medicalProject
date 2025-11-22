// 孕产妇风险预测服务
import axios from 'axios';

// 使用空字符串作为基础路径，让vue.config.js中的代理配置处理/api前缀
const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || '';

const maternalPredictionService = {
  // 获取模型状态
  async getModelStatus() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/maternal_risk/models/status`);
      return response.data;
    } catch (error) {
      console.error('获取模型状态失败:', error);
      throw error;
    }
  },

  // 预测子痫前期风险
  async predictPreeclampsia(patientData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/maternal_risk/predict/preeclampsia`, patientData);
      return response.data;
    } catch (error) {
      console.error('预测子痫前期风险失败:', error);
      throw error;
    }
  },

  // 预测妊娠期糖尿病风险
  async predictGestationalDiabetes(patientData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/maternal_risk/predict/gestational_diabetes`, patientData);
      return response.data;
    } catch (error) {
      console.error('预测妊娠期糖尿病风险失败:', error);
      throw error;
    }
  },

  // 预测早产风险
  async predictPretermBirth(patientData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/maternal_risk/predict/preterm_birth`, patientData);
      return response.data;
    } catch (error) {
      console.error('预测早产风险失败:', error);
      throw error;
    }
  },

  // 综合风险评估
  async predictComprehensiveRisk(patientData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/maternal_risk/predict/comprehensive`, patientData);
      return response.data;
    } catch (error) {
      console.error('综合风险评估失败:', error);
      throw error;
    }
  },

  // 获取特征信息
  async getFeatureInfo() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/maternal_risk/features`);
      return response.data;
    } catch (error) {
      console.error('获取特征信息失败:', error);
      throw error;
    }
  },

  // 获取统计信息
  async getStatistics() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/maternal_risk/statistics`);
      return response.data;
    } catch (error) {
      console.error('获取统计信息失败:', error);
      throw error;
    }
  },

  // 训练模型
  async trainModel(modelType = 'all') {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/maternal_risk/train/models`, { model_type: modelType });
      return response.data;
    } catch (error) {
      console.error('训练模型失败:', error);
      throw error;
    }
  },

  // 健康检查
  async healthCheck() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/maternal_risk/health`);
      return response.data;
    } catch (error) {
      console.error('健康检查失败:', error);
      throw error;
    }
  }
};

export default maternalPredictionService;
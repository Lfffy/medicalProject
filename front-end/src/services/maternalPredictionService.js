// 孕产妇风险预测服务
import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8081/api',
  timeout: 20000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 增加详细日志
apiClient.interceptors.request.use(
  config => {
    console.log('API请求:', {
      url: config.url,
      method: config.method,
      data: config.data ? JSON.parse(JSON.stringify(config.data)) : null
    });
    return config;
  },
  error => {
    console.error('请求配置错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器 - 增加详细日志和错误处理
apiClient.interceptors.response.use(
  response => {
    console.log('API响应:', {
      url: response.config.url,
      status: response.status,
      data: response.data
    });
    return response;
  },
  error => {
    console.error('API响应错误:', {
      message: error.message,
      response: error.response ? {
        status: error.response.status,
        data: error.response.data
      } : null
    });
    return Promise.reject(error);
  }
);

const maternalPredictionService = {
  // 获取模型状态
  async getModelStatus() {
    try {
      const response = await apiClient.get('/maternal_risk/models/status');
      return response.data;
    } catch (error) {
      console.error('获取模型状态失败:', error);
      // 返回模拟数据作为备选
      return {
        status: 'simulation',
        models: [
          { type: 'preeclampsia', available: true, last_updated: new Date().toISOString() },
          { type: 'gestational_diabetes', available: true, last_updated: new Date().toISOString() },
          { type: 'preterm_birth', available: true, last_updated: new Date().toISOString() }
        ]
      };
    }
  },

  // 预测子痫前期风险
  async predictPreeclampsia(patientData) {
    try {
      const response = await apiClient.post('/maternal_risk/predict/preeclampsia', patientData);
      return response.data;
    } catch (error) {
      console.error('预测子痫前期风险失败:', error);
      throw error;
    }
  },

  // 预测妊娠期糖尿病风险
  async predictGestationalDiabetes(patientData) {
    try {
      const response = await apiClient.post('/maternal_risk/predict/gestational_diabetes', patientData);
      return response.data;
    } catch (error) {
      console.error('预测妊娠期糖尿病风险失败:', error);
      throw error;
    }
  },

  // 预测早产风险
  async predictPretermBirth(patientData) {
    try {
      const response = await apiClient.post('/maternal_risk/predict/preterm_birth', patientData);
      return response.data;
    } catch (error) {
      console.error('预测早产风险失败:', error);
      throw error;
    }
  },

  // 综合风险评估
  async predictComprehensiveRisk(patientData) {
    try {
      // 添加必要的字段转换和验证
      const enrichedData = {
        ...patientData,
        timestamp: new Date().toISOString(),
        request_type: 'comprehensive_prediction'
      };
      console.log('提交给后端的富集数据:', enrichedData);
      
      // 调用后端API
      const response = await apiClient.post('/maternal_risk/predict/comprehensive', enrichedData);
      console.log('后端API返回原始数据:', response.data);
      
      // 验证响应数据结构
      if (!response.data || typeof response.data !== 'object') {
        throw new Error('无效的预测结果格式');
      }
      
      // 直接返回后端API的实际数据，确保格式与前端期望一致
      const backendResult = response.data;
      
      // 确保返回的数据格式规范，并标记来源
      return {
        success: backendResult.success !== false, // 如果后端没有明确设置success为false，则视为成功
        comprehensive: backendResult.comprehensive || backendResult,
        preeclampsia: backendResult.preeclampsia,
        gestational_diabetes: backendResult.gestational_diabetes,
        preterm_birth: backendResult.preterm_birth,
        overall_risk_level: backendResult.overall_risk_level || backendResult.comprehensive?.overall_risk_level,
        prediction_id: backendResult.prediction_id,
        source: 'machine_learning'
      };
    } catch (error) {
      console.error('综合风险评估失败:', error);
      // 不返回模拟数据，直接抛出错误，让调用者知道API调用失败
      // 这样前端可以正确显示错误信息而不是模拟数据
      throw error;
    }
  },

  // 获取特征信息
  async getFeatureInfo() {
    try {
      const response = await apiClient.get('/maternal_risk/features');
      return response.data;
    } catch (error) {
      console.error('获取特征信息失败:', error);
      // 返回空数组作为备选
      return [];
    }
  },

  // 获取统计信息
  async getStatistics() {
    try {
      const response = await apiClient.get('/maternal_risk/statistics');
      return response.data;
    } catch (error) {
      console.error('获取统计信息失败:', error);
      // 返回空对象作为备选
      return {};
    }
  },

  // 训练模型
  async trainModel(modelType = 'all') {
    try {
      const response = await apiClient.post('/maternal_risk/train/models', { model_type: modelType });
      return response.data;
    } catch (error) {
      console.error('训练模型失败:', error);
      throw error;
    }
  },

  // 健康检查
  async healthCheck() {
    try {
      const response = await apiClient.get('/maternal_risk/health');
      return response.data;
    } catch (error) {
      console.error('健康检查失败:', error);
      // 返回基本健康状态作为备选
      return { status: 'service_unavailable' };
    }
  },
  
  // 获取历史预测记录
  async getPredictionHistory(patientId = null) {
    try {
      const url = patientId ? `/maternal_risk/history?patient_id=${patientId}` : '/maternal_risk/history';
      const response = await apiClient.get(url);
      return response.data;
    } catch (error) {
      console.error('获取历史记录失败:', error);
      // 返回空数组作为备选
      return [];
    }
  }
};

export default maternalPredictionService;
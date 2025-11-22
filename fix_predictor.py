import os
import sys

# 读取原始文件
with open('maternal_risk_predictor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找predict_comprehensive_risk方法
start_index = content.find('def predict_comprehensive_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:')
end_index = content.find('\n    def ', start_index + 1)
if end_index == -1:
    end_index = len(content)

# 提取原始方法
original_method = content[start_index:end_index]

# 创建新的方法实现
new_method = '''def predict_comprehensive_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合风险评估
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            综合风险预测结果字典
        """
        try:
            # 预测各类风险
            preeclampsia_result = self.predict_preeclampsia_risk(patient_data)
            gestational_diabetes_result = self.predict_gestational_diabetes_risk(patient_data)
            preterm_birth_result = self.predict_preterm_birth_risk(patient_data)
            
            # 计算综合风险评分
            risk_scores = []
            risk_factors = []
            
            if preeclampsia_result:
                risk_scores.append(preeclampsia_result['risk_probability'])
                risk_factors.extend(preeclampsia_result['top_risk_factors'])
            
            if gestational_diabetes_result:
                risk_scores.append(gestational_diabetes_result['risk_probability'])
                risk_factors.extend(gestational_diabetes_result['top_risk_factors'])
            
            if preterm_birth_result:
                risk_scores.append(preterm_birth_result['risk_probability'])
                risk_factors.extend(preterm_birth_result['top_risk_factors'])
            
            # 计算平均风险
            if risk_scores:
                overall_risk = np.mean(risk_scores)
            else:
                overall_risk = 0.0
            
            # 确定风险等级
            if overall_risk >= 0.7:
                risk_level = '高风险'
            elif overall_risk >= 0.4:
                risk_level = '中风险'
            else:
                risk_level = '低风险'
            
            # 合并风险因素（去重）
            unique_factors = {}
            for factor in risk_factors:
                name = factor['name']
                if name not in unique_factors or factor['importance'] > unique_factors[name]['importance']:
                    unique_factors[name] = factor
            
            # 按重要性排序
            sorted_factors = sorted(unique_factors.values(), key=lambda x: x['importance'], reverse=True)[:5]
            
            # 创建综合结果 - 修改为前端期望的结构
            result = {
                'comprehensive': {
                    'overall_risk_level': risk_level,
                    'overall_risk_score': float(overall_risk),
                    'risk_description': f'根据您的健康数据分析，您的综合风险等级为{risk_level}。',
                    'recommendations': self.get_comprehensive_recommendations(risk_level, overall_risk)
                },
                'preeclampsia': {
                    'risk_level': self._get_risk_level(preeclampsia_result['risk_probability'] if preeclampsia_result else 0),
                    'risk_score': int((preeclampsia_result['risk_probability'] if preeclampsia_result else 0) * 100),
                    'description': f'子痫前期风险等级为{self._get_risk_level(preeclampsia_result["risk_probability"] if preeclampsia_result else 0)}。',
                    'key_factors': [factor['name'] for factor in (preeclampsia_result['top_risk_factors'] if preeclampsia_result else [])[:3]]
                },
                'gestational_diabetes': {
                    'risk_level': self._get_risk_level(gestational_diabetes_result['risk_probability'] if gestational_diabetes_result else 0),
                    'risk_score': int((gestational_diabetes_result['risk_probability'] if gestational_diabetes_result else 0) * 100),
                    'description': f'妊娠期糖尿病风险等级为{self._get_risk_level(gestational_diabetes_result["risk_probability"] if gestational_diabetes_result else 0)}。',
                    'key_factors': [factor['name'] for factor in (gestational_diabetes_result['top_risk_factors'] if gestational_diabetes_result else [])[:3]]
                },
                'preterm_birth': {
                    'risk_level': self._get_risk_level(preterm_birth_result['risk_probability'] if preterm_birth_result else 0),
                    'risk_score': int((preterm_birth_result['risk_probability'] if preterm_birth_result else 0) * 100),
                    'description': f'早产风险等级为{self._get_risk_level(preterm_birth_result["risk_probability"] if preterm_birth_result else 0)}。',
                    'key_factors': [factor['name'] for factor in (preterm_birth_result['top_risk_factors'] if preterm_birth_result else [])[:3]]
                },
                'top_risk_factors': sorted_factors,
                'overall_risk_level': risk_level,
                'overall_risk_score': float(overall_risk),
                'recommendations': self.get_comprehensive_recommendations(risk_level, overall_risk)
            }
            
            return result
            
        except Exception as e:
            print(f"综合风险评估错误: {e}")
            return None
    
    def _get_risk_level(self, probability: float) -> str:
        """根据概率获取风险等级"""
        if probability >= 0.7:
            return '高风险'
        elif probability >= 0.4:
            return '中风险'
        else:
            return '低风险'"""

# 替换方法
new_content = content[:start_index] + new_method + content[end_index:]

# 写入文件
with open('maternal_risk_predictor.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("已修改predict_comprehensive_risk方法以匹配前端期望的数据结构")
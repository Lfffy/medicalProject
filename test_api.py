import requests
import json

# 测试数据
test_data = {
    'age': 28,
    'height': 165,
    'weight': 65,
    'bmi': 23.9,
    'parity': 0,
    'pregnancy_count': 1,
    'gestational_weeks': 24,
    'systolic_pressure': 120,
    'diastolic_pressure': 80,
    'heart_rate': 75,
    'temperature': 36.5,
    'blood_sugar': 4.8,
    'hemoglobin': 120,
    'risk_factors': '',
    'pregnancy_type': '单胎',
    'last_menstrual_date': '2023-03-15',
    'due_date': '2023-12-20'
}

# 测试综合风险预测
response = requests.post('http://localhost:8081/api/maternal-risk/predict/comprehensive', json=test_data, headers={'Content-Type': 'application/json'})

print('状态码:', response.status_code)
result = response.json()
print('综合风险等级:', result.get('data', {}).get('overall_risk_level', '未知'))
print('综合风险评分:', result.get('data', {}).get('overall_risk_score', 0))

# 检查个别风险
individual_risks = result.get('data', {}).get('individual_risks', {})
print('子痫前期风险:', individual_risks.get('preeclampsia', {}).get('risk_level', '未知'))
print('妊娠期糖尿病风险:', individual_risks.get('gestational_diabetes', {}).get('risk_level', '未知'))
print('早产风险:', individual_risks.get('preterm_birth', {}).get('risk_level', '未知'))
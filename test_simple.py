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

# 只打印关键信息
print('综合风险等级:', result.get('data', {}).get('overall_risk_level'))
print('综合风险评分:', result.get('data', {}).get('overall_risk_score'))

# 检查各个风险等级
if 'preeclampsia' in result.get('data', {}):
    print('子痫前期风险等级:', result['data']['preeclampsia'].get('risk_level'))
    
if 'gestational_diabetes' in result.get('data', {}):
    print('妊娠期糖尿病风险等级:', result['data']['gestational_diabetes'].get('risk_level'))
    
if 'preterm_birth' in result.get('data', {}):
    print('早产风险等级:', result['data']['preterm_birth'].get('risk_level'))
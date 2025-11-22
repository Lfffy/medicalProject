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

# 检查返回的数据结构是否符合前端期望
print('返回数据结构:')
print(json.dumps(result, indent=2, ensure_ascii=False))

# 检查前端期望的数据结构
expected_structure = {
    'comprehensive': {
        'overall_risk_level': 'string',
        'overall_risk_score': 'number',
        'risk_description': 'string',
        'recommendations': ['string']
    },
    'preeclampsia': {
        'risk_level': 'string',
        'risk_score': 'number',
        'description': 'string',
        'key_factors': ['string']
    },
    'gestational_diabetes': {
        'risk_level': 'string',
        'risk_score': 'number',
        'description': 'string',
        'key_factors': ['string']
    },
    'preterm_birth': {
        'risk_level': 'string',
        'risk_score': 'number',
        'description': 'string',
        'key_factors': ['string']
    }
}

print('\n期望的数据结构:')
print(json.dumps(expected_structure, indent=2, ensure_ascii=False))

# 检查实际返回的数据是否包含前端期望的字段
def check_structure(actual, expected, path=''):
    missing = []
    for key, value in expected.items():
        current_path = f"{path}.{key}" if path else key
        if key not in actual:
            missing.append(current_path)
        elif isinstance(value, dict):
            missing.extend(check_structure(actual[key], value, current_path))
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # 如果期望列表中的元素是字典，检查第一个元素
            if actual[key] and isinstance(actual[key][0], dict):
                missing.extend(check_structure(actual[key][0], value[0], f"{current_path}[0]"))
    return missing

missing_fields = check_structure(result.get('data', {}), expected_structure)
if missing_fields:
    print(f'\n缺少字段: {missing_fields}')
else:
    print('\n数据结构符合前端期望')
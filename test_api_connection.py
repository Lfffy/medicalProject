import requests
import json

# 测试API连接
def test_api_connection():
    base_url = "http://localhost:8081"
    
    print("=== 测试API连接 ===")
    
    # 测试健康检查端点
    print("\n1. 测试健康检查端点:")
    try:
        response = requests.get(f"{base_url}/api/maternal-risk/health")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("响应:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("错误:", response.text)
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试模型状态端点
    print("\n2. 测试模型状态端点:")
    try:
        response = requests.get(f"{base_url}/api/maternal-risk/models/status")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("响应:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("错误:", response.text)
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试综合风险预测端点
    print("\n3. 测试综合风险预测端点:")
    test_data = {
        "age": 30,
        "height": 165,
        "weight": 65,
        "gestational_weeks": 20,
        "pregnancy_type": "单胎",
        "systolic_pressure": 120,
        "diastolic_pressure": 80,
        "heart_rate": 75,
        "temperature": 36.5,
        "blood_sugar": 5.0,
        "hemoglobin": 120,
        "parity": 0,
        "pregnancy_count": 1,
        "lmp_month": 1,
        "risk_factors": []
    }
    
    try:
        response = requests.post(f"{base_url}/api/maternal-risk/predict/comprehensive", json=test_data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("响应:", json.dumps(result, indent=2, ensure_ascii=False))
            
            # 提取关键信息
            comprehensive = result.get('data', {}).get('comprehensive', {})
            print("\n关键信息:")
            print(f"- 综合风险等级: {comprehensive.get('overall_risk_level')}")
            print(f"- 综合风险评分: {comprehensive.get('overall_risk_score')}")
            
            preeclampsia = result.get('data', {}).get('preeclampsia', {})
            print(f"- 子痫前期风险等级: {preeclampsia.get('risk_level')}")
            print(f"- 子痫前期风险评分: {preeclampsia.get('risk_score')}")
            
            gestational_diabetes = result.get('data', {}).get('gestational_diabetes', {})
            print(f"- 妊娠期糖尿病风险等级: {gestational_diabetes.get('risk_level')}")
            print(f"- 妊娠期糖尿病风险评分: {gestational_diabetes.get('risk_score')}")
            
            preterm_birth = result.get('data', {}).get('preterm_birth', {})
            print(f"- 早产风险等级: {preterm_birth.get('risk_level')}")
            print(f"- 早产风险评分: {preterm_birth.get('risk_score')}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_api_connection()
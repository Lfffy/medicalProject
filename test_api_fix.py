import requests

# 测试API端点
def test_api_endpoints():
    base_url = 'http://localhost:8081'
    
    print("Testing API endpoints...\n")
    
    # 测试dashboard overview API
    print("1. Testing /api/dashboard/overview...")
    try:
        response = requests.get(f'{base_url}/api/dashboard/overview')
        print(f"   Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! Data received: {data['message']}")
            print(f"   Total patients: {data['data']['total_patients']}")
            print(f"   Total maternal: {data['data']['total_maternal']}")
            print(f"   High risk cases: {data['data']['high_risk_cases']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print("\n2. Testing /api/monitoring/realtime...")
    try:
        response = requests.get(f'{base_url}/api/monitoring/realtime')
        print(f"   Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! Data received: {data['message']}")
            print(f"   Realtime data count: {len(data['data']['realtimeData'])}")
            print(f"   Recent alerts count: {len(data['data']['recentAlerts'])}")
            print(f"   Total alert count: {data['data']['alertCount']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")

if __name__ == '__main__':
    test_api_endpoints()

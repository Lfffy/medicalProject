import requests
import json

# 测试后端首页数据API
url = "http://localhost:8081/getHomeData"
try:
    response = requests.get(url)
    data = response.json()
    
    print("状态码:", response.status_code)
    print("响应消息:", data.get('message'))
    print("响应代码:", data.get('code'))
    
    if data.get('code') == 200:
        print("\n数据获取成功!")
        print("病例数据数量:", len(data.get('data', {}).get('casesData', [])))
        print("中心数据数量:", len(data.get('data', {}).get('circleData', [])))
        
        # 打印前几个病例数据
        cases = data.get('data', {}).get('casesData', [])
        if cases:
            print("\n前3个病例数据:")
            for i, case in enumerate(cases[:3]):
                print(f"  病例{i+1}: {case}")
    else:
        print("API返回错误:", data.get('message'))
        
except Exception as e:
    print("请求失败:", str(e))
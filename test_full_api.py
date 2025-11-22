import requests
import json

# 测试后端API是否返回模拟数据
url = "http://localhost:8081/getHomeData"
try:
    response = requests.get(url)
    data = response.json()
    
    print("后端API测试结果:")
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
            print("\n后端返回空病例数据")
            
        # 打印中心数据
        circleData = data.get('data', {}).get('circleData', [])
        if circleData:
            print("\n中心数据:")
            for item in circleData:
                print(f"  {item}")
        else:
            print("\n后端返回空中心数据")
    else:
        print("API返回错误:", data.get('message'))
        
except Exception as e:
    print("请求失败:", str(e))

# 测试前端页面是否可以访问
print("\n前端页面测试:")
try:
    response = requests.get("http://localhost:8082")
    if response.status_code == 200:
        print("前端页面加载成功，状态码:", response.status_code)
    else:
        print("前端页面加载失败，状态码:", response.status_code)
except Exception as e:
    print("前端页面请求失败:", str(e))
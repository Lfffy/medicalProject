import requests
from bs4 import BeautifulSoup

# 测试前端页面是否正确加载
url = "http://localhost:8082"
try:
    response = requests.get(url)
    if response.status_code == 200:
        print("前端页面加载成功!")
        # 检查页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找是否有错误信息
        error_elements = soup.find_all(text=lambda text: "获取数据失败" in text)
        if error_elements:
            print("发现错误信息:", error_elements[0].strip())
        
        # 查找是否有模拟数据
        mock_data_elements = soup.find_all(text=lambda text: "张女士" in text)
        if mock_data_elements:
            print("发现模拟数据，页面正常显示模拟内容")
        else:
            print("未发现模拟数据")
    else:
        print(f"前端页面加载失败，状态码: {response.status_code}")
        
except Exception as e:
    print(f"请求失败: {str(e)}")
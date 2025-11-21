import random
import pandas as pd

def getMockCasesData():
    """生成模拟病例数据"""
    diseases = ['感冒', '发烧', '咳嗽', '头痛', '胃痛', '高血压', '糖尿病', '心脏病']
    departments = ['内科', '外科', '儿科', '妇科', '眼科', '耳鼻喉科']
    hospitals = ['中心医院', '人民医院', '中医院', '妇幼保健院']
    
    data = []
    for i in range(100):
        data.append({
            'id': i + 1,
            'name': f'患者{i+1}',
            'age': random.randint(1, 80),
            'gender': random.choice(['男', '女']),
            'disease': random.choice(diseases),
            'department': random.choice(departments),
            'hospital': random.choice(hospitals)
        })
    
    return data

def getMockMaternalData():
    """生成模拟孕产妇数据"""
    pregnancy_status = ['早孕', '中孕', '晚孕', '产后']
    departments = ['产科', '妇科', '新生儿科']
    hospitals = ['妇幼保健院', '中心医院', '人民医院']
    
    data = []
    for i in range(50):
        data.append({
            'id': i + 1,
            'name': f'孕产妇{i+1}',
            'age': random.randint(20, 45),
            'gender': '女',
            'pregnancy_status': random.choice(pregnancy_status),
            'department': random.choice(departments),
            'hospital': random.choice(hospitals),
            'gestation_week': random.randint(1, 42) if random.choice(pregnancy_status) != '产后' else 0
        })
    
    return data
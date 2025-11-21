import pandas as pd
import numpy as np
from utils.query import querys
from utils.mock_data import getMockCasesData, getMockMaternalData

def getAllCasesData():
    """获取所有病例数据（优先使用孕产妇数据）"""
    try:
        # 首先尝试从数据库获取数据
        result = querys('SHOW TABLES')
        
        # 如果数据库连接成功，尝试获取数据
        if result and result != '执行成功':
            # 检查是否有孕产妇表
            check_maternal = querys("SHOW TABLES LIKE 'maternal_info'")
            if check_maternal:
                maternal_data = querys('select * from maternal_info')
                if maternal_data:
                    print("从数据库获取孕产妇数据")
                    return maternal_data
            
            # 检查是否有普通病例表
            check_cases = querys("SHOW TABLES LIKE 'cases'")
            if check_cases:
                cases_data = querys('select * from cases')
                if cases_data:
                    print("从数据库获取普通病例数据")
                    return cases_data
        
        # 如果数据库连接失败或没有数据，使用模拟数据
        print("数据库连接失败，使用模拟孕产妇数据")
        return getMockMaternalData()
        
    except Exception as e:
        print(f"数据库连接失败: {e}")
        print("使用模拟孕产妇数据")
        return getMockMaternalData()

def getMaternalCasesData():
    """专门获取孕产妇数据"""
    try:
        check_maternal = querys("SHOW TABLES LIKE 'maternal_info'")
        if check_maternal:
            maternal_data = querys('select * from maternal_info')
            if maternal_data:
                print("从数据库获取孕产妇数据")
                return maternal_data
        
        # 如果数据库没有孕产妇数据，使用模拟数据
        print("数据库无孕产妇数据，使用模拟数据")
        return getMockMaternalData()
        
    except Exception as e:
        print(f"获取孕产妇数据失败: {e}")
        print("使用模拟孕产妇数据")
        return getMockMaternalData()

# 保留原有的函数名以保持兼容性
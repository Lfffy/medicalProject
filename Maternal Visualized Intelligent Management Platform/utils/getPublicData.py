import pandas as pd
import numpy as np
from utils.query import querys
from utils.mock_data import getMockCasesData, getMockMaternalData

def getAllCasesData():
    """获取所有病例数据（优先使用孕产妇数据）"""
    try:
        # 首先尝试从数据库获取数据
        # 检查是否有孕产妇表
        check_maternal = querys("SELECT name FROM sqlite_master WHERE type='table' AND name='maternal_info'")
        if check_maternal and len(check_maternal) > 0:
            maternal_data = querys('select * from maternal_info')
            if maternal_data and len(maternal_data) > 0:
                print("从数据库获取真实孕产妇数据")
                # 将sqlite3.Row对象转换为字典列表
                result = []
                for row in maternal_data:
                    # 确保我们可以正确转换为字典
                    if hasattr(row, '__iter__'):
                        # 如果row是元组，我们需要手动创建字典
                        columns = ['id', 'patient_id', 'last_menstrual_period', 'expected_date_delivery', 
                                  'current_gestational_week', 'parity', 'gravidity', 'abortion_count', 
                                  'live_birth_count', 'preterm_birth_count', 'stillbirth_count', 
                                  'ectopic_pregnancy_count', 'previous_cesarean', 'pregnancy_complications', 
                                  'risk_level', 'risk_factors', 'prenatal_care_count', 'last_prenatal_date', 
                                  'expected_delivery_hospital', 'delivery_plan', 'created_at', 'updated_at']
                        row_dict = {columns[i]: row[i] for i in range(min(len(columns), len(row)))} if len(row) > 0 else {}
                        result.append(row_dict)
                    elif hasattr(row, 'keys'):
                        # 如果row已经有keys方法（如sqlite3.Row）
                        result.append(dict(row))
                print(f"成功获取{len(result)}条真实孕产妇数据")
                # 确保返回的是数据库数据而不是模拟数据
                return result
        
        # 检查是否有普通病例表
        check_cases = querys("SELECT name FROM sqlite_master WHERE type='table' AND name='cases'")
        if check_cases and len(check_cases) > 0:
            cases_data = querys('select * from cases')
            if cases_data and len(cases_data) > 0:
                print("从数据库获取真实普通病例数据")
                # 将sqlite3.Row对象转换为字典列表
                result = []
                for row in cases_data:
                    if hasattr(row, 'keys'):
                        result.append(dict(row))
                return result
        
        # 检查是否有medical_data表
        check_medical = querys("SELECT name FROM sqlite_master WHERE type='table' AND name='medical_data'")
        if check_medical and len(check_medical) > 0:
            medical_data = querys('select * from medical_data')
            if medical_data and len(medical_data) > 0:
                print("从数据库获取真实医疗数据")
                # 将sqlite3.Row对象转换为字典列表
                result = []
                for row in medical_data:
                    if hasattr(row, 'keys'):
                        result.append(dict(row))
                return result
        
        # 如果数据库中没有任何表或数据，返回空列表而不是模拟数据
        print("警告：数据库中没有找到任何有效表或数据")
        return []
        
    except Exception as e:
        print(f"获取数据时发生异常: {e}")
        # 发生异常时返回空列表而不是模拟数据
        return []

def getMaternalCasesData():
    """专门获取孕产妇数据"""
    try:
        check_maternal = querys("SELECT name FROM sqlite_master WHERE type='table' AND name='maternal_info'")
        if check_maternal and len(check_maternal) > 0:
            maternal_data = querys('select * from maternal_info')
            if maternal_data and len(maternal_data) > 0:
                print("从数据库获取真实孕产妇数据")
                # 将sqlite3.Row对象转换为字典列表，并确保返回真实数据
                result = []
                for row in maternal_data:
                    # 确保我们可以正确转换为字典
                    if hasattr(row, '__iter__'):
                        # 如果row是元组，我们需要手动创建字典
                        columns = ['id', 'patient_id', 'last_menstrual_period', 'expected_date_delivery', 
                                  'current_gestational_week', 'parity', 'gravidity', 'abortion_count', 
                                  'live_birth_count', 'preterm_birth_count', 'stillbirth_count', 
                                  'ectopic_pregnancy_count', 'previous_cesarean', 'pregnancy_complications', 
                                  'risk_level', 'risk_factors', 'prenatal_care_count', 'last_prenatal_date', 
                                  'expected_delivery_hospital', 'delivery_plan', 'created_at', 'updated_at']
                        row_dict = {columns[i]: row[i] for i in range(min(len(columns), len(row)))} if len(row) > 0 else {}
                        result.append(row_dict)
                    elif hasattr(row, 'keys'):
                        # 如果row已经有keys方法（如sqlite3.Row）
                        result.append(dict(row))
                print(f"成功获取{len(result)}条真实孕产妇数据")
                # 确保我们返回的是数据库数据而不是模拟数据
                # 即使数据中包含CURRENT_TEXTSTAMP，这也是真实的数据库数据
                return result
        
        # 只有当数据库确实没有数据时才使用模拟数据
        print("警告：数据库中maternal_info表不存在或无数据")
        # 这里不再直接返回模拟数据，而是返回一个空列表，让调用者知道没有真实数据
        return []
        
    except Exception as e:
        print(f"获取孕产妇数据时发生异常: {e}")
        # 发生异常时也不使用模拟数据，返回空列表
        return []

# 保留原有的函数名以保持兼容性
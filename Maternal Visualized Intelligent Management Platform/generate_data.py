#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成更多孕产妇数据用于训练模型
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta

def generate_maternal_data(num_samples=100):
    """生成孕产妇数据"""
    data = []
    
    for i in range(1, num_samples + 1):
        # 基本信息随机生成
        age = random.randint(20, 40)
        height = random.randint(150, 175)
        weight = random.randint(50, 90)
        bmi = round(weight / ((height/100) ** 2), 1)
        parity = random.randint(0, 3)
        pregnancy_count = random.randint(1, 5)
        gestational_weeks = random.randint(10, 40)
        pregnancy_type = random.choice(["单胎", "双胎", "多胎"])
        
        # 生命体征
        systolic_pressure = random.randint(100, 160)
        diastolic_pressure = random.randint(60, 100)
        heart_rate = random.randint(60, 90)
        temperature = round(36.0 + random.random() * 1.0, 1)
        blood_sugar = round(4.0 + random.random() * 3.0, 1)
        hemoglobin = round(10.0 + random.random() * 3.0, 1)
        
        # 糖尿病相关指标
        fasting_glucose = round(4.0 + random.random() * 2.0, 1)
        ogtt_1h = round(6.0 + random.random() * 5.0, 1)
        ogtt_2h = round(5.0 + random.random() * 4.0, 1)
        
        # 早产相关指标
        cervical_length = random.randint(15, 45)
        fetal_fibronectin = random.randint(5, 80)
        
        # 风险因素
        risk_factors_options = ["", "高龄", "肥胖", "高血压", "糖尿病", "多胎", "既往子痫前期", 
                               "既往妊娠期糖尿病", "吸烟", "家族史"]
        risk_factors = random.sample(risk_factors_options, random.randint(0, 3))
        risk_factors = ",".join(risk_factors)
        
        # 日期
        lmp_date = datetime.now() - timedelta(weeks=gestational_weeks)
        due_date = lmp_date + timedelta(weeks=40)
        
        # 根据生命体征和指标确定风险标签
        preeclampsia = 1 if systolic_pressure >= 140 or diastolic_pressure >= 90 else 0
        gestational_diabetes = 1 if fasting_glucose >= 5.1 or ogtt_1h >= 10.0 or ogtt_2h >= 8.5 else 0
        preterm_birth = 1 if gestational_weeks < 37 and cervical_length < 25 else 0
        
        # 综合风险等级
        risk_score = preeclampsia * 0.4 + gestational_diabetes * 0.3 + preterm_birth * 0.3
        if risk_score >= 0.7:
            risk_level = "高风险"
        elif risk_score >= 0.3:
            risk_level = "中风险"
        else:
            risk_level = "低风险"
        
        # 创建记录
        record = {
            "id": i,
            "patient_id": random.randint(1000, 9999),
            "age": age,
            "height": height,
            "weight": weight,
            "bmi": bmi,
            "parity": parity,
            "pregnancy_count": pregnancy_count,
            "gestational_weeks": gestational_weeks,
            "pregnancy_type": pregnancy_type,
            "systolic_pressure": systolic_pressure,
            "diastolic_pressure": diastolic_pressure,
            "heart_rate": heart_rate,
            "temperature": temperature,
            "blood_sugar": blood_sugar,
            "hemoglobin": hemoglobin,
            "fasting_glucose": fasting_glucose,
            "ogtt_1h": ogtt_1h,
            "ogtt_2h": ogtt_2h,
            "cervical_length": cervical_length,
            "fetal_fibronectin": fetal_fibronectin,
            "risk_factors": risk_factors,
            "last_menstrual_date": lmp_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "preeclampsia": preeclampsia,
            "gestational_diabetes": gestational_diabetes,
            "preterm_birth": preterm_birth,
            "risk_level": risk_level,
            "notes": f"孕产妇备注{i}",
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
        
        data.append(record)
    
    return data

# 生成数据
maternal_data = generate_maternal_data(200)

# 保存到文件
with open("data/maternal_data_large.json", "w", encoding="utf-8") as f:
    json.dump(maternal_data, f, ensure_ascii=False, indent=2)

print(f"已生成 {len(maternal_data)} 条孕产妇数据，保存到 data/maternal_data_large.json")
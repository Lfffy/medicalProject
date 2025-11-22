#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化数据库并导入孕产妇数据
"""

import sqlite3
import json
import os

def init_database():
    """初始化数据库"""
    # 连接数据库
    conn = sqlite3.connect('maternal_health.db')
    cursor = conn.cursor()
    
    # 创建孕产妇信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maternal_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        age INTEGER,
        height REAL,
        weight REAL,
        bmi REAL,
        parity INTEGER,
        pregnancy_count INTEGER,
        gestational_weeks INTEGER,
        pregnancy_type TEXT,
        systolic_pressure INTEGER,
        diastolic_pressure INTEGER,
        heart_rate REAL,
        temperature REAL,
        blood_sugar REAL,
        hemoglobin REAL,
        fasting_glucose REAL,
        ogtt_1h REAL,
        ogtt_2h REAL,
        cervical_length REAL,
        fetal_fibronectin REAL,
        risk_factors TEXT,
        last_menstrual_date DATE,
        due_date DATE,
        preeclampsia INTEGER,
        gestational_diabetes INTEGER,
        preterm_birth INTEGER,
        risk_level TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("数据库初始化完成")

def import_maternal_data():
    """导入孕产妇数据"""
    # 连接数据库
    conn = sqlite3.connect('maternal_health.db')
    cursor = conn.cursor()
    
    # 读取JSON数据文件
    data_file = os.path.join('data', 'maternal_data_complete.json')
    
    if not os.path.exists(data_file):
        print(f"数据文件不存在: {data_file}")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        maternal_data = json.load(f)
    
    # 清空现有数据
    cursor.execute("DELETE FROM maternal_info")
    
    # 插入数据
    for record in maternal_data:
        cursor.execute('''
        INSERT INTO maternal_info (
            patient_id, age, height, weight, bmi, parity, pregnancy_count, 
            gestational_weeks, pregnancy_type, systolic_pressure, diastolic_pressure,
            heart_rate, temperature, blood_sugar, hemoglobin, fasting_glucose,
            ogtt_1h, ogtt_2h, cervical_length, fetal_fibronectin, risk_factors,
            last_menstrual_date, due_date, preeclampsia, gestational_diabetes,
            preterm_birth, risk_level, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record.get('patient_id'),
            record.get('age'),
            record.get('height'),
            record.get('weight'),
            record.get('bmi'),
            record.get('parity'),
            record.get('pregnancy_count'),
            record.get('gestational_weeks'),
            record.get('pregnancy_type'),
            record.get('systolic_pressure'),
            record.get('diastolic_pressure'),
            record.get('heart_rate'),
            record.get('temperature'),
            record.get('blood_sugar'),
            record.get('hemoglobin'),
            record.get('fasting_glucose'),
            record.get('ogtt_1h'),
            record.get('ogtt_2h'),
            record.get('cervical_length'),
            record.get('fetal_fibronectin'),
            record.get('risk_factors'),
            record.get('last_menstrual_date'),
            record.get('due_date'),
            record.get('preeclampsia'),
            record.get('gestational_diabetes'),
            record.get('preterm_birth'),
            record.get('risk_level'),
            record.get('notes')
        ))
    
    conn.commit()
    conn.close()
    print(f"成功导入 {len(maternal_data)} 条孕产妇数据")

def verify_data():
    """验证数据导入"""
    conn = sqlite3.connect('maternal_health.db')
    cursor = conn.cursor()
    
    # 检查记录数
    cursor.execute("SELECT COUNT(*) FROM maternal_info")
    count = cursor.fetchone()[0]
    print(f"数据库中共有 {count} 条孕产妇记录")
    
    # 显示前3条记录
    cursor.execute("SELECT * FROM maternal_info LIMIT 3")
    records = cursor.fetchall()
    
    # 获取列名
    cursor.execute("PRAGMA table_info(maternal_info)")
    columns = [column[1] for column in cursor.fetchall()]
    
    print("\n示例数据:")
    for i, record in enumerate(records, 1):
        print(f"记录 {i}:")
        for j, value in enumerate(record):
            print(f"  {columns[j]}: {value}")
        print()
    
    conn.close()

if __name__ == "__main__":
    # 初始化数据库
    init_database()
    
    # 导入数据
    import_maternal_data()
    
    # 验证数据
    verify_data()
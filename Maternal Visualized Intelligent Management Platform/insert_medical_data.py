import sqlite3
import json
import random
from datetime import datetime, timedelta

# 数据库路径
db_path = 'medical_system.db'

def generate_medical_data():
    # 生成示例患者医疗数据
    medical_records = []
    
    # 常见疾病类型
    disease_types = ['妊娠期高血压', '妊娠期糖尿病', '前置胎盘', '胎盘早剥', '子痫前期', 
                     '早产风险', '胎儿生长受限', '羊水过多', '羊水过少', '胎位异常']
    
    # 常见症状
    symptoms_pool = [
        '头痛、头晕',
        '恶心、呕吐',
        '血压升高',
        '血糖异常',
        '腹痛',
        '水肿',
        '胎动异常',
        '阴道出血',
        '体重增长过快'
    ]
    
    # 常见诊断
    diagnosis_pool = [
        '轻度妊娠期高血压',
        '中度妊娠期高血压',
        '重度妊娠期高血压',
        '妊娠期糖尿病（A1级）',
        '妊娠期糖尿病（A2级）',
        '完全性前置胎盘',
        '部分性前置胎盘',
        '边缘性前置胎盘',
        '轻度子痫前期',
        '重度子痫前期'
    ]
    
    # 常见治疗方案
    treatment_pool = [
        '定期监测血压，控制饮食',
        '胰岛素治疗，定期监测血糖',
        '卧床休息，密切观察',
        '药物控制血压',
        '住院观察，必要时终止妊娠',
        '期待治疗，定期超声检查',
        '补充营养，促进胎儿生长',
        '定期胎心监护',
        '剖宫产术'
    ]
    
    # 生成50条示例数据
    for i in range(1, 51):
        # 生成随机日期（过去一年内）
        base_date = datetime.now() - timedelta(days=random.randint(0, 365))
        created_at = base_date.strftime('%Y-%m-%d %H:%M:%S')
        updated_at = created_at
        
        # 随机选择数据
        disease_type = random.choice(disease_types)
        # 根据疾病类型关联相关症状
        num_symptoms = random.randint(1, 3)
        symptoms = ', '.join(random.sample(symptoms_pool, num_symptoms))
        diagnosis = random.choice(diagnosis_pool)
        treatment = random.choice(treatment_pool)
        
        # 生成随机生理数据
        systolic_pressure = random.randint(110, 160)
        diastolic_pressure = random.randint(70, 100)
        
        # 创建记录
        record = {
            'name': f'患者{i:03d}',
            'gender': random.choice(['女', '男']),
            'age': random.randint(18, 45),
            'height': round(random.uniform(150, 180), 1),
            'weight': round(random.uniform(45, 85), 1),
            'systolic_pressure': systolic_pressure,
            'diastolic_pressure': diastolic_pressure,
            'disease_type': disease_type,
            'symptoms': symptoms,
            'diagnosis': diagnosis,
            'treatment': treatment,
            'created_at': created_at,
            'updated_at': updated_at
        }
        
        medical_records.append(record)
    
    return medical_records

def insert_medical_data():
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 清空现有数据（可选）
        # cursor.execute("DELETE FROM medical_data")
        # print("已清空medical_data表中的现有数据")
        
        # 生成医疗数据
        medical_records = generate_medical_data()
        
        # 插入数据
        inserted_count = 0
        for record in medical_records:
            cursor.execute(
                "INSERT INTO medical_data (name, gender, age, height, weight, systolic_pressure, diastolic_pressure, "
                "disease_type, symptoms, diagnosis, treatment, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (record['name'], record['gender'], record['age'], record['height'], record['weight'],
                 record['systolic_pressure'], record['diastolic_pressure'], record['disease_type'],
                 record['symptoms'], record['diagnosis'], record['treatment'],
                 record['created_at'], record['updated_at'])
            )
            inserted_count += 1
        
        # 提交事务
        conn.commit()
        print(f"成功插入 {inserted_count} 条医疗数据到medical_data表")
        
        # 验证插入结果
        cursor.execute("SELECT COUNT(*) FROM medical_data")
        total_count = cursor.fetchone()[0]
        print(f"medical_data表当前共有 {total_count} 条记录")
        
        # 显示前5条记录作为预览
        print("\n前5条医疗记录预览：")
        cursor.execute("SELECT id, name, gender, age, disease_type, diagnosis, created_at FROM medical_data ORDER BY id DESC LIMIT 5")
        preview_records = cursor.fetchall()
        
        print("ID | 姓名 | 性别 | 年龄 | 疾病类型 | 诊断 | 创建时间")
        print("---|------|------|------|----------|------|----------")
        for record in preview_records:
            print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]} | {record[5]} | {record[6]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"插入数据时出错: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("开始向medical_data表插入示例医疗数据...")
    success = insert_medical_data()
    
    if success:
        print("\n医疗数据插入完成！")
    else:
        print("\n医疗数据插入失败，请检查错误信息。")

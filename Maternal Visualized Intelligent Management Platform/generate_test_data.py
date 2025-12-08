# 生成真实可信的医疗数据用于测试
import sqlite3
import random
from datetime import datetime, timedelta

# 连接到数据库
conn = sqlite3.connect('medical_system.db')
cursor = conn.cursor()
conn.row_factory = sqlite3.Row

# 定义生成测试数据的函数
def generate_medical_data(num_records):
    """生成医疗数据测试数据"""
    # 姓名列表（中文姓名）
    first_names = ['张', '李', '王', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '胡', '朱', '高']
    last_names = ['伟', '芳', '娜', '秀英', '敏', '静', '强', '磊', '军', '洋', '勇', '艳', '杰', '涛', '明']
    
    # 疾病类型
    disease_types = ['高血压', '糖尿病', '冠心病', '脑卒中', '慢性阻塞性肺疾病', '哮喘', '慢性胃炎', '胆囊炎', '胆结石', '甲状腺疾病']
    
    # 症状列表
    symptoms_list = [
        ['头痛', '头晕', '心悸'],
        ['多饮', '多尿', '多食', '体重减轻'],
        ['胸闷', '胸痛', '气短'],
        ['肢体麻木', '言语不清', '视力模糊'],
        ['咳嗽', '咳痰', '呼吸困难'],
        ['喘息', '气急', '胸闷'],
        ['上腹痛', '恶心', '呕吐'],
        ['右上腹痛', '发热'],
        ['腹痛', '黄疸'],
        ['颈部肿胀', '乏力', '多汗']
    ]
    
    # 诊断列表
    diagnosis_list = [
        ['原发性高血压', '继发性高血压'],
        ['2型糖尿病', '1型糖尿病'],
        ['稳定性心绞痛', '不稳定性心绞痛', '心肌梗死'],
        ['缺血性脑卒中', '出血性脑卒中'],
        ['慢性阻塞性肺疾病急性加重期', '慢性阻塞性肺疾病稳定期'],
        ['支气管哮喘急性发作', '支气管哮喘慢性持续期'],
        ['慢性浅表性胃炎', '慢性萎缩性胃炎'],
        ['急性胆囊炎', '慢性胆囊炎'],
        ['胆囊结石伴胆囊炎', '单纯胆囊结石'],
        ['甲状腺功能亢进', '甲状腺功能减退', '甲状腺结节']
    ]
    
    # 治疗方法列表
    treatment_list = [
        ['降压药物治疗', '生活方式干预'],
        ['降糖药物治疗', '胰岛素治疗', '饮食控制'],
        ['药物治疗', '介入治疗', '手术治疗'],
        ['药物治疗', '康复治疗'],
        ['抗感染治疗', '平喘治疗', '氧疗'],
        ['平喘药物治疗', '抗炎治疗'],
        ['抑酸药物治疗', '保护胃黏膜治疗'],
        ['抗感染治疗', '利胆治疗', '手术治疗'],
        ['利胆治疗', '溶石治疗', '手术治疗'],
        ['药物治疗', '手术治疗', '定期复查']
    ]
    
    records = []
    
    for i in range(num_records):
        # 随机生成姓名
        name = random.choice(first_names) + random.choice(last_names)
        
        # 随机生成年龄（18-85岁）
        age = random.randint(18, 85)
        
        # 随机生成性别
        gender = random.choice(['男', '女'])
        
        # 随机选择疾病类型
        disease_index = random.randint(0, len(disease_types) - 1)
        disease_type = disease_types[disease_index]
        
        # 随机选择症状（从对应疾病的症状列表中）
        symptoms = random.sample(symptoms_list[disease_index], random.randint(1, len(symptoms_list[disease_index])))
        symptoms_str = ','.join(symptoms)
        
        # 随机选择诊断（从对应疾病的诊断列表中）
        diagnosis = random.choice(diagnosis_list[disease_index])
        
        # 随机选择治疗方法（从对应疾病的治疗列表中）
        treatments = random.sample(treatment_list[disease_index], random.randint(1, len(treatment_list[disease_index])))
        treatment_str = ','.join(treatments)
        
        # 随机生成血压（收缩压/舒张压）
        if disease_type == '高血压':
            systolic_pressure = random.randint(140, 180)
            diastolic_pressure = random.randint(90, 110)
        else:
            systolic_pressure = random.randint(110, 139)
            diastolic_pressure = random.randint(70, 89)
        
        # 随机生成体重（kg）
        if gender == '男':
            weight = random.randint(55, 90)
        else:
            weight = random.randint(45, 75)
        
        # 随机生成身高（cm）
        if gender == '男':
            height = random.randint(160, 185)
        else:
            height = random.randint(150, 175)
        
        # 随机生成创建时间（过去3个月内）
        created_at = datetime.now() - timedelta(days=random.randint(0, 90))
        created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
        
        # 随机生成更新时间（创建时间之后，不超过当前时间）
        updated_at = created_at + timedelta(days=random.randint(0, 30))
        updated_at_str = updated_at.strftime('%Y-%m-%d %H:%M:%S')
        
        # 添加到记录列表
        records.append((
            name, gender, age, disease_type, symptoms_str, diagnosis, treatment_str,
            systolic_pressure, diastolic_pressure, weight, height, created_at_str, updated_at_str
        ))
    
    return records

# 生成100条医疗数据记录
medical_data = generate_medical_data(100)

# 插入数据到medical_data表
try:
    # 清空表（可选）
    # cursor.execute("DELETE FROM medical_data")
    
    # 插入新数据
    insert_query = """
    INSERT INTO medical_data (name, gender, age, disease_type, symptoms, diagnosis, treatment,
                            systolic_pressure, diastolic_pressure, weight, height, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.executemany(insert_query, medical_data)
    conn.commit()
    print(f"成功插入{len(medical_data)}条医疗数据记录")
    
    # 验证插入结果
    cursor.execute("SELECT COUNT(*) as total FROM medical_data")
    total = cursor.fetchone()['total']
    print(f"medical_data表中现在共有{total}条记录")
    
except Exception as e:
    print(f"插入数据失败: {e}")
    conn.rollback()

# 关闭连接
conn.close()

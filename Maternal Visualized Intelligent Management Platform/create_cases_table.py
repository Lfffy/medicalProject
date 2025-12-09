import sqlite3
import os

def create_cases_table():
    # 数据库文件路径
    db_path = 'medical_system.db'
    
    # 检查数据库文件是否存在
    db_exists = os.path.exists(db_path)
    print(f"数据库文件 {db_path} {'存在' if db_exists else '不存在'}")
    
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 创建cases表
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,  -- 类型
            gender INTEGER NOT NULL,  -- 性别 (1=男, 2=女)
            age INTEGER NOT NULL,  -- 年龄
            time TEXT NOT NULL,  -- 时间
            description TEXT NOT NULL,  -- 描述
            doctor TEXT NOT NULL,  -- 医生
            hospital TEXT NOT NULL,  -- 医院
            department TEXT NOT NULL,  -- 科室
            details_link TEXT,  -- 详情链接
            height REAL,  -- 身高
            weight REAL,  -- 体重
            duration INTEGER,  -- 患病时长
            allergy_history TEXT,  -- 过敏史
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_sql)
        print("cases表创建成功")
        
        # 创建索引
        create_indexes_sql = [
            'CREATE INDEX IF NOT EXISTS idx_cases_type ON cases(type);',
            'CREATE INDEX IF NOT EXISTS idx_cases_time ON cases(time);',
            'CREATE INDEX IF NOT EXISTS idx_cases_hospital ON cases(hospital);',
            'CREATE INDEX IF NOT EXISTS idx_cases_department ON cases(department);'
        ]
        for sql in create_indexes_sql:
            cursor.execute(sql)
        print("索引创建成功")
        
        # 检查是否已有数据
        cursor.execute('SELECT COUNT(*) FROM cases')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # 插入示例数据
            insert_data_sql = '''
            INSERT INTO cases (type, gender, age, time, description, doctor, hospital, department, details_link, height, weight, duration, allergy_history)
            VALUES
            ('感冒', 1, 35, '2025-06-15 10:30:00', '患者有发热、咳嗽症状，持续2天', '张医生', '北京协和医院', '内科', '#case1', 175.5, 70.2, 2, '无'),
            ('高血压', 2, 55, '2025-06-15 09:15:00', '患者血压偏高，需要药物控制', '李医生', '北京协和医院', '心内科', '#case2', 160.0, 65.5, 365, '无'),
            ('糖尿病', 1, 45, '2025-06-15 14:20:00', '患者血糖控制不佳，调整用药方案', '王医生', '北京协和医院', '内分泌科', '#case3', 172.0, 78.0, 730, '无'),
            ('肺炎', 2, 28, '2025-06-15 16:45:00', '患者咳嗽、胸闷，X光显示肺部炎症', '刘医生', '北京协和医院', '呼吸科', '#case4', 165.0, 58.5, 5, '青霉素'),
            ('骨折', 1, 62, '2025-06-15 11:00:00', '患者右前臂骨折，需要固定治疗', '赵医生', '北京协和医院', '骨科', '#case5', 168.0, 72.0, 1, '无'),
            ('胃炎', 2, 32, '2025-06-15 13:30:00', '患者胃痛、恶心，需要药物治疗', '孙医生', '北京协和医院', '消化科', '#case6', 163.0, 55.0, 14, '无'),
            ('头痛', 1, 25, '2025-06-15 08:45:00', '患者偏头痛，需要止痛药', '周医生', '北京协和医院', '神经内科', '#case7', 178.0, 68.0, 3, '无'),
            ('皮肤病', 2, 40, '2025-06-15 15:10:00', '患者皮肤瘙痒、红肿，可能是过敏', '吴医生', '北京协和医院', '皮肤科', '#case8', 162.0, 59.0, 7, '海鲜'),
            ('眼科疾病', 1, 50, '2025-06-15 10:00:00', '患者视力下降，需要进一步检查', '郑医生', '北京协和医院', '眼科', '#case9', 170.0, 75.0, 30, '无'),
            ('口腔科疾病', 2, 38, '2025-06-15 14:00:00', '患者牙痛，需要根管治疗', '陈医生', '北京协和医院', '口腔科', '#case10', 165.0, 62.0, 2, '无');
            '''
            cursor.executescript(insert_data_sql)
            print("示例数据插入成功")
        else:
            print(f"cases表已存在数据，共 {count} 条记录，跳过数据插入")
        
        # 提交事务
        conn.commit()
        print("操作成功完成")
        
    except Exception as e:
        print(f"操作失败: {e}")
        conn.rollback()
    finally:
        # 关闭连接
        conn.close()

if __name__ == '__main__':
    create_cases_table()

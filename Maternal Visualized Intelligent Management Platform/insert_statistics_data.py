import sqlite3
import json
import datetime

# 数据库路径
db_path = 'medical_system.db'

def insert_statistics_data():
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 清空现有数据
        cursor.execute("DELETE FROM data_statistics")
        print("已清空data_statistics表中的现有数据")
        
        # 获取当前时间用于created_at和updated_at
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 准备示例数据（使用正确的列名）
        statistics_data = [
            # 2025年数据 - 月度统计
            {'stat_type': 'monthly', 'stat_date': '2025-01-31', 'total_patients': 120, 'new_patients': 35,
             'disease_counts': json.dumps({'pregnancy': 45, 'hypertension': 25, 'diabetes': 15, 'other': 35}),
             'department_stats': json.dumps({'obstetrics': 70, 'gynecology': 30, 'internal': 20}),
             'age_distribution': json.dumps({'20-29': 50, '30-39': 45, '40-49': 20, '50+': 5}),
             'gender_distribution': json.dumps({'male': 5, 'female': 115})},
            {'stat_type': 'monthly', 'stat_date': '2025-02-28', 'total_patients': 108, 'new_patients': 30,
             'disease_counts': json.dumps({'pregnancy': 40, 'hypertension': 22, 'diabetes': 12, 'other': 34}),
             'department_stats': json.dumps({'obstetrics': 65, 'gynecology': 28, 'internal': 15}),
             'age_distribution': json.dumps({'20-29': 45, '30-39': 42, '40-49': 18, '50+': 3}),
             'gender_distribution': json.dumps({'male': 4, 'female': 104})},
            {'stat_type': 'monthly', 'stat_date': '2025-03-31', 'total_patients': 135, 'new_patients': 40,
             'disease_counts': json.dumps({'pregnancy': 52, 'hypertension': 28, 'diabetes': 18, 'other': 37}),
             'department_stats': json.dumps({'obstetrics': 80, 'gynecology': 32, 'internal': 23}),
             'age_distribution': json.dumps({'20-29': 55, '30-39': 50, '40-49': 25, '50+': 5}),
             'gender_distribution': json.dumps({'male': 6, 'female': 129})},
            {'stat_type': 'monthly', 'stat_date': '2025-04-30', 'total_patients': 142, 'new_patients': 42,
             'disease_counts': json.dumps({'pregnancy': 55, 'hypertension': 30, 'diabetes': 20, 'other': 37}),
             'department_stats': json.dumps({'obstetrics': 85, 'gynecology': 35, 'internal': 22}),
             'age_distribution': json.dumps({'20-29': 58, '30-39': 52, '40-49': 27, '50+': 5}),
             'gender_distribution': json.dumps({'male': 7, 'female': 135})},
            {'stat_type': 'monthly', 'stat_date': '2025-05-31', 'total_patients': 156, 'new_patients': 48,
             'disease_counts': json.dumps({'pregnancy': 62, 'hypertension': 35, 'diabetes': 22, 'other': 37}),
             'department_stats': json.dumps({'obstetrics': 95, 'gynecology': 38, 'internal': 23}),
             'age_distribution': json.dumps({'20-29': 65, '30-39': 58, '40-49': 28, '50+': 5}),
             'gender_distribution': json.dumps({'male': 8, 'female': 148})},
            {'stat_type': 'monthly', 'stat_date': '2025-06-30', 'total_patients': 149, 'new_patients': 45,
             'disease_counts': json.dumps({'pregnancy': 58, 'hypertension': 32, 'diabetes': 20, 'other': 39}),
             'department_stats': json.dumps({'obstetrics': 90, 'gynecology': 36, 'internal': 23}),
             'age_distribution': json.dumps({'20-29': 60, '30-39': 55, '40-49': 30, '50+': 4}),
             'gender_distribution': json.dumps({'male': 7, 'female': 142})},
            {'stat_type': 'monthly', 'stat_date': '2025-07-31', 'total_patients': 138, 'new_patients': 42,
             'disease_counts': json.dumps({'pregnancy': 55, 'hypertension': 28, 'diabetes': 18, 'other': 37}),
             'department_stats': json.dumps({'obstetrics': 82, 'gynecology': 33, 'internal': 23}),
             'age_distribution': json.dumps({'20-29': 58, '30-39': 50, '40-49': 26, '50+': 4}),
             'gender_distribution': json.dumps({'male': 6, 'female': 132})},
            {'stat_type': 'monthly', 'stat_date': '2025-08-31', 'total_patients': 145, 'new_patients': 44,
             'disease_counts': json.dumps({'pregnancy': 58, 'hypertension': 30, 'diabetes': 19, 'other': 38}),
             'department_stats': json.dumps({'obstetrics': 88, 'gynecology': 35, 'internal': 22}),
             'age_distribution': json.dumps({'20-29': 60, '30-39': 52, '40-49': 29, '50+': 4}),
             'gender_distribution': json.dumps({'male': 7, 'female': 138})},
            {'stat_type': 'monthly', 'stat_date': '2025-09-30', 'total_patients': 152, 'new_patients': 46,
             'disease_counts': json.dumps({'pregnancy': 60, 'hypertension': 33, 'diabetes': 21, 'other': 38}),
             'department_stats': json.dumps({'obstetrics': 92, 'gynecology': 38, 'internal': 22}),
             'age_distribution': json.dumps({'20-29': 63, '30-39': 55, '40-49': 30, '50+': 4}),
             'gender_distribution': json.dumps({'male': 8, 'female': 144})},
            {'stat_type': 'monthly', 'stat_date': '2025-10-31', 'total_patients': 165, 'new_patients': 50,
             'disease_counts': json.dumps({'pregnancy': 68, 'hypertension': 38, 'diabetes': 24, 'other': 35}),
             'department_stats': json.dumps({'obstetrics': 100, 'gynecology': 42, 'internal': 23}),
             'age_distribution': json.dumps({'20-29': 70, '30-39': 62, '40-49': 29, '50+': 4}),
             'gender_distribution': json.dumps({'male': 9, 'female': 156})},
            {'stat_type': 'monthly', 'stat_date': '2025-11-30', 'total_patients': 158, 'new_patients': 48,
             'disease_counts': json.dumps({'pregnancy': 65, 'hypertension': 35, 'diabetes': 22, 'other': 36}),
             'department_stats': json.dumps({'obstetrics': 95, 'gynecology': 40, 'internal': 23}),
             'age_distribution': json.dumps({'20-29': 68, '30-39': 58, '40-49': 28, '50+': 4}),
             'gender_distribution': json.dumps({'male': 8, 'female': 150})},
            {'stat_type': 'monthly', 'stat_date': '2025-12-31', 'total_patients': 147, 'new_patients': 45,
             'disease_counts': json.dumps({'pregnancy': 60, 'hypertension': 32, 'diabetes': 20, 'other': 35}),
             'department_stats': json.dumps({'obstetrics': 88, 'gynecology': 37, 'internal': 22}),
             'age_distribution': json.dumps({'20-29': 62, '30-39': 55, '40-49': 26, '50+': 4}),
             'gender_distribution': json.dumps({'male': 7, 'female': 140})},
            # 2026年最新数据
            {'stat_type': 'monthly', 'stat_date': '2026-01-31', 'total_patients': 132, 'new_patients': 40,
             'disease_counts': json.dumps({'pregnancy': 52, 'hypertension': 28, 'diabetes': 18, 'other': 34}),
             'department_stats': json.dumps({'obstetrics': 80, 'gynecology': 34, 'internal': 18}),
             'age_distribution': json.dumps({'20-29': 55, '30-39': 50, '40-49': 23, '50+': 4}),
             'gender_distribution': json.dumps({'male': 6, 'female': 126})},
            {'stat_type': 'monthly', 'stat_date': '2026-02-29', 'total_patients': 118, 'new_patients': 35,
             'disease_counts': json.dumps({'pregnancy': 46, 'hypertension': 24, 'diabetes': 15, 'other': 33}),
             'department_stats': json.dumps({'obstetrics': 72, 'gynecology': 28, 'internal': 18}),
             'age_distribution': json.dumps({'20-29': 50, '30-39': 45, '40-49': 20, '50+': 3}),
             'gender_distribution': json.dumps({'male': 5, 'female': 113})},
            {'stat_type': 'monthly', 'stat_date': '2026-03-31', 'total_patients': 143, 'new_patients': 45,
             'disease_counts': json.dumps({'pregnancy': 58, 'hypertension': 32, 'diabetes': 21, 'other': 32}),
             'department_stats': json.dumps({'obstetrics': 90, 'gynecology': 35, 'internal': 18}),
             'age_distribution': json.dumps({'20-29': 60, '30-39': 55, '40-49': 25, '50+': 3}),
             'gender_distribution': json.dumps({'male': 7, 'female': 136})},
            # 添加季度统计数据
            {'stat_type': 'quarterly', 'stat_date': '2025-03-31', 'total_patients': 363, 'new_patients': 105,
             'disease_counts': json.dumps({'pregnancy': 137, 'hypertension': 75, 'diabetes': 45, 'other': 106}),
             'department_stats': json.dumps({'obstetrics': 215, 'gynecology': 90, 'internal': 58}),
             'age_distribution': json.dumps({'20-29': 150, '30-39': 137, '40-49': 63, '50+': 13}),
             'gender_distribution': json.dumps({'male': 15, 'female': 348})},
            {'stat_type': 'quarterly', 'stat_date': '2025-06-30', 'total_patients': 447, 'new_patients': 135,
             'disease_counts': json.dumps({'pregnancy': 175, 'hypertension': 97, 'diabetes': 60, 'other': 115}),
             'department_stats': json.dumps({'obstetrics': 270, 'gynecology': 109, 'internal': 68}),
             'age_distribution': json.dumps({'20-29': 183, '30-39': 165, '40-49': 85, '50+': 14}),
             'gender_distribution': json.dumps({'male': 22, 'female': 425})},
        ]
        
        # 插入数据
        inserted_count = 0
        for data in statistics_data:
            cursor.execute(
                "INSERT INTO data_statistics (stat_type, stat_date, total_patients, new_patients, "
                "disease_counts, department_stats, age_distribution, gender_distribution, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (data['stat_type'], data['stat_date'], data['total_patients'], data['new_patients'],
                 data['disease_counts'], data['department_stats'], data['age_distribution'], data['gender_distribution'],
                 now, now)
            )
            inserted_count += 1
        
        # 提交事务
        conn.commit()
        
        print(f"成功向data_statistics表插入{inserted_count}条统计数据")
        
        # 验证数据
        cursor.execute("SELECT COUNT(*) FROM data_statistics")
        count = cursor.fetchone()[0]
        print(f"插入后表中共有{count}条记录")
        
        # 显示前5条记录
        cursor.execute("SELECT * FROM data_statistics LIMIT 5")
        print("\n插入的前5条数据:")
        columns = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            row_dict = {columns[i]: row[i] for i in range(len(columns))}
            # 简化显示JSON字段
            if 'patient_gender_distribution' in row_dict and isinstance(row_dict['patient_gender_distribution'], str):
                row_dict['patient_gender_distribution'] = 'JSON数据'
            if 'risk_factors_analysis' in row_dict and isinstance(row_dict['risk_factors_analysis'], str):
                row_dict['risk_factors_analysis'] = 'JSON数据'
            print(row_dict)
        
        # 关闭连接
        conn.close()
        
    except Exception as e:
        print(f"插入数据时出错: {e}")
        # 回滚事务
        if 'conn' in locals():
            conn.rollback()

if __name__ == "__main__":
    insert_statistics_data()

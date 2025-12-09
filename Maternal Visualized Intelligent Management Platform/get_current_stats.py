import sqlite3

# 数据库路径
db_path = 'medical_system.db'

def get_table_stats():
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取data_statistics表的记录数
        cursor.execute("SELECT COUNT(*) FROM data_statistics")
        data_stats_count = cursor.fetchone()[0]
        
        # 获取data_statistics表的前3条记录（用于数据样本）
        cursor.execute("SELECT id, stat_type, stat_date, total_patients, new_patients, created_at FROM data_statistics LIMIT 3")
        data_stats_samples = cursor.fetchall()
        
        # 获取disease_analysis表的记录数
        cursor.execute("SELECT COUNT(*) FROM disease_analysis")
        disease_analysis_count = cursor.fetchone()[0]
        
        # 获取disease_analysis表的前3条记录（用于数据样本）
        cursor.execute("SELECT id, disease_name, disease_category, incidence_rate, analysis_date, created_at FROM disease_analysis LIMIT 3")
        disease_analysis_samples = cursor.fetchall()
        
        # 打印结果
        print("=== 当前数据库统计信息 ===")
        print(f"data_statistics表记录数: {data_stats_count}")
        print("\ndata_statistics表数据样本（前3条）:")
        print("ID | stat_type | stat_date | total_patients | new_patients | created_at")
        print("---|-----------|-----------|----------------|--------------|-----------")
        for sample in data_stats_samples:
            print(f"{sample[0]} | {sample[1]} | {sample[2]} | {sample[3]} | {sample[4]} | {sample[5]}")
        
        print(f"\ndisease_analysis表记录数: {disease_analysis_count}")
        print("\ndisease_analysis表数据样本（前3条）:")
        print("ID | disease_name | disease_category | incidence_rate | analysis_date | created_at")
        print("---|--------------|------------------|----------------|---------------|-----------")
        for sample in disease_analysis_samples:
            print(f"{sample[0]} | {sample[1]} | {sample[2]} | {sample[3]} | {sample[4]} | {sample[5]}")
        
        conn.close()
        
    except Exception as e:
        print(f"获取统计信息时出错: {e}")

if __name__ == "__main__":
    get_table_stats()

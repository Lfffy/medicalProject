import sqlite3
import json
import os

# 数据库路径
db_path = 'medical_system.db'

def check_database():
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"数据库文件: {db_path}")
        print(f"总表数量: {len(tables)}")
        print("\n表列表:")
        
        table_info = {}
        
        for table in tables:
            table_name = table[0]
            print(f"\n--- 表名: {table_name} ---")
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print(f"列信息:")
            column_info = []
            for col in columns:
                column_info.append({
                    'name': col[1],
                    'type': col[2],
                    'pk': col[5]
                })
                print(f"  {col[1]} ({col[2]}) {'(主键)' if col[5] else ''}")
            
            # 获取记录数量
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"记录数量: {count}")
            
            # 获取前3条记录样本（如果有数据）
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                sample_data = cursor.fetchall()
                print(f"前3条记录样本:")
                
                # 获取列名
                col_names = [desc[0] for desc in cursor.description]
                
                # 打印样本数据
                for row in sample_data:
                    row_dict = {col_names[i]: row[i] for i in range(len(col_names))}
                    # 限制显示长度
                    for key, value in row_dict.items():
                        if isinstance(value, str) and len(value) > 50:
                            row_dict[key] = value[:50] + '...'
                    print(f"  {row_dict}")
            
            # 存储表信息
            table_info[table_name] = {
                'columns': column_info,
                'record_count': count
            }
        
        # 关闭连接
        conn.close()
        
        # 特别检查我们需要插入数据的表
        for table_name in ['data_statistics', 'disease_analysis']:
            if table_name in table_info:
                print(f"\n\n=== 详细检查 {table_name} 表 ===")
                print(f"当前记录数量: {table_info[table_name]['record_count']}")
            else:
                print(f"\n\n=== {table_name} 表不存在 ===")
        
    except Exception as e:
        print(f"检查数据库时出错: {e}")

if __name__ == "__main__":
    check_database()

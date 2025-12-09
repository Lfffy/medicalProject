import sqlite3

# 数据库路径
db_path = 'medical_system.db'

def check_disease_columns():
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取disease_analysis表的所有列信息
        cursor.execute("PRAGMA table_info(disease_analysis)")
        columns = cursor.fetchall()
        
        print("disease_analysis表的列信息：")
        print("-" * 60)
        print(f"{'索引':<5} {'列名':<20} {'数据类型':<15} {'是否为空':<8} {'默认值':<10}")
        print("-" * 60)
        
        for col in columns:
            index = col[0]
            name = col[1]
            col_type = col[2]
            not_null = '否' if col[3] else '是'
            default = col[4] if col[4] is not None else '无'
            
            print(f"{index:<5} {name:<20} {col_type:<15} {not_null:<8} {default:<10}")
        
        # 只获取列名列表
        column_names = [col[1] for col in columns]
        print("\n列名列表：")
        print(column_names)
        
    except Exception as e:
        print(f"查询出错: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_disease_columns()

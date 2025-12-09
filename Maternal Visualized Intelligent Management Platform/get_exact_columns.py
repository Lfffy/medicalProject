import sqlite3

# 数据库路径
db_path = 'medical_system.db'

def get_exact_column_names(table_name):
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"获取表 {table_name} 的精确列名:")
        
        # 使用PRAGMA table_info获取所有列信息
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"列名列表 (按顺序):")
        column_names = []
        for col in columns:
            column_names.append(col[1])
            print(f"  - {col[1]} (类型: {col[2]})")
        
        print(f"\n列名字符串 (用于SQL语句):")
        print(", ".join(column_names))
        
        # 关闭连接
        conn.close()
        
        return column_names
        
    except Exception as e:
        print(f"获取列名时出错: {e}")
        return []

if __name__ == "__main__":
    # 只检查data_statistics表
    get_exact_column_names('data_statistics')

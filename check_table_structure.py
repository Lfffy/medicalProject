import sqlite3

# 数据库路径
db_path = 'medical_system.db'

def check_specific_table(table_name):
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"检查表: {table_name}")
        
        # 获取表结构
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"表 {table_name} 的列信息:")
        for col in columns:
            print(f"  列索引: {col[0]}, 列名: {col[1]}, 数据类型: {col[2]}, 可为空: {col[3]}, 默认值: {col[4]}, 主键: {col[5]}")
        
        # 关闭连接
        conn.close()
        
    except Exception as e:
        print(f"检查表结构时出错: {e}")

if __name__ == "__main__":
    # 检查两个需要操作的表
    check_specific_table('data_statistics')
    print("\n" + "="*50 + "\n")
    check_specific_table('disease_analysis')

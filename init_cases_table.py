import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('medical_system.db')
cursor = conn.cursor()

try:
    # 读取SQL文件
    with open('create_cases_table.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # 执行SQL脚本
    cursor.executescript(sql_script)
    conn.commit()
    print("cases表创建成功，并成功插入示例数据！")
    
    # 验证数据是否插入成功
    cursor.execute("SELECT COUNT(*) FROM cases")
    count = cursor.fetchone()[0]
    print(f"当前cases表中有 {count} 条记录")
    
    # 查看表结构
    cursor.execute("PRAGMA table_info(cases)")
    columns = cursor.fetchall()
    print("\ncases表结构:")
    for col in columns:
        print(f"列名: {col[1]}, 类型: {col[2]}")
    
    # 查看前几条数据
    print("\n示例数据:")
    cursor.execute("SELECT * FROM cases LIMIT 3")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
except Exception as e:
    print(f"执行过程中出现错误: {e}")
    conn.rollback()
    
finally:
    # 关闭连接
    conn.close()
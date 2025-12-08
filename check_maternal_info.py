import sqlite3

# 连接到数据库
conn = sqlite3.connect('medical_system.db')
cursor = conn.cursor()

# 检查maternal_info表结构
print("Maternal_info table structure:")
cursor.execute("PRAGMA table_info(maternal_info)")
structure = cursor.fetchall()
for col in structure:
    print(f"  {col[1]} ({col[2]})")

# 查询前几条数据
print("\nSample data from maternal_info:")
cursor.execute("SELECT * FROM maternal_info LIMIT 2")
data = cursor.fetchall()
if data:
    for row in data:
        print("  Row data:")
        for i, col in enumerate(structure):
            print(f"    {col[1]}: {row[i]}")

conn.close()

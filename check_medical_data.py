import sqlite3

# 连接到数据库
conn = sqlite3.connect('medical_system.db')
cursor = conn.cursor()

# 检查medical_data表结构
print("Medical_data table structure:")
cursor.execute("PRAGMA table_info(medical_data)")
structure = cursor.fetchall()
for col in structure:
    print(f"  {col[1]} ({col[2]})")

# 查询前几条数据
print("\nSample data from medical_data:")
cursor.execute("SELECT * FROM medical_data LIMIT 2")
data = cursor.fetchall()
if data:
    for row in data:
        print("  Row data:")
        for i, col in enumerate(structure):
            print(f"    {col[1]}: {row[i]}")

conn.close()

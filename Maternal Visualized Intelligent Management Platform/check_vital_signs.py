import sqlite3
import os

# 连接数据库
db_path = 'medical_system.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询vital_signs表结构
cursor.execute("PRAGMA table_info(vital_signs)")
columns = cursor.fetchall()

print("vital_signs表结构:")
for col in columns:
    print(f"  {col[1]} {col[2]} {'NOT NULL' if col[3] else ''} {'PRIMARY KEY' if col[5] else ''}")

conn.close()
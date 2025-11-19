import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'medical_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查medical_records表结构
cursor.execute('PRAGMA table_info(medical_records);')
columns = cursor.fetchall()
print('medical_records columns:')
for col in columns:
    print(f'  {col}')

conn.close()
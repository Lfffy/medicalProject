import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'medical_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 获取所有表
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print('Tables:', [table[0] for table in tables])

# 检查medical_records表结构
if 'medical_records' in [table[0] for table in tables]:
    cursor.execute('PRAGMA table_info(medical_records);')
    columns = cursor.fetchall()
    print('medical_records columns:')
    for col in columns:
        print(f'  {col}')

# 检查vital_signs表结构
if 'vital_signs' in [table[0] for table in tables]:
    cursor.execute('PRAGMA table_info(vital_signs);')
    columns = cursor.fetchall()
    print('vital_signs columns:')
    for col in columns:
        print(f'  {col}')

# 检查maternal_info表结构
if 'maternal_info' in [table[0] for table in tables]:
    cursor.execute('PRAGMA table_info(maternal_info);')
    columns = cursor.fetchall()
    print('maternal_info columns:')
    for col in columns:
        print(f'  {col}')

conn.close()
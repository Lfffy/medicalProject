import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'medical_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查patients表结构
cursor.execute('PRAGMA table_info(patients);')
columns = cursor.fetchall()
print('patients columns:')
for col in columns:
    print(f'  {col}')

conn.close()
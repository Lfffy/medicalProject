import re

# 读取monitoring_api.py文件
with open('monitoring_api.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有包含patient_id的行
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'patient_id' in line:
        print(f"第{i}行: {line.strip()}")
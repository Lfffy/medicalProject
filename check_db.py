#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库检查脚本
"""

import sqlite3
import os

def check_database():
    """检查数据库文件和表的情况"""
    db_path = 'medical_system.db'
    
    print("=== 数据库检查报告 ===")
    
    # 检查数据库文件是否存在
    if os.path.exists(db_path):
        print(f"1. 数据库文件: {db_path} - 存在")
        print(f"   文件大小: {os.path.getsize(db_path)} 字节")
        
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"2. 表数量: {len(tables)}")
        print("3. 表列表:")
        
        for table in tables:
            table_name = table[0]
            
            # 获取表的记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            # 获取表的结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_count = len(columns)
            
            print(f"   - {table_name}: {count} 条记录, {column_count} 个字段")
            
            # 显示前3条记录（如果有数据）
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                records = cursor.fetchall()
                print(f"     前3条记录示例:")
                for record in records:
                    print(f"     {record}")
                print()
        
        conn.close()
        print("数据库检查完成")
    else:
        print(f"1. 数据库文件: {db_path} - 不存在")
        print("   可能需要运行数据库初始化脚本")

if __name__ == "__main__":
    check_database()

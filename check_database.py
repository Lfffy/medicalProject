#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中的数据
"""

import sqlite3
import json

def check_database():
    try:
        # 连接数据库
        conn = sqlite3.connect('maternal_health.db')
        cursor = conn.cursor()
        
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("数据库表:", [table[0] for table in tables])
        
        # 检查maternal_info表
        if any('maternal_info' in table for table in tables):
            cursor.execute("SELECT COUNT(*) FROM maternal_info")
            count = cursor.fetchone()
            print(f"maternal_info表记录数: {count[0]}")
            
            if count[0] > 0:
                cursor.execute("SELECT * FROM maternal_info LIMIT 3")
                rows = cursor.fetchall()
                print("示例数据:")
                
                # 获取列名
                cursor.execute("PRAGMA table_info(maternal_info)")
                columns = [column[1] for column in cursor.fetchall()]
                print("列名:", columns)
                
                # 打印数据
                for row in rows:
                    print(row)
            else:
                print("maternal_info表为空")
        else:
            print("maternal_info表不存在")
        
        # 检查是否有其他数据表
        for table in tables:
            table_name = table[0]
            if table_name != 'maternal_info':
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()
                print(f"{table_name}表记录数: {count[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"检查数据库时出错: {e}")

if __name__ == "__main__":
    check_database()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查nutrition_advice表是否存在
"""

import sqlite3

def check_nutrition_table():
    """检查nutrition_advice表是否存在并创建"""
    try:
        # 连接数据库
        conn = sqlite3.connect('maternal_health.db')
        cursor = conn.cursor()
        
        # 检查nutrition_advice表是否存在
        cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='nutrition_advice'
        """)
        
        result = cursor.fetchone()
        
        if result:
            print("✓ nutrition_advice表已存在")
            
            # 获取表结构
            cursor.execute("PRAGMA table_info(nutrition_advice)")
            columns = cursor.fetchall()
            print("表结构:")
            for column in columns:
                print(f"  {column[1]} ({column[2]})")
            
            # 检查是否有数据
            cursor.execute("SELECT COUNT(*) FROM nutrition_advice")
            count = cursor.fetchone()[0]
            print(f"表中有 {count} 条记录")
            
        else:
            print("✗ nutrition_advice表不存在，正在创建...")
            
            # 创建nutrition_advice表
            cursor.execute('''
            CREATE TABLE nutrition_advice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                patient_name TEXT,
                gestational_stage TEXT,
                advice_type TEXT,
                advice_content TEXT,
                priority TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            print("✓ nutrition_advice表创建成功")
            
            # 插入一些示例数据
            sample_data = [
                (1, '张三', '早期妊娠', '饮食建议', '建议增加蛋白质摄入', 'medium', 'pending'),
                (2, '李四', '中期妊娠', '营养补充', '建议补充叶酸和铁剂', 'high', 'completed'),
                (3, '王五', '晚期妊娠', '体重管理', '控制碳水化合物摄入，适量运动', 'medium', 'pending')
            ]
            
            cursor.executemany('''
            INSERT INTO nutrition_advice (patient_id, patient_name, gestational_stage, advice_type, advice_content, priority, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
            
            conn.commit()
            print(f"✓ 已插入 {len(sample_data)} 条示例数据")
        
    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    check_nutrition_table()

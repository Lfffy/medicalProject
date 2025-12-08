import sqlite3
import os

def querys(sql):
    """执行SQL查询"""
    try:
        # 连接到SQLite数据库（与app.py保持一致）
        db_path = os.path.join(os.path.dirname(__file__), '..', 'medical_system.db')
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(sql)
        
        if sql.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = '执行成功'
        
        conn.close()
        return result
        
    except Exception as e:
        print(f"SQL查询失败: {e}")
        return None
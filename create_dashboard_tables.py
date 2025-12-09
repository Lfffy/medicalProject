import sqlite3
import os

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'medical_data.db')

def create_dashboard_tables():
    """创建仪表盘相关的表"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 创建仪表板总览数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dashboard_overview (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_patients INTEGER DEFAULT 0, -- 总患者数
                today_new_cases INTEGER DEFAULT 0, -- 今日新增病例
                total_maternal INTEGER DEFAULT 0, -- 总孕产妇数
                alert_count INTEGER DEFAULT 0, -- 预警数量
                trends_json TEXT, -- JSON格式存储趋势数据
                statistics_json TEXT, -- JSON格式存储统计数据
                recent_alerts_json TEXT, -- JSON格式存储最近预警
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # 创建仪表板医疗数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dashboard_medical (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total INTEGER DEFAULT 0, -- 总记录数
                today INTEGER DEFAULT 0, -- 今日记录数
                disease_distribution_json TEXT, -- JSON格式存储疾病分布
                department_distribution_json TEXT, -- JSON格式存储科室分布
                monthly_trend_json TEXT, -- JSON格式存储月度趋势
                department_details_json TEXT, -- JSON格式存储科室详情
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("仪表盘表创建成功！")
        return True
    except Exception as e:
        print(f"创建仪表盘表失败: {e}")
        return False

if __name__ == '__main__':
    create_dashboard_tables()

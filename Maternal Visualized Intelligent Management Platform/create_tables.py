import sqlite3
import os

# 数据库文件路径
db_path = r"c:\Users\14978\Desktop\Maternal-Visualized-Intelligent-Management-Platform\Maternal Visualized Intelligent Management Platform\medical_system.db"

# 检查数据库文件是否存在
if not os.path.exists(db_path):
    print("数据库文件不存在，正在创建...")
    # 创建空数据库文件
    open(db_path, 'w').close()

# 连接到SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL语句
create_tables_sql = '''
-- 创建仪表板总览数据表
CREATE TABLE IF NOT EXISTS dashboard_overview (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_patients INTEGER DEFAULT 0, -- 总患者数
    today_new_cases INTEGER DEFAULT 0, -- 今日新增病例
    total_maternal INTEGER DEFAULT 0, -- 总孕产妇数
    alert_count INTEGER DEFAULT 0, -- 预警数量
    trends_json TEXT, -- JSON格式存储趋势数据
    statistics_json TEXT, -- JSON格式存储统计数据
    recent_alerts_json TEXT, -- JSON格式存储最近预警
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建仪表板医疗数据表
CREATE TABLE IF NOT EXISTS dashboard_medical (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total INTEGER DEFAULT 0, -- 总记录数
    today INTEGER DEFAULT 0, -- 今日记录数
    disease_distribution_json TEXT, -- JSON格式存储疾病分布
    department_distribution_json TEXT, -- JSON格式存储科室分布
    monthly_trend_json TEXT, -- JSON格式存储月度趋势
    department_details_json TEXT, -- JSON格式存储科室详情
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建仪表板孕产数据表
CREATE TABLE IF NOT EXISTS dashboard_maternal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total INTEGER DEFAULT 0, -- 总孕产妇数
    today INTEGER DEFAULT 0, -- 今日产检数
    pregnancy_distribution_json TEXT, -- JSON格式存储孕期分布
    risk_distribution_json TEXT, -- JSON格式存储风险分布
    maternal_details_json TEXT, -- JSON格式存储孕产妇详情
    reminders_json TEXT, -- JSON格式存储提醒
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建仪表板对比分析数据表
CREATE TABLE IF NOT EXISTS dashboard_comparison (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comparison_type TEXT NOT NULL, -- 对比类型：year-over-year(同比)/month-over-month(环比)
    comparison_date DATE NOT NULL, -- 对比日期
    previous_value REAL DEFAULT 0, -- 上期值
    current_value REAL DEFAULT 0, -- 本期值
    change_rate REAL DEFAULT 0, -- 变化率
    comparison_details_json TEXT, -- JSON格式存储详细对比数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_dashboard_overview_updated_at ON dashboard_overview(updated_at);
CREATE INDEX IF NOT EXISTS idx_dashboard_medical_updated_at ON dashboard_medical(updated_at);
CREATE INDEX IF NOT EXISTS idx_dashboard_maternal_updated_at ON dashboard_maternal(updated_at);
CREATE INDEX IF NOT EXISTS idx_dashboard_comparison_date ON dashboard_comparison(comparison_date);
CREATE INDEX IF NOT EXISTS idx_dashboard_comparison_type ON dashboard_comparison(comparison_type);
'''

# 执行SQL语句
print("开始创建表...")
try:
    cursor.executescript(create_tables_sql)
    conn.commit()
    print("表创建成功!")
    
    # 列出所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\n数据库中所有表:")
    for table in tables:
        print(f"- {table[0]}")
        
    # 列出刚创建的仪表板相关表
    print("\n新创建的仪表板相关表:")
    dashboard_tables = ['dashboard_overview', 'dashboard_medical', 'dashboard_maternal', 'dashboard_comparison']
    for table in dashboard_tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        if cursor.fetchone():
            print(f"✓ {table}")
        else:
            print(f"✗ {table}")
            
except Exception as e:
    print(f"表创建失败: {e}")
    conn.rollback()

# 关闭数据库连接
cursor.close()
conn.close()
print("\n数据库连接已关闭。")

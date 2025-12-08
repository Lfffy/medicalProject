import sqlite3
import json
import datetime

# 数据库文件路径
db_path = r"c:\Users\14978\Desktop\Maternal-Visualized-Intelligent-Management-Platform\Maternal Visualized Intelligent Management Platform\medical_system.db"

# 连接到SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("开始插入仪表板数据...")

# 1. 插入仪表板总览数据
try:
    # 准备趋势数据
    trends = {
        "daily_cases": [
            {"date": "2025-01-10", "value": 120},
            {"date": "2025-01-11", "value": 135},
            {"date": "2025-01-12", "value": 110},
            {"date": "2025-01-13", "value": 145},
            {"date": "2025-01-14", "value": 150},
            {"date": "2025-01-15", "value": 165},
            {"date": "2025-01-16", "value": 170}
        ]
    }
    
    # 准备统计数据
    statistics = {
        "risk_level_distribution": [
            {"name": "低风险", "value": 1200},
            {"name": "中风险", "value": 580},
            {"name": "高风险", "value": 156}
        ]
    }
    
    # 准备最近预警
    recent_alerts = [
        {"id": 1, "patient_name": "张女士", "risk_level": "高风险", "alert_time": "2025-01-16T14:30:00"},
        {"id": 2, "patient_name": "李女士", "risk_level": "中风险", "alert_time": "2025-01-16T13:45:00"},
        {"id": 3, "patient_name": "王女士", "risk_level": "高风险", "alert_time": "2025-01-16T12:20:00"}
    ]
    
    # 插入数据
    cursor.execute('''
        INSERT INTO dashboard_overview (total_patients, today_new_cases, total_maternal, alert_count, 
                                      trends_json, statistics_json, recent_alerts_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (12000, 170, 2500, 8, 
          json.dumps(trends), json.dumps(statistics), json.dumps(recent_alerts)))
    
    print("✓ 仪表板总览数据插入成功")
    
except Exception as e:
    print(f"✗ 仪表板总览数据插入失败: {e}")
    conn.rollback()

# 2. 插入仪表板医疗数据
try:
    # 准备疾病分布数据
    disease_distribution = [
        {"name": "高血压", "value": 350},
        {"name": "糖尿病", "value": 280},
        {"name": "冠心病", "value": 200},
        {"name": "慢性胃炎", "value": 180},
        {"name": "其他", "value": 450}
    ]
    
    # 准备科室分布数据
    department_distribution = [
        {"name": "内科", "value": 650},
        {"name": "外科", "value": 420},
        {"name": "妇产科", "value": 380},
        {"name": "儿科", "value": 250},
        {"name": "急诊科", "value": 180}
    ]
    
    # 准备月度趋势数据
    monthly_trend = [
        {"month": "2024-08", "value": 1200},
        {"month": "2024-09", "value": 1250},
        {"month": "2024-10", "value": 1300},
        {"month": "2024-11", "value": 1350},
        {"month": "2024-12", "value": 1400},
        {"month": "2025-01", "value": 1450}
    ]
    
    # 准备科室详情数据
    department_details = [
        {"name": "内科", "total": 650, "today": 45, "disease_types": 12, "doctors": 32},
        {"name": "外科", "total": 420, "today": 32, "disease_types": 8, "doctors": 25},
        {"name": "妇产科", "total": 380, "today": 28, "disease_types": 6, "doctors": 20},
        {"name": "儿科", "total": 250, "today": 18, "disease_types": 10, "doctors": 15},
        {"name": "急诊科", "total": 180, "today": 12, "disease_types": 15, "doctors": 10}
    ]
    
    # 插入数据
    cursor.execute('''
        INSERT INTO dashboard_medical (total, today, disease_distribution_json, department_distribution_json, 
                                     monthly_trend_json, department_details_json)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (2500, 170, 
          json.dumps(disease_distribution), json.dumps(department_distribution), 
          json.dumps(monthly_trend), json.dumps(department_details)))
    
    print("✓ 仪表板医疗数据插入成功")
    
except Exception as e:
    print(f"✗ 仪表板医疗数据插入失败: {e}")
    conn.rollback()

# 3. 插入仪表板孕产数据
try:
    # 准备孕期分布数据
    pregnancy_distribution = [
        {"name": "早期", "value": 850},
        {"name": "中期", "value": 950},
        {"name": "晚期", "value": 700}
    ]
    
    # 准备风险分布数据
    risk_distribution = [
        {"name": "低风险", "value": 1800},
        {"name": "中风险", "value": 500},
        {"name": "高风险", "value": 200}
    ]
    
    # 准备孕产妇详情数据
    maternal_details = [
        {"id": 1, "name": "张女士", "age": 32, "gestational_week": 28, "risk_level": "低风险"},
        {"id": 2, "name": "李女士", "age": 28, "gestational_week": 16, "risk_level": "低风险"},
        {"id": 3, "name": "王女士", "age": 35, "gestational_week": 32, "risk_level": "中风险"},
        {"id": 4, "name": "刘女士", "age": 40, "gestational_week": 22, "risk_level": "高风险"},
        {"id": 5, "name": "陈女士", "age": 30, "gestational_week": 12, "risk_level": "低风险"}
    ]
    
    # 准备产检提醒数据
    reminders = [
        {"id": 1, "patient_name": "张女士", "reminder_date": "2025-01-18", "content": "常规产检"},
        {"id": 2, "patient_name": "李女士", "reminder_date": "2025-01-20", "content": "唐筛检查"},
        {"id": 3, "patient_name": "王女士", "reminder_date": "2025-01-22", "content": "四维彩超"}
    ]
    
    # 插入数据
    cursor.execute('''
        INSERT INTO dashboard_maternal (total, today, pregnancy_distribution_json, risk_distribution_json, 
                                      maternal_details_json, reminders_json)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (2500, 35, 
          json.dumps(pregnancy_distribution), json.dumps(risk_distribution), 
          json.dumps(maternal_details), json.dumps(reminders)))
    
    print("✓ 仪表板孕产数据插入成功")
    
except Exception as e:
    print(f"✗ 仪表板孕产数据插入失败: {e}")
    conn.rollback()

# 4. 插入仪表板对比分析数据
try:
    # 准备同比数据
    yoy_details = {
        "indicators": [
            {"name": "总患者数", "previous": 10500, "current": 12000, "change_rate": 14.29},
            {"name": "今日新增", "previous": 150, "current": 170, "change_rate": 13.33},
            {"name": "总孕产妇数", "previous": 2200, "current": 2500, "change_rate": 13.64},
            {"name": "预警数量", "previous": 6, "current": 8, "change_rate": 33.33}
        ]
    }
    
    # 准备环比数据
    mom_details = {
        "indicators": [
            {"name": "总患者数", "previous": 11800, "current": 12000, "change_rate": 1.69},
            {"name": "今日新增", "previous": 160, "current": 170, "change_rate": 6.25},
            {"name": "总孕产妇数", "previous": 2450, "current": 2500, "change_rate": 2.04},
            {"name": "预警数量", "previous": 7, "current": 8, "change_rate": 14.29}
        ]
    }
    
    # 插入同比数据
    cursor.execute('''
        INSERT INTO dashboard_comparison (comparison_type, comparison_date, previous_value, current_value, change_rate, comparison_details_json)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('year-over-year', '2025-01-15', 10500, 12000, 14.29, json.dumps(yoy_details)))
    
    # 插入环比数据
    cursor.execute('''
        INSERT INTO dashboard_comparison (comparison_type, comparison_date, previous_value, current_value, change_rate, comparison_details_json)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('month-over-month', '2025-01-15', 11800, 12000, 1.69, json.dumps(mom_details)))
    
    print("✓ 仪表板对比分析数据插入成功")
    
except Exception as e:
    print(f"✗ 仪表板对比分析数据插入失败: {e}")
    conn.rollback()

# 提交事务
conn.commit()

# 验证数据插入结果
try:
    print("\n验证数据插入结果:")
    
    # 验证总览表
    cursor.execute("SELECT COUNT(*) FROM dashboard_overview")
    print(f"仪表板总览表记录数: {cursor.fetchone()[0]}")
    
    # 验证医疗表
    cursor.execute("SELECT COUNT(*) FROM dashboard_medical")
    print(f"仪表板医疗表记录数: {cursor.fetchone()[0]}")
    
    # 验证孕产表
    cursor.execute("SELECT COUNT(*) FROM dashboard_maternal")
    print(f"仪表板孕产表记录数: {cursor.fetchone()[0]}")
    
    # 验证对比表
    cursor.execute("SELECT COUNT(*) FROM dashboard_comparison")
    print(f"仪表板对比表记录数: {cursor.fetchone()[0]}")
    
except Exception as e:
    print(f"数据验证失败: {e}")

# 关闭数据库连接
cursor.close()
conn.close()

print("\n仪表板数据插入完成！")

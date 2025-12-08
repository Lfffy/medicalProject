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
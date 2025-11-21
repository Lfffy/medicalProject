-- 孕产妇健康管理系统数据表创建脚本

-- 注意：此脚本不会删除或修改原始的cases表，确保兼容性

-- 检查并创建孕产妇信息表
CREATE TABLE IF NOT EXISTS maternal_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '孕妇姓名',
    age INT NOT NULL COMMENT '年龄',
    gender VARCHAR(10) DEFAULT '女' COMMENT '性别',
    department VARCHAR(100) NOT NULL COMMENT '科室',
    hospital VARCHAR(255) NOT NULL COMMENT '医院',
    diagnosis_date DATE NOT NULL COMMENT '产检日期',
    pregnancy_status VARCHAR(100) NOT NULL COMMENT '孕期状态',
    gestational_week INT COMMENT '孕周',
    expected_date DATE COMMENT '预产期',
    pregnancy_type VARCHAR(50) COMMENT '妊娠类型',
    risk_level VARCHAR(50) COMMENT '风险等级',
    weight FLOAT COMMENT '体重',
    blood_pressure VARCHAR(50) COMMENT '血压',
    hemoglobin FLOAT COMMENT '血红蛋白',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入测试数据（如果表为空）
INSERT INTO maternal_info (name, age, gender, department, hospital, diagnosis_date, pregnancy_status, gestational_week, expected_date, pregnancy_type, risk_level, weight, blood_pressure, hemoglobin)
SELECT '张女士', 28, '女', '产科', '妇幼保健院', '2025-01-15', '正常妊娠', 20, '2025-06-20', '单胎', '低风险', 65.5, '120/80', 125
WHERE NOT EXISTS (SELECT 1 FROM maternal_info LIMIT 1);

-- 插入更多测试数据
INSERT INTO maternal_info (name, age, gender, department, hospital, diagnosis_date, pregnancy_status, gestational_week, expected_date, pregnancy_type, risk_level, weight, blood_pressure, hemoglobin)
VALUES 
('王女士', 25, '女', '产科', '妇幼保健院', '2025-01-20', '正常妊娠', 12, '2025-07-10', '单胎', '低风险', 58.5, '118/78', 132),
('刘女士', 35, '女', '产科', '省人民医院', '2025-01-22', '高危妊娠', 32, '2025-04-25', '双胎', '高风险', 78.0, '135/85', 115),
('陈女士', 29, '女', '产科', '市妇幼保健院', '2025-01-25', '正常妊娠', 16, '2025-06-30', '单胎', '中风险', 62.0, '125/82', 128)
ON DUPLICATE KEY UPDATE id=id;

-- 删除旧视图（如果存在）
DROP VIEW IF EXISTS cases_maternal_view;

-- 创建兼容视图，确保与原系统查询兼容
CREATE VIEW cases_maternal_view AS
SELECT 
    id,
    pregnancy_status AS type,  -- 确保字段名与原cases表匹配
    gender,
    age,
    DATE_FORMAT(diagnosis_date, '%m.%d') AS time,  -- 格式化为与原表相同的日期格式
    CONCAT('孕期第', gestational_week, '周，', risk_level) AS content,
    '待补充' AS docName,  -- 补充原表需要的字段
    hospital AS docHospital,
    department,
    CONCAT('/maternal/', id) AS detailUrl,
    NULL AS height,  -- 原表字段
    weight,  -- 原表字段
    NULL AS illDuration,  -- 原表字段
    NULL AS allergy  -- 原表字段
FROM maternal_info;
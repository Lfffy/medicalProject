-- 医院管理系统数据库表结构
-- 创建时间：2024-01-01
-- 说明：包含医院、科室、医生、排班等管理功能

-- 1. 医院信息表
CREATE TABLE IF NOT EXISTS hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '医院名称',
    level ENUM('primary', 'secondary', 'tertiary') DEFAULT 'secondary' COMMENT '医院等级：primary-一级, secondary-二级, tertiary-三级',
    address VARCHAR(500) COMMENT '医院地址',
    phone VARCHAR(50) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '邮箱',
    website VARCHAR(200) COMMENT '官网地址',
    description TEXT COMMENT '医院简介',
    bed_count INT DEFAULT 0 COMMENT '床位数',
    established_date DATE COMMENT '建院日期',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态：active-启用, inactive-禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_hospital_name (name),
    INDEX idx_hospital_level (level),
    INDEX idx_hospital_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='医院信息表';

-- 2. 科室信息表
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '科室名称',
    hospital_id INT NOT NULL COMMENT '所属医院ID',
    parent_id INT DEFAULT NULL COMMENT '上级科室ID',
    department_code VARCHAR(50) COMMENT '科室编码',
    description TEXT COMMENT '科室简介',
    bed_count INT DEFAULT 0 COMMENT '床位数',
    floor_number VARCHAR(20) COMMENT '楼层位置',
    phone VARCHAR(50) COMMENT '科室电话',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态：active-启用, inactive-禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES departments(id) ON DELETE SET NULL,
    INDEX idx_department_name (name),
    INDEX idx_department_hospital (hospital_id),
    INDEX idx_department_parent (parent_id),
    INDEX idx_department_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='科室信息表';

-- 3. 医生信息表
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '医生姓名',
    title VARCHAR(100) COMMENT '职称',
    gender ENUM('male', 'female') COMMENT '性别：male-男, female-女',
    age INT COMMENT '年龄',
    phone VARCHAR(50) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '邮箱',
    hospital_id INT NOT NULL COMMENT '所属医院ID',
    department_id INT NOT NULL COMMENT '所属科室ID',
    specialization TEXT COMMENT '专业专长',
    bio TEXT COMMENT '个人简介',
    education_background VARCHAR(200) COMMENT '教育背景',
    work_experience TEXT COMMENT '工作经历',
    license_number VARCHAR(100) COMMENT '执业证书编号',
    consultation_fee DECIMAL(10,2) DEFAULT 0.00 COMMENT '挂号费',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态：active-启用, inactive-禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
    INDEX idx_doctor_name (name),
    INDEX idx_doctor_hospital (hospital_id),
    INDEX idx_doctor_department (department_id),
    INDEX idx_doctor_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='医生信息表';

-- 4. 排班信息表
CREATE TABLE IF NOT EXISTS schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL COMMENT '医生ID',
    schedule_date DATE NOT NULL COMMENT '排班日期',
    start_time TIME NOT NULL COMMENT '开始时间',
    end_time TIME NOT NULL COMMENT '结束时间',
    shift_type ENUM('morning', 'afternoon', 'evening', 'full_day') NOT NULL COMMENT '班次类型：morning-上午班, afternoon-下午班, evening-夜班, full_day-全天班',
    max_patients INT DEFAULT 20 COMMENT '最大接诊数',
    current_patients INT DEFAULT 0 COMMENT '当前已预约数',
    status ENUM('active', 'inactive', 'cancelled') DEFAULT 'active' COMMENT '状态：active-启用, inactive-禁用, cancelled-取消',
    notes TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    INDEX idx_schedule_doctor (doctor_id),
    INDEX idx_schedule_date (schedule_date),
    INDEX idx_schedule_shift (shift_type),
    INDEX idx_schedule_status (status),
    UNIQUE KEY uk_doctor_date_time (doctor_id, schedule_date, start_time, end_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='排班信息表';

-- 5. 患者预约表（可选扩展）
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL COMMENT '患者姓名',
    patient_phone VARCHAR(50) NOT NULL COMMENT '患者电话',
    patient_age INT COMMENT '患者年龄',
    patient_gender ENUM('male', 'female') COMMENT '患者性别',
    schedule_id INT NOT NULL COMMENT '排班ID',
    appointment_date DATETIME NOT NULL COMMENT '预约时间',
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '状态：pending-待确认, confirmed-已确认, completed-已完成, cancelled-已取消',
    symptoms TEXT COMMENT '症状描述',
    notes TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
    INDEX idx_appointment_schedule (schedule_id),
    INDEX idx_appointment_date (appointment_date),
    INDEX idx_appointment_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='患者预约表';

-- 插入基础数据

-- 插入示例医院数据
INSERT INTO hospitals (name, level, address, phone, email, description, bed_count, status) VALUES
('北京协和医院', 'tertiary', '北京市东城区东单帅府园1号', '010-69156114', 'info@pumch.cn', '北京协和医院是集医疗、教学、科研于一体的现代化综合三级甲等医院', 2000, 'active'),
('北京同仁医院', 'tertiary', '北京市东城区东交民巷1号', '010-58266699', 'info@trhos.com', '北京同仁医院是一所以眼科、耳鼻咽喉科为重点的三级甲等综合医院', 1500, 'active'),
('北京朝阳医院', 'tertiary', '北京市朝阳区工体南路8号', '010-85231000', 'info@cyh.com.cn', '北京朝阳医院是集医疗、教学、科研、预防为一体的三级甲等医院', 1800, 'active'),
('北京市海淀医院', 'secondary', '北京市海淀区中关村大街29号', '010-82619999', 'info@bjhdkyy.com', '北京市海淀医院是集医疗、教学、科研、预防为一体的二级甲等综合医院', 800, 'active'),
('北京市西城区展览路医院', 'primary', '北京市西城区展览路24号', '010-68354466', 'info@zllyy.com', '北京市西城区展览路医院是一级甲等综合医院', 300, 'active');

-- 插入示例科室数据
INSERT INTO departments (name, hospital_id, description, bed_count, phone, status) VALUES
-- 北京协和医院科室
('内科', 1, '内科系统疾病诊治', 200, '010-69156001', 'active'),
('外科', 1, '外科系统疾病诊治', 180, '010-69156002', 'active'),
('妇产科', 1, '妇产科疾病诊治及孕产妇保健', 120, '010-69156003', 'active'),
('儿科', 1, '儿科疾病诊治', 100, '010-69156004', 'active'),
('眼科', 1, '眼科疾病诊治', 80, '010-69156005', 'active'),
('耳鼻喉科', 1, '耳鼻喉科疾病诊治', 60, '010-69156006', 'active'),
('急诊科', 1, '急诊急救', 50, '010-69156007', 'active'),
('麻醉科', 1, '手术麻醉', 40, '010-69156008', 'active'),

-- 北京同仁医院科室
('眼科', 2, '眼科疾病诊治', 150, '010-58266601', 'active'),
('耳鼻咽喉科', 2, '耳鼻咽喉科疾病诊治', 120, '010-58266602', 'active'),
('内科', 2, '内科系统疾病诊治', 100, '010-58266603', 'active'),
('外科', 2, '外科系统疾病诊治', 90, '010-58266604', 'active'),
('妇产科', 2, '妇产科疾病诊治', 80, '010-58266605', 'active'),

-- 北京朝阳医院科室
('内科', 3, '内科系统疾病诊治', 150, '010-85231001', 'active'),
('外科', 3, '外科系统疾病诊治', 140, '010-85231002', 'active'),
('妇产科', 3, '妇产科疾病诊治', 100, '010-85231003', 'active'),
('儿科', 3, '儿科疾病诊治', 80, '010-85231004', 'active'),
('急诊科', 3, '急诊急救', 60, '010-85231005', 'active'),

-- 北京市海淀医院科室
('内科', 4, '内科系统疾病诊治', 100, '010-82619901', 'active'),
('外科', 4, '外科系统疾病诊治', 80, '010-82619902', 'active'),
('妇产科', 4, '妇产科疾病诊治', 60, '010-82619903', 'active'),
('儿科', 4, '儿科疾病诊治', 50, '010-82619904', 'active'),

-- 北京市西城区展览路医院科室
('内科', 5, '内科系统疾病诊治', 50, '010-68354401', 'active'),
('外科', 5, '外科系统疾病诊治', 40, '010-68354402', 'active'),
('妇产科', 5, '妇产科疾病诊治', 30, '010-68354403', 'active'),
('儿科', 5, '儿科疾病诊治', 25, '010-68354404', 'active');

-- 插入示例医生数据
INSERT INTO doctors (name, title, gender, age, phone, email, hospital_id, department_id, specialization, bio, consultation_fee, status) VALUES
-- 北京协和医院医生
('张明华', '主任医师', 'male', 45, '13800138001', 'zhangmh@pumch.cn', 1, 1, '心血管疾病、高血压、冠心病', '从事内科临床工作20年，擅长心血管疾病的诊治', 100.00, 'active'),
('李晓红', '副主任医师', 'female', 38, '13800138002', 'lixh@pumch.cn', 1, 1, '消化系统疾病、胃肠疾病', '从事内科临床工作15年，擅长消化系统疾病诊治', 80.00, 'active'),
('王建国', '主任医师', 'male', 50, '13800138003', 'wangjg@pumch.cn', 1, 2, '普外科手术、微创手术', '从事外科临床工作25年，擅长普外科手术', 120.00, 'active'),
('赵丽娜', '副主任医师', 'female', 42, '13800138004', 'zhaoln@pumch.cn', 1, 3, '产科、高危妊娠管理', '从事妇产科临床工作18年，擅长高危妊娠管理', 90.00, 'active'),
('刘小军', '主治医师', 'male', 35, '13800138005', 'liuxj@pumch.cn', 1, 4, '小儿呼吸系统疾病、儿童保健', '从事儿科临床工作10年，擅长小儿呼吸系统疾病诊治', 60.00, 'active'),

-- 北京同仁医院医生
('陈光明', '主任医师', 'male', 48, '13800138006', 'chengm@trhos.com', 2, 5, '白内障、青光眼、眼底病', '从事眼科临床工作22年，擅长白内障手术', 150.00, 'active'),
('孙美华', '副主任医师', 'female', 40, '13800138007', 'sunmh@trhos.com', 2, 6, '鼻窦炎、中耳炎、喉部疾病', '从事耳鼻喉科临床工作16年，擅长鼻内镜手术', 100.00, 'active'),

-- 北京朝阳医院医生
('黄志强', '主任医师', 'male', 52, '13800138008', 'huangzq@cyh.com.cn', 3, 1, '呼吸系统疾病、肺部感染', '从事内科临床工作28年，擅长呼吸系统疾病诊治', 110.00, 'active'),
('周晓芳', '副主任医师', 'female', 39, '13800138009', 'zhouxf@cyh.com.cn', 3, 3, '产前检查、正常分娩、产后康复', '从事妇产科临床工作14年，擅长产前保健', 85.00, 'active'),

-- 北京市海淀医院医生
('吴文涛', '主治医师', 'male', 36, '13800138010', 'wuwt@bjhdkyy.com', 4, 1, '内分泌疾病、糖尿病', '从事内科临床工作11年，擅长内分泌疾病诊治', 70.00, 'active'),
('杨丽娟', '住院医师', 'female', 28, '13800138011', 'yanglj@bjhdkyy.com', 4, 3, '妇科炎症、宫颈疾病', '从事妇产科临床工作5年，擅长妇科常见病诊治', 50.00, 'active'),

-- 北京市西城区展览路医院医生
('马志明', '主治医师', 'male', 37, '13800138012', 'mazm@zllyy.com', 5, 1, '老年病、慢性病管理', '从事内科临床工作12年，擅长老年病诊治', 65.00, 'active'),
('林小红', '住院医师', 'female', 26, '13800138013', 'linxh@zllyy.com', 5, 3, '计划生育、妇科检查', '从事妇产科临床工作3年，擅长计划生育服务', 45.00, 'active');

-- 插入示例排班数据（未来一周）
INSERT INTO schedules (doctor_id, schedule_date, start_time, end_time, shift_type, max_patients, current_patients, status, notes) VALUES
-- 张明华医生的排班
(1, CURDATE(), '08:00:00', '12:00:00', 'morning', 20, 8, 'active', '上午门诊'),
(1, CURDATE(), '14:00:00', '17:00:00', 'afternoon', 15, 5, 'active', '下午门诊'),
(1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', '12:00:00', 'morning', 20, 12, 'active', '上午门诊'),
(1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '14:00:00', '17:00:00', 'afternoon', 15, 7, 'active', '下午门诊'),

-- 李晓红医生的排班
(2, CURDATE(), '08:00:00', '12:00:00', 'morning', 20, 10, 'active', '上午门诊'),
(2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '08:00:00', '12:00:00', 'morning', 20, 6, 'active', '上午门诊'),
(2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '14:00:00', '17:00:00', 'afternoon', 15, 4, 'active', '下午门诊'),

-- 王建国医生的排班
(3, CURDATE(), '09:00:00', '12:00:00', 'morning', 10, 3, 'active', '上午手术'),
(3, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '09:00:00', '12:00:00', 'morning', 10, 2, 'active', '上午手术'),

-- 赵丽娜医生的排班
(4, CURDATE(), '08:00:00', '12:00:00', 'morning', 15, 8, 'active', '产科门诊'),
(4, CURDATE(), '14:00:00', '17:00:00', 'afternoon', 12, 4, 'active', '产科门诊'),
(4, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', '12:00:00', 'morning', 15, 11, 'active', '产科门诊'),

-- 刘小军医生的排班
(5, CURDATE(), '08:00:00', '12:00:00', 'morning', 25, 15, 'active', '儿科门诊'),
(5, CURDATE(), '14:00:00', '17:00:00', 'afternoon', 20, 8, 'active', '儿科门诊'),
(5, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '08:00:00', '12:00:00', 'morning', 25, 18, 'active', '儿科门诊'),

-- 陈光明医生的排班
(6, CURDATE(), '08:00:00', '12:00:00', 'morning', 15, 12, 'active', '眼科门诊'),
(6, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', '12:00:00', 'morning', 15, 9, 'active', '眼科门诊'),

-- 孙美华医生的排班
(7, CURDATE(), '14:00:00', '17:00:00', 'afternoon', 12, 5, 'active', '耳鼻喉科门诊'),
(7, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '14:00:00', '17:00:00', 'afternoon', 12, 3, 'active', '耳鼻喉科门诊'),

-- 黄志强医生的排班
(8, CURDATE(), '08:00:00', '12:00:00', 'morning', 20, 14, 'active', '呼吸科门诊'),
(8, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '08:00:00', '12:00:00', 'morning', 20, 7, 'active', '呼吸科门诊'),

-- 周晓芳医生的排班
(9, CURDATE(), '08:00:00', '12:00:00', 'morning', 18, 10, 'active', '产科门诊'),
(9, CURDATE(), '14:00:00', '17:00:00', 'afternoon', 15, 6, 'active', '产科门诊'),
(9, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', '12:00:00', 'morning', 18, 13, 'active', '产科门诊'),

-- 吴文涛医生的排班
(10, CURDATE(), '14:00:00', '17:00:00', 'afternoon', 16, 7, 'active', '内科门诊'),
(10, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '14:00:00', '17:00:00', 'afternoon', 16, 4, 'active', '内科门诊'),

-- 杨丽娟医生的排班
(11, CURDATE(), '08:00:00', '12:00:00', 'morning', 20, 12, 'active', '妇科门诊'),
(11, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '08:00:00', '12:00:00', 'morning', 20, 8, 'active', '妇科门诊'),

-- 马志明医生的排班
(12, CURDATE(), '08:00:00', '12:00:00', 'morning', 18, 9, 'active', '内科门诊'),
(12, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', '12:00:00', 'morning', 18, 11, 'active', '内科门诊'),

-- 林小红医生的排班
(13, CURDATE(), '14:00:00', '17:00:00', 'afternoon', 15, 6, 'active', '妇科门诊'),
(13, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '14:00:00', '17:00:00', 'afternoon', 15, 3, 'active', '妇科门诊');

-- 创建视图：医生排班详情视图
CREATE VIEW v_doctor_schedule_details AS
SELECT 
    s.id as schedule_id,
    s.schedule_date,
    s.start_time,
    s.end_time,
    s.shift_type,
    s.max_patients,
    s.current_patients,
    s.status as schedule_status,
    s.notes,
    d.id as doctor_id,
    d.name as doctor_name,
    d.title as doctor_title,
    d.gender as doctor_gender,
    d.age as doctor_age,
    d.phone as doctor_phone,
    d.email as doctor_email,
    d.specialization,
    d.consultation_fee,
    h.id as hospital_id,
    h.name as hospital_name,
    h.level as hospital_level,
    h.address as hospital_address,
    h.phone as hospital_phone,
    dep.id as department_id,
    dep.name as department_name,
    dep.phone as department_phone
FROM schedules s
JOIN doctors d ON s.doctor_id = d.id
JOIN hospitals h ON d.hospital_id = h.id
JOIN departments dep ON d.department_id = dep.id
WHERE s.status IN ('active', 'cancelled')
ORDER BY s.schedule_date, s.start_time;

-- 创建视图：医院统计视图
CREATE VIEW v_hospital_statistics AS
SELECT 
    h.id as hospital_id,
    h.name as hospital_name,
    h.level as hospital_level,
    h.bed_count as hospital_beds,
    COUNT(DISTINCT dep.id) as department_count,
    COUNT(DISTINCT d.id) as doctor_count,
    COUNT(DISTINCT s.id) as schedule_count,
    SUM(CASE WHEN d.status = 'active' THEN 1 ELSE 0 END) as active_doctors,
    SUM(CASE WHEN dep.status = 'active' THEN 1 ELSE 0 END) as active_departments,
    SUM(CASE WHEN s.status = 'active' THEN 1 ELSE 0 END) as active_schedules,
    h.status as hospital_status
FROM hospitals h
LEFT JOIN departments dep ON h.id = dep.hospital_id
LEFT JOIN doctors d ON dep.id = d.department_id
LEFT JOIN schedules s ON d.id = s.doctor_id AND s.schedule_date >= CURDATE()
GROUP BY h.id, h.name, h.level, h.bed_count, h.status;

-- 创建视图：科室统计视图
CREATE VIEW v_department_statistics AS
SELECT 
    dep.id as department_id,
    dep.name as department_name,
    h.id as hospital_id,
    h.name as hospital_name,
    h.level as hospital_level,
    dep.bed_count as department_beds,
    COUNT(DISTINCT d.id) as doctor_count,
    COUNT(DISTINCT s.id) as schedule_count,
    SUM(CASE WHEN d.status = 'active' THEN 1 ELSE 0 END) as active_doctors,
    SUM(CASE WHEN s.status = 'active' THEN 1 ELSE 0 END) as active_schedules,
    dep.status as department_status
FROM departments dep
JOIN hospitals h ON dep.hospital_id = h.id
LEFT JOIN doctors d ON dep.id = d.department_id
LEFT JOIN schedules s ON d.id = s.doctor_id AND s.schedule_date >= CURDATE()
GROUP BY dep.id, dep.name, h.id, h.name, h.level, dep.bed_count, dep.status;
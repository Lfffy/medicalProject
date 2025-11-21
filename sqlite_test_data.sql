-- 医疗疾病数据分析大屏可视化系统 - SQLite测试数据
-- 创建时间：2025-06-18
-- 说明：符合业务规则的测试数据，覆盖各类业务场景

-- =============================================
-- 1. 医院机构测试数据
-- =============================================

-- 插入医院测试数据
INSERT INTO hospitals (hospital_name, hospital_code, hospital_level, hospital_type, province_code, province_name, city_code, city_name, district_code, district_name, address, contact_phone, emergency_phone, email, website, description, bed_count, doctor_count, nurse_count, established_date, status) VALUES
('北京协和医院', 'BJXH001', '三级甲等', '综合医院', '11', '北京市', '1101', '北京市', '110101', '东城区', '北京市东城区东单帅府园1号', '010-69156114', '010-69155564', 'info@pumch.cn', 'www.pumch.cn', '北京协和医院是集医疗、教学、科研于一体的现代化综合三级甲等医院', 2000, 1500, 2000, '1921-01-01', 1),
('上海瑞金医院', 'SHRJ001', '三级甲等', '综合医院', '31', '上海市', '3101', '上海市', '310104', '徐汇区', '上海市瑞金二路197号', '021-64370045', '021-64370045', 'info@rjh.com.cn', 'www.rjh.com.cn', '上海交通大学医学院附属瑞金医院是一所三级甲等大型综合性教学医院', 1800, 1200, 1800, '1907-01-01', 1),
('广州中山大学附属第一医院', 'GZZS001', '三级甲等', '综合医院', '44', '广东省', '4401', '广州市', '440104', '越秀区', '广州市越秀区中山二路58号', '020-87755766', '020-87755766', 'zs-hospital@163.com', 'www.zs-hospital.sh.cn', '中山大学附属第一医院是国家重点大学中山大学附属医院中规模最大、综合实力最强的附属医院', 2200, 1800, 2500, '1910-01-01', 1),
('深圳市人民医院', 'SZRM001', '三级甲等', '综合医院', '44', '广东省', '4403', '深圳市', '440304', '福田区', '深圳市东门北路1017号', '0755-25533018', '0755-25533018', 'szph@szhospital.com', 'www.szhospital.com', '深圳市人民医院（深圳市第一人民医院）位于广东省深圳市，是一家集医疗、教学、科研、预防、保健为一体的现代化综合性医院', 1500, 1000, 1500, '1946-01-01', 1),
('成都市华西医院', 'CDHX001', '三级甲等', '综合医院', '51', '四川省', '5101', '成都市', '510104', '武侯区', '成都市武侯区国学巷37号', '028-85422114', '028-85422114', 'info@wcums.edu.cn', 'www.cd120.com', '四川大学华西医院是中国西部疑难危急重症诊疗的国家级中心', 2500, 2000, 3000, '1892-01-01', 1),
('杭州市第一人民医院', 'HZDY001', '三级甲等', '综合医院', '33', '浙江省', '3301', '杭州市', '330102', '上城区', '杭州市上城区浣纱路261号', '0571-56006600', '0571-56006600', 'hz-hospital@163.com', 'www.hz-hospital.com', '杭州市第一人民医院是杭州地区规模最大的综合性三级甲等医院', 1200, 800, 1200, '1923-01-01', 1);

-- 插入科室测试数据
INSERT INTO departments (hospital_id, department_name, department_code, parent_id, department_type, category, description, location, contact_phone, doctor_count, bed_count, sort_order, status) VALUES
(1, '内科', 'NK001', 0, '临床科室', '内科', '内科系统疾病诊疗', '门诊楼3楼', '010-69156120', 50, 200, 1, 1),
(1, '外科', 'WK001', 0, '临床科室', '外科', '外科系统疾病诊疗', '门诊楼4楼', '010-69156121', 60, 300, 2, 1),
(1, '妇产科', 'FCK001', 0, '临床科室', '妇产科', '妇产科疾病诊疗', '门诊楼5楼', '010-69156122', 30, 150, 3, 1),
(1, '儿科', 'EK001', 0, '临床科室', '儿科', '儿科疾病诊疗', '门诊楼2楼', '010-69156123', 25, 100, 4, 1),
(1, '心血管内科', 'XNZ001', 1, '临床科室', '内科', '心血管疾病诊疗', '门诊楼3楼东区', '010-69156124', 20, 80, 5, 1),
(1, '神经内科', 'SNK001', 1, '临床科室', '内科', '神经系统疾病诊疗', '门诊楼3楼西区', '010-69156125', 18, 70, 6, 1),
(1, '消化内科', 'XHK001', 1, '临床科室', '内科', '消化系统疾病诊疗', '门诊楼3楼南区', '010-69156126', 15, 60, 7, 1),
(1, '呼吸内科', 'HNK001', 1, '临床科室', '内科', '呼吸系统疾病诊疗', '门诊楼3楼北区', '010-69156127', 16, 65, 8, 1),
(2, '内科', 'NK001', 0, '临床科室', '内科', '内科系统疾病诊疗', '门诊楼2楼', '021-64370046', 40, 180, 1, 1),
(2, '外科', 'WK001', 0, '临床科室', '外科', '外科系统疾病诊疗', '门诊楼3楼', '021-64370047', 45, 250, 2, 1),
(2, '妇产科', 'FCK001', 0, '临床科室', '妇产科', '妇产科疾病诊疗', '门诊楼4楼', '021-64370048', 25, 120, 3, 1),
(2, '儿科', 'EK001', 0, '临床科室', '儿科', '儿科疾病诊疗', '门诊楼1楼', '021-64370049', 20, 80, 4, 1);

-- =============================================
-- 2. 用户测试数据
-- =============================================

-- 插入用户测试数据
INSERT INTO users (username, email, password_hash, salt, real_name, phone, role_id, hospital_id, department_id, status, created_at) VALUES
('admin', 'admin@hospital.com', 'hashed_password_1', 'salt_1', '系统管理员', '13800138001', 1, NULL, NULL, 1, '2025-06-18 10:00:00'),
('doctor1', 'doctor1@hospital.com', 'hashed_password_2', 'salt_2', '张医生', '13800138002', 3, 1, 5, 1, '2025-06-18 10:00:00'),
('doctor2', 'doctor2@hospital.com', 'hashed_password_3', 'salt_3', '李医生', '13800138003', 3, 1, 6, 1, '2025-06-18 10:00:00'),
('nurse1', 'nurse1@hospital.com', 'hashed_password_4', 'salt_4', '王护士', '13800138004', 4, 1, 1, 1, '2025-06-18 10:00:00'),
('user1', 'user1@hospital.com', 'hashed_password_5', 'salt_5', '普通用户', '13800138005', 5, NULL, NULL, 1, '2025-06-18 10:00:00'),
('doctor3', 'doctor3@hospital.com', 'hashed_password_6', 'salt_6', '陈医生', '13800138006', 3, 2, 1, 1, '2025-06-18 10:00:00'),
('doctor4', 'doctor4@hospital.com', 'hashed_password_7', 'salt_7', '刘医生', '13800138007', 3, 2, 3, 1, '2025-06-18 10:00:00'),
('nurse2', 'nurse2@hospital.com', 'hashed_password_8', 'salt_8', '赵护士', '13800138008', 4, 2, 1, 1, '2025-06-18 10:00:00');

-- =============================================
-- 3. 患者测试数据
-- =============================================

-- 插入患者测试数据
INSERT INTO patients (patient_no, name, gender, birth_date, age, id_card, phone, email, address, province_code, city_code, district_code, blood_type, rh_factor, marital_status, occupation, education, created_at) VALUES
('P20250001', '张三', 1, '1985-03-15', 39, '110101198503150001', '13901000001', 'zhangsan@email.com', '北京市朝阳区建国路88号', '11', '1101', '110105', 'A', 1, 2, '软件工程师', '本科', CURRENT_TIMESTAMP),
('P20250002', '李四', 2, '1990-07-22', 34, '110101199007220002', '13901000002', 'lisi@email.com', '北京市海淀区中关村大街1号', '11', '1101', '110108', 'B', 1, 1, '教师', '硕士', CURRENT_TIMESTAMP),
('P20250003', '王五', 1, '1978-11-30', 46, '110101197811300003', '13901000003', 'wangwu@email.com', '北京市西城区金融街25号', '11', '1101', '110102', 'O', 1, 2, '金融分析师', '本科', CURRENT_TIMESTAMP),
('P20250004', '赵六', 2, '1995-05-18', 29, '310101199505180004', '13901000004', 'zhaoliu@email.com', '上海市浦东新区陆家嘴环路1000号', '31', '3101', '310115', 'AB', 1, 1, '市场专员', '大专', CURRENT_TIMESTAMP),
('P20250005', '钱七', 1, '1982-09-08', 42, '440101198209080005', '13901000005', 'qianqi@email.com', '广东省广州市天河区珠江新城', '44', '4401', '440106', 'A', 1, 2, '企业经理', '本科', CURRENT_TIMESTAMP),
('P20250006', '孙八', 2, '1988-12-25', 36, '440101198812250006', '13901000006', 'sunba@email.com', '广东省深圳市南山区科技园', '44', '4403', '440305', 'B', 1, 1, '产品经理', '硕士', CURRENT_TIMESTAMP),
('P20250007', '周九', 1, '1975-04-12', 49, '510101197504120007', '13901000007', 'zhoujiu@email.com', '四川省成都市锦江区春熙路', '51', '5101', '510104', 'O', 1, 2, '公务员', '本科', CURRENT_TIMESTAMP),
('P20250008', '吴十', 2, '1992-08-06', 32, '330101199208060008', '13901000008', 'wushi@email.com', '浙江省杭州市西湖区文三路', '33', '3301', '330106', 'A', 1, 2, '设计师', '本科', CURRENT_TIMESTAMP),
('P20250009', '郑十一', 1, '1980-02-28', 44, '110101198002280009', '13901000009', 'zhengsy@email.com', '北京市东城区王府井大街', '11', '1101', '110101', 'B', 1, 2, '律师', '硕士', CURRENT_TIMESTAMP),
('P20250010', '王小芳', 2, '1993-06-15', 31, '110101199306150010', '13901000010', 'wangxf@email.com', '北京市朝阳区三里屯', '11', '1101', '110105', 'O', 1, 1, '护士', '大专', CURRENT_TIMESTAMP);

-- =============================================
-- 4. 医疗记录测试数据
-- =============================================

-- 插入医疗记录测试数据
INSERT INTO medical_records (record_no, patient_id, hospital_id, department_id, doctor_id, visit_type, visit_date, chief_complaint, present_illness, diagnosis, disease_code, disease_category, disease_severity, treatment_plan, status, created_by, created_at) VALUES
('MR20250001', 1, 1, 5, 2, 1, '2025-01-15', '胸闷、气短3天', '患者3天前无明显诱因出现胸闷、气短，活动后加重，伴有心悸', '冠心病', 'I25.1', '心血管疾病', 2, '抗血小板聚集、调脂稳定斑块、扩冠治疗', 1, 2, CURRENT_TIMESTAMP),
('MR20250002', 2, 1, 6, 3, 1, '2025-01-16', '头痛、头晕1周', '患者1周前开始出现头痛、头晕，呈持续性钝痛', '高血压病', 'I10', '心血管疾病', 1, '降压治疗、生活方式干预', 1, 3, CURRENT_TIMESTAMP),
('MR20250003', 3, 1, 7, 2, 2, '2025-01-17', '腹痛、恶心半天', '患者半天前进食后出现腹痛、恶心，呕吐2次', '急性胃炎', 'K29.1', '消化系统疾病', 2, '抑酸、保护胃黏膜、补液治疗', 1, 2, CURRENT_TIMESTAMP),
('MR20250004', 4, 2, 3, 7, 1, '2025-01-18', '停经45天，恶心呕吐1周', '患者停经45天，近1周出现恶心、呕吐等早孕反应', '早孕', 'O09.9', '妇产科疾病', 1, '定期产检、补充叶酸', 1, 7, CURRENT_TIMESTAMP),
('MR20250005', 5, 1, 8, 2, 3, '2025-01-10', '发热、咳嗽3天', '患者3天前出现发热，体温最高38.5℃，伴有咳嗽、咳痰', '肺炎', 'J18.9', '呼吸系统疾病', 2, '抗感染、对症支持治疗', 1, 2, CURRENT_TIMESTAMP),
('MR20250006', 6, 2, 1, 6, 1, '2025-01-19', '上腹部不适1个月', '患者1个月来反复出现上腹部不适，餐后加重', '慢性胃炎', 'K29.5', '消化系统疾病', 1, '抑酸、保护胃黏膜、饮食调理', 1, 6, CURRENT_TIMESTAMP),
('MR20250007', 7, 1, 5, 2, 2, '2025-01-20', '胸痛2小时', '患者2小时前突发胸痛，呈压榨性，向左肩放射', '急性心肌梗死', 'I21.9', '心血管疾病', 3, '急诊PCI、抗血小板、抗凝治疗', 1, 2, CURRENT_TIMESTAMP),
('MR20250008', 8, 1, 4, 2, 1, '2025-01-21', '发热、皮疹2天', '患者2天前出现发热，体温38.0℃，伴有全身皮疹', '麻疹', 'B05.9', '传染病', 2, '隔离、对症支持治疗', 1, 2, CURRENT_TIMESTAMP),
('MR20250009', 9, 1, 6, 3, 1, '2025-01-22', '记忆力下降3个月', '患者3个月来逐渐出现记忆力下降，注意力不集中', '阿尔茨海默病', 'F03', '神经系统疾病', 2, '认知功能训练、药物治疗', 1, 3, CURRENT_TIMESTAMP),
('MR20250010', 10, 2, 3, 7, 1, '2025-01-23', '孕28周，胎动减少1天', '患者孕28周，自觉胎动减少1天', '胎儿窘迫', 'O68.9', '妇产科疾病', 3, '吸氧、左侧卧位、密切监护', 1, 7, CURRENT_TIMESTAMP);

-- =============================================
-- 5. 生命体征测试数据
-- =============================================

-- 插入生命体征测试数据
INSERT INTO vital_signs (record_id, measure_time, systolic_pressure, diastolic_pressure, heart_rate, body_temperature, respiratory_rate, blood_oxygen, weight, height, bmi, created_by, created_at) VALUES
(1, '2025-01-15 09:00:00', 140, 90, 88, 36.5, 18, 98, 75.5, 175.0, 24.7, 2, CURRENT_TIMESTAMP),
(1, '2025-01-15 14:00:00', 135, 85, 85, 36.3, 17, 99, 75.5, 175.0, 24.7, 2, CURRENT_TIMESTAMP),
(2, '2025-01-16 10:00:00', 150, 95, 92, 36.8, 19, 97, 62.3, 165.0, 22.9, 3, CURRENT_TIMESTAMP),
(3, '2025-01-17 11:00:00', 120, 80, 78, 37.2, 20, 98, 68.8, 172.0, 23.2, 2, CURRENT_TIMESTAMP),
(4, '2025-01-18 09:30:00', 110, 70, 75, 36.2, 16, 99, 55.2, 162.0, 21.0, 7, CURRENT_TIMESTAMP),
(5, '2025-01-10 08:00:00', 125, 82, 95, 38.5, 22, 96, 70.2, 170.0, 24.3, 2, CURRENT_TIMESTAMP),
(5, '2025-01-11 08:00:00', 122, 80, 88, 37.8, 20, 97, 70.2, 170.0, 24.3, 2, CURRENT_TIMESTAMP),
(6, '2025-01-19 10:30:00', 118, 78, 72, 36.6, 17, 98, 65.5, 168.0, 23.2, 6, CURRENT_TIMESTAMP),
(7, '2025-01-20 15:00:00', 160, 100, 110, 36.0, 24, 92, 80.3, 178.0, 25.3, 2, CURRENT_TIMESTAMP),
(8, '2025-01-21 14:30:00', 115, 75, 90, 38.0, 21, 98, 48.5, 158.0, 19.4, 2, CURRENT_TIMESTAMP);

-- =============================================
-- 6. 孕产妇信息测试数据
-- =============================================

-- 插入孕产妇信息测试数据
INSERT INTO maternal_info (patient_id, last_menstrual_period, expected_date_delivery, current_gestational_week, parity, gravidity, abortion_count, live_birth_count, risk_level, risk_factors, prenatal_care_count, last_prenatal_date, expected_delivery_hospital, created_at) VALUES
(4, '2024-10-04', '2025-07-11', 15, 0, 1, 0, 0, '低风险', '无特殊风险因素', 3, '2025-01-18', '北京协和医院', CURRENT_TIMESTAMP),
(10, '2024-07-30', '2025-05-07', 28, 1, 2, 0, 1, '中风险', '高龄产妇、瘢痕子宫', 8, '2025-01-23', '上海瑞金医院', CURRENT_TIMESTAMP);

-- 插入产检记录测试数据
INSERT INTO prenatal_examinations (maternal_id, examination_date, gestational_week, hospital_id, department_id, doctor_id, weight, blood_pressure_systolic, blood_pressure_diastolic, fundal_height, abdominal_circumference, fetal_heart_rate, fetal_position, edema, proteinuria, hemoglobin, diagnosis, next_visit_date, risk_assessment, created_by, created_at) VALUES
(1, '2025-01-18', 15, 2, 3, 7, 55.2, 110, 70, NULL, NULL, 145, 'LOA', 0, 0, 115, '早孕，胎儿发育正常', '2025-02-15', '低风险', 7, CURRENT_TIMESTAMP),
(2, '2025-01-23', 28, 2, 3, 7, 62.8, 125, 82, 26.5, 92.3, 142, 'ROA', 1, 1, 108, '孕28周，胎儿发育良好，轻度水肿', '2025-02-20', '中风险', 7, CURRENT_TIMESTAMP);

-- =============================================
-- 7. 操作日志测试数据
-- =============================================

-- 插入操作日志测试数据
INSERT INTO operation_logs (user_id, username, operation_type, operation_module, operation_description, request_method, request_url, ip_address, execution_time, status, created_at) VALUES
(1, 'admin', 'LOGIN', 'AUTH', '用户登录系统', 'POST', '/api/login', '192.168.1.100', 120, 1, CURRENT_TIMESTAMP),
(2, 'doctor1', 'CREATE', 'MEDICAL_RECORD', '创建医疗记录', 'POST', '/api/medical_records', '192.168.1.101', 350, 1, CURRENT_TIMESTAMP),
(3, 'doctor2', 'UPDATE', 'PATIENT', '更新患者信息', 'PUT', '/api/patients/1', '192.168.1.102', 200, 1, CURRENT_TIMESTAMP),
(4, 'nurse1', 'CREATE', 'VITAL_SIGNS', '记录生命体征', 'POST', '/api/vital_signs', '192.168.1.103', 180, 1, CURRENT_TIMESTAMP),
(5, 'user1', 'VIEW', 'DASHBOARD', '查看数据大屏', 'GET', '/api/dashboard', '192.168.1.104', 500, 1, CURRENT_TIMESTAMP);

-- =============================================
-- 8. 疾病统计测试数据
-- =============================================

-- 插入疾病统计测试数据
INSERT INTO disease_statistics (disease_code, disease_name, disease_category, statistic_date, statistic_type, total_cases, new_cases, cured_cases, death_cases, male_cases, female_cases, age_group_0_18, age_group_19_35, age_group_36_50, age_group_51_65, age_group_65_plus, hospital_id, created_at) VALUES
('I25.1', '冠心病', '心血管疾病', '2025-01-15', 'daily', 120, 5, 8, 1, 70, 50, 2, 15, 45, 40, 18, 1, CURRENT_TIMESTAMP),
('I10', '高血压病', '心血管疾病', '2025-01-15', 'daily', 200, 8, 12, 0, 110, 90, 5, 25, 60, 70, 40, 1, CURRENT_TIMESTAMP),
('K29.1', '急性胃炎', '消化系统疾病', '2025-01-15', 'daily', 80, 3, 6, 0, 45, 35, 8, 20, 30, 15, 7, 1, CURRENT_TIMESTAMP),
('J18.9', '肺炎', '呼吸系统疾病', '2025-01-15', 'daily', 150, 6, 10, 1, 80, 70, 25, 35, 40, 35, 15, 1, CURRENT_TIMESTAMP),
('O09.9', '早孕', '妇产科疾病', '2025-01-15', 'daily', 60, 4, 0, 0, 0, 60, 0, 35, 20, 5, 0, 2, CURRENT_TIMESTAMP);

-- =============================================
-- 9. 孕产妇统计测试数据
-- =============================================

-- 插入孕产妇统计测试数据
INSERT INTO maternal_statistics (statistic_date, statistic_type, total_pregnant, new_pregnant, delivered_count, natural_delivery, cesarean_delivery, premature_birth, low_birth_weight, stillbirth, maternal_death, low_risk_count, medium_risk_count, high_risk_count, prenatal_care_rate, hospital_id, created_at) VALUES
('2025-01-15', 'daily', 450, 8, 12, 8, 4, 2, 1, 0, 0, 320, 110, 20, 95.5, 1, CURRENT_TIMESTAMP),
('2025-01-15', 'daily', 380, 6, 10, 7, 3, 1, 1, 0, 0, 280, 85, 15, 94.2, 2, CURRENT_TIMESTAMP);

-- =============================================
-- 10. 系统配置更新测试数据
-- =============================================

-- 更新系统配置
UPDATE system_configs SET config_value = '医疗疾病数据分析大屏可视化系统v3.0' WHERE config_key = 'system_name';
UPDATE system_configs SET config_value = '2025-06-18' WHERE config_key = 'system_version';
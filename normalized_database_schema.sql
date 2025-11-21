-- 医疗疾病数据分析大屏可视化系统 - 规范化数据库表结构设计
-- 创建时间：2025-06-18
-- 版本：v3.0 - 规范化版本
-- 说明：本设计遵循数据库规范化原则，确保数据完整性和查询效率

-- =============================================
-- 数据库配置和基础设置
-- =============================================

-- 设置字符集和排序规则
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================
-- 1. 用户权限管理模块
-- =============================================

-- 用户表
CREATE TABLE `users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `email` VARCHAR(100) NOT NULL COMMENT '邮箱',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希值',
  `salt` VARCHAR(32) NOT NULL COMMENT '密码盐值',
  `real_name` VARCHAR(50) DEFAULT NULL COMMENT '真实姓名',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号码',
  `avatar` VARCHAR(500) DEFAULT NULL COMMENT '头像URL',
  `role_id` BIGINT UNSIGNED NOT NULL DEFAULT 3 COMMENT '角色ID：1-超级管理员，2-管理员，3-普通用户',
  `hospital_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '所属医院ID',
  `department_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '所属科室ID',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `last_login_time` DATETIME DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` VARCHAR(45) DEFAULT NULL COMMENT '最后登录IP',
  `login_count` INT UNSIGNED DEFAULT 0 COMMENT '登录次数',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  KEY `idx_role_id` (`role_id`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_department_id` (`department_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 角色表
CREATE TABLE `roles` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` VARCHAR(50) NOT NULL COMMENT '角色名称',
  `role_code` VARCHAR(50) NOT NULL COMMENT '角色编码',
  `description` VARCHAR(255) DEFAULT NULL COMMENT '角色描述',
  `level` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '角色级别：数字越小权限越高',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_code` (`role_code`),
  KEY `idx_level` (`level`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- 权限表
CREATE TABLE `permissions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '权限ID',
  `permission_name` VARCHAR(100) NOT NULL COMMENT '权限名称',
  `permission_code` VARCHAR(100) NOT NULL COMMENT '权限编码',
  `resource_type` VARCHAR(50) DEFAULT NULL COMMENT '资源类型：menu-菜单，button-按钮，api-接口',
  `resource_path` VARCHAR(255) DEFAULT NULL COMMENT '资源路径',
  `request_method` VARCHAR(10) DEFAULT NULL COMMENT '请求方法：GET,POST,PUT,DELETE',
  `parent_id` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '父权限ID',
  `sort_order` INT UNSIGNED DEFAULT 0 COMMENT '排序',
  `level` TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '权限层级',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_permission_code` (`permission_code`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_resource_type` (`resource_type`),
  KEY `idx_level` (`level`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- 角色权限关联表
CREATE TABLE `role_permissions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_id` BIGINT UNSIGNED NOT NULL COMMENT '角色ID',
  `permission_id` BIGINT UNSIGNED NOT NULL COMMENT '权限ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_permission` (`role_id`, `permission_id`),
  KEY `idx_role_id` (`role_id`),
  KEY `idx_permission_id` (`permission_id`),
  CONSTRAINT `fk_rp_role_id` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_rp_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- =============================================
-- 2. 医院机构管理模块
-- =============================================

-- 医院信息表
CREATE TABLE `hospitals` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '医院ID',
  `hospital_name` VARCHAR(100) NOT NULL COMMENT '医院名称',
  `hospital_code` VARCHAR(50) NOT NULL COMMENT '医院编码',
  `hospital_level` VARCHAR(20) DEFAULT NULL COMMENT '医院等级：三级甲等、三级乙等、二级甲等',
  `hospital_type` VARCHAR(50) DEFAULT NULL COMMENT '医院类型：综合医院、专科医院、中医医院',
  `province_code` VARCHAR(20) DEFAULT NULL COMMENT '省份编码',
  `province_name` VARCHAR(50) DEFAULT NULL COMMENT '省份名称',
  `city_code` VARCHAR(20) DEFAULT NULL COMMENT '城市编码',
  `city_name` VARCHAR(50) DEFAULT NULL COMMENT '城市名称',
  `district_code` VARCHAR(20) DEFAULT NULL COMMENT '区县编码',
  `district_name` VARCHAR(50) DEFAULT NULL COMMENT '区县名称',
  `address` VARCHAR(255) DEFAULT NULL COMMENT '详细地址',
  `longitude` DECIMAL(10,6) DEFAULT NULL COMMENT '经度',
  `latitude` DECIMAL(10,6) DEFAULT NULL COMMENT '纬度',
  `contact_phone` VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
  `emergency_phone` VARCHAR(20) DEFAULT NULL COMMENT '急救电话',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `website` VARCHAR(255) DEFAULT NULL COMMENT '官网',
  `description` TEXT DEFAULT NULL COMMENT '医院简介',
  `bed_count` INT UNSIGNED DEFAULT 0 COMMENT '床位数',
  `doctor_count` INT UNSIGNED DEFAULT 0 COMMENT '医生数',
  `nurse_count` INT UNSIGNED DEFAULT 0 COMMENT '护士数',
  `established_date` DATE DEFAULT NULL COMMENT '建院日期',
  `logo_url` VARCHAR(500) DEFAULT NULL COMMENT '医院Logo',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_hospital_code` (`hospital_code`),
  KEY `idx_hospital_name` (`hospital_name`),
  KEY `idx_province_city` (`province_code`, `city_code`),
  KEY `idx_hospital_level` (`hospital_level`),
  KEY `idx_hospital_type` (`hospital_type`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='医院信息表';

-- 科室信息表
CREATE TABLE `departments` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '科室ID',
  `hospital_id` BIGINT UNSIGNED NOT NULL COMMENT '所属医院ID',
  `department_name` VARCHAR(100) NOT NULL COMMENT '科室名称',
  `department_code` VARCHAR(50) NOT NULL COMMENT '科室编码',
  `parent_id` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '父科室ID',
  `department_type` VARCHAR(50) DEFAULT NULL COMMENT '科室类型：临床科室、医技科室、行政科室',
  `category` VARCHAR(50) DEFAULT NULL COMMENT '科室分类：内科、外科、妇产科、儿科等',
  `description` TEXT DEFAULT NULL COMMENT '科室简介',
  `location` VARCHAR(255) DEFAULT NULL COMMENT '科室位置',
  `contact_phone` VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
  `doctor_count` INT UNSIGNED DEFAULT 0 COMMENT '医生数量',
  `bed_count` INT UNSIGNED DEFAULT 0 COMMENT '床位数',
  `director_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '科室主任ID',
  `sort_order` INT UNSIGNED DEFAULT 0 COMMENT '排序',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_hospital_dept` (`hospital_id`, `department_code`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_department_name` (`department_name`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_dept_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='科室信息表';

-- =============================================
-- 3. 患者信息管理模块
-- =============================================

-- 患者基础信息表
CREATE TABLE `patients` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '患者ID',
  `patient_no` VARCHAR(50) NOT NULL COMMENT '患者编号',
  `name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `gender` TINYINT(1) NOT NULL COMMENT '性别：1-男，2-女',
  `birth_date` DATE DEFAULT NULL COMMENT '出生日期',
  `age` TINYINT UNSIGNED DEFAULT NULL COMMENT '年龄',
  `age_type` TINYINT(1) DEFAULT 1 COMMENT '年龄类型：1-周岁，2-月龄',
  `id_card` VARCHAR(18) DEFAULT NULL COMMENT '身份证号',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号码',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `address` VARCHAR(255) DEFAULT NULL COMMENT '居住地址',
  `province_code` VARCHAR(20) DEFAULT NULL COMMENT '省份编码',
  `city_code` VARCHAR(20) DEFAULT NULL COMMENT '城市编码',
  `district_code` VARCHAR(20) DEFAULT NULL COMMENT '区县编码',
  `blood_type` VARCHAR(10) DEFAULT NULL COMMENT '血型：A、B、AB、O',
  `rh_factor` TINYINT(1) DEFAULT NULL COMMENT 'RH因子：1-阳性，2-阴性',
  `marital_status` TINYINT(1) DEFAULT NULL COMMENT '婚姻状况：1-未婚，2-已婚，3-离异，4-丧偶',
  `occupation` VARCHAR(50) DEFAULT NULL COMMENT '职业',
  `education` VARCHAR(50) DEFAULT NULL COMMENT '学历',
  `nationality` VARCHAR(50) DEFAULT '中国' COMMENT '国籍',
  `ethnicity` VARCHAR(50) DEFAULT NULL COMMENT '民族',
  `emergency_contact` VARCHAR(50) DEFAULT NULL COMMENT '紧急联系人',
  `emergency_phone` VARCHAR(20) DEFAULT NULL COMMENT '紧急联系电话',
  `relationship` VARCHAR(20) DEFAULT NULL COMMENT '与患者关系',
  `allergy_history` TEXT DEFAULT NULL COMMENT '过敏史',
  `family_history` TEXT DEFAULT NULL COMMENT '家族病史',
  `past_history` TEXT DEFAULT NULL COMMENT '既往病史',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-正常，0-注销',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_patient_no` (`patient_no`),
  UNIQUE KEY `uk_id_card` (`id_card`),
  KEY `idx_name` (`name`),
  KEY `idx_gender` (`gender`),
  KEY `idx_birth_date` (`birth_date`),
  KEY `idx_phone` (`phone`),
  KEY `idx_address` (`province_code`, `city_code`, `district_code`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='患者基础信息表';

-- =============================================
-- 4. 医疗数据管理模块
-- =============================================

-- 医疗记录表
CREATE TABLE `medical_records` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `record_no` VARCHAR(50) NOT NULL COMMENT '记录编号',
  `patient_id` BIGINT UNSIGNED NOT NULL COMMENT '患者ID',
  `hospital_id` BIGINT UNSIGNED NOT NULL COMMENT '医院ID',
  `department_id` BIGINT UNSIGNED NOT NULL COMMENT '科室ID',
  `doctor_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '主治医生ID',
  `visit_type` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '就诊类型：1-门诊，2-急诊，3-住院',
  `admission_date` DATETIME DEFAULT NULL COMMENT '入院时间',
  `discharge_date` DATETIME DEFAULT NULL COMMENT '出院时间',
  `chief_complaint` VARCHAR(500) DEFAULT NULL COMMENT '主诉',
  `present_illness` TEXT DEFAULT NULL COMMENT '现病史',
  `physical_examination` TEXT DEFAULT NULL COMMENT '体格检查',
  `diagnosis` TEXT DEFAULT NULL COMMENT '诊断结果',
  `disease_code` VARCHAR(100) DEFAULT NULL COMMENT '疾病编码',
  `disease_name` VARCHAR(200) DEFAULT NULL COMMENT '疾病名称',
  `disease_category` VARCHAR(100) DEFAULT NULL COMMENT '疾病分类',
  `severity` TINYINT(1) DEFAULT NULL COMMENT '严重程度：1-轻度，2-中度，3-重度',
  `treatment_plan` TEXT DEFAULT NULL COMMENT '治疗方案',
  `medication` TEXT DEFAULT NULL COMMENT '用药信息',
  `surgery_info` TEXT DEFAULT NULL COMMENT '手术信息',
  `lab_results` TEXT DEFAULT NULL COMMENT '检验结果',
  `imaging_results` TEXT DEFAULT NULL COMMENT '影像结果',
  `pathology_results` TEXT DEFAULT NULL COMMENT '病理结果',
  `prognosis` VARCHAR(200) DEFAULT NULL COMMENT '预后评估',
  `follow_up_plan` TEXT DEFAULT NULL COMMENT '随访计划',
  `notes` TEXT DEFAULT NULL COMMENT '备注',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-正常，2-作废',
  `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
  `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '更新人ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_record_no` (`record_no`),
  KEY `idx_patient_id` (`patient_id`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_department_id` (`department_id`),
  KEY `idx_doctor_id` (`doctor_id`),
  KEY `idx_visit_type` (`visit_type`),
  KEY `idx_admission_date` (`admission_date`),
  KEY `idx_disease_code` (`disease_code`),
  KEY `idx_disease_category` (`disease_category`),
  KEY `idx_severity` (`severity`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_mr_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_mr_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_mr_department_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='医疗记录表';

-- 生命体征表
CREATE TABLE `vital_signs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `record_id` BIGINT UNSIGNED NOT NULL COMMENT '医疗记录ID',
  `patient_id` BIGINT UNSIGNED NOT NULL COMMENT '患者ID',
  `measure_time` DATETIME NOT NULL COMMENT '测量时间',
  `height` DECIMAL(5,2) DEFAULT NULL COMMENT '身高(cm)',
  `weight` DECIMAL(5,2) DEFAULT NULL COMMENT '体重(kg)',
  `bmi` DECIMAL(4,1) DEFAULT NULL COMMENT 'BMI指数',
  `systolic_pressure` SMALLINT UNSIGNED DEFAULT NULL COMMENT '收缩压(mmHg)',
  `diastolic_pressure` SMALLINT UNSIGNED DEFAULT NULL COMMENT '舒张压(mmHg)',
  `heart_rate` SMALLINT UNSIGNED DEFAULT NULL COMMENT '心率(次/分)',
  `respiratory_rate` SMALLINT UNSIGNED DEFAULT NULL COMMENT '呼吸频率(次/分)',
  `body_temperature` DECIMAL(4,1) DEFAULT NULL COMMENT '体温(℃)',
  `oxygen_saturation` DECIMAL(4,1) DEFAULT NULL COMMENT '血氧饱和度(%)',
  `blood_glucose` DECIMAL(5,2) DEFAULT NULL COMMENT '血糖(mmol/L)',
  `pain_score` TINYINT UNSIGNED DEFAULT NULL COMMENT '疼痛评分(0-10分)',
  `consciousness` VARCHAR(50) DEFAULT NULL COMMENT '意识状态',
  `measure_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '测量人ID',
  `notes` VARCHAR(500) DEFAULT NULL COMMENT '备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_record_id` (`record_id`),
  KEY `idx_patient_id` (`patient_id`),
  KEY `idx_measure_time` (`measure_time`),
  KEY `idx_systolic_pressure` (`systolic_pressure`),
  KEY `idx_diastolic_pressure` (`diastolic_pressure`),
  KEY `idx_heart_rate` (`heart_rate`),
  CONSTRAINT `fk_vs_record_id` FOREIGN KEY (`record_id`) REFERENCES `medical_records` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_vs_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='生命体征表';

-- =============================================
-- 5. 孕产妇专项管理模块
-- =============================================

-- 孕产妇信息表
CREATE TABLE `maternal_info` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '孕产妇ID',
  `patient_id` BIGINT UNSIGNED NOT NULL COMMENT '患者ID',
  `maternal_no` VARCHAR(50) NOT NULL COMMENT '孕产妇编号',
  `pregnancy_count` TINYINT UNSIGNED DEFAULT 0 COMMENT '孕次',
  `parity_count` TINYINT UNSIGNED DEFAULT 0 COMMENT '产次',
  `last_menstrual_date` DATE DEFAULT NULL COMMENT '末次月经时间',
  `expected_date` DATE DEFAULT NULL COMMENT '预产期',
  `pregnancy_type` VARCHAR(50) DEFAULT NULL COMMENT '妊娠类型：单胎、双胎、多胎',
  `fetal_count` TINYINT UNSIGNED DEFAULT 1 COMMENT '胎儿数量',
  `current_gestational_week` TINYINT UNSIGNED DEFAULT NULL COMMENT '当前孕周',
  `pregnancy_status` VARCHAR(50) DEFAULT NULL COMMENT '孕期状态：孕早期、孕中期、孕晚期',
  `risk_level` VARCHAR(20) DEFAULT NULL COMMENT '风险等级：低风险、中风险、高风险',
  `risk_factors` TEXT DEFAULT NULL COMMENT '风险因素',
  `prenatal_care_count` TINYINT UNSIGNED DEFAULT 0 COMMENT '产检次数',
  `last_check_date` DATE DEFAULT NULL COMMENT '末次产检日期',
  `next_check_date` DATE DEFAULT NULL COMMENT '下次产检日期',
  `delivery_hospital_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '分娩医院ID',
  `delivery_method` VARCHAR(50) DEFAULT NULL COMMENT '分娩方式：顺产、剖宫产',
  `delivery_date` DATETIME DEFAULT NULL COMMENT '分娩时间',
  `newborn_count` TINYINT UNSIGNED DEFAULT 0 COMMENT '新生儿数量',
  `complications` TEXT DEFAULT NULL COMMENT '并发症',
  `notes` TEXT DEFAULT NULL COMMENT '备注',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-正常，2-结束，3-异常',
  `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
  `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '更新人ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_maternal_no` (`maternal_no`),
  KEY `idx_patient_id` (`patient_id`),
  KEY `idx_current_gestational_week` (`current_gestational_week`),
  KEY `idx_pregnancy_status` (`pregnancy_status`),
  KEY `idx_risk_level` (`risk_level`),
  KEY `idx_expected_date` (`expected_date`),
  KEY `idx_last_check_date` (`last_check_date`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_mi_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='孕产妇信息表';

-- 产检记录表
CREATE TABLE `prenatal_examinations` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '产检ID',
  `maternal_id` BIGINT UNSIGNED NOT NULL COMMENT '孕产妇ID',
  `examination_no` VARCHAR(50) NOT NULL COMMENT '产检编号',
  `gestational_week` TINYINT UNSIGNED NOT NULL COMMENT '孕周',
  `examination_date` DATETIME NOT NULL COMMENT '产检日期',
  `hospital_id` BIGINT UNSIGNED NOT NULL COMMENT '检查医院ID',
  `department_id` BIGINT UNSIGNED NOT NULL COMMENT '检查科室ID',
  `doctor_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '检查医生ID',
  `weight` DECIMAL(5,2) DEFAULT NULL COMMENT '体重(kg)',
  `height` DECIMAL(5,2) DEFAULT NULL COMMENT '身高(cm)',
  `bmi` DECIMAL(4,1) DEFAULT NULL COMMENT 'BMI指数',
  `systolic_pressure` SMALLINT UNSIGNED DEFAULT NULL COMMENT '收缩压(mmHg)',
  `diastolic_pressure` SMALLINT UNSIGNED DEFAULT NULL COMMENT '舒张压(mmHg)',
  `blood_glucose` DECIMAL(5,2) DEFAULT NULL COMMENT '血糖(mmol/L)',
  `hemoglobin` DECIMAL(5,1) DEFAULT NULL COMMENT '血红蛋白(g/L)',
  `urine_protein` VARCHAR(20) DEFAULT NULL COMMENT '尿蛋白',
  `edema` VARCHAR(50) DEFAULT NULL COMMENT '水肿情况',
  `fundal_height` DECIMAL(4,1) DEFAULT NULL COMMENT '宫高(cm)',
  `abdominal_circumference` DECIMAL(4,1) DEFAULT NULL COMMENT '腹围(cm)',
  `fetal_heart_rate` SMALLINT UNSIGNED DEFAULT NULL COMMENT '胎心率(次/分)',
  `fetal_position` VARCHAR(50) DEFAULT NULL COMMENT '胎位',
  `ultrasound_results` TEXT DEFAULT NULL COMMENT 'B超结果',
  `laboratory_results` TEXT DEFAULT NULL COMMENT '实验室检查结果',
  `diagnosis` TEXT DEFAULT NULL COMMENT '诊断',
  `treatment_advice` TEXT DEFAULT NULL COMMENT '治疗建议',
  `next_check_date` DATE DEFAULT NULL COMMENT '下次产检日期',
  `risk_assessment` TEXT DEFAULT NULL COMMENT '风险评估',
  `notes` TEXT DEFAULT NULL COMMENT '备注',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-正常，2-异常',
  `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
  `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '更新人ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_examination_no` (`examination_no`),
  KEY `idx_maternal_id` (`maternal_id`),
  KEY `idx_gestational_week` (`gestational_week`),
  KEY `idx_examination_date` (`examination_date`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_department_id` (`department_id`),
  KEY `idx_doctor_id` (`doctor_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_pe_maternal_id` FOREIGN KEY (`maternal_id`) REFERENCES `maternal_info` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_pe_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_pe_department_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='产检记录表';

-- =============================================
-- 6. 系统管理模块
-- =============================================

-- 操作日志表
CREATE TABLE `operation_logs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '操作用户ID',
  `username` VARCHAR(50) DEFAULT NULL COMMENT '操作用户名',
  `operation_type` VARCHAR(50) NOT NULL COMMENT '操作类型：login,logout,create,update,delete,query,export',
  `module` VARCHAR(50) DEFAULT NULL COMMENT '操作模块',
  `resource_type` VARCHAR(50) DEFAULT NULL COMMENT '资源类型',
  `resource_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '资源ID',
  `operation_desc` VARCHAR(255) DEFAULT NULL COMMENT '操作描述',
  `request_method` VARCHAR(10) DEFAULT NULL COMMENT '请求方法',
  `request_url` VARCHAR(500) DEFAULT NULL COMMENT '请求URL',
  `request_params` TEXT DEFAULT NULL COMMENT '请求参数',
  `response_result` TEXT DEFAULT NULL COMMENT '响应结果',
  `ip_address` VARCHAR(45) DEFAULT NULL COMMENT 'IP地址',
  `user_agent` VARCHAR(500) DEFAULT NULL COMMENT '用户代理',
  `execution_time` INT UNSIGNED DEFAULT NULL COMMENT '执行时间(毫秒)',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '操作状态：1-成功，0-失败',
  `error_message` VARCHAR(500) DEFAULT NULL COMMENT '错误信息',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_username` (`username`),
  KEY `idx_operation_type` (`operation_type`),
  KEY `idx_module` (`module`),
  KEY `idx_ip_address` (`ip_address`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- 系统配置表
CREATE TABLE `system_configs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `config_key` VARCHAR(100) NOT NULL COMMENT '配置键',
  `config_value` TEXT DEFAULT NULL COMMENT '配置值',
  `config_type` VARCHAR(50) DEFAULT 'string' COMMENT '配置类型：string,number,boolean,json',
  `description` VARCHAR(255) DEFAULT NULL COMMENT '配置描述',
  `group_name` VARCHAR(50) DEFAULT NULL COMMENT '配置分组',
  `is_system` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否系统配置：1-是，0-否',
  `sort_order` INT UNSIGNED DEFAULT 0 COMMENT '排序',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
  `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '更新人ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_key` (`config_key`),
  KEY `idx_group_name` (`group_name`),
  KEY `idx_is_system` (`is_system`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- =============================================
-- 7. 数据统计和分析模块
-- =============================================

-- 疾病统计表
CREATE TABLE `disease_statistics` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '统计ID',
  `stat_date` DATE NOT NULL COMMENT '统计日期',
  `hospital_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '医院ID',
  `department_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '科室ID',
  `disease_code` VARCHAR(100) DEFAULT NULL COMMENT '疾病编码',
  `disease_name` VARCHAR(200) DEFAULT NULL COMMENT '疾病名称',
  `disease_category` VARCHAR(100) DEFAULT NULL COMMENT '疾病分类',
  `total_cases` INT UNSIGNED DEFAULT 0 COMMENT '总病例数',
  `new_cases` INT UNSIGNED DEFAULT 0 COMMENT '新增病例数',
  `male_cases` INT UNSIGNED DEFAULT 0 COMMENT '男性病例数',
  `female_cases` INT UNSIGNED DEFAULT 0 COMMENT '女性病例数',
  `age_group_0_18` INT UNSIGNED DEFAULT 0 COMMENT '0-18岁病例数',
  `age_group_19_35` INT UNSIGNED DEFAULT 0 COMMENT '19-35岁病例数',
  `age_group_36_50` INT UNSIGNED DEFAULT 0 COMMENT '36-50岁病例数',
  `age_group_51_65` INT UNSIGNED DEFAULT 0 COMMENT '51-65岁病例数',
  `age_group_65_plus` INT UNSIGNED DEFAULT 0 COMMENT '65岁以上病例数',
  `mild_cases` INT UNSIGNED DEFAULT 0 COMMENT '轻度病例数',
  `moderate_cases` INT UNSIGNED DEFAULT 0 COMMENT '中度病例数',
  `severe_cases` INT UNSIGNED DEFAULT 0 COMMENT '重度病例数',
  `recovery_cases` INT UNSIGNED DEFAULT 0 COMMENT '康复病例数',
  `death_cases` INT UNSIGNED DEFAULT 0 COMMENT '死亡病例数',
  `avg_treatment_days` DECIMAL(6,2) DEFAULT 0 COMMENT '平均治疗天数',
  `total_cost` DECIMAL(12,2) DEFAULT 0 COMMENT '总费用',
  `avg_cost` DECIMAL(10,2) DEFAULT 0 COMMENT '平均费用',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_stat_date_hospital_dept_disease` (`stat_date`, `hospital_id`, `department_id`, `disease_code`),
  KEY `idx_stat_date` (`stat_date`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_department_id` (`department_id`),
  KEY `idx_disease_code` (`disease_code`),
  KEY `idx_disease_category` (`disease_category`),
  KEY `idx_total_cases` (`total_cases`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='疾病统计表';

-- 孕产妇统计表
CREATE TABLE `maternal_statistics` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '统计ID',
  `stat_date` DATE NOT NULL COMMENT '统计日期',
  `hospital_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '医院ID',
  `total_pregnant` INT UNSIGNED DEFAULT 0 COMMENT '孕妇总数',
  `new_pregnant` INT UNSIGNED DEFAULT 0 COMMENT '新增孕妇数',
  `first_trimester` INT UNSIGNED DEFAULT 0 COMMENT '孕早期人数',
  `second_trimester` INT UNSIGNED DEFAULT 0 COMMENT '孕中期人数',
  `third_trimester` INT UNSIGNED DEFAULT 0 COMMENT '孕晚期人数',
  `low_risk` INT UNSIGNED DEFAULT 0 COMMENT '低风险人数',
  `medium_risk` INT UNSIGNED DEFAULT 0 COMMENT '中风险人数',
  `high_risk` INT UNSIGNED DEFAULT 0 COMMENT '高风险人数',
  `total_deliveries` INT UNSIGNED DEFAULT 0 COMMENT '分娩总数',
  `natural_delivery` INT UNSIGNED DEFAULT 0 COMMENT '顺产数',
  `cesarean_delivery` INT UNSIGNED DEFAULT 0 COMMENT '剖宫产数',
  `total_prenatal_checks` INT UNSIGNED DEFAULT 0 COMMENT '产检总数',
  `avg_prenatal_checks` DECIMAL(4,1) DEFAULT 0 COMMENT '平均产检次数',
  `complications_count` INT UNSIGNED DEFAULT 0 COMMENT '并发症数',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_stat_date_hospital` (`stat_date`, `hospital_id`),
  KEY `idx_stat_date` (`stat_date`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_total_pregnant` (`total_pregnant`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='孕产妇统计表';

-- =============================================
-- 初始化基础数据
-- =============================================

-- 插入默认角色
INSERT INTO `roles` (`role_name`, `role_code`, `description`, `level`) VALUES
('超级管理员', 'SUPER_ADMIN', '系统超级管理员，拥有所有权限', 1),
('管理员', 'ADMIN', '系统管理员，拥有大部分管理权限', 2),
('医生', 'DOCTOR', '医生角色，拥有医疗相关权限', 3),
('护士', 'NURSE', '护士角色，拥有护理相关权限', 4),
('普通用户', 'USER', '普通用户，拥有基本查看权限', 5);

-- 插入系统配置
INSERT INTO `system_configs` (`config_key`, `config_value`, `config_type`, `description`, `group_name`, `is_system`) VALUES
('system_name', '医疗疾病数据分析大屏可视化系统', 'string', '系统名称', 'system', 1),
('system_version', '3.0.0', 'string', '系统版本', 'system', 1),
('max_login_attempts', '5', 'number', '最大登录尝试次数', 'security', 1),
('session_timeout', '7200', 'number', '会话超时时间(秒)', 'security', 1),
('data_retention_days', '2555', 'number', '数据保留天数', 'data', 1),
('export_limit', '10000', 'number', '数据导出限制条数', 'data', 1);

-- 启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================
-- 创建视图
-- =============================================

-- 患者完整信息视图
CREATE VIEW `patient_full_info` AS
SELECT 
    p.id,
    p.patient_no,
    p.name,
    CASE p.gender WHEN 1 THEN '男' WHEN 2 THEN '女' ELSE '未知' END as gender_name,
    p.birth_date,
    p.age,
    p.phone,
    p.id_card,
    p.address,
    h.hospital_name,
    d.department_name,
    p.created_at
FROM patients p
LEFT JOIN maternal_info mi ON p.id = mi.patient_id
LEFT JOIN hospitals h ON mi.delivery_hospital_id = h.id
LEFT JOIN departments d ON mi.delivery_hospital_id = d.hospital_id;

-- 医疗记录统计视图
CREATE VIEW `medical_record_stats` AS
SELECT 
    DATE(mr.created_at) as stat_date,
    h.hospital_name,
    d.department_name,
    mr.disease_category,
    COUNT(*) as total_cases,
    COUNT(CASE WHEN mr.gender = 1 THEN 1 END) as male_cases,
    COUNT(CASE WHEN mr.gender = 2 THEN 1 END) as female_cases,
    AVG(TIMESTAMPDIFF(DAY, mr.admission_date, mr.discharge_date)) as avg_stay_days
FROM medical_records mr
LEFT JOIN hospitals h ON mr.hospital_id = h.id
LEFT JOIN departments d ON mr.department_id = d.id
GROUP BY DATE(mr.created_at), h.hospital_name, d.department_name, mr.disease_category;

-- =============================================
-- 创建存储过程
-- =============================================

DELIMITER $$

-- 生成疾病统计数据的存储过程
CREATE PROCEDURE `GenerateDiseaseStatistics`(IN stat_date DATE)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- 删除当天的统计数据
    DELETE FROM disease_statistics WHERE stat_date = stat_date;
    
    -- 生成新的统计数据
    INSERT INTO disease_statistics (
        stat_date, hospital_id, department_id, disease_code, disease_name, disease_category,
        total_cases, new_cases, male_cases, female_cases,
        age_group_0_18, age_group_19_35, age_group_36_50, age_group_51_65, age_group_65_plus,
        mild_cases, moderate_cases, severe_cases, recovery_cases, death_cases
    )
    SELECT 
        stat_date,
        mr.hospital_id,
        mr.department_id,
        mr.disease_code,
        mr.disease_name,
        mr.disease_category,
        COUNT(*) as total_cases,
        COUNT(CASE WHEN DATE(mr.created_at) = stat_date THEN 1 END) as new_cases,
        COUNT(CASE WHEN p.gender = 1 THEN 1 END) as male_cases,
        COUNT(CASE WHEN p.gender = 2 THEN 1 END) as female_cases,
        COUNT(CASE WHEN p.age BETWEEN 0 AND 18 THEN 1 END) as age_group_0_18,
        COUNT(CASE WHEN p.age BETWEEN 19 AND 35 THEN 1 END) as age_group_19_35,
        COUNT(CASE WHEN p.age BETWEEN 36 AND 50 THEN 1 END) as age_group_36_50,
        COUNT(CASE WHEN p.age BETWEEN 51 AND 65 THEN 1 END) as age_group_51_65,
        COUNT(CASE WHEN p.age > 65 THEN 1 END) as age_group_65_plus,
        COUNT(CASE WHEN mr.severity = 1 THEN 1 END) as mild_cases,
        COUNT(CASE WHEN mr.severity = 2 THEN 1 END) as moderate_cases,
        COUNT(CASE WHEN mr.severity = 3 THEN 1 END) as severe_cases,
        COUNT(CASE WHEN mr.status = 1 THEN 1 END) as recovery_cases,
        COUNT(CASE WHEN mr.status = 0 THEN 1 END) as death_cases
    FROM medical_records mr
    INNER JOIN patients p ON mr.patient_id = p.id
    WHERE DATE(mr.created_at) <= stat_date
    GROUP BY mr.hospital_id, mr.department_id, mr.disease_code, mr.disease_name, mr.disease_category;
    
    COMMIT;
END$$

-- 生成孕产妇统计数据的存储过程
CREATE PROCEDURE `GenerateMaternalStatistics`(IN stat_date DATE)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- 删除当天的统计数据
    DELETE FROM maternal_statistics WHERE stat_date = stat_date;
    
    -- 生成新的统计数据
    INSERT INTO maternal_statistics (
        stat_date, hospital_id,
        total_pregnant, new_pregnant,
        first_trimester, second_trimester, third_trimester,
        low_risk, medium_risk, high_risk,
        total_deliveries, natural_delivery, cesarean_delivery,
        total_prenatal_checks, avg_prenatal_checks, complications_count
    )
    SELECT 
        stat_date,
        h.id as hospital_id,
        COUNT(*) as total_pregnant,
        COUNT(CASE WHEN DATE(mi.created_at) = stat_date THEN 1 END) as new_pregnant,
        COUNT(CASE WHEN mi.current_gestational_week <= 12 THEN 1 END) as first_trimester,
        COUNT(CASE WHEN mi.current_gestational_week BETWEEN 13 AND 28 THEN 1 END) as second_trimester,
        COUNT(CASE WHEN mi.current_gestational_week > 28 THEN 1 END) as third_trimester,
        COUNT(CASE WHEN mi.risk_level = '低风险' THEN 1 END) as low_risk,
        COUNT(CASE WHEN mi.risk_level = '中风险' THEN 1 END) as medium_risk,
        COUNT(CASE WHEN mi.risk_level = '高风险' THEN 1 END) as high_risk,
        COUNT(CASE WHEN mi.delivery_date IS NOT NULL THEN 1 END) as total_deliveries,
        COUNT(CASE WHEN mi.delivery_method = '顺产' THEN 1 END) as natural_delivery,
        COUNT(CASE WHEN mi.delivery_method = '剖宫产' THEN 1 END) as cesarean_delivery,
        COUNT(pe.id) as total_prenatal_checks,
        AVG(CASE WHEN mi.id IS NOT NULL THEN 
            (SELECT COUNT(*) FROM prenatal_examinations WHERE maternal_id = mi.id) 
        END) as avg_prenatal_checks,
        COUNT(CASE WHEN mi.complications IS NOT NULL AND mi.complications != '' THEN 1 END) as complications_count
    FROM maternal_info mi
    LEFT JOIN hospitals h ON mi.delivery_hospital_id = h.id
    LEFT JOIN prenatal_examinations pe ON mi.id = pe.maternal_id
    WHERE DATE(mi.created_at) <= stat_date
    GROUP BY h.id;
    
    COMMIT;
END$$

DELIMITER ;

-- =============================================
-- 创建触发器
-- =============================================

-- 医疗记录插入触发器
DELIMITER $$
CREATE TRIGGER `tr_medical_records_insert` 
AFTER INSERT ON `medical_records`
FOR EACH ROW
BEGIN
    -- 记录操作日志
    INSERT INTO operation_logs (
        user_id, operation_type, module, resource_type, resource_id, 
        operation_desc, status
    ) VALUES (
        NEW.created_by, 'create', 'medical', 'medical_record', NEW.id,
        CONCAT('创建医疗记录：', NEW.record_no), 1
    );
END$$
DELIMITER ;

-- 孕产妇信息更新触发器
DELIMITER $$
CREATE TRIGGER `tr_maternal_info_update` 
AFTER UPDATE ON `maternal_info`
FOR EACH ROW
BEGIN
    -- 记录操作日志
    INSERT INTO operation_logs (
        user_id, operation_type, module, resource_type, resource_id, 
        operation_desc, status
    ) VALUES (
        NEW.updated_by, 'update', 'maternal', 'maternal_info', NEW.id,
        CONCAT('更新孕产妇信息：', NEW.maternal_no), 1
    );
END$$
DELIMITER ;

-- =============================================
-- 创建索引优化
-- =============================================

-- 为常用查询创建复合索引
CREATE INDEX `idx_mr_patient_date` ON `medical_records` (`patient_id`, `created_at`);
CREATE INDEX `idx_mr_hospital_dept_date` ON `medical_records` (`hospital_id`, `department_id`, `created_at`);
CREATE INDEX `idx_vs_patient_time` ON `vital_signs` (`patient_id`, `measure_time`);
CREATE INDEX `idx_pe_maternal_week` ON `prenatal_examinations` (`maternal_id`, `gestational_week`);
CREATE INDEX `idx_logs_user_time` ON `operation_logs` (`user_id`, `created_at`);
CREATE INDEX `idx_ds_date_hospital` ON `disease_statistics` (`stat_date`, `hospital_id`);
CREATE INDEX `idx_ms_date_hospital` ON `maternal_statistics` (`stat_date`, `hospital_id`);

-- =============================================
-- 数据库设计说明
-- =============================================

/*
设计原则：
1. 遵循第三范式(3NF)，消除数据冗余
2. 使用合适的数据类型，节省存储空间
3. 建立完善的外键约束，保证数据完整性
4. 创建合理的索引，提高查询性能
5. 使用软删除，保留历史数据
6. 添加审计字段，记录数据变更
7. 使用存储过程处理复杂业务逻辑
8. 创建视图简化复杂查询
9. 使用触发器自动记录操作日志
10. 支持多医院、多科室的数据隔离

表结构特点：
- 用户权限管理：支持RBAC权限模型
- 医院机构管理：支持多级医院和科室结构
- 患者信息管理：完整的患者档案信息
- 医疗数据管理：标准化的医疗记录格式
- 孕产妇专项：专业的孕产妇健康管理
- 系统管理：完善的日志和配置管理
- 数据统计：多维度的统计分析能力

扩展性：
- 支持水平分表分库
- 支持读写分离
- 支持缓存层集成
- 支持微服务拆分
- 支持大数据分析集成
*/
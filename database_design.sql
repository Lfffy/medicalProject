-- 医疗疾病数据分析系统扩展功能数据库设计
-- 创建时间：2025-06-17
-- 版本：v2.0

-- =============================================
-- 1. 用户管理相关表
-- =============================================

-- 用户表
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `email` varchar(100) NOT NULL COMMENT '邮箱',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希',
  `real_name` varchar(50) DEFAULT NULL COMMENT '真实姓名',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  `hospital_id` int(11) DEFAULT NULL COMMENT '所属医院ID',
  `department_id` int(11) DEFAULT NULL COMMENT '所属科室ID',
  `status` tinyint(1) DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  KEY `idx_role_id` (`role_id`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_department_id` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 角色表
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL COMMENT '角色名称',
  `role_code` varchar(50) NOT NULL COMMENT '角色编码',
  `description` varchar(255) DEFAULT NULL COMMENT '角色描述',
  `status` tinyint(1) DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_code` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- 权限表
CREATE TABLE `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_name` varchar(100) NOT NULL COMMENT '权限名称',
  `permission_code` varchar(100) NOT NULL COMMENT '权限编码',
  `resource_type` varchar(50) DEFAULT NULL COMMENT '资源类型',
  `resource_path` varchar(255) DEFAULT NULL COMMENT '资源路径',
  `parent_id` int(11) DEFAULT 0 COMMENT '父权限ID',
  `sort_order` int(11) DEFAULT 0 COMMENT '排序',
  `status` tinyint(1) DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_permission_code` (`permission_code`),
  KEY `idx_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

-- 角色权限关联表
CREATE TABLE `role_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL COMMENT '角色ID',
  `permission_id` int(11) NOT NULL COMMENT '权限ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_permission` (`role_id`, `permission_id`),
  KEY `idx_role_id` (`role_id`),
  KEY `idx_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色权限关联表';

-- 操作日志表
CREATE TABLE `operation_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '操作用户ID',
  `username` varchar(50) NOT NULL COMMENT '操作用户名',
  `operation_type` varchar(50) NOT NULL COMMENT '操作类型',
  `resource_type` varchar(50) DEFAULT NULL COMMENT '资源类型',
  `resource_id` int(11) DEFAULT NULL COMMENT '资源ID',
  `operation_desc` varchar(255) DEFAULT NULL COMMENT '操作描述',
  `ip_address` varchar(50) DEFAULT NULL COMMENT 'IP地址',
  `user_agent` varchar(500) DEFAULT NULL COMMENT '用户代理',
  `request_params` text COMMENT '请求参数',
  `response_result` text COMMENT '响应结果',
  `status` tinyint(1) DEFAULT 1 COMMENT '操作状态：1-成功，0-失败',
  `error_message` varchar(500) DEFAULT NULL COMMENT '错误信息',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_operation_type` (`operation_type`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- =============================================
-- 2. 医院管理相关表
-- =============================================

-- 医院信息表
CREATE TABLE `hospitals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hospital_name` varchar(100) NOT NULL COMMENT '医院名称',
  `hospital_code` varchar(50) NOT NULL COMMENT '医院编码',
  `hospital_level` varchar(20) DEFAULT NULL COMMENT '医院等级',
  `province` varchar(50) DEFAULT NULL COMMENT '省份',
  `city` varchar(50) DEFAULT NULL COMMENT '城市',
  `district` varchar(50) DEFAULT NULL COMMENT '区县',
  `address` varchar(255) DEFAULT NULL COMMENT '详细地址',
  `contact_phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `website` varchar(255) DEFAULT NULL COMMENT '官网',
  `description` text COMMENT '医院简介',
  `bed_count` int(11) DEFAULT NULL COMMENT '床位数',
  `established_date` date DEFAULT NULL COMMENT '建院日期',
  `logo_url` varchar(255) DEFAULT NULL COMMENT '医院Logo',
  `status` tinyint(1) DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_hospital_code` (`hospital_code`),
  KEY `idx_hospital_name` (`hospital_name`),
  KEY `idx_city` (`city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='医院信息表';

-- 科室信息表
CREATE TABLE `departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hospital_id` int(11) NOT NULL COMMENT '所属医院ID',
  `department_name` varchar(100) NOT NULL COMMENT '科室名称',
  `department_code` varchar(50) NOT NULL COMMENT '科室编码',
  `parent_id` int(11) DEFAULT 0 COMMENT '父科室ID',
  `department_type` varchar(50) DEFAULT NULL COMMENT '科室类型',
  `description` text COMMENT '科室简介',
  `location` varchar(255) DEFAULT NULL COMMENT '科室位置',
  `contact_phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `doctor_count` int(11) DEFAULT 0 COMMENT '医生数量',
  `bed_count` int(11) DEFAULT 0 COMMENT '床位数',
  `sort_order` int(11) DEFAULT 0 COMMENT '排序',
  `status` tinyint(1) DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_hospital_dept` (`hospital_id`, `department_code`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_department_name` (`department_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='科室信息表';

-- 医生信息表
CREATE TABLE `doctors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '关联用户ID',
  `hospital_id` int(11) NOT NULL COMMENT '所属医院ID',
  `department_id` int(11) NOT NULL COMMENT '所属科室ID',
  `doctor_code` varchar(50) NOT NULL COMMENT '医生编号',
  `title` varchar(50) DEFAULT NULL COMMENT '职称',
  `specialty` varchar(100) DEFAULT NULL COMMENT '专业特长',
  `education` varchar(50) DEFAULT NULL COMMENT '学历',
  `experience_years` int(11) DEFAULT 0 COMMENT '从业年限',
  `introduction` text COMMENT '个人简介',
  `consultation_fee` decimal(10,2) DEFAULT 0.00 COMMENT '挂号费',
  `rating` decimal(3,2) DEFAULT 5.00 COMMENT '评分',
  `consultation_count` int(11) DEFAULT 0 COMMENT '接诊次数',
  `status` tinyint(1) DEFAULT 1 COMMENT '状态：1-在职，0-离职',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_doctor_code` (`doctor_code`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_department_id` (`department_id`),
  KEY `idx_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='医生信息表';

-- 排班表
CREATE TABLE `schedules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` int(11) NOT NULL COMMENT '医生ID',
  `hospital_id` int(11) NOT NULL COMMENT '医院ID',
  `department_id` int(11) NOT NULL COMMENT '科室ID',
  `schedule_date` date NOT NULL COMMENT '排班日期',
  `shift_type` varchar(20) NOT NULL COMMENT '班次类型：morning,afternoon,night',
  `start_time` time NOT NULL COMMENT '开始时间',
  `end_time` time NOT NULL COMMENT '结束时间',
  `max_patients` int(11) DEFAULT 20 COMMENT '最大接诊人数',
  `booked_patients` int(11) DEFAULT 0 COMMENT '已预约人数',
  `status` tinyint(1) DEFAULT 1 COMMENT '状态：1-正常，0-取消',
  `notes` varchar(255) DEFAULT NULL COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_doctor_schedule` (`doctor_id`, `schedule_date`, `shift_type`),
  KEY `idx_doctor_id` (`doctor_id`),
  KEY `idx_schedule_date` (`schedule_date`),
  KEY `idx_hospital_id` (`hospital_id`),
  KEY `idx_department_id` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='医生排班表';

-- =============================================
-- 3. 数据管理相关表
-- =============================================

-- 数据导入记录表
CREATE TABLE `import_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '导入用户ID',
  `file_name` varchar(255) NOT NULL COMMENT '文件名',
  `file_path` varchar(500) DEFAULT NULL COMMENT '文件路径',
  `file_size` int(11) DEFAULT NULL COMMENT '文件大小（字节）',
  `data_type` varchar(50) NOT NULL COMMENT '数据类型：medical,maternal',
  `total_records` int(11) DEFAULT 0 COMMENT '总记录数',
  `success_records` int(11) DEFAULT 0 COMMENT '成功记录数',
  `failed_records` int(11) DEFAULT 0 COMMENT '失败记录数',
  `error_details` text COMMENT '错误详情',
  `import_status` varchar(20) DEFAULT 'processing' COMMENT '导入状态：processing,completed,failed',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_data_type` (`data_type`),
  KEY `idx_import_status` (`import_status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据导入记录表';

-- 数据变更记录表
CREATE TABLE `data_change_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '操作用户ID',
  `table_name` varchar(50) NOT NULL COMMENT '表名',
  `record_id` int(11) NOT NULL COMMENT '记录ID',
  `operation_type` varchar(20) NOT NULL COMMENT '操作类型：insert,update,delete',
  `old_values` json DEFAULT NULL COMMENT '旧值',
  `new_values` json DEFAULT NULL COMMENT '新值',
  `change_reason` varchar(255) DEFAULT NULL COMMENT '变更原因',
  `ip_address` varchar(50) DEFAULT NULL COMMENT 'IP地址',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_table_record` (`table_name`, `record_id`),
  KEY `idx_operation_type` (`operation_type`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据变更记录表';

-- =============================================
-- 4. 高级分析相关表
-- =============================================

-- 分析报告表
CREATE TABLE `analysis_reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `report_name` varchar(100) NOT NULL COMMENT '报告名称',
  `report_type` varchar(50) NOT NULL COMMENT '报告类型：trend,comparison,prediction',
  `data_type` varchar(50) NOT NULL COMMENT '数据类型：medical,maternal',
  `parameters` json DEFAULT NULL COMMENT '分析参数',
  `chart_config` json DEFAULT NULL COMMENT '图表配置',
  `report_data` json DEFAULT NULL COMMENT '报告数据',
  `conclusion` text COMMENT '分析结论',
  `file_path` varchar(500) DEFAULT NULL COMMENT '报告文件路径',
  `created_by` int(11) NOT NULL COMMENT '创建人ID',
  `status` varchar(20) DEFAULT 'draft' COMMENT '状态：draft,published,archived',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_report_type` (`report_type`),
  KEY `idx_data_type` (`data_type`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分析报告表';

-- 预测模型表
CREATE TABLE `prediction_models` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_name` varchar(100) NOT NULL COMMENT '模型名称',
  `model_type` varchar(50) NOT NULL COMMENT '模型类型：regression,classification,clustering',
  `target_variable` varchar(50) NOT NULL COMMENT '目标变量',
  `feature_variables` json DEFAULT NULL COMMENT '特征变量',
  `model_parameters` json DEFAULT NULL COMMENT '模型参数',
  `model_file_path` varchar(500) DEFAULT NULL COMMENT '模型文件路径',
  `accuracy_score` decimal(5,4) DEFAULT NULL COMMENT '准确率',
  `training_data_count` int(11) DEFAULT NULL COMMENT '训练数据量',
  `validation_data_count` int(11) DEFAULT NULL COMMENT '验证数据量',
  `training_date` datetime DEFAULT NULL COMMENT '训练时间',
  `created_by` int(11) NOT NULL COMMENT '创建人ID',
  `status` varchar(20) DEFAULT 'training' COMMENT '状态：training,completed,failed',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_model_type` (`model_type`),
  KEY `idx_target_variable` (`target_variable`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预测模型表';

-- =============================================
-- 5. 孕产妇专项功能相关表
-- =============================================

-- 产检记录表
CREATE TABLE `prenatal_checkups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maternal_id` int(11) NOT NULL COMMENT '孕产妇ID',
  `checkup_date` date NOT NULL COMMENT '检查日期',
  `gestational_weeks` int(11) NOT NULL COMMENT '孕周',
  `weight` decimal(5,2) DEFAULT NULL COMMENT '体重(kg)',
  `systolic_pressure` int(11) DEFAULT NULL COMMENT '收缩压',
  `diastolic_pressure` int(11) DEFAULT NULL COMMENT '舒张压',
  `fetal_heart_rate` int(11) DEFAULT NULL COMMENT '胎心率',
  `fundal_height` decimal(5,2) DEFAULT NULL COMMENT '宫高',
  `abdominal_circumference` decimal(5,2) DEFAULT NULL COMMENT '腹围',
  `urine_protein` varchar(10) DEFAULT NULL COMMENT '尿蛋白',
  `urine_glucose` varchar(10) DEFAULT NULL COMMENT '尿糖',
  `edema` varchar(20) DEFAULT NULL COMMENT '水肿程度',
  `doctor_id` int(11) DEFAULT NULL COMMENT '检查医生ID',
  `hospital_id` int(11) DEFAULT NULL COMMENT '检查医院ID',
  `checkup_items` json DEFAULT NULL COMMENT '检查项目详情',
  `abnormal_findings` text COMMENT '异常发现',
  `doctor_notes` text COMMENT '医生建议',
  `next_checkup_date` date DEFAULT NULL COMMENT '下次检查日期',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_maternal_id` (`maternal_id`),
  KEY `idx_checkup_date` (`checkup_date`),
  KEY `idx_gestational_weeks` (`gestational_weeks`),
  KEY `idx_doctor_id` (`doctor_id`),
  KEY `idx_hospital_id` (`hospital_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产检记录表';

-- 胎心监测记录表
CREATE TABLE `fetal_monitoring` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maternal_id` int(11) NOT NULL COMMENT '孕产妇ID',
  `monitoring_date` datetime NOT NULL COMMENT '监测时间',
  `gestational_weeks` int(11) NOT NULL COMMENT '孕周',
  `baseline_fhr` int(11) DEFAULT NULL COMMENT '基础胎心率',
  `fhr_variability` varchar(20) DEFAULT NULL COMMENT '胎心率变异',
  `accelerations` int(11) DEFAULT 0 COMMENT '加速次数',
  `decelerations` int(11) DEFAULT 0 COMMENT '减速次数',
  `contractions` int(11) DEFAULT 0 COMMENT '宫缩次数',
  `monitoring_duration` int(11) DEFAULT NULL COMMENT '监测时长(分钟)',
  `fhr_data` json DEFAULT NULL COMMENT '胎心率数据点',
  `contraction_data` json DEFAULT NULL COMMENT '宫缩数据点',
  `fetal_movements` int(11) DEFAULT 0 COMMENT '胎动次数',
  `interpretation` text COMMENT '监测结果解读',
  `risk_level` varchar(20) DEFAULT NULL COMMENT '风险等级',
  `doctor_id` int(11) DEFAULT NULL COMMENT '监测医生ID',
  `hospital_id` int(11) DEFAULT NULL COMMENT '监测医院ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_maternal_id` (`maternal_id`),
  KEY `idx_monitoring_date` (`monitoring_date`),
  KEY `idx_gestational_weeks` (`gestational_weeks`),
  KEY `idx_risk_level` (`risk_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='胎心监测记录表';

-- 营养建议表
CREATE TABLE `nutrition_recommendations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maternal_id` int(11) NOT NULL COMMENT '孕产妇ID',
  `gestational_weeks` int(11) NOT NULL COMMENT '孕周',
  `recommendation_date` date NOT NULL COMMENT '建议日期',
  `daily_calories` int(11) DEFAULT NULL COMMENT '每日所需热量(kcal)',
  `protein_intake` decimal(5,2) DEFAULT NULL COMMENT '蛋白质摄入量(g)',
  `carbohydrate_intake` decimal(5,2) DEFAULT NULL COMMENT '碳水化合物摄入量(g)',
  `fat_intake` decimal(5,2) DEFAULT NULL COMMENT '脂肪摄入量(g)',
  `fiber_intake` decimal(5,2) DEFAULT NULL COMMENT '纤维摄入量(g)',
  `vitamin_recommendations` json DEFAULT NULL COMMENT '维生素推荐',
  `mineral_recommendations` json DEFAULT NULL COMMENT '矿物质推荐',
  `food_recommendations` json DEFAULT NULL COMMENT '食物推荐',
  `food_restrictions` json DEFAULT NULL COMMENT '饮食禁忌',
  `weight_gain_target` decimal(5,2) DEFAULT NULL COMMENT '体重增长目标(kg)',
  `current_weight` decimal(5,2) DEFAULT NULL COMMENT '当前体重(kg)',
  `bmi` decimal(4,2) DEFAULT NULL COMMENT 'BMI指数',
  `nutrition_risk_factors` json DEFAULT NULL COMMENT '营养风险因素',
  `custom_advice` text COMMENT '个性化建议',
  `nutritionist_id` int(11) DEFAULT NULL COMMENT '营养师ID',
  `hospital_id` int(11) DEFAULT NULL COMMENT '医院ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_maternal_id` (`maternal_id`),
  KEY `idx_gestational_weeks` (`gestational_weeks`),
  KEY `idx_recommendation_date` (`recommendation_date`),
  KEY `idx_nutritionist_id` (`nutritionist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='营养建议表';

-- 预警记录表
CREATE TABLE `alert_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maternal_id` int(11) NOT NULL COMMENT '孕产妇ID',
  `alert_type` varchar(50) NOT NULL COMMENT '预警类型',
  `alert_level` varchar(20) NOT NULL COMMENT '预警级别：low,medium,high,critical',
  `alert_title` varchar(100) NOT NULL COMMENT '预警标题',
  `alert_description` text NOT NULL COMMENT '预警描述',
  `trigger_conditions` json DEFAULT NULL COMMENT '触发条件',
  `alert_data` json DEFAULT NULL COMMENT '相关数据',
  `gestational_weeks` int(11) DEFAULT NULL COMMENT '孕周',
  `doctor_id` int(11) DEFAULT NULL COMMENT '负责医生ID',
  `hospital_id` int(11) DEFAULT NULL COMMENT '医院ID',
  `notification_sent` tinyint(1) DEFAULT 0 COMMENT '是否已发送通知',
  `notification_time` datetime DEFAULT NULL COMMENT '通知发送时间',
  `notification_method` varchar(50) DEFAULT NULL COMMENT '通知方式',
  `status` varchar(20) DEFAULT 'active' COMMENT '状态：active,resolved,ignored',
  `resolution_notes` text COMMENT '处理说明',
  `resolved_by` int(11) DEFAULT NULL COMMENT '处理人ID',
  `resolved_at` datetime DEFAULT NULL COMMENT '处理时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_maternal_id` (`maternal_id`),
  KEY `idx_alert_type` (`alert_type`),
  KEY `idx_alert_level` (`alert_level`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预警记录表';

-- =============================================
-- 6. 初始化数据
-- =============================================

-- 插入默认角色
INSERT INTO `roles` (`role_name`, `role_code`, `description`) VALUES
('超级管理员', 'super_admin', '系统超级管理员，拥有所有权限'),
('医院管理员', 'hospital_admin', '医院管理员，管理本院数据和用户'),
('科室主任', 'department_director', '科室主任，管理科室内部事务'),
('医生', 'doctor', '普通医生，处理日常医疗工作'),
('护士', 'nurse', '护士，协助医生工作'),
('数据分析师', 'data_analyst', '数据分析师，负责数据分析和报告'),
('访客', 'visitor', '访客用户，只有查看权限');

-- 插入基础权限
INSERT INTO `permissions` (`permission_name`, `permission_code`, `resource_type`, `resource_path`, `parent_id`) VALUES
('用户管理', 'user:manage', 'module', '/users', 0),
('用户查看', 'user:view', 'action', '/users/view', 1),
('用户新增', 'user:add', 'action', '/users/add', 1),
('用户编辑', 'user:edit', 'action', '/users/edit', 1),
('用户删除', 'user:delete', 'action', '/users/delete', 1),

('医院管理', 'hospital:manage', 'module', '/hospitals', 0),
('医院查看', 'hospital:view', 'action', '/hospitals/view', 6),
('医院新增', 'hospital:add', 'action', '/hospitals/add', 6),
('医院编辑', 'hospital:edit', 'action', '/hospitals/edit', 6),
('医院删除', 'hospital:delete', 'action', '/hospitals/delete', 6),

('科室管理', 'department:manage', 'module', '/departments', 0),
('科室查看', 'department:view', 'action', '/departments/view', 11),
('科室新增', 'department:add', 'action', '/departments/add', 11),
('科室编辑', 'department:edit', 'action', '/departments/edit', 11),
('科室删除', 'department:delete', 'action', '/departments/delete', 11),

('医生管理', 'doctor:manage', 'module', '/doctors', 0),
('医生查看', 'doctor:view', 'action', '/doctors/view', 16),
('医生新增', 'doctor:add', 'action', '/doctors/add', 16),
('医生编辑', 'doctor:edit', 'action', '/doctors/edit', 16),
('医生删除', 'doctor:delete', 'action', '/doctors/delete', 16),

('数据管理', 'data:manage', 'module', '/data', 0),
('数据查看', 'data:view', 'action', '/data/view', 21),
('数据新增', 'data:add', 'action', '/data/add', 21),
('数据编辑', 'data:edit', 'action', '/data/edit', 21),
('数据删除', 'data:delete', 'action', '/data/delete', 21),
('数据导入', 'data:import', 'action', '/data/import', 21),
('数据导出', 'data:export', 'action', '/data/export', 21),

('高级分析', 'analysis:manage', 'module', '/analysis', 0),
('趋势分析', 'analysis:trend', 'action', '/analysis/trend', 27),
('对比分析', 'analysis:comparison', 'action', '/analysis/comparison', 27),
('预测分析', 'analysis:prediction', 'action', '/analysis/prediction', 27),
('报告生成', 'analysis:report', 'action', '/analysis/report', 27),

('孕产妇管理', 'maternal:manage', 'module', '/maternal', 0),
('产检记录', 'maternal:checkup', 'action', '/maternal/checkup', 32),
('胎心监测', 'maternal:fetal', 'action', '/maternal/fetal', 32),
('营养建议', 'maternal:nutrition', 'action', '/maternal/nutrition', 32),
('预警管理', 'maternal:alert', 'action', '/maternal/alert', 32);

-- 为超级管理员角色分配所有权限
INSERT INTO `role_permissions` (role_id, permission_id)
SELECT 1, id FROM permissions WHERE status = 1;

-- 创建默认超级管理员用户（密码：admin123）
INSERT INTO `users` (`username`, `email`, `password_hash`, `real_name`, `role_id`, `status`) VALUES
('admin', 'admin@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e', '系统管理员', 1, 1);

-- 创建示例医院数据
INSERT INTO `hospitals` (`hospital_name`, `hospital_code`, `hospital_level`, `province`, `city`, `district`, `address`, `contact_phone`, `description`) VALUES
('北京协和医院', 'BJXH001', '三级甲等', '北京市', '北京市', '东城区', '北京市东城区东单帅府园1号', '010-69156114', '国内顶级综合性医院'),
('上海瑞金医院', 'SHRJ001', '三级甲等', '上海市', '上海市', '黄浦区', '上海市黄浦区瑞金二路197号', '021-64370045', '上海著名综合性医院'),
('广州中山医院', 'GZS001', '三级甲等', '广东省', '广州市', '越秀区', '广州市越秀区东风东路658号', '020-87755766', '华南地区知名医院');

-- 创建示例科室数据
INSERT INTO `departments` (`hospital_id`, `department_name`, `department_code`, `parent_id`, `department_type`, `description`) VALUES
(1, '妇产科', 'OBGYN', 0, 'clinical', '妇产科专业诊疗'),
(1, '产科', 'OB', 1, 'clinical', '产科专业'),
(1, '妇科', 'GYN', 1, 'clinical', '妇科专业'),
(2, '妇产科', 'OBGYN', 0, 'clinical', '妇产科专业诊疗'),
(2, '产科', 'OB', 4, 'clinical', '产科专业'),
(2, '妇科', 'GYN', 4, 'clinical', '妇科专业'),
(3, '妇产科', 'OBGYN', 0, 'clinical', '妇产科专业诊疗'),
(3, '产科', 'OB', 7, 'clinical', '产科专业'),
(3, '妇科', 'GYN', 7, 'clinical', '妇科专业');
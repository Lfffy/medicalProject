-- 医疗疾病数据分析大屏可视化系统 - SQLite数据库表结构设计
-- 创建时间：2025-06-18
-- 版本：v3.0 - SQLite兼容版本
-- 说明：本设计遵循数据库规范化原则，确保数据完整性和查询效率

-- =============================================
-- 1. 用户权限管理模块
-- =============================================

-- 用户表
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  salt TEXT NOT NULL,
  real_name TEXT,
  phone TEXT,
  avatar TEXT,
  role_id INTEGER NOT NULL DEFAULT 3,
  hospital_id INTEGER,
  department_id INTEGER,
  status INTEGER NOT NULL DEFAULT 1,
  last_login_time TEXT,
  last_login_ip TEXT,
  login_count INTEGER DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TEXT
);

-- 角色表
CREATE TABLE roles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  role_name TEXT NOT NULL,
  role_code TEXT NOT NULL UNIQUE,
  description TEXT,
  level INTEGER NOT NULL DEFAULT 0,
  status INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 权限表
CREATE TABLE permissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  permission_name TEXT NOT NULL,
  permission_code TEXT NOT NULL UNIQUE,
  resource_type TEXT,
  resource_path TEXT,
  request_method TEXT,
  parent_id INTEGER NOT NULL DEFAULT 0,
  sort_order INTEGER DEFAULT 0,
  level INTEGER NOT NULL DEFAULT 1,
  status INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 角色权限关联表
CREATE TABLE role_permissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  role_id INTEGER NOT NULL,
  permission_id INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(role_id, permission_id),
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
  FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

-- =============================================
-- 2. 医院机构管理模块
-- =============================================

-- 医院信息表
CREATE TABLE hospitals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hospital_name TEXT NOT NULL,
  hospital_code TEXT NOT NULL UNIQUE,
  hospital_level TEXT,
  hospital_type TEXT,
  province_code TEXT,
  province_name TEXT,
  city_code TEXT,
  city_name TEXT,
  district_code TEXT,
  district_name TEXT,
  address TEXT,
  longitude REAL,
  latitude REAL,
  contact_phone TEXT,
  emergency_phone TEXT,
  email TEXT,
  website TEXT,
  description TEXT,
  bed_count INTEGER DEFAULT 0,
  doctor_count INTEGER DEFAULT 0,
  nurse_count INTEGER DEFAULT 0,
  established_date TEXT,
  logo_url TEXT,
  status INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TEXT
);

-- 科室信息表
CREATE TABLE departments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hospital_id INTEGER NOT NULL,
  department_name TEXT NOT NULL,
  department_code TEXT NOT NULL,
  parent_id INTEGER NOT NULL DEFAULT 0,
  department_type TEXT,
  category TEXT,
  description TEXT,
  location TEXT,
  contact_phone TEXT,
  doctor_count INTEGER DEFAULT 0,
  bed_count INTEGER DEFAULT 0,
  director_id INTEGER,
  sort_order INTEGER DEFAULT 0,
  status INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TEXT,
  UNIQUE(hospital_id, department_code),
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE
);

-- =============================================
-- 3. 患者信息管理模块
-- =============================================

-- 患者基础信息表
CREATE TABLE patients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_no TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  gender INTEGER NOT NULL,
  birth_date TEXT,
  age INTEGER,
  age_type INTEGER DEFAULT 1,
  id_card TEXT,
  phone TEXT,
  email TEXT,
  address TEXT,
  province_code TEXT,
  city_code TEXT,
  district_code TEXT,
  blood_type TEXT,
  rh_factor INTEGER,
  marital_status INTEGER,
  occupation TEXT,
  education TEXT,
  nationality TEXT DEFAULT '中国',
  ethnicity TEXT,
  emergency_contact TEXT,
  emergency_phone TEXT,
  emergency_relation TEXT,
  medical_history TEXT,
  allergy_history TEXT,
  family_history TEXT,
  insurance_type TEXT,
  insurance_no TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TEXT
);

-- =============================================
-- 4. 医疗数据管理模块
-- =============================================

-- 医疗记录表
CREATE TABLE medical_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  record_no TEXT NOT NULL UNIQUE,
  patient_id INTEGER NOT NULL,
  hospital_id INTEGER NOT NULL,
  department_id INTEGER NOT NULL,
  doctor_id INTEGER,
  visit_type INTEGER NOT NULL,
  visit_date TEXT NOT NULL,
  admission_date TEXT,
  discharge_date TEXT,
  chief_complaint TEXT,
  present_illness TEXT,
  past_history TEXT,
  physical_examination TEXT,
  auxiliary_examination TEXT,
  diagnosis TEXT,
  disease_code TEXT,
  disease_category TEXT,
  disease_severity INTEGER,
  treatment_plan TEXT,
  medication TEXT,
  surgery TEXT,
  prognosis TEXT,
  follow_up_plan TEXT,
  status INTEGER NOT NULL DEFAULT 1,
  created_by INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TEXT,
  FOREIGN KEY (patient_id) REFERENCES patients(id),
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- 生命体征表
CREATE TABLE vital_signs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  record_id INTEGER NOT NULL,
  measure_time TEXT NOT NULL,
  systolic_pressure REAL,
  diastolic_pressure REAL,
  heart_rate INTEGER,
  body_temperature REAL,
  respiratory_rate INTEGER,
  blood_oxygen REAL,
  blood_glucose REAL,
  weight REAL,
  height REAL,
  bmi REAL,
  pain_score INTEGER,
  consciousness_level INTEGER,
  pupil_left REAL,
  pupil_right REAL,
  notes TEXT,
  created_by INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (record_id) REFERENCES medical_records(id) ON DELETE CASCADE
);

-- =============================================
-- 5. 孕产妇专项管理模块
-- =============================================

-- 孕产妇信息表
CREATE TABLE maternal_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL UNIQUE,
  last_menstrual_period TEXT,
  expected_date_delivery TEXT,
  current_gestational_week INTEGER,
  parity INTEGER DEFAULT 0,
  gravidity INTEGER DEFAULT 0,
  abortion_count INTEGER DEFAULT 0,
  live_birth_count INTEGER DEFAULT 0,
  preterm_birth_count INTEGER DEFAULT 0,
  stillbirth_count INTEGER DEFAULT 0,
  ectopic_pregnancy_count INTEGER DEFAULT 0,
  previous_cesarean INTEGER DEFAULT 0,
  pregnancy_complications TEXT,
  risk_level TEXT DEFAULT '低风险',
  risk_factors TEXT,
  prenatal_care_count INTEGER DEFAULT 0,
  last_prenatal_date TEXT,
  expected_delivery_hospital TEXT,
  delivery_plan TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- 产检记录表
CREATE TABLE prenatal_examinations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  maternal_id INTEGER NOT NULL,
  examination_date TEXT NOT NULL,
  gestational_week INTEGER NOT NULL,
  hospital_id INTEGER,
  department_id INTEGER,
  doctor_id INTEGER,
  weight REAL,
  blood_pressure_systolic REAL,
  blood_pressure_diastolic REAL,
  fundal_height REAL,
  abdominal_circumference REAL,
  fetal_heart_rate REAL,
  fetal_position TEXT,
  fetal_presentation TEXT,
  edema INTEGER,
  proteinuria INTEGER,
  hemoglobin REAL,
  blood_glucose REAL,
  ultrasound_findings TEXT,
  laboratory_findings TEXT,
  diagnosis TEXT,
  treatment_plan TEXT,
  next_visit_date TEXT,
  risk_assessment TEXT,
  notes TEXT,
  created_by INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (maternal_id) REFERENCES maternal_info(id) ON DELETE CASCADE,
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- =============================================
-- 6. 系统管理模块
-- =============================================

-- 操作日志表
CREATE TABLE operation_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  username TEXT,
  operation_type TEXT NOT NULL,
  operation_module TEXT NOT NULL,
  operation_description TEXT,
  request_method TEXT,
  request_url TEXT,
  request_params TEXT,
  response_status INTEGER,
  ip_address TEXT,
  user_agent TEXT,
  execution_time INTEGER,
  status INTEGER NOT NULL DEFAULT 1,
  error_message TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 系统配置表
CREATE TABLE system_configs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  config_key TEXT NOT NULL UNIQUE,
  config_value TEXT,
  config_type TEXT DEFAULT 'string',
  description TEXT,
  is_encrypted INTEGER DEFAULT 0,
  is_public INTEGER DEFAULT 0,
  sort_order INTEGER DEFAULT 0,
  status INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 7. 数据统计分析模块
-- =============================================

-- 疾病统计表
CREATE TABLE disease_statistics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disease_code TEXT NOT NULL,
  disease_name TEXT NOT NULL,
  disease_category TEXT NOT NULL,
  statistic_date TEXT NOT NULL,
  statistic_type TEXT NOT NULL,
  total_cases INTEGER DEFAULT 0,
  new_cases INTEGER DEFAULT 0,
  cured_cases INTEGER DEFAULT 0,
  death_cases INTEGER DEFAULT 0,
  male_cases INTEGER DEFAULT 0,
  female_cases INTEGER DEFAULT 0,
  age_group_0_18 INTEGER DEFAULT 0,
  age_group_19_35 INTEGER DEFAULT 0,
  age_group_36_50 INTEGER DEFAULT 0,
  age_group_51_65 INTEGER DEFAULT 0,
  age_group_65_plus INTEGER DEFAULT 0,
  hospital_id INTEGER,
  department_id INTEGER,
  region_code TEXT,
  region_name TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- 孕产妇统计表
CREATE TABLE maternal_statistics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  statistic_date TEXT NOT NULL,
  statistic_type TEXT NOT NULL,
  total_pregnant INTEGER DEFAULT 0,
  new_pregnant INTEGER DEFAULT 0,
  delivered_count INTEGER DEFAULT 0,
  natural_delivery INTEGER DEFAULT 0,
  cesarean_delivery INTEGER DEFAULT 0,
  premature_birth INTEGER DEFAULT 0,
  low_birth_weight INTEGER DEFAULT 0,
  stillbirth INTEGER DEFAULT 0,
  maternal_death INTEGER DEFAULT 0,
  low_risk_count INTEGER DEFAULT 0,
  medium_risk_count INTEGER DEFAULT 0,
  high_risk_count INTEGER DEFAULT 0,
  prenatal_care_rate REAL DEFAULT 0,
  hospital_id INTEGER,
  region_code TEXT,
  region_name TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
);

-- =============================================
-- 初始化基础数据
-- =============================================

-- 插入角色数据
INSERT INTO roles (role_name, role_code, description, level) VALUES
('超级管理员', 'super_admin', '系统超级管理员，拥有所有权限', 1),
('管理员', 'admin', '系统管理员，拥有大部分管理权限', 2),
('医生', 'doctor', '医生用户，拥有医疗相关权限', 3),
('护士', 'nurse', '护士用户，拥有护理相关权限', 4),
('普通用户', 'user', '普通用户，拥有基本查看权限', 5);

-- 插入权限数据
INSERT INTO permissions (permission_name, permission_code, resource_type, resource_path, request_method, parent_id, level) VALUES
('系统管理', 'system_management', 'menu', '/system', 'GET', 0, 1),
('用户管理', 'user_management', 'menu', '/system/users', 'GET', 1, 2),
('角色管理', 'role_management', 'menu', '/system/roles', 'GET', 1, 2),
('权限管理', 'permission_management', 'menu', '/system/permissions', 'GET', 1, 2),
('医院管理', 'hospital_management', 'menu', '/hospital', 'GET', 0, 1),
('医院列表', 'hospital_list', 'menu', '/hospital/list', 'GET', 5, 2),
('科室管理', 'department_management', 'menu', '/hospital/departments', 'GET', 5, 2),
('患者管理', 'patient_management', 'menu', '/patient', 'GET', 0, 1),
('患者列表', 'patient_list', 'menu', '/patient/list', 'GET', 8, 2),
('医疗记录', 'medical_records', 'menu', '/patient/records', 'GET', 8, 2),
('数据分析', 'data_analysis', 'menu', '/analysis', 'GET', 0, 1),
('疾病统计', 'disease_statistics', 'menu', '/analysis/disease', 'GET', 11, 2),
('孕产妇统计', 'maternal_statistics', 'menu', '/analysis/maternal', 'GET', 11, 2);

-- 插入角色权限关联数据
INSERT INTO role_permissions (role_id, permission_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13),
(2, 1), (2, 2), (2, 3), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13),
(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13),
(4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13),
(5, 11), (5, 12), (5, 13);

-- 插入系统配置数据
INSERT INTO system_configs (config_key, config_value, config_type, description) VALUES
('system_name', '医疗疾病数据分析大屏可视化系统', 'string', '系统名称'),
('system_version', 'v3.0', 'string', '系统版本'),
('max_login_attempts', '5', 'integer', '最大登录尝试次数'),
('session_timeout', '30', 'integer', '会话超时时间（分钟）'),
('password_min_length', '8', 'integer', '密码最小长度'),
('data_retention_days', '365', 'integer', '数据保留天数'),
('enable_email_notification', 'true', 'boolean', '是否启用邮件通知'),
('backup_frequency', 'daily', 'string', '备份频率'),
('max_upload_size', '10', 'integer', '最大上传文件大小（MB）'),
('default_page_size', '20', 'integer', '默认分页大小');

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_users_hospital_id ON users(hospital_id);
CREATE INDEX idx_users_department_id ON users(department_id);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created_at ON users(created_at);

CREATE INDEX idx_patients_patient_no ON patients(patient_no);
CREATE INDEX idx_patients_name ON patients(name);
CREATE INDEX idx_patients_id_card ON patients(id_card);
CREATE INDEX idx_patients_phone ON patients(phone);
CREATE INDEX idx_patients_gender ON patients(gender);
CREATE INDEX idx_patients_created_at ON patients(created_at);

CREATE INDEX idx_medical_records_record_no ON medical_records(record_no);
CREATE INDEX idx_medical_records_patient_id ON medical_records(patient_id);
CREATE INDEX idx_medical_records_hospital_id ON medical_records(hospital_id);
CREATE INDEX idx_medical_records_department_id ON medical_records(department_id);
CREATE INDEX idx_medical_records_visit_type ON medical_records(visit_type);
CREATE INDEX idx_medical_records_visit_date ON medical_records(visit_date);
CREATE INDEX idx_medical_records_disease_category ON medical_records(disease_category);
CREATE INDEX idx_medical_records_created_at ON medical_records(created_at);

CREATE INDEX idx_vital_signs_record_id ON vital_signs(record_id);
CREATE INDEX idx_vital_signs_measure_time ON vital_signs(measure_time);
CREATE INDEX idx_vital_signs_created_at ON vital_signs(created_at);

CREATE INDEX idx_maternal_info_patient_id ON maternal_info(patient_id);
CREATE INDEX idx_maternal_info_risk_level ON maternal_info(risk_level);
CREATE INDEX idx_maternal_info_created_at ON maternal_info(created_at);

CREATE INDEX idx_prenatal_examinations_maternal_id ON prenatal_examinations(maternal_id);
CREATE INDEX idx_prenatal_examinations_examination_date ON prenatal_examinations(examination_date);
CREATE INDEX idx_prenatal_examinations_gestational_week ON prenatal_examinations(gestational_week);
CREATE INDEX idx_prenatal_examinations_created_at ON prenatal_examinations(created_at);

CREATE INDEX idx_operation_logs_user_id ON operation_logs(user_id);
CREATE INDEX idx_operation_logs_operation_type ON operation_logs(operation_type);
CREATE INDEX idx_operation_logs_operation_module ON operation_logs(operation_module);
CREATE INDEX idx_operation_logs_created_at ON operation_logs(created_at);

CREATE INDEX idx_disease_statistics_disease_code ON disease_statistics(disease_code);
CREATE INDEX idx_disease_statistics_disease_category ON disease_statistics(disease_category);
CREATE INDEX idx_disease_statistics_statistic_date ON disease_statistics(statistic_date);
CREATE INDEX idx_disease_statistics_statistic_type ON disease_statistics(statistic_type);
CREATE INDEX idx_disease_statistics_hospital_id ON disease_statistics(hospital_id);

CREATE INDEX idx_maternal_statistics_statistic_date ON maternal_statistics(statistic_date);
CREATE INDEX idx_maternal_statistics_statistic_type ON maternal_statistics(statistic_type);
CREATE INDEX idx_maternal_statistics_hospital_id ON maternal_statistics(hospital_id);
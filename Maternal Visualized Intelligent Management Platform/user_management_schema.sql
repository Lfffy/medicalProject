-- 用户管理系统数据库表结构

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码哈希',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    full_name VARCHAR(100) NOT NULL COMMENT '真实姓名',
    phone VARCHAR(20) COMMENT '电话号码',
    role ENUM('admin', 'manager', 'doctor', 'user') DEFAULT 'user' COMMENT '角色',
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active' COMMENT '状态',
    avatar VARCHAR(255) COMMENT '头像URL',
    last_login TIMESTAMP NULL COMMENT '最后登录时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 创建权限表
CREATE TABLE IF NOT EXISTS permissions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '权限ID',
    name VARCHAR(100) UNIQUE NOT NULL COMMENT '权限名称',
    description TEXT COMMENT '权限描述',
    category VARCHAR(50) NOT NULL COMMENT '权限分类',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- 创建用户权限关联表
CREATE TABLE IF NOT EXISTS user_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关联ID',
    user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
    permission_id INT NOT NULL COMMENT '权限ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_permission (user_id, permission_id),
    INDEX idx_user_id (user_id),
    INDEX idx_permission_id (permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户权限关联表';

-- 创建角色权限关联表
CREATE TABLE IF NOT EXISTS role_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关联ID',
    role_name VARCHAR(50) NOT NULL COMMENT '角色名称',
    permission_id INT NOT NULL COMMENT '权限ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_permission (role_name, permission_id),
    INDEX idx_role_name (role_name),
    INDEX idx_permission_id (permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- 创建操作日志表
CREATE TABLE IF NOT EXISTS operation_logs (
    id VARCHAR(36) PRIMARY KEY COMMENT '日志ID',
    user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    action VARCHAR(100) NOT NULL COMMENT '操作动作',
    module VARCHAR(50) NOT NULL COMMENT '操作模块',
    details JSON COMMENT '操作详情',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_username (username),
    INDEX idx_action (action),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- 插入基础权限数据
INSERT IGNORE INTO permissions (name, description, category) VALUES
-- 用户管理权限
('user_view', '查看用户信息', '用户管理'),
('user_create', '创建用户', '用户管理'),
('user_edit', '编辑用户信息', '用户管理'),
('user_delete', '删除用户', '用户管理'),
('user_manage_status', '管理用户状态', '用户管理'),

-- 权限管理权限
('permission_view', '查看权限信息', '权限管理'),
('permission_create', '创建权限', '权限管理'),
('permission_edit', '编辑权限', '权限管理'),
('permission_delete', '删除权限', '权限管理'),
('permission_assign', '分配权限', '权限管理'),

-- 数据管理权限
('data_view', '查看数据', '数据管理'),
('data_create', '创建数据', '数据管理'),
('data_edit', '编辑数据', '数据管理'),
('data_delete', '删除数据', '数据管理'),
('data_import', '导入数据', '数据管理'),
('data_export', '导出数据', '数据管理'),

-- 分析管理权限
('analysis_view', '查看分析结果', '分析管理'),
('analysis_create', '创建分析', '分析管理'),
('analysis_edit', '编辑分析', '分析管理'),
('analysis_delete', '删除分析', '分析管理'),
('analysis_advanced', '高级分析功能', '分析管理'),

-- 系统管理权限
('system_config', '系统配置管理', '系统管理'),
('system_logs', '查看系统日志', '系统管理'),
('system_backup', '系统备份', '系统管理'),
('system_monitor', '系统监控', '系统管理'),

-- 医院管理权限
('hospital_view', '查看医院信息', '医院管理'),
('hospital_create', '创建医院', '医院管理'),
('hospital_edit', '编辑医院信息', '医院管理'),
('hospital_delete', '删除医院', '医院管理'),

-- 科室管理权限
('department_view', '查看科室信息', '科室管理'),
('department_create', '创建科室', '科室管理'),
('department_edit', '编辑科室信息', '科室管理'),
('department_delete', '删除科室', '科室管理'),

-- 医生管理权限
('doctor_view', '查看医生信息', '医生管理'),
('doctor_create', '创建医生', '医生管理'),
('doctor_edit', '编辑医生信息', '医生管理'),
('doctor_delete', '删除医生', '医生管理'),

-- 排班管理权限
('schedule_view', '查看排班信息', '排班管理'),
('schedule_create', '创建排班', '排班管理'),
('schedule_edit', '编辑排班信息', '排班管理'),
('schedule_delete', '删除排班', '排班管理');

-- 为角色分配默认权限
INSERT IGNORE INTO role_permissions (role_name, permission_id) 
SELECT 'admin', id FROM permissions;

INSERT IGNORE INTO role_permissions (role_name, permission_id) 
SELECT 'manager', id FROM permissions 
WHERE category IN ('用户管理', '数据管理', '分析管理', '医院管理', '科室管理', '医生管理', '排班管理');

INSERT IGNORE INTO role_permissions (role_name, permission_id) 
SELECT 'doctor', id FROM permissions 
WHERE name IN ('data_view', 'analysis_view', 'analysis_create', 'hospital_view', 'department_view', 'doctor_view', 'schedule_view');

INSERT IGNORE INTO role_permissions (role_name, permission_id) 
SELECT 'user', id FROM permissions 
WHERE name IN ('data_view', 'analysis_view');

-- 创建默认管理员用户
INSERT IGNORE INTO users (id, username, password, email, full_name, role, status) 
VALUES (
    UUID(),
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e', -- 密码: admin123
    'admin@medical.com',
    '系统管理员',
    'admin',
    'active'
);

-- 创建默认经理用户
INSERT IGNORE INTO users (id, username, password, email, full_name, role, status) 
VALUES (
    UUID(),
    'manager',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e', -- 密码: admin123
    'manager@medical.com',
    '系统经理',
    'manager',
    'active'
);

-- 创建默认医生用户
INSERT IGNORE INTO users (id, username, password, email, full_name, role, status) 
VALUES (
    UUID(),
    'doctor',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e', -- 密码: admin123
    'doctor@medical.com',
    '医生',
    'doctor',
    'active'
);

-- 创建默认普通用户
INSERT IGNORE INTO users (id, username, password, email, full_name, role, status) 
VALUES (
    UUID(),
    'user',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e', -- 密码: admin123
    'user@medical.com',
    '普通用户',
    'user',
    'active'
);
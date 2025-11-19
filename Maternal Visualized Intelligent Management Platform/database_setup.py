#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗疾病数据分析大屏可视化系统 - 数据插入和验证脚本
创建时间：2025-06-18
功能：执行数据库初始化、数据插入和验证
"""

import sqlite3
import os
import sys
import logging
from datetime import datetime, timedelta
import random
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_setup.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, db_path="medical_system.db"):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """连接数据库"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # 使结果可以按列名访问
            logger.info(f"成功连接数据库：{self.db_path}")
            return True
        except Exception as e:
            logger.error(f"连接数据库失败：{e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已关闭")
    
    def execute_script(self, script_file):
        """执行SQL脚本文件"""
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                script = f.read()
            
            # 移除MySQL特有的语法，转换为SQLite兼容语法
            script = self._convert_mysql_to_sqlite(script)
            
            cursor = self.connection.cursor()
            cursor.executescript(script)
            self.connection.commit()
            logger.info(f"成功执行SQL脚本：{script_file}")
            return True
        except Exception as e:
            logger.error(f"执行SQL脚本失败：{e}")
            return False
    
    def _convert_mysql_to_sqlite(self, script):
        """将MySQL语法转换为SQLite兼容语法"""
        # 移除MySQL特有的语法
        replacements = [
            ('ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci', ''),
            ('ENGINE=InnoDB DEFAULT CHARSET=utf8mb4', ''),
            ('UNSIGNED', ''),
            ('AUTO_INCREMENT', 'AUTOINCREMENT'),
            ('BIGINT', 'INTEGER'),
            ('TINYINT', 'INTEGER'),
            ('SMALLINT', 'INTEGER'),
            ('DECIMAL', 'REAL'),
            ('TEXT DEFAULT NULL', 'TEXT'),
            ('VARCHAR', 'TEXT'),
            ('DATETIME', 'TEXT'),
            ('DATE', 'TEXT'),
            ('TIME', 'TEXT'),
            ('TIMESTAMP', 'TEXT'),
            ('SET FOREIGN_KEY_CHECKS = 0', ''),
            ('SET FOREIGN_KEY_CHECKS = 1', ''),
            ('DELIMITER $$', ''),
            ('DELIMITER ;', ''),
            ('BEGIN', ''),
            ('COMMIT', ''),
            ('END$$', ''),
            ('END', ''),
            ('START TRANSACTION', ''),
            ('ROLLBACK', ''),
            ('DECLARE EXIT HANDLER FOR SQLEXCEPTION', ''),
            ('BEGIN', ''),
            ('RESIGNAL', ''),
            ('IF 1=1 THEN', ''),
            ('END IF', ''),
            ('IF EXISTS', ''),
            ('DROP PROCEDURE IF EXISTS', ''),
            ('CREATE PROCEDURE', '-- CREATE PROCEDURE'),
            ('CREATE TRIGGER', '-- CREATE TRIGGER'),
            ('CREATE VIEW', '-- CREATE VIEW'),
        ]
        
        for old, new in replacements:
            script = script.replace(old, new)
        
        return script
    
    def execute_query(self, query, params=None):
        """执行查询语句"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"执行查询失败：{e}")
            return None
    
    def verify_data_integrity(self):
        """验证数据完整性"""
        logger.info("开始验证数据完整性...")
        
        verification_results = {}
        
        # 验证表是否存在
        tables_to_check = [
            'users', 'hospitals', 'departments', 'patients', 
            'medical_records', 'vital_signs', 'maternal_info', 
            'prenatal_examinations', 'operation_logs',
            'disease_statistics', 'maternal_statistics', 'system_configs'
        ]
        
        existing_tables = []
        for table in tables_to_check:
            result = self.execute_query(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if result:
                existing_tables.append(table)
                count = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")[0]['count']
                verification_results[table] = count
                logger.info(f"表 {table} 存在，记录数：{count}")
            else:
                logger.warning(f"表 {table} 不存在")
        
        verification_results['existing_tables'] = existing_tables
        verification_results['total_tables'] = len(existing_tables)
        
        # 验证数据关系
        self._verify_foreign_keys(verification_results)
        
        # 验证数据质量
        self._verify_data_quality(verification_results)
        
        return verification_results
    
    def _verify_foreign_keys(self, results):
        """验证外键关系"""
        logger.info("验证外键关系...")
        
        # 验证医疗记录的patient_id是否存在
        query = """
        SELECT COUNT(*) as invalid_count 
        FROM medical_records mr 
        LEFT JOIN patients p ON mr.patient_id = p.id 
        WHERE p.id IS NULL
        """
        result = self.execute_query(query)
        if result:
            results['invalid_medical_records'] = result[0]['invalid_count']
        
        # 验证生命体征的record_id是否存在
        query = """
        SELECT COUNT(*) as invalid_count 
        FROM vital_signs vs 
        LEFT JOIN medical_records mr ON vs.record_id = mr.id 
        WHERE mr.id IS NULL
        """
        result = self.execute_query(query)
        if result:
            results['invalid_vital_signs'] = result[0]['invalid_count']
        
        # 验证孕产妇信息的patient_id是否存在
        query = """
        SELECT COUNT(*) as invalid_count 
        FROM maternal_info mi 
        LEFT JOIN patients p ON mi.patient_id = p.id 
        WHERE p.id IS NULL
        """
        result = self.execute_query(query)
        if result:
            results['invalid_maternal_info'] = result[0]['invalid_count']
    
    def _verify_data_quality(self, results):
        """验证数据质量"""
        logger.info("验证数据质量...")
        
        # 验证必填字段
        quality_checks = []
        
        # 检查患者信息完整性
        query = """
        SELECT COUNT(*) as incomplete_count 
        FROM patients 
        WHERE name IS NULL OR name = '' OR gender IS NULL
        """
        result = self.execute_query(query)
        if result:
            quality_checks.append(f"患者信息不完整记录数：{result[0]['incomplete_count']}")
        
        # 检查医疗记录完整性
        query = """
        SELECT COUNT(*) as incomplete_count 
        FROM medical_records 
        WHERE patient_id IS NULL OR hospital_id IS NULL OR department_id IS NULL
        """
        result = self.execute_query(query)
        if result:
            quality_checks.append(f"医疗记录信息不完整记录数：{result[0]['incomplete_count']}")
        
        # 检查生命体征数据合理性
        query = """
        SELECT COUNT(*) as abnormal_count 
        FROM vital_signs 
        WHERE systolic_pressure < 60 OR systolic_pressure > 250 
        OR diastolic_pressure < 30 OR diastolic_pressure > 150
        OR heart_rate < 30 OR heart_rate > 200
        OR body_temperature < 35 OR body_temperature > 42
        """
        result = self.execute_query(query)
        if result:
            quality_checks.append(f"生命体征异常记录数：{result[0]['abnormal_count']}")
        
        results['data_quality_checks'] = quality_checks
    
    def generate_sample_reports(self):
        """生成示例报告"""
        logger.info("生成示例报告...")
        
        reports = {}
        
        # 患者统计报告
        query = """
        SELECT 
            COUNT(*) as total_patients,
            COUNT(CASE WHEN gender = 1 THEN 1 END) as male_patients,
            COUNT(CASE WHEN gender = 2 THEN 1 END) as female_patients,
            AVG(age) as avg_age,
            MIN(age) as min_age,
            MAX(age) as max_age
        FROM patients
        """
        result = self.execute_query(query)
        if result:
            reports['patient_statistics'] = result[0]
        
        # 医疗记录统计报告
        query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(CASE WHEN visit_type = 1 THEN 1 END) as outpatient_records,
            COUNT(CASE WHEN visit_type = 2 THEN 1 END) as emergency_records,
            COUNT(CASE WHEN visit_type = 3 THEN 1 END) as inpatient_records,
            COUNT(DISTINCT patient_id) as unique_patients
        FROM medical_records
        """
        result = self.execute_query(query)
        if result:
            reports['medical_record_statistics'] = result[0]
        
        # 疾病分布报告
        query = """
        SELECT 
            disease_category,
            COUNT(*) as case_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM medical_records), 2) as percentage
        FROM medical_records 
        WHERE disease_category IS NOT NULL
        GROUP BY disease_category
        ORDER BY case_count DESC
        """
        result = self.execute_query(query)
        if result:
            reports['disease_distribution'] = result
        
        # 孕产妇统计报告
        query = """
        SELECT 
            COUNT(*) as total_pregnant,
            COUNT(CASE WHEN risk_level = '低风险' THEN 1 END) as low_risk,
            COUNT(CASE WHEN risk_level = '中风险' THEN 1 END) as medium_risk,
            COUNT(CASE WHEN risk_level = '高风险' THEN 1 END) as high_risk,
            AVG(current_gestational_week) as avg_gestational_week
        FROM maternal_info
        """
        result = self.execute_query(query)
        if result:
            reports['maternal_statistics'] = result[0]
        
        return reports
    
    def export_data_summary(self, filename="data_summary.json"):
        """导出数据摘要"""
        summary = {
            'export_time': datetime.now().isoformat(),
            'database_path': self.db_path,
            'data_integrity': self.verify_data_integrity(),
            'sample_reports': self.generate_sample_reports()
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            logger.info(f"数据摘要已导出到：{filename}")
            return True
        except Exception as e:
            logger.error(f"导出数据摘要失败：{e}")
            return False

def main():
    """主函数"""
    logger.info("开始数据库初始化和数据插入...")
    
    # 初始化数据库管理器
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        logger.error("无法连接数据库，程序退出")
        return False
    
    try:
        # 1. 创建数据库表结构
        logger.info("步骤1：创建数据库表结构...")
        schema_file = "sqlite_database_schema.sql"
        if os.path.exists(schema_file):
            if db_manager.execute_script(schema_file):
                logger.info("数据库表结构创建成功")
            else:
                logger.error("数据库表结构创建失败")
                return False
        else:
            logger.error(f"数据库表结构文件不存在：{schema_file}")
            return False
        
        # 2. 插入测试数据
        logger.info("步骤2：插入测试数据...")
        data_file = "sqlite_test_data_simple.sql"
        if os.path.exists(data_file):
            if db_manager.execute_script(data_file):
                logger.info("测试数据插入成功")
            else:
                logger.error("测试数据插入失败")
                return False
        else:
            logger.error(f"测试数据文件不存在：{data_file}")
            return False
        
        # 3. 验证数据完整性
        logger.info("步骤3：验证数据完整性...")
        verification_results = db_manager.verify_data_integrity()
        
        # 4. 生成示例报告
        logger.info("步骤4：生成示例报告...")
        reports = db_manager.generate_sample_reports()
        
        # 5. 导出数据摘要
        logger.info("步骤5：导出数据摘要...")
        db_manager.export_data_summary()
        
        # 打印验证结果
        logger.info("=" * 50)
        logger.info("数据验证结果摘要：")
        logger.info(f"总表数：{verification_results.get('total_tables', 0)}")
        logger.info(f"存在的表：{', '.join(verification_results.get('existing_tables', []))}")
        
        for table, count in verification_results.items():
            if isinstance(count, int) and table != 'total_tables' and table != 'existing_tables':
                logger.info(f"表 {table}：{count} 条记录")
        
        if 'data_quality_checks' in verification_results:
            logger.info("数据质量检查结果：")
            for check in verification_results['data_quality_checks']:
                logger.info(f"  - {check}")
        
        logger.info("=" * 50)
        logger.info("示例报告：")
        
        if 'patient_statistics' in reports:
            stats = reports['patient_statistics']
            logger.info(f"患者统计：总数 {stats['total_patients']}，男性 {stats['male_patients']}，女性 {stats['female_patients']}")
        
        if 'medical_record_statistics' in reports:
            stats = reports['medical_record_statistics']
            logger.info(f"医疗记录统计：总数 {stats['total_records']}，门诊 {stats['outpatient_records']}，急诊 {stats['emergency_records']}，住院 {stats['inpatient_records']}")
        
        if 'disease_distribution' in reports:
            logger.info("疾病分布：")
            for disease in reports['disease_distribution']:
                logger.info(f"  - {disease['disease_category']}：{disease['case_count']} 例 ({disease['percentage']}%)")
        
        if 'maternal_statistics' in reports:
            stats = reports['maternal_statistics']
            logger.info(f"孕产妇统计：总数 {stats['total_pregnant']}，低风险 {stats['low_risk']}，中风险 {stats['medium_risk']}，高风险 {stats['high_risk']}")
        
        logger.info("=" * 50)
        logger.info("数据库初始化和数据插入完成！")
        
        return True
        
    except Exception as e:
        logger.error(f"数据库初始化过程中发生错误：{e}")
        return False
    
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
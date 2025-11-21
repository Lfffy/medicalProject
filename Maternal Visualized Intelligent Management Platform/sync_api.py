#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗疾病数据分析系统 - 数据同步API服务
创建时间：2025-06-18
功能：提供数据同步的HTTP API接口
"""

from flask import Flask, request, jsonify, Blueprint
import sqlite3
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import time
from realtime_data_updater import RealtimeDataUpdater, DatabaseConfig

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建同步API蓝图
sync_bp = Blueprint('sync', __name__, url_prefix='/api/sync')

# 全局变量
updater_instance = None
sync_status = {
    "is_running": False,
    "last_sync": None,
    "total_syncs": 0,
    "failed_syncs": 0,
    "sync_history": []
}

def get_updater_instance():
    """获取更新器实例"""
    global updater_instance
    if updater_instance is None:
        config = DatabaseConfig()
        updater_instance = RealtimeDataUpdater(config)
    return updater_instance

def get_db_connection():
    """获取数据库连接"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'medical_analysis.db')
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        raise

@sync_bp.route('/status', methods=['GET'])
def get_sync_status():
    """获取同步状态"""
    try:
        updater = get_updater_instance()
        status = updater.get_status()
        
        # 添加额外的状态信息
        status.update({
            "sync_service_status": sync_status,
            "database_info": get_database_info()
        })
        
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        logger.error(f"获取同步状态失败: {e}")
        return jsonify({
            'success': False,
            'message': f'获取同步状态失败: {str(e)}'
        }), 500

@sync_bp.route('/start', methods=['POST'])
def start_sync_service():
    """启动同步服务"""
    try:
        updater = get_updater_instance()
        
        if updater.is_running:
            return jsonify({
                'success': False,
                'message': '同步服务已在运行'
            }), 400
        
        # 注册回调函数
        updater.register_callback('update_success', on_sync_success)
        updater.register_callback('update_failed', on_sync_failed)
        
        # 启动服务
        updater.start()
        
        sync_status['is_running'] = True
        sync_status['last_sync'] = datetime.now().isoformat()
        
        logger.info("同步服务启动成功")
        
        return jsonify({
            'success': True,
            'message': '同步服务启动成功',
            'data': {
                'start_time': sync_status['last_sync']
            }
        })
    except Exception as e:
        logger.error(f"启动同步服务失败: {e}")
        return jsonify({
            'success': False,
            'message': f'启动同步服务失败: {str(e)}'
        }), 500

@sync_bp.route('/stop', methods=['POST'])
def stop_sync_service():
    """停止同步服务"""
    try:
        updater = get_updater_instance()
        
        if not updater.is_running:
            return jsonify({
                'success': False,
                'message': '同步服务未在运行'
            }), 400
        
        updater.stop()
        sync_status['is_running'] = False
        
        logger.info("同步服务停止成功")
        
        return jsonify({
            'success': True,
            'message': '同步服务停止成功'
        })
    except Exception as e:
        logger.error(f"停止同步服务失败: {e}")
        return jsonify({
            'success': False,
            'message': f'停止同步服务失败: {str(e)}'
        }), 500

@sync_bp.route('/trigger', methods=['POST'])
def trigger_manual_sync():
    """手动触发同步"""
    try:
        data = request.get_json() or {}
        source_name = data.get('source_name', 'all')
        
        updater = get_updater_instance()
        
        if not updater.is_running:
            return jsonify({
                'success': False,
                'message': '同步服务未运行，请先启动服务'
            }), 400
        
        if source_name == 'all':
            # 触发所有数据源的同步
            for source_name in updater.data_sources.keys():
                updater._update_data_source(source_name)
            
            message = '已触发所有数据源的同步'
        else:
            # 触发指定数据源的同步
            if source_name not in updater.data_sources:
                return jsonify({
                    'success': False,
                    'message': f'未知数据源: {source_name}'
                }), 400
            
            updater._update_data_source(source_name)
            message = f'已触发数据源 {source_name} 的同步'
        
        return jsonify({
            'success': True,
            'message': message,
            'data': {
                'trigger_time': datetime.now().isoformat(),
                'source_name': source_name
            }
        })
    except Exception as e:
        logger.error(f"手动触发同步失败: {e}")
        return jsonify({
            'success': False,
            'message': f'手动触发同步失败: {str(e)}'
        }), 500

@sync_bp.route('/config', methods=['GET'])
def get_sync_config():
    """获取同步配置"""
    try:
        config = DatabaseConfig()
        return jsonify({
            'success': True,
            'data': config.config
        })
    except Exception as e:
        logger.error(f"获取同步配置失败: {e}")
        return jsonify({
            'success': False,
            'message': f'获取同步配置失败: {str(e)}'
        }), 500

@sync_bp.route('/config', methods=['PUT'])
def update_sync_config():
    """更新同步配置"""
    try:
        new_config = request.get_json()
        
        if not new_config:
            return jsonify({
                'success': False,
                'message': '请提供有效的配置数据'
            }), 400
        
        config = DatabaseConfig()
        
        # 更新配置
        for key, value in new_config.items():
            if key in config.config:
                config.config[key] = value
        
        # 保存配置
        config._save_config(config.config)
        
        # 如果服务正在运行，需要重启以应用新配置
        updater = get_updater_instance()
        was_running = updater.is_running
        
        if was_running:
            updater.stop()
            time.sleep(2)
        
        # 重新初始化更新器
        global updater_instance
        updater_instance = None
        updater = get_updater_instance()
        
        if was_running:
            updater.start()
        
        return jsonify({
            'success': True,
            'message': '配置更新成功',
            'data': {
                'config': config.config,
                'service_restarted': was_running
            }
        })
    except Exception as e:
        logger.error(f"更新同步配置失败: {e}")
        return jsonify({
            'success': False,
            'message': f'更新同步配置失败: {str(e)}'
        }), 500

@sync_bp.route('/history', methods=['GET'])
def get_sync_history():
    """获取同步历史"""
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        source = request.args.get('source', '')
        status_filter = request.args.get('status', '')
        
        # 这里可以从数据库或日志文件中读取同步历史
        # 暂时返回内存中的历史记录
        history = sync_status['sync_history']
        
        # 过滤
        if source:
            history = [h for h in history if h.get('source') == source]
        
        if status_filter:
            history = [h for h in history if h.get('status') == status_filter]
        
        # 分页
        total = len(history)
        start = (page - 1) * size
        end = start + size
        paginated_history = history[start:end]
        
        return jsonify({
            'success': True,
            'data': {
                'history': paginated_history,
                'pagination': {
                    'page': page,
                    'size': size,
                    'total': total,
                    'pages': (total + size - 1) // size
                }
            }
        })
    except Exception as e:
        logger.error(f"获取同步历史失败: {e}")
        return jsonify({
            'success': False,
            'message': f'获取同步历史失败: {str(e)}'
        }), 500

@sync_bp.route('/backup', methods=['POST'])
def create_backup():
    """创建数据库备份"""
    try:
        import shutil
        from datetime import datetime
        
        config = DatabaseConfig()
        db_path = config.config["main_database"]["path"]
        backup_path = config.config["main_database"]["backup_path"]
        
        # 创建带时间戳的备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{timestamp}.db"
        backup_full_path = os.path.join(os.path.dirname(db_path), backup_file)
        
        # 复制数据库文件
        shutil.copy2(db_path, backup_full_path)
        
        logger.info(f"数据库备份创建成功: {backup_full_path}")
        
        return jsonify({
            'success': True,
            'message': '数据库备份创建成功',
            'data': {
                'backup_file': backup_file,
                'backup_path': backup_full_path,
                'backup_time': datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"创建数据库备份失败: {e}")
        return jsonify({
            'success': False,
            'message': f'创建数据库备份失败: {str(e)}'
        }), 500

@sync_bp.route('/validate', methods=['POST'])
def validate_data_integrity():
    """验证数据完整性"""
    try:
        updater = get_updater_instance()
        
        if not updater.db_manager.connect():
            return jsonify({
                'success': False,
                'message': '无法连接到数据库'
            }), 500
        
        try:
            # 执行数据完整性检查
            validation_results = {
                'tables_checked': [],
                'issues_found': [],
                'statistics': {}
            }
            
            # 检查主要表的记录数
            tables_to_check = [
                'patients', 'medical_records', 'vital_signs', 
                'maternal_info', 'hospitals', 'departments'
            ]
            
            total_records = 0
            for table in tables_to_check:
                try:
                    query = f"SELECT COUNT(*) as count FROM {table}"
                    result = updater.db_manager.execute_query(query)
                    count = result[0]['count'] if result else 0
                    
                    validation_results['tables_checked'].append({
                        'table': table,
                        'record_count': count
                    })
                    
                    total_records += count
                    
                except Exception as e:
                    validation_results['issues_found'].append({
                        'table': table,
                        'issue': f'无法查询表记录数: {str(e)}'
                    })
            
            validation_results['statistics']['total_records'] = total_records
            
            # 检查外键完整性
            foreign_key_checks = [
                {
                    'query': '''
                        SELECT COUNT(*) as count 
                        FROM medical_records mr 
                        LEFT JOIN patients p ON mr.patient_id = p.id 
                        WHERE p.id IS NULL
                    ''',
                    'description': '医疗记录中无效的患者ID'
                },
                {
                    'query': '''
                        SELECT COUNT(*) as count 
                        FROM vital_signs vs 
                        LEFT JOIN medical_records mr ON vs.record_id = mr.id 
                        WHERE mr.id IS NULL
                    ''',
                    'description': '生命体征中无效的医疗记录ID'
                }
            ]
            
            for check in foreign_key_checks:
                try:
                    result = updater.db_manager.execute_query(check['query'])
                    count = result[0]['count'] if result else 0
                    
                    if count > 0:
                        validation_results['issues_found'].append({
                            'type': 'foreign_key_violation',
                            'description': check['description'],
                            'count': count
                        })
                except Exception as e:
                    validation_results['issues_found'].append({
                        'type': 'validation_error',
                        'description': f'外键检查失败: {str(e)}'
                    })
            
            # 计算完整性评分
            total_issues = len(validation_results['issues_found'])
            if total_issues == 0:
                integrity_score = 100
            else:
                integrity_score = max(0, 100 - (total_issues * 10))
            
            validation_results['integrity_score'] = integrity_score
            validation_results['validation_time'] = datetime.now().isoformat()
            
            return jsonify({
                'success': True,
                'message': f'数据完整性验证完成，评分: {integrity_score}',
                'data': validation_results
            })
            
        finally:
            updater.db_manager.disconnect()
            
    except Exception as e:
        logger.error(f"验证数据完整性失败: {e}")
        return jsonify({
            'success': False,
            'message': f'验证数据完整性失败: {str(e)}'
        }), 500

def on_sync_success(data):
    """同步成功回调"""
    sync_status['total_syncs'] += 1
    sync_status['last_sync'] = datetime.now().isoformat()
    
    # 添加到历史记录
    sync_history_entry = {
        'timestamp': datetime.now().isoformat(),
        'source': data.get('source'),
        'status': 'success',
        'message': f"数据源 {data.get('source')} 同步成功"
    }
    sync_status['sync_history'].insert(0, sync_history_entry)
    
    # 保持历史记录在合理范围内
    if len(sync_status['sync_history']) > 100:
        sync_status['sync_history'] = sync_status['sync_history'][:100]
    
    logger.info(f"同步成功: {data}")

def on_sync_failed(data):
    """同步失败回调"""
    sync_status['failed_syncs'] += 1
    
    # 添加到历史记录
    sync_history_entry = {
        'timestamp': datetime.now().isoformat(),
        'source': data.get('source'),
        'status': 'failed',
        'message': f"数据源 {data.get('source')} 同步失败: {data.get('error', '未知错误')}",
        'retry_count': data.get('retry_count', 0)
    }
    sync_status['sync_history'].insert(0, sync_history_entry)
    
    # 保持历史记录在合理范围内
    if len(sync_status['sync_history']) > 100:
        sync_status['sync_history'] = sync_status['sync_history'][:100]
    
    logger.error(f"同步失败: {data}")

def get_database_info():
    """获取数据库信息"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 获取数据库文件大小
        db_path = os.path.join(os.path.dirname(__file__), 'medical_analysis.db')
        file_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        
        # 获取表信息
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        connection.close()
        
        return {
            'file_path': db_path,
            'file_size': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'table_count': len(tables),
            'tables': tables
        }
    except Exception as e:
        logger.error(f"获取数据库信息失败: {e}")
        return {
            'error': str(e)
        }

# 注册蓝图到主应用的函数
def register_sync_api(app):
    """注册同步API到主应用"""
    app.register_blueprint(sync_bp)
    logger.info("数据同步API已注册")

if __name__ == "__main__":
    # 测试API
    app = Flask(__name__)
    register_sync_api(app)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
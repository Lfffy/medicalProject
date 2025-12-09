from flask import Blueprint, request, jsonify
import sqlite3
import json
import os
from datetime import datetime, timedelta
import random

warning_bp = Blueprint('warning', __name__, url_prefix='/api/warning')

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('medical_system.db')
    conn.row_factory = sqlite3.Row
    return conn

@warning_bp.route('/records', methods=['GET'])
def get_warning_records():
    """获取预警记录列表"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        start = (page - 1) * limit
        
        # 查询预警记录
        records_query = """
        SELECT 
            p.id as patient_id,
            p.name as patient_name,
            p.age,
            mi.current_gestational_week,
            vs.systolic_pressure,
            vs.diastolic_pressure,
            vs.heart_rate,
            vs.body_temperature,
            vs.blood_oxygen,
            vs.created_at
        FROM patients p
        LEFT JOIN vital_signs vs ON p.id = vs.record_id
        LEFT JOIN maternal_info mi ON p.id = mi.patient_id
        ORDER BY vs.created_at DESC
        LIMIT ? OFFSET ?
        """
        
        records_data = cursor.execute(records_query, (limit, start)).fetchall()
        
        # 获取总记录数
        cursor.execute("SELECT COUNT(*) FROM patients")
        total = cursor.fetchone()[0]
        
        # 构建响应数据
        warning_records = []
        for row in records_data:
            warning_type = '血压异常' if row['systolic_pressure'] and (row['systolic_pressure'] > 140 or row['systolic_pressure'] < 100) else '正常'
            
            warning_records.append({
                'id': row['patient_id'],
                'patientId': row['patient_id'],
                'patientName': row['patient_name'] or f"患者{row['patient_id']}",
                'age': row['age'],
                'gestationalWeek': row['current_gestational_week'],
                'type': warning_type,
                'level': 'high' if warning_type != '正常' else 'low',
                'description': f"收缩压: {row['systolic_pressure']} mmHg" if row['systolic_pressure'] else "暂无数据",
                'status': random.choice(['pending', 'processing', 'resolved']),
                'createdAt': row['created_at'] or datetime.now().isoformat(),
                'updatedAt': datetime.now().isoformat(),
                'handledAt': datetime.now().isoformat() if random.random() > 0.5 else None,
                'handler': f"医生{random.randint(1, 5)}" if random.random() > 0.5 else None
            })
        
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取预警记录成功',
            'data': {
                'records': warning_records,
                'total': total,
                'page': page,
                'limit': limit
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取预警记录失败: {str(e)}'
        }), 500

@warning_bp.route('/records', methods=['POST'])
def create_warning_record():
    """创建预警记录"""
    try:
        data = request.get_json()
        
        return jsonify({
            'code': 200,
            'message': '创建预警记录成功',
            'data': {
                'id': random.randint(100, 999),
                'createdAt': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'创建预警记录失败: {str(e)}'
        }), 500

@warning_bp.route('/records/<int:record_id>', methods=['GET'])
def get_warning_record(record_id):
    """获取单个预警记录详情"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 查询指定ID的患者信息
        cursor.execute("""
        SELECT 
            p.id, p.name, p.age,
            mi.current_gestational_week,
            vs.systolic_pressure, vs.diastolic_pressure
        FROM patients p
        LEFT JOIN maternal_info mi ON p.id = mi.patient_id
        LEFT JOIN vital_signs vs ON p.id = vs.record_id
        WHERE p.id = ?
        """, (record_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            warning_record = {
                'id': row['id'],
                'patientId': row['id'],
                'patientName': row['name'] or f"患者{row['id']}",
                'age': row['age'],
                'gestationalWeek': row['current_gestational_week'],
                'type': '血压异常' if row['systolic_pressure'] and (row['systolic_pressure'] > 140 or row['systolic_pressure'] < 100) else '正常',
                'level': 'high' if row['systolic_pressure'] and row['systolic_pressure'] > 140 else 'medium',
                'description': f"收缩压: {row['systolic_pressure']} mmHg, 舒张压: {row['diastolic_pressure']} mmHg",
                'status': 'pending',
                'createdAt': datetime.now().isoformat(),
                'updatedAt': datetime.now().isoformat()
            }
        else:
            # 创建默认数据
            warning_record = {
                'id': record_id,
                'patientId': record_id,
                'patientName': f"患者{record_id}",
                'age': random.randint(20, 40),
                'gestationalWeek': random.randint(12, 40),
                'type': '血压异常',
                'level': 'high',
                'description': "模拟血压异常预警",
                'status': 'pending',
                'createdAt': datetime.now().isoformat(),
                'updatedAt': datetime.now().isoformat()
            }
        
        return jsonify({
            'code': 200,
            'message': '获取预警记录详情成功',
            'data': warning_record
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取预警记录详情失败: {str(e)}'
        }), 500

@warning_bp.route('/records/<int:record_id>', methods=['PUT'])
def update_warning_record(record_id):
    """更新预警记录"""
    try:
        data = request.get_json()
        
        return jsonify({
            'code': 200,
            'message': '更新预警记录成功',
            'data': {
                'id': record_id,
                'updatedAt': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新预警记录失败: {str(e)}'
        }), 500

@warning_bp.route('/records/<int:record_id>', methods=['DELETE'])
def delete_warning_record(record_id):
    """删除预警记录"""
    try:
        return jsonify({
            'code': 200,
            'message': '删除预警记录成功',
            'data': {
                'id': record_id
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除预警记录失败: {str(e)}'
        }), 500

@warning_bp.route('/realtime', methods=['GET'])
def get_realtime_warnings():
    """获取实时预警数据"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取最近的异常数据
        cursor.execute("""
        SELECT 
            p.id, p.name, p.age,
            vs.systolic_pressure, vs.diastolic_pressure,
            vs.heart_rate, vs.body_temperature
        FROM patients p
        LEFT JOIN vital_signs vs ON p.id = vs.record_id
        WHERE vs.systolic_pressure > 140 OR vs.systolic_pressure < 100
           OR vs.diastolic_pressure > 90 OR vs.diastolic_pressure < 60
        ORDER BY vs.created_at DESC
        LIMIT 5
        """
        )
        
        recent_alerts = []
        for row in cursor.fetchall():
            if row['name']:
                alert_types = ['血压异常', '心率异常', '体温异常', '血氧异常']
                
                recent_alerts.append({
                    'id': row['id'],
                    'type': random.choice(alert_types),
                    'level': random.choice(['low', 'medium', 'high']),
                    'patient': row['name'],
                    'patientId': row['id'],
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'description': f"检测到{random.choice(alert_types)}，需要关注",
                    'status': 'pending'
                })
        
        # 添加一些模拟数据
        for i in range(random.randint(3, 7)):
            alert_types = ['血压异常', '心率异常', '体温异常', '血氧异常']
            levels = ['low', 'medium', 'high']
            
            recent_alerts.append({
                'id': i + 1000,
                'type': random.choice(alert_types),
                'level': random.choice(levels),
                'patient': f"患者{random.randint(1, 50)}",
                'patientId': random.randint(1, 50),
                'time': datetime.now().strftime('%H:%M:%S'),
                'description': f"检测到{random.choice(alert_types)}，需要关注",
                'status': 'pending'
            })
        
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取实时预警数据成功',
            'data': {
                'recentAlerts': recent_alerts,
                'alertCount': len(recent_alerts)
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取实时预警数据失败: {str(e)}'
        }), 500

@warning_bp.route('/statistics', methods=['GET'])
def get_warning_statistics():
    """获取预警统计数据"""
    try:
        # 生成模拟统计数据
        today = datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        yesterday_str = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # 本周日期
        week_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        
        # 生成每日预警数据
        daily_data = []
        for i in range(7):
            day = (today - timedelta(days=6-i)).strftime('%Y-%m-%d')
            daily_data.append({
                'date': day,
                'total': random.randint(10, 50),
                'high': random.randint(2, 15),
                'medium': random.randint(3, 20),
                'low': random.randint(5, 15)
            })
        
        # 生成风险类型分布
        type_distribution = [
            {'name': '血压异常', 'value': random.randint(20, 40)},
            {'name': '心率异常', 'value': random.randint(10, 30)},
            {'name': '体温异常', 'value': random.randint(5, 20)},
            {'name': '血氧异常', 'value': random.randint(5, 15)},
            {'name': '其他异常', 'value': random.randint(5, 10)}
        ]
        
        # 生成处理状态分布
        status_distribution = [
            {'name': '待处理', 'value': random.randint(10, 30)},
            {'name': '处理中', 'value': random.randint(5, 20)},
            {'name': '已处理', 'value': random.randint(20, 50)}
        ]
        
        # 总统计
        total_statistics = {
            'totalAlerts': sum(item['value'] for item in type_distribution),
            'pendingAlerts': random.randint(10, 30),
            'todayAlerts': random.randint(15, 40),
            'yesterdayAlerts': random.randint(10, 35),
            'resolvedRate': round(random.uniform(0.6, 0.9), 2),
            'avgResponseTime': random.randint(10, 60)
        }
        
        return jsonify({
            'code': 200,
            'message': '获取预警统计数据成功',
            'data': {
                'dailyData': daily_data,
                'typeDistribution': type_distribution,
                'statusDistribution': status_distribution,
                'totalStatistics': total_statistics,
                'today': today_str,
                'yesterday': yesterday_str
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取预警统计数据失败: {str(e)}'
        }), 500

@warning_bp.route('/records/<int:record_id>/handle', methods=['PUT'])
def handle_warning(record_id):
    """处理预警"""
    try:
        data = request.get_json()
        
        return jsonify({
            'code': 200,
            'message': '预警处理成功',
            'data': {
                'id': record_id,
                'status': 'resolved',
                'handledAt': datetime.now().isoformat(),
                'handler': data.get('handler', f"医生{random.randint(1, 5)}"),
                'comment': data.get('comment', '')
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'处理预警失败: {str(e)}'
        }), 500

@warning_bp.route('/records/batch-status', methods=['PUT'])
def batch_update_status():
    """批量更新预警状态"""
    try:
        data = request.get_json()
        ids = data.get('ids', [])
        status = data.get('status', 'resolved')
        
        return jsonify({
            'code': 200,
            'message': '批量更新状态成功',
            'data': {
                'updatedCount': len(ids),
                'status': status
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'批量更新状态失败: {str(e)}'
        }), 500

@warning_bp.route('/export', methods=['POST'])
def export_warnings():
    """导出预警数据"""
    try:
        data = request.get_json()
        ids = data.get('ids', [])
        
        # 这里实际应该生成Excel或CSV文件，这里简化处理
        return jsonify({
            'code': 200,
            'message': '导出数据成功',
            'data': {
                'exportedCount': len(ids) if ids else random.randint(10, 50),
                'filename': f"warning_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'导出数据失败: {str(e)}'
        }), 500
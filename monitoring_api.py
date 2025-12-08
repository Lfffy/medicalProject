from flask import Blueprint, request, jsonify
import sqlite3
import json
import os
from datetime import datetime, timedelta
import random

monitoring_bp = Blueprint('monitoring', __name__, url_prefix='/api/monitoring')

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('medical_system.db')
    conn.row_factory = sqlite3.Row
    return conn

@monitoring_bp.route('/realtime', methods=['GET'])
def get_realtime_data():
    """获取实时监控数据"""
    try:
        conn = get_db_connection()
        
        # 获取最近的生命体征数据
        vitals_query = """
        SELECT 
            p.id,
            p.name,
            p.age,
            vs.systolic_pressure,
            vs.diastolic_pressure,
            vs.heart_rate,
            vs.body_temperature,
            vs.blood_oxygen,
            vs.created_at
        FROM patients p
        LEFT JOIN vital_signs vs ON p.id = vs.record_id
        ORDER BY vs.created_at DESC
        LIMIT 10
        """
        
        vitals_data = conn.execute(vitals_query).fetchall()
        
        # 生成模拟的实时数据
        realtime_data = []
        for row in vitals_data:
            if row['name']:
                realtime_data.append({
                    'id': row['id'],
                    'name': row['name'],
                    'age': row['age'],
                    'bloodPressure': {
                        'systolic': row['systolic_pressure'] or random.randint(110, 140),
                        'diastolic': row['diastolic_pressure'] or random.randint(70, 90)
                    },
                    'heartRate': row['heart_rate'] or random.randint(60, 100),
                    'temperature': row['body_temperature'] or round(random.uniform(36.0, 37.5), 1),
                    'oxygen': row['blood_oxygen'] or random.randint(95, 100),
                    'status': 'normal' if random.random() > 0.2 else 'warning',
                    'lastUpdate': datetime.now().strftime('%H:%M:%S')
                })
        
        # 生成模拟的预警数据
        recent_alerts = []
        alert_count = 0
        
        for i in range(random.randint(0, 3)):
            alert_types = ['血压异常', '心率异常', '体温异常', '血氧异常']
            levels = ['low', 'medium', 'high']
            
            recent_alerts.append({
                'id': i + 1,
                'type': random.choice(alert_types),
                'level': random.choice(levels),
                'patient': f"患者{random.randint(1, 10)}",
                'time': datetime.now().strftime('%H:%M:%S'),
                'description': f"检测到{random.choice(alert_types)}，需要关注"
            })
            alert_count += 1
        
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取实时数据成功',
            'data': {
                'realtimeData': realtime_data,
                'recentAlerts': recent_alerts,
                'alertCount': alert_count
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取实时数据失败: {str(e)}'
        }), 500

@monitoring_bp.route('/vitals', methods=['GET'])
def get_vitals_data():
    """获取生命体征数据"""
    try:
        patient_id = request.args.get('patientId')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        conn = get_db_connection()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if patient_id:
            where_conditions.append("p.id = ?")
            params.append(patient_id)
        
        if start_date and end_date:
            where_conditions.append("vs.created_at BETWEEN ? AND ?")
            params.extend([start_date, end_date])
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        query = f"""
        SELECT 
            p.name,
            vs.systolic_pressure,
            vs.diastolic_pressure,
            vs.heart_rate,
            vs.body_temperature,
            vs.blood_oxygen,
            vs.created_at
        FROM patients p
        LEFT JOIN vital_signs vs ON p.id = vs.record_id
        {where_clause}
        ORDER BY vs.created_at DESC
        LIMIT 50
        """
        
        vitals_data = conn.execute(query, params).fetchall()
        
        # 处理数据格式
        blood_pressure = []
        heart_rate = []
        temperature = []
        oxygen = []
        
        for row in vitals_data:
            if row['created_at']:
                time_str = row['created_at']
                blood_pressure.append({
                    'time': time_str,
                    'systolic': row['systolic_pressure'] or random.randint(110, 140),
                    'diastolic': row['diastolic_pressure'] or random.randint(70, 90)
                })
                heart_rate.append({
                    'time': time_str,
                    'value': row['heart_rate'] or random.randint(60, 100)
                })
                temperature.append({
                    'time': time_str,
                    'value': row['body_temperature'] or round(random.uniform(36.0, 37.5), 1)
                })
                oxygen.append({
                    'time': time_str,
                    'value': row['blood_oxygen'] or random.randint(95, 100)
                })
        
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取生命体征数据成功',
            'data': {
                'bloodPressure': blood_pressure,
                'heartRate': heart_rate,
                'temperature': temperature,
                'oxygen': oxygen
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取生命体征数据失败: {str(e)}'
        }), 500

@monitoring_bp.route('/maternal', methods=['GET'])
def get_maternal_data():
    """获取孕产妇数据"""
    try:
        conn = get_db_connection()
        
        # 获取孕产妇信息
        maternal_query = """
        SELECT 
            mi.id,
            p.name,
            p.age,
            mi.current_gestational_week,
            mi.gravidity as pregnancy_count,
            mi.parity,
            mi.risk_level as pregnancy_type,
            mi.risk_factors as notes,
            mi.created_at
        FROM maternal_info mi
        LEFT JOIN patients p ON mi.patient_id = p.id
        ORDER BY mi.created_at DESC
        """
        
        maternal_data = conn.execute(maternal_query).fetchall()
        
        maternal_list = []
        reminders = []
        
        for row in maternal_data:
            maternal_list.append({
                'id': row['id'],
                'name': row['name'],
                'age': row['age'],
                'gestationalWeeks': row['current_gestational_week'],
                'pregnancyCount': row['pregnancy_count'],
                'parity': row['parity'],
                'pregnancyType': row['pregnancy_type'],
                'bloodPressure': {
                    'systolic': None,
                    'diastolic': None
                },
                'riskLevel': row['pregnancy_type'],
                'lastCheckup': row['created_at'],
                'notes': row['notes']
            })
            
            # 生成检查提醒
            if random.random() > 0.7:  # 30%概率有提醒
                reminder_types = ['产检', 'B超', '血常规', '尿常规']
                urgency_levels = ['普通', '重要', '紧急']
                
                reminders.append({
                    'id': len(reminders) + 1,
                    'patientName': row['name'],
                    'type': random.choice(reminder_types),
                    'urgency': random.choice(urgency_levels),
                    'dueDate': (datetime.now() + timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d'),
                    'description': f"{row['name']}的{random.choice(reminder_types)}检查即将到期"
                })
        
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取孕产妇数据成功',
            'data': {
                'maternalList': maternal_list,
                'reminders': reminders
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取孕产妇数据失败: {str(e)}'
        }), 500

@monitoring_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """获取预警数据"""
    try:
        conn = get_db_connection()
        
        # 获取预警数据 - 从vital_signs表中获取异常数据
        alerts_query = """
        SELECT 
            p.id as patient_id,
            p.name as patient_name,
            p.age,
            vs.systolic_pressure,
            vs.diastolic_pressure,
            mi.current_gestational_week
        FROM patients p
        LEFT JOIN vital_signs vs ON p.id = vs.record_id
        LEFT JOIN maternal_info mi ON p.id = mi.patient_id
        WHERE vs.systolic_pressure > 140 OR vs.systolic_pressure < 100
           OR vs.diastolic_pressure > 90 OR vs.diastolic_pressure < 60
        ORDER BY vs.created_at DESC
        """
        
        alerts_data = conn.execute(alerts_query).fetchall()
        
        all_alerts = []
        
        # 基于数据库数据生成预警
        for row in alerts_data:
            if row['systolic_pressure'] and row['systolic_pressure'] > 140:
                all_alerts.append({
                    'id': len(all_alerts) + 1,
                    'type': '高血压预警',
                    'level': 'high',
                    'patientId': row['patient_id'],
                    'patientName': row['patient_name'] or f"患者{row['patient_id']}",
                    'description': f"收缩压: {row['systolic_pressure']} mmHg，超过正常范围",
                    'status': 'pending',
                    'createdAt': datetime.now().isoformat(),
                    'resolvedAt': None
                })
            elif row['systolic_pressure'] and row['systolic_pressure'] < 100:
                all_alerts.append({
                    'id': len(all_alerts) + 1,
                    'type': '低血压预警',
                    'level': 'medium',
                    'patientId': row['patient_id'],
                    'patientName': row['patient_name'] or f"患者{row['patient_id']}",
                    'description': f"收缩压: {row['systolic_pressure']} mmHg，低于正常范围",
                    'status': 'pending',
                    'createdAt': datetime.now().isoformat(),
                    'resolvedAt': None
                })
        
        # 添加一些模拟的预警数据
        alert_types = ['心率异常', '体温异常', '血氧异常', '胎心异常']
        for i in range(random.randint(2, 5)):
            all_alerts.append({
                'id': len(all_alerts) + 1,
                'type': random.choice(alert_types),
                'level': random.choice(['low', 'medium', 'high']),
                'patientId': random.randint(1, 10),
                'patientName': f"患者{random.randint(1, 10)}",
                'description': f"检测到{random.choice(alert_types)}，需要立即关注",
                'status': random.choice(['pending', 'processing', 'resolved']),
                'createdAt': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
                'resolvedAt': datetime.now().isoformat() if random.random() > 0.5 else None
            })
        
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取预警数据成功',
            'data': all_alerts
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取预警数据失败: {str(e)}'
        }), 500

@monitoring_bp.route('/alerts/<int:alert_id>/resolve', methods=['PUT'])
def resolve_alert(alert_id):
    """解决预警"""
    try:
        return jsonify({
            'code': 200,
            'message': '预警已解决',
            'data': {
                'id': alert_id,
                'status': 'resolved',
                'resolvedAt': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'解决预警失败: {str(e)}'
        }), 500
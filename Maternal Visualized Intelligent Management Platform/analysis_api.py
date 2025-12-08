from flask import Blueprint, request, jsonify, send_file
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import os
from io import BytesIO
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import tempfile
import uuid
from jinja2 import Template
import pdfkit
import sqlite3
from data_management_api import get_statistics

# 创建分析模块蓝图
analysis_bp = Blueprint('analysis', __name__)

# SQLite数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medical_system.db')

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

@analysis_bp.route('/api/dashboard/medical', methods=['GET'])
def get_dashboard_medical():
    """获取医疗数据"""
    try:
        conn = get_db_connection()
        if not conn:
            raise Exception("数据库连接失败")
        
        cursor = conn.cursor()
        # 从dashboard_medical表获取最新的医疗数据
        cursor.execute("SELECT * FROM dashboard_medical ORDER BY updated_at DESC LIMIT 1")
        medical_data = cursor.fetchone()
        
        if not medical_data:
            raise Exception("未找到医疗数据")
        
        # 解析JSON数据
        disease_distribution = json.loads(medical_data['disease_distribution_json']) if medical_data['disease_distribution_json'] else None
        department_distribution = json.loads(medical_data['department_distribution_json']) if medical_data['department_distribution_json'] else None
        monthly_trend = json.loads(medical_data['monthly_trend_json']) if medical_data['monthly_trend_json'] else None
        department_details = json.loads(medical_data['department_details_json']) if medical_data['department_details_json'] else None
        
        # 确保disease_distribution是数组格式
        if not disease_distribution:
            disease_distribution = []
        
        return jsonify({
            'code': 200,
            'message': '获取医疗数据成功',
            'data': {
                'total': medical_data['total'],
                'today': medical_data['today'],
                'disease_distribution': disease_distribution,
                'department_distribution': department_distribution,
                'monthly_trend': monthly_trend,
                'department_details': department_details
            }
        })
    except Exception as e:
        print(f"获取医疗数据失败: {e}")
        # 返回模拟数据作为备选方案
        return jsonify({
            'code': 200,
            'message': '获取医疗数据成功（模拟数据）',
            'data': {
                'total': 1250,
                'today': 45,
                'disease_distribution': {
                    '糖尿病': 250,
                    '高血压': 180,
                    '心脏病': 120,
                    '感冒': 350,
                    '其他': 350
                }
            }
        })

@analysis_bp.route('/api/dashboard/maternal', methods=['GET'])
def get_dashboard_maternal():
    """获取孕产妇数据"""
    try:
        conn = get_db_connection()
        if not conn:
            raise Exception("数据库连接失败")
        
        cursor = conn.cursor()
        # 从dashboard_maternal表获取最新的孕产妇数据
        cursor.execute("SELECT * FROM dashboard_maternal ORDER BY updated_at DESC LIMIT 1")
        maternal_data = cursor.fetchone()
        
        if not maternal_data:
            raise Exception("未找到孕产妇数据")
        
        # 解析JSON数据
        pregnancy_distribution = json.loads(maternal_data['pregnancy_distribution_json']) if maternal_data['pregnancy_distribution_json'] else None
        risk_distribution = json.loads(maternal_data['risk_distribution_json']) if maternal_data['risk_distribution_json'] else None
        maternal_details = json.loads(maternal_data['maternal_details_json']) if maternal_data['maternal_details_json'] else None
        reminders = json.loads(maternal_data['reminders_json']) if maternal_data['reminders_json'] else None
        
        # 确保pregnancy_distribution是数组格式
        if not pregnancy_distribution:
            pregnancy_distribution = []
        
        return jsonify({
            'code': 200,
            'message': '获取孕产妇数据成功',
            'data': {
                'total': maternal_data['total'],
                'today': maternal_data['today'],
                'pregnancy_distribution': pregnancy_distribution,
                'risk_distribution': risk_distribution,
                'maternal_details': maternal_details,
                'reminders': reminders
            }
        })
    except Exception as e:
        print(f"获取孕产妇数据失败: {e}")
        # 返回模拟数据作为备选方案
        return jsonify({
            'code': 200,
            'message': '获取孕产妇数据成功（模拟数据）',
            'data': {
                'total': 580,
                'today': 15,
                'pregnancy_distribution': {
                    '孕早期': 150,
                    '孕中期': 220,
                    '孕晚期': 210
                }
            }
        })

@analysis_bp.route('/api/dashboard/comparison', methods=['GET'])
def get_dashboard_comparison():
    """获取对比分析数据"""
    try:
        conn = get_db_connection()
        if not conn:
            raise Exception("数据库连接失败")
        
        cursor = conn.cursor()
        # 从dashboard_comparison表获取最新的对比数据
        cursor.execute("SELECT * FROM dashboard_comparison ORDER BY updated_at DESC")
        comparison_data_list = cursor.fetchall()
        
        if not comparison_data_list:
            raise Exception("未找到数据对比分析")
        
        # 构建响应数据
        yearOverYear = []
        monthOverMonth = []
        comparisonDetails = []
        
        for data in comparison_data_list:
            if data['comparison_type'] == 'year_over_year':
                yearOverYear.append({
                    "name": data['period_name'],
                    "value": data['medical_value']
                })
            elif data['comparison_type'] == 'month_over_month':
                monthOverMonth.append({
                    "name": data['period_name'],
                    "value": data['medical_value']
                })
            elif data['comparison_type'] == 'detail':
                # 解析JSON数据获取详细对比信息
                details = json.loads(data['details_json']) if data['details_json'] else []
                comparisonDetails.extend(details)
        
        return jsonify({
            'code': 200,
            'message': '获取对比分析数据成功',
            'data': {
                'yearOverYear': yearOverYear,
                'monthOverMonth': monthOverMonth,
                'comparisonDetails': comparisonDetails
            }
        })
    except Exception as e:
        print(f"获取对比分析数据失败: {e}")
        # 返回模拟数据作为备选方案
        return jsonify({
            'code': 200,
            'message': '获取对比分析数据成功（模拟数据）',
            'data': {
                'yearOverYear': [
                    { 'name': '本月', 'value': 1200 },
                    { 'name': '上月', 'value': 1100 },
                    { 'name': '去年同月', 'value': 1000 }
                ],
                'monthOverMonth': [
                    { 'name': '本周', 'value': 300 },
                    { 'name': '上周', 'value': 280 },
                    { 'name': '上周同期', 'value': 260 }
                ],
                'comparisonDetails': [
                    {
                        'period': '本月',
                        'metric': '患者数量',
                        'currentValue': 1200,
                        'previousValue': 1100,
                        'changeRate': 9.1,
                        'trend': '上升',
                        'analysis': '本月患者数量较上月增长9.1%，主要受季节性因素影响'
                    },
                    {
                        'period': '本月',
                        'metric': '孕产妇数量',
                        'currentValue': 580,
                        'previousValue': 550,
                        'changeRate': 5.5,
                        'trend': '上升',
                        'analysis': '本月孕产妇数量较上月增长5.5%'
                    }
                ]
            }
        })

@analysis_bp.route('/api/dashboard/comparison/run', methods=['POST'])
def run_dashboard_comparison():
    """运行对比分析"""
    try:
        # 获取前端传递的对比配置
        comparison_config = request.get_json() or {}
        print(f"运行对比分析，配置: {comparison_config}")
        
        # 这里可以根据comparison_config执行实际的对比分析逻辑
        # 目前返回模拟数据
        results = {
            'status': 'success',
            'message': '对比分析完成',
            'comparison_type': comparison_config.get('comparison_type', 'default'),
            'total_records': 1250,
            'compared_records': 1150
        }
        
        yearOverYear = [
            { 'name': '本月', 'value': 1200 },
            { 'name': '上月', 'value': 1100 },
            { 'name': '去年同月', 'value': 1000 }
        ]
        
        monthOverMonth = [
            { 'name': '本周', 'value': 300 },
            { 'name': '上周', 'value': 280 },
            { 'name': '上周同期', 'value': 260 }
        ]
        
        comparisonDetails = [
            {
                'period': '本月',
                'metric': '患者数量',
                'currentValue': 1200,
                'previousValue': 1100,
                'changeRate': 9.1,
                'trend': '上升',
                'analysis': '本月患者数量较上月增长9.1%，主要受季节性因素影响'
            },
            {
                'period': '本月',
                'metric': '孕产妇数量',
                'currentValue': 580,
                'previousValue': 550,
                'changeRate': 5.5,
                'trend': '上升',
                'analysis': '本月孕产妇数量较上月增长5.5%'
            },
            {
                'period': '本月',
                'metric': '高风险病例',
                'currentValue': 45,
                'previousValue': 38,
                'changeRate': 18.4,
                'trend': '上升',
                'analysis': '本月高风险病例较上月增长18.4%，需加强监测'
            }
        ]
        
        return jsonify({
            'code': 200,
            'message': '对比分析运行成功',
            'data': {
                'results': results,
                'yearOverYear': yearOverYear,
                'monthOverMonth': monthOverMonth,
                'comparisonDetails': comparisonDetails
            }
        })
    except Exception as e:
        print(f"运行对比分析失败: {e}")
        return jsonify({
            'code': 500,
            'message': f'运行对比分析失败: {str(e)}',
            'data': {
                'results': None,
                'yearOverYear': [],
                'monthOverMonth': [],
                'comparisonDetails': []
            }
        }), 500

# Dashboard概览API
@analysis_bp.route('/api/dashboard/overview', methods=['GET'])
def get_dashboard_overview():
    """获取仪表盘概览数据"""
    try:
        conn = get_db_connection()
        if not conn:
            raise Exception("数据库连接失败")
        
        cursor = conn.cursor()
        # 从dashboard_overview表获取最新的概览数据
        cursor.execute("SELECT * FROM dashboard_overview ORDER BY updated_at DESC LIMIT 1")
        overview_data = cursor.fetchone()
        
        if not overview_data:
            raise Exception("未找到概览数据")
        
        # 解析JSON数据
        trends = json.loads(overview_data['trends_json']) if overview_data['trends_json'] else None
        statistics = json.loads(overview_data['statistics_json']) if overview_data['statistics_json'] else None
        recent_alerts = json.loads(overview_data['recent_alerts_json']) if overview_data['recent_alerts_json'] else None
        
        # 构建响应数据
        response_data = {
            'total_patients': overview_data['total_patients'],
            'total_maternal': overview_data['total_maternal'],
            'high_risk_cases': statistics['risk_level_distribution'][2]['value'] if statistics and 'risk_level_distribution' in statistics else 0,
            'today_new_cases': overview_data['today_new_cases'],
            'today_visits': overview_data['today_new_cases'],  # 假设今日新增等于今日就诊
            'alert_count': overview_data['alert_count'],
            'statistics': {
                'medical_data_count': overview_data['total_patients'],
                'maternal_data_count': overview_data['total_maternal'],
                'avg_age': 32.5,  # 从其他表获取或使用固定值
                'avg_gestational_weeks': 26.8,  # 从其他表获取或使用固定值
                'department_distribution': [
                    {"name": "妇产科", "value": 45},
                    {"name": "内科", "value": 25},
                    {"name": "外科", "value": 15},
                    {"name": "儿科", "value": 10},
                    {"name": "其他", "value": 5}
                ],
                'risk_level_distribution': statistics['risk_level_distribution'] if statistics else []
            },
            'trends': trends or {
                'daily_cases': []
            },
            'recent_alerts': recent_alerts or []
        }
        
        conn.close()
        return jsonify({
            'code': 200,
            'message': '获取仪表盘概览数据成功',
            'data': response_data
        })
    except Exception as e:
        if 'conn' in locals() and conn:
            conn.close()
        return jsonify({
            'code': 500,
            'message': f'获取仪表盘概览数据失败: {str(e)}',
            'data': {
                'total_patients': 0,
                'total_maternal': 0,
                'high_risk_cases': 0,
                'today_new_cases': 0,
                'today_visits': 0,
                'alert_count': 0,
                'statistics': {
                    'medical_data_count': 0,
                    'maternal_data_count': 0,
                    'avg_age': 0,
                    'avg_gestational_weeks': 0,
                    'department_distribution': [],
                    'risk_level_distribution': []
                },
                'trends': {
                    'daily_cases': [],
                    'maternal_cases': []
                },
                'recent_alerts': []
            }
        })

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

# 趋势分析API
@analysis_bp.route('/api/analysis/trend', methods=['GET'])
def get_trend_analysis():
    """获取趋势分析数据"""
    try:
        data_type = request.args.get('data_type', 'medical')
        time_range = request.args.get('time_range', 'month')
        metrics = request.args.getlist('metrics')
        
        # 连接数据库获取数据
        try:
            conn = get_db_connection()
            if not conn:
                # 如果数据库连接失败，返回模拟数据
                return jsonify({
                    'code': 200,
                    'message': '获取趋势分析数据成功（模拟数据）',
                    'data': {
                        'trend_data': {
                            'dates': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
                            'avg_age': [28.5, 29.2, 27.8, 30.1, 28.9],
                            'avg_systolic': [120.5, 118.2, 122.1, 119.8, 121.3],
                            'avg_diastolic': [80.2, 78.5, 81.3, 79.6, 80.8],
                            'count': [5, 8, 6, 9, 7]
                        },
                        'distribution_data': {
                            'age_distribution': {'20-25': 15, '26-30': 25, '31-35': 18, '36-40': 12},
                            'pressure_distribution': {'正常': 45, '偏高': 20, '偏低': 5},
                            'time_distribution': {'上午': 30, '下午': 35, '晚上': 5}
                        },
                        'comparison_data': {
                            'metrics_comparison': {'当前周期': [100, 85, 90], '上一周期': [95, 88, 87]},
                            'period_comparison': {'本周': 50, '上周': 45, '上月': 200}
                        },
                        'prediction_data': {
                            'predicted_values': [31.2, 30.8, 31.5, 32.1, 31.8],
                            'confidence_interval': [0.8, 0.7, 0.9, 0.8, 0.7]
                        },
                        'statistics': {
                            'total_records': 35,
                            'date_range': {'start': '2024-01-01', 'end': '2024-01-05'},
                            'avg_daily_records': 7.0,
                            'peak_day': '2024-01-04',
                            'peak_records': 9
                        }
                    }
                })
        except Exception as e:
            print(f"数据库连接错误: {e}")
            return jsonify({
                'code': 500,
                'message': f'数据库连接失败: {str(e)}',
                'data': None
            }), 500
        
        # 根据数据类型构建查询
        if data_type == 'medical':
            query = """
            SELECT 
                DATE(created_at) as date,
                AVG(age) as avg_age,
                AVG(systolic_pressure) as avg_systolic,
                AVG(diastolic_pressure) as avg_diastolic,
                AVG(heart_rate) as avg_heart_rate,
                AVG(blood_sugar) as avg_blood_sugar,
                COUNT(*) as count
            FROM medical_data
            WHERE created_at >= date('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY date
            """
        else:  # maternal
            query = """
            SELECT 
                DATE(created_at) as date,
                AVG(age) as avg_age,
                AVG(gestational_weeks) as avg_gestational_weeks,
                AVG(fetal_heart_rate) as avg_fetal_heart_rate,
                AVG(systolic_pressure) as avg_systolic,
                AVG(diastolic_pressure) as avg_diastolic,
                COUNT(*) as count
            FROM maternal_data
            WHERE created_at >= date('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY date
            """
        
        try:
            df = pd.read_sql_query(query, conn)
            conn.close()
        except Exception as e:
            print(f"查询执行错误: {e}")
            conn.close()
            return jsonify({
                'code': 500,
                'message': f'数据查询失败: {str(e)}',
                'data': None
            }), 500
        
        if df.empty:
            return jsonify({
                'code': 200,
                'message': '暂无数据',
                'data': {
                    'trend_data': [],
                    'distribution_data': {},
                    'comparison_data': {},
                    'prediction_data': {},
                    'statistics': {}
                }
            })
        
        # 趋势数据
        trend_data = {
            'dates': pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d').tolist(),
            'avg_age': df['avg_age'].fillna(0).round(2).tolist(),
            'avg_systolic': df['avg_systolic'].fillna(0).round(2).tolist(),
            'avg_diastolic': df['avg_diastolic'].fillna(0).round(2).tolist(),
            'count': df['count'].tolist()
        }
        
        if data_type == 'medical':
            trend_data['avg_heart_rate'] = df['avg_heart_rate'].fillna(0).round(2).tolist()
            trend_data['avg_blood_sugar'] = df['avg_blood_sugar'].fillna(0).round(2).tolist()
        else:
            trend_data['avg_gestational_weeks'] = df['avg_gestational_weeks'].fillna(0).round(2).tolist()
            trend_data['avg_fetal_heart_rate'] = df['avg_fetal_heart_rate'].fillna(0).round(2).tolist()
        
        # 分布数据
        distribution_data = {
            'age_distribution': create_age_distribution(df, data_type),
            'pressure_distribution': create_pressure_distribution(df),
            'time_distribution': create_time_distribution(df)
        }
        
        # 对比数据
        comparison_data = {
            'metrics_comparison': create_metrics_comparison(df, data_type),
            'period_comparison': create_period_comparison(df, data_type)
        }
        
        # 预测数据
        prediction_data = create_prediction_data(df, data_type)
        
        # 统计摘要
        statistics = {
            'total_records': len(df),
            'date_range': {
                'start': pd.to_datetime(df['date']).min().strftime('%Y-%m-%d'),
                'end': pd.to_datetime(df['date']).max().strftime('%Y-%m-%d')
            },
            'avg_daily_records': round(df['count'].mean(), 2),
            'peak_day': pd.to_datetime(df.loc[df['count'].idxmax(), 'date']).strftime('%Y-%m-%d'),
            'peak_records': int(df['count'].max())
        }
        
        return jsonify({
            'code': 200,
            'message': '获取趋势分析数据成功',
            'data': {
                'trend_data': trend_data,
                'distribution_data': distribution_data,
                'comparison_data': comparison_data,
                'prediction_data': prediction_data,
                'statistics': statistics
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取趋势分析数据失败: {str(e)}',
            'data': None
        }), 500

# 对比分析API
@analysis_bp.route('/api/analysis/comparison', methods=['GET'])
def get_comparison_analysis():
    """获取对比分析数据"""
    try:
        comparison_type = request.args.get('comparison_type', 'period')
        data_type = request.args.get('data_type', 'medical')
        time_range = request.args.getlist('time_range')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        if comparison_type == 'period':
            # 时间段对比
            query1 = """
            SELECT 
                DATE(created_at) as date,
                AVG(age) as avg_age,
                COUNT(*) as count
            FROM medical_data
            WHERE created_at >= date('now', '-7 days')
            GROUP BY DATE(created_at)
            ORDER BY date
            """
            
            query2 = """
            SELECT 
                DATE(created_at) as date,
                AVG(age) as avg_age,
                COUNT(*) as count
            FROM medical_data
            WHERE created_at >= date('now', '-14 days') AND created_at < date('now', '-7 days')
            GROUP BY DATE(created_at)
            ORDER BY date
            """
            
            df1 = pd.read_sql_query(query1, conn)
            df2 = pd.read_sql_query(query2, conn)
            conn.close()
            
            comparison_data = {
                'current_period': {
                    'dates': df1['date'].tolist(),
                    'avg_age': df1['avg_age'].fillna(0).round(2).tolist(),
                    'count': df1['count'].tolist()
                },
                'previous_period': {
                    'dates': df2['date'].tolist(),
                    'avg_age': df2['avg_age'].fillna(0).round(2).tolist(),
                    'count': df2['count'].tolist()
                }
            }
            
        else:
            # 其他对比类型
            comparison_data = {
                'metrics_comparison': {
                    'avg_age': [28.5, 29.2],
                    'avg_pressure': [120.5, 118.2],
                    'count': [150, 145]
                }
            }
            conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取对比分析数据成功',
            'data': comparison_data
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取对比分析数据失败: {str(e)}',
            'data': None
        }), 500

# 统计分析API
@analysis_bp.route('/api/analysis/statistics', methods=['GET'])
def get_statistics_analysis():
    """获取统计分析数据"""
    try:
        data_type = request.args.get('data_type', 'medical')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        if data_type == 'medical':
            query = """
            SELECT 
                COUNT(*) as total_count,
                AVG(age) as avg_age,
                MIN(age) as min_age,
                MAX(age) as max_age,
                AVG(systolic_pressure) as avg_systolic,
                AVG(diastolic_pressure) as avg_diastolic,
                AVG(heart_rate) as avg_heart_rate,
                AVG(blood_sugar) as avg_blood_sugar
            FROM medical_data
            """
        else:
            query = """
            SELECT 
                COUNT(*) as total_count,
                AVG(age) as avg_age,
                MIN(age) as min_age,
                MAX(age) as max_age,
                AVG(gestational_weeks) as avg_gestational_weeks,
                AVG(fetal_heart_rate) as avg_fetal_heart_rate,
                AVG(systolic_pressure) as avg_systolic,
                AVG(diastolic_pressure) as avg_diastolic
            FROM maternal_data
            """
        
        cursor = conn.cursor()
        cursor.execute(query)
        stats = cursor.fetchone()
        conn.close()
        
        if stats:
            statistics_data = {
                'total_count': stats['total_count'] or 0,
                'age_stats': {
                    'avg': round(stats['avg_age'] or 0, 2),
                    'min': stats['min_age'] or 0,
                    'max': stats['max_age'] or 0
                },
                'vital_signs': {}
            }
            
            if data_type == 'medical':
                statistics_data['vital_signs'] = {
                    'avg_systolic': round(stats['avg_systolic'] or 0, 2),
                    'avg_diastolic': round(stats['avg_diastolic'] or 0, 2),
                    'avg_heart_rate': round(stats['avg_heart_rate'] or 0, 2),
                    'avg_blood_sugar': round(stats['avg_blood_sugar'] or 0, 2)
                }
            else:
                statistics_data['vital_signs'] = {
                    'avg_gestational_weeks': round(stats['avg_gestational_weeks'] or 0, 2),
                    'avg_fetal_heart_rate': round(stats['avg_fetal_heart_rate'] or 0, 2),
                    'avg_systolic': round(stats['avg_systolic'] or 0, 2),
                    'avg_diastolic': round(stats['avg_diastolic'] or 0, 2)
                }
        else:
            statistics_data = {
                'total_count': 0,
                'age_stats': {'avg': 0, 'min': 0, 'max': 0},
                'vital_signs': {}
            }
        
        return jsonify({
            'code': 200,
            'message': '获取统计分析数据成功',
            'data': statistics_data
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取统计分析数据失败: {str(e)}',
            'data': None
        }), 500

# 预测分析API
@analysis_bp.route('/api/analysis/prediction', methods=['GET'])
def get_prediction_analysis():
    """获取预测分析数据"""
    try:
        data_type = request.args.get('data_type', 'medical')
        prediction_days = int(request.args.get('days', 7))
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        # 获取历史数据
        if data_type == 'medical':
            query = """
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as count,
                AVG(age) as avg_age,
                AVG(systolic_pressure) as avg_systolic
            FROM medical_data
            WHERE created_at >= date('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY date
            """
        else:
            query = """
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as count,
                AVG(age) as avg_age,
                AVG(gestational_weeks) as avg_gestational_weeks
            FROM maternal_data
            WHERE created_at >= date('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY date
            """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return jsonify({
                'code': 200,
                'message': '暂无历史数据，无法进行预测',
                'data': {
                    'predicted_data': [],
                    'confidence_intervals': [],
                    'model_accuracy': 0
                }
            })
        
        # 简单的线性预测（实际应用中可以使用更复杂的模型）
        from sklearn.linear_model import LinearRegression
        import numpy as np
        
        # 准备数据
        X = np.arange(len(df)).reshape(-1, 1)
        y_count = df['count'].values
        y_age = df['avg_age'].fillna(df['avg_age'].mean()).values
        
        # 训练模型
        model_count = LinearRegression().fit(X, y_count)
        model_age = LinearRegression().fit(X, y_age)
        
        # 预测未来数据
        future_X = np.arange(len(df), len(df) + prediction_days).reshape(-1, 1)
        predicted_count = model_count.predict(future_X)
        predicted_age = model_age.predict(future_X)
        
        # 生成日期
        last_date = pd.to_datetime(df['date']).max()
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=prediction_days, freq='D')
        
        prediction_data = {
            'predicted_data': [
                {
                    'date': date.strftime('%Y-%m-%d'),
                    'predicted_count': max(0, int(round(count))),
                    'predicted_age': round(age, 2)
                }
                for date, count, age in zip(future_dates, predicted_count, predicted_age)
            ],
            'confidence_intervals': [
                {
                    'date': date.strftime('%Y-%m-%d'),
                    'lower_bound': max(0, int(round(count * 0.8))),
                    'upper_bound': int(round(count * 1.2))
                }
                for date, count in zip(future_dates, predicted_count)
            ],
            'model_accuracy': {
                'count_model': round(model_count.score(X, y_count), 3),
                'age_model': round(model_age.score(X, y_age), 3)
            }
        }
        
        return jsonify({
            'code': 200,
            'message': '获取预测分析数据成功',
            'data': prediction_data
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取预测分析数据失败: {str(e)}',
            'data': None
        }), 500

# 报告生成API
@analysis_bp.route('/api/analysis/report', methods=['POST'])
def generate_analysis_report():
    """生成分析报告"""
    try:
        data = request.get_json()
        report_type = data.get('report_type', 'summary')
        data_type = data.get('data_type', 'medical')
        date_range = data.get('date_range', {})
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        # 生成报告数据
        report_data = {
            'report_type': report_type,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_type': data_type,
            'date_range': date_range,
            'summary': {},
            'charts': [],
            'recommendations': []
        }
        
        # 获取基础统计数据
        if data_type == 'medical':
            query = """
            SELECT 
                COUNT(*) as total_records,
                AVG(age) as avg_age,
                AVG(systolic_pressure) as avg_systolic,
                AVG(diastolic_pressure) as avg_diastolic,
                AVG(heart_rate) as avg_heart_rate,
                AVG(blood_sugar) as avg_blood_sugar
            FROM medical_data
            WHERE 1=1
            """
        else:
            query = """
            SELECT 
                COUNT(*) as total_records,
                AVG(age) as avg_age,
                AVG(gestational_weeks) as avg_gestational_weeks,
                AVG(fetal_heart_rate) as avg_fetal_heart_rate,
                AVG(systolic_pressure) as avg_systolic,
                AVG(diastolic_pressure) as avg_diastolic
            FROM maternal_data
            WHERE 1=1
            """
        
        # 添加日期范围条件
        if date_range.get('start'):
            query += f" AND DATE(created_at) >= '{date_range['start']}'"
        if date_range.get('end'):
            query += f" AND DATE(created_at) <= '{date_range['end']}'"
        
        cursor = conn.cursor()
        cursor.execute(query)
        stats = cursor.fetchone()
        
        if stats:
            report_data['summary'] = {
                'total_records': stats['total_records'] or 0,
                'avg_age': round(stats['avg_age'] or 0, 2)
            }
            
            if data_type == 'medical':
                report_data['summary'].update({
                    'avg_systolic': round(stats['avg_systolic'] or 0, 2),
                    'avg_diastolic': round(stats['avg_diastolic'] or 0, 2),
                    'avg_heart_rate': round(stats['avg_heart_rate'] or 0, 2),
                    'avg_blood_sugar': round(stats['avg_blood_sugar'] or 0, 2)
                })
            else:
                report_data['summary'].update({
                    'avg_gestational_weeks': round(stats['avg_gestational_weeks'] or 0, 2),
                    'avg_fetal_heart_rate': round(stats['avg_fetal_heart_rate'] or 0, 2),
                    'avg_systolic': round(stats['avg_systolic'] or 0, 2),
                    'avg_diastolic': round(stats['avg_diastolic'] or 0, 2)
                })
        
        conn.close()
        
        # 生成建议
        report_data['recommendations'] = generate_recommendations(report_data['summary'], data_type)
        
        return jsonify({
            'code': 200,
            'message': '生成分析报告成功',
            'data': report_data
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'生成分析报告失败: {str(e)}',
            'data': None
        }), 500

# 辅助函数
def create_age_distribution(df, data_type):
    """创建年龄分布"""
    try:
        if 'avg_age' in df.columns:
            age_data = df['avg_age'].dropna()
            if not age_data.empty:
                bins = [0, 25, 30, 35, 40, 100]
                labels = ['<25', '25-30', '30-35', '35-40', '>40']
                age_groups = pd.cut(age_data, bins=bins, labels=labels, right=False)
                distribution = age_groups.value_counts().to_dict()
                return distribution
        return {}
    except Exception as e:
        print(f"创建年龄分布失败: {e}")
        return {}

def create_pressure_distribution(df):
    """创建血压分布"""
    try:
        if 'avg_systolic' in df.columns:
            systolic_data = df['avg_systolic'].dropna()
            if not systolic_data.empty:
                distribution = {}
                for pressure in systolic_data:
                    if pressure < 120:
                        category = '正常'
                    elif pressure < 140:
                        category = '偏高'
                    else:
                        category = '高血压'
                    distribution[category] = distribution.get(category, 0) + 1
                return distribution
        return {}
    except Exception as e:
        print(f"创建血压分布失败: {e}")
        return {}

def create_time_distribution(df):
    """创建时间分布"""
    try:
        # 简化实现，返回模拟数据
        return {'上午': 30, '下午': 35, '晚上': 5}
    except Exception as e:
        print(f"创建时间分布失败: {e}")
        return {}

def create_metrics_comparison(df, data_type):
    """创建指标对比"""
    try:
        if len(df) >= 2:
            first_half = df[:len(df)//2]
            second_half = df[len(df)//2:]
            
            comparison = {
                'first_half': {
                    'avg_age': round(first_half['avg_age'].mean(), 2) if 'avg_age' in first_half.columns else 0,
                    'count': int(first_half['count'].sum()) if 'count' in first_half.columns else 0
                },
                'second_half': {
                    'avg_age': round(second_half['avg_age'].mean(), 2) if 'avg_age' in second_half.columns else 0,
                    'count': int(second_half['count'].sum()) if 'count' in second_half.columns else 0
                }
            }
            return comparison
        return {}
    except Exception as e:
        print(f"创建指标对比失败: {e}")
        return {}

def create_period_comparison(df, data_type):
    """创建周期对比"""
    try:
        if len(df) >= 7:
            recent_week = df.tail(7)
            previous_week = df.iloc[-14:-7] if len(df) >= 14 else df.head(len(df)-7)
            
            comparison = {
                'recent_week': {
                    'total_records': int(recent_week['count'].sum()) if 'count' in recent_week.columns else 0,
                    'avg_daily': round(recent_week['count'].mean(), 2) if 'count' in recent_week.columns else 0
                },
                'previous_week': {
                    'total_records': int(previous_week['count'].sum()) if 'count' in previous_week.columns else 0,
                    'avg_daily': round(previous_week['count'].mean(), 2) if 'count' in previous_week.columns else 0
                }
            }
            return comparison
        return {}
    except Exception as e:
        print(f"创建周期对比失败: {e}")
        return {}

def create_prediction_data(df, data_type):
    """创建预测数据"""
    try:
        if len(df) >= 3:
            # 简单的线性预测
            import numpy as np
            from sklearn.linear_model import LinearRegression
            
            X = np.arange(len(df)).reshape(-1, 1)
            y = df['count'].values if 'count' in df.columns else np.zeros(len(df))
            
            model = LinearRegression().fit(X, y)
            future_X = np.arange(len(df), len(df) + 5).reshape(-1, 1)
            predicted_values = model.predict(future_X)
            
            # 确保预测值为正数
            predicted_values = np.maximum(predicted_values, 0)
            
            return {
                'predicted_values': predicted_values.round(2).tolist(),
                'confidence_interval': [0.8] * len(predicted_values)
            }
        return {}
    except Exception as e:
        print(f"创建预测数据失败: {e}")
        return {}

def generate_recommendations(summary, data_type):
    """生成建议"""
    recommendations = []
    
    try:
        if data_type == 'medical':
            if summary.get('avg_systolic', 0) > 130:
                recommendations.append("平均收缩压偏高，建议加强血压监测和干预")
            if summary.get('avg_blood_sugar', 0) > 6.1:
                recommendations.append("平均血糖偏高，建议关注血糖控制")
        else:
            if summary.get('avg_systolic', 0) > 130:
                recommendations.append("孕产妇血压偏高，建议加强孕期监护")
            if summary.get('avg_fetal_heart_rate', 0) > 160:
                recommendations.append("胎心率偏高，建议进一步检查")
        
        if summary.get('total_records', 0) < 100:
            recommendations.append("数据样本量较少，建议增加数据收集")
        
        if not recommendations:
            recommendations.append("各项指标正常，继续保持良好的健康管理")
        
        return recommendations
    except Exception as e:
        print(f"生成建议失败: {e}")
        return ["数据分析完成，请关注各项健康指标"]

@analysis_bp.route('/analysis/model-info', methods=['GET'])
def get_model_info():
    """获取模型信息"""
    try:
        model_type = request.args.get('model_type', 'disease_risk')
        data_type = request.args.get('data_type', '')
        algorithm = request.args.get('algorithm', 'random_forest')
        
        # 模拟模型信息数据
        model_info = {
            'model_name': f'{model_type}_model',
            'algorithm': algorithm,
            'accuracy': 0.85,
            'precision': 0.82,
            'recall': 0.88,
            'f1_score': 0.85,
            'training_samples': 1000,
            'test_samples': 200,
            'created_at': '2024-01-01',
            'last_updated': '2024-01-15'
        }
        
        # 模拟特征重要性数据
        feature_importance = {
            'features': ['年龄', '收缩压', '舒张压', '心率', '血糖', '体重指数'],
            'importance': [0.25, 0.20, 0.18, 0.15, 0.12, 0.10]
        }
        
        # 模拟混淆矩阵数据
        confusion_matrix = {
            'xAxis': ['预测阴性', '预测阳性'],
            'yAxis': ['实际阴性', '实际阳性'],
            'data': [
                [0, 0, 80],
                [0, 1, 15],
                [1, 0, 10],
                [1, 1, 95]
            ]
        }
        
        # 模拟ROC曲线数据
        roc_curve = {
            'roc_data': [
                [0.0, 0.0],
                [0.1, 0.35],
                [0.2, 0.55],
                [0.3, 0.70],
                [0.4, 0.80],
                [0.5, 0.85],
                [0.6, 0.89],
                [0.7, 0.92],
                [0.8, 0.95],
                [0.9, 0.98],
                [1.0, 1.0]
            ]
        }
        
        # 模拟学习曲线数据
        learning_curve = {
            'train_scores': [0.75, 0.80, 0.83, 0.85, 0.86],
            'test_scores': [0.70, 0.78, 0.82, 0.84, 0.85],
            'train_sizes': [200, 400, 600, 800, 1000]
        }
        
        # 模拟预测分布数据
        prediction_distribution = {
            'categories': ['低风险', '中风险', '高风险'],
            'values': [120, 60, 20]
        }
        
        return jsonify({
            'code': 200,
            'message': '获取模型信息成功',
            'data': {
                'model_info': model_info,
                'feature_importance': feature_importance,
                'confusion_matrix': confusion_matrix,
                'roc_curve': roc_curve,
                'learning_curve': learning_curve,
                'prediction_distribution': prediction_distribution
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取模型信息失败: {str(e)}',
            'data': None
        }), 500
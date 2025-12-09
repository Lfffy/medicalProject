from flask import Flask,request,jsonify,render_template,send_from_directory,redirect,session,url_for,flash,send_file
from flask_cors import CORS
from flask_socketio import SocketIO
from utils.getAllData import *
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'medical_data_analysis_secret_key_2024'  # 设置密钥
CORS(app)  # 启用CORS支持

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', 
                   ping_timeout=60, ping_interval=25, 
                   transports=['websocket', 'polling'],
                   allow_upgrades=True,
                   engineio_logger=False)
from utils.getPublicData import *

# 导入数据管理API蓝图
from data_management_api import data_bp

# 导入分析API蓝图
from analysis_api import analysis_bp

# 导入孕产妇专项功能API蓝图
from maternal_api import maternal_bp

# 导入用户管理API蓝图
from user_api import user_bp

# 导入权限管理API蓝图
from permission_api import permission_bp

# 导入操作日志API蓝图
from log_api import log_bp

# 导入医院管理API蓝图
from hospital_api import hospital_bp

# 导入监控API蓝图
from monitoring_api import monitoring_bp

# 导入机器学习API蓝图（已注释，因为模块不存在）
# from ml_api import ml_bp

# 导入孕产妇风险预测API蓝图
from maternal_risk_api import maternal_risk_bp

# 导入预警API蓝图
from warning_api import warning_bp

# 导入营养建议API蓝图
from nutrition_api import nutrition_bp

# 注册数据管理API蓝图
app.register_blueprint(data_bp)

# 注册分析API蓝图
app.register_blueprint(analysis_bp)

# 注册孕产妇专项功能API蓝图
app.register_blueprint(maternal_risk_bp, name='unique_maternal_risk_bp')

# 注册用户管理API蓝图
app.register_blueprint(user_bp)

# 注册权限管理API蓝图
app.register_blueprint(permission_bp)

# 注册操作日志API蓝图
app.register_blueprint(log_bp)

# 注册医院管理API蓝图
app.register_blueprint(hospital_bp)

# 注册监控API蓝图
app.register_blueprint(monitoring_bp)

# 注册机器学习API蓝图（已注释，因为模块不存在）
# app.register_blueprint(ml_bp)

# 注册预警API蓝图
app.register_blueprint(warning_bp)

# 注册营养建议API蓝图
app.register_blueprint(nutrition_bp)

# 初始化AI聊天服务
from ai_chat_service import init_ai_chat_service
ai_chat_service = init_ai_chat_service(socketio)

# 初始化机器学习预测器（从maternal_risk_api导入现有实例）
from maternal_risk_api import predictor
# 验证预测器状态
if predictor is None:
    print("预测器未正确初始化")
else:
    print("预测器初始化成功")

# SQLite数据库配置
import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'medical_system.db')

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
    return conn

def init_database():
    """初始化数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建权限表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        permission_name TEXT UNIQUE NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建用户权限关联表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        permission_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (permission_id) REFERENCES permissions (id)
    )
    ''')
    
    # 创建操作日志表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS operation_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        operation_type TEXT NOT NULL,
        operation_detail TEXT,
        ip_address TEXT,
        user_agent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # 创建医疗数据表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        systolic_pressure INTEGER,
        diastolic_pressure INTEGER,
        disease_type TEXT,
        symptoms TEXT,
        diagnosis TEXT,
        treatment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建疾病分析表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disease_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease_name TEXT NOT NULL,
        disease_category TEXT,
        incidence_rate REAL,
        mortality_rate REAL,
        age_group TEXT,
        gender_distribution TEXT,
        risk_factors TEXT,
        symptoms TEXT,
        treatment_methods TEXT,
        prevention_methods TEXT,
        analysis_date DATE,
        data_source TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建数据统计表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data_statistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stat_type TEXT NOT NULL,
        stat_date DATE NOT NULL,
        total_patients INTEGER DEFAULT 0,
        new_patients INTEGER DEFAULT 0,
        disease_counts TEXT, -- JSON格式存储疾病统计
        department_stats TEXT, -- JSON格式存储科室统计
        age_distribution TEXT, -- JSON格式存储年龄分布
        gender_distribution TEXT, -- JSON格式存储性别分布
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建孕产妇信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maternal_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gestational_weeks INTEGER,
        pregnancy_count INTEGER,
        parity INTEGER,
        pregnancy_type TEXT,
        weight REAL,
        height REAL,
        systolic_pressure INTEGER,
        diastolic_pressure INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("数据库初始化完成")

# 初始化数据库
try:
    init_database()
except Exception as e:
    print(f"数据库初始化失败: {e}")

# 训练模型 - 暂时注释掉，因为getData和model_train函数未定义
# try:
#     trainData = getData()
#     model = model_train(trainData)
# except Exception as e:
#     print(f"模型训练失败: {e}")
#     model = None


@app.route('/')
def index():
    """系统主页面 - 重定向到医院管理页面"""
    return redirect('/hospital_management')

@app.route('/getHomeData',methods=['GET','POST'])
def getHomeData():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取总患者数
        cursor.execute("SELECT COUNT(*) as count FROM medical_data")
        total_patients = cursor.fetchone()['count']
        
        # 获取今日新增患者数
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) as count FROM medical_data WHERE DATE(created_at) = ?", (today,))
        new_patients = cursor.fetchone()['count']
        
        # 获取最常见疾病
        cursor.execute("""
            SELECT diagnosis, COUNT(*) as count 
            FROM medical_data 
            WHERE diagnosis IS NOT NULL AND diagnosis != ''
            GROUP BY diagnosis 
            ORDER BY count DESC 
            LIMIT 1
        """)
        most_common_disease = cursor.fetchone()
        common_disease = most_common_disease['diagnosis'] if most_common_disease else '暂无数据'
        
        # 获取最繁忙科室
        # 获取最繁忙科室（使用disease_type代替department）
        cursor.execute("""
            SELECT disease_type as department, COUNT(*) as count 
            FROM medical_data 
            WHERE disease_type IS NOT NULL AND disease_type != ''
            GROUP BY disease_type 
            ORDER BY count DESC 
            LIMIT 1
        """)
        busiest_department = cursor.fetchone()
        busy_department = busiest_department['department'] if busiest_department else '暂无数据'
        
        # 获取年龄统计
        cursor.execute("SELECT MAX(age) as max_age, MIN(age) as min_age FROM medical_data WHERE age IS NOT NULL")
        age_stats = cursor.fetchone()
        max_age = age_stats['max_age'] if age_stats['max_age'] else 0
        min_age = age_stats['min_age'] if age_stats['min_age'] else 0
        
        # 获取最常见医院（由于没有hospital字段，使用默认值）
        common_hospital = '暂无数据'
        
        # 获取疾病类型分布（用于饼图）
        cursor.execute("""
            SELECT diagnosis as name, COUNT(*) as value 
            FROM medical_data 
            WHERE diagnosis IS NOT NULL AND diagnosis != ''
            GROUP BY diagnosis 
            ORDER BY value DESC 
            LIMIT 10
        """)
        pieData = [dict(row) for row in cursor.fetchall()]
        
        # 获取性别分布
        cursor.execute("""
            SELECT gender as name, COUNT(*) as value 
            FROM medical_data 
            WHERE gender IS NOT NULL AND gender != ''
            GROUP BY gender
        """)
        gender_distribution = [dict(row) for row in cursor.fetchall()]
        boyList = [item for item in gender_distribution if item['name'] == '男']
        girlList = [item for item in gender_distribution if item['name'] == '女']
        ratioData = gender_distribution
        
        # 获取年龄分布
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN age < 18 THEN '0-17岁'
                    WHEN age < 30 THEN '18-29岁'
                    WHEN age < 40 THEN '30-39岁'
                    WHEN age < 50 THEN '40-49岁'
                    WHEN age < 60 THEN '50-59岁'
                    ELSE '60岁以上'
                END as age_group,
                COUNT(*) as value
            FROM medical_data 
            WHERE age IS NOT NULL
            GROUP BY age_group
            ORDER BY age_group
        """)
        age_distribution = [dict(row) for row in cursor.fetchall()]
        
        # 获取最新病例数据（用于表格显示）
        cursor.execute("""
            SELECT name as patient_name, diagnosis, gender, age, height, weight, 
                   systolic_pressure || '/' || diastolic_pressure as blood_pressure
            FROM medical_data 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        casesData = [dict(row) for row in cursor.fetchall()]
        
        # 获取科室统计（用于circleData，使用disease_type代替department）
        cursor.execute("""
            SELECT disease_type as name, COUNT(*) as value 
            FROM medical_data 
            WHERE disease_type IS NOT NULL AND disease_type != ''
            GROUP BY disease_type 
            ORDER BY value DESC
        """)
        circleData = [dict(row) for row in cursor.fetchall()]
        
        # 获取体重和血压数据
        cursor.execute("""
            SELECT name as xData, weight as y1Data, 
                   systolic_pressure || '/' || diastolic_pressure as y2Data
            FROM medical_data 
            WHERE weight IS NOT NULL AND systolic_pressure IS NOT NULL 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        body_data = cursor.fetchall()
        xData = [row['xData'] for row in body_data]
        y1Data = [row['y1Data'] for row in body_data]
        y2Data = [int(row['y2Data'].split('/')[0]) if '/' in str(row['y2Data']) else 0 for row in body_data]
        
        conn.close()
        
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'pieData': pieData,
                'configOne': circleData[:5],  # 取前5个科室作为配置数据
                'casesData': casesData,
                'maxNum': total_patients,
                'maxType': common_disease,
                'maxDep': busy_department,
                'maxHos': common_hospital,
                'maxAge': max_age,
                'minAge': min_age,
                'boyList': boyList,
                'girlList': girlList,
                'ratioData': ratioData,
                'circleData': circleData,
                'wordData': circleData,  # 使用科室数据作为词云数据
                'lastData': {
                    'xData': xData,
                    'y1Data': y1Data,
                    'y2Data': y2Data
                },
                'isMaternalData': False  # 默认不是孕产妇数据
            }
        })
        
    except Exception as e:
        print(f"获取首页数据失败: {e}")
        return jsonify({
            'message': f'获取数据失败: {str(e)}',
            'code': 500,
            'data': {
                'pieData': [],
                'configOne': [],
                'casesData': [],
                'maxNum': 0,
                'maxType': '暂无数据',
                'maxDep': '暂无数据',
                'maxHos': '暂无数据',
                'maxAge': 0,
                'minAge': 0,
                'boyList': [],
                'girlList': [],
                'ratioData': [],
                'circleData': [],
                'wordData': [],
                'lastData': {
                    'xData': [],
                    'y1Data': [],
                    'y2Data': []
                },
                'isMaternalData': False
            }
        })

# 添加专门的孕产妇健康数据API接口
@app.route('/getMaternalHealthData', methods=['GET', 'POST'])
def getMaternalHealthData():
    """专门获取孕产妇健康数据的接口"""
    try:
        maternalData = getMaternalCasesData()
        
        # 导入风险预测器
        from maternal_risk_predictor import MaternalRiskPredictor
        predictor = MaternalRiskPredictor()
        
        # 为每个孕产妇记录生成风险评估
        for case in maternalData:
            try:
                # 准备预测所需的数据，使用maternal_info表中的实际字段名
                patient_data = {
                    'age': case.get('age', 25),  # 从表中直接获取年龄
                    'systolic_pressure': case.get('systolic_pressure', 120),  # 获取收缩压
                    'diastolic_pressure': case.get('diastolic_pressure', 80),  # 获取舒张压
                    'current_gestational_week': case.get('gestational_weeks', 0),  # 使用正确的字段名
                    'parity': case.get('parity', 0),
                    'gravidity': case.get('pregnancy_count', 0),  # 使用正确的字段名
                    'previous_cesarean': '剖宫产' in case.get('notes', '') or '剖腹产' in case.get('notes', ''),  # 从notes中推断
                    'pregnancy_complications': case.get('notes', '')  # 使用notes字段存储并发症信息
                }
                
                # 执行综合风险评估
                risk_result = predictor.predict_comprehensive_risk(patient_data)
                
                # 更新记录的风险信息
                if risk_result:
                    # 正确提取各风险类型的风险分数和信息
                    case['risk_prediction'] = {
                        'gestational_diabetes_risk': risk_result.get('gestational_diabetes', {}).get('risk_score', 0) / 100,  # 转换为小数
                        'preeclampsia_risk': risk_result.get('preeclampsia', {}).get('risk_score', 0) / 100,
                        'preterm_birth_risk': risk_result.get('preterm_birth', {}).get('risk_score', 0) / 100,
                        'overall_risk_level': risk_result.get('overall_risk_level', '低风险'),
                        'risk_factors': [factor.get('name', '') for factor in risk_result.get('top_risk_factors', [])],
                        'recommendations': risk_result.get('recommendations', [])
                    }
                    # 更新risk_level字段以保持向后兼容
                    case['risk_level'] = risk_result.get('overall_risk_level', '低风险')
                else:
                    # 如果预测失败，使用基于规则的简单风险评估
                    case['risk_prediction'] = {
                        'gestational_diabetes_risk': 0.05,
                        'preeclampsia_risk': 0.05,
                        'preterm_birth_risk': 0.05,
                        'overall_risk_level': '低风险',
                        'risk_factors': [],
                        'recommendations': []
                    }
            except Exception as e:
                print(f"对孕产妇 {case.get('name', 'Unknown')} 进行风险评估时出错: {e}")
                # 出错时设置默认值
                case['risk_prediction'] = {
                    'gestational_diabetes_risk': 0.05,
                    'preeclampsia_risk': 0.05,
                    'preterm_birth_risk': 0.05,
                    'overall_risk_level': '低风险',
                    'risk_factors': [],
                    'recommendations': []
                }
        
        # 统计分析
        total_cases = len(maternalData)
        
        # 风险等级统计
        risk_stats = {}
        for case in maternalData:
            risk = case.get('risk_level', '未知')
            risk_stats[risk] = risk_stats.get(risk, 0) + 1
        
        # 孕周分布
        week_stats = {'早期(<12周)': 0, '中期(12-28周)': 0, '晚期(>28周)': 0}
        for case in maternalData:
            week = case.get('gestational_week', 0)
            if week < 12:
                week_stats['早期(<12周)'] += 1
            elif week <= 28:
                week_stats['中期(12-28周)'] += 1
            else:
                week_stats['晚期(>28周)'] += 1
        
        # 年龄分布
        age_stats = {'20-25岁': 0, '26-30岁': 0, '31-35岁': 0, '35岁以上': 0}
        for case in maternalData:
            age = case.get('age', 0)
            if 20 <= age <= 25:
                age_stats['20-25岁'] += 1
            elif 26 <= age <= 30:
                age_stats['26-30岁'] += 1
            elif 31 <= age <= 35:
                age_stats['31-35岁'] += 1
            elif age > 35:
                age_stats['35岁以上'] += 1
        
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'totalCases': total_cases,
                'riskStats': risk_stats,
                'weekStats': week_stats,
                'ageStats': age_stats,
                'maternalData': maternalData
            }
        })
    except Exception as e:
        print(f"获取孕产妇健康数据时出错: {e}")
        return jsonify({
            'message': f'获取数据失败: {str(e)}',
            'code': 500
        })

@app.route('/submitModel',methods=['GET','POST'])
def submitModel():
    try:
        params = request.json
        # 判断请求是否包含孕产妇特征参数
        is_maternal_request = 'gestational_week' in params or 'pregnancy_type' in params
        
        if is_maternal_request:
            # 孕产妇风险评估
            # 获取必要参数
            age = int(params.get('age', 0))
            gestational_week = int(params.get('gestational_week', 0))
            weight = float(params.get('weight', 0))
            blood_pressure = params.get('blood_pressure', '0/0')
            pregnancy_type = params.get('pregnancy_type', '单胎')
            medical_history = params.get('medical_history', '')
            
            # 提取血压值
            systolic = 0
            diastolic = 0
            try:
                bp_values = blood_pressure.split('/')
                systolic = int(bp_values[0])
                diastolic = int(bp_values[1])
            except:
                pass
            
            # 风险评估逻辑
            risk_level = '低风险'
            risk_factors = []
            
            # 年龄风险
            if age < 18 or age > 35:
                risk_factors.append('年龄异常')
            
            # 血压风险
            if systolic > 140 or diastolic > 90:
                risk_factors.append('高血压')
                risk_level = '高风险'
            
            # 孕周风险
            if gestational_week < 12 and age > 35:
                risk_factors.append('高龄早期妊娠')
                risk_level = '中风险'
            elif gestational_week > 37 and systolic > 130:
                risk_factors.append('晚期妊娠高血压倾向')
                risk_level = '中风险'
            
            # 妊娠类型风险
            if pregnancy_type in ['双胎', '多胎']:
                risk_factors.append('多胎妊娠')
                risk_level = '中风险'
            
            # 病史风险
            if '糖尿病' in medical_history or '高血压' in medical_history:
                risk_factors.append('慢性病病史')
                risk_level = '高风险'
            
            # 生成描述
            description = f"孕期风险评估结果：{risk_level}。"
            if risk_factors:
                description += f"风险因素：{', '.join(risk_factors)}。"
                description += "建议增加产检频率，密切关注自身健康状况。"
            else:
                description += "孕期状况良好，请继续保持健康的生活方式，定期进行产检。"
            
            result = risk_level
        else:
            # 原有医疗疾病预测逻辑
            if model is None:
                return jsonify({
                    'message': '预测模型未初始化',
                    'code': 500
                })
            
            # 获取参数（从JSON请求体中获取）
            content = request.json.get('content') if request.is_json else request.args.get('content')
            # 预测
            result = pred(model, content)
            description = f"预测结果：{result}"
        
        # 构造返回数据
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'result': result,
                'description': description,
                'isMaternal': is_maternal_request
            }
        })
    except Exception as e:
        print(f"预测过程中出错: {e}")
        return jsonify({
            'message': f'预测失败: {str(e)}',
            'code': 500
        })

@app.route('/help')
def help_docs():
    """帮助文档页面"""
    return render_template('help.html')

@app.route('/api/help/docs')
def get_help_docs():
    """获取帮助文档内容API"""
    try:
        import os
        import json
        
        # 定义文档文件路径
        docs_dir = os.path.dirname(__file__)
        doc_files = {
            'database': '数据库表完整信息.md',
            'system': '数据库完整文档.md'
        }
        
        help_data = {}
        
        for doc_key, filename in doc_files.items():
            file_path = os.path.join(docs_dir, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        help_data[doc_key] = {
                            'title': content.split('\n')[0].replace('#', '').strip(),
                            'content': content,
                            'filename': filename
                        }
                except Exception as e:
                    print(f"读取文档 {filename} 失败: {e}")
                    help_data[doc_key] = {
                        'title': f'{doc_key}文档',
                        'content': f'文档加载失败: {str(e)}',
                        'filename': filename
                    }
            else:
                help_data[doc_key] = {
                    'title': f'{doc_key}文档',
                    'content': f'文档文件 {filename} 不存在',
                    'filename': filename
                }
        
        # 添加系统使用指南
        help_data['guide'] = {
            'title': '系统使用指南',
            'content': '''# 医疗疾病数据分析大屏可视化系统 - 使用指南

## 🎯 系统概述
本系统是一个专业的医疗数据分析平台，提供全面的数据可视化、分析和管理功能。

## 📋 主要功能模块

### 1. 认证中心
- 用户登录和权限管理
- 安全认证和会话管理

### 2. 数据中心
- 医疗数据查看和管理
- 数据导入导出功能
- 数据质量监控

### 3. 分析中心
- 疾病趋势分析
- 数据统计和报表
- 预测模型分析

### 4. 监测中心
- 实时数据监控
- 异常数据预警
- 系统状态监测

### 5. 大屏中心
- 数据可视化大屏
- 实时数据展示
- 多维度数据分析

## 🚀 快速开始

1. **登录系统**: 使用您的用户名和密码登录
2. **选择模块**: 根据需要选择相应的功能模块
3. **查看数据**: 在数据中心查看和管理医疗数据
4. **分析数据**: 使用分析中心进行深度数据分析
5. **监控大屏**: 在大屏中心查看实时数据可视化

## 📞 技术支持
如有问题，请联系系统管理员或查看详细的技术文档。
''',
            'filename': 'guide.md'
        }
        
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': help_data
        })
        
    except Exception as e:
        print(f"获取帮助文档时出错: {e}")
        return jsonify({
            'message': f'获取帮助文档失败: {str(e)}',
            'code': 500,
            'data': {}
        })

@app.route('/hospital_management')
def hospital_management():
    """医院管理页面"""
    return render_template('hospital_management.html')

@app.route('/tableData',methods=['GET','POST'])
def tableData():
    try:
        print("开始处理tableData请求...")
        
        # 直接查询cases表获取数据
        from utils.query import querys
        cases_data = querys('select * from cases')
        
        print(f"从cases表获取到{len(cases_data) if cases_data else 0}条记录")
        
        # 转换数据格式为二维数组
        rows = []
        
        if cases_data and len(cases_data) > 0:
            is_maternal_data = False
            
            for row in cases_data:
                # 确保row是字典格式
                if hasattr(row, 'keys'):
                    row_dict = dict(row)
                elif hasattr(row, '__iter__'):
                    # 如果是元组，手动创建字典
                    columns = ['id', 'type', 'gender', 'age', 'time', 'description', 'doctor', 
                              'hospital', 'department', 'details_link', 'height', 'weight', 
                              'duration', 'allergy_history', 'created_at', 'updated_at']
                    row_dict = {columns[i]: row[i] for i in range(min(len(columns), len(row)))} if len(row) > 0 else {}
                else:
                    row_dict = {}
                
                # 构建表格行数据
                table_row = [
                    row_dict.get('type', ''),
                    '男' if row_dict.get('gender', 1) == 1 else '女',
                    str(row_dict.get('age', '')),
                    row_dict.get('time', row_dict.get('created_at', '')),
                    row_dict.get('description', ''),
                    row_dict.get('doctor', ''),
                    row_dict.get('hospital', ''),
                    row_dict.get('department', ''),
                    row_dict.get('details_link', ''),
                    str(row_dict.get('height', '')) if row_dict.get('height') is not None else '',
                    str(row_dict.get('weight', '')) if row_dict.get('weight') is not None else '',
                    str(row_dict.get('duration', '')) + '天' if row_dict.get('duration') is not None else '',
                    row_dict.get('allergy_history', '')
                ]
                # 确保所有字段都是字符串且不为None
                table_row = [str(cell) if cell is not None else '' for cell in table_row]
                rows.append(table_row)
        else:
            # 如果没有数据，提供友好提示
            rows = [["暂无数据", "", "", "", "", "", "", "", "", "", "", "", ""]]
            is_maternal_data = False
        
        print(f"最终处理的表格数据行数: {len(rows)}")
        
        # 固定表头
        headers = ['类型', '性别', '年龄', '时间', '描述', '医生', '医院', '科室', '详情链接', '身高', '体重', '患病时长', '过敏史']
        
        # 返回标准格式数据
        response = {
            'data': {
                'isMaternal': is_maternal_data,
                'rows': rows,
                'headers': headers
            }
        }
        
        print("准备返回tableData响应")
        return jsonify(response)
    except Exception as e:
        print(f"获取表格数据时出错: {e}")
        return jsonify({
            'data': {
                'isMaternal': False,
                'rows': [["获取数据失败"]],
                'headers': ['错误信息'],
                'rowMapping': {}
            }
        })



# 胎儿监护相关API端点
@app.route('/api/fetal-monitoring/records', methods=['GET'])
def get_fetal_monitoring_records():
    """获取胎儿监护记录"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        patient_name = request.args.get('patient_name', '')
        hospital = request.args.get('hospital', '')
        monitoring_status = request.args.get('monitoring_status', '')
        
        # 模拟数据
        total = 20
        records = []
        for i in range((page-1)*page_size, min(page*page_size, total)):
            records.append({
                'id': i + 1,
                'patient_name': f'患者{i+1}',
                'hospital': '妇产科医院',
                'monitoring_date': '2024-01-15',
                'gestational_week': 32,
                'fetal_heart_rate': 145,
                'amniotic_fluid': '正常',
                'placenta': '前壁',
                'monitoring_status': '正常',
                'doctor': '张医生'
            })
        
        return jsonify({
            'code': 200,
            'message': '获取胎儿监护记录成功',
            'data': {
                'records': records,
                'total': total,
                'page': page,
                'page_size': page_size
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取胎儿监护记录失败: {str(e)}'
        }), 500

@app.route('/api/fetal-monitoring/statistics', methods=['GET'])
def get_fetal_monitoring_statistics():
    """获取胎儿监护统计数据"""
    try:
        # 模拟统计数据
        statistics = {
            'total_monitoring': 156,
            'normal_cases': 132,
            'abnormal_cases': 24,
            'high_risk_cases': 8,
            'week_distribution': {
                '28-32周': 45,
                '32-36周': 67,
                '36周以上': 44
            },
            'daily_trend': [
                {'date': '01-10', 'count': 12},
                {'date': '01-11', 'count': 15},
                {'date': '01-12', 'count': 18},
                {'date': '01-13', 'count': 14},
                {'date': '01-14', 'count': 16},
                {'date': '01-15', 'count': 20}
            ]
        }
        
        return jsonify({
            'code': 200,
            'message': '获取胎儿监护统计数据成功',
            'data': statistics
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取胎儿监护统计数据失败: {str(e)}'
        }), 500

@app.route('/api/fetal-monitoring/start', methods=['POST'])
def start_fetal_monitoring():
    """开始胎儿监护会话"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 模拟开始监护会话
        monitoring_session = {
            'session_id': f'monitor-{int(time.time())}',
            'maternal_id': data.get('maternal_id', 0),
            'patient_name': data.get('patient_name', ''),
            'start_time': datetime.now().isoformat(),
            'gestational_week': data.get('gestational_week', 0),
            'status': 'active',
            'initial_data': {
                'fetal_heart_rate': 140,
                'fetal_movement': 0,
                'uterine_contractions': 0
            }
        }
        
        return jsonify({
            'code': 200,
            'message': '胎儿监护会话已成功开始',
            'data': monitoring_session
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'开始胎儿监护会话失败: {str(e)}'
        }), 500

# 启动应用
if __name__ == '__main__':
    print("医疗数据分析系统启动中...")
    print("请访问: http://localhost:8081")
    app.run(debug=True, host='0.0.0.0', port=8081)

from flask import Blueprint, request, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建蓝图
maternal_bp = Blueprint('maternal', __name__, url_prefix='/api/maternal')

# SQLite数据库配置
DB_PATH = os.path.join(os.path.dirname(__file__), 'medical_data.db')

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        raise

def calculate_risk_score(data):
    """计算孕产妇健康风险评分"""
    risk_score = 0
    risk_factors = []
    
    # 年龄风险
    age = int(data.get('age', 0))
    if age >= 35:
        risk_score += 20
        risk_factors.append("高龄产妇")
    elif age < 18:
        risk_score += 15
        risk_factors.append("低龄产妇")
    
    # 孕周风险
    gestational_week = int(data.get('gestationalWeek', 0))
    if gestational_week < 12:
        risk_score += 5
    elif gestational_week > 42:
        risk_score += 15
        risk_factors.append("过期妊娠")
    
    # BMI风险
    height = float(data.get('height', 0))
    weight = float(data.get('weight', 0))
    if height > 0:
        bmi = weight / ((height/100) ** 2)
        if bmi < 18.5:
            risk_score += 10
            risk_factors.append("体重过轻")
        elif bmi > 30:
            risk_score += 15
            risk_factors.append("肥胖")
    
    # 血压风险
    vital_signs = data.get('vitalSigns', {})
    systolic = int(vital_signs.get('systolic', 0))
    diastolic = int(vital_signs.get('diastolic', 0))
    if systolic >= 140 or diastolic >= 90:
        risk_score += 20
        risk_factors.append("高血压")
    elif systolic >= 130 or diastolic >= 80:
        risk_score += 10
        risk_factors.append("血压偏高")
    
    # 病史风险
    medical_history = data.get('medicalHistory', {})
    chronic_diseases = medical_history.get('chronicDiseases', {})
    if chronic_diseases.get('hypertension', 0) == 1:
        risk_score += 15
        risk_factors.append("慢性高血压")
    if chronic_diseases.get('diabetes', 0) == 1:
        risk_score += 15
        risk_factors.append("糖尿病")
    if chronic_diseases.get('cardiovascular', 0) == 1:
        risk_score += 20
        risk_factors.append("心血管疾病")
    
    # 妊娠史风险
    pregnancy_history = medical_history.get('pregnancyHistory', {})
    if pregnancy_history.get('preeclampsia', 0) == 1:
        risk_score += 25
        risk_factors.append("子痫前期史")
    if pregnancy_history.get('gestationalDiabetes', 0) == 1:
        risk_score += 15
        risk_factors.append("妊娠期糖尿病史")
    if pregnancy_history.get('preterm', 0) == 1:
        risk_score += 10
        risk_factors.append("早产史")
    
    # 生活习惯风险
    lifestyle = data.get('lifestyle', {})
    if lifestyle.get('smoking', 0) >= 1:
        risk_score += 15
        risk_factors.append("吸烟")
    if lifestyle.get('alcohol', 0) >= 1:
        risk_score += 10
        risk_factors.append("饮酒")
    if lifestyle.get('stressLevel', 0) >= 3:
        risk_score += 10
        risk_factors.append("高压力水平")
    
    # 限制风险评分在0-100范围内
    risk_score = min(100, max(0, risk_score))
    
    # 确定风险等级
    if risk_score <= 30:
        risk_level = "低风险"
    elif risk_score <= 60:
        risk_level = "中风险"
    else:
        risk_level = "高风险"
    
    return {
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "riskFactors": risk_factors
    }

def generate_complications(risk_score, data):
    """生成可能的并发症及概率"""
    complications = []
    
    # 妊娠高血压
    hypertension_prob = min(90, max(5, risk_score * 0.8))
    if data.get('vitalSigns', {}).get('systolic', 0) >= 130:
        hypertension_prob += 10
    
    complications.append({
        "id": "gestational_hypertension",
        "name": "妊娠高血压",
        "riskLevel": "low" if hypertension_prob < 30 else "medium" if hypertension_prob < 60 else "high",
        "riskText": "低风险" if hypertension_prob < 30 else "中风险" if hypertension_prob < 60 else "高风险",
        "probability": int(hypertension_prob),
        "description": f"基于当前健康指标，妊娠高血压的风险为{int(hypertension_prob)}%"
    })
    
    # 妊娠期糖尿病
    diabetes_prob = min(80, max(5, risk_score * 0.6))
    if data.get('medicalHistory', {}).get('chronicDiseases', {}).get('diabetes', 0) == 1:
        diabetes_prob += 20
    if data.get('age', 0) >= 35:
        diabetes_prob += 10
    
    complications.append({
        "id": "gestational_diabetes",
        "name": "妊娠期糖尿病",
        "riskLevel": "low" if diabetes_prob < 30 else "medium" if diabetes_prob < 60 else "high",
        "riskText": "低风险" if diabetes_prob < 30 else "中风险" if diabetes_prob < 60 else "高风险",
        "probability": int(diabetes_prob),
        "description": f"基于当前健康指标，妊娠期糖尿病的风险为{int(diabetes_prob)}%"
    })
    
    # 早产
    preterm_prob = min(70, max(5, risk_score * 0.5))
    if data.get('medicalHistory', {}).get('pregnancyHistory', {}).get('preterm', 0) == 1:
        preterm_prob += 25
    
    complications.append({
        "id": "preterm_birth",
        "name": "早产",
        "riskLevel": "low" if preterm_prob < 30 else "medium" if preterm_prob < 60 else "high",
        "riskText": "低风险" if preterm_prob < 30 else "中风险" if preterm_prob < 60 else "高风险",
        "probability": int(preterm_prob),
        "description": f"基于当前健康指标，早产的风险为{int(preterm_prob)}%"
    })
    
    return complications

def generate_recommendations(risk_level, risk_factors, data):
    """生成健康建议"""
    recommendations = []
    
    # 基础建议
    recommendations.append("保持均衡饮食，适量补充叶酸")
    recommendations.append("定期进行产检，监测血压和体重变化")
    recommendations.append("保持适度运动，如散步、孕妇瑜伽等")
    
    # 基于风险等级的建议
    if risk_level == "高风险":
        recommendations.append("增加产检频率，密切监测各项指标")
        recommendations.append("遵医嘱进行相关检查和治疗")
    
    # 基于风险因素的建议
    if "高龄产妇" in risk_factors:
        recommendations.append("高龄产妇需特别关注胎儿发育情况")
    
    if "高血压" in risk_factors or "血压偏高" in risk_factors:
        recommendations.append("控制盐分摄入，定期监测血压")
    
    if "肥胖" in risk_factors:
        recommendations.append("控制体重增长，避免过度增重")
    
    if "吸烟" in risk_factors:
        recommendations.append("立即戒烟，避免二手烟环境")
    
    if "饮酒" in risk_factors:
        recommendations.append("完全戒酒，避免任何酒精摄入")
    
    if "高压力水平" in risk_factors:
        recommendations.append("学习放松技巧，保持良好心态")
    
    return recommendations

@maternal_bp.route('/predict', methods=['POST'])
def predict_maternal_health():
    """孕产妇健康风险预测接口"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name', 'age', 'gestationalWeek']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({
                    'message': f'缺少必填字段: {field}',
                    'code': 400,
                    'data': None
                }), 400
        
        # 计算风险评分
        risk_assessment = calculate_risk_score(data)
        
        # 生成并发症
        complications = generate_complications(risk_assessment['riskScore'], data)
        
        # 生成建议
        recommendations = generate_recommendations(
            risk_assessment['riskLevel'], 
            risk_assessment['riskFactors'], 
            data
        )
        
        # 构建预测结果
        prediction = {
            "riskLevel": risk_assessment['riskLevel'],
            "riskScore": risk_assessment['riskScore'],
            "confidence": 85,  # 默认置信度
            "riskFactors": risk_assessment['riskFactors'],
            "complications": complications,
            "recommendations": recommendations
        }
        
        # 构建描述文本
        description = f"孕期风险评估结果：{risk_assessment['riskLevel']}。"
        if risk_assessment['riskLevel'] == "低风险":
            description += "孕期状况良好，请继续保持健康的生活方式，定期进行产检。"
        elif risk_assessment['riskLevel'] == "中风险":
            description += "存在一定风险因素，建议加强孕期监测，遵医嘱进行相关检查。"
        else:
            description += "存在较高风险，请务必遵医嘱进行密切监测和必要干预。"
        
        # 返回结果
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'result': risk_assessment['riskLevel'],
                'description': description,
                'isMaternal': True,
                'prediction': prediction
            }
        })
        
    except Exception as e:
        logger.error(f"孕产妇健康风险预测失败: {e}")
        return jsonify({
            'message': f'预测失败: {str(e)}',
            'code': 500,
            'data': None
        }), 500

@maternal_bp.route('/history', methods=['GET'])
def get_prediction_history():
    """获取历史预测记录"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        name = request.args.get('name', '')
        start_date = request.args.get('startDate', '')
        end_date = request.args.get('endDate', '')
        risk_level = request.args.get('riskLevel', '')
        
        # 计算偏移量
        offset = (page - 1) * limit
        
        # 连接数据库
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if name:
            where_conditions.append("name LIKE ?")
            params.append(f'%{name}%')
        
        if start_date:
            where_conditions.append("created_at >= ?")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= ?")
            params.append(end_date)
        
        if risk_level:
            where_conditions.append("risk_level = ?")
            params.append(risk_level)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 查询总数
        count_query = f"SELECT COUNT(*) as total FROM maternal_predictions{where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # 查询数据
        query = f"""
        SELECT id, name, age, gestational_week, risk_level, risk_score, 
               created_at as prediction_date, confidence
        FROM maternal_predictions{where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """
        cursor.execute(query, params + [limit, offset])
        records = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        # 计算总页数
        pages = (total + limit - 1) // limit
        
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'records': records,
                'total': total,
                'page': page,
                'pages': pages
            }
        })
        
    except Exception as e:
        logger.error(f"获取历史预测记录失败: {e}")
        return jsonify({
            'message': f'获取历史记录失败: {str(e)}',
            'code': 500,
            'data': None
        }), 500

@maternal_bp.route('/prediction/<prediction_id>', methods=['GET'])
def get_prediction_details(prediction_id):
    """获取预测详情"""
    try:
        # 连接数据库
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 查询预测记录
        cursor.execute("""
        SELECT id, risk_level, risk_score, confidence, risk_factors, 
               complications, recommendations, input_data, created_at
        FROM maternal_predictions
        WHERE id = ?
        """, (prediction_id,))
        
        record = cursor.fetchone()
        if not record:
            cursor.close()
            connection.close()
            return jsonify({
                'message': '预测记录不存在',
                'code': 404,
                'data': None
            }), 404
        
        # 解析JSON字段
        risk_factors = json.loads(record['risk_factors']) if record['risk_factors'] else []
        complications = json.loads(record['complications']) if record['complications'] else []
        recommendations = json.loads(record['recommendations']) if record['recommendations'] else []
        input_data = json.loads(record['input_data']) if record['input_data'] else {}
        
        # 构建返回数据
        prediction = {
            'id': record['id'],
            'riskLevel': record['risk_level'],
            'riskScore': record['risk_score'],
            'confidence': record['confidence'],
            'riskFactors': risk_factors,
            'complications': complications,
            'recommendations': recommendations
        }
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'prediction': prediction,
                'inputData': input_data,
                'createdAt': record['created_at']
            }
        })
        
    except Exception as e:
        logger.error(f"获取预测详情失败: {e}")
        return jsonify({
            'message': f'获取预测详情失败: {str(e)}',
            'code': 500,
            'data': None
        }), 500

@maternal_bp.route('/save', methods=['POST'])
def save_prediction():
    """保存预测结果"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if 'prediction' not in data or 'inputData' not in data:
            return jsonify({
                'message': '缺少必填字段',
                'code': 400,
                'data': None
            }), 400
        
        prediction = data['prediction']
        input_data = data['inputData']
        
        # 连接数据库
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 检查表是否存在，不存在则创建
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS maternal_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gestational_week INTEGER,
            risk_level TEXT,
            risk_score INTEGER,
            confidence INTEGER,
            risk_factors TEXT,
            complications TEXT,
            recommendations TEXT,
            input_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 插入数据
        insert_query = """
        INSERT INTO maternal_predictions (
            name, age, gestational_week, risk_level, risk_score, confidence,
            risk_factors, complications, recommendations, input_data, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            input_data.get('name', ''),
            input_data.get('age', 0),
            input_data.get('gestationalWeek', 0),
            prediction.get('riskLevel', ''),
            prediction.get('riskScore', 0),
            prediction.get('confidence', 0),
            json.dumps(prediction.get('riskFactors', [])),
            json.dumps(prediction.get('complications', [])),
            json.dumps(prediction.get('recommendations', [])),
            json.dumps(input_data),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        cursor.execute(insert_query, values)
        connection.commit()
        
        record_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'id': record_id,
                'message': '保存成功'
            }
        })
        
    except Exception as e:
        logger.error(f"保存预测结果失败: {e}")
        return jsonify({
            'message': f'保存失败: {str(e)}',
            'code': 500,
            'data': None
        }), 500

@maternal_bp.route('/export', methods=['GET'])
def export_predictions():
    """导出预测数据"""
    try:
        import pandas as pd
        import tempfile
        from flask import send_file
        
        # 获取查询参数
        format_type = request.args.get('format', 'csv')
        start_date = request.args.get('startDate', '')
        end_date = request.args.get('endDate', '')
        risk_level = request.args.get('riskLevel', '')
        
        # 连接数据库
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if start_date:
            where_conditions.append("created_at >= ?")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= ?")
            params.append(end_date)
        
        if risk_level:
            where_conditions.append("risk_level = ?")
            params.append(risk_level)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 查询数据
        query = f"""
        SELECT id, name, age, gestational_week, risk_level, risk_score, 
               confidence, created_at
        FROM maternal_predictions{where_clause}
        ORDER BY created_at DESC
        """
        cursor.execute(query, params)
        data = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        if not data:
            return jsonify({
                'message': '没有数据可导出',
                'code': 404,
                'data': None
            }), 404
        
        # 转换为DataFrame
        df = pd.DataFrame(data)
        
        # 创建临时文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == 'excel':
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
            df.to_excel(temp_file.name, index=False)
            filename = f'maternal_predictions_{timestamp}.xlsx'
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
            df.to_csv(temp_file.name, index=False)
            filename = f'maternal_predictions_{timestamp}.csv'
            mimetype = 'text/csv'
        
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
    except Exception as e:
        logger.error(f"导出预测数据失败: {e}")
        return jsonify({
            'message': f'导出失败: {str(e)}',
            'code': 500,
            'data': None
        }), 500

@maternal_bp.route('/statistics', methods=['GET'])
def get_prediction_statistics():
    """获取统计信息"""
    try:
        # 获取查询参数
        period = request.args.get('period', 'monthly')
        start_date = request.args.get('startDate', '')
        end_date = request.args.get('endDate', '')
        
        # 连接数据库
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if start_date:
            where_conditions.append("created_at >= ?")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= ?")
            params.append(end_date)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 总预测数
        cursor.execute(f"SELECT COUNT(*) as total FROM maternal_predictions{where_clause}")
        total_predictions = cursor.fetchone()[0]
        
        # 风险等级分布
        cursor.execute(f"""
        SELECT risk_level, COUNT(*) as count 
        FROM maternal_predictions{where_clause}
        GROUP BY risk_level
        """)
        risk_distribution = {row['risk_level']: row['count'] for row in cursor.fetchall()}
        
        # 年龄分布
        cursor.execute(f"""
        SELECT 
            CASE 
                WHEN age < 25 THEN '18-25'
                WHEN age < 30 THEN '26-30'
                WHEN age < 35 THEN '31-35'
                ELSE '36+'
            END as age_group,
            COUNT(*) as count
        FROM maternal_predictions{where_clause}
        GROUP BY age_group
        """)
        age_distribution = {row['age_group']: row['count'] for row in cursor.fetchall()}
        
        # 孕周分布
        cursor.execute(f"""
        SELECT 
            CASE 
                WHEN gestational_week <= 12 THEN '早期(1-12周)'
                WHEN gestational_week <= 27 THEN '中期(13-27周)'
                ELSE '晚期(28-40周)'
            END as gestational_period,
            COUNT(*) as count
        FROM maternal_predictions{where_clause}
        GROUP BY gestational_period
        """)
        gestational_week_distribution = {row['gestational_period']: row['count'] for row in cursor.fetchall()}
        
        # 常见风险因素
        cursor.execute(f"""
        SELECT risk_factors
        FROM maternal_predictions{where_clause}
        WHERE risk_factors IS NOT NULL AND risk_factors != '[]'
        """)
        
        risk_factors_count = {}
        for row in cursor.fetchall():
            factors = json.loads(row['risk_factors'])
            for factor in factors:
                if factor in risk_factors_count:
                    risk_factors_count[factor] += 1
                else:
                    risk_factors_count[factor] = 1
        
        # 转换为列表格式并排序
        common_risk_factors = [
            {"factor": factor, "count": count} 
            for factor, count in sorted(risk_factors_count.items(), key=lambda x: x[1], reverse=True)
        ]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'totalPredictions': total_predictions,
                'riskDistribution': risk_distribution,
                'ageDistribution': age_distribution,
                'gestationalWeekDistribution': gestational_week_distribution,
                'commonRiskFactors': common_risk_factors
            }
        })
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({
            'message': f'获取统计信息失败: {str(e)}',
            'code': 500,
            'data': None
        }), 500
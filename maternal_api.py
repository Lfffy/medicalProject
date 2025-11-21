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

@maternal_bp.route('/records', methods=['GET'])
def get_maternal_records():
    """获取孕产妇记录列表"""
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        keyword = request.args.get('keyword', '')
        gestational_weeks = request.args.get('gestational_weeks', '')
        pregnancy_type = request.args.get('pregnancy_type', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        offset = (page - 1) * size
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if keyword:
            where_conditions.append("(name LIKE ? OR notes LIKE ?)")
            params.extend([f'%{keyword}%', f'%{keyword}%'])
        
        if gestational_weeks:
            where_conditions.append("gestational_weeks = ?")
            params.append(gestational_weeks)
        
        if pregnancy_type:
            where_conditions.append("pregnancy_type = ?")
            params.append(pregnancy_type)
        
        if start_date:
            where_conditions.append("created_at >= ?")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= ?")
            params.append(end_date)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 查询总数
        count_query = f"SELECT COUNT(*) as total FROM maternal_info{where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # 查询数据
        query = f"""
        SELECT * FROM maternal_info{where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """
        cursor.execute(query, params + [size, offset])
        data = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': data,
            'total': total,
            'page': page,
            'size': size
        })
        
    except Exception as e:
        logger.error(f"获取孕产妇记录失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/record/<int:record_id>', methods=['GET'])
def get_maternal_record(record_id):
    """获取单个孕产妇记录详情"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM maternal_info WHERE id = ?", (record_id,))
        record = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if not record:
            return jsonify({'success': False, 'message': '记录不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': dict(record)
        })
        
    except Exception as e:
        logger.error(f"获取孕产妇记录详情失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/record', methods=['POST'])
def create_maternal_record():
    """创建孕产妇记录"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name', 'age', 'gestational_weeks', 'pregnancy_count', 'parity', 'pregnancy_type']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({'success': False, 'message': f'缺少必填字段: {field}'}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 插入数据
        insert_query = """
        INSERT INTO maternal_info (
            name, age, gestational_weeks, pregnancy_count, parity, pregnancy_type,
            weight, height, systolic_pressure, diastolic_pressure, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        current_time = datetime.now()
        values = (
            data['name'], data['age'], data['gestational_weeks'], data['pregnancy_count'],
            data['parity'], data['pregnancy_type'], data.get('weight'), data.get('height'),
            data.get('systolic_pressure'), data.get('diastolic_pressure'), data.get('notes'),
            current_time, current_time
        )
        
        cursor.execute(insert_query, values)
        connection.commit()
        
        record_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': '孕产妇记录创建成功',
            'data': {'id': record_id}
        })
        
    except Exception as e:
        logger.error(f"创建孕产妇记录失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/record/<int:record_id>', methods=['PUT'])
def update_maternal_record(record_id):
    """更新孕产妇记录"""
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 检查记录是否存在
        cursor.execute("SELECT id FROM maternal_info WHERE id = ?", (record_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': '记录不存在'}), 404
        
        # 构建更新字段
        update_fields = []
        update_values = []
        
        for field in ['name', 'age', 'gestational_weeks', 'pregnancy_count', 'parity', 
                     'pregnancy_type', 'weight', 'height', 'systolic_pressure', 
                     'diastolic_pressure', 'notes']:
            if field in data:
                update_fields.append(f"{field} = ?")
                update_values.append(data[field])
        
        if update_fields:
            update_fields.append("updated_at = ?")
            update_values.append(datetime.now())
            update_values.append(record_id)
            
            update_query = f"UPDATE maternal_info SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(update_query, update_values)
            connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'message': '孕产妇记录更新成功'})
        
    except Exception as e:
        logger.error(f"更新孕产妇记录失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/record/<int:record_id>', methods=['DELETE'])
def delete_maternal_record(record_id):
    """删除孕产妇记录"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 检查记录是否存在
        cursor.execute("SELECT name FROM maternal_info WHERE id = ?", (record_id,))
        record = cursor.fetchone()
        if not record:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': '记录不存在'}), 404
        
        # 删除记录
        cursor.execute("DELETE FROM maternal_info WHERE id = ?", (record_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'message': '孕产妇记录删除成功'})
        
    except Exception as e:
        logger.error(f"删除孕产妇记录失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/statistics', methods=['GET'])
def get_maternal_statistics():
    """获取孕产妇统计数据"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 总数统计
        cursor.execute("SELECT COUNT(*) as total FROM maternal_info")
        total_count = cursor.fetchone()[0]
        
        # 按孕周分布统计
        cursor.execute("""
        SELECT 
            CASE 
                WHEN gestational_weeks <= 12 THEN '早期(≤12周)'
                WHEN gestational_weeks <= 28 THEN '中期(13-28周)'
                ELSE '晚期(>28周)'
            END as gestational_period,
            COUNT(*) as count
        FROM maternal_info
        GROUP BY gestational_period
        ORDER BY MIN(gestational_weeks)
        """)
        gestational_distribution = [dict(row) for row in cursor.fetchall()]
        
        # 按妊娠类型统计
        cursor.execute("SELECT pregnancy_type, COUNT(*) as count FROM maternal_info GROUP BY pregnancy_type")
        pregnancy_type_distribution = [dict(row) for row in cursor.fetchall()]
        
        # 按年龄分布统计
        cursor.execute("""
        SELECT 
            CASE 
                WHEN age < 25 THEN '<25岁'
                WHEN age < 30 THEN '25-29岁'
                WHEN age < 35 THEN '30-34岁'
                ELSE '≥35岁'
            END as age_group,
            COUNT(*) as count
        FROM maternal_info
        GROUP BY age_group
        ORDER BY MIN(age)
        """)
        age_distribution = [dict(row) for row in cursor.fetchall()]
        
        # 今日新增统计
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) as today_count FROM maternal_info WHERE DATE(created_at) = ?", (today,))
        today_count = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total_count': total_count,
                'today_count': today_count,
                'gestational_distribution': gestational_distribution,
                'pregnancy_type_distribution': pregnancy_type_distribution,
                'age_distribution': age_distribution
            }
        })
        
    except Exception as e:
        logger.error(f"获取孕产妇统计失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/risk-analysis', methods=['GET'])
def get_risk_analysis():
    """获取孕产妇风险分析"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 高龄产妇统计（≥35岁）
        cursor.execute("SELECT COUNT(*) as count FROM maternal_info WHERE age >= 35")
        advanced_maternal_age = cursor.fetchone()[0]
        
        # 高血压风险统计（收缩压≥140或舒张压≥90）
        cursor.execute("""
        SELECT COUNT(*) as count 
        FROM maternal_info 
        WHERE systolic_pressure >= 140 OR diastolic_pressure >= 90
        """)
        hypertension_risk = cursor.fetchone()[0]
        
        # 多胎妊娠统计
        cursor.execute("SELECT COUNT(*) as count FROM maternal_info WHERE pregnancy_type != '单胎'")
        multiple_pregnancy = cursor.fetchone()[0]
        
        # 经产妇统计（经产次数≥1）
        cursor.execute("SELECT COUNT(*) as count FROM maternal_info WHERE parity >= 1")
        multiparous = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': {
                'advanced_maternal_age': advanced_maternal_age,
                'hypertension_risk': hypertension_risk,
                'multiple_pregnancy': multiple_pregnancy,
                'multiparous': multiparous
            }
        })
        
    except Exception as e:
        logger.error(f"获取风险分析失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/health-indicators', methods=['GET'])
def get_health_indicators():
    """获取健康指标统计"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 血压分布统计
        cursor.execute("""
        SELECT 
            CASE 
                WHEN systolic_pressure < 120 AND diastolic_pressure < 80 THEN '正常'
                WHEN systolic_pressure < 140 AND diastolic_pressure < 90 THEN '偏高'
                ELSE '高血压'
            END as bp_category,
            COUNT(*) as count
        FROM maternal_info
        WHERE systolic_pressure IS NOT NULL AND diastolic_pressure IS NOT NULL
        GROUP BY bp_category
        """)
        blood_pressure_distribution = [dict(row) for row in cursor.fetchall()]
        
        # BMI分布统计
        cursor.execute("""
        SELECT 
            CASE 
                WHEN (weight / ((height/100) * (height/100))) < 18.5 THEN '偏瘦'
                WHEN (weight / ((height/100) * (height/100))) < 24 THEN '正常'
                WHEN (weight / ((height/100) * (height/100))) < 28 THEN '偏胖'
                ELSE '肥胖'
            END as bmi_category,
            COUNT(*) as count
        FROM maternal_info
        WHERE weight IS NOT NULL AND height IS NOT NULL AND height > 0
        GROUP BY bmi_category
        """)
        bmi_distribution = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': {
                'blood_pressure_distribution': blood_pressure_distribution,
                'bmi_distribution': bmi_distribution
            }
        })
        
    except Exception as e:
        logger.error(f"获取健康指标失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@maternal_bp.route('/export', methods=['GET'])
def export_maternal_data():
    """导出孕产妇数据"""
    try:
        import pandas as pd
        import tempfile
        
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
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
        
        # 查询数据
        query = f"SELECT * FROM maternal_info{where_clause} ORDER BY created_at DESC"
        cursor.execute(query, params)
        data = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        if not data:
            return jsonify({'success': False, 'message': '没有数据可导出'}), 404
        
        # 转换为DataFrame
        df = pd.DataFrame(data)
        
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        df.to_excel(temp_file.name, index=False)
        temp_file.close()
        
        from flask import send_file
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'maternal_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        logger.error(f"导出孕产妇数据失败: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
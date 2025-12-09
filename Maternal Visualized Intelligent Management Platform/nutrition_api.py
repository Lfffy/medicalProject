from flask import Blueprint, request, jsonify, send_file
import sqlite3
import json
from datetime import datetime
import io
import xlsxwriter

# 创建nutrition_bp蓝图
nutrition_bp = Blueprint('nutrition', __name__, url_prefix='/api')

# 数据库连接函数
def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('maternal_health.db')
    # 设置返回字典格式
    conn.row_factory = sqlite3.Row
    return conn

# 获取营养建议列表
@nutrition_bp.route('/nutrition/advice', methods=['GET'])
def get_nutrition_advice():
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        patient_name = request.args.get('patient_name', '')
        gestational_stage = request.args.get('gestational_stage', '')
        advice_type = request.args.get('advice_type', '')
        priority = request.args.get('priority', '')
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 构建查询
        query = """
        SELECT * FROM nutrition_advice 
        WHERE 1=1
        """
        params = []
        
        # 添加过滤条件
        if patient_name:
            query += " AND patient_name LIKE ?"
            params.append(f"%{patient_name}%")
        
        if gestational_stage:
            query += " AND gestational_stage = ?"
            params.append(gestational_stage)
        
        if advice_type:
            query += " AND advice_type = ?"
            params.append(advice_type)
        
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        # 添加排序和分页
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([page_size, offset])
        
        # 获取数据
        cursor.execute(query, params)
        advice = cursor.fetchall()
        
        # 获取总数
        # 直接构建计数查询，只包含WHERE条件部分
        count_query = "SELECT COUNT(*) FROM nutrition_advice WHERE 1=1"
        count_conditions = ""
        count_params = []
        
        if patient_name:
            count_conditions += " AND patient_name LIKE ?"
            count_params.append(f"%{patient_name}%")
        if gestational_stage:
            count_conditions += " AND gestational_stage = ?"
            count_params.append(gestational_stage)
        if advice_type:
            count_conditions += " AND advice_type = ?"
            count_params.append(advice_type)
        if priority:
            count_conditions += " AND priority = ?"
            count_params.append(priority)
        
        cursor.execute(count_query + count_conditions, count_params)
        total = cursor.fetchone()[0]
        
        conn.close()
        
        # 显式转换为字典列表
        advice_list = []
        for item in advice:
            advice_list.append(dict(item))
        
        return jsonify({
            'success': True,
            'data': {
                'advice': advice_list,
                'total': total
            },
            'message': '获取营养建议成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': f'获取营养建议失败: {str(e)}'
        }), 500

# 获取营养建议统计信息
@nutrition_bp.route('/nutrition/statistics', methods=['GET'])
def get_nutrition_statistics():
    try:
        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取总患者数
        cursor.execute("SELECT COUNT(DISTINCT patient_id) FROM nutrition_advice")
        total_patients = cursor.fetchone()[0]
        
        # 获取总建议数
        cursor.execute("SELECT COUNT(*) FROM nutrition_advice")
        total_advice = cursor.fetchone()[0]
        
        # 获取高优先级建议数
        cursor.execute("SELECT COUNT(*) FROM nutrition_advice WHERE priority = 'high'")
        high_priority_count = cursor.fetchone()[0]
        
        # 获取已完成建议数
        cursor.execute("SELECT COUNT(*) FROM nutrition_advice WHERE status = 'completed'")
        completed_count = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total_patients': total_patients,
                'total_advice': total_advice,
                'high_priority_count': high_priority_count,
                'completed_count': completed_count
            },
            'message': '获取营养建议统计成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': f'获取营养建议统计失败: {str(e)}'
        }), 500

# 导出营养建议为Excel文件
@nutrition_bp.route('/nutrition/export', methods=['POST'])
def export_nutrition_advice():
    try:
        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取所有营养建议数据
        cursor.execute("SELECT * FROM nutrition_advice ORDER BY created_at DESC")
        advice_data = cursor.fetchall()
        conn.close()
        
        # 创建一个内存中的Excel文件
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('营养建议')
        
        # 设置表头
        headers = ['患者ID', '患者姓名', '孕期阶段', '建议类型', '建议内容', '优先级', '状态', '创建时间', '更新时间', '创建人']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)
        
        # 写入数据
        for row_num, row in enumerate(advice_data, 1):
            row_dict = dict(row)
            worksheet.write(row_num, 0, row_dict.get('patient_id', ''))
            worksheet.write(row_num, 1, row_dict.get('patient_name', ''))
            worksheet.write(row_num, 2, row_dict.get('gestational_stage', ''))
            worksheet.write(row_num, 3, row_dict.get('advice_type', ''))
            worksheet.write(row_num, 4, row_dict.get('advice_content', ''))
            worksheet.write(row_num, 5, row_dict.get('priority', ''))
            worksheet.write(row_num, 6, row_dict.get('status', ''))
            worksheet.write(row_num, 7, row_dict.get('created_at', ''))
            worksheet.write(row_num, 8, row_dict.get('updated_at', ''))
            worksheet.write(row_num, 9, row_dict.get('created_by', ''))
        
        # 关闭工作簿
        workbook.close()
        output.seek(0)
        
        # 返回文件
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='营养建议.xlsx')
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'导出营养建议失败: {str(e)}'
        }), 500

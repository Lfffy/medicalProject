from flask import Blueprint, request, jsonify, session
from datetime import datetime
import sqlite3
import os

# 医院管理API蓝图
hospital_bp = Blueprint('hospital', __name__)

# SQLite数据库配置
DB_PATH = os.path.join(os.path.dirname(__file__), 'medical_data.db')

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def require_admin(func):
    """权限验证装饰器"""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'code': 401, 'message': '请先登录'}), 401
        if session.get('role') != 'admin':
            return jsonify({'code': 403, 'message': '权限不足'}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# 获取医院列表API
@hospital_bp.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        search = request.args.get('search', '').strip()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("(name LIKE ? OR address LIKE ? OR contact_phone LIKE ?)")
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 获取总数
        count_query = f"SELECT COUNT(*) as total FROM hospitals{where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # 获取医院列表
        offset = (page - 1) * page_size
        list_query = f"""
        SELECT id, name, address, contact_phone, level, bed_count, status, created_at, updated_at
        FROM hospitals{where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """
        
        cursor.execute(list_query, params + [page_size, offset])
        hospitals = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'hospitals': hospitals,
                'pagination': {
                    'current': page,
                    'pageSize': page_size,
                    'total': total
                }
            }
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取医院列表失败: {str(e)}'}), 500

# 获取医院详情API
@hospital_bp.route('/api/hospitals/<int:hospital_id>', methods=['GET'])
def get_hospital_detail(hospital_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取医院基本信息
        cursor.execute("SELECT * FROM hospitals WHERE id = ?", (hospital_id,))
        hospital = cursor.fetchone()
        
        if not hospital:
            cursor.close()
            conn.close()
            return jsonify({'code': 404, 'message': '医院不存在'}), 404
        
        # 获取科室信息
        cursor.execute("SELECT * FROM departments WHERE hospital_id = ? ORDER BY name", (hospital_id,))
        departments = [dict(row) for row in cursor.fetchall()]
        
        # 获取医生信息
        cursor.execute("""
        SELECT d.*, dep.name as department_name 
        FROM doctors d 
        LEFT JOIN departments dep ON d.department_id = dep.id 
        WHERE d.hospital_id = ? 
        ORDER BY d.name
        """, (hospital_id,))
        doctors = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'hospital': dict(hospital),
                'departments': departments,
                'doctors': doctors
            }
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取医院详情失败: {str(e)}'}), 500

# 添加医院API
@hospital_bp.route('/api/hospitals', methods=['POST'])
@require_admin
def add_hospital():
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name', 'address', 'contact_phone']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({'code': 400, 'message': f'{field}不能为空'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查医院名称是否已存在
        cursor.execute("SELECT id FROM hospitals WHERE name = ?", (data['name'].strip(),))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'code': 400, 'message': '医院名称已存在'}), 400
        
        # 创建医院
        cursor.execute("""
            INSERT INTO hospitals (name, address, contact_phone, level, bed_count, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['name'].strip(),
            data['address'].strip(),
            data['contact_phone'].strip(),
            data.get('level', ''),
            data.get('bed_count', 0),
            data.get('status', 'active'),
            datetime.now(),
            datetime.now()
        ))
        
        hospital_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '添加成功',
            'data': {'hospital_id': hospital_id}
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'添加医院失败: {str(e)}'}), 500

# 更新医院API
@hospital_bp.route('/api/hospitals/<int:hospital_id>', methods=['PUT'])
@require_admin
def update_hospital(hospital_id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查医院是否存在
        cursor.execute("SELECT id FROM hospitals WHERE id = ?", (hospital_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'code': 404, 'message': '医院不存在'}), 404
        
        # 如果更新名称，检查是否重复
        if 'name' in data and data['name'].strip():
            cursor.execute("SELECT id FROM hospitals WHERE name = ? AND id != ?", 
                          (data['name'].strip(), hospital_id))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return jsonify({'code': 400, 'message': '医院名称已存在'}), 400
        
        # 构建更新字段
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append("name = ?")
            update_values.append(data['name'].strip())
        
        if 'address' in data:
            update_fields.append("address = ?")
            update_values.append(data['address'].strip())
        
        if 'contact_phone' in data:
            update_fields.append("contact_phone = ?")
            update_values.append(data['contact_phone'].strip())
        
        if 'level' in data:
            update_fields.append("level = ?")
            update_values.append(data['level'])
        
        if 'bed_count' in data:
            update_fields.append("bed_count = ?")
            update_values.append(data['bed_count'])
        
        if 'status' in data:
            update_fields.append("status = ?")
            update_values.append(data['status'])
        
        if update_fields:
            update_fields.append("updated_at = ?")
            update_values.append(datetime.now())
            update_values.append(hospital_id)
            
            update_query = f"UPDATE hospitals SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(update_query, update_values)
            conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'code': 200, 'message': '更新成功'})
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'更新医院失败: {str(e)}'}), 500

# 删除医院API
@hospital_bp.route('/api/hospitals/<int:hospital_id>', methods=['DELETE'])
@require_admin
def delete_hospital(hospital_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查医院是否存在
        cursor.execute("SELECT id FROM hospitals WHERE id = ?", (hospital_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'code': 404, 'message': '医院不存在'}), 404
        
        # 删除医院（级联删除相关数据）
        cursor.execute("DELETE FROM hospitals WHERE id = ?", (hospital_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'code': 200, 'message': '删除成功'})
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'删除医院失败: {str(e)}'}), 500

# 获取科室列表API
@hospital_bp.route('/api/departments', methods=['GET'])
def get_departments():
    try:
        hospital_id = request.args.get('hospital_id', type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM departments"
        params = []
        
        if hospital_id:
            query += " WHERE hospital_id = ?"
            params.append(hospital_id)
        
        query += " ORDER BY name"
        
        cursor.execute(query, params)
        departments = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {'departments': departments}
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取科室列表失败: {str(e)}'}), 500

# 添加科室API
@hospital_bp.route('/api/departments', methods=['POST'])
@require_admin
def add_department():
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('hospital_id') or not data.get('name', '').strip():
            return jsonify({'code': 400, 'message': '医院ID和科室名称不能为空'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查医院是否存在
        cursor.execute("SELECT id FROM hospitals WHERE id = ?", (data['hospital_id'],))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'code': 400, 'message': '医院不存在'}), 400
        
        # 检查科室名称是否已存在
        cursor.execute("SELECT id FROM departments WHERE hospital_id = ? AND name = ?", 
                      (data['hospital_id'], data['name'].strip()))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'code': 400, 'message': '科室名称已存在'}), 400
        
        # 创建科室
        cursor.execute("""
            INSERT INTO departments (hospital_id, name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data['hospital_id'],
            data['name'].strip(),
            data.get('description', ''),
            datetime.now(),
            datetime.now()
        ))
        
        department_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '添加成功',
            'data': {'department_id': department_id}
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'添加科室失败: {str(e)}'}), 500

# 获取医生列表API
@hospital_bp.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        hospital_id = request.args.get('hospital_id', type=int)
        department_id = request.args.get('department_id', type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT d.*, h.name as hospital_name, dep.name as department_name
        FROM doctors d
        LEFT JOIN hospitals h ON d.hospital_id = h.id
        LEFT JOIN departments dep ON d.department_id = dep.id
        WHERE 1=1
        """
        params = []
        
        if hospital_id:
            query += " AND d.hospital_id = ?"
            params.append(hospital_id)
        
        if department_id:
            query += " AND d.department_id = ?"
            params.append(department_id)
        
        query += " ORDER BY d.name"
        
        cursor.execute(query, params)
        doctors = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {'doctors': doctors}
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取医生列表失败: {str(e)}'}), 500
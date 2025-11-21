# 用户管理API
from flask import Blueprint, request, jsonify, session
from datetime import datetime
import sqlite3
import hashlib
import uuid
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# 创建用户管理蓝图
user_bp = Blueprint('user', __name__)

# 数据库配置
DB_PATH = 'medical_data.db'

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """密码哈希"""
    return generate_password_hash(password)

def check_password_hash_func(hashed_password, password):
    """验证密码"""
    return check_password_hash(hashed_password, password)

# 用户注册API
@user_bp.route('/api/user/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['username', 'password', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'message': f'缺少必填字段: {field}',
                    'data': None
                }), 400
        
        username = data['username']
        password = data['password']
        email = data['email']
        phone = data.get('phone', '')
        role = data.get('role', 'user')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 检查用户名是否已存在
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 400,
                'message': '用户名已存在',
                'data': None
            }), 400
        
        # 检查邮箱是否已存在
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 400,
                'message': '邮箱已存在',
                'data': None
            }), 400
        
        # 创建新用户
        hashed_password = hash_password(password)
        created_at = datetime.now()
        
        insert_query = """
        INSERT INTO users (username, password, email, role, created_at, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (username, hashed_password, email, role, created_at, 1))
        conn.commit()
        
        # 获取插入的用户ID
        user_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '注册成功',
            'data': {
                'user_id': user_id,
                'username': username,
                'email': email,
                'role': role
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'注册失败: {str(e)}',
            'data': None
        }), 500

# 用户登录API
@user_bp.route('/api/user/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'code': 400,
                'message': '用户名和密码不能为空',
                'data': None
            }), 400
        
        username = data['username']
        password = data['password']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 查询用户
        cursor.execute("""
        SELECT id, username, password, email, role, is_active, created_at, updated_at
        FROM users WHERE username = ? OR email = ?
        """, (username, username))
        
        user = cursor.fetchone()
        
        if not user or not check_password_hash_func(user[2], password):
            cursor.close()
            conn.close()
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误',
                'data': None
            }), 401
        
        if user[5] != 1:
            cursor.close()
            conn.close()
            return jsonify({
                'code': 401,
                'message': '账户已被禁用',
                'data': None
            }), 401
        
        # 更新最后登录时间
        cursor.execute("UPDATE users SET updated_at = ? WHERE id = ?", (datetime.now(), user[0]))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        # 设置session
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['role'] = user[4]
        
        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'user_id': user[0],
                'username': user[1],
                'email': user[3],
                'full_name': user[1],
                'phone': '',
                'role': user[4],
                'last_login': user[7].isoformat() if user[7] and hasattr(user[7], 'isoformat') else str(user[7]) if user[7] else None
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'登录失败: {str(e)}',
            'data': None
        }), 500

# 用户登出API
@user_bp.route('/api/user/logout', methods=['POST'])
def logout():
    """用户登出"""
    try:
        session.clear()
        return jsonify({
            'code': 200,
            'message': '登出成功',
            'data': None
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'登出失败: {str(e)}',
            'data': None
        }), 500

# 获取用户信息API
@user_bp.route('/api/user/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_id = session['user_id']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({
                'code': 404,
                'message': '用户不存在',
                'data': None
            }), 404
        
        # 转换Row对象为字典
        user_data = {
            'id': user[0],
            'username': user[1], 
            'email': user[2],
            'role': user[3],
            'is_active': user[4],
            'created_at': user[5].isoformat() if user[5] and hasattr(user[5], 'isoformat') else str(user[5]) if user[5] else None,
            'updated_at': user[6].isoformat() if user[6] and hasattr(user[6], 'isoformat') else str(user[6]) if user[6] else None
        }
        
        return jsonify({
            'code': 200,
            'message': '获取用户信息成功',
            'data': user_data
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取用户信息失败: {str(e)}',
            'data': None
        }), 500

# 更新用户信息API
@user_bp.route('/api/user/profile', methods=['PUT'])
def update_profile():
    """更新用户信息"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_id = session['user_id']
        data = request.get_json()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 构建更新语句
        update_fields = []
        update_values = []
        
        if 'email' in data:
            update_fields.append("email = ?")
            update_values.append(data['email'])
        
        if update_fields:
            update_fields.append("updated_at = ?")
            update_values.append(datetime.now())
            update_values.append(user_id)
            
            update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(update_query, update_values)
            conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '更新用户信息成功',
            'data': None
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新用户信息失败: {str(e)}',
            'data': None
        }), 500

# 修改密码API
@user_bp.route('/api/user/change-password', methods=['POST'])
def change_password():
    """修改密码"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_id = session['user_id']
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({
                'code': 400,
                'message': '旧密码和新密码不能为空',
                'data': None
            }), 400
        
        old_password = data['old_password']
        new_password = data['new_password']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 验证旧密码
        cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash_func(user['password'], old_password):
            cursor.close()
            conn.close()
            return jsonify({
                'code': 400,
                'message': '旧密码错误',
                'data': None
            }), 400
        
        # 更新密码
        hashed_password = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ?, updated_at = ? WHERE id = ?", 
                      (hashed_password, datetime.now(), user_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '修改密码成功',
            'data': None
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'修改密码失败: {str(e)}',
            'data': None
        }), 500

# 获取用户列表API（管理员）
@user_bp.route('/api/user/list', methods=['GET'])
def get_user_list():
    """获取用户列表（管理员）"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        # 检查权限
        if session.get('role') not in ['admin', 'manager']:
            return jsonify({
                'code': 403,
                'message': '权限不足',
                'data': None
            }), 403
        
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        search = request.args.get('search', '')
        role = request.args.get('role', '')
        status = request.args.get('status', '')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("(username LIKE ? OR email LIKE ?)")
            params.extend([f'%{search}%', f'%{search}%'])
        
        if role:
            where_conditions.append("role = ?")
            params.append(role)
        
        if status:
            where_conditions.append("is_active = ?")
            params.append(1 if status == 'active' else 0)
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 获取总数
        count_query = f"SELECT COUNT(*) as total FROM users {where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # 获取用户列表
        offset = (page - 1) * page_size
        list_query = f"""
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM users {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """
        
        cursor.execute(list_query, params + [page_size, offset])
        users = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取用户列表成功',
            'data': {
                'users': users,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取用户列表失败: {str(e)}',
            'data': None
        }), 500

# 用户状态管理API（管理员）
@user_bp.route('/api/user/<user_id>/status', methods=['PUT'])
def update_user_status(user_id):
    """更新用户状态（管理员）"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        # 检查权限
        if session.get('role') not in ['admin']:
            return jsonify({
                'code': 403,
                'message': '权限不足',
                'data': None
            }), 403
        
        data = request.get_json()
        is_active = data.get('status')
        
        if is_active not in [0, 1]:
            return jsonify({
                'code': 400,
                'message': '无效的状态值',
                'data': None
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET is_active = ?, updated_at = ? WHERE id = ?", 
                      (is_active, datetime.now(), user_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '更新用户状态成功',
            'data': None
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新用户状态失败: {str(e)}',
            'data': None
        }), 500
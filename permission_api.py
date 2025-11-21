# 权限管理API
from flask import Blueprint, request, jsonify, session
import sqlite3
import os
from datetime import datetime
import functools

# 创建权限管理蓝图
permission_bp = Blueprint('permission', __name__, url_prefix='/api/permissions')

# SQLite数据库配置
DB_PATH = os.path.join(os.path.dirname(__file__), 'medical_data.db')

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        print(f"数据库连接错误: {e}")
        return None

# 权限装饰器
def require_permission(permission):
    """权限验证装饰器"""
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({
                    'code': 401,
                    'message': '未登录',
                    'data': None
                }), 401
            
            user_id = session['user_id']
            user_role = session.get('role', 'user')
            
            # 管理员拥有所有权限
            if user_role == 'admin':
                return f(*args, **kwargs)
            
            conn = get_db_connection()
            if not conn:
                return jsonify({
                    'code': 500,
                    'message': '数据库连接失败',
                    'data': None
                }), 500
            
            cursor = conn.cursor()
            
            # 检查用户权限
            cursor.execute("""
            SELECT COUNT(*) FROM user_permissions up
            JOIN permissions p ON up.permission_id = p.id
            WHERE up.user_id = ? AND p.name = ?
            """, (user_id, permission))
            
            has_permission = cursor.fetchone()[0] > 0
            
            cursor.close()
            conn.close()
            
            if not has_permission:
                return jsonify({
                    'code': 403,
                    'message': '权限不足',
                    'data': None
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 角色权限装饰器
def require_role(*allowed_roles):
    """角色验证装饰器"""
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({
                    'code': 401,
                    'message': '未登录',
                    'data': None
                }), 401
            
            user_role = session.get('role', 'user')
            
            if user_role not in allowed_roles:
                return jsonify({
                    'code': 403,
                    'message': '权限不足',
                    'data': None
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 获取所有权限列表API
@permission_bp.route('/list', methods=['GET'])
@require_role('admin', 'manager')
def get_permissions_list():
    """获取所有权限列表"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, name, description, category, created_at
        FROM permissions
        ORDER BY category, name
        """)
        
        permissions = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取权限列表成功',
            'data': permissions
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取权限列表失败: {str(e)}',
            'data': None
        }), 500

# 获取用户权限API
@permission_bp.route('/user/<user_id>', methods=['GET'])
@require_role('admin', 'manager')
def get_user_permissions(user_id):
    """获取用户权限"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT p.id, p.name, p.description, p.category
        FROM permissions p
        JOIN user_permissions up ON p.id = up.permission_id
        WHERE up.user_id = ?
        ORDER BY p.category, p.name
        """, (user_id,))
        
        permissions = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取用户权限成功',
            'data': permissions
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取用户权限失败: {str(e)}',
            'data': None
        }), 500

# 分配用户权限API
@permission_bp.route('/user/<user_id>/assign', methods=['POST'])
@require_role('admin')
def assign_user_permissions(user_id):
    """分配用户权限"""
    try:
        data = request.get_json()
        permission_ids = data.get('permission_ids', [])
        
        if not permission_ids:
            return jsonify({
                'code': 400,
                'message': '请选择要分配的权限',
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
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 404,
                'message': '用户不存在',
                'data': None
            }), 404
        
        # 删除用户现有权限
        cursor.execute("DELETE FROM user_permissions WHERE user_id = ?", (user_id,))
        
        # 分配新权限
        for permission_id in permission_ids:
            cursor.execute("""
            INSERT INTO user_permissions (user_id, permission_id, created_at)
            VALUES (?, ?, ?)
            """, (user_id, permission_id, datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '分配用户权限成功',
            'data': None
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'分配用户权限失败: {str(e)}',
            'data': None
        }), 500

# 移除用户权限API
@permission_bp.route('/user/<user_id>/remove/<permission_id>', methods=['DELETE'])
@require_role('admin')
def remove_user_permission(user_id, permission_id):
    """移除用户权限"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 删除用户权限
        cursor.execute("""
        DELETE FROM user_permissions 
        WHERE user_id = ? AND permission_id = ?
        """, (user_id, permission_id))
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        cursor.close()
        conn.close()
        
        if deleted_count == 0:
            return jsonify({
                'code': 404,
                'message': '权限不存在或已移除',
                'data': None
            }), 404
        
        return jsonify({
            'code': 200,
            'message': '移除用户权限成功',
            'data': None
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'移除用户权限失败: {str(e)}',
            'data': None
        }), 500

# 创建权限API
@permission_bp.route('/create', methods=['POST'])
@require_role('admin')
def create_permission():
    """创建权限"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        category = data.get('category', '').strip()
        
        if not name:
            return jsonify({
                'code': 400,
                'message': '权限名称不能为空',
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
        
        # 检查权限是否已存在
        cursor.execute("SELECT id FROM permissions WHERE name = ?", (name,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 400,
                'message': '权限名称已存在',
                'data': None
            }), 400
        
        # 创建权限
        cursor.execute("""
        INSERT INTO permissions (name, description, category, created_at)
        VALUES (?, ?, ?, ?)
        """, (name, description, category, datetime.now()))
        
        permission_id = cursor.lastrowid
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '创建权限成功',
            'data': {
                'id': permission_id,
                'name': name,
                'description': description,
                'category': category
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'创建权限失败: {str(e)}',
            'data': None
        }), 500

# 更新权限API
@permission_bp.route('/<permission_id>', methods=['PUT'])
@require_role('admin')
def update_permission(permission_id):
    """更新权限"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        category = data.get('category', '').strip()
        
        if not name:
            return jsonify({
                'code': 400,
                'message': '权限名称不能为空',
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
        
        # 检查权限是否存在
        cursor.execute("SELECT id FROM permissions WHERE id = ?", (permission_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 404,
                'message': '权限不存在',
                'data': None
            }), 404
        
        # 检查权限名称是否重复
        cursor.execute("SELECT id FROM permissions WHERE name = ? AND id != ?", (name, permission_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 400,
                'message': '权限名称已存在',
                'data': None
            }), 400
        
        # 更新权限
        cursor.execute("""
        UPDATE permissions 
        SET name = ?, description = ?, category = ?, updated_at = ?
        WHERE id = ?
        """, (name, description, category, datetime.now(), permission_id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '更新权限成功',
            'data': None
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新权限失败: {str(e)}',
            'data': None
        }), 500

# 删除权限API
@permission_bp.route('/<permission_id>', methods=['DELETE'])
@require_role('admin')
def delete_permission(permission_id):
    """删除权限"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 检查权限是否存在
        cursor.execute("SELECT id FROM permissions WHERE id = ?", (permission_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 404,
                'message': '权限不存在',
                'data': None
            }), 404
        
        # 删除权限（级联删除用户权限关联）
        cursor.execute("DELETE FROM permissions WHERE id = ?", (permission_id,))
        deleted_count = cursor.rowcount
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '删除权限成功',
            'data': {
                'deleted_count': deleted_count
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除权限失败: {str(e)}',
            'data': None
        }), 500

# 获取权限统计API
@permission_bp.route('/statistics', methods=['GET'])
@require_role('admin', 'manager')
def get_permission_statistics():
    """获取权限统计"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 总权限数
        cursor.execute("SELECT COUNT(*) as total FROM permissions")
        total_permissions = cursor.fetchone()[0]
        
        # 按分类统计权限
        cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM permissions
        GROUP BY category
        ORDER BY count DESC
        """)
        category_stats = [dict(row) for row in cursor.fetchall()]
        
        # 用户权限分配统计
        cursor.execute("""
        SELECT COUNT(DISTINCT user_id) as users_with_permissions
        FROM user_permissions
        """)
        users_with_permissions = cursor.fetchone()[0]
        
        # 总用户权限关联数
        cursor.execute("SELECT COUNT(*) as total_user_permissions FROM user_permissions")
        total_user_permissions = cursor.fetchone()[0]
        
        # 最常用的权限
        cursor.execute("""
        SELECT p.name, COUNT(up.user_id) as user_count
        FROM permissions p
        LEFT JOIN user_permissions up ON p.id = up.permission_id
        GROUP BY p.id, p.name
        ORDER BY user_count DESC
        LIMIT 10
        """)
        popular_permissions = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取权限统计成功',
            'data': {
                'total_permissions': total_permissions,
                'category_stats': category_stats,
                'users_with_permissions': users_with_permissions,
                'total_user_permissions': total_user_permissions,
                'popular_permissions': popular_permissions
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取权限统计失败: {str(e)}',
            'data': None
        }), 500

# 批量分配权限API
@permission_bp.route('/batch-assign', methods=['POST'])
@require_role('admin')
def batch_assign_permissions():
    """批量分配权限"""
    try:
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        permission_ids = data.get('permission_ids', [])
        
        if not user_ids or not permission_ids:
            return jsonify({
                'code': 400,
                'message': '请选择用户和权限',
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
        
        # 批量分配权限
        assigned_count = 0
        for user_id in user_ids:
            for permission_id in permission_ids:
                # 检查是否已存在
                cursor.execute("""
                SELECT COUNT(*) FROM user_permissions 
                WHERE user_id = ? AND permission_id = ?
                """, (user_id, permission_id))
                
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                    INSERT INTO user_permissions (user_id, permission_id, created_at)
                    VALUES (?, ?, ?)
                    """, (user_id, permission_id, datetime.now()))
                    assigned_count += 1
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': f'批量分配权限成功，共分配{assigned_count}条权限',
            'data': {
                'assigned_count': assigned_count
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'批量分配权限失败: {str(e)}',
            'data': None
        }), 500

# 检查用户权限API
@permission_bp.route('/check', methods=['POST'])
def check_user_permission():
    """检查用户权限"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        data = request.get_json()
        permission = data.get('permission', '')
        
        if not permission:
            return jsonify({
                'code': 400,
                'message': '权限名称不能为空',
                'data': None
            }), 400
        
        user_id = session['user_id']
        user_role = session.get('role', 'user')
        
        # 管理员拥有所有权限
        if user_role == 'admin':
            return jsonify({
                'code': 200,
                'message': '权限检查成功',
                'data': {
                    'has_permission': True,
                    'permission': permission,
                    'user_role': user_role
                }
            })
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 检查用户权限
        cursor.execute("""
        SELECT COUNT(*) FROM user_permissions up
        JOIN permissions p ON up.permission_id = p.id
        WHERE up.user_id = ? AND p.name = ?
        """, (user_id, permission))
        
        has_permission = cursor.fetchone()[0] > 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '权限检查成功',
            'data': {
                'has_permission': has_permission,
                'permission': permission,
                'user_role': user_role
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'权限检查失败: {str(e)}',
            'data': None
        }), 500
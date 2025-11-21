# 操作日志API
from flask import Blueprint, request, jsonify, session
import sqlite3
import os
from datetime import datetime, timedelta
import json
import uuid

# 创建操作日志蓝图
log_bp = Blueprint('log', __name__, url_prefix='/api/logs')

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

def log_operation(user_id, username, action, module, details, ip_address=None):
    """记录操作日志"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        log_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # 将详情转换为JSON字符串
        details_json = json.dumps(details, ensure_ascii=False) if details else None
        
        cursor.execute("""
        INSERT INTO operation_logs (id, user_id, username, action, module, details, ip_address, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (log_id, user_id, username, action, module, details_json, ip_address, timestamp))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"记录操作日志失败: {e}")
        return False

# 获取操作日志列表API
@log_bp.route('/operations', methods=['GET'])
def get_operation_logs():
    """获取操作日志列表"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        # 检查权限（管理员和经理可以查看所有日志，普通用户只能查看自己的日志）
        user_role = session.get('role', 'user')
        current_user_id = session['user_id']
        
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        search = request.args.get('search', '')
        action = request.args.get('action', '')
        module = request.args.get('module', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
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
        
        # 非管理员只能查看自己的日志
        if user_role not in ['admin', 'manager']:
            where_conditions.append("user_id = ?")
            params.append(current_user_id)
        
        if search:
            where_conditions.append("(username LIKE ? OR action LIKE ? OR module LIKE ?)")
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
        
        if action:
            where_conditions.append("action = ?")
            params.append(action)
        
        if module:
            where_conditions.append("module = ?")
            params.append(module)
        
        if start_date:
            where_conditions.append("created_at >= ?")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= ?")
            params.append(end_date + ' 23:59:59')
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 获取总数
        count_query = f"SELECT COUNT(*) as total FROM operation_logs {where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # 获取日志列表
        offset = (page - 1) * page_size
        list_query = f"""
        SELECT id, user_id, username, action, module, details, ip_address, created_at
        FROM operation_logs {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """
        
        cursor.execute(list_query, params + [page_size, offset])
        logs = [dict(row) for row in cursor.fetchall()]
        
        # 解析JSON详情
        for log in logs:
            if log['details']:
                try:
                    log['details'] = json.loads(log['details'])
                except:
                    log['details'] = None
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取操作日志成功',
            'data': {
                'logs': logs,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取操作日志失败: {str(e)}',
            'data': None
        }), 500

# 获取操作日志详情API
@log_bp.route('/operations/<log_id>', methods=['GET'])
def get_operation_log_detail(log_id):
    """获取操作日志详情"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_role = session.get('role', 'user')
        current_user_id = session['user_id']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 构建查询条件
        where_clause = "WHERE id = ?"
        params = [log_id]
        
        # 非管理员只能查看自己的日志
        if user_role not in ['admin', 'manager']:
            where_clause += " AND user_id = ?"
            params.append(current_user_id)
        
        cursor.execute(f"""
        SELECT id, user_id, username, action, module, details, ip_address, created_at
        FROM operation_logs {where_clause}
        """, params)
        
        log = cursor.fetchone()
        
        if not log:
            cursor.close()
            conn.close()
            return jsonify({
                'code': 404,
                'message': '日志不存在',
                'data': None
            }), 404
        
        log_data = dict(log)
        
        # 解析JSON详情
        if log_data['details']:
            try:
                log_data['details'] = json.loads(log_data['details'])
            except:
                log_data['details'] = None
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取操作日志详情成功',
            'data': log_data
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取操作日志详情失败: {str(e)}',
            'data': None
        }), 500

# 删除操作日志API
@log_bp.route('/operations/<log_id>', methods=['DELETE'])
def delete_operation_log(log_id):
    """删除操作日志"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_role = session.get('role', 'user')
        current_user_id = session['user_id']
        
        # 只有管理员可以删除日志
        if user_role != 'admin':
            return jsonify({
                'code': 403,
                'message': '权限不足',
                'data': None
            }), 403
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 检查日志是否存在
        cursor.execute("SELECT id FROM operation_logs WHERE id = ?", (log_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'code': 404,
                'message': '日志不存在',
                'data': None
            }), 404
        
        # 删除日志
        cursor.execute("DELETE FROM operation_logs WHERE id = ?", (log_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '删除操作日志成功',
            'data': None
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除操作日志失败: {str(e)}',
            'data': None
        }), 500

# 批量删除操作日志API
@log_bp.route('/operations/batch-delete', methods=['POST'])
def batch_delete_operation_logs():
    """批量删除操作日志"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_role = session.get('role', 'user')
        
        # 只有管理员可以删除日志
        if user_role != 'admin':
            return jsonify({
                'code': 403,
                'message': '权限不足',
                'data': None
            }), 403
        
        data = request.get_json()
        log_ids = data.get('log_ids', [])
        
        if not log_ids:
            return jsonify({
                'code': 400,
                'message': '请选择要删除的日志',
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
        
        # 构建IN查询
        placeholders = ','.join(['?' for _ in log_ids])
        cursor.execute(f"DELETE FROM operation_logs WHERE id IN ({placeholders})", log_ids)
        deleted_count = cursor.rowcount
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': f'批量删除操作日志成功，共删除{deleted_count}条记录',
            'data': {
                'deleted_count': deleted_count
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'批量删除操作日志失败: {str(e)}',
            'data': None
        }), 500

# 清理过期日志API
@log_bp.route('/operations/cleanup', methods=['POST'])
def cleanup_operation_logs():
    """清理过期操作日志"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_role = session.get('role', 'user')
        
        # 只有管理员可以清理日志
        if user_role != 'admin':
            return jsonify({
                'code': 403,
                'message': '权限不足',
                'data': None
            }), 403
        
        data = request.get_json()
        days = data.get('days', 90)  # 默认清理90天前的日志
        
        if days <= 0:
            return jsonify({
                'code': 400,
                'message': '天数必须大于0',
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
        
        # 计算截止日期
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 删除过期日志
        cursor.execute("DELETE FROM operation_logs WHERE created_at < ?", (cutoff_date,))
        deleted_count = cursor.rowcount
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': f'清理过期日志成功，共删除{deleted_count}条记录',
            'data': {
                'deleted_count': deleted_count,
                'cutoff_date': cutoff_date.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'清理过期日志失败: {str(e)}',
            'data': None
        }), 500

# 获取操作日志统计API
@log_bp.route('/operations/statistics', methods=['GET'])
def get_operation_log_statistics():
    """获取操作日志统计"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_role = session.get('role', 'user')
        current_user_id = session['user_id']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'code': 500,
                'message': '数据库连接失败',
                'data': None
            }), 500
        
        cursor = conn.cursor()
        
        # 构建查询条件
        where_clause = ""
        params = []
        
        # 非管理员只能查看自己的日志统计
        if user_role not in ['admin', 'manager']:
            where_clause = "WHERE user_id = ?"
            params.append(current_user_id)
        
        # 总日志数
        cursor.execute(f"SELECT COUNT(*) as total FROM operation_logs {where_clause}", params)
        total_logs = cursor.fetchone()[0]
        
        # 今日日志数
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(f"SELECT COUNT(*) as today_total FROM operation_logs {where_clause} AND DATE(created_at) = ?", params + [today])
        today_logs = cursor.fetchone()[0]
        
        # 按操作类型统计
        cursor.execute(f"""
        SELECT action, COUNT(*) as count 
        FROM operation_logs {where_clause}
        GROUP BY action
        ORDER BY count DESC
        LIMIT 10
        """, params)
        action_stats = [dict(row) for row in cursor.fetchall()]
        
        # 按模块统计
        cursor.execute(f"""
        SELECT module, COUNT(*) as count 
        FROM operation_logs {where_clause}
        GROUP BY module
        ORDER BY count DESC
        LIMIT 10
        """, params)
        module_stats = [dict(row) for row in cursor.fetchall()]
        
        # 最近7天日志趋势
        cursor.execute(f"""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM operation_logs {where_clause}
        WHERE created_at >= date('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date
        """, params)
        trend_stats = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'code': 200,
            'message': '获取操作日志统计成功',
            'data': {
                'total_logs': total_logs,
                'today_logs': today_logs,
                'action_stats': action_stats,
                'module_stats': module_stats,
                'trend_stats': trend_stats
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取操作日志统计失败: {str(e)}',
            'data': None
        }), 500

# 导出操作日志API
@log_bp.route('/operations/export', methods=['GET'])
def export_operation_logs():
    """导出操作日志"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'code': 401,
                'message': '未登录',
                'data': None
            }), 401
        
        user_role = session.get('role', 'user')
        current_user_id = session['user_id']
        
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        action = request.args.get('action', '')
        module = request.args.get('module', '')
        
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
        
        # 非管理员只能导出自己的日志
        if user_role not in ['admin', 'manager']:
            where_conditions.append("user_id = ?")
            params.append(current_user_id)
        
        if start_date:
            where_conditions.append("created_at >= ?")
            params.append(start_date)
        
        if end_date:
            where_conditions.append("created_at <= ?")
            params.append(end_date + ' 23:59:59')
        
        if action:
            where_conditions.append("action = ?")
            params.append(action)
        
        if module:
            where_conditions.append("module = ?")
            params.append(module)
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 查询日志数据
        cursor.execute(f"""
        SELECT id, user_id, username, action, module, details, ip_address, created_at
        FROM operation_logs {where_clause}
        ORDER BY created_at DESC
        """, params)
        
        logs = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        if not logs:
            return jsonify({
                'code': 404,
                'message': '没有数据可导出',
                'data': None
            }), 404
        
        # 解析JSON详情并格式化数据
        for log in logs:
            if log['details']:
                try:
                    details = json.loads(log['details'])
                    log['details'] = json.dumps(details, ensure_ascii=False, indent=2)
                except:
                    log['details'] = log['details']
        
        # 生成CSV格式的数据
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        writer.writerow(['ID', '用户ID', '用户名', '操作', '模块', '详情', 'IP地址', '创建时间'])
        
        # 写入数据
        for log in logs:
            writer.writerow([
                log['id'],
                log['user_id'],
                log['username'],
                log['action'],
                log['module'],
                log['details'] or '',
                log['ip_address'] or '',
                log['created_at']
            ])
        
        output.seek(0)
        
        from flask import Response
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=operation_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        )
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'导出操作日志失败: {str(e)}',
            'data': None
        }), 500
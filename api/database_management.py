# -*- coding: utf-8 -*-
"""
AgriDec 数据库管理API
提供数据库配置、切换和同步的API接口
"""

import logging
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from datetime import datetime
from database import get_multi_db_manager, get_config_manager, switch_database

logger = logging.getLogger(__name__)

# 创建蓝图
db_management_bp = Blueprint('db_management', __name__, url_prefix='/api/database')

@db_management_bp.route('/status', methods=['GET'])
@login_required
def get_database_status():
    """获取数据库状态"""
    try:
        config_manager = get_config_manager()
        multi_db_manager = get_multi_db_manager()
        
        if not config_manager:
            return jsonify({
                'success': False,
                'error': '配置管理器未初始化'
            }), 500
        
        # 基本配置信息
        config = config_manager.get_config()
        status_info = {
            'primary_db': config.get('primary_db'),
            'backup_db': config.get('backup_db'),
            'sync_enabled': config.get('sync_enabled', False),
            'databases': {}
        }
        
        # 数据库连接状态
        if multi_db_manager:
            db_status = multi_db_manager.get_database_status()
            status_info['databases'] = db_status
        else:
            # 如果多数据库管理器未初始化，只显示当前数据库状态
            status_info['databases'] = {
                config.get('primary_db', 'unknown'): {
                    'status': 'connected',
                    'note': '单数据库模式'
                }
            }
        
        return jsonify({
            'success': True,
            'data': status_info
        })
        
    except Exception as e:
        logger.error(f"获取数据库状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@db_management_bp.route('/config', methods=['GET'])
@login_required
def get_database_config():
    """获取数据库配置"""
    try:
        config_manager = get_config_manager()
        
        if not config_manager:
            return jsonify({
                'success': False,
                'error': '配置管理器未初始化'
            }), 500
        
        config = config_manager.get_config()
        
        # 隐藏敏感信息
        safe_config = config.copy()
        if 'databases' in safe_config:
            for db_type, db_config in safe_config['databases'].items():
                if 'password' in db_config:
                    db_config['password'] = '***'
        
        return jsonify({
            'success': True,
            'data': safe_config
        })
        
    except Exception as e:
        logger.error(f"获取数据库配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@db_management_bp.route('/config', methods=['POST'])
@login_required
def update_database_config():
    """更新数据库配置"""
    try:
        # 检查管理员权限
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': '需要管理员权限'
            }), 403
        
        config_manager = get_config_manager()
        
        if not config_manager:
            return jsonify({
                'success': False,
                'error': '配置管理器未初始化'
            }), 500
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400
        
        # 更新配置
        if 'primary_db' in data:
            config_manager.set_primary_database(data['primary_db'])
        
        if 'backup_db' in data:
            config_manager.set_backup_database(data['backup_db'])
        
        if 'sync_enabled' in data:
            config_manager.enable_sync(data['sync_enabled'])
        
        if 'databases' in data:
            for db_type, db_config in data['databases'].items():
                config_manager.update_database_config(db_type, db_config)
        
        return jsonify({
            'success': True,
            'message': '配置更新成功'
        })
        
    except Exception as e:
        logger.error(f"更新数据库配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@db_management_bp.route('/switch', methods=['POST'])
@login_required
def switch_primary_database():
    """切换主数据库"""
    try:
        # 检查管理员权限
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': '需要管理员权限'
            }), 403
        
        data = request.get_json()
        if not data or 'db_type' not in data:
            return jsonify({
                'success': False,
                'error': '缺少db_type参数'
            }), 400
        
        db_type = data['db_type']
        
        # 执行切换
        success = switch_database(db_type, current_app)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'数据库已切换到: {db_type}'
            })
        else:
            return jsonify({
                'success': False,
                'error': '数据库切换失败'
            }), 500
        
    except Exception as e:
        logger.error(f"切换数据库失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@db_management_bp.route('/sync', methods=['POST'])
@login_required
def sync_databases():
    """同步数据库"""
    try:
        # 检查管理员权限
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': '需要管理员权限'
            }), 403
        
        multi_db_manager = get_multi_db_manager()
        
        if not multi_db_manager:
            return jsonify({
                'success': False,
                'error': '多数据库管理器未初始化'
            }), 500
        
        data = request.get_json() or {}
        tables = data.get('tables')  # 可选：指定要同步的表
        
        # 执行同步
        sync_results = multi_db_manager.sync_databases(tables)
        
        # 统计结果
        total_tables = len(sync_results)
        success_count = sum(1 for result in sync_results.values() if result)
        
        return jsonify({
            'success': True,
            'message': f'同步完成: {success_count}/{total_tables} 个表同步成功',
            'data': {
                'sync_results': sync_results,
                'total_tables': total_tables,
                'success_count': success_count,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"数据库同步失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@db_management_bp.route('/backup', methods=['POST'])
@login_required
def backup_database():
    """备份数据库"""
    try:
        # 检查管理员权限
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': '需要管理员权限'
            }), 403
        
        config_manager = get_config_manager()
        multi_db_manager = get_multi_db_manager()
        
        if not config_manager or not multi_db_manager:
            return jsonify({
                'success': False,
                'error': '数据库管理器未初始化'
            }), 500
        
        data = request.get_json() or {}
        db_type = data.get('db_type', config_manager.config.get('primary_db'))
        
        # 执行备份（这里简化为同步操作）
        if db_type == config_manager.config.get('primary_db'):
            # 备份主数据库到备份数据库
            sync_results = multi_db_manager.sync_databases()
            
            success_count = sum(1 for result in sync_results.values() if result)
            total_tables = len(sync_results)
            
            return jsonify({
                'success': True,
                'message': f'备份完成: {success_count}/{total_tables} 个表备份成功',
                'data': {
                    'backup_type': 'sync_to_backup',
                    'source_db': db_type,
                    'target_db': config_manager.config.get('backup_db'),
                    'tables_backed_up': success_count,
                    'timestamp': datetime.now().isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '只能备份主数据库'
            }), 400
        
    except Exception as e:
        logger.error(f"数据库备份失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@db_management_bp.route('/test-connection', methods=['POST'])
@login_required
def test_database_connection():
    """测试数据库连接"""
    try:
        data = request.get_json()
        if not data or 'db_type' not in data:
            return jsonify({
                'success': False,
                'error': '缺少db_type参数'
            }), 400
        
        db_type = data['db_type']
        multi_db_manager = get_multi_db_manager()
        
        if not multi_db_manager:
            return jsonify({
                'success': False,
                'error': '多数据库管理器未初始化'
            }), 500
        
        # 获取指定数据库的状态
        db_status = multi_db_manager.get_database_status()
        
        if db_type in db_status:
            status = db_status[db_type]
            return jsonify({
                'success': True,
                'data': {
                    'db_type': db_type,
                    'status': status['status'],
                    'connected': status['status'] == 'connected',
                    'details': status
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'数据库类型 {db_type} 未配置'
            }), 400
        
    except Exception as e:
        logger.error(f"测试数据库连接失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

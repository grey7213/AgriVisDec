# -*- coding: utf-8 -*-
"""
AgriDec 数据库配置
共享的数据库实例，支持基础多数据库功能
"""

import os
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

logger = logging.getLogger(__name__)

# 创建共享的数据库和加密实例
db = SQLAlchemy()
bcrypt = Bcrypt()

# 全局管理器实例（简化版）
multi_db_manager = None
config_manager = None

def init_db(app):
    """
    初始化数据库
    """
    global multi_db_manager, config_manager

    try:
        # 使用环境变量或默认配置
        mysql_uri = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123456@localhost/agridec?charset=utf8mb4'
        sqlite_uri = 'sqlite:///agridec.db'

        # 根据环境选择数据库
        if os.environ.get('USE_SQLITE', '').lower() == 'true':
            app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
            logger.info("使用SQLite数据库")
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
            logger.info("使用MySQL数据库")

        # 设置其他数据库配置
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 3600
        }

        # 初始化Flask-SQLAlchemy
        db.init_app(app)
        bcrypt.init_app(app)

        logger.info("数据库初始化成功")
        return db, bcrypt

    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        # 回退到SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agridec_fallback.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        bcrypt.init_app(app)
        return db, bcrypt

def get_multi_db_manager():
    """获取多数据库管理器实例（简化版）"""
    return None  # 暂时返回None，多数据库功能需要完整实现

def get_config_manager():
    """获取配置管理器实例（简化版）"""
    return None  # 暂时返回None

def switch_database(db_type: str, app=None):
    """
    切换数据库（简化版）

    Args:
        db_type: 数据库类型 ('mysql' 或 'sqlite')
        app: Flask应用实例
    """
    try:
        if app:
            if db_type == 'sqlite':
                new_uri = 'sqlite:///agridec.db'
            else:
                new_uri = 'mysql+pymysql://root:123456@localhost/agridec?charset=utf8mb4'

            app.config['SQLALCHEMY_DATABASE_URI'] = new_uri
            logger.info(f"数据库已切换到: {db_type}")

        return True

    except Exception as e:
        logger.error(f"数据库切换失败: {str(e)}")
        return False

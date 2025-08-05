# -*- coding: utf-8 -*-
"""
AgriDec 数据库配置管理器
支持灵活的数据库配置和切换
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseConfigManager:
    """数据库配置管理器"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file or 'database/db_config.json'
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"从 {self.config_file} 加载配置成功")
                return config
            else:
                # 创建默认配置
                config = self._create_default_config()
                self._save_config(config)
                logger.info("创建默认数据库配置")
                return config
                
        except Exception as e:
            logger.error(f"加载配置失败: {str(e)}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """创建默认配置"""
        return {
            "version": "1.0",
            "primary_db": "mysql",
            "backup_db": "sqlite",
            "sync_enabled": True,
            "auto_backup": True,
            "backup_interval": 3600,  # 1小时
            "databases": {
                "mysql": {
                    "host": os.environ.get('MYSQL_HOST', 'localhost'),
                    "port": int(os.environ.get('MYSQL_PORT', 3306)),
                    "user": os.environ.get('MYSQL_USER', 'root'),
                    "password": os.environ.get('MYSQL_PASSWORD', '123456'),
                    "database": os.environ.get('MYSQL_DATABASE', 'agridec'),
                    "charset": "utf8mb4",
                    "pool_size": 10,
                    "pool_recycle": 3600,
                    "echo": False,
                    "enabled": True
                },
                "sqlite": {
                    "path": os.environ.get('SQLITE_PATH', 'data/agridec.db'),
                    "echo": False,
                    "enabled": True
                }
            },
            "sync_tables": [
                "user",
                "seed_price",
                "weather_data", 
                "farm_machine",
                "user_session"
            ],
            "backup_settings": {
                "backup_dir": "backups/database",
                "max_backups": 30,
                "compress": True
            }
        }
    
    def _save_config(self, config: Dict[str, Any]):
        """保存配置到文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"配置保存到 {self.config_file} 成功")
            
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def get_config(self) -> Dict[str, Any]:
        """获取完整配置"""
        return self.config.copy()
    
    def get_database_config(self, db_type: str) -> Optional[Dict[str, Any]]:
        """
        获取指定数据库配置
        
        Args:
            db_type: 数据库类型 ('mysql' 或 'sqlite')
            
        Returns:
            数据库配置字典
        """
        return self.config.get('databases', {}).get(db_type)
    
    def update_database_config(self, db_type: str, config: Dict[str, Any]):
        """
        更新数据库配置
        
        Args:
            db_type: 数据库类型
            config: 新的配置字典
        """
        if 'databases' not in self.config:
            self.config['databases'] = {}
        
        self.config['databases'][db_type] = config
        self._save_config(self.config)
        logger.info(f"更新 {db_type} 数据库配置")
    
    def set_primary_database(self, db_type: str):
        """
        设置主数据库
        
        Args:
            db_type: 数据库类型
        """
        if db_type not in self.config.get('databases', {}):
            raise ValueError(f"数据库类型 {db_type} 未配置")
        
        self.config['primary_db'] = db_type
        self._save_config(self.config)
        logger.info(f"设置主数据库为: {db_type}")
    
    def set_backup_database(self, db_type: str):
        """
        设置备份数据库
        
        Args:
            db_type: 数据库类型
        """
        if db_type not in self.config.get('databases', {}):
            raise ValueError(f"数据库类型 {db_type} 未配置")
        
        self.config['backup_db'] = db_type
        self._save_config(self.config)
        logger.info(f"设置备份数据库为: {db_type}")
    
    def enable_sync(self, enabled: bool = True):
        """
        启用/禁用数据库同步
        
        Args:
            enabled: 是否启用同步
        """
        self.config['sync_enabled'] = enabled
        self._save_config(self.config)
        logger.info(f"数据库同步: {'启用' if enabled else '禁用'}")
    
    def add_sync_table(self, table_name: str):
        """
        添加同步表
        
        Args:
            table_name: 表名
        """
        if 'sync_tables' not in self.config:
            self.config['sync_tables'] = []
        
        if table_name not in self.config['sync_tables']:
            self.config['sync_tables'].append(table_name)
            self._save_config(self.config)
            logger.info(f"添加同步表: {table_name}")
    
    def remove_sync_table(self, table_name: str):
        """
        移除同步表
        
        Args:
            table_name: 表名
        """
        if 'sync_tables' in self.config and table_name in self.config['sync_tables']:
            self.config['sync_tables'].remove(table_name)
            self._save_config(self.config)
            logger.info(f"移除同步表: {table_name}")
    
    def get_flask_database_uri(self, db_type: str = None) -> str:
        """
        获取Flask SQLAlchemy数据库URI
        
        Args:
            db_type: 数据库类型，默认使用主数据库
            
        Returns:
            数据库URI字符串
        """
        if db_type is None:
            db_type = self.config.get('primary_db', 'mysql')
        
        db_config = self.get_database_config(db_type)
        if not db_config:
            raise ValueError(f"数据库类型 {db_type} 未配置")
        
        if db_type == 'mysql':
            return (
                f"mysql+pymysql://{db_config['user']}:{db_config['password']}@"
                f"{db_config['host']}:{db_config['port']}/{db_config['database']}?"
                f"charset={db_config.get('charset', 'utf8mb4')}"
            )
        elif db_type == 'sqlite':
            return f"sqlite:///{db_config['path']}"
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
    
    def validate_config(self) -> Dict[str, Any]:
        """
        验证配置有效性
        
        Returns:
            验证结果字典
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # 检查必需字段
        required_fields = ['primary_db', 'databases']
        for field in required_fields:
            if field not in self.config:
                results['errors'].append(f"缺少必需字段: {field}")
                results['valid'] = False
        
        # 检查主数据库配置
        primary_db = self.config.get('primary_db')
        if primary_db and primary_db not in self.config.get('databases', {}):
            results['errors'].append(f"主数据库 {primary_db} 未配置")
            results['valid'] = False
        
        # 检查备份数据库配置
        backup_db = self.config.get('backup_db')
        if backup_db and backup_db not in self.config.get('databases', {}):
            results['warnings'].append(f"备份数据库 {backup_db} 未配置")
        
        # 检查数据库配置完整性
        for db_type, db_config in self.config.get('databases', {}).items():
            if db_type == 'mysql':
                required_mysql_fields = ['host', 'port', 'user', 'password', 'database']
                for field in required_mysql_fields:
                    if field not in db_config:
                        results['errors'].append(f"MySQL配置缺少字段: {field}")
                        results['valid'] = False
            elif db_type == 'sqlite':
                if 'path' not in db_config:
                    results['errors'].append("SQLite配置缺少path字段")
                    results['valid'] = False
        
        return results
    
    def export_config(self, export_path: str):
        """
        导出配置到指定路径
        
        Args:
            export_path: 导出路径
        """
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"配置导出到 {export_path} 成功")
            
        except Exception as e:
            logger.error(f"配置导出失败: {str(e)}")
            raise
    
    def import_config(self, import_path: str):
        """
        从指定路径导入配置
        
        Args:
            import_path: 导入路径
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # 验证导入的配置
            temp_manager = DatabaseConfigManager()
            temp_manager.config = imported_config
            validation = temp_manager.validate_config()
            
            if not validation['valid']:
                raise ValueError(f"导入的配置无效: {validation['errors']}")
            
            self.config = imported_config
            self._save_config(self.config)
            logger.info(f"从 {import_path} 导入配置成功")
            
        except Exception as e:
            logger.error(f"配置导入失败: {str(e)}")
            raise

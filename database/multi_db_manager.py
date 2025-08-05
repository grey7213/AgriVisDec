# -*- coding: utf-8 -*-
"""
AgriDec 多数据库管理器
支持MySQL和SQLite的双重存储架构
"""

import os
import sqlite3
import pymysql
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class MultiDatabaseManager:
    """多数据库管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化多数据库管理器
        
        Args:
            config: 数据库配置字典
        """
        self.config = config
        self.engines = {}
        self.sessions = {}
        self.sync_enabled = config.get('sync_enabled', False)
        self.primary_db = config.get('primary_db', 'mysql')
        self.backup_db = config.get('backup_db', 'sqlite')
        
        # 初始化数据库连接
        self._init_databases()
    
    def _init_databases(self):
        """初始化数据库连接"""
        try:
            # 初始化MySQL连接
            if 'mysql' in self.config.get('databases', {}):
                mysql_config = self.config['databases']['mysql']
                mysql_uri = (
                    f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@"
                    f"{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}?"
                    f"charset=utf8mb4"
                )
                self.engines['mysql'] = create_engine(
                    mysql_uri,
                    pool_size=mysql_config.get('pool_size', 10),
                    pool_recycle=mysql_config.get('pool_recycle', 3600),
                    pool_pre_ping=True,
                    echo=mysql_config.get('echo', False)
                )
                self.sessions['mysql'] = sessionmaker(bind=self.engines['mysql'])
                logger.info("MySQL数据库连接初始化成功")
            
            # 初始化SQLite连接
            if 'sqlite' in self.config.get('databases', {}):
                sqlite_config = self.config['databases']['sqlite']
                sqlite_path = sqlite_config['path']
                
                # 确保SQLite数据库目录存在
                os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
                
                sqlite_uri = f"sqlite:///{sqlite_path}"
                self.engines['sqlite'] = create_engine(
                    sqlite_uri,
                    echo=sqlite_config.get('echo', False)
                )
                self.sessions['sqlite'] = sessionmaker(bind=self.engines['sqlite'])
                logger.info("SQLite数据库连接初始化成功")
                
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise
    
    @contextmanager
    def get_session(self, db_type: str = None):
        """
        获取数据库会话上下文管理器
        
        Args:
            db_type: 数据库类型 ('mysql' 或 'sqlite')，默认使用主数据库
        """
        if db_type is None:
            db_type = self.primary_db
        
        if db_type not in self.sessions:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        
        session = self.sessions[db_type]()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败 ({db_type}): {str(e)}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Dict = None, db_type: str = None) -> List[Dict]:
        """
        执行查询语句
        
        Args:
            query: SQL查询语句
            params: 查询参数
            db_type: 数据库类型
            
        Returns:
            查询结果列表
        """
        if db_type is None:
            db_type = self.primary_db
        
        try:
            with self.get_session(db_type) as session:
                result = session.execute(text(query), params or {})
                
                # 处理查询结果
                if result.returns_rows:
                    columns = result.keys()
                    rows = result.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    return []
                    
        except Exception as e:
            logger.error(f"查询执行失败 ({db_type}): {str(e)}")
            raise
    
    def insert_data(self, table: str, data: Dict, sync: bool = None) -> bool:
        """
        插入数据
        
        Args:
            table: 表名
            data: 数据字典
            sync: 是否同步到备份数据库
            
        Returns:
            操作是否成功
        """
        if sync is None:
            sync = self.sync_enabled
        
        try:
            # 插入到主数据库
            success = self._insert_to_db(table, data, self.primary_db)
            
            # 如果启用同步，插入到备份数据库
            if sync and success and self.backup_db in self.engines:
                try:
                    self._insert_to_db(table, data, self.backup_db)
                    logger.debug(f"数据同步到备份数据库成功: {table}")
                except Exception as e:
                    logger.warning(f"数据同步到备份数据库失败: {str(e)}")
            
            return success
            
        except Exception as e:
            logger.error(f"数据插入失败: {str(e)}")
            return False
    
    def _insert_to_db(self, table: str, data: Dict, db_type: str) -> bool:
        """插入数据到指定数据库"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join([f':{key}' for key in data.keys()])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with self.get_session(db_type) as session:
                session.execute(text(query), data)
                return True
                
        except Exception as e:
            logger.error(f"插入数据到{db_type}失败: {str(e)}")
            return False
    
    def update_data(self, table: str, data: Dict, where_clause: str, where_params: Dict = None, sync: bool = None) -> bool:
        """
        更新数据
        
        Args:
            table: 表名
            data: 更新数据字典
            where_clause: WHERE条件
            where_params: WHERE参数
            sync: 是否同步到备份数据库
            
        Returns:
            操作是否成功
        """
        if sync is None:
            sync = self.sync_enabled
        
        try:
            # 更新主数据库
            success = self._update_in_db(table, data, where_clause, where_params, self.primary_db)
            
            # 如果启用同步，更新备份数据库
            if sync and success and self.backup_db in self.engines:
                try:
                    self._update_in_db(table, data, where_clause, where_params, self.backup_db)
                    logger.debug(f"数据同步更新到备份数据库成功: {table}")
                except Exception as e:
                    logger.warning(f"数据同步更新到备份数据库失败: {str(e)}")
            
            return success
            
        except Exception as e:
            logger.error(f"数据更新失败: {str(e)}")
            return False
    
    def _update_in_db(self, table: str, data: Dict, where_clause: str, where_params: Dict, db_type: str) -> bool:
        """在指定数据库中更新数据"""
        try:
            set_clause = ', '.join([f'{key} = :{key}' for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            
            # 合并参数
            all_params = {**data, **(where_params or {})}
            
            with self.get_session(db_type) as session:
                session.execute(text(query), all_params)
                return True
                
        except Exception as e:
            logger.error(f"在{db_type}中更新数据失败: {str(e)}")
            return False
    
    def sync_databases(self, tables: List[str] = None) -> Dict[str, bool]:
        """
        同步数据库
        
        Args:
            tables: 要同步的表列表，None表示同步所有表
            
        Returns:
            同步结果字典
        """
        if not self.backup_db in self.engines:
            logger.warning("备份数据库未配置，跳过同步")
            return {}
        
        sync_results = {}
        
        try:
            # 如果未指定表，获取所有表
            if tables is None:
                tables = self._get_table_list(self.primary_db)
            
            for table in tables:
                try:
                    # 从主数据库获取数据
                    data = self.execute_query(f"SELECT * FROM {table}", db_type=self.primary_db)
                    
                    # 清空备份数据库中的表
                    with self.get_session(self.backup_db) as session:
                        session.execute(text(f"DELETE FROM {table}"))
                    
                    # 插入数据到备份数据库
                    for row in data:
                        self._insert_to_db(table, row, self.backup_db)
                    
                    sync_results[table] = True
                    logger.info(f"表 {table} 同步成功，同步了 {len(data)} 条记录")
                    
                except Exception as e:
                    sync_results[table] = False
                    logger.error(f"表 {table} 同步失败: {str(e)}")
            
            return sync_results
            
        except Exception as e:
            logger.error(f"数据库同步失败: {str(e)}")
            return {}
    
    def _get_table_list(self, db_type: str) -> List[str]:
        """获取数据库中的表列表"""
        try:
            if db_type == 'mysql':
                query = "SHOW TABLES"
            elif db_type == 'sqlite':
                query = "SELECT name FROM sqlite_master WHERE type='table'"
            else:
                return []
            
            result = self.execute_query(query, db_type=db_type)
            
            if db_type == 'mysql':
                return [list(row.values())[0] for row in result]
            else:
                return [row['name'] for row in result]
                
        except Exception as e:
            logger.error(f"获取表列表失败 ({db_type}): {str(e)}")
            return []
    
    def get_database_status(self) -> Dict[str, Dict]:
        """获取数据库状态"""
        status = {}
        
        for db_type, engine in self.engines.items():
            try:
                with engine.connect() as conn:
                    # 测试连接
                    if db_type == 'mysql':
                        result = conn.execute(text("SELECT VERSION()"))
                        version = result.scalar()
                        conn.execute(text("SELECT 1"))
                    else:
                        result = conn.execute(text("SELECT sqlite_version()"))
                        version = result.scalar()
                        conn.execute(text("SELECT 1"))
                    
                    status[db_type] = {
                        'status': 'connected',
                        'version': version,
                        'tables': len(self._get_table_list(db_type))
                    }
                    
            except Exception as e:
                status[db_type] = {
                    'status': 'error',
                    'error': str(e),
                    'tables': 0
                }
        
        return status
    
    def close_connections(self):
        """关闭所有数据库连接"""
        for db_type, engine in self.engines.items():
            try:
                engine.dispose()
                logger.info(f"{db_type}数据库连接已关闭")
            except Exception as e:
                logger.error(f"关闭{db_type}数据库连接失败: {str(e)}")

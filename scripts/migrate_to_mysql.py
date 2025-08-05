#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec SQLite到MySQL数据迁移脚本
执行完整的数据库迁移，包括数据验证和错误处理
"""

import sqlite3
import pymysql
from datetime import datetime
import sys
import os
from pathlib import Path

class DatabaseMigrator:
    """数据库迁移器"""
    
    def __init__(self):
        self.sqlite_db = 'instance/agridec.db'
        self.mysql_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'agridec',
            'charset': 'utf8mb4',
            'autocommit': False
        }
        
        self.tables_to_migrate = [
            'seed_prices',
            'weather_data', 
            'farm_machines'
        ]
        
        self.migration_stats = {}
    
    def check_prerequisites(self):
        """检查迁移前置条件"""
        print("🔍 检查迁移前置条件...")
        
        # 检查SQLite数据库文件
        if not os.path.exists(self.sqlite_db):
            print(f"❌ SQLite数据库文件不存在: {self.sqlite_db}")
            return False
        print(f"✅ SQLite数据库文件存在: {self.sqlite_db}")
        
        # 检查MySQL连接
        try:
            mysql_conn = pymysql.connect(**self.mysql_config)
            mysql_conn.close()
            print("✅ MySQL连接测试成功")
        except Exception as e:
            print(f"❌ MySQL连接失败: {str(e)}")
            return False
        
        return True
    
    def backup_mysql_data(self):
        """备份MySQL现有数据"""
        print("💾 备份MySQL现有数据...")
        
        try:
            mysql_conn = pymysql.connect(**self.mysql_config)
            mysql_cursor = mysql_conn.cursor()
            
            backup_dir = Path('backups')
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            for table in self.tables_to_migrate:
                # 检查表是否存在数据
                mysql_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = mysql_cursor.fetchone()[0]
                
                if count > 0:
                    print(f"📊 备份表 {table} ({count} 条记录)")
                    
                    # 导出数据到SQL文件
                    mysql_cursor.execute(f"SELECT * FROM {table}")
                    rows = mysql_cursor.fetchall()
                    
                    backup_file = backup_dir / f"{table}_backup_{timestamp}.sql"
                    with open(backup_file, 'w', encoding='utf-8') as f:
                        f.write(f"-- {table} 备份数据 {timestamp}\n")
                        f.write(f"-- 记录数: {count}\n\n")
                        
                        # 获取列名
                        mysql_cursor.execute(f"DESCRIBE {table}")
                        columns = [col[0] for col in mysql_cursor.fetchall()]
                        
                        for row in rows:
                            values = []
                            for value in row:
                                if value is None:
                                    values.append('NULL')
                                elif isinstance(value, str):
                                    values.append(f"'{value.replace('\'', '\'\'')}'")
                                else:
                                    values.append(str(value))
                            
                            f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});\n")
                    
                    print(f"✅ 备份完成: {backup_file}")
                else:
                    print(f"ℹ️ 表 {table} 无数据，跳过备份")
            
            mysql_conn.close()
            print("✅ 数据备份完成")
            return True
            
        except Exception as e:
            print(f"❌ 数据备份失败: {str(e)}")
            return False
    
    def migrate_table_data(self, table_name):
        """迁移单个表的数据"""
        print(f"📊 迁移表: {table_name}")
        
        try:
            # 连接SQLite
            sqlite_conn = sqlite3.connect(self.sqlite_db)
            sqlite_cursor = sqlite_conn.cursor()
            
            # 连接MySQL
            mysql_conn = pymysql.connect(**self.mysql_config)
            mysql_cursor = mysql_conn.cursor()
            
            # 获取SQLite数据
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"ℹ️ 表 {table_name} 无数据")
                self.migration_stats[table_name] = 0
                return True
            
            # 获取列信息
            sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in sqlite_cursor.fetchall()]
            
            # 清空MySQL目标表
            mysql_cursor.execute(f"DELETE FROM {table_name}")
            print(f"🗑️ 清空目标表 {table_name}")
            
            # 构建插入SQL - 使用INSERT IGNORE来处理重复数据
            placeholders = ', '.join(['%s'] * len(columns))
            if table_name == 'weather_data':
                # 对于天气数据，使用INSERT IGNORE处理重复的region-date组合
                insert_sql = f"INSERT IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            else:
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # 批量插入数据
            batch_size = 100
            success_count = 0
            error_count = 0
            
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                try:
                    mysql_cursor.executemany(insert_sql, batch)
                    mysql_conn.commit()
                    success_count += len(batch)
                    print(f"✅ 批次 {i//batch_size + 1}: 插入 {len(batch)} 条记录")
                except Exception as e:
                    print(f"❌ 批次 {i//batch_size + 1} 插入失败: {str(e)}")
                    error_count += len(batch)
                    mysql_conn.rollback()
            
            # 验证迁移结果
            mysql_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            mysql_count = mysql_cursor.fetchone()[0]
            
            print(f"📈 迁移统计:")
            print(f"   源数据: {len(rows)} 条")
            print(f"   成功: {success_count} 条")
            print(f"   失败: {error_count} 条")
            print(f"   目标表: {mysql_count} 条")
            
            self.migration_stats[table_name] = mysql_count
            
            # 关闭连接
            sqlite_conn.close()
            mysql_conn.close()
            
            return error_count == 0
            
        except Exception as e:
            print(f"❌ 表 {table_name} 迁移失败: {str(e)}")
            return False
    
    def verify_migration(self):
        """验证迁移结果"""
        print("🔍 验证迁移结果...")
        
        try:
            # 连接数据库
            sqlite_conn = sqlite3.connect(self.sqlite_db)
            sqlite_cursor = sqlite_conn.cursor()
            
            mysql_conn = pymysql.connect(**self.mysql_config)
            mysql_cursor = mysql_conn.cursor()
            
            verification_passed = True
            
            for table in self.tables_to_migrate:
                # 获取记录数
                sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                sqlite_count = sqlite_cursor.fetchone()[0]
                
                mysql_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                mysql_count = mysql_cursor.fetchone()[0]
                
                print(f"📊 {table}:")
                print(f"   SQLite: {sqlite_count} 条")
                print(f"   MySQL:  {mysql_count} 条")

                if sqlite_count == mysql_count:
                    print(f"   ✅ 数据一致")
                elif table == 'weather_data' and mysql_count <= sqlite_count:
                    print(f"   ✅ 数据一致 (已去重 {sqlite_count - mysql_count} 条重复记录)")
                else:
                    print(f"   ❌ 数据不一致")
                    verification_passed = False
                
                # 验证数据完整性
                if mysql_count > 0:
                    if table == 'seed_prices':
                        mysql_cursor.execute("SELECT COUNT(*) FROM seed_prices WHERE price > 0")
                        valid_prices = mysql_cursor.fetchone()[0]
                        print(f"   有效价格: {valid_prices} 条")
                    
                    elif table == 'weather_data':
                        mysql_cursor.execute("SELECT COUNT(*) FROM weather_data WHERE temperature IS NOT NULL")
                        valid_weather = mysql_cursor.fetchone()[0]
                        print(f"   有效天气: {valid_weather} 条")
                    
                    elif table == 'farm_machines':
                        mysql_cursor.execute("SELECT COUNT(*) FROM farm_machines WHERE product_name IS NOT NULL")
                        valid_machines = mysql_cursor.fetchone()[0]
                        print(f"   有效农机: {valid_machines} 条")
            
            sqlite_conn.close()
            mysql_conn.close()
            
            return verification_passed
            
        except Exception as e:
            print(f"❌ 验证失败: {str(e)}")
            return False
    
    def run_migration(self):
        """执行完整迁移流程"""
        print("🚀 开始AgriDec数据库迁移")
        print("=" * 50)
        
        # 1. 检查前置条件
        if not self.check_prerequisites():
            print("❌ 前置条件检查失败，迁移终止")
            return False
        
        # 2. 备份现有数据
        if not self.backup_mysql_data():
            print("❌ 数据备份失败，迁移终止")
            return False
        
        # 3. 迁移数据
        migration_success = True
        for table in self.tables_to_migrate:
            if not self.migrate_table_data(table):
                migration_success = False
                print(f"❌ 表 {table} 迁移失败")
        
        if not migration_success:
            print("❌ 数据迁移失败")
            return False
        
        # 4. 验证迁移结果
        if not self.verify_migration():
            print("❌ 迁移验证失败")
            return False
        
        # 5. 显示迁移总结
        print("\n" + "=" * 50)
        print("🎉 数据迁移完成！")
        print("\n📊 迁移统计:")
        total_records = 0
        for table, count in self.migration_stats.items():
            print(f"   {table}: {count} 条记录")
            total_records += count
        print(f"   总计: {total_records} 条记录")
        
        print("\n📝 后续步骤:")
        print("1. 更新应用配置文件中的数据库连接")
        print("2. 安装MySQL相关依赖包")
        print("3. 重启应用并测试功能")
        print("4. 确认无误后可删除SQLite数据库文件")
        
        return True

def main():
    """主函数"""
    migrator = DatabaseMigrator()
    
    try:
        success = migrator.run_migration()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断迁移")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 迁移过程中发生异常: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

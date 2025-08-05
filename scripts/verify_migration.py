#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec MySQL迁移验证脚本
验证数据库迁移的完整性和正确性
"""

import pymysql
from datetime import datetime, timedelta
import sys
import json

class MigrationVerifier:
    """迁移验证器"""
    
    def __init__(self):
        self.mysql_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'agridec',
            'charset': 'utf8mb4'
        }
        
        self.expected_tables = [
            'seed_prices',
            'weather_data',
            'farm_machines',
            'system_config',
            'crawl_logs'
        ]
        
        self.expected_views = [
            'v_latest_seed_prices',
            'v_weather_forecast',
            'v_machine_price_stats'
        ]
        
        self.verification_results = {}
    
    def connect_mysql(self):
        """连接MySQL数据库"""
        try:
            conn = pymysql.connect(**self.mysql_config)
            return conn
        except Exception as e:
            print(f"❌ MySQL连接失败: {str(e)}")
            return None
    
    def verify_database_connection(self):
        """验证数据库连接"""
        print("🔗 验证数据库连接...")
        
        conn = self.connect_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"✅ MySQL连接成功，版本: {version}")
            conn.close()
            return True
        else:
            print("❌ 数据库连接失败")
            return False
    
    def verify_table_structure(self):
        """验证表结构"""
        print("📋 验证表结构...")
        
        conn = self.connect_mysql()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 检查表是否存在
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            print("📊 数据库表检查:")
            all_tables_exist = True
            
            for table in self.expected_tables:
                if table in existing_tables:
                    print(f"✅ {table} - 存在")
                    
                    # 检查表结构
                    cursor.execute(f"DESCRIBE {table}")
                    columns = cursor.fetchall()
                    print(f"   列数: {len(columns)}")
                    
                    # 检查索引
                    cursor.execute(f"SHOW INDEX FROM {table}")
                    indexes = cursor.fetchall()
                    print(f"   索引数: {len(indexes)}")
                    
                else:
                    print(f"❌ {table} - 不存在")
                    all_tables_exist = False
            
            # 检查视图
            print("\n👁️ 数据库视图检查:")
            cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
            existing_views = [view[0] for view in cursor.fetchall()]
            
            all_views_exist = True
            for view in self.expected_views:
                if view in existing_views:
                    print(f"✅ {view} - 存在")
                else:
                    print(f"❌ {view} - 不存在")
                    all_views_exist = False
            
            conn.close()
            return all_tables_exist and all_views_exist
            
        except Exception as e:
            print(f"❌ 表结构验证失败: {str(e)}")
            conn.close()
            return False
    
    def verify_data_integrity(self):
        """验证数据完整性"""
        print("🔍 验证数据完整性...")
        
        conn = self.connect_mysql()
        if not conn:
            return False
        
        cursor = conn.cursor()
        integrity_passed = True
        
        try:
            # 验证种子价格数据
            print("\n🌱 种子价格数据验证:")
            cursor.execute("SELECT COUNT(*) FROM seed_prices")
            total_seeds = cursor.fetchone()[0]
            print(f"   总记录数: {total_seeds}")
            
            if total_seeds > 0:
                cursor.execute("SELECT COUNT(*) FROM seed_prices WHERE price > 0")
                valid_prices = cursor.fetchone()[0]
                print(f"   有效价格: {valid_prices}")
                
                cursor.execute("SELECT COUNT(*) FROM seed_prices WHERE product_name IS NOT NULL AND product_name != ''")
                valid_names = cursor.fetchone()[0]
                print(f"   有效产品名: {valid_names}")
                
                cursor.execute("SELECT AVG(price), MIN(price), MAX(price) FROM seed_prices WHERE price > 0")
                price_stats = cursor.fetchone()
                print(f"   价格统计: 平均 {price_stats[0]:.2f}, 最低 {price_stats[1]:.2f}, 最高 {price_stats[2]:.2f}")
                
                if valid_prices < total_seeds * 0.8:  # 80%的数据应该有有效价格
                    print("   ⚠️ 价格数据完整性较低")
                    integrity_passed = False
            
            # 验证天气数据
            print("\n🌤️ 天气数据验证:")
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            total_weather = cursor.fetchone()[0]
            print(f"   总记录数: {total_weather}")
            
            if total_weather > 0:
                cursor.execute("SELECT COUNT(*) FROM weather_data WHERE temperature IS NOT NULL")
                valid_temp = cursor.fetchone()[0]
                print(f"   有效温度: {valid_temp}")
                
                cursor.execute("SELECT COUNT(DISTINCT region) FROM weather_data")
                regions = cursor.fetchone()[0]
                print(f"   覆盖地区: {regions}")
                
                cursor.execute("SELECT AVG(temperature), MIN(temperature), MAX(temperature) FROM weather_data WHERE temperature IS NOT NULL")
                temp_stats = cursor.fetchone()
                if temp_stats[0]:
                    print(f"   温度统计: 平均 {temp_stats[0]:.1f}°C, 最低 {temp_stats[1]:.1f}°C, 最高 {temp_stats[2]:.1f}°C")
            
            # 验证农机数据
            print("\n🚜 农机数据验证:")
            cursor.execute("SELECT COUNT(*) FROM farm_machines")
            total_machines = cursor.fetchone()[0]
            print(f"   总记录数: {total_machines}")
            
            if total_machines > 0:
                cursor.execute("SELECT COUNT(*) FROM farm_machines WHERE price > 0")
                valid_machine_prices = cursor.fetchone()[0]
                print(f"   有效价格: {valid_machine_prices}")
                
                cursor.execute("SELECT COUNT(DISTINCT brand) FROM farm_machines WHERE brand IS NOT NULL")
                brands = cursor.fetchone()[0]
                print(f"   品牌数量: {brands}")
                
                cursor.execute("SELECT AVG(price), MIN(price), MAX(price) FROM farm_machines WHERE price > 0")
                machine_price_stats = cursor.fetchone()
                if machine_price_stats[0]:
                    print(f"   价格统计: 平均 {machine_price_stats[0]:,.0f}元, 最低 {machine_price_stats[1]:,.0f}元, 最高 {machine_price_stats[2]:,.0f}元")
            
            # 验证系统配置
            print("\n⚙️ 系统配置验证:")
            cursor.execute("SELECT COUNT(*) FROM system_config")
            config_count = cursor.fetchone()[0]
            print(f"   配置项数量: {config_count}")
            
            if config_count > 0:
                cursor.execute("SELECT config_key, config_value FROM system_config ORDER BY config_key")
                configs = cursor.fetchall()
                for key, value in configs:
                    print(f"   {key}: {value}")
            
            conn.close()
            return integrity_passed
            
        except Exception as e:
            print(f"❌ 数据完整性验证失败: {str(e)}")
            conn.close()
            return False
    
    def verify_performance(self):
        """验证数据库性能"""
        print("⚡ 验证数据库性能...")
        
        conn = self.connect_mysql()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 测试查询性能
            performance_tests = [
                ("种子价格查询", "SELECT * FROM seed_prices WHERE region = '山东' ORDER BY date DESC LIMIT 10"),
                ("天气数据查询", "SELECT * FROM weather_data WHERE date >= CURDATE() ORDER BY region"),
                ("农机品牌统计", "SELECT brand, COUNT(*) FROM farm_machines GROUP BY brand"),
                ("最新价格视图", "SELECT * FROM v_latest_seed_prices WHERE rn = 1 LIMIT 5"),
                ("天气预报视图", "SELECT * FROM v_weather_forecast LIMIT 7")
            ]
            
            for test_name, query in performance_tests:
                start_time = datetime.now()
                cursor.execute(query)
                results = cursor.fetchall()
                end_time = datetime.now()
                
                execution_time = (end_time - start_time).total_seconds() * 1000
                print(f"   {test_name}: {len(results)} 条记录, {execution_time:.2f}ms")
                
                if execution_time > 1000:  # 超过1秒认为性能较差
                    print(f"   ⚠️ {test_name} 查询较慢")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ 性能验证失败: {str(e)}")
            conn.close()
            return False
    
    def generate_verification_report(self):
        """生成验证报告"""
        print("📄 生成验证报告...")
        
        report = {
            'verification_time': datetime.now().isoformat(),
            'database_info': {},
            'table_stats': {},
            'data_quality': {},
            'recommendations': []
        }
        
        conn = self.connect_mysql()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 数据库信息
            cursor.execute("SELECT VERSION()")
            report['database_info']['mysql_version'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT DATABASE()")
            report['database_info']['database_name'] = cursor.fetchone()[0]
            
            # 表统计
            for table in self.expected_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                report['table_stats'][table] = count
            
            # 数据质量评估
            cursor.execute("SELECT COUNT(*) FROM seed_prices WHERE price > 0")
            valid_prices = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM seed_prices")
            total_prices = cursor.fetchone()[0]
            
            if total_prices > 0:
                report['data_quality']['seed_price_completeness'] = valid_prices / total_prices
            
            # 生成建议
            if total_prices == 0:
                report['recommendations'].append("建议执行数据采集以获取种子价格数据")
            
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            weather_count = cursor.fetchone()[0]
            if weather_count == 0:
                report['recommendations'].append("建议执行天气数据采集")
            
            # 保存报告
            report_file = f"migration_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 验证报告已保存: {report_file}")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ 报告生成失败: {str(e)}")
            conn.close()
            return False
    
    def run_verification(self):
        """执行完整验证流程"""
        print("🔍 开始AgriDec迁移验证")
        print("=" * 50)
        
        verification_steps = [
            ("数据库连接", self.verify_database_connection),
            ("表结构验证", self.verify_table_structure),
            ("数据完整性", self.verify_data_integrity),
            ("性能测试", self.verify_performance),
            ("生成报告", self.generate_verification_report)
        ]
        
        all_passed = True
        
        for step_name, step_func in verification_steps:
            print(f"\n🔄 执行: {step_name}")
            try:
                result = step_func()
                if result:
                    print(f"✅ {step_name} - 通过")
                else:
                    print(f"❌ {step_name} - 失败")
                    all_passed = False
            except Exception as e:
                print(f"❌ {step_name} - 异常: {str(e)}")
                all_passed = False
        
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 所有验证通过！MySQL迁移成功！")
            print("\n📝 后续步骤:")
            print("1. 更新应用配置使用MySQL数据库")
            print("2. 重启AgriDec应用")
            print("3. 测试所有功能模块")
            print("4. 监控系统运行状态")
        else:
            print("⚠️ 部分验证失败，请检查问题并修复")
        
        return all_passed

def main():
    """主函数"""
    verifier = MigrationVerifier()
    
    try:
        success = verifier.run_verification()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断验证")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 验证过程中发生异常: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

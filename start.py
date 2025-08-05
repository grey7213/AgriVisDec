#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 快速启动脚本
简化版启动脚本，用于快速演示系统功能
"""

import os
import sys
from datetime import datetime, date, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database_connection():
    """检查数据库连接"""
    try:
        print("✓ 跳过数据库连接检查（将在应用启动时检查）")
        return True

    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        print("请确保MySQL服务正在运行，并且数据库配置正确")
        return False

def test_system_modules():
    """测试系统模块"""
    print("测试系统模块...")
    
    try:
        # 测试爬虫管理器
        from data_crawler.crawler_manager import CrawlerManager
        crawler = CrawlerManager()
        print("✓ 数据爬虫模块加载成功")
        
        # 测试数据分析器
        from data_analysis.analyzer import DataAnalyzer
        analyzer = DataAnalyzer()
        print("✓ 数据分析模块加载成功")
        
        # 测试图表生成器
        from visualization.chart_generator import ChartGenerator
        chart_generator = ChartGenerator()
        print("✓ 图表生成模块加载成功")
        
        return True
        
    except Exception as e:
        print(f"模块测试失败: {str(e)}")
        return False

def start_application():
    """启动应用程序"""
    print("\n" + "="*60)
    print("AgriDec 农户专属农业信息可视化决策系统")
    print("="*60)
    print("系统启动中...")
    
    # 检查数据库连接
    if not check_database_connection():
        print("警告: 数据库连接失败，但系统仍可运行")
    
    # 测试系统模块
    if not test_system_modules():
        print("警告: 模块测试失败，但系统仍可运行")
    
    print("\n系统功能模块:")
    print("• 种子推荐面板 - 基于数据的种子品种推荐")
    print("• 天气适宜度看板 - 农事活动天气评估")
    print("• 农具对比表 - 农机设备价格对比")
    print("• 农事日历 - 农时安排和提醒")
    print("• 农资采购模块 - 采购决策支持")
    
    print("\n技术特性:")
    print("• 基于网络爬虫的数据采集")
    print("• 专业的数据分析算法")
    print("• ECharts可视化图表")
    print("• 响应式Web界面")
    print("• MySQL/SQLite数据存储")
    
    try:
        from app import app
        
        print("\n" + "="*60)
        print("系统已启动！")
        print("访问地址: http://localhost:5000")
        print("按 Ctrl+C 停止服务器")
        print("="*60)
        
        # 启动Flask应用
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # 生产模式
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\n\n系统已停止运行")
    except Exception as e:
        print(f"\n启动失败: {str(e)}")
        print("请检查端口5000是否被占用")

if __name__ == '__main__':
    start_application()

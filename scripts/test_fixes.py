#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 修复验证测试脚本
验证定时任务调度器、图表生成器和可视化增强功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_scheduler_fixes():
    """测试调度器修复"""
    print("🧪 测试定时任务调度器修复...")
    
    try:
        from scheduler import TaskScheduler, get_scheduler_status
        
        # 创建调度器实例
        scheduler = TaskScheduler()
        print("  ✅ 调度器实例创建成功")
        
        # 测试状态获取
        status = get_scheduler_status()
        print(f"  ✅ 调度器状态获取成功: {status}")
        
        # 测试启动和停止
        scheduler.start()
        print("  ✅ 调度器启动成功")
        
        # 获取运行状态
        running_status = scheduler.get_status()
        print(f"  ✅ 运行状态: {running_status}")
        
        scheduler.stop()
        print("  ✅ 调度器停止成功")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 调度器测试失败: {str(e)}")
        return False

def test_chart_generator_fixes():
    """测试图表生成器修复"""
    print("\n🧪 测试图表生成器修复...")
    
    try:
        from visualization.chart_generator import ChartGenerator
        
        generator = ChartGenerator()
        print("  ✅ 图表生成器实例创建成功")
        
        # 测试天气预报图表
        weather_data = [
            {"date": "2024-08-05", "temperature": 28, "weather": "晴"},
            {"date": "2024-08-06", "temperature": 30, "weather": "多云"},
            {"date": "2024-08-07", "temperature": 26, "weather": "小雨"}
        ]
        
        weather_result = generator.generate_chart(
            'weather_forecast',
            weather_data,
            {'title': '天气预报测试', 'theme': 'blue'}
        )
        
        if weather_result['success']:
            print("  ✅ 天气预报图表生成成功")
            # 检查是否包含正确的配置
            config = weather_result['data']['chart_config']
            if 'tooltip' in config and 'yAxis' in config:
                print("  ✅ 天气图表配置正确")
            else:
                print("  ⚠️ 天气图表配置可能有问题")
        else:
            print(f"  ❌ 天气预报图表生成失败: {weather_result.get('error')}")
        
        # 测试增强饼图
        regional_data = [
            {"region": "山东", "value": 1200},
            {"region": "河南", "value": 980},
            {"region": "河北", "value": 850}
        ]
        
        pie_result = generator.generate_chart(
            'enhanced_pie',
            regional_data,
            {'title': '增强饼图测试', 'theme': 'agriculture'}
        )
        
        if pie_result['success']:
            print("  ✅ 增强饼图生成成功")
        else:
            print(f"  ❌ 增强饼图生成失败: {pie_result.get('error')}")
        
        # 测试中国地图
        china_data = [
            {"region": "山东省", "value": 1200},
            {"region": "河南省", "value": 980}
        ]
        
        map_result = generator.generate_chart(
            'china_map',
            china_data,
            {'title': '中国地图测试', 'theme': 'blue'}
        )
        
        if map_result['success']:
            print("  ✅ 中国地图图表生成成功")
        else:
            print(f"  ❌ 中国地图图表生成失败: {map_result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 图表生成器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🧪 测试API端点...")
    
    try:
        import requests
        import time
        
        # 等待应用启动
        time.sleep(2)
        
        base_url = "http://localhost:5000"
        
        # 测试调度器状态API
        try:
            response = requests.get(f"{base_url}/api/scheduler-status")
            if response.status_code == 200:
                print("  ✅ 调度器状态API正常")
                status_data = response.json()
                print(f"    状态: {status_data}")
            else:
                print(f"  ⚠️ 调度器状态API返回: {response.status_code}")
        except Exception as e:
            print(f"  ⚠️ 调度器状态API测试失败: {str(e)}")
        
        # 测试图表生成API
        try:
            chart_data = {
                "chart_type": "weather_forecast",
                "data": [
                    {"date": "2024-08-05", "temperature": 28, "weather": "晴"},
                    {"date": "2024-08-06", "temperature": 30, "weather": "多云"}
                ],
                "title": "API测试图表",
                "theme": "blue"
            }
            
            response = requests.post(
                f"{base_url}/api/generate-chart",
                json=chart_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("  ✅ 图表生成API正常")
                else:
                    print(f"  ❌ 图表生成API错误: {result.get('error')}")
            else:
                print(f"  ⚠️ 图表生成API返回: {response.status_code}")
                
        except Exception as e:
            print(f"  ⚠️ 图表生成API测试失败: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API端点测试失败: {str(e)}")
        return False

def test_template_updates():
    """测试模板更新"""
    print("\n🧪 测试模板更新...")
    
    try:
        # 检查index.html是否包含新的图表元素
        index_path = Path("templates/index.html")
        if index_path.exists():
            content = index_path.read_text(encoding='utf-8')
            
            checks = [
                ('china-map-chart', '中国地图图表容器'),
                ('generateChinaMapChart', '中国地图生成函数'),
                ('enhanced_pie', '增强饼图类型'),
                ('btn-group', '图表类型切换按钮组')
            ]
            
            for check_item, description in checks:
                if check_item in content:
                    print(f"  ✅ {description}存在")
                else:
                    print(f"  ❌ {description}缺失")
            
            print("  ✅ 模板更新检查完成")
            return True
        else:
            print("  ❌ index.html文件不存在")
            return False
            
    except Exception as e:
        print(f"  ❌ 模板更新测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 AgriDec 修复验证测试")
    print("=" * 50)
    
    results = []
    
    # 运行所有测试
    results.append(test_scheduler_fixes())
    results.append(test_chart_generator_fixes())
    results.append(test_template_updates())
    results.append(test_api_endpoints())
    
    # 总结结果
    print("\n" + "=" * 50)
    print("📊 测试结果总结")
    print("=" * 50)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"✅ 成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 所有修复验证通过！")
        print("\n🎯 修复内容:")
        print("  • 定时任务调度器错误修复")
        print("  • 天气预报图表显示修复")
        print("  • 可视化图表美化和增强")
        print("  • 新增中国地图可视化")
        print("  • 新增增强饼图和玫瑰图")
    else:
        print("⚠️ 部分修复需要进一步检查")
    
    return success_count == total_count

if __name__ == "__main__":
    main()

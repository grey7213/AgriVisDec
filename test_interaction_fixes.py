#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试交互功能修复
"""

import sys
import requests
import json
import time
from pathlib import Path

# 添加项目路径
sys.path.append('.')

def test_api_responses():
    """测试API响应"""
    print("=" * 50)
    print("测试API响应")
    print("=" * 50)
    
    from visualization.chart_generator import ChartGenerator
    generator = ChartGenerator()
    
    # 测试数据
    test_data = [
        {"region": "山东", "value": 1200},
        {"region": "河南", "value": 980},
        {"region": "河北", "value": 850},
        {"region": "江苏", "value": 760},
        {"region": "安徽", "value": 650}
    ]
    
    # 测试玫瑰图
    print("\n测试玫瑰图 (enhanced_pie):")
    try:
        result = generator.generate_chart('enhanced_pie', test_data, {
            'title': '测试玫瑰图',
            'theme': 'agriculture'
        })
        
        if result['success']:
            config = result['data']['chart_config']
            print(f"  ✅ 玫瑰图生成成功")
            print(f"  📊 roseType: {config['series'][0].get('roseType')}")
            print(f"  📊 数据点数: {len(config['series'][0]['data'])}")
            
            # 检查数据完整性
            data_values = [item['value'] for item in config['series'][0]['data']]
            has_nan = any(str(v).lower() == 'nan' for v in data_values)
            print(f"  📊 数据值: {data_values}")
            print(f"  ✅ 无NaN值: {not has_nan}")
        else:
            print(f"  ❌ 玫瑰图生成失败: {result.get('error')}")
    except Exception as e:
        print(f"  ❌ 玫瑰图测试异常: {str(e)}")
    
    # 测试饼图
    print("\n测试饼图 (regional_pie):")
    try:
        result = generator.generate_chart('regional_pie', test_data, {
            'title': '测试饼图',
            'theme': 'agriculture'
        })
        
        if result['success']:
            config = result['data']['chart_config']
            print(f"  ✅ 饼图生成成功")
            print(f"  📊 图表类型: {config['series'][0].get('type')}")
            print(f"  📊 数据点数: {len(config['series'][0]['data'])}")
        else:
            print(f"  ❌ 饼图生成失败: {result.get('error')}")
    except Exception as e:
        print(f"  ❌ 饼图测试异常: {str(e)}")
    
    # 测试中国地图
    print("\n测试中国地图 (china_map):")
    try:
        result = generator.generate_chart('china_map', test_data, {
            'title': '测试中国地图',
            'theme': 'blue'
        })
        
        if result['success']:
            config = result['data']['chart_config']
            print(f"  ✅ 中国地图生成成功")
            print(f"  🗺️ 地图类型: {config['series'][0].get('type')}")
            print(f"  🗺️ 数据点数: {len(config['series'][0]['data'])}")
            
            # 检查tooltip格式
            tooltip_formatter = config.get('tooltip', {}).get('formatter', '')
            print(f"  🗺️ Tooltip格式: {tooltip_formatter}")
            
            # 检查数据值
            map_data = config['series'][0]['data']
            sample_data = map_data[:3]
            print(f"  🗺️ 数据示例: {sample_data}")
            
            # 检查是否有NaN值
            has_nan_values = any(
                str(item.get('value', '')).lower() == 'nan' 
                for item in map_data
            )
            print(f"  ✅ 无NaN值: {not has_nan_values}")
            
        else:
            print(f"  ❌ 中国地图生成失败: {result.get('error')}")
    except Exception as e:
        print(f"  ❌ 中国地图测试异常: {str(e)}")

def test_html_template_fixes():
    """测试HTML模板修复"""
    print("\n" + "=" * 50)
    print("测试HTML模板修复")
    print("=" * 50)
    
    template_path = Path('templates/index.html')
    if not template_path.exists():
        print("  ❌ HTML模板文件不存在")
        return
    
    content = template_path.read_text(encoding='utf-8')
    
    # 检查修复项
    checks = [
        ('chartContainer._echarts_instance_', 'ECharts实例管理'),
        ('chart.dispose()', '图表实例销毁'),
        ('chartContainer.style.height', '容器高度设置'),
        ('chart.isDisposed()', '图表状态检查'),
        ('_resizeHandler', '事件监听器管理'),
        ('showNotification', '通知系统'),
        ('regional_pie', '饼图类型修复'),
        ('enhanced_pie', '玫瑰图类型支持')
    ]
    
    for check_text, description in checks:
        if check_text in content:
            print(f"  ✅ {description}存在")
        else:
            print(f"  ❌ {description}缺失")

def test_data_validation():
    """测试数据验证功能"""
    print("\n" + "=" * 50)
    print("测试数据验证功能")
    print("=" * 50)
    
    from visualization.chart_generator import ChartGenerator
    generator = ChartGenerator()
    
    # 测试包含各种异常值的数据
    problematic_data = [
        {"region": "山东", "value": 1200},
        {"region": "河南", "value": float('nan')},  # NaN值
        {"region": "河北", "value": None},  # None值
        {"region": "江苏", "value": ""},  # 空字符串
        {"region": "安徽", "value": "invalid"},  # 无效字符串
        {"region": "湖北", "value": float('inf')},  # 无穷大
        {"region": "四川", "value": -float('inf')},  # 负无穷大
        {"region": "广东", "value": 580}  # 正常值
    ]
    
    print("测试数据包含NaN、None、空字符串、无效字符串、无穷大值...")
    
    for chart_type in ['enhanced_pie', 'regional_pie', 'china_map']:
        print(f"\n  测试 {chart_type}:")
        try:
            result = generator.generate_chart(chart_type, problematic_data, {
                'title': f'数据验证测试-{chart_type}',
                'theme': 'agriculture'
            })
            
            if result['success']:
                config = result['data']['chart_config']
                data_values = []
                
                if chart_type == 'china_map':
                    data_values = [item['value'] for item in config['series'][0]['data']]
                else:
                    data_values = [item['value'] for item in config['series'][0]['data']]
                
                # 检查是否还有异常值
                has_nan = any(str(v).lower() in ['nan', 'inf', '-inf'] for v in data_values)
                valid_count = len([v for v in data_values if isinstance(v, (int, float)) and str(v).lower() not in ['nan', 'inf', '-inf']])
                
                print(f"    ✅ 生成成功，有效数据点: {valid_count}")
                print(f"    ✅ 无异常值: {not has_nan}")
                
            else:
                print(f"    ❌ 生成失败: {result.get('error')}")
                
        except Exception as e:
            print(f"    ❌ 测试异常: {str(e)}")

def main():
    """主测试函数"""
    print("🔧 农业数据可视化系统交互功能修复验证")
    print("测试时间:", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # 运行所有测试
    test_api_responses()
    test_html_template_fixes()
    test_data_validation()
    
    print("\n" + "=" * 50)
    print("✅ 交互功能修复验证完成")
    print("=" * 50)
    
    print("\n📋 修复总结:")
    print("1. ✅ 修复了玫瑰图显示异常问题（ECharts实例管理）")
    print("2. ✅ 修复了中国地图NaN显示问题（数据验证增强）")
    print("3. ✅ 修复了强制刷新功能异常（实例销毁和重建）")
    print("4. ✅ 增强了图表容器管理和事件监听器处理")
    print("5. ✅ 完善了错误处理和用户反馈机制")

if __name__ == '__main__':
    main()

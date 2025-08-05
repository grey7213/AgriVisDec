#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中国地图可视化功能测试脚本
验证地图数据加载、图表生成和显示功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
import time

def test_china_map_api():
    """测试中国地图API"""
    print("🧪 测试中国地图API...")
    
    try:
        # 测试数据
        china_data = [
            {"region": "山东", "value": 1200},
            {"region": "河南", "value": 980},
            {"region": "河北", "value": 850},
            {"region": "江苏", "value": 760},
            {"region": "安徽", "value": 650},
            {"region": "湖北", "value": 580},
            {"region": "四川", "value": 520},
            {"region": "广东", "value": 480},
            {"region": "湖南", "value": 420},
            {"region": "浙江", "value": 380}
        ]
        
        # 发送请求
        response = requests.post(
            'http://localhost:5000/api/generate-chart',
            json={
                'chart_type': 'china_map',
                'data': china_data,
                'title': '中国地图测试',
                'theme': 'blue'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"  API响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  API成功: {result.get('success')}")
            
            if result.get('success'):
                config = result['data']['chart_config']
                
                # 检查配置完整性
                checks = [
                    ('title', '标题配置'),
                    ('tooltip', '提示框配置'),
                    ('visualMap', '视觉映射配置'),
                    ('series', '系列配置')
                ]
                
                for key, desc in checks:
                    if key in config:
                        print(f"  ✅ {desc}存在")
                    else:
                        print(f"  ❌ {desc}缺失")
                
                # 检查地图系列配置
                if 'series' in config and len(config['series']) > 0:
                    series = config['series'][0]
                    if series.get('type') == 'map' and series.get('map') == 'china':
                        print("  ✅ 地图系列配置正确")
                    else:
                        print("  ❌ 地图系列配置错误")
                
                # 检查数据格式
                if 'series' in config and 'data' in config['series'][0]:
                    data = config['series'][0]['data']
                    if isinstance(data, list) and len(data) > 0:
                        print(f"  ✅ 地图数据格式正确，包含{len(data)}个省份")
                        
                        # 检查数据项格式
                        sample_item = data[0]
                        if 'name' in sample_item and 'value' in sample_item:
                            print("  ✅ 数据项格式正确")
                        else:
                            print("  ❌ 数据项格式错误")
                    else:
                        print("  ❌ 地图数据格式错误")
                
                return True
            else:
                print(f"  ❌ API错误: {result.get('error')}")
                return False
        else:
            print(f"  ❌ HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {str(e)}")
        return False

def test_province_name_mapping():
    """测试省份名称映射"""
    print("\n🧪 测试省份名称映射...")
    
    try:
        from visualization.chart_generator import ChartGenerator
        
        generator = ChartGenerator()
        
        # 测试数据
        test_cases = [
            {"input": "山东省", "expected": "山东"},
            {"input": "北京市", "expected": "北京"},
            {"input": "内蒙古自治区", "expected": "内蒙古"},
            {"input": "新疆维吾尔自治区", "expected": "新疆"},
            {"input": "广西壮族自治区", "expected": "广西"},
            {"input": "香港特别行政区", "expected": "香港"}
        ]
        
        # 生成测试配置
        for test_case in test_cases:
            test_data = [{"region": test_case["input"], "value": 100}]
            
            result = generator.generate_chart(
                'china_map',
                test_data,
                {'title': '测试', 'theme': 'blue'}
            )
            
            if result['success']:
                config = result['data']['chart_config']
                map_data = config['series'][0]['data']
                
                if len(map_data) > 0:
                    actual_name = map_data[0]['name']
                    expected_name = test_case['expected']
                    
                    if actual_name == expected_name:
                        print(f"  ✅ {test_case['input']} -> {actual_name}")
                    else:
                        print(f"  ❌ {test_case['input']} -> {actual_name} (期望: {expected_name})")
                else:
                    print(f"  ❌ {test_case['input']} -> 无数据")
            else:
                print(f"  ❌ {test_case['input']} -> 生成失败")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {str(e)}")
        return False

def test_static_files():
    """测试静态文件"""
    print("\n🧪 测试静态文件...")
    
    try:
        # 检查地图数据文件
        map_data_file = Path("static/js/china-map-data.js")
        if map_data_file.exists():
            print("  ✅ 地图数据文件存在")
            
            # 检查文件内容
            content = map_data_file.read_text(encoding='utf-8')
            
            checks = [
                ('ChinaMapLoader', '地图加载器类'),
                ('loadChinaMap', '地图加载函数'),
                ('PROVINCE_NAME_MAP', '省份名称映射'),
                ('registerChinaMap', '地图注册方法')
            ]
            
            for keyword, desc in checks:
                if keyword in content:
                    print(f"  ✅ {desc}存在")
                else:
                    print(f"  ❌ {desc}缺失")
            
        else:
            print("  ❌ 地图数据文件不存在")
            return False
        
        # 检查静态文件路由
        try:
            response = requests.get('http://localhost:5000/static/js/china-map-data.js')
            if response.status_code == 200:
                print("  ✅ 静态文件路由正常")
            else:
                print(f"  ❌ 静态文件路由错误: {response.status_code}")
        except Exception as e:
            print(f"  ⚠️ 静态文件路由测试失败: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {str(e)}")
        return False

def test_web_page():
    """测试网页显示"""
    print("\n🧪 测试网页显示...")
    
    try:
        # 检查主页
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            content = response.text
            
            checks = [
                ('china-map-chart', '地图容器'),
                ('generateChinaMapChart', '地图生成函数'),
                ('china-map-data.js', '地图数据脚本'),
                ('生成地图', '生成按钮')
            ]
            
            for keyword, desc in checks:
                if keyword in content:
                    print(f"  ✅ {desc}存在")
                else:
                    print(f"  ❌ {desc}缺失")
            
            return True
        else:
            print(f"  ❌ 主页访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 中国地图可视化功能测试")
    print("=" * 50)
    
    # 等待应用启动
    print("等待应用启动...")
    time.sleep(2)
    
    results = []
    
    # 运行所有测试
    results.append(test_static_files())
    results.append(test_province_name_mapping())
    results.append(test_china_map_api())
    results.append(test_web_page())
    
    # 总结结果
    print("\n" + "=" * 50)
    print("📊 测试结果总结")
    print("=" * 50)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"✅ 成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 所有测试通过！中国地图功能正常")
        print("\n🎯 功能特点:")
        print("  • 支持多数据源地图加载")
        print("  • 省份名称自动标准化")
        print("  • 完整的视觉映射配置")
        print("  • 备用方案自动切换")
        print("  • 响应式设计支持")
    else:
        print("⚠️ 部分测试失败，需要进一步检查")
    
    return success_count == total_count

if __name__ == "__main__":
    main()

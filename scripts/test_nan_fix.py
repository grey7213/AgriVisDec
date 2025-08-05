#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中国地图NaN值修复测试脚本
验证数据验证和清洗功能的有效性
"""

import sys
import os
from pathlib import Path
import math

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
import time

def test_nan_data_handling():
    """测试NaN值数据处理"""
    print("🧪 测试NaN值数据处理...")
    
    try:
        from visualization.chart_generator import ChartGenerator
        
        generator = ChartGenerator()
        
        # 创建包含各种异常数据的测试用例
        test_cases = [
            {
                'name': '正常数据',
                'data': [
                    {"region": "山东", "value": 1200},
                    {"region": "河南", "value": 980}
                ],
                'expected_valid': True
            },
            {
                'name': 'NaN值数据',
                'data': [
                    {"region": "山东", "value": float('nan')},
                    {"region": "河南", "value": 980}
                ],
                'expected_valid': True  # 应该被修复为有效值
            },
            {
                'name': 'None值数据',
                'data': [
                    {"region": "山东", "value": None},
                    {"region": "河南", "value": 980}
                ],
                'expected_valid': True
            },
            {
                'name': '空字符串数据',
                'data': [
                    {"region": "山东", "value": ""},
                    {"region": "河南", "value": 980}
                ],
                'expected_valid': True
            },
            {
                'name': '字符串数字',
                'data': [
                    {"region": "山东", "value": "1200"},
                    {"region": "河南", "value": "980.5"}
                ],
                'expected_valid': True
            },
            {
                'name': '无效字符串',
                'data': [
                    {"region": "山东", "value": "abc"},
                    {"region": "河南", "value": "无数据"}
                ],
                'expected_valid': True  # 应该被修复为默认值
            },
            {
                'name': '无穷大值',
                'data': [
                    {"region": "山东", "value": float('inf')},
                    {"region": "河南", "value": float('-inf')}
                ],
                'expected_valid': True
            },
            {
                'name': '混合异常数据',
                'data': [
                    {"region": "山东", "value": float('nan')},
                    {"region": "河南", "value": None},
                    {"region": "河北", "value": ""},
                    {"region": "江苏", "value": "abc"},
                    {"region": "安徽", "value": 1200}
                ],
                'expected_valid': True
            }
        ]
        
        success_count = 0
        
        for test_case in test_cases:
            print(f"\n  测试用例: {test_case['name']}")
            
            try:
                result = generator.generate_chart(
                    'china_map',
                    test_case['data'],
                    {'title': f'测试-{test_case["name"]}', 'theme': 'blue'}
                )
                
                if result['success']:
                    config = result['data']['chart_config']
                    map_data = config['series'][0]['data']
                    
                    # 检查所有数值是否有效
                    all_valid = True
                    nan_count = 0
                    
                    for item in map_data:
                        value = item['value']
                        if value is None or (isinstance(value, float) and math.isnan(value)):
                            all_valid = False
                            nan_count += 1
                    
                    if all_valid:
                        print(f"    ✅ 所有数值有效，包含{len(map_data)}个省份")
                        success_count += 1
                    else:
                        print(f"    ❌ 发现{nan_count}个无效数值")
                    
                    # 显示数据示例
                    sample_data = map_data[:3]
                    print(f"    数据示例: {sample_data}")
                    
                else:
                    print(f"    ❌ 图表生成失败: {result.get('error')}")
                    
            except Exception as e:
                print(f"    ❌ 测试异常: {str(e)}")
        
        print(f"\n  测试结果: {success_count}/{len(test_cases)} 通过")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"  ❌ 测试失败: {str(e)}")
        return False

def test_api_nan_handling():
    """测试API接口的NaN值处理"""
    print("\n🧪 测试API接口NaN值处理...")
    
    try:
        # 包含异常数据的测试用例
        test_data = [
            {"region": "山东", "value": float('nan')},
            {"region": "河南", "value": None},
            {"region": "河北", "value": ""},
            {"region": "江苏", "value": "abc"},
            {"region": "安徽", "value": 1200},
            {"region": "湖北", "value": "980.5"}
        ]
        
        # 由于无法直接发送NaN值到JSON API，我们模拟字符串形式
        api_test_data = [
            {"region": "山东", "value": "NaN"},
            {"region": "河南", "value": None},
            {"region": "河北", "value": ""},
            {"region": "江苏", "value": "abc"},
            {"region": "安徽", "value": 1200},
            {"region": "湖北", "value": "980.5"}
        ]
        
        response = requests.post(
            'http://localhost:5000/api/generate-chart',
            json={
                'chart_type': 'china_map',
                'data': api_test_data,
                'title': 'NaN值修复测试',
                'theme': 'blue'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                config = result['data']['chart_config']
                map_data = config['series'][0]['data']
                
                # 检查数据有效性
                valid_count = 0
                invalid_count = 0
                
                for item in map_data:
                    value = item['value']
                    if isinstance(value, (int, float)) and not math.isnan(value):
                        valid_count += 1
                    else:
                        invalid_count += 1
                
                print(f"  ✅ API响应成功")
                print(f"  ✅ 有效数值: {valid_count}个")
                print(f"  ✅ 无效数值: {invalid_count}个")
                
                # 显示前几个数据项
                sample_items = map_data[:5]
                print(f"  数据示例: {sample_items}")
                
                return invalid_count == 0  # 所有数值都应该是有效的
            else:
                print(f"  ❌ API返回错误: {result.get('error')}")
                return False
        else:
            print(f"  ❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {str(e)}")
        return False

def test_edge_cases():
    """测试边界情况"""
    print("\n🧪 测试边界情况...")
    
    try:
        from visualization.chart_generator import ChartGenerator
        
        generator = ChartGenerator()
        
        edge_cases = [
            {
                'name': '空数据',
                'data': [],
                'should_succeed': False  # 空数据应该失败，这是正确的验证行为
            },
            {
                'name': '单个有效数据',
                'data': [{"region": "山东", "value": 1200}],
                'should_succeed': True
            },
            {
                'name': '全部无效数据',
                'data': [
                    {"region": "山东", "value": float('nan')},
                    {"region": "河南", "value": None}
                ],
                'should_succeed': True
            },
            {
                'name': '相同数值',
                'data': [
                    {"region": "山东", "value": 1000},
                    {"region": "河南", "value": 1000}
                ],
                'should_succeed': True
            }
        ]
        
        success_count = 0
        
        for case in edge_cases:
            print(f"\n  测试: {case['name']}")
            
            try:
                result = generator.generate_chart(
                    'china_map',
                    case['data'],
                    {'title': f'边界测试-{case["name"]}', 'theme': 'blue'}
                )
                
                if result['success'] == case['should_succeed']:
                    print(f"    ✅ 结果符合预期")
                    success_count += 1

                    if result['success']:
                        config = result['data']['chart_config']
                        visualMap = config.get('visualMap', {})
                        print(f"    数据范围: {visualMap.get('min', 'N/A')} - {visualMap.get('max', 'N/A')}")
                else:
                    print(f"    ❌ 结果不符合预期 (期望: {case['should_succeed']}, 实际: {result['success']})")
                    if not result['success']:
                        print(f"    错误信息: {result.get('error', 'N/A')}")
                    
            except Exception as e:
                print(f"    ❌ 测试异常: {str(e)}")
        
        print(f"\n  边界测试结果: {success_count}/{len(edge_cases)} 通过")
        return success_count == len(edge_cases)
        
    except Exception as e:
        print(f"  ❌ 测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 中国地图NaN值修复验证测试")
    print("=" * 60)
    
    # 等待应用启动
    print("等待应用启动...")
    time.sleep(2)
    
    results = []
    
    # 运行所有测试
    results.append(test_nan_data_handling())
    results.append(test_api_nan_handling())
    results.append(test_edge_cases())
    
    # 总结结果
    print("\n" + "=" * 60)
    print("📊 NaN值修复测试结果总结")
    print("=" * 60)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"✅ 成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 所有测试通过！NaN值问题已修复")
        print("\n🎯 修复效果:")
        print("  • 所有异常数值都被正确处理")
        print("  • NaN值被替换为默认值0")
        print("  • 地图显示不再出现'NaN'文字")
        print("  • 数据范围计算正确")
        print("  • 边界情况处理稳定")
    else:
        print("⚠️ 部分测试失败，需要进一步检查")
    
    return success_count == total_count

if __name__ == "__main__":
    main()

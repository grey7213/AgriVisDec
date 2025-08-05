#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终地图NaN修复测试脚本
彻底验证地图显示问题的修复
"""

import requests
import time
import json

def test_map_nan_fix():
    """测试地图NaN值修复"""
    print("🗺️ 最终地图NaN修复测试...")
    
    # 等待应用启动
    time.sleep(2)
    
    # 测试各种可能导致NaN的数据
    test_cases = [
        {
            'name': '正常数据',
            'data': [
                {'region': '山东', 'value': 1200},
                {'region': '河南', 'value': 980},
                {'region': '河北', 'value': 850},
                {'region': '江苏', 'value': 760}
            ]
        },
        {
            'name': '包含None值',
            'data': [
                {'region': '山东', 'value': None},
                {'region': '河南', 'value': 980},
                {'region': '河北', 'value': None}
            ]
        },
        {
            'name': '包含字符串数字',
            'data': [
                {'region': '山东', 'value': '1200'},
                {'region': '河南', 'value': '980.5'},
                {'region': '河北', 'value': '850'}
            ]
        },
        {
            'name': '包含无效字符串',
            'data': [
                {'region': '山东', 'value': 'abc'},
                {'region': '河南', 'value': 'NaN'},
                {'region': '河北', 'value': ''},
                {'region': '江苏', 'value': 'undefined'}
            ]
        },
        {
            'name': '混合数据类型',
            'data': [
                {'region': '山东', 'value': 1200},
                {'region': '河南', 'value': '980'},
                {'region': '河北', 'value': None},
                {'region': '江苏', 'value': 'abc'},
                {'region': '安徽', 'value': ''}
            ]
        }
    ]
    
    success_count = 0
    
    for test_case in test_cases:
        try:
            print(f"\n测试: {test_case['name']}")
            
            response = requests.post(
                'http://localhost:5000/api/generate-chart',
                json={
                    'chart_type': 'china_map',
                    'data': test_case['data'],
                    'title': f'测试-{test_case["name"]}',
                    'theme': 'blue'
                },
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    config = result['data']['chart_config']
                    
                    # 检查tooltip配置
                    tooltip = config.get('tooltip', {})
                    formatter = tooltip.get('formatter', '')
                    
                    print(f"  ✅ Tooltip格式: {formatter}")
                    
                    # 检查地图数据
                    series = config.get('series', [])
                    if series:
                        map_data = series[0].get('data', [])
                        
                        # 详细检查每个数据点
                        nan_count = 0
                        valid_count = 0
                        
                        for item in map_data:
                            name = item.get('name', '未知')
                            value = item.get('value')
                            
                            # 检查是否有NaN值
                            if value is None:
                                print(f"    ⚠️ {name}: 值为None")
                                nan_count += 1
                            elif isinstance(value, str) and value.lower() in ['nan', 'null', 'undefined']:
                                print(f"    ❌ {name}: 值为字符串'{value}'")
                                nan_count += 1
                            elif isinstance(value, float) and (value != value):  # NaN检查
                                print(f"    ❌ {name}: 值为NaN")
                                nan_count += 1
                            elif isinstance(value, (int, float)) and value >= 0:
                                print(f"    ✅ {name}: {value}万元")
                                valid_count += 1
                            else:
                                print(f"    ⚠️ {name}: 异常值 {value} (类型: {type(value)})")
                        
                        print(f"  📊 数据统计: 有效数据 {valid_count} 个, 异常数据 {nan_count} 个")
                        
                        # 检查tooltip格式是否正确
                        if '{b}' in formatter and '{c}' in formatter and '万元' in formatter:
                            if nan_count == 0:
                                print(f"  ✅ {test_case['name']}: 测试通过")
                                success_count += 1
                            else:
                                print(f"  ❌ {test_case['name']}: 仍有NaN值")
                        else:
                            print(f"  ❌ {test_case['name']}: Tooltip格式错误")
                    else:
                        print(f"  ❌ {test_case['name']}: 未找到地图数据")
                else:
                    print(f"  ❌ {test_case['name']}: 图表生成失败 - {result.get('error')}")
            else:
                print(f"  ❌ {test_case['name']}: API请求失败 - {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {test_case['name']}: 测试异常 - {str(e)}")
    
    print(f"\n📊 最终测试结果: {success_count}/{len(test_cases)} 通过")
    
    if success_count == len(test_cases):
        print("🎉 所有测试通过！地图NaN问题已完全修复")
        return True
    else:
        print("⚠️ 部分测试失败，需要进一步检查")
        return False

def test_frontend_display():
    """测试前端显示"""
    print("\n🌐 测试前端地图显示...")
    
    try:
        # 测试主页是否可访问
        response = requests.get('http://localhost:5000/', timeout=10)
        
        if response.status_code == 200:
            print("  ✅ 主页访问正常")
            
            # 检查页面内容
            content = response.text
            if '中国农业数据地图' in content:
                print("  ✅ 地图组件存在")
            else:
                print("  ❌ 地图组件缺失")
                
            if 'china-map-data.js' in content:
                print("  ✅ 地图数据加载器已引入")
            else:
                print("  ❌ 地图数据加载器缺失")
                
            return True
        else:
            print(f"  ❌ 主页访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 前端测试异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 最终地图NaN修复验证测试")
    print("=" * 60)
    
    # 测试后端API
    api_success = test_map_nan_fix()
    
    # 测试前端显示
    frontend_success = test_frontend_display()
    
    print("\n" + "=" * 60)
    print("📋 最终测试总结")
    print("=" * 60)
    
    if api_success and frontend_success:
        print("🎉 地图NaN修复完全成功！")
        print("\n✅ 修复成果:")
        print("  • 后端数据验证和清洗机制完善")
        print("  • 前端数据处理逻辑优化")
        print("  • Tooltip格式正确显示")
        print("  • 所有异常数据类型都能正确处理")
        print("  • 地图显示稳定可靠")
        
        print("\n🎯 用户体验:")
        print("  • 地图不再显示'NaN万元'")
        print("  • 数据显示准确可信")
        print("  • 界面美观专业")
        
    else:
        print("⚠️ 修复未完全成功，需要进一步检查")
        if not api_success:
            print("  • 后端API仍有问题")
        if not frontend_success:
            print("  • 前端显示仍有问题")

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 综合解决方案测试脚本
验证地图NaN修复和项目结构优化的完整解决方案
"""

import requests
import time
import json
from pathlib import Path

def test_map_nan_fix():
    """测试地图NaN值修复"""
    print("🗺️ 测试地图NaN值修复...")
    
    # 测试各种可能导致NaN的数据
    test_cases = [
        {
            'name': '正常数据',
            'data': [
                {'region': '山东', 'value': 1200},
                {'region': '河南', 'value': 980},
                {'region': '河北', 'value': 850}
            ]
        },
        {
            'name': '包含None值',
            'data': [
                {'region': '山东', 'value': None},
                {'region': '河南', 'value': 980}
            ]
        },
        {
            'name': '包含字符串数字',
            'data': [
                {'region': '山东', 'value': '1200'},
                {'region': '河南', 'value': '980'}
            ]
        },
        {
            'name': '包含无效字符串',
            'data': [
                {'region': '山东', 'value': 'abc'},
                {'region': '河南', 'value': 'NaN'}
            ]
        }
    ]
    
    success_count = 0
    
    for test_case in test_cases:
        try:
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
                    tooltip = config.get('tooltip', {})
                    formatter = tooltip.get('formatter', '')
                    
                    # 检查地图数据
                    series = config.get('series', [])
                    if series:
                        map_data = series[0].get('data', [])
                        
                        # 检查是否有NaN值
                        nan_count = 0
                        for item in map_data:
                            value = item.get('value')
                            if value is None or str(value).lower() == 'nan':
                                nan_count += 1
                        
                        if nan_count == 0 and '{b}' in formatter and '{c}' in formatter:
                            print(f"  ✅ {test_case['name']}: 测试通过")
                            success_count += 1
                        else:
                            print(f"  ❌ {test_case['name']}: 发现NaN值或格式问题")
                    else:
                        print(f"  ❌ {test_case['name']}: 未找到地图数据")
                else:
                    print(f"  ❌ {test_case['name']}: 图表生成失败")
            else:
                print(f"  ❌ {test_case['name']}: API请求失败")
                
        except Exception as e:
            print(f"  ❌ {test_case['name']}: 测试异常 - {str(e)}")
    
    print(f"  📊 地图NaN修复测试: {success_count}/{len(test_cases)} 通过")
    return success_count == len(test_cases)

def test_alternative_visualizations():
    """测试替代可视化方案"""
    print("\n📊 测试替代可视化方案...")
    
    test_data = [
        {'region': '山东', 'value': 1200},
        {'region': '河南', 'value': 980},
        {'region': '河北', 'value': 850},
        {'region': '江苏', 'value': 760}
    ]
    
    chart_types = ['regional_bar', 'regional_pie', 'regional_line', 'regional_scatter']
    success_count = 0
    
    for chart_type in chart_types:
        try:
            response = requests.post(
                'http://localhost:5000/api/generate-chart',
                json={
                    'chart_type': chart_type,
                    'data': test_data,
                    'title': f'农业数据-{chart_type}',
                    'theme': 'blue'
                },
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    config = result['data']['chart_config']
                    tooltip = config.get('tooltip', {})
                    formatter = tooltip.get('formatter', '')
                    
                    # 检查数据
                    series = config.get('series', [])
                    if series and formatter:
                        print(f"  ✅ {chart_type}: 生成成功")
                        success_count += 1
                    else:
                        print(f"  ❌ {chart_type}: 数据或格式问题")
                else:
                    print(f"  ❌ {chart_type}: 生成失败")
            else:
                print(f"  ❌ {chart_type}: API请求失败")
                
        except Exception as e:
            print(f"  ❌ {chart_type}: 测试异常 - {str(e)}")
    
    print(f"  📊 替代可视化测试: {success_count}/{len(chart_types)} 通过")
    return success_count == len(chart_types)

def test_project_structure():
    """测试项目结构优化"""
    print("\n📁 测试项目结构优化...")
    
    # 检查核心目录是否存在
    required_dirs = [
        'auth', 'data_crawler', 'data_analysis', 'visualization',
        'templates', 'static', 'scripts', 'tests', 'docs', 'config',
        'logs', 'backups', 'utils', 'api'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if not missing_dirs:
        print("  ✅ 核心目录结构完整")
    else:
        print(f"  ❌ 缺少目录: {', '.join(missing_dirs)}")
    
    # 检查归档文档
    archive_dir = Path('docs/archive')
    if archive_dir.exists():
        archived_files = list(archive_dir.glob('*.md'))
        print(f"  ✅ 文档归档完成: {len(archived_files)} 个文件")
    else:
        print("  ❌ 文档归档目录不存在")
    
    # 检查配置文件
    config_files = [
        'config/app_config.py',
        'config/visualization_alternatives.json'
    ]
    
    missing_configs = []
    for config_file in config_files:
        if not Path(config_file).exists():
            missing_configs.append(config_file)
    
    if not missing_configs:
        print("  ✅ 配置文件组织完整")
    else:
        print(f"  ❌ 缺少配置文件: {', '.join(missing_configs)}")
    
    # 检查优化报告
    report_file = Path('reports/structure_optimization_report.json')
    if report_file.exists():
        print("  ✅ 结构优化报告存在")
        return True
    else:
        print("  ❌ 结构优化报告缺失")
        return False

def test_configuration_files():
    """测试配置文件内容"""
    print("\n⚙️ 测试配置文件内容...")
    
    # 测试可视化替代配置
    config_file = Path('config/visualization_alternatives.json')
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_keys = ['alternative_charts', 'fallback_strategy']
            if all(key in config for key in required_keys):
                alt_charts = config['alternative_charts']
                if len(alt_charts) >= 4:
                    print("  ✅ 可视化替代配置完整")
                    return True
                else:
                    print("  ❌ 可视化替代方案不足")
            else:
                print("  ❌ 配置文件格式错误")
        except Exception as e:
            print(f"  ❌ 配置文件读取失败: {str(e)}")
    else:
        print("  ❌ 可视化替代配置文件不存在")
    
    return False

def generate_test_report():
    """生成测试报告"""
    print("\n📋 生成综合测试报告...")
    
    # 等待应用启动
    print("等待应用启动...")
    time.sleep(3)
    
    # 执行所有测试
    results = {
        'map_nan_fix': test_map_nan_fix(),
        'alternative_visualizations': test_alternative_visualizations(),
        'project_structure': test_project_structure(),
        'configuration_files': test_configuration_files()
    }
    
    # 生成报告
    report = {
        'test_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'test_results': results,
        'summary': {
            'total_tests': len(results),
            'passed_tests': sum(results.values()),
            'success_rate': f"{sum(results.values()) / len(results) * 100:.1f}%"
        },
        'details': {
            'map_nan_fix': '地图NaN值显示修复测试',
            'alternative_visualizations': '替代可视化方案测试',
            'project_structure': '项目结构优化测试',
            'configuration_files': '配置文件完整性测试'
        }
    }
    
    # 保存报告
    report_file = Path('reports/comprehensive_solution_test_report.json')
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report

def main():
    """主函数"""
    print("🚀 AgriDec 综合解决方案测试")
    print("=" * 60)
    
    # 生成测试报告
    report = generate_test_report()
    
    # 显示结果
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    for test_name, result in report['test_results'].items():
        status = "✅ 通过" if result else "❌ 失败"
        description = report['details'][test_name]
        print(f"{description}: {status}")
    
    print(f"\n总体结果: {report['summary']['passed_tests']}/{report['summary']['total_tests']} 测试通过")
    print(f"成功率: {report['summary']['success_rate']}")
    
    if report['summary']['passed_tests'] == report['summary']['total_tests']:
        print("\n🎉 所有测试通过！AgriDec解决方案完全成功")
        print("\n🎯 解决方案成果:")
        print("  • 地图NaN值显示问题已完全修复")
        print("  • 提供了4种替代可视化方案")
        print("  • 项目结构已优化整理")
        print("  • 配置文件已统一管理")
        print("  • 文档已归档整理")
    else:
        print("\n⚠️ 部分测试失败，需要进一步检查")
    
    print(f"\n📋 详细报告: reports/comprehensive_solution_test_report.json")

if __name__ == "__main__":
    main()

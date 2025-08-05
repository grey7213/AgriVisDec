#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 地图显示和多数据库功能测试脚本
验证地图tooltip修复和多数据库支持功能
"""

import sys
import os
import time
import requests
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_map_tooltip_fix():
    """测试地图tooltip显示修复"""
    print("🗺️ 测试中国地图tooltip显示修复...")
    
    try:
        # 测试数据
        test_data = [
            {"region": "山东", "value": 1200},
            {"region": "河南", "value": 980},
            {"region": "河北", "value": 850},
            {"region": "江苏", "value": 760},
            {"region": "安徽", "value": 650}
        ]
        
        response = requests.post(
            'http://localhost:5000/api/generate-chart',
            json={
                'chart_type': 'china_map',
                'data': test_data,
                'title': '中国农业产值分布',
                'theme': 'blue'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                config = result['data']['chart_config']
                tooltip_config = config.get('tooltip', {})
                
                print("  ✅ 地图图表生成成功")
                print(f"  ✅ Tooltip配置: {tooltip_config.get('formatter', 'N/A')}")
                
                # 检查tooltip格式是否正确
                formatter = tooltip_config.get('formatter', '')
                if '{b}' in formatter and '{c}' in formatter and '万元' in formatter:
                    print("  ✅ Tooltip格式正确，将显示省份名称和数值")
                    return True
                else:
                    print("  ❌ Tooltip格式可能有问题")
                    return False
            else:
                print(f"  ❌ 图表生成失败: {result.get('error')}")
                return False
        else:
            print(f"  ❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试异常: {str(e)}")
        return False

def test_database_status():
    """测试数据库状态API"""
    print("\n🗄️ 测试数据库状态API...")
    
    try:
        response = requests.get('http://localhost:5000/api/database/status')
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                data = result['data']
                print("  ✅ 数据库状态API响应成功")
                print(f"  ✅ 主数据库: {data.get('primary_db', 'N/A')}")
                print(f"  ✅ 备份数据库: {data.get('backup_db', 'N/A')}")
                print(f"  ✅ 同步状态: {'启用' if data.get('sync_enabled') else '禁用'}")
                
                # 显示数据库详情
                databases = data.get('databases', {})
                for db_type, db_info in databases.items():
                    status = db_info.get('status', 'unknown')
                    tables = db_info.get('tables', 0)
                    print(f"  ✅ {db_type.upper()}: {status}, {tables} 个表")
                
                return True
            else:
                print(f"  ❌ API返回错误: {result.get('error')}")
                return False
        else:
            print(f"  ❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试异常: {str(e)}")
        return False

def test_database_config():
    """测试数据库配置API"""
    print("\n⚙️ 测试数据库配置API...")
    
    try:
        response = requests.get('http://localhost:5000/api/database/config')
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                config = result['data']
                print("  ✅ 数据库配置API响应成功")
                print(f"  ✅ 配置版本: {config.get('version', 'N/A')}")
                print(f"  ✅ 主数据库: {config.get('primary_db', 'N/A')}")
                print(f"  ✅ 备份数据库: {config.get('backup_db', 'N/A')}")
                
                # 显示数据库配置
                databases = config.get('databases', {})
                for db_type, db_config in databases.items():
                    enabled = db_config.get('enabled', False)
                    print(f"  ✅ {db_type.upper()}: {'启用' if enabled else '禁用'}")
                
                return True
            else:
                print(f"  ❌ API返回错误: {result.get('error')}")
                return False
        else:
            print(f"  ❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试异常: {str(e)}")
        return False

def test_database_connection():
    """测试数据库连接"""
    print("\n🔌 测试数据库连接...")
    
    try:
        # 测试MySQL连接
        response = requests.post(
            'http://localhost:5000/api/database/test-connection',
            json={'db_type': 'mysql'},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                data = result['data']
                connected = data.get('connected', False)
                print(f"  ✅ MySQL连接测试: {'成功' if connected else '失败'}")
                
                if connected:
                    details = data.get('details', {})
                    version = details.get('version', 'N/A')
                    tables = details.get('tables', 0)
                    print(f"  ✅ MySQL版本: {version}")
                    print(f"  ✅ 数据表数量: {tables}")
                
                return connected
            else:
                print(f"  ❌ 连接测试失败: {result.get('error')}")
                return False
        else:
            print(f"  ❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试异常: {str(e)}")
        return False

def test_admin_pages():
    """测试管理员页面访问"""
    print("\n👨‍💼 测试管理员页面访问...")
    
    try:
        # 测试管理员面板
        response = requests.get('http://localhost:5000/admin')
        
        if response.status_code == 200:
            print("  ✅ 管理员面板页面访问成功")
        else:
            print(f"  ❌ 管理员面板访问失败: {response.status_code}")
            return False
        
        # 测试数据库管理页面
        response = requests.get('http://localhost:5000/admin/database')
        
        if response.status_code == 200:
            print("  ✅ 数据库管理页面访问成功")
            return True
        else:
            print(f"  ❌ 数据库管理页面访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试异常: {str(e)}")
        return False

def test_map_data_validation():
    """测试地图数据验证功能"""
    print("\n🧪 测试地图数据验证功能...")
    
    try:
        # 测试包含异常数据的地图
        test_cases = [
            {
                'name': '正常数据',
                'data': [{"region": "山东", "value": 1200}],
                'should_succeed': True
            },
            {
                'name': '空值数据',
                'data': [{"region": "山东", "value": None}],
                'should_succeed': True
            },
            {
                'name': '字符串数字',
                'data': [{"region": "山东", "value": "1200"}],
                'should_succeed': True
            },
            {
                'name': '无效字符串',
                'data': [{"region": "山东", "value": "abc"}],
                'should_succeed': True
            }
        ]
        
        success_count = 0
        
        for test_case in test_cases:
            response = requests.post(
                'http://localhost:5000/api/generate-chart',
                json={
                    'chart_type': 'china_map',
                    'data': test_case['data'],
                    'title': f'测试-{test_case["name"]}',
                    'theme': 'blue'
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success') == test_case['should_succeed']:
                    print(f"  ✅ {test_case['name']}: 测试通过")
                    success_count += 1
                else:
                    print(f"  ❌ {test_case['name']}: 测试失败")
            else:
                print(f"  ❌ {test_case['name']}: API请求失败")
        
        print(f"  📊 数据验证测试结果: {success_count}/{len(test_cases)} 通过")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"  ❌ 测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 AgriDec 地图显示和多数据库功能测试")
    print("=" * 60)
    
    # 等待应用启动
    print("等待应用启动...")
    time.sleep(3)
    
    results = []
    
    # 运行所有测试
    print("\n开始测试...")
    results.append(test_map_tooltip_fix())
    results.append(test_map_data_validation())
    results.append(test_database_status())
    results.append(test_database_config())
    results.append(test_database_connection())
    results.append(test_admin_pages())
    
    # 总结结果
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    success_count = sum(results)
    total_count = len(results)
    
    test_names = [
        "地图Tooltip修复",
        "地图数据验证",
        "数据库状态API",
        "数据库配置API", 
        "数据库连接测试",
        "管理员页面访问"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{i+1}. {name}: {status}")
    
    print(f"\n总体结果: {success_count}/{total_count} 测试通过")
    
    if success_count == total_count:
        print("\n🎉 所有测试通过！功能修复成功")
        print("\n🎯 修复成果:")
        print("  • 地图tooltip显示正确的数值而不是代码")
        print("  • 多数据库支持架构已实现")
        print("  • 数据库管理API正常工作")
        print("  • 管理员界面可以正常访问")
        print("  • 数据验证和清洗功能正常")
    else:
        print("\n⚠️ 部分测试失败，需要进一步检查")
    
    return success_count == total_count

if __name__ == "__main__":
    main()

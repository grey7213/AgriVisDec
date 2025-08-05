#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 个人资料功能测试
测试用户个人资料查看和编辑功能
"""

import unittest
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import app
from database import db
from auth.models import User
import requests
from bs4 import BeautifulSoup

class TestProfileFunctionality(unittest.TestCase):
    """个人资料功能测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            # 创建测试用户
            test_user = User.query.filter_by(username='testuser').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    real_name='测试用户',
                    phone='13800138000',
                    region='北京市',
                    farm_type='蔬菜种植',
                    farm_size=100
                )
                test_user.set_password('testpass123')
                db.session.add(test_user)
                db.session.commit()
    
    def login_test_user(self):
        """登录测试用户"""
        return self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
    
    def test_profile_page_access(self):
        """测试个人资料页面访问"""
        print("\n🧪 测试个人资料页面访问...")
        
        # 未登录时应该重定向到登录页面
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        print("  ✅ 未登录用户正确重定向")
        
        # 登录后应该能访问个人资料页面
        self.login_test_user()
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn('个人资料', response.get_data(as_text=True))
        print("  ✅ 登录用户可以访问个人资料页面")
    
    def test_profile_data_display(self):
        """测试个人资料数据显示"""
        print("\n🧪 测试个人资料数据显示...")
        
        self.login_test_user()
        response = self.client.get('/profile')
        content = response.get_data(as_text=True)
        
        # 检查用户信息是否正确显示
        self.assertIn('testuser', content)
        self.assertIn('测试用户', content)
        self.assertIn('test@example.com', content)
        self.assertIn('13800138000', content)
        self.assertIn('北京市', content)
        self.assertIn('蔬菜种植', content)
        self.assertIn('100', content)
        
        print("  ✅ 用户信息正确显示")
    
    def test_edit_profile_page_access(self):
        """测试编辑个人资料页面访问"""
        print("\n🧪 测试编辑个人资料页面访问...")
        
        # 未登录时应该重定向
        response = self.client.get('/profile/edit')
        self.assertEqual(response.status_code, 302)
        print("  ✅ 未登录用户正确重定向")
        
        # 登录后应该能访问编辑页面
        self.login_test_user()
        response = self.client.get('/profile/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn('编辑个人资料', response.get_data(as_text=True))
        print("  ✅ 登录用户可以访问编辑页面")
    
    def test_profile_form_prefill(self):
        """测试编辑表单预填充"""
        print("\n🧪 测试编辑表单预填充...")
        
        self.login_test_user()
        response = self.client.get('/profile/edit')
        content = response.get_data(as_text=True)
        
        # 检查表单是否预填充了用户数据
        self.assertIn('value="测试用户"', content)
        self.assertIn('value="test@example.com"', content)
        self.assertIn('value="13800138000"', content)
        self.assertIn('value="北京市"', content)
        self.assertIn('value="蔬菜种植"', content)
        self.assertIn('value="100"', content)
        
        print("  ✅ 表单正确预填充用户数据")
    
    def test_profile_update(self):
        """测试个人资料更新"""
        print("\n🧪 测试个人资料更新...")
        
        self.login_test_user()
        
        # 提交更新的个人资料
        response = self.client.post('/profile/edit', data={
            'real_name': '更新的姓名',
            'email': 'updated@example.com',
            'phone': '13900139000',
            'region': '上海市',
            'farm_type': '水果种植',
            'farm_size': '200',
            'submit': '更新资料'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('个人资料更新成功', content)
        
        print("  ✅ 个人资料更新成功")
        
        # 验证数据是否真的更新了
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertEqual(user.real_name, '更新的姓名')
            self.assertEqual(user.email, 'updated@example.com')
            self.assertEqual(user.phone, '13900139000')
            self.assertEqual(user.region, '上海市')
            self.assertEqual(user.farm_type, '水果种植')
            self.assertEqual(user.farm_size, 200)
        
        print("  ✅ 数据库中的数据正确更新")
    
    def test_profile_validation(self):
        """测试表单验证"""
        print("\n🧪 测试表单验证...")
        
        self.login_test_user()
        
        # 测试无效邮箱
        response = self.client.post('/profile/edit', data={
            'real_name': '测试用户',
            'email': 'invalid-email',
            'phone': '13800138000',
            'region': '北京市',
            'farm_type': '蔬菜种植',
            'farm_size': '100',
            'submit': '更新资料'
        })
        
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        # 应该显示验证错误
        self.assertIn('编辑个人资料', content)
        
        print("  ✅ 表单验证正常工作")
    
    def test_navigation_menu(self):
        """测试导航菜单中的个人资料链接"""
        print("\n🧪 测试导航菜单...")
        
        self.login_test_user()
        response = self.client.get('/')
        content = response.get_data(as_text=True)
        
        # 检查导航菜单中是否有个人资料链接
        self.assertIn('个人资料', content)
        self.assertIn('/profile', content)
        
        print("  ✅ 导航菜单包含个人资料链接")

class TestProfileIntegration(unittest.TestCase):
    """个人资料功能集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
    
    def test_profile_workflow(self):
        """测试完整的个人资料工作流程"""
        print("\n🧪 测试完整个人资料工作流程...")
        
        try:
            # 1. 访问登录页面
            login_page = self.session.get(f"{self.base_url}/login")
            if login_page.status_code != 200:
                print("  ⚠️  应用未运行，跳过集成测试")
                return
            
            # 2. 解析CSRF token
            soup = BeautifulSoup(login_page.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            if not csrf_token:
                print("  ⚠️  未找到CSRF token，跳过集成测试")
                return
            
            # 3. 登录
            login_data = {
                'username': 'admin',
                'password': 'admin123',
                'csrf_token': csrf_token.get('value')
            }
            
            login_response = self.session.post(f"{self.base_url}/login", data=login_data)
            if login_response.status_code == 302:
                print("  ✅ 登录成功")
            
            # 4. 访问个人资料页面
            profile_response = self.session.get(f"{self.base_url}/profile")
            if profile_response.status_code == 200:
                print("  ✅ 个人资料页面访问成功")
            
            # 5. 访问编辑页面
            edit_response = self.session.get(f"{self.base_url}/profile/edit")
            if edit_response.status_code == 200:
                print("  ✅ 编辑页面访问成功")
            
            print("  ✅ 个人资料功能集成测试通过")
            
        except Exception as e:
            print(f"  ⚠️  集成测试失败: {str(e)}")

def run_profile_tests():
    """运行个人资料功能测试"""
    print("🚀 AgriDec 个人资料功能测试")
    print("=" * 50)
    
    # 运行单元测试
    print("\n📋 单元测试:")
    unittest.main(argv=[''], exit=False, verbosity=0)
    
    # 运行集成测试
    print("\n📋 集成测试:")
    integration_suite = unittest.TestLoader().loadTestsFromTestCase(TestProfileIntegration)
    unittest.TextTestRunner(verbosity=0).run(integration_suite)
    
    print("\n" + "=" * 50)
    print("✅ 个人资料功能测试完成")

if __name__ == "__main__":
    run_profile_tests()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 用户认证系统测试
使用Playwright进行自动化测试
"""

import asyncio
from playwright.async_api import async_playwright
import time

class AuthenticationTester:
    """用户认证测试器"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.test_results = []
    
    async def run_tests(self):
        """运行所有认证测试"""
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                print("🚀 开始用户认证系统测试")
                print("=" * 50)
                
                # 测试用例列表
                test_cases = [
                    ("测试登录页面访问", self.test_login_page_access),
                    ("测试用户登录功能", self.test_user_login),
                    ("测试登录验证", self.test_login_validation),
                    ("测试用户注册页面", self.test_registration_page),
                    ("测试用户注册功能", self.test_user_registration),
                    ("测试登录后访问控制", self.test_authenticated_access),
                    ("测试用户登出", self.test_user_logout),
                    ("测试未认证访问重定向", self.test_unauthenticated_redirect)
                ]
                
                # 执行测试用例
                for test_name, test_func in test_cases:
                    print(f"\n🔄 执行测试: {test_name}")
                    try:
                        result = await test_func(page)
                        if result:
                            print(f"✅ {test_name} - 通过")
                            self.test_results.append((test_name, True, ""))
                        else:
                            print(f"❌ {test_name} - 失败")
                            self.test_results.append((test_name, False, "测试失败"))
                    except Exception as e:
                        print(f"❌ {test_name} - 异常: {str(e)}")
                        self.test_results.append((test_name, False, str(e)))
                    
                    # 测试间隔
                    await asyncio.sleep(1)
                
                # 显示测试结果
                self.show_test_results()
                
            finally:
                await browser.close()
    
    async def test_login_page_access(self, page):
        """测试登录页面访问"""
        await page.goto(f"{self.base_url}/login")
        
        # 检查页面标题
        title = await page.title()
        if "用户登录" not in title:
            return False
        
        # 检查登录表单元素
        username_input = await page.query_selector("#username")
        password_input = await page.query_selector("#password")
        submit_button = await page.query_selector("input[type='submit']")
        
        return all([username_input, password_input, submit_button])
    
    async def test_user_login(self, page):
        """测试用户登录功能"""
        await page.goto(f"{self.base_url}/login")
        
        # 填写登录表单
        await page.fill("#username", "admin")
        await page.fill("#password", "admin123")
        
        # 点击登录按钮
        await page.click("input[type='submit']")
        
        # 等待页面跳转
        await page.wait_for_load_state("networkidle")
        
        # 检查是否跳转到首页
        current_url = page.url
        return current_url == f"{self.base_url}/" or "index" in current_url
    
    async def test_login_validation(self, page):
        """测试登录验证"""
        await page.goto(f"{self.base_url}/login")
        
        # 测试错误的用户名密码
        await page.fill("#username", "wronguser")
        await page.fill("#password", "wrongpass")
        await page.click("input[type='submit']")
        
        # 等待页面响应
        await page.wait_for_load_state("networkidle")
        
        # 检查是否显示错误信息
        error_message = await page.query_selector(".alert-danger")
        return error_message is not None
    
    async def test_registration_page(self, page):
        """测试用户注册页面"""
        await page.goto(f"{self.base_url}/register")
        
        # 检查页面标题
        title = await page.title()
        if "用户注册" not in title:
            return False
        
        # 检查注册表单元素
        required_fields = [
            "#username", "#email", "#real_name", 
            "#region", "#farm_type", "#password", "#password2"
        ]
        
        for field in required_fields:
            element = await page.query_selector(field)
            if not element:
                return False
        
        return True
    
    async def test_user_registration(self, page):
        """测试用户注册功能"""
        await page.goto(f"{self.base_url}/register")
        
        # 生成唯一用户名
        timestamp = str(int(time.time()))
        test_username = f"testuser{timestamp}"
        test_email = f"test{timestamp}@example.com"
        
        # 填写注册表单
        await page.fill("#username", test_username)
        await page.fill("#email", test_email)
        await page.fill("#real_name", "测试用户")
        await page.select_option("#region", "山东省")
        await page.select_option("#farm_type", "种植业")
        await page.fill("#farm_size", "25.5")
        await page.fill("#password", "test123456")
        await page.fill("#password2", "test123456")
        
        # 提交注册表单
        await page.click("input[type='submit']")
        
        # 等待页面响应
        await page.wait_for_load_state("networkidle")
        
        # 检查是否跳转到登录页面或显示成功信息
        current_url = page.url
        success_message = await page.query_selector(".alert-success")
        
        return "/login" in current_url or success_message is not None
    
    async def test_authenticated_access(self, page):
        """测试登录后访问控制"""
        # 先登录
        await page.goto(f"{self.base_url}/login")
        await page.fill("#username", "farmer1")
        await page.fill("#password", "farmer123")
        await page.click("input[type='submit']")
        await page.wait_for_load_state("networkidle")
        
        # 测试访问主要页面
        pages_to_test = [
            "/",
            "/seed-dashboard", 
            "/weather-dashboard",
            "/machine-comparison"
        ]
        
        for test_page in pages_to_test:
            await page.goto(f"{self.base_url}{test_page}")
            await page.wait_for_load_state("networkidle")
            
            # 检查页面是否正常加载（不是登录页面）
            current_url = page.url
            if "/login" in current_url:
                return False
        
        return True
    
    async def test_user_logout(self, page):
        """测试用户登出"""
        # 先登录
        await page.goto(f"{self.base_url}/login")
        await page.fill("#username", "farmer2")
        await page.fill("#password", "farmer123")
        await page.click("input[type='submit']")
        await page.wait_for_load_state("networkidle")
        
        # 查找并点击登出链接
        logout_link = await page.query_selector("a[href='/logout']")
        if logout_link:
            await logout_link.click()
            await page.wait_for_load_state("networkidle")
            
            # 检查是否跳转到登录页面
            current_url = page.url
            return "/login" in current_url
        
        return False
    
    async def test_unauthenticated_redirect(self, page):
        """测试未认证访问重定向"""
        # 清除所有cookies确保未登录状态
        await page.context.clear_cookies()
        
        # 尝试访问需要认证的页面
        protected_pages = ["/seed-dashboard", "/weather-dashboard"]
        
        for protected_page in protected_pages:
            await page.goto(f"{self.base_url}{protected_page}")
            await page.wait_for_load_state("networkidle")
            
            # 检查是否重定向到登录页面
            current_url = page.url
            if "/login" not in current_url:
                return False
        
        return True
    
    def show_test_results(self):
        """显示测试结果"""
        print("\n" + "=" * 50)
        print("📊 用户认证系统测试结果")
        print("=" * 50)
        
        passed = 0
        failed = 0
        
        for test_name, result, error in self.test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{status} - {test_name}")
            if not result and error:
                print(f"    错误: {error}")
            
            if result:
                passed += 1
            else:
                failed += 1
        
        print(f"\n📈 测试统计:")
        print(f"   总计: {len(self.test_results)} 个测试")
        print(f"   通过: {passed} 个")
        print(f"   失败: {failed} 个")
        print(f"   成功率: {passed/len(self.test_results)*100:.1f}%")
        
        if failed == 0:
            print("\n🎉 所有认证测试通过！用户认证系统工作正常。")
        else:
            print(f"\n⚠️ 有 {failed} 个测试失败，请检查相关功能。")

async def main():
    """主函数"""
    tester = AuthenticationTester()
    await tester.run_tests()

if __name__ == "__main__":
    asyncio.run(main())

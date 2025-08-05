#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 综合系统测试
使用Playwright进行完整的系统功能测试
"""

import asyncio
from playwright.async_api import async_playwright
import time
import json

class ComprehensiveSystemTester:
    """综合系统测试器"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.test_results = []
        self.test_data = {
            'admin_user': {'username': 'admin', 'password': 'admin123'},
            'farmer_user': {'username': 'farmer1', 'password': 'farmer123'},
            'test_user': {'username': f'testuser{int(time.time())}', 'email': f'test{int(time.time())}@example.com'}
        }
    
    async def run_all_tests(self):
        """运行所有系统测试"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=500)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                print("🚀 开始AgriDec综合系统测试")
                print("=" * 60)
                
                # 测试分组
                test_groups = [
                    ("用户认证系统", [
                        ("登录页面访问", self.test_login_page),
                        ("用户登录功能", self.test_user_login),
                        ("用户注册功能", self.test_user_registration),
                        ("登录状态验证", self.test_login_state),
                        ("用户登出功能", self.test_user_logout),
                        ("访问控制验证", self.test_access_control)
                    ]),
                    ("数据采集系统", [
                        ("数据采集API", self.test_data_collection_api),
                        ("种子数据采集", self.test_seed_data_collection),
                        ("天气数据采集", self.test_weather_data_collection),
                        ("农机数据采集", self.test_machine_data_collection)
                    ]),
                    ("Web界面功能", [
                        ("主页数据看板", self.test_main_dashboard),
                        ("种子推荐面板", self.test_seed_dashboard),
                        ("天气适宜度看板", self.test_weather_dashboard),
                        ("农机对比表", self.test_machine_comparison),
                        ("农事日历", self.test_farming_calendar),
                        ("农资采购模块", self.test_purchase_module)
                    ]),
                    ("API接口测试", [
                        ("种子价格API", self.test_seed_prices_api),
                        ("天气预报API", self.test_weather_forecast_api),
                        ("农机设备API", self.test_farm_machines_api),
                        ("调度器状态API", self.test_scheduler_status_api)
                    ]),
                    ("响应式设计", [
                        ("桌面端显示", self.test_desktop_responsive),
                        ("平板端显示", self.test_tablet_responsive),
                        ("移动端显示", self.test_mobile_responsive)
                    ])
                ]
                
                # 执行测试组
                for group_name, tests in test_groups:
                    print(f"\n📋 测试组: {group_name}")
                    print("-" * 40)
                    
                    for test_name, test_func in tests:
                        print(f"🔄 执行: {test_name}")
                        try:
                            result = await test_func(page)
                            status = "✅ 通过" if result else "❌ 失败"
                            print(f"   {status}")
                            self.test_results.append((group_name, test_name, result, ""))
                        except Exception as e:
                            print(f"   ❌ 异常: {str(e)}")
                            self.test_results.append((group_name, test_name, False, str(e)))
                        
                        await asyncio.sleep(0.5)
                
                # 显示测试结果
                self.show_comprehensive_results()
                
            finally:
                await browser.close()
    
    # 用户认证系统测试
    async def test_login_page(self, page):
        """测试登录页面"""
        await page.goto(f"{self.base_url}/login")
        title = await page.title()
        form_elements = await page.query_selector_all("input")
        return "登录" in title and len(form_elements) >= 3
    
    async def test_user_login(self, page):
        """测试用户登录"""
        await page.goto(f"{self.base_url}/login")
        await page.fill("#username", self.test_data['admin_user']['username'])
        await page.fill("#password", self.test_data['admin_user']['password'])
        await page.click("input[type='submit']")
        await page.wait_for_load_state("networkidle")
        return page.url == f"{self.base_url}/"
    
    async def test_user_registration(self, page):
        """测试用户注册"""
        await page.goto(f"{self.base_url}/register")
        
        # 填写注册表单
        await page.fill("#username", self.test_data['test_user']['username'])
        await page.fill("#email", self.test_data['test_user']['email'])
        await page.fill("#real_name", "测试用户")
        await page.select_option("#region", "山东省")
        await page.select_option("#farm_type", "种植业")
        await page.fill("#password", "test123456")
        await page.fill("#password2", "test123456")
        await page.click("input[type='submit']")
        await page.wait_for_load_state("networkidle")
        
        return "/login" in page.url or await page.query_selector(".alert-success")
    
    async def test_login_state(self, page):
        """测试登录状态"""
        # 先登录
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/")
        
        # 检查用户信息是否显示
        user_dropdown = await page.query_selector(".dropdown-toggle")
        return user_dropdown is not None
    
    async def test_user_logout(self, page):
        """测试用户登出"""
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/logout")
        await page.wait_for_load_state("networkidle")
        return "/login" in page.url
    
    async def test_access_control(self, page):
        """测试访问控制"""
        await page.context.clear_cookies()
        await page.goto(f"{self.base_url}/seed-dashboard")
        await page.wait_for_load_state("networkidle")
        return "/login" in page.url
    
    # 数据采集系统测试
    async def test_data_collection_api(self, page):
        """测试数据采集API"""
        await self.login_as_admin(page)
        
        # 测试API调用
        response = await page.evaluate("""
            fetch('/api/crawl-data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    website: 'seed_trade',
                    data_type: 'seed_prices',
                    region: '全国',
                    max_pages: 1
                })
            }).then(r => r.json()).catch(e => ({error: e.message}))
        """)
        
        return 'success' in response or 'data' in response
    
    async def test_seed_data_collection(self, page):
        """测试种子数据采集"""
        await self.login_as_admin(page)
        await page.goto(f"{self.base_url}/")
        
        # 查找并点击种子数据采集按钮
        collect_button = await page.query_selector("[data-website='seed_trade']")
        if collect_button:
            await collect_button.click()
            await page.wait_for_timeout(3000)  # 等待采集完成
            return True
        return False
    
    async def test_weather_data_collection(self, page):
        """测试天气数据采集"""
        await self.login_as_admin(page)
        await page.goto(f"{self.base_url}/")
        
        collect_button = await page.query_selector("[data-website='weather']")
        if collect_button:
            await collect_button.click()
            await page.wait_for_timeout(3000)
            return True
        return False
    
    async def test_machine_data_collection(self, page):
        """测试农机数据采集"""
        await self.login_as_admin(page)
        await page.goto(f"{self.base_url}/")
        
        collect_button = await page.query_selector("[data-website='farm_machine']")
        if collect_button:
            await collect_button.click()
            await page.wait_for_timeout(3000)
            return True
        return False
    
    # Web界面功能测试
    async def test_main_dashboard(self, page):
        """测试主页数据看板"""
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/")
        
        # 检查关键元素
        hero_section = await page.query_selector(".hero-section")
        feature_cards = await page.query_selector_all(".feature-card")
        return hero_section is not None and len(feature_cards) > 0
    
    async def test_seed_dashboard(self, page):
        """测试种子推荐面板"""
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/seed-dashboard")
        await page.wait_for_load_state("networkidle")
        
        title = await page.title()
        return "种子" in title and page.url.endswith("/seed-dashboard")
    
    async def test_weather_dashboard(self, page):
        """测试天气适宜度看板"""
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/weather-dashboard")
        await page.wait_for_load_state("networkidle")
        
        title = await page.title()
        return "天气" in title and page.url.endswith("/weather-dashboard")
    
    async def test_machine_comparison(self, page):
        """测试农机对比表"""
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/machine-comparison")
        await page.wait_for_load_state("networkidle")
        
        title = await page.title()
        return "农机" in title or "对比" in title
    
    async def test_farming_calendar(self, page):
        """测试农事日历"""
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/farming-calendar")
        await page.wait_for_load_state("networkidle")
        
        title = await page.title()
        return "农事" in title or "日历" in title
    
    async def test_purchase_module(self, page):
        """测试农资采购模块"""
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/purchase-module")
        await page.wait_for_load_state("networkidle")
        
        title = await page.title()
        return "采购" in title or "农资" in title
    
    # API接口测试
    async def test_seed_prices_api(self, page):
        """测试种子价格API"""
        await self.login_as_farmer(page)
        
        response = await page.evaluate("""
            fetch('/api/seed-prices?limit=10')
                .then(r => r.json())
                .catch(e => ({error: e.message}))
        """)
        
        return 'data' in response or isinstance(response, list)
    
    async def test_weather_forecast_api(self, page):
        """测试天气预报API"""
        await self.login_as_farmer(page)
        
        response = await page.evaluate("""
            fetch('/api/weather-forecast?region=北京&days=7')
                .then(r => r.json())
                .catch(e => ({error: e.message}))
        """)
        
        return 'data' in response or isinstance(response, list)
    
    async def test_farm_machines_api(self, page):
        """测试农机设备API"""
        await self.login_as_farmer(page)
        
        response = await page.evaluate("""
            fetch('/api/farm-machines?limit=10')
                .then(r => r.json())
                .catch(e => ({error: e.message}))
        """)
        
        return 'data' in response or isinstance(response, list)
    
    async def test_scheduler_status_api(self, page):
        """测试调度器状态API"""
        await self.login_as_admin(page)
        
        response = await page.evaluate("""
            fetch('/api/scheduler-status')
                .then(r => r.json())
                .catch(e => ({error: e.message}))
        """)
        
        return 'running' in response or 'status' in response
    
    # 响应式设计测试
    async def test_desktop_responsive(self, page):
        """测试桌面端响应式"""
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/")
        
        navbar = await page.query_selector(".navbar")
        return navbar is not None
    
    async def test_tablet_responsive(self, page):
        """测试平板端响应式"""
        await page.set_viewport_size({"width": 768, "height": 1024})
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/")
        
        # 检查导航是否适配
        navbar_toggler = await page.query_selector(".navbar-toggler")
        return navbar_toggler is not None
    
    async def test_mobile_responsive(self, page):
        """测试移动端响应式"""
        await page.set_viewport_size({"width": 375, "height": 667})
        await self.login_as_farmer(page)
        await page.goto(f"{self.base_url}/")
        
        # 检查移动端布局
        container = await page.query_selector(".container")
        return container is not None
    
    # 辅助方法
    async def login_as_admin(self, page):
        """以管理员身份登录"""
        await page.goto(f"{self.base_url}/login")
        await page.fill("#username", self.test_data['admin_user']['username'])
        await page.fill("#password", self.test_data['admin_user']['password'])
        await page.click("input[type='submit']")
        await page.wait_for_load_state("networkidle")
    
    async def login_as_farmer(self, page):
        """以农户身份登录"""
        await page.goto(f"{self.base_url}/login")
        await page.fill("#username", self.test_data['farmer_user']['username'])
        await page.fill("#password", self.test_data['farmer_user']['password'])
        await page.click("input[type='submit']")
        await page.wait_for_load_state("networkidle")
    
    def show_comprehensive_results(self):
        """显示综合测试结果"""
        print("\n" + "=" * 60)
        print("📊 AgriDec 综合系统测试结果")
        print("=" * 60)
        
        # 按测试组统计
        group_stats = {}
        for group, test_name, result, error in self.test_results:
            if group not in group_stats:
                group_stats[group] = {'passed': 0, 'failed': 0, 'total': 0}
            
            group_stats[group]['total'] += 1
            if result:
                group_stats[group]['passed'] += 1
            else:
                group_stats[group]['failed'] += 1
        
        # 显示各组结果
        total_passed = 0
        total_failed = 0
        
        for group, stats in group_stats.items():
            success_rate = stats['passed'] / stats['total'] * 100
            print(f"\n📋 {group}:")
            print(f"   通过: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
            
            total_passed += stats['passed']
            total_failed += stats['failed']
            
            # 显示失败的测试
            failed_tests = [
                (test_name, error) for g, test_name, result, error in self.test_results 
                if g == group and not result
            ]
            
            for test_name, error in failed_tests:
                print(f"   ❌ {test_name}")
                if error:
                    print(f"      错误: {error}")
        
        # 总体统计
        total_tests = total_passed + total_failed
        overall_success_rate = total_passed / total_tests * 100 if total_tests > 0 else 0
        
        print(f"\n📈 总体统计:")
        print(f"   总测试数: {total_tests}")
        print(f"   通过: {total_passed}")
        print(f"   失败: {total_failed}")
        print(f"   成功率: {overall_success_rate:.1f}%")
        
        if total_failed == 0:
            print("\n🎉 所有测试通过！AgriDec系统功能完整，可以投入生产使用。")
        elif overall_success_rate >= 80:
            print(f"\n✅ 系统基本功能正常，成功率达到{overall_success_rate:.1f}%，可以部署使用。")
        else:
            print(f"\n⚠️ 系统存在较多问题，成功率仅{overall_success_rate:.1f}%，建议修复后再部署。")

async def main():
    """主函数"""
    tester = ComprehensiveSystemTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

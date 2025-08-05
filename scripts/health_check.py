#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 项目健康检查脚本
验证项目结构完整性和功能正常性
"""

import os
import sys
import importlib
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class ProjectHealthChecker:
    """项目健康检查器"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        
    def check_directory_structure(self):
        """检查目录结构"""
        print("📁 检查目录结构...")
        
        required_dirs = [
            'auth', 'data_crawler', 'data_analysis', 'visualization',
            'templates', 'static', 'scripts', 'tests', 'docs',
            'logs', 'backups', 'reports'
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            self.issues.append(f"缺少目录: {', '.join(missing_dirs)}")
            print(f"  ❌ 缺少目录: {', '.join(missing_dirs)}")
        else:
            print("  ✅ 目录结构完整")
        
        return len(missing_dirs) == 0
    
    def check_core_files(self):
        """检查核心文件"""
        print("\n📄 检查核心文件...")
        
        core_files = [
            'app.py', 'start.py', 'database.py', 'scheduler.py',
            'requirements.txt', 'README.md', '.gitignore'
        ]
        
        missing_files = []
        for file_name in core_files:
            if not Path(file_name).exists():
                missing_files.append(file_name)
        
        if missing_files:
            self.issues.append(f"缺少核心文件: {', '.join(missing_files)}")
            print(f"  ❌ 缺少核心文件: {', '.join(missing_files)}")
        else:
            print("  ✅ 核心文件完整")
        
        return len(missing_files) == 0
    
    def check_module_imports(self):
        """检查模块导入"""
        print("\n🔗 检查模块导入...")
        
        modules_to_check = [
            ('auth.models', 'User'),
            ('auth.forms', 'LoginForm'),
            ('data_crawler.crawler_manager', 'CrawlerManager'),
            ('data_analysis.analyzer', 'DataAnalyzer'),
            ('visualization.chart_generator', 'ChartGenerator')
        ]
        
        import_errors = []
        for module_name, class_name in modules_to_check:
            try:
                module = importlib.import_module(module_name)
                getattr(module, class_name)
                print(f"  ✅ {module_name}.{class_name}")
            except ImportError as e:
                import_errors.append(f"{module_name}: {e}")
                print(f"  ❌ {module_name}.{class_name}: {e}")
            except AttributeError as e:
                import_errors.append(f"{module_name}.{class_name}: {e}")
                print(f"  ❌ {module_name}.{class_name}: {e}")
        
        if import_errors:
            self.issues.extend(import_errors)
        
        return len(import_errors) == 0
    
    def check_template_files(self):
        """检查模板文件"""
        print("\n🎨 检查模板文件...")
        
        required_templates = [
            'index.html', 'seed_dashboard.html', 'weather_dashboard.html',
            'machine_comparison.html', 'farming_calendar.html', 'purchase_module.html'
        ]
        
        missing_templates = []
        for template in required_templates:
            template_path = Path('templates') / template
            if not template_path.exists():
                missing_templates.append(template)
        
        if missing_templates:
            self.warnings.append(f"缺少模板文件: {', '.join(missing_templates)}")
            print(f"  ⚠️  缺少模板文件: {', '.join(missing_templates)}")
        else:
            print("  ✅ 模板文件完整")
        
        return len(missing_templates) == 0
    
    def check_static_resources(self):
        """检查静态资源"""
        print("\n🎯 检查静态资源...")
        
        static_dirs = ['css', 'js', 'images']
        missing_static = []
        
        for dir_name in static_dirs:
            static_path = Path('static') / dir_name
            if not static_path.exists():
                missing_static.append(dir_name)
        
        if missing_static:
            self.warnings.append(f"缺少静态资源目录: {', '.join(missing_static)}")
            print(f"  ⚠️  缺少静态资源目录: {', '.join(missing_static)}")
        else:
            print("  ✅ 静态资源目录完整")
        
        return len(missing_static) == 0
    
    def check_documentation(self):
        """检查文档完整性"""
        print("\n📚 检查文档...")
        
        required_docs = [
            'PROJECT_STRUCTURE.md', 'DEPLOYMENT_GUIDE.md', 
            'MAINTENANCE_GUIDE.md'
        ]
        
        missing_docs = []
        for doc in required_docs:
            doc_path = Path('docs') / doc
            if not doc_path.exists():
                missing_docs.append(doc)
        
        if missing_docs:
            self.warnings.append(f"缺少文档: {', '.join(missing_docs)}")
            print(f"  ⚠️  缺少文档: {', '.join(missing_docs)}")
        else:
            print("  ✅ 文档完整")
        
        return len(missing_docs) == 0
    
    def check_temp_directory(self):
        """检查临时目录"""
        print("\n🗂️  检查临时文件...")
        
        temp_dir = Path('temp')
        if temp_dir.exists():
            temp_files = list(temp_dir.iterdir())
            if temp_files:
                print(f"  ℹ️  临时目录包含 {len(temp_files)} 个文件")
                print("     建议定期清理临时文件")
            else:
                print("  ✅ 临时目录为空")
        else:
            print("  ℹ️  无临时目录")
    
    def check_file_permissions(self):
        """检查文件权限"""
        print("\n🔐 检查文件权限...")
        
        writable_dirs = ['logs', 'backups', 'reports', 'instance']
        permission_issues = []
        
        for dir_name in writable_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                if not os.access(dir_path, os.W_OK):
                    permission_issues.append(dir_name)
        
        if permission_issues:
            self.warnings.append(f"目录权限问题: {', '.join(permission_issues)}")
            print(f"  ⚠️  目录权限问题: {', '.join(permission_issues)}")
        else:
            print("  ✅ 文件权限正常")
        
        return len(permission_issues) == 0
    
    def generate_report(self):
        """生成健康检查报告"""
        print("\n" + "=" * 50)
        print("📊 项目健康检查报告")
        print("=" * 50)
        
        if not self.issues and not self.warnings:
            print("🎉 项目状态优秀！")
            print("✅ 所有检查项目都通过")
            return True
        
        if self.issues:
            print("❌ 发现严重问题:")
            for issue in self.issues:
                print(f"   • {issue}")
        
        if self.warnings:
            print("\n⚠️  发现警告:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        print(f"\n📈 检查结果:")
        print(f"   严重问题: {len(self.issues)}")
        print(f"   警告: {len(self.warnings)}")
        
        if self.issues:
            print("\n🔧 建议:")
            print("   1. 修复所有严重问题")
            print("   2. 运行 python scripts/organize_project_structure.py")
            print("   3. 重新运行健康检查")
        
        return len(self.issues) == 0
    
    def run_full_check(self):
        """运行完整健康检查"""
        print("🔍 AgriDec 项目健康检查")
        print("=" * 50)
        
        # 执行所有检查
        self.check_directory_structure()
        self.check_core_files()
        self.check_module_imports()
        self.check_template_files()
        self.check_static_resources()
        self.check_documentation()
        self.check_temp_directory()
        self.check_file_permissions()
        
        # 生成报告
        return self.generate_report()

def main():
    """主函数"""
    checker = ProjectHealthChecker()
    is_healthy = checker.run_full_check()
    
    sys.exit(0 if is_healthy else 1)

if __name__ == "__main__":
    main()

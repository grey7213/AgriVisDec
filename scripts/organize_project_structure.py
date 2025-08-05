#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 项目结构整理脚本
按照规范整理项目目录结构，清理临时文件，确保项目组织良好
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class ProjectOrganizer:
    """项目结构整理器"""
    
    def __init__(self):
        self.root_dir = Path('.')
        self.cleanup_log = []
        
    def analyze_current_structure(self):
        """分析当前项目结构"""
        print("📊 分析当前项目结构...")
        
        structure = {
            'core_files': [],
            'temp_files': [],
            'test_files': [],
            'docs': [],
            'configs': [],
            'misplaced_files': []
        }
        
        # 定义文件分类规则
        temp_patterns = ['test_', 'verify_', 'make_', 'run_demo', 'independence_report']
        test_patterns = ['test_', '_test']
        doc_patterns = ['.md', '.txt', '.rst']
        config_patterns = ['config', '.env', 'requirements']
        
        for file_path in self.root_dir.iterdir():
            if file_path.is_file():
                name = file_path.name.lower()
                
                if any(pattern in name for pattern in temp_patterns):
                    structure['temp_files'].append(file_path)
                elif any(pattern in name for pattern in test_patterns):
                    structure['test_files'].append(file_path)
                elif any(name.endswith(pattern) for pattern in doc_patterns):
                    structure['docs'].append(file_path)
                elif any(pattern in name for pattern in config_patterns):
                    structure['configs'].append(file_path)
                elif name in ['app.py', 'start.py', 'scheduler.py', 'database.py']:
                    structure['core_files'].append(file_path)
                else:
                    structure['misplaced_files'].append(file_path)
        
        return structure
    
    def create_directory_structure(self):
        """创建标准目录结构"""
        print("📁 创建标准目录结构...")
        
        directories = [
            'auth',
            'data_crawler', 
            'data_analysis',
            'visualization',
            'templates/auth',
            'templates/errors',
            'static/css',
            'static/js', 
            'static/images',
            'scripts',
            'tests',
            'docs',
            'config',
            'logs',
            'backups',
            'reports',
            'utils'
        ]
        
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        print("  ✅ 目录结构创建完成")
    
    def move_temp_files(self, temp_files):
        """移动临时文件到临时目录"""
        if not temp_files:
            return
            
        print("🗂️  整理临时文件...")
        temp_dir = Path('temp')
        temp_dir.mkdir(exist_ok=True)
        
        for file_path in temp_files:
            try:
                dest = temp_dir / file_path.name
                shutil.move(str(file_path), str(dest))
                self.cleanup_log.append(f"移动临时文件: {file_path.name} -> temp/")
                print(f"  📦 {file_path.name} -> temp/")
            except Exception as e:
                print(f"  ❌ 移动失败 {file_path.name}: {e}")
    
    def move_test_files(self, test_files):
        """移动测试文件到tests目录"""
        if not test_files:
            return
            
        print("🧪 整理测试文件...")
        
        for file_path in test_files:
            try:
                dest = Path('tests') / file_path.name
                if not dest.exists():
                    shutil.move(str(file_path), str(dest))
                    self.cleanup_log.append(f"移动测试文件: {file_path.name} -> tests/")
                    print(f"  🧪 {file_path.name} -> tests/")
            except Exception as e:
                print(f"  ❌ 移动失败 {file_path.name}: {e}")
    
    def organize_docs(self, docs):
        """整理文档文件"""
        if not docs:
            return
            
        print("📚 整理文档文件...")
        
        # 保留在根目录的重要文档
        keep_in_root = ['README.md', 'requirements.txt']
        
        for file_path in docs:
            if file_path.name in keep_in_root:
                print(f"  📋 保留在根目录: {file_path.name}")
                continue
                
            try:
                dest = Path('docs') / file_path.name
                if not dest.exists():
                    shutil.move(str(file_path), str(dest))
                    self.cleanup_log.append(f"移动文档: {file_path.name} -> docs/")
                    print(f"  📚 {file_path.name} -> docs/")
            except Exception as e:
                print(f"  ❌ 移动失败 {file_path.name}: {e}")
    
    def clean_pycache(self):
        """清理__pycache__目录"""
        print("🧹 清理__pycache__目录...")
        
        for pycache_dir in self.root_dir.rglob('__pycache__'):
            try:
                shutil.rmtree(pycache_dir)
                self.cleanup_log.append(f"删除缓存目录: {pycache_dir}")
                print(f"  🗑️  删除: {pycache_dir}")
            except Exception as e:
                print(f"  ❌ 删除失败 {pycache_dir}: {e}")
    
    def clean_duplicate_configs(self):
        """清理重复的配置文件"""
        print("⚙️  清理重复配置...")
        
        # 检查是否有重复的config文件
        config_py = Path('config.py')
        config_dir = Path('config/config.py')
        
        if config_py.exists() and config_dir.exists():
            # 比较文件内容，保留更完整的版本
            try:
                with open(config_py, 'r', encoding='utf-8') as f:
                    content1 = f.read()
                with open(config_dir, 'r', encoding='utf-8') as f:
                    content2 = f.read()
                
                if len(content1) > len(content2):
                    config_dir.unlink()
                    print("  🗑️  删除重复配置: config/config.py")
                else:
                    config_py.unlink()
                    print("  🗑️  删除重复配置: config.py")
                    
            except Exception as e:
                print(f"  ⚠️  配置文件处理警告: {e}")
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        print("📝 创建.gitignore文件...")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite3
instance/

# Logs
logs/*.log
*.log

# Temporary files
temp/
*.tmp
*.bak

# OS
.DS_Store
Thumbs.db

# Project specific
backups/*.sql
reports/*.json
independence_report.json
migration_verification_report_*.json

# Environment variables
.env
.env.local
.env.production
"""
        
        gitignore_path = Path('.gitignore')
        if not gitignore_path.exists():
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("  ✅ .gitignore 文件已创建")
        else:
            print("  ℹ️  .gitignore 文件已存在")
    
    def generate_cleanup_report(self):
        """生成清理报告"""
        print("📋 生成清理报告...")
        
        report = {
            'cleanup_time': datetime.now().isoformat(),
            'actions_performed': self.cleanup_log,
            'final_structure': self._get_directory_tree()
        }
        
        report_path = Path('reports/project_cleanup_report.json')
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ 清理报告已保存: {report_path}")
    
    def _get_directory_tree(self):
        """获取目录树结构"""
        tree = {}
        for item in self.root_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                tree[item.name] = len(list(item.iterdir()))
        return tree
    
    def organize(self):
        """执行完整的项目整理"""
        print("🚀 开始项目结构整理")
        print("=" * 50)
        
        # 分析当前结构
        structure = self.analyze_current_structure()
        
        # 创建标准目录结构
        self.create_directory_structure()
        
        # 移动文件到合适位置
        self.move_temp_files(structure['temp_files'])
        self.move_test_files(structure['test_files'])
        self.organize_docs(structure['docs'])
        
        # 清理工作
        self.clean_pycache()
        self.clean_duplicate_configs()
        
        # 创建项目文件
        self.create_gitignore()
        
        # 生成报告
        self.generate_cleanup_report()
        
        print("\n" + "=" * 50)
        print("✅ 项目结构整理完成！")
        print(f"📊 执行了 {len(self.cleanup_log)} 项清理操作")
        print("📁 项目现在具有清晰的模块化结构")
        print("📋 详细报告: reports/project_cleanup_report.json")

def main():
    """主函数"""
    organizer = ProjectOrganizer()
    organizer.organize()

if __name__ == "__main__":
    main()

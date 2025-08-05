#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgriDec 项目结构优化脚本
清理冗余文件，重新组织项目结构，提供替代可视化方案
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class ProjectStructureOptimizer:
    """项目结构优化器"""
    
    def __init__(self):
        self.root_dir = Path('.')
        self.cleanup_log = []
        self.backup_dir = Path('backups/structure_backup')
        
    def analyze_current_issues(self):
        """分析当前项目结构问题"""
        print("🔍 分析项目结构问题...")
        
        issues = {
            'redundant_docs': [],
            'temp_files': [],
            'misplaced_configs': [],
            'duplicate_files': [],
            'large_files': []
        }
        
        # 检查冗余文档
        doc_patterns = [
            'CHINA_MAP_FIX_SUMMARY.md',
            'FIXES_COMPLETION_SUMMARY.md', 
            'MULTI_DATABASE_GUIDE.md',
            'NAN_FIX_COMPLETION_SUMMARY.md',
            'PROJECT_STATUS.md',
            'SOLUTION_SUMMARY.md',
            'TASK_COMPLETION_SUMMARY.md'
        ]
        
        for pattern in doc_patterns:
            if (self.root_dir / pattern).exists():
                issues['redundant_docs'].append(pattern)
        
        # 检查临时文件
        temp_dir = self.root_dir / 'temp'
        if temp_dir.exists():
            for file in temp_dir.iterdir():
                if file.is_file():
                    issues['temp_files'].append(str(file))
        
        # 检查配置文件
        config_files = ['config.py']
        for config_file in config_files:
            if (self.root_dir / config_file).exists():
                issues['misplaced_configs'].append(config_file)
        
        # 检查__pycache__目录
        for pycache in self.root_dir.rglob('__pycache__'):
            issues['temp_files'].append(str(pycache))
        
        return issues
    
    def create_backup(self):
        """创建备份"""
        print("💾 创建项目备份...")
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 备份重要文件
        important_files = [
            'app.py', 'database.py', 'scheduler.py', 'start.py',
            'requirements.txt', 'README.md'
        ]
        
        backup_subdir = self.backup_dir / f'backup_{timestamp}'
        backup_subdir.mkdir(exist_ok=True)
        
        for file_name in important_files:
            src = self.root_dir / file_name
            if src.exists():
                dst = backup_subdir / file_name
                shutil.copy2(src, dst)
                self.cleanup_log.append(f"备份文件: {file_name}")
        
        print(f"  ✅ 备份完成: {backup_subdir}")
    
    def clean_redundant_docs(self, redundant_docs):
        """清理冗余文档"""
        print("📄 清理冗余文档...")
        
        # 创建文档归档目录
        archive_dir = Path('docs/archive')
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        for doc_file in redundant_docs:
            src = self.root_dir / doc_file
            if src.exists():
                dst = archive_dir / doc_file
                shutil.move(str(src), str(dst))
                self.cleanup_log.append(f"归档文档: {doc_file} -> docs/archive/")
                print(f"  ✅ 归档: {doc_file}")
    
    def clean_temp_files(self, temp_files):
        """清理临时文件"""
        print("🗑️ 清理临时文件...")
        
        for temp_file in temp_files:
            temp_path = Path(temp_file)
            if temp_path.exists():
                if temp_path.is_dir():
                    shutil.rmtree(temp_path)
                    self.cleanup_log.append(f"删除目录: {temp_file}")
                else:
                    temp_path.unlink()
                    self.cleanup_log.append(f"删除文件: {temp_file}")
                print(f"  ✅ 删除: {temp_file}")
    
    def reorganize_configs(self):
        """重新组织配置文件"""
        print("⚙️ 重新组织配置文件...")
        
        config_dir = Path('config')
        config_dir.mkdir(exist_ok=True)
        
        # 移动配置文件到config目录
        if (self.root_dir / 'config.py').exists():
            shutil.move('config.py', 'config/app_config.py')
            self.cleanup_log.append("移动: config.py -> config/app_config.py")
            print("  ✅ 移动配置文件到config目录")
    
    def create_optimized_structure(self):
        """创建优化的目录结构"""
        print("📁 创建优化的目录结构...")
        
        # 确保核心目录存在
        core_dirs = [
            'auth', 'data_crawler', 'data_analysis', 'visualization',
            'templates/auth', 'templates/admin', 'templates/errors',
            'static/css', 'static/js', 'static/images',
            'scripts', 'tests', 'docs', 'config', 'logs', 'backups',
            'utils', 'api'
        ]
        
        for dir_path in core_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        print("  ✅ 核心目录结构创建完成")
    
    def create_alternative_visualizations(self):
        """创建替代可视化方案"""
        print("📊 创建替代可视化方案...")
        
        # 创建替代可视化配置
        alt_viz_config = {
            "alternative_charts": {
                "regional_bar": {
                    "name": "地区柱状图",
                    "description": "使用柱状图展示各地区农业数据",
                    "chart_type": "bar",
                    "suitable_for": ["农业产值对比", "种植面积对比", "产量对比"]
                },
                "regional_pie": {
                    "name": "地区饼图", 
                    "description": "使用饼图展示各地区数据占比",
                    "chart_type": "pie",
                    "suitable_for": ["产值占比", "面积占比", "品种分布"]
                },
                "regional_line": {
                    "name": "地区趋势图",
                    "description": "使用折线图展示各地区数据趋势",
                    "chart_type": "line", 
                    "suitable_for": ["时间序列数据", "趋势分析", "季节变化"]
                },
                "regional_scatter": {
                    "name": "地区散点图",
                    "description": "使用散点图展示地区间数据关系",
                    "chart_type": "scatter",
                    "suitable_for": ["相关性分析", "分布分析", "异常检测"]
                }
            },
            "fallback_strategy": {
                "primary": "china_map",
                "fallback_1": "regional_bar", 
                "fallback_2": "regional_pie",
                "fallback_3": "regional_line"
            }
        }
        
        # 保存配置文件
        config_file = Path('config/visualization_alternatives.json')
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(alt_viz_config, f, ensure_ascii=False, indent=2)
        
        self.cleanup_log.append("创建: config/visualization_alternatives.json")
        print("  ✅ 替代可视化配置创建完成")
    
    def update_gitignore(self):
        """更新.gitignore文件"""
        print("📝 更新.gitignore文件...")
        
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

# Flask
instance/
.webassets-cache

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/*.log
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Temporary files
temp/
*.tmp
*.temp

# Backups
backups/*.sql
backups/structure_backup/

# OS
.DS_Store
Thumbs.db

# Documentation archives
docs/archive/

# Reports
reports/*.json
"""
        
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        self.cleanup_log.append("更新: .gitignore")
        print("  ✅ .gitignore文件更新完成")
    
    def generate_structure_report(self):
        """生成结构优化报告"""
        print("📋 生成结构优化报告...")
        
        report = {
            "optimization_date": datetime.now().isoformat(),
            "actions_performed": self.cleanup_log,
            "optimized_structure": {
                "core_modules": ["auth", "data_crawler", "data_analysis", "visualization"],
                "support_modules": ["scripts", "tests", "docs", "config", "utils", "api"],
                "static_resources": ["templates", "static"],
                "runtime_dirs": ["logs", "backups", "instance"]
            },
            "alternative_visualizations": {
                "enabled": True,
                "config_file": "config/visualization_alternatives.json",
                "fallback_charts": ["regional_bar", "regional_pie", "regional_line", "regional_scatter"]
            },
            "cleanup_summary": {
                "redundant_docs_archived": len([log for log in self.cleanup_log if "归档文档" in log]),
                "temp_files_removed": len([log for log in self.cleanup_log if "删除" in log]),
                "configs_reorganized": len([log for log in self.cleanup_log if "移动" in log and "config" in log])
            }
        }
        
        # 保存报告
        report_file = Path('reports/structure_optimization_report.json')
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ 报告生成完成: {report_file}")
        return report
    
    def optimize(self):
        """执行完整的项目结构优化"""
        print("🚀 开始项目结构优化")
        print("=" * 60)
        
        # 分析问题
        issues = self.analyze_current_issues()
        
        # 创建备份
        self.create_backup()
        
        # 清理工作
        self.clean_redundant_docs(issues['redundant_docs'])
        self.clean_temp_files(issues['temp_files'])
        
        # 重新组织
        self.reorganize_configs()
        self.create_optimized_structure()
        
        # 创建替代方案
        self.create_alternative_visualizations()
        
        # 更新配置
        self.update_gitignore()
        
        # 生成报告
        report = self.generate_structure_report()
        
        print("\n" + "=" * 60)
        print("✅ 项目结构优化完成！")
        print(f"📊 执行了 {len(self.cleanup_log)} 项优化操作")
        print("📁 项目现在具有清晰的模块化结构")
        print("📊 已创建地图可视化的替代方案")
        print("📋 详细报告: reports/structure_optimization_report.json")
        
        return report

def main():
    """主函数"""
    optimizer = ProjectStructureOptimizer()
    optimizer.optimize()

if __name__ == "__main__":
    main()

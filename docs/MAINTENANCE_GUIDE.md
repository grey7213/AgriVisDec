# AgriDec 项目维护指南

## 🎯 项目结构维护原则

### 1. 目录结构规范
- **保持模块化**: 每个功能模块独立目录
- **职责单一**: 每个目录只包含相关功能的文件
- **层次清晰**: 避免过深的目录嵌套（建议不超过3层）

### 2. 文件组织规范
- **核心文件**: 保持在根目录（app.py, start.py等）
- **功能模块**: 按功能分组到对应目录
- **临时文件**: 统一放在temp/目录，定期清理

### 3. 命名约定
- **Python文件**: 小写字母+下划线 (`user_manager.py`)
- **目录名**: 小写字母+下划线 (`data_analysis/`)
- **文档文件**: 大写字母+下划线 (`PROJECT_STRUCTURE.md`)

## 🔧 日常维护任务

### 定期清理（每周）
```bash
# 清理Python缓存
find . -name "__pycache__" -type d -exec rm -rf {} +

# 清理临时文件
rm -rf temp/*.tmp temp/*.log

# 清理过期备份（保留最近7天）
find backups/ -name "*.sql" -mtime +7 -delete
```

### 代码质量检查（每次提交前）
```bash
# 检查代码风格
flake8 --max-line-length=100 --ignore=E501,W503

# 运行测试套件
python -m pytest tests/ -v

# 检查导入路径
python -c "from app import app; print('导入检查通过')"
```

### 依赖管理
```bash
# 更新requirements.txt
pip freeze > requirements.txt

# 检查安全漏洞
pip audit

# 清理未使用的包
pip-autoremove -y
```

## 📁 新功能开发规范

### 添加新模块
1. **创建模块目录**:
   ```bash
   mkdir new_module
   touch new_module/__init__.py
   ```

2. **添加模块文件**:
   ```
   new_module/
   ├── __init__.py
   ├── manager.py      # 主要功能类
   ├── models.py       # 数据模型（如需要）
   └── utils.py        # 工具函数
   ```

3. **更新导入路径**:
   ```python
   # 在app.py中添加
   from new_module.manager import NewModuleManager
   ```

### 添加新页面
1. **创建模板文件**:
   ```bash
   # 放在templates/目录下
   touch templates/new_page.html
   ```

2. **添加静态资源**:
   ```bash
   # CSS文件
   touch static/css/new_page.css
   # JavaScript文件
   touch static/js/new_page.js
   ```

3. **添加路由**:
   ```python
   # 在app.py中添加
   @app.route('/new-page')
   def new_page():
       return render_template('new_page.html')
   ```

### 添加测试
1. **创建测试文件**:
   ```bash
   touch tests/test_new_module.py
   ```

2. **测试文件结构**:
   ```python
   import unittest
   from new_module.manager import NewModuleManager
   
   class TestNewModule(unittest.TestCase):
       def setUp(self):
           self.manager = NewModuleManager()
       
       def test_basic_functionality(self):
           # 测试代码
           pass
   ```

## 🗂️ 文件管理最佳实践

### 临时文件处理
- **开发期间**: 临时文件放在`temp/`目录
- **测试文件**: 以`test_`开头，放在`tests/`目录
- **脚本文件**: 工具脚本放在`scripts/`目录

### 文档管理
- **技术文档**: 放在`docs/`目录
- **API文档**: 使用docstring，可生成到`docs/api/`
- **用户手册**: 放在`docs/user/`目录

### 配置文件管理
- **应用配置**: `config.py`或`config/`目录
- **环境变量**: `.env`文件（不提交到版本控制）
- **部署配置**: `docker-compose.yml`, `Dockerfile`等

## 🚨 常见问题和解决方案

### 导入错误
**问题**: `ModuleNotFoundError`
**解决**: 检查`__init__.py`文件和导入路径

### 循环导入
**问题**: `ImportError: cannot import name`
**解决**: 重构代码结构，避免相互依赖

### 文件权限问题
**问题**: 无法写入日志或备份文件
**解决**: 检查目录权限，确保应用有写权限

### 数据库连接问题
**问题**: 数据库连接失败
**解决**: 检查`database.py`配置和数据库服务状态

## 📊 项目健康检查清单

### 每月检查
- [ ] 项目结构是否整洁
- [ ] 是否有未使用的文件
- [ ] 依赖包是否有安全更新
- [ ] 日志文件是否过大
- [ ] 备份文件是否正常

### 每季度检查
- [ ] 重构过时的代码
- [ ] 更新文档
- [ ] 性能优化
- [ ] 安全审计

### 版本发布前
- [ ] 运行完整测试套件
- [ ] 检查所有功能正常
- [ ] 更新版本号
- [ ] 生成发布说明

## 🔄 自动化维护脚本

### 项目清理脚本
```bash
#!/bin/bash
# scripts/cleanup.sh

echo "开始项目清理..."

# 清理Python缓存
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# 清理临时文件
rm -rf temp/*.tmp temp/*.log 2>/dev/null

# 清理过期日志
find logs/ -name "*.log" -mtime +30 -delete 2>/dev/null

echo "项目清理完成"
```

### 健康检查脚本
```python
#!/usr/bin/env python
# scripts/health_check.py

import os
import sys
from pathlib import Path

def check_project_structure():
    """检查项目结构完整性"""
    required_dirs = [
        'auth', 'data_crawler', 'data_analysis', 
        'visualization', 'templates', 'static',
        'scripts', 'tests', 'docs'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ 缺少目录: {', '.join(missing_dirs)}")
        return False
    
    print("✅ 项目结构完整")
    return True

def check_core_files():
    """检查核心文件存在性"""
    core_files = [
        'app.py', 'start.py', 'database.py', 
        'requirements.txt', 'README.md'
    ]
    
    missing_files = []
    for file_name in core_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ 缺少核心文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 核心文件完整")
    return True

if __name__ == "__main__":
    print("🔍 AgriDec 项目健康检查")
    print("=" * 30)
    
    structure_ok = check_project_structure()
    files_ok = check_core_files()
    
    if structure_ok and files_ok:
        print("\n🎉 项目状态良好！")
        sys.exit(0)
    else:
        print("\n⚠️ 项目需要维护")
        sys.exit(1)
```

## 📞 维护支持

遇到维护问题时，请参考：
1. 项目结构文档：`docs/PROJECT_STRUCTURE.md`
2. 部署指南：`docs/DEPLOYMENT_GUIDE.md`
3. 运行健康检查：`python scripts/health_check.py`
4. 执行项目清理：`python scripts/organize_project_structure.py`

保持项目结构的整洁和组织良好是确保长期可维护性的关键！

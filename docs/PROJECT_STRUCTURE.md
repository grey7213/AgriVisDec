# AgriDec 项目结构说明

## 📁 目录结构概览

```
AgriDec/
├── 📄 app.py                    # Flask主应用程序
├── 📄 start.py                  # 应用启动脚本
├── 📄 scheduler.py              # 定时任务调度器
├── 📄 database.py               # 共享数据库配置
├── 📄 config.py                 # 应用配置文件
├── 📄 requirements.txt          # Python依赖包列表
├── 📄 README.md                 # 项目说明文档
├── 📄 .gitignore               # Git忽略文件配置
│
├── 📂 auth/                     # 用户认证模块
│   ├── __init__.py
│   ├── models.py               # 用户数据模型
│   └── forms.py                # 认证表单定义
│
├── 📂 data_crawler/             # 数据爬虫模块
│   ├── __init__.py
│   └── crawler_manager.py      # 爬虫管理器
│
├── 📂 data_analysis/            # 数据分析模块
│   ├── __init__.py
│   └── analyzer.py             # 数据分析器
│
├── 📂 visualization/            # 数据可视化模块
│   ├── __init__.py
│   └── chart_generator.py      # 图表生成器
│
├── 📂 templates/                # HTML模板文件
│   ├── auth/                   # 认证相关模板
│   ├── errors/                 # 错误页面模板
│   ├── index.html              # 主页模板
│   ├── seed_dashboard.html     # 种子推荐面板
│   ├── weather_dashboard.html  # 天气看板
│   ├── machine_comparison.html # 农机对比
│   ├── farming_calendar.html   # 农事日历
│   └── purchase_module.html    # 采购模块
│
├── 📂 static/                   # 静态资源文件
│   ├── css/                    # 样式表文件
│   ├── js/                     # JavaScript文件
│   └── images/                 # 图片资源
│
├── 📂 scripts/                  # 工具脚本
│   ├── create_users.py         # 用户创建脚本
│   ├── migrate_to_mysql.py     # 数据库迁移脚本
│   ├── verify_migration.py     # 迁移验证脚本
│   ├── mysql_schema.sql        # MySQL数据库结构
│   └── organize_project_structure.py # 项目结构整理脚本
│
├── 📂 tests/                    # 测试文件
│   ├── __init__.py
│   ├── test_authentication.py  # 认证功能测试
│   ├── test_comprehensive_system.py # 系统综合测试
│   └── test_final_validation.py # 最终验证测试
│
├── 📂 docs/                     # 项目文档
│   ├── PROJECT_STRUCTURE.md    # 项目结构说明（本文件）
│   ├── DEPLOYMENT_GUIDE.md     # 部署指南
│   ├── PROJECT_INDEPENDENCE_SUMMARY.md # 独立性验证报告
│   ├── FINAL_DELIVERABLES_SUMMARY.md # 最终交付总结
│   ├── PROJECT_AUDIT_REPORT.md # 项目审计报告
│   ├── SYSTEM_STATUS_REPORT.md # 系统状态报告
│   └── 项目需求.md              # 原始项目需求
│
├── 📂 config/                   # 配置文件目录
│   └── __init__.py
│
├── 📂 utils/                    # 工具函数模块
│   └── __init__.py
│
├── 📂 logs/                     # 日志文件
│   └── scheduler.log           # 调度器日志
│
├── 📂 backups/                  # 数据备份
│   └── *.sql                   # SQL备份文件
│
├── 📂 reports/                  # 系统报告
│   └── project_cleanup_report.json # 项目清理报告
│
├── 📂 instance/                 # Flask实例文件
│   └── agridec.db              # SQLite数据库文件
│
└── 📂 temp/                     # 临时文件（开发用）
    ├── independence_report.json
    ├── make_independent.py
    ├── run_demo.py
    ├── test_login_fix.py
    ├── test_real_scraping.py
    └── verify_independence.py
```

## 🎯 模块职责说明

### 核心应用模块
- **app.py**: Flask主应用，包含路由定义和应用配置
- **start.py**: 应用启动入口，包含启动检查和初始化
- **scheduler.py**: 定时任务调度器，管理后台任务
- **database.py**: 数据库配置和连接管理

### 功能模块
- **auth/**: 用户认证和权限管理
- **data_crawler/**: 网络数据爬取和采集
- **data_analysis/**: 数据处理和分析算法
- **visualization/**: 图表生成和数据可视化

### 前端资源
- **templates/**: Jinja2 HTML模板
- **static/**: CSS、JavaScript和图片等静态资源

### 支持模块
- **scripts/**: 数据库管理、用户创建等工具脚本
- **tests/**: 单元测试和集成测试
- **docs/**: 项目文档和说明
- **config/**: 配置文件和环境设置

### 运行时目录
- **logs/**: 应用运行日志
- **backups/**: 数据备份文件
- **reports/**: 系统报告和分析结果
- **instance/**: Flask实例特定文件
- **temp/**: 临时文件和开发工具

## 📋 文件命名规范

### Python文件
- 使用小写字母和下划线：`user_manager.py`
- 模块名简洁明确：`analyzer.py`, `crawler_manager.py`
- 测试文件前缀：`test_authentication.py`

### 模板文件
- 使用小写字母和下划线：`seed_dashboard.html`
- 按功能分组到子目录：`auth/login.html`

### 静态资源
- CSS文件：`style.css`, `dashboard.css`
- JavaScript文件：`main.js`, `charts.js`
- 图片文件：使用描述性名称

### 文档文件
- 使用大写字母和下划线：`PROJECT_STRUCTURE.md`
- 中文文档可使用中文名：`项目需求.md`

## 🔧 开发规范

### 导入路径
```python
# 正确的导入方式
from auth.models import User
from data_crawler.crawler_manager import CrawlerManager
from visualization.chart_generator import ChartGenerator
```

### 模块组织
- 每个模块包含`__init__.py`文件
- 相关功能放在同一模块下
- 避免循环导入

### 代码注释
- 文件头部包含模块说明
- 函数和类包含docstring
- 复杂逻辑添加行内注释

## 🚀 部署注意事项

### 生产环境
- `temp/`目录不应部署到生产环境
- 确保`logs/`和`backups/`目录有写权限
- 配置适当的`.gitignore`忽略敏感文件

### 开发环境
- 使用虚拟环境隔离依赖
- 定期清理`temp/`目录
- 保持测试文件在`tests/`目录下

这个结构确保了项目的可维护性、可扩展性和专业性。

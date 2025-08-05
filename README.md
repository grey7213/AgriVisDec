# AgriDec - 农户专属农业信息可视化决策系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于网络爬虫的农业数据服务平台，为农户提供精准的农业信息服务和决策支持。

## 🌟 功能特性

### 核心功能模块

- 🌾 **种子推荐面板** - 基于实时数据的种子品种推荐和价格分析
- 🌤️ **天气适宜度看板** - 农事活动天气评估和预报服务
- 🚜 **农机对比表** - 农机设备价格对比和性能分析
- 📅 **农事日历** - 智能农时安排和提醒系统
- 🛒 **农资采购模块** - 采购决策支持和供应商信息

### 用户认证系统

- 👤 **用户注册/登录** - 完整的用户认证和会话管理
- 🔐 **权限控制** - 基于角色的访问控制系统
- 👨‍🌾 **个人资料管理** - 完整的用户信息编辑和查看功能
- 🏠 **农场信息** - 农场类型、规模、地区等详细信息管理
- 📊 **个人仪表板** - 定制化数据展示

### 数据采集与分析

- 🕷️ **智能爬虫** - 多源农业数据自动采集
- 📈 **数据分析** - 专业的农业数据分析算法
- 📊 **可视化图表** - ECharts驱动的交互式图表
- ⏰ **定时更新** - 自动化数据更新机制

## 🏗️ 技术架构

### 后端技术栈

- **Web框架**: Flask 2.3+ + Flask-SQLAlchemy
- **数据库**: MySQL 8.0+ (生产环境) / SQLite (开发环境)
- **认证系统**: Flask-Login + Flask-Bcrypt
- **表单处理**: Flask-WTF + WTForms
- **任务调度**: APScheduler
- **数据采集**: Requests + BeautifulSoup4

### 前端技术栈

- **UI框架**: Bootstrap 5.1+
- **图表库**: ECharts 5.4+
- **图标库**: Font Awesome 6.0+
- **JavaScript**: jQuery + 原生ES6+

### 数据库设计

- **用户系统**: 用户表、偏好设置表
- **农业数据**: 种子价格、天气数据、农机信息
- **系统管理**: 会话管理、日志记录

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+ (推荐 3.12+)
- **MySQL**: 8.0+ (生产环境)
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/your-username/AgriDec.git
cd AgriDec
```

2. **创建虚拟环境**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置数据库**

**MySQL配置 (推荐生产环境):**

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE agridec CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**环境变量配置:**

```bash
# 复制环境变量模板
cp config/.env.example .env
# 编辑 .env 文件，配置数据库连接
```

5. **初始化数据**

```bash
# 创建数据库表
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 创建默认用户
python scripts/create_users.py
```

6. **启动应用**

```bash
python start.py
```

7. **访问应用**
   打开浏览器访问: http://localhost:5000

### 默认账户

| 角色   | 用户名  | 密码      | 说明           |
| ------ | ------- | --------- | -------------- |
| 管理员 | admin   | admin123  | 系统管理员账户 |
| 农户   | farmer1 | farmer123 | 示例农户账户1  |
| 农户   | farmer2 | farmer123 | 示例农户账户2  |

## 📁 项目结构

```
AgriDec/
├── 📄 app.py                          # 主应用程序入口
├── 📄 start.py                        # 应用启动脚本
├── 📄 scheduler.py                    # 定时任务调度器
├── 📄 requirements.txt                # Python依赖包列表
├── 📄 README.md                       # 项目说明文档
├── 🔐 auth/                           # 用户认证模块
│   ├── 📄 __init__.py
│   ├── 📄 models.py                   # 数据模型定义
│   └── 📄 forms.py                    # 表单定义
├── ⚙️ config/                         # 配置文件目录
│   ├── 📄 __init__.py
│   ├── 📄 config.py                   # 应用配置
│   └── 📄 .env.example               # 环境变量模板
├── 🕷️ data_crawler/                   # 数据爬虫模块
│   ├── 📄 __init__.py
│   └── 📄 crawler_manager.py          # 爬虫管理器
├── 📊 data_analysis/                  # 数据分析模块
│   ├── 📄 __init__.py
│   └── 📄 analyzer.py                 # 数据分析器
├── 📈 visualization/                  # 数据可视化模块
│   ├── 📄 __init__.py
│   └── 📄 chart_generator.py          # 图表生成器
├── 🎨 templates/                      # HTML模板目录
│   ├── 🔐 auth/                       # 认证相关模板
│   │   ├── 📄 login.html              # 登录页面
│   │   ├── 📄 register.html           # 注册页面
│   │   ├── 📄 profile.html            # 个人资料查看页面
│   │   └── 📄 edit_profile.html       # 个人资料编辑页面
│   ├── ❌ errors/                     # 错误页面模板
│   │   ├── 📄 404.html                # 404错误页面
│   │   └── 📄 500.html                # 500错误页面
│   ├── 📄 index.html                  # 主页模板
│   ├── 📄 seed_dashboard.html         # 种子推荐面板
│   ├── 📄 weather_dashboard.html      # 天气看板
│   ├── 📄 machine_comparison.html     # 农机对比表
│   ├── 📄 farming_calendar.html       # 农事日历
│   └── 📄 purchase_module.html        # 采购模块
├── 🎯 static/                         # 静态资源目录
│   ├── 🎨 css/
│   │   └── 📄 main.css                # 主样式文件
│   ├── 📜 js/
│   │   └── 📄 main.js                 # 主JavaScript文件
│   └── 🖼️ images/                     # 图片资源
├── 🧪 tests/                          # 测试文件目录
│   ├── 📄 __init__.py
│   ├── 📄 test_authentication.py      # 认证系统测试
│   └── 📄 test_comprehensive_system.py # 综合系统测试
├── 📜 scripts/                        # 工具脚本目录
│   ├── 📄 create_users.py             # 用户创建脚本
│   ├── 📄 migrate_to_mysql.py         # 数据库迁移脚本
│   ├── 📄 verify_migration.py         # 迁移验证脚本
│   └── 📄 mysql_schema.sql            # MySQL数据库架构
├── 📚 docs/                           # 项目文档目录
│   ├── 📄 PROJECT_STRUCTURE.md        # 项目结构说明
│   ├── 📄 DEPLOYMENT_GUIDE.md         # 部署指南
│   ├── 📄 MAINTENANCE_GUIDE.md        # 维护指南
│   ├── 📄 GITHUB_UPLOAD_GUIDE.md      # GitHub上传指南
│   ├── 📄 PROJECT_AUDIT_REPORT.md     # 项目审计报告
│   └── 📄 FINAL_DELIVERABLES_SUMMARY.md # 最终交付总结
├── 🛠️ utils/                          # 工具函数目录
│   └── 📄 __init__.py
├── 📝 logs/                           # 日志文件目录
│   └── 📄 scheduler.log               # 调度器日志
└── 💾 instance/                       # 实例文件目录
    └── 📄 agridec.db                  # SQLite数据库文件
```

## 🌐 API接口文档

### 认证相关接口

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/login` | POST | 用户登录 | username, password |
| `/register` | POST | 用户注册 | username, email, password, real_name, phone, region, farm_type, farm_size |
| `/logout` | GET | 用户登出 | - |
| `/profile` | GET | 查看个人资料 | - |
| `/profile/edit` | GET/POST | 编辑个人资料 | real_name, email, phone, region, farm_type, farm_size |

### 数据接口

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/seed-prices` | GET | 获取种子价格数据 | limit, region, crop_type |
| `/api/weather-forecast` | GET | 获取天气预报数据 | region, days |
| `/api/farm-machines` | GET | 获取农机设备信息 | category, brand |
| `/api/generate-chart` | POST | 生成图表配置 | chart_type, data, options |
| `/api/crawl-data` | POST | 触发数据爬取 | website, data_type, region |

### 页面路由

| 路由 | 说明 | 权限要求 |
|------|------|----------|
| `/` | 主页数据看板 | 无 |
| `/seed-dashboard` | 种子推荐面板 | 登录用户 |
| `/weather-dashboard` | 天气适宜度看板 | 登录用户 |
| `/machine-comparison` | 农机对比表 | 登录用户 |
| `/farming-calendar` | 农事日历 | 登录用户 |
| `/purchase-module` | 农资采购模块 | 登录用户 |

## 🌐 数据源

### 主要数据来源

- **中国种子交易网** - 实时种子价格和品种信息
- **中国天气网** - 天气预报和气象数据
- **农机360网** - 农机设备信息和价格对比

### 数据更新频率

- **种子价格**: 每日更新
- **天气数据**: 每6小时更新
- **农机信息**: 每周更新

## 🔧 配置说明

### 环境变量配置

创建 `.env` 文件并配置以下变量:

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost/agridec?charset=utf8mb4

# 应用配置
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# 爬虫配置
CRAWLER_DELAY=1
MAX_RETRY_TIMES=3

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/agridec.log
```

### MySQL数据库配置

```sql
-- 创建数据库
CREATE DATABASE agridec CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（可选）
CREATE USER 'agridec_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON agridec.* TO 'agridec_user'@'localhost';
FLUSH PRIVILEGES;
```

## 🧪 测试

### 运行测试套件

```bash
# 运行认证系统测试
python tests/test_authentication.py

# 运行综合系统测试
python tests/test_comprehensive_system.py
```

### 测试覆盖范围

- ✅ 用户认证系统
- ✅ 数据采集功能
- ✅ Web界面响应
- ✅ API接口测试
- ✅ 数据库操作
- ✅ 响应式设计

## 🚀 部署

### 生产环境部署

1. **服务器要求**

   - CPU: 2核心以上
   - 内存: 4GB以上
   - 存储: 20GB以上
   - 网络: 稳定的互联网连接
2. **使用Gunicorn部署**

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **使用Nginx反向代理**

```nginx
server {
    listen 80;
    server_name your-domain.com;
  
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. **使用Docker部署**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 更新日志

### v2.1.0 (2025-08-05)

- ✨ 新增用户个人资料管理功能
- 👤 完善用户信息编辑和查看页面
- 🎨 优化导航栏用户菜单
- 📚 新增GitHub上传指南
- 🔧 完善项目文档体系

### v2.0.0 (2025-01-05)

- ✨ 新增用户认证系统
- 🗄️ 迁移到MySQL数据库
- 🎨 重构项目架构
- 📱 优化响应式设计
- 🧪 完善测试覆盖

### v1.0.0 (2024-12-01)

- 🎉 初始版本发布
- 🕷️ 实现数据爬虫功能
- 📊 基础数据可视化
- 🌾 农业数据分析

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下步骤：

### 1. Fork项目
```bash
# 在GitHub上点击Fork按钮
# 克隆你的Fork
git clone https://github.com/你的用户名/AgriDec.git
cd AgriDec
```

### 2. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

### 3. 提交更改
```bash
git add .
git commit -m "feat: 添加新功能描述"
git push origin feature/your-feature-name
```

### 4. 创建Pull Request
- 在GitHub上创建Pull Request
- 详细描述你的更改
- 等待代码审查

### 代码规范
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档
- 编写测试用例
- 确保所有测试通过

### 提交信息规范
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👥 开发团队

- **项目负责人**: AgriDec Team
- **技术架构**: Full Stack Development
- **数据分析**: Agricultural Data Science
- **UI/UX设计**: Modern Web Design

## 📞 联系我们

- **项目主页**: https://github.com/grey7213/AgriVisDec
- **问题反馈**: https://github.com/grey7213/AgriVisDec/issues
- **邮箱**: yjy112508@163.com
- **上传指南**: [GitHub上传指南](docs/GITHUB_UPLOAD_GUIDE.md)
- **项目文档**: [文档目录](docs/)

## 🙏 致谢

感谢所有为AgriDec项目做出贡献的开发者和用户！

特别感谢：
- Flask框架和相关扩展的开发者
- 开源数据源提供者
- 测试和反馈的用户们

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！

**AgriDec** - 让农业决策更智能，让农民生活更美好！ 🌾

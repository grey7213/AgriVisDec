# AgriDec GitHub 上传指南

## 📋 前置准备

### 1. 安装Git

```bash
# Windows
# 下载并安装 Git for Windows: https://git-scm.com/download/win

# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# CentOS/RHEL
sudo yum install git
```

### 2. 配置Git用户信息

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"
```

### 3. 创建GitHub账户

- 访问 [GitHub.com](https://github.com) 注册账户
- 验证邮箱地址

## 🚀 创建GitHub仓库

### 方法一：通过GitHub网站创建

1. **登录GitHub**

   - 访问 [GitHub.com](https://github.com)
   - 点击右上角 "Sign in" 登录
2. **创建新仓库**

   - 点击右上角 "+" 号
   - 选择 "New repository"
3. **配置仓库信息**

   ```
   Repository name: AgriDec
   Description: 基于网络爬虫的农业数据服务平台 - 农户专属农业信息可视化决策系统

   ☑️ Public (公开仓库)
   ☐ Add a README file (不勾选，我们已有README)
   ☐ Add .gitignore (不勾选，我们已有.gitignore)
   ☐ Choose a license (可选择MIT License)
   ```
4. **点击 "Create repository"**

### 方法二：通过GitHub CLI创建

```bash
# 安装GitHub CLI
# Windows: winget install GitHub.CLI
# macOS: brew install gh
# Linux: 参考 https://cli.github.com/manual/installation

# 登录GitHub
gh auth login

# 创建仓库
gh repo create AgriDec --public --description "基于网络爬虫的农业数据服务平台"
```

## 📤 上传代码到GitHub

### 1. 初始化本地Git仓库

```bash
# 进入项目目录
cd /path/to/AgriDec

# 初始化Git仓库
git init

# 添加远程仓库地址（替换为你的GitHub用户名）
git remote add origin https://github.com/你的用户名/AgriDec.git
```

### 2. 准备提交文件

```bash
# 查看当前状态
git status

# 添加所有文件到暂存区
git add .

# 或者选择性添加文件
git add app.py
git add requirements.txt
git add README.md
# ... 其他文件
```

### 3. 创建首次提交

```bash
# 创建提交
git commit -m "Initial commit: AgriDec农业数据服务平台

- 完整的Flask Web应用
- 用户认证系统
- 数据爬虫模块
- 数据分析和可视化
- 种子推荐、天气看板等功能模块
- MySQL/SQLite数据库支持
- 响应式Web界面"
```

### 4. 推送到GitHub

```bash
# 推送到GitHub（首次推送）
git push -u origin main

# 如果遇到分支名问题，可能需要：
git branch -M main
git push -u origin main
```

## 🔐 SSH密钥配置（推荐）

### 1. 生成SSH密钥

```bash
# 生成SSH密钥对
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 如果系统不支持ed25519，使用RSA
ssh-keygen -t rsa -b 4096 -C "你的邮箱@example.com"

# 按提示操作，可以直接回车使用默认设置
```

### 2. 添加SSH密钥到ssh-agent

```bash
# 启动ssh-agent
eval "$(ssh-agent -s)"

# 添加私钥到ssh-agent
ssh-add ~/.ssh/id_ed25519
```

### 3. 添加公钥到GitHub

```bash
# 复制公钥内容
cat ~/.ssh/id_ed25519.pub

# Windows用户可以使用：
# type %USERPROFILE%\.ssh\id_ed25519.pub
```

然后：

1. 登录GitHub
2. 点击右上角头像 → Settings
3. 左侧菜单选择 "SSH and GPG keys"
4. 点击 "New SSH key"
5. 粘贴公钥内容，添加标题
6. 点击 "Add SSH key"

### 4. 使用SSH地址

```bash
# 更改远程仓库地址为SSH
git remote set-url origin git@github.com:你的用户名/AgriDec.git
```

## 📝 日常Git操作

### 基本工作流程

```bash
# 1. 查看状态
git status

# 2. 添加修改的文件
git add .
# 或添加特定文件
git add app.py templates/

# 3. 提交更改
git commit -m "feat: 添加用户个人资料管理功能

- 新增个人资料查看页面
- 新增个人资料编辑功能
- 更新导航栏用户菜单
- 完善表单验证"

# 4. 推送到GitHub
git push origin main
```

### 常用Git命令

```bash
# 查看提交历史
git log --oneline

# 查看文件差异
git diff

# 撤销工作区修改
git checkout -- 文件名

# 撤销暂存区文件
git reset HEAD 文件名

# 创建新分支
git checkout -b feature/new-feature

# 切换分支
git checkout main

# 合并分支
git merge feature/new-feature

# 删除分支
git branch -d feature/new-feature
```

## 🏷️ 版本标签管理

```bash
# 创建标签
git tag -a v1.0.0 -m "AgriDec v1.0.0 正式版本

主要功能：
- 用户认证系统
- 数据爬虫和分析
- 种子推荐面板
- 天气适宜度看板
- 农具对比和农事日历
- 农资采购模块"

# 推送标签到GitHub
git push origin v1.0.0

# 推送所有标签
git push origin --tags

# 查看标签
git tag -l
```

## 📋 提交信息规范

### 提交类型

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 提交格式

```
<类型>(<范围>): <简短描述>

<详细描述>

<相关issue或PR>
```

### 示例

```bash
git commit -m "feat(auth): 添加用户个人资料管理功能

- 新增个人资料查看和编辑页面
- 添加表单验证和错误处理
- 更新导航栏用户菜单
- 完善用户数据模型

Closes #123"
```

## 🔄 协作开发

### Fork工作流程

1. **Fork仓库**

   - 在GitHub上点击 "Fork" 按钮
2. **克隆Fork的仓库**

   ```bash
   git clone https://github.com/你的用户名/AgriDec.git
   cd AgriDec
   ```
3. **添加上游仓库**

   ```bash
   git remote add upstream https://github.com/原作者/AgriDec.git
   ```
4. **创建功能分支**

   ```bash
   git checkout -b feature/your-feature
   ```
5. **提交更改并推送**

   ```bash
   git add .
   git commit -m "feat: 你的功能描述"
   git push origin feature/your-feature
   ```
6. **创建Pull Request**

   - 在GitHub上点击 "New pull request"

## 🚨 常见问题解决

### 1. 推送被拒绝

```bash
# 先拉取远程更改
git pull origin main

# 解决冲突后再推送
git push origin main
```

### 2. 忘记添加.gitignore

```bash
# 移除已跟踪的文件
git rm -r --cached .
git add .
git commit -m "fix: 更新.gitignore规则"
```

### 3. 撤销最后一次提交

```bash
# 保留更改
git reset --soft HEAD~1

# 完全撤销
git reset --hard HEAD~1
```

### 4. 修改最后一次提交信息

```bash
git commit --amend -m "新的提交信息"
```

## 📞 获取帮助

- Git官方文档: https://git-scm.com/doc
- GitHub帮助: https://docs.github.com
- Git教程: https://www.atlassian.com/git/tutorials

完成上传后，你的AgriDec项目将在GitHub上可见，其他开发者可以查看、Fork和贡献代码！

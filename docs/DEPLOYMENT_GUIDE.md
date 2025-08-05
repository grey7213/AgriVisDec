# AgriDec 部署指南

本文档提供了 AgriDec 农业信息可视化决策系统的完整部署指南。

## 📋 部署前检查清单

### 系统要求
- [ ] Python 3.8+ (推荐 3.12+)
- [ ] MySQL 8.0+ (生产环境)
- [ ] 至少 4GB RAM
- [ ] 至少 20GB 存储空间
- [ ] 稳定的互联网连接

### 环境准备
- [ ] 服务器或云主机已准备
- [ ] 域名已配置 (可选)
- [ ] SSL证书已准备 (生产环境推荐)
- [ ] 防火墙规则已配置

## 🚀 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/your-username/AgriDec.git
cd AgriDec
```

### 2. 创建虚拟环境

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp config/.env.example .env

# 编辑环境变量文件
nano .env
```

**重要配置项：**
```env
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost/agridec?charset=utf8mb4

# 应用密钥 (请修改为随机字符串)
SECRET_KEY=your-super-secret-key-change-this-in-production

# 运行环境
FLASK_ENV=production
FLASK_DEBUG=False
```

### 5. 数据库初始化

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE agridec CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit

# 初始化数据表
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 创建默认用户
python scripts/create_users.py
```

### 6. 启动应用

**开发环境：**
```bash
python start.py
```

**生产环境：**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐳 Docker 部署

### 1. 创建 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p logs uploads instance

# 设置权限
RUN chmod +x start.py

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://agridec:password@db/agridec?charset=utf8mb4
      - SECRET_KEY=your-secret-key
      - FLASK_ENV=production
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=agridec
      - MYSQL_USER=agridec
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

volumes:
  mysql_data:
```

### 3. 启动容器

```bash
docker-compose up -d
```

## 🌐 Nginx 反向代理

### 1. 安装 Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

### 2. 配置 Nginx

创建配置文件 `/etc/nginx/sites-available/agridec`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 重定向到HTTPS (可选)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL配置
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 静态文件
    location /static {
        alias /path/to/AgriDec/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 应用代理
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持 (如果需要)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

### 3. 启用配置

```bash
sudo ln -s /etc/nginx/sites-available/agridec /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔧 系统服务配置

### 1. 创建 systemd 服务

创建文件 `/etc/systemd/system/agridec.service`:

```ini
[Unit]
Description=AgriDec Agricultural Decision Support System
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/AgriDec
Environment=PATH=/path/to/AgriDec/venv/bin
ExecStart=/path/to/AgriDec/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 2. 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable agridec
sudo systemctl start agridec
sudo systemctl status agridec
```

## 📊 监控和日志

### 1. 日志配置

应用日志位置：
- 应用日志: `logs/agridec.log`
- 调度器日志: `logs/scheduler.log`
- Nginx日志: `/var/log/nginx/`

### 2. 日志轮转

创建 `/etc/logrotate.d/agridec`:

```
/path/to/AgriDec/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload agridec
    endscript
}
```

### 3. 系统监控

推荐监控指标：
- CPU 使用率
- 内存使用率
- 磁盘空间
- 数据库连接数
- HTTP 响应时间
- 错误率

## 🔒 安全配置

### 1. 防火墙设置

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 2. 数据库安全

```sql
-- 创建专用数据库用户
CREATE USER 'agridec_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON agridec.* TO 'agridec_user'@'localhost';
FLUSH PRIVILEGES;

-- 删除默认用户
DROP USER 'root'@'';
```

### 3. 应用安全

- 定期更新依赖包
- 使用强密码
- 启用 HTTPS
- 配置 CSP 头
- 定期备份数据

## 🔄 更新和维护

### 1. 应用更新

```bash
# 备份数据库
mysqldump -u root -p agridec > backup_$(date +%Y%m%d).sql

# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt

# 重启服务
sudo systemctl restart agridec
```

### 2. 数据库备份

```bash
# 创建备份脚本
cat > /usr/local/bin/agridec-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/agridec"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
mysqldump -u root -p agridec | gzip > $BACKUP_DIR/agridec_$DATE.sql.gz
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
EOF

chmod +x /usr/local/bin/agridec-backup.sh

# 添加到 crontab
echo "0 2 * * * /usr/local/bin/agridec-backup.sh" | crontab -
```

## 🚨 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务状态
   - 验证连接字符串
   - 检查防火墙设置

2. **静态文件无法加载**
   - 检查 Nginx 配置
   - 验证文件权限
   - 检查路径设置

3. **应用启动失败**
   - 查看应用日志
   - 检查端口占用
   - 验证环境变量

4. **性能问题**
   - 增加 Gunicorn worker 数量
   - 优化数据库查询
   - 启用缓存

### 日志查看

```bash
# 应用日志
tail -f logs/agridec.log

# 系统服务日志
sudo journalctl -u agridec -f

# Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 查看相关日志文件
2. 检查系统资源使用情况
3. 验证配置文件设置
4. 参考故障排除部分
5. 提交 GitHub Issue

---

**部署成功后，您的 AgriDec 系统将为农户提供专业的农业信息服务！** 🌾

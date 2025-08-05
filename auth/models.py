# -*- coding: utf-8 -*-
"""
AgriDec 数据模型
定义用户认证和数据库模型
"""

from flask_login import UserMixin
from datetime import datetime, date
import secrets

# 导入共享数据库实例
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db, bcrypt

class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    real_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    region = db.Column(db.String(50))  # 用户所在地区
    farm_type = db.Column(db.String(50))  # 农场类型
    farm_size = db.Column(db.Float)  # 农场规模（亩）
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    
    # 用户偏好设置
    preferences = db.relationship('UserPreference', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def update_login_info(self):
        """更新登录信息"""
        self.last_login = datetime.utcnow()
        self.login_count += 1
        db.session.commit()
    
    def get_preference(self, key, default=None):
        """获取用户偏好设置"""
        pref = UserPreference.query.filter_by(user_id=self.id, key=key).first()
        return pref.value if pref else default
    
    def set_preference(self, key, value):
        """设置用户偏好"""
        pref = UserPreference.query.filter_by(user_id=self.id, key=key).first()
        if pref:
            pref.value = str(value)
        else:
            pref = UserPreference(user_id=self.id, key=key, value=str(value))
            db.session.add(pref)
        db.session.commit()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'real_name': self.real_name,
            'region': self.region,
            'farm_type': self.farm_type,
            'farm_size': self.farm_size,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'login_count': self.login_count
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserPreference(db.Model):
    """用户偏好设置"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'key', name='uk_user_preference'),)
    
    def __repr__(self):
        return f'<UserPreference {self.key}={self.value}>'

class UserSession(db.Model):
    """用户会话管理"""
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    user = db.relationship('User', backref='sessions')
    
    @staticmethod
    def generate_token():
        """生成会话令牌"""
        return secrets.token_urlsafe(32)
    
    def is_expired(self):
        """检查会话是否过期"""
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f'<UserSession {self.session_token[:8]}...>'

# 数据库初始化函数
def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        # 创建用户相关表
        db.create_all()
        
        # 创建默认管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@agridec.com',
                real_name='系统管理员',
                region='全国',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ 创建默认管理员用户: admin/admin123")

def create_sample_users():
    """创建示例用户"""
    sample_users = [
        {
            'username': 'farmer1',
            'email': 'farmer1@example.com',
            'password': 'farmer123',
            'real_name': '张三',
            'region': '山东省',
            'farm_type': '种植业',
            'farm_size': 50.0
        },
        {
            'username': 'farmer2',
            'email': 'farmer2@example.com',
            'password': 'farmer123',
            'real_name': '李四',
            'region': '河南省',
            'farm_type': '养殖业',
            'farm_size': 30.0
        },
        {
            'username': 'farmer3',
            'email': 'farmer3@example.com',
            'password': 'farmer123',
            'real_name': '王五',
            'region': '江苏省',
            'farm_type': '混合农业',
            'farm_size': 80.0
        }
    ]
    
    for user_data in sample_users:
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                real_name=user_data['real_name'],
                region=user_data['region'],
                farm_type=user_data['farm_type'],
                farm_size=user_data['farm_size']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
    
    db.session.commit()
    print("✅ 创建示例用户完成")

# 添加用户表到MySQL schema
def get_user_tables_sql():
    """获取用户表的SQL创建语句"""
    return """
-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    real_name VARCHAR(100),
    phone VARCHAR(20),
    region VARCHAR(50),
    farm_type VARCHAR(50),
    farm_size DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    login_count INT DEFAULT 0,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户偏好设置表
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    `key` VARCHAR(100) NOT NULL,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_preference (user_id, `key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户会话表
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

# 数据模型
class SeedPrice(db.Model):
    """种子价格数据模型"""
    __tablename__ = 'seed_prices'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))
    region = db.Column(db.String(50))
    date = db.Column(db.Date, nullable=False)
    source_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherData(db.Model):
    """天气数据模型"""
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float)
    weather = db.Column(db.String(50))
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FarmMachine(db.Model):
    """农机设备数据模型"""
    __tablename__ = 'farm_machines'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    price = db.Column(db.Float)
    specifications = db.Column(db.Text)
    region = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建默认用户脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth.models import db, User, bcrypt

# 创建应用实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/agridec?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'agridec-secret-key-2025'

# 初始化数据库
db.init_app(app)
bcrypt.init_app(app)

def create_default_users():
    """创建默认用户"""
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 创建管理员用户
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
            print("✅ 创建管理员用户: admin/admin123")
        
        # 创建示例农户用户
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
                print(f"✅ 创建用户: {user_data['username']}/{user_data['password']}")
        
        db.session.commit()
        print("🎉 用户创建完成！")

if __name__ == '__main__':
    create_default_users()

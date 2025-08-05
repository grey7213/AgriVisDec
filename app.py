# -*- coding: utf-8 -*-
"""
AgriDec - 基于网络爬虫的农业数据服务平台
农户专属农业信息可视化决策系统
主应用程序入口
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import os
import json

# 导入共享数据库实例
from database import db, bcrypt, init_db

# 创建Flask应用
app = Flask(__name__)

# 数据库配置 - 现在由多数据库管理器处理
app.config['SECRET_KEY'] = 'agridec-secret-key-2025'

# 初始化增强数据库系统
init_db(app)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面'
login_manager.login_message_category = 'info'

# 提供应用实例访问函数
def get_app():
    """获取当前Flask应用实例"""
    return app

def get_db():
    """获取数据库实例"""
    return db

# 导入模块
from data_crawler.crawler_manager import CrawlerManager
from data_analysis.analyzer import DataAnalyzer

# 强制重新加载图表生成器模块
import importlib
import sys
if 'visualization.chart_generator' in sys.modules:
    importlib.reload(sys.modules['visualization.chart_generator'])

from visualization.chart_generator import ChartGenerator
from scheduler import start_scheduler, get_scheduler_status

# 导入认证相关模块
from auth.models import User, SeedPrice, WeatherData, FarmMachine
from auth.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm, DataCollectionForm

# 导入数据库管理API
from api.database_management import db_management_bp

@login_manager.user_loader
def load_user(user_id):
    """加载用户"""
    return User.query.get(int(user_id))

# 初始化组件
crawler_manager = CrawlerManager()
data_analyzer = DataAnalyzer()

# 强制重新创建图表生成器实例以获取最新功能
chart_generator = ChartGenerator()

# 注册数据库管理API蓝图
app.register_blueprint(db_management_bp)

# 数据库模型已在 auth.models 中定义

# 认证路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.update_login_info()
            flash('登录成功！', 'success')

            # 重定向到用户原本想访问的页面
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('用户名或密码错误', 'error')

    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            real_name=form.real_name.data,
            phone=form.phone.data,
            region=form.region.data,
            farm_type=form.farm_type.data,
            farm_size=form.farm_size.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    """用户个人资料页面"""
    return render_template('auth/profile.html', user=current_user)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑用户个人资料"""
    form = ProfileForm(original_email=current_user.email)

    if form.validate_on_submit():
        current_user.real_name = form.real_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.region = form.region.data
        current_user.farm_type = form.farm_type.data
        current_user.farm_size = form.farm_size.data

        db.session.commit()
        flash('个人资料更新成功！', 'success')
        return redirect(url_for('profile'))

    # 预填充表单数据
    form.real_name.data = current_user.real_name
    form.email.data = current_user.email
    form.phone.data = current_user.phone
    form.region.data = current_user.region
    form.farm_type.data = current_user.farm_type
    form.farm_size.data = current_user.farm_size

    return render_template('auth/edit_profile.html', form=form)

# 主要路由
@app.route('/')
def index():
    """首页 - 农业数据看板"""
    return render_template('index.html')

@app.route('/seed-dashboard')
@login_required
def seed_dashboard():
    """种子推荐面板"""
    return render_template('seed_dashboard.html')

@app.route('/weather-dashboard')
@login_required
def weather_dashboard():
    """天气适宜度看板"""
    return render_template('weather_dashboard.html')

@app.route('/machine-comparison')
@login_required
def machine_comparison():
    """农具对比表"""
    return render_template('machine_comparison.html')

@app.route('/farming-calendar')
@login_required
def farming_calendar():
    """农事日历"""
    return render_template('farming_calendar.html')

@app.route('/purchase-module')
@login_required
def purchase_module():
    """农资采购模块"""
    return render_template('purchase_module.html')

@app.route('/admin')
@login_required
def admin():
    """管理员面板"""
    if not current_user.is_admin:
        flash('需要管理员权限', 'error')
        return redirect(url_for('index'))

    return render_template('admin/admin.html')

@app.route('/admin/database')
@login_required
def admin_database():
    """数据库管理页面"""
    if not current_user.is_admin:
        flash('需要管理员权限', 'error')
        return redirect(url_for('index'))

    return render_template('admin/database_management.html')

# API接口
@app.route('/api/crawl-data', methods=['POST'])
def crawl_data():
    """数据采集API"""
    try:
        data = request.get_json()
        website = data.get('website')
        data_type = data.get('data_type')
        region = data.get('region', '全国')
        
        # 调用爬虫管理器
        result = crawler_manager.crawl_data(website, data_type, region)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-chart', methods=['POST'])
def generate_chart():
    """图表生成API"""
    try:
        data = request.get_json()
        chart_type = data.get('chart_type')
        chart_data = data.get('data')

        # 调试信息
        app.logger.info(f"生成图表类型: {chart_type}")
        app.logger.info(f"支持的图表类型: {list(chart_generator.supported_chart_types.keys())}")

        # 调用图表生成器
        result = chart_generator.generate_chart(chart_type, chart_data, data)

        return jsonify(result)
    except Exception as e:
        app.logger.error(f"图表生成错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scheduler-status')
def scheduler_status():
    """获取调度器状态"""
    try:
        status = get_scheduler_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/seed-prices')
def get_seed_prices():
    """获取种子价格数据"""
    region = request.args.get('region', '全国')
    limit = request.args.get('limit', 50, type=int)
    
    query = SeedPrice.query
    if region != '全国':
        query = query.filter(SeedPrice.region.like(f'%{region}%'))
    
    prices = query.order_by(SeedPrice.date.desc()).limit(limit).all()
    
    result = []
    for price in prices:
        result.append({
            'product_name': price.product_name,
            'variety': price.variety,
            'price': price.price,
            'unit': price.unit,
            'region': price.region,
            'date': price.date.strftime('%Y-%m-%d')
        })
    
    return jsonify(result)

@app.route('/api/weather-forecast')
def get_weather_forecast():
    """获取天气预报数据"""
    region = request.args.get('region', '全国')
    days = request.args.get('days', 7, type=int)
    
    query = WeatherData.query
    if region != '全国':
        query = query.filter(WeatherData.region.like(f'%{region}%'))
    
    weather_data = query.order_by(WeatherData.date.desc()).limit(days).all()
    
    result = []
    for weather in weather_data:
        result.append({
            'region': weather.region,
            'date': weather.date.strftime('%Y-%m-%d'),
            'temperature': weather.temperature,
            'weather': weather.weather,
            'humidity': weather.humidity,
            'wind_speed': weather.wind_speed
        })
    
    return jsonify(result)

@app.route('/api/farm-machines')
def get_farm_machines():
    """获取农机设备数据"""
    category = request.args.get('category', '')
    region = request.args.get('region', '全国')
    limit = request.args.get('limit', 20, type=int)
    
    query = FarmMachine.query
    if category:
        query = query.filter(FarmMachine.product_name.like(f'%{category}%'))
    if region != '全国':
        query = query.filter(FarmMachine.region.like(f'%{region}%'))
    
    machines = query.order_by(FarmMachine.created_at.desc()).limit(limit).all()
    
    result = []
    for machine in machines:
        result.append({
            'product_name': machine.product_name,
            'brand': machine.brand,
            'model': machine.model,
            'price': machine.price,
            'specifications': machine.specifications,
            'region': machine.region
        })
    
    return jsonify(result)

# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    """404错误处理"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """全局异常处理"""
    import traceback
    app.logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
    return render_template('errors/500.html'), 500

# 初始化数据库
def create_tables():
    """创建数据库表"""
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    # 创建必要的目录
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('data_crawler', exist_ok=True)
    os.makedirs('data_analysis', exist_ok=True)
    os.makedirs('visualization', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

    # 初始化数据库
    create_tables()

    # 启动定时任务调度器
    try:
        start_scheduler()
        app.logger.info("定时任务调度器启动成功")
    except Exception as e:
        app.logger.error(f"定时任务调度器启动失败: {str(e)}")

    # 启动应用
    app.run(debug=True, host='0.0.0.0', port=5000)

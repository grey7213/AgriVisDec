# -*- coding: utf-8 -*-
"""
AgriDec 项目配置文件
"""

import os
from datetime import timedelta

class Config:
    """基础配置"""
    
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agridec-secret-key-2024'
    
    # 数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'agri_data'
    
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@'
        f'{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # Redis配置（用于缓存和任务队列）
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_DB = int(os.environ.get('REDIS_DB') or 0)
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    
    # 缓存配置
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = REDIS_HOST
    CACHE_REDIS_PORT = REDIS_PORT
    CACHE_REDIS_DB = REDIS_DB
    CACHE_REDIS_PASSWORD = REDIS_PASSWORD
    CACHE_DEFAULT_TIMEOUT = 300
    
    # 爬虫配置
    CRAWLER_CONFIG = {
        'default_delay': 2000,  # 默认请求间隔（毫秒）
        'max_pages': 10,        # 默认最大页数
        'timeout': 30,          # 请求超时时间（秒）
        'retry_times': 3,       # 重试次数
        'user_agent': 'AgriDec-Bot/1.0 (Agricultural Data Service)',
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    }
    
    # 数据源配置
    DATA_SOURCES = {
        'seed_trade': {
            'name': '中国种子交易网',
            'base_url': 'https://www.114seeds.com',
            'enabled': True,
            'rate_limit': 1000,  # 每小时请求限制
            'data_types': ['price', 'product_info']
        },
        'weather': {
            'name': '中国天气网',
            'base_url': 'http://www.weather.com.cn',
            'enabled': True,
            'rate_limit': 2000,
            'data_types': ['weather_forecast']
        },
        'farm_machine': {
            'name': '农机360网',
            'base_url': 'https://www.nongjx.com',
            'enabled': True,
            'rate_limit': 800,
            'data_types': ['product_info', 'price']
        }
    }
    
    # 任务调度配置
    SCHEDULER_CONFIG = {
        'SCHEDULER_API_ENABLED': True,
        'SCHEDULER_TIMEZONE': 'Asia/Shanghai',
        'JOBS': [
            {
                'id': 'seed_price_crawler',
                'func': 'tasks.crawl_seed_prices',
                'trigger': 'cron',
                'hour': 6,
                'minute': 0,
                'args': ['全国']
            },
            {
                'id': 'weather_data_crawler',
                'func': 'tasks.crawl_weather_data',
                'trigger': 'cron',
                'hour': '*/4',  # 每4小时执行一次
                'minute': 0,
                'args': ['全国']
            },
            {
                'id': 'farm_machine_crawler',
                'func': 'tasks.crawl_farm_machine_data',
                'trigger': 'cron',
                'hour': 8,
                'minute': 0,
                'args': ['全国']
            }
        ]
    }
    
    # 日志配置
    LOG_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': 'logs/agridec.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
    
    # 图表配置
    CHART_CONFIG = {
        'default_theme': 'agriculture',
        'default_width': 800,
        'default_height': 400,
        'themes': {
            'agriculture': {
                'colors': ['#52c41a', '#faad14', '#1890ff', '#f5222d', '#722ed1'],
                'backgroundColor': '#fafafa'
            },
            'green': {
                'colors': ['#52c41a', '#73d13d', '#95de64', '#b7eb8f', '#d9f7be'],
                'backgroundColor': '#f6ffed'
            },
            'blue': {
                'colors': ['#1890ff', '#40a9ff', '#69c0ff', '#91d5ff', '#bae7ff'],
                'backgroundColor': '#f0f8ff'
            }
        }
    }
    
    # API配置
    API_CONFIG = {
        'rate_limit': '1000 per hour',
        'pagination': {
            'default_page_size': 20,
            'max_page_size': 100
        }
    }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False
    
    # 开发环境使用SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///agridec_dev.db'
    
    # 降低爬虫频率限制
    CRAWLER_CONFIG = Config.CRAWLER_CONFIG.copy()
    CRAWLER_CONFIG.update({
        'default_delay': 1000,
        'max_pages': 5
    })

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    
    # 测试数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # 禁用CSRF保护
    WTF_CSRF_ENABLED = False
    
    # 测试环境不启用任务调度
    SCHEDULER_CONFIG = {'SCHEDULER_API_ENABLED': False}

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    
    # 生产环境安全配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 更严格的爬虫配置
    CRAWLER_CONFIG = Config.CRAWLER_CONFIG.copy()
    CRAWLER_CONFIG.update({
        'default_delay': 3000,
        'max_pages': 20,
        'respect_robots_txt': True
    })

# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """获取当前配置"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

-- AgriDec MySQL数据库结构创建脚本
-- 用于从SQLite迁移到MySQL生产环境

-- 使用AgriDec数据库
USE agridec;

-- 删除已存在的表（如果存在）
DROP TABLE IF EXISTS farm_machines;
DROP TABLE IF EXISTS weather_data;
DROP TABLE IF EXISTS seed_prices;

-- 创建种子价格表
CREATE TABLE seed_prices (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    product_name VARCHAR(100) NOT NULL COMMENT '产品名称',
    variety VARCHAR(100) COMMENT '品种',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    unit VARCHAR(20) COMMENT '单位',
    region VARCHAR(50) COMMENT '地区',
    date DATE NOT NULL COMMENT '日期',
    source_url VARCHAR(500) COMMENT '数据源URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引优化
    INDEX idx_region (region),
    INDEX idx_date (date),
    INDEX idx_product (product_name),
    INDEX idx_region_date (region, date),
    INDEX idx_price (price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='种子价格数据表';

-- 创建天气数据表
CREATE TABLE weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    region VARCHAR(50) NOT NULL COMMENT '地区',
    date DATE NOT NULL COMMENT '日期',
    temperature DECIMAL(5,2) COMMENT '温度(摄氏度)',
    weather VARCHAR(50) COMMENT '天气状况',
    humidity DECIMAL(5,2) COMMENT '湿度(%)',
    wind_speed DECIMAL(5,2) COMMENT '风速(m/s)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引优化
    INDEX idx_region_date (region, date),
    INDEX idx_date (date),
    INDEX idx_region (region),
    INDEX idx_temperature (temperature),
    
    -- 唯一约束：同一地区同一天只能有一条记录
    UNIQUE KEY uk_region_date (region, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='天气数据表';

-- 创建农机设备表
CREATE TABLE farm_machines (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    product_name VARCHAR(200) NOT NULL COMMENT '产品名称',
    brand VARCHAR(100) COMMENT '品牌',
    model VARCHAR(100) COMMENT '型号',
    price DECIMAL(12,2) COMMENT '价格(元)',
    specifications TEXT COMMENT '规格参数',
    region VARCHAR(50) COMMENT '地区',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引优化
    INDEX idx_brand (brand),
    INDEX idx_region (region),
    INDEX idx_product (product_name),
    INDEX idx_price (price),
    INDEX idx_brand_model (brand, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='农机设备数据表';

-- 创建系统配置表（新增）
CREATE TABLE system_config (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    config_type ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string' COMMENT '配置类型',
    description VARCHAR(500) COMMENT '配置描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_config_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 创建数据采集日志表（新增）
CREATE TABLE crawl_logs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    website VARCHAR(50) NOT NULL COMMENT '网站名称',
    data_type VARCHAR(50) NOT NULL COMMENT '数据类型',
    status ENUM('success', 'failed', 'partial') NOT NULL COMMENT '采集状态',
    records_count INT DEFAULT 0 COMMENT '采集记录数',
    error_message TEXT COMMENT '错误信息',
    execution_time INT COMMENT '执行时间(毫秒)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    INDEX idx_website (website),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数据采集日志表';

-- 插入默认系统配置
INSERT INTO system_config (config_key, config_value, config_type, description) VALUES
('crawler_delay_min', '1', 'number', '爬虫请求最小延迟(秒)'),
('crawler_delay_max', '3', 'number', '爬虫请求最大延迟(秒)'),
('crawler_timeout', '30', 'number', '爬虫请求超时时间(秒)'),
('crawler_max_retries', '3', 'number', '爬虫最大重试次数'),
('data_retention_days', '365', 'number', '数据保留天数'),
('enable_auto_cleanup', 'true', 'boolean', '启用自动数据清理'),
('system_name', 'AgriDec', 'string', '系统名称'),
('system_version', '1.0.0', 'string', '系统版本');

-- 创建视图：最新种子价格
CREATE VIEW v_latest_seed_prices AS
SELECT 
    sp.*,
    ROW_NUMBER() OVER (PARTITION BY sp.product_name, sp.region ORDER BY sp.date DESC) as rn
FROM seed_prices sp
WHERE sp.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);

-- 创建视图：7天天气预报
CREATE VIEW v_weather_forecast AS
SELECT 
    wd.*
FROM weather_data wd
WHERE wd.date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY wd.region, wd.date;

-- 创建视图：农机价格统计
CREATE VIEW v_machine_price_stats AS
SELECT 
    brand,
    COUNT(*) as machine_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM farm_machines 
WHERE price > 0
GROUP BY brand
ORDER BY avg_price DESC;

-- 显示创建结果
SHOW TABLES;

-- 显示表结构
DESCRIBE seed_prices;
DESCRIBE weather_data;
DESCRIBE farm_machines;
DESCRIBE system_config;
DESCRIBE crawl_logs;

-- 创建用户认证相关表
-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(80) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(120) NOT NULL UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(128) NOT NULL COMMENT '密码哈希',
    real_name VARCHAR(100) COMMENT '真实姓名',
    phone VARCHAR(20) COMMENT '手机号码',
    region VARCHAR(50) COMMENT '所在地区',
    farm_type VARCHAR(50) COMMENT '农场类型',
    farm_size DECIMAL(10,2) COMMENT '农场规模（亩）',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_admin BOOLEAN DEFAULT FALSE COMMENT '是否管理员',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    last_login TIMESTAMP NULL COMMENT '最后登录时间',
    login_count INT DEFAULT 0 COMMENT '登录次数',

    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 用户偏好设置表
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '偏好ID',
    user_id INT NOT NULL COMMENT '用户ID',
    `key` VARCHAR(100) NOT NULL COMMENT '偏好键',
    value TEXT COMMENT '偏好值',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_preference (user_id, `key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户偏好设置表';

-- 用户会话表
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '会话ID',
    user_id INT NOT NULL COMMENT '用户ID',
    session_token VARCHAR(255) NOT NULL UNIQUE COMMENT '会话令牌',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    expires_at TIMESTAMP NOT NULL COMMENT '过期时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户会话表';

-- 插入默认管理员用户
INSERT IGNORE INTO users (username, email, password_hash, real_name, region, is_admin) VALUES
('admin', 'admin@agridec.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXwtO5S5EM.S', '系统管理员', '全国', TRUE);

-- 显示视图
SHOW FULL TABLES WHERE Table_type = 'VIEW';

SELECT 'MySQL数据库结构创建完成！' as status;

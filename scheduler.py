# -*- coding: utf-8 -*-
"""
AgriDec 定时任务调度器
自动执行数据采集和系统维护任务
"""

import schedule
import time
import threading
from datetime import datetime
import logging
import os
from data_crawler.crawler_manager import CrawlerManager

# 确保日志目录存在
os.makedirs('logs', exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        self.crawler_manager = CrawlerManager()
        self.is_running = False
        self.scheduler_thread = None
        
    def start(self):
        """启动调度器"""
        if self.is_running:
            logger.warning("调度器已经在运行中")
            return
            
        logger.info("启动定时任务调度器...")
        self.is_running = True
        
        # 配置定时任务
        self._setup_schedules()
        
        # 在单独线程中运行调度器
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("定时任务调度器启动成功")
    
    def stop(self):
        """停止调度器"""
        logger.info("停止定时任务调度器...")
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        schedule.clear()
        logger.info("定时任务调度器已停止")
    
    def _setup_schedules(self):
        """配置定时任务"""
        
        # 每天早上6点采集种子价格数据
        schedule.every().day.at("06:00").do(
            self._safe_execute, 
            self._collect_seed_data,
            "种子价格数据采集"
        )
        
        # 每天早上7点采集天气数据
        schedule.every().day.at("07:00").do(
            self._safe_execute,
            self._collect_weather_data,
            "天气数据采集"
        )
        
        # 每天早上8点采集农机数据
        schedule.every().day.at("08:00").do(
            self._safe_execute,
            self._collect_machine_data,
            "农机数据采集"
        )
        
        # 每小时执行一次系统健康检查
        schedule.every().hour.do(
            self._safe_execute,
            self._system_health_check,
            "系统健康检查"
        )
        
        # 每周日凌晨2点执行数据库清理
        schedule.every().sunday.at("02:00").do(
            self._safe_execute,
            self._database_cleanup,
            "数据库清理"
        )
        
        # 每月1号生成月度报告
        schedule.every().day.at("01:00").do(
            self._safe_execute,
            self._check_monthly_report,
            "月度报告检查"
        )
        
        logger.info("定时任务配置完成")
    
    def _run_scheduler(self):
        """运行调度器主循环"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.error(f"调度器运行异常: {str(e)}")
                time.sleep(60)
    
    def _safe_execute(self, task_func, task_name):
        """安全执行任务，包含异常处理"""
        try:
            logger.info(f"开始执行任务: {task_name}")
            start_time = datetime.now()
            
            task_func()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"任务 {task_name} 执行成功，耗时: {duration:.2f}秒")
            
        except Exception as e:
            logger.error(f"任务 {task_name} 执行失败: {str(e)}")
    
    def _collect_seed_data(self):
        """采集种子价格数据"""
        try:
            result = self.crawler_manager.crawl_data(
                website='seed_trade',
                data_type='price',
                region='全国',
                max_pages=5
            )
            logger.info(f"种子数据采集完成，获取 {result.get('total_records', 0)} 条记录")
        except Exception as e:
            logger.error(f"种子数据采集失败: {str(e)}")
    
    def _collect_weather_data(self):
        """采集天气数据"""
        try:
            result = self.crawler_manager.crawl_data(
                website='weather',
                data_type='weather_forecast',
                region='全国',
                max_pages=3
            )
            logger.info(f"天气数据采集完成，获取 {result.get('total_records', 0)} 条记录")
        except Exception as e:
            logger.error(f"天气数据采集失败: {str(e)}")
    
    def _collect_machine_data(self):
        """采集农机数据"""
        try:
            result = self.crawler_manager.crawl_data(
                website='farm_machine',
                data_type='product_info',
                region='全国',
                max_pages=3
            )
            logger.info(f"农机数据采集完成，获取 {result.get('total_records', 0)} 条记录")
        except Exception as e:
            logger.error(f"农机数据采集失败: {str(e)}")
    
    def _system_health_check(self):
        """系统健康检查"""
        try:
            from app import app
            from database import db
            from sqlalchemy import text

            with app.app_context():
                # 检查数据库连接
                db.session.execute(text('SELECT 1'))

                # 检查数据表记录数
                from auth.models import SeedPrice, WeatherData, FarmMachine
                seed_count = SeedPrice.query.count()
                weather_count = WeatherData.query.count()
                machine_count = FarmMachine.query.count()

                logger.info(f"系统健康检查完成 - 种子数据: {seed_count}, 天气数据: {weather_count}, 农机数据: {machine_count}")

        except Exception as e:
            logger.error(f"系统健康检查失败: {str(e)}")
    
    def _database_cleanup(self):
        """数据库清理"""
        try:
            from app import app
            from database import db
            from datetime import datetime, timedelta

            with app.app_context():
                # 删除30天前的过期数据
                cutoff_date = datetime.now() - timedelta(days=30)

                from auth.models import SeedPrice, WeatherData

                # 清理过期的种子价格数据
                old_seeds = SeedPrice.query.filter(SeedPrice.date < cutoff_date.date()).count()
                SeedPrice.query.filter(SeedPrice.date < cutoff_date.date()).delete()

                # 清理过期的天气数据
                old_weather = WeatherData.query.filter(WeatherData.date < cutoff_date.date()).count()
                WeatherData.query.filter(WeatherData.date < cutoff_date.date()).delete()

                db.session.commit()

                logger.info(f"数据库清理完成 - 清理种子数据: {old_seeds}, 天气数据: {old_weather}")

        except Exception as e:
            logger.error(f"数据库清理失败: {str(e)}")
    
    def _check_monthly_report(self):
        """检查是否需要生成月度报告"""
        try:
            now = datetime.now()
            # 只在每月1号执行
            if now.day == 1:
                self._generate_monthly_report()
        except Exception as e:
            logger.error(f"月度报告检查失败: {str(e)}")

    def _generate_monthly_report(self):
        """生成月度报告"""
        try:
            from app import app
            from database import db
            from datetime import datetime, timedelta
            import json
            import os

            with app.app_context():
                # 获取上个月的数据统计
                now = datetime.now()
                last_month = now.replace(day=1) - timedelta(days=1)
                month_start = last_month.replace(day=1)

                from auth.models import SeedPrice, WeatherData, FarmMachine

                # 统计数据
                seed_count = SeedPrice.query.filter(
                    SeedPrice.date >= month_start.date(),
                    SeedPrice.date <= last_month.date()
                ).count()

                weather_count = WeatherData.query.filter(
                    WeatherData.date >= month_start.date(),
                    WeatherData.date <= last_month.date()
                ).count()

                machine_count = FarmMachine.query.count()

                # 生成报告
                report = {
                    'month': last_month.strftime('%Y-%m'),
                    'generated_at': now.isoformat(),
                    'data_summary': {
                        'seed_records': seed_count,
                        'weather_records': weather_count,
                        'machine_records': machine_count
                    },
                    'system_status': 'healthy'
                }

                # 保存报告
                os.makedirs('reports', exist_ok=True)
                report_file = f"reports/monthly_report_{last_month.strftime('%Y_%m')}.json"
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)

                logger.info(f"月度报告生成完成: {report_file}")

        except Exception as e:
            logger.error(f"月度报告生成失败: {str(e)}")
    
    def get_status(self):
        """获取调度器状态"""
        return {
            'is_running': self.is_running,
            'scheduled_jobs': len(schedule.jobs),
            'next_run': str(schedule.next_run()) if schedule.jobs else None
        }

# 全局调度器实例
scheduler = TaskScheduler()

def start_scheduler():
    """启动调度器"""
    scheduler.start()

def stop_scheduler():
    """停止调度器"""
    scheduler.stop()

def get_scheduler_status():
    """获取调度器状态"""
    return scheduler.get_status()

if __name__ == '__main__':
    # 直接运行时启动调度器
    import os
    os.makedirs('logs', exist_ok=True)
    
    try:
        start_scheduler()
        logger.info("调度器已启动，按 Ctrl+C 停止")
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("接收到停止信号")
        stop_scheduler()
        logger.info("调度器已停止")

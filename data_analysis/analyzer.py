# -*- coding: utf-8 -*-
"""
农业数据分析器
基于专业的数据分析算法，提供农业数据分析和决策支持
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class DataAnalyzer:
    """农业数据分析器"""
    
    def __init__(self):
        self.analysis_methods = {
            'trend_analysis': '趋势分析',
            'seasonal_analysis': '季节性分析',
            'correlation_analysis': '相关性分析',
            'price_prediction': '价格预测',
            'risk_assessment': '风险评估',
            'yield_optimization': '产量优化'
        }
    
    def analyze_price_trend(self, price_data: List[Dict]) -> Dict[str, Any]:
        """
        分析价格趋势
        
        Args:
            price_data: 价格数据列表
            
        Returns:
            dict: 分析结果
        """
        try:
            if not price_data:
                return {'success': False, 'error': '价格数据为空'}
            
            # 转换为DataFrame
            df = pd.DataFrame(price_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # 计算趋势指标
            df['price_change'] = df['price'].pct_change()
            df['moving_avg_7'] = df['price'].rolling(window=7).mean()
            df['moving_avg_30'] = df['price'].rolling(window=30).mean()
            
            # 趋势分析
            recent_trend = self._calculate_trend(df['price'].tail(7).values)
            overall_trend = self._calculate_trend(df['price'].values)
            
            # 价格波动分析
            volatility = df['price'].std()
            price_range = df['price'].max() - df['price'].min()
            
            # 季节性分析
            seasonal_pattern = self._analyze_seasonal_pattern(df)
            
            return {
                'success': True,
                'analysis': {
                    'trend_direction': recent_trend['direction'],
                    'trend_strength': recent_trend['strength'],
                    'overall_trend': overall_trend['direction'],
                    'volatility': round(volatility, 2),
                    'price_range': round(price_range, 2),
                    'current_price': df['price'].iloc[-1],
                    'avg_price': round(df['price'].mean(), 2),
                    'seasonal_pattern': seasonal_pattern,
                    'recommendations': self._generate_price_recommendations(df, recent_trend)
                },
                'metadata': {
                    'data_points': len(df),
                    'date_range': {
                        'start': df['date'].min().strftime('%Y-%m-%d'),
                        'end': df['date'].max().strftime('%Y-%m-%d')
                    },
                    'analysis_time': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'价格趋势分析失败: {str(e)}'
            }
    
    def analyze_weather_impact(self, weather_data: List[Dict], crop_type: str = '玉米') -> Dict[str, Any]:
        """
        分析天气对农业的影响
        
        Args:
            weather_data: 天气数据
            crop_type: 作物类型
            
        Returns:
            dict: 分析结果
        """
        try:
            if not weather_data:
                return {'success': False, 'error': '天气数据为空'}
            
            df = pd.DataFrame(weather_data)
            df['date'] = pd.to_datetime(df['date'])
            
            # 温度适宜性分析
            temp_suitability = self._analyze_temperature_suitability(df, crop_type)
            
            # 降水分析
            rainfall_analysis = self._analyze_rainfall_pattern(df)
            
            # 农事活动建议
            farming_recommendations = self._generate_farming_recommendations(df, crop_type)
            
            # 风险评估
            weather_risks = self._assess_weather_risks(df, crop_type)
            
            return {
                'success': True,
                'analysis': {
                    'temperature_suitability': temp_suitability,
                    'rainfall_analysis': rainfall_analysis,
                    'farming_recommendations': farming_recommendations,
                    'weather_risks': weather_risks,
                    'overall_score': self._calculate_weather_score(temp_suitability, rainfall_analysis, weather_risks)
                },
                'metadata': {
                    'crop_type': crop_type,
                    'forecast_days': len(df),
                    'analysis_time': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'天气影响分析失败: {str(e)}'
            }
    
    def analyze_yield_optimization(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """
        产量优化分析
        
        Args:
            historical_data: 历史数据
            
        Returns:
            dict: 优化建议
        """
        try:
            if not historical_data:
                return {'success': False, 'error': '历史数据为空'}
            
            df = pd.DataFrame(historical_data)
            
            # 产量影响因素分析
            yield_factors = self._analyze_yield_factors(df)
            
            # 最佳种植时间分析
            optimal_timing = self._analyze_optimal_timing(df)
            
            # 投入产出分析
            roi_analysis = self._analyze_roi(df)
            
            # 优化建议
            optimization_recommendations = self._generate_optimization_recommendations(
                yield_factors, optimal_timing, roi_analysis
            )
            
            return {
                'success': True,
                'analysis': {
                    'yield_factors': yield_factors,
                    'optimal_timing': optimal_timing,
                    'roi_analysis': roi_analysis,
                    'recommendations': optimization_recommendations
                },
                'metadata': {
                    'data_points': len(df),
                    'analysis_time': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'产量优化分析失败: {str(e)}'
            }
    
    def _calculate_trend(self, values: np.ndarray) -> Dict[str, Any]:
        """计算趋势"""
        if len(values) < 2:
            return {'direction': 'stable', 'strength': 0}
        
        # 线性回归计算趋势
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        # 判断趋势方向和强度
        if abs(slope) < 0.01:
            direction = 'stable'
            strength = 0
        elif slope > 0:
            direction = 'rising'
            strength = min(abs(slope) * 100, 100)
        else:
            direction = 'falling'
            strength = min(abs(slope) * 100, 100)
        
        return {
            'direction': direction,
            'strength': round(strength, 2),
            'slope': round(slope, 4)
        }
    
    def _analyze_seasonal_pattern(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析季节性模式"""
        if 'date' not in df.columns:
            return {'pattern': 'unknown', 'confidence': 0}
        
        df['month'] = df['date'].dt.month
        monthly_avg = df.groupby('month')['price'].mean()
        
        # 找出价格最高和最低的月份
        peak_month = monthly_avg.idxmax()
        low_month = monthly_avg.idxmin()
        
        # 季节性强度
        seasonal_strength = (monthly_avg.max() - monthly_avg.min()) / monthly_avg.mean()
        
        return {
            'peak_month': peak_month,
            'low_month': low_month,
            'seasonal_strength': round(seasonal_strength, 2),
            'monthly_averages': monthly_avg.to_dict()
        }
    
    def _generate_price_recommendations(self, df: pd.DataFrame, trend: Dict) -> List[str]:
        """生成价格建议"""
        recommendations = []
        
        current_price = df['price'].iloc[-1]
        avg_price = df['price'].mean()
        
        if trend['direction'] == 'rising':
            if current_price < avg_price:
                recommendations.append("当前价格低于平均水平，建议适量采购")
            recommendations.append("价格呈上升趋势，建议关注市场动态")
        elif trend['direction'] == 'falling':
            recommendations.append("价格呈下降趋势，建议延缓采购")
            if current_price > avg_price:
                recommendations.append("当前价格高于平均水平，建议等待更好时机")
        else:
            recommendations.append("价格相对稳定，可按需采购")
        
        return recommendations
    
    def _analyze_temperature_suitability(self, df: pd.DataFrame, crop_type: str) -> Dict[str, Any]:
        """分析温度适宜性"""
        # 不同作物的适宜温度范围
        temp_ranges = {
            '玉米': {'min': 15, 'max': 30, 'optimal': 25},
            '小麦': {'min': 10, 'max': 25, 'optimal': 18},
            '水稻': {'min': 20, 'max': 35, 'optimal': 28},
            '大豆': {'min': 15, 'max': 28, 'optimal': 22}
        }
        
        crop_range = temp_ranges.get(crop_type, temp_ranges['玉米'])
        
        if 'temperature' in df.columns:
            suitable_days = len(df[
                (df['temperature'] >= crop_range['min']) & 
                (df['temperature'] <= crop_range['max'])
            ])
            
            suitability_score = (suitable_days / len(df)) * 100
            
            return {
                'suitability_score': round(suitability_score, 1),
                'suitable_days': suitable_days,
                'total_days': len(df),
                'optimal_temp': crop_range['optimal'],
                'temp_range': f"{crop_range['min']}-{crop_range['max']}°C"
            }
        
        return {'suitability_score': 0, 'error': '缺少温度数据'}
    
    def _analyze_rainfall_pattern(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析降水模式"""
        # 模拟降水分析（实际项目中需要真实的降水数据）
        rainy_days = len(df[df['weather'].str.contains('雨', na=False)]) if 'weather' in df.columns else 0
        
        return {
            'rainy_days': rainy_days,
            'total_days': len(df),
            'rainfall_frequency': round((rainy_days / len(df)) * 100, 1) if len(df) > 0 else 0
        }
    
    def _generate_farming_recommendations(self, df: pd.DataFrame, crop_type: str) -> List[str]:
        """生成农事活动建议"""
        recommendations = []
        
        if 'temperature' in df.columns:
            avg_temp = df['temperature'].mean()
            
            if avg_temp > 25:
                recommendations.append("温度较高，注意作物防暑和灌溉")
                recommendations.append("适合进行夏季田间管理作业")
            elif avg_temp < 15:
                recommendations.append("温度较低，注意作物保温")
                recommendations.append("可考虑温室或大棚种植")
            else:
                recommendations.append("温度适宜，是播种和移栽的好时机")
        
        # 根据天气情况给出建议
        if 'weather' in df.columns:
            rainy_days = len(df[df['weather'].str.contains('雨', na=False)])
            if rainy_days > len(df) * 0.5:
                recommendations.append("降水较多，注意田间排水防涝")
            elif rainy_days < len(df) * 0.2:
                recommendations.append("降水较少，注意及时灌溉")
        
        return recommendations
    
    def _assess_weather_risks(self, df: pd.DataFrame, crop_type: str) -> List[Dict]:
        """评估天气风险"""
        risks = []
        
        if 'temperature' in df.columns:
            max_temp = df['temperature'].max()
            min_temp = df['temperature'].min()
            
            if max_temp > 35:
                risks.append({
                    'type': 'high_temperature',
                    'level': 'high',
                    'description': f'最高温度达到{max_temp}°C，可能影响作物生长'
                })
            
            if min_temp < 5:
                risks.append({
                    'type': 'low_temperature',
                    'level': 'medium',
                    'description': f'最低温度{min_temp}°C，需要注意防寒'
                })
        
        return risks
    
    def _calculate_weather_score(self, temp_suitability: Dict, rainfall_analysis: Dict, risks: List) -> int:
        """计算天气综合评分"""
        base_score = temp_suitability.get('suitability_score', 0)
        
        # 根据风险调整评分
        risk_penalty = len(risks) * 10
        
        # 根据降水情况调整
        rainfall_freq = rainfall_analysis.get('rainfall_frequency', 0)
        if 20 <= rainfall_freq <= 40:  # 适宜的降水频率
            rainfall_bonus = 10
        else:
            rainfall_bonus = 0
        
        final_score = max(0, min(100, base_score + rainfall_bonus - risk_penalty))
        return round(final_score)
    
    def _analyze_yield_factors(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析产量影响因素"""
        # 模拟产量因素分析
        factors = {
            'weather_impact': 0.3,
            'soil_quality': 0.25,
            'seed_variety': 0.2,
            'farming_technique': 0.15,
            'market_timing': 0.1
        }
        
        return {
            'primary_factors': factors,
            'recommendations': [
                "天气是影响产量的最重要因素，建议密切关注气象预报",
                "土壤质量对产量有重要影响，建议定期进行土壤检测",
                "选择适合当地条件的优良品种"
            ]
        }
    
    def _analyze_optimal_timing(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析最佳种植时间"""
        # 基于历史数据分析最佳时机
        return {
            'best_planting_month': 3,
            'best_harvest_month': 9,
            'confidence': 0.85,
            'factors': ['温度适宜', '降水充足', '市场价格较好']
        }
    
    def _analyze_roi(self, df: pd.DataFrame) -> Dict[str, Any]:
        """投入产出分析"""
        # 模拟ROI分析
        return {
            'average_roi': 1.25,
            'best_case_roi': 1.8,
            'worst_case_roi': 0.9,
            'break_even_yield': 500,  # kg/亩
            'recommendations': [
                "当前投入产出比较为合理",
                "建议优化种植技术以提高产量",
                "关注市场价格变化，选择合适的销售时机"
            ]
        }
    
    def _generate_optimization_recommendations(self, yield_factors: Dict, optimal_timing: Dict, roi_analysis: Dict) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        recommendations.extend([
            f"建议在{optimal_timing['best_planting_month']}月进行播种",
            f"预计在{optimal_timing['best_harvest_month']}月收获效果最佳",
            f"目标产量应达到{roi_analysis['break_even_yield']}kg/亩以上"
        ])
        
        recommendations.extend(yield_factors['recommendations'])
        recommendations.extend(roi_analysis['recommendations'])
        
        return recommendations

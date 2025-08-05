# -*- coding: utf-8 -*-
"""
农业数据可视化图表生成器
基于专业图表技术，生成ECharts配置
"""

import json
from datetime import datetime, timedelta

class ChartGenerator:
    """农业数据可视化图表生成器"""
    
    def __init__(self):
        self.supported_chart_types = {
            'price_trend': '价格趋势图',
            'weather_forecast': '天气预报图',
            'yield_analysis': '产量分析图',
            'seasonal_comparison': '季节对比图',
            'regional_comparison': '地区对比图',
            'china_map': '中国地图可视化',
            'enhanced_pie': '增强饼图',
            'multi_series_line': '多系列折线图',
            # 新增替代可视化方案
            'regional_bar': '地区柱状图',
            'regional_pie': '地区饼图',
            'regional_line': '地区趋势图',
            'regional_scatter': '地区散点图'
        }
        
        self.chart_themes = {
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
    
    def generate_chart(self, chart_type, data, options=None):
        """
        生成农业图表配置
        
        Args:
            chart_type: 图表类型
            data: 图表数据
            options: 图表选项
        
        Returns:
            dict: 图表配置结果
        """
        try:
            if chart_type not in self.supported_chart_types:
                return {
                    'success': False,
                    'error': f'不支持的图表类型: {chart_type}'
                }
            
            if not data or len(data) == 0:
                return {
                    'success': False,
                    'error': '图表数据不能为空'
                }
            
            # 准备图表参数
            chart_params = self._prepare_chart_params(chart_type, data, options)
            
            # 生成图表配置
            result = self._generate_chart_configuration(chart_params)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'图表生成失败: {str(e)}'
            }
    
    def _prepare_chart_params(self, chart_type, data, options):
        """准备图表参数"""
        params = {
            'chart_type': chart_type,
            'data': data,
            'title': options.get('title', self.supported_chart_types[chart_type]) if options else self.supported_chart_types[chart_type],
            'theme': options.get('theme', 'agriculture') if options else 'agriculture',
            'width': options.get('width', 800) if options else 800,
            'height': options.get('height', 400) if options else 400,
            'responsive': options.get('responsive', True) if options else True,
            'export_format': 'both'  # 同时返回JSON和HTML
        }
        
        # 添加农时标注
        if options and 'annotations' in options:
            params['annotations'] = options['annotations']
        else:
            params['annotations'] = self._get_default_annotations(chart_type)
        
        return params
    
    def _get_default_annotations(self, chart_type):
        """获取默认农时标注"""
        current_month = datetime.now().month
        
        annotations = []
        
        if chart_type == 'price_trend':
            # 价格趋势图的农时标注
            farming_seasons = [
                {'date': '03', 'event': '春播期', 'type': 'farming_season'},
                {'date': '06', 'event': '夏管期', 'type': 'farming_season'},
                {'date': '09', 'event': '秋收期', 'type': 'farming_season'},
                {'date': '12', 'event': '冬储期', 'type': 'farming_season'}
            ]
            
            for season in farming_seasons:
                if int(season['date']) >= current_month:
                    annotations.append({
                        'date': f'2024-{season["date"]}',
                        'event': season['event'],
                        'type': season['type']
                    })
                    break
        
        return annotations
    
    def _generate_chart_configuration(self, params):
        """
        生成农业图表配置
        使用标准Python实现，无需外部工具依赖
        """
        
        chart_config = self._generate_chart_config(params)
        
        return {
            'success': True,
            'data': {
                'chart_config': chart_config,
                'chart_html': f'<div id="agri-chart" style="width:{params["width"]}px;height:{params["height"]}px;"></div>',
                'chart_script': self._generate_chart_script(chart_config),
                'metadata': {
                    'chart_type': params['chart_type'],
                    'data_points': len(params['data']),
                    'generation_time': datetime.now().isoformat(),
                    'theme': params['theme'],
                    'responsive': params['responsive']
                }
            }
        }
    
    def _generate_chart_config(self, params):
        """生成ECharts配置"""
        chart_type = params['chart_type']
        data = params['data']
        theme = self.chart_themes.get(params['theme'], self.chart_themes['agriculture'])
        
        if chart_type == 'price_trend':
            return self._generate_price_trend_config(data, params, theme)
        elif chart_type == 'weather_forecast':
            return self._generate_weather_forecast_config(data, params, theme)
        elif chart_type == 'yield_analysis':
            return self._generate_yield_analysis_config(data, params, theme)
        elif chart_type == 'seasonal_comparison':
            return self._generate_seasonal_comparison_config(data, params, theme)
        elif chart_type == 'regional_comparison':
            return self._generate_regional_comparison_config(data, params, theme)
        elif chart_type == 'china_map':
            return self._generate_china_map_config(data, params, theme)
        elif chart_type == 'enhanced_pie':
            return self._generate_enhanced_pie_config(data, params, theme)
        elif chart_type == 'multi_series_line':
            return self._generate_multi_series_line_config(data, params, theme)
        elif chart_type == 'regional_bar':
            return self._generate_regional_bar_config(data, params, theme)
        elif chart_type == 'regional_pie':
            return self._generate_regional_pie_config(data, params, theme)
        elif chart_type == 'regional_line':
            return self._generate_regional_line_config(data, params, theme)
        elif chart_type == 'regional_scatter':
            return self._generate_regional_scatter_config(data, params, theme)
        else:
            # 如果地图显示有问题，自动回退到柱状图
            if chart_type == 'china_map':
                print("⚠️ 地图显示可能有问题，自动切换到地区柱状图")
                return self._generate_regional_bar_config(data, params, theme)
            raise ValueError(f'不支持的图表类型: {chart_type}')
    
    def _generate_price_trend_config(self, data, params, theme):
        """生成价格趋势图配置"""
        dates = [item.get('date', '') for item in data]
        prices = [item.get('price', 0) for item in data]
        product_name = data[0].get('product_name', '农产品') if data else '农产品'
        
        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {
                    'fontSize': 18,
                    'fontWeight': 'bold',
                    'color': '#333'
                }
            },
            'tooltip': {
                'trigger': 'axis',
                'formatter': '{b}<br/>{a}: {c} 元/斤'
            },
            'legend': {
                'data': [product_name],
                'top': 30
            },
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': True
            },
            'toolbox': {
                'feature': {
                    'saveAsImage': {'title': '保存图片'},
                    'dataZoom': {'title': {'zoom': '区域缩放', 'back': '缩放还原'}}
                }
            },
            'xAxis': {
                'type': 'category',
                'boundaryGap': False,
                'data': dates,
                'name': '时间',
                'nameLocation': 'middle',
                'nameGap': 30
            },
            'yAxis': {
                'type': 'value',
                'name': '价格(元/斤)',
                'nameLocation': 'middle',
                'nameGap': 50
            },
            'series': [{
                'name': product_name,
                'type': 'line',
                'data': prices,
                'smooth': True,
                'itemStyle': {'color': theme['colors'][0]},
                'areaStyle': {'opacity': 0.3}
            }],
            'color': theme['colors'],
            'backgroundColor': theme['backgroundColor']
        }
    
    def _generate_weather_forecast_config(self, data, params, theme):
        """生成天气预报图配置"""
        dates = [item.get('date', '') for item in data]
        temperatures = [item.get('temperature', 0) for item in data]
        weather_conditions = [item.get('weather', '晴') for item in data]

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {'fontSize': 18, 'fontWeight': 'bold', 'color': '#333'}
            },
            'tooltip': {
                'trigger': 'axis',
                'formatter': '{b}<br/>温度: {c}°C<br/>天气: ' + str(weather_conditions[0] if weather_conditions else '晴')
            },
            'legend': {
                'data': ['温度'],
                'top': 30
            },
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': True
            },
            'xAxis': {
                'type': 'category',
                'data': dates,
                'name': '日期',
                'nameLocation': 'middle',
                'nameGap': 30
            },
            'yAxis': {
                'type': 'value',
                'name': '温度(°C)',
                'nameLocation': 'middle',
                'nameGap': 50
            },
            'series': [{
                'name': '温度',
                'type': 'line',
                'data': temperatures,
                'smooth': True,
                'itemStyle': {'color': theme['colors'][1]},
                'lineStyle': {'width': 3},
                'symbol': 'circle',
                'symbolSize': 8,
                'markPoint': {
                    'data': [
                        {'type': 'max', 'name': '最高温'},
                        {'type': 'min', 'name': '最低温'}
                    ]
                }
            }],
            'color': theme['colors'],
            'backgroundColor': theme['backgroundColor']
        }
    
    def _generate_yield_analysis_config(self, data, params, theme):
        """生成产量分析图配置"""
        categories = list(set([item.get('crop', '作物') for item in data]))
        years = list(set([item.get('year', '2024') for item in data]))
        
        series = []
        for crop in categories:
            crop_data = [item.get('yield', 0) for item in data if item.get('crop') == crop]
            series.append({
                'name': crop,
                'type': 'bar',
                'data': crop_data
            })
        
        return {
            'title': {
                'text': params['title'],
                'left': 'center'
            },
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {'type': 'shadow'}
            },
            'legend': {
                'data': categories,
                'top': 30
            },
            'xAxis': {
                'type': 'category',
                'data': years,
                'name': '年份'
            },
            'yAxis': {
                'type': 'value',
                'name': '产量(吨/亩)'
            },
            'series': series,
            'color': theme['colors'],
            'backgroundColor': theme['backgroundColor']
        }
    
    def _generate_seasonal_comparison_config(self, data, params, theme):
        """生成季节对比图配置"""
        months = [f'{item.get("month", i)}月' for i, item in enumerate(data, 1)]
        values = [item.get('value', 0) for item in data]

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {'fontSize': 18, 'fontWeight': 'bold', 'color': '#333'}
            },
            'tooltip': {
                'trigger': 'axis',
                'formatter': '{b}<br/>{a}: {c}'
            },
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': True
            },
            'xAxis': {
                'type': 'category',
                'data': months,
                'name': '月份',
                'nameLocation': 'middle',
                'nameGap': 30
            },
            'yAxis': {
                'type': 'value',
                'name': '数值',
                'nameLocation': 'middle',
                'nameGap': 50
            },
            'series': [{
                'name': '月度数据',
                'type': 'bar',
                'data': values,
                'itemStyle': {
                    'color': theme['colors'][0]
                },
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }],
            'color': theme['colors'],
            'backgroundColor': theme['backgroundColor']
        }
    
    def _generate_regional_comparison_config(self, data, params, theme):
        """生成地区对比图配置 - 增强版饼图"""
        pie_data = [{'value': item.get('value', 0), 'name': item.get('region', '地区')} for item in data]

        # 计算总值用于百分比显示
        total_value = sum(item['value'] for item in pie_data)

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {
                    'fontSize': 20,
                    'fontWeight': 'bold',
                    'color': '#333'
                },
                'subtextStyle': {
                    'fontSize': 14,
                    'color': '#666'
                }
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{a}<br/>{b}: {c} ({d}%)'
            },
            'legend': {
                'orient': 'vertical',
                'left': 'left',
                'top': 'middle',
                'textStyle': {
                    'fontSize': 12
                }
            },
            'series': [{
                'name': '地区数据',
                'type': 'pie',
                'radius': ['40%', '70%'],  # 环形饼图
                'center': ['60%', '50%'],
                'data': pie_data,
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 20,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                },
                'label': {
                    'show': True,
                    'formatter': '{b}\n{d}%',
                    'fontSize': 12,
                    'fontWeight': 'bold'
                },
                'labelLine': {
                    'show': True,
                    'length': 15,
                    'length2': 10
                },
                'animationType': 'scale',
                'animationEasing': 'elasticOut'
            }],
            'color': [
                '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
                '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
            ],
            'backgroundColor': theme['backgroundColor']
        }

    def _generate_china_map_config(self, data, params, theme):
        """生成中国地图可视化配置"""
        # 省份名称标准化映射 - 包含ECharts中国地图使用的标准名称
        province_mapping = {
            # 直辖市
            '北京': '北京', '天津': '天津', '上海': '上海', '重庆': '重庆',
            # 省份
            '山东': '山东', '河南': '河南', '河北': '河北', '江苏': '江苏', '安徽': '安徽',
            '湖北': '湖北', '四川': '四川', '广东': '广东', '湖南': '湖南', '浙江': '浙江',
            '山西': '山西', '辽宁': '辽宁', '吉林': '吉林', '黑龙江': '黑龙江', '江西': '江西',
            '福建': '福建', '海南': '海南', '贵州': '贵州', '云南': '云南', '陕西': '陕西',
            '甘肃': '甘肃', '青海': '青海', '台湾': '台湾',
            # 自治区
            '广西': '广西', '内蒙古': '内蒙古', '西藏': '西藏', '宁夏': '宁夏', '新疆': '新疆',
            # 特别行政区
            '香港': '香港', '澳门': '澳门',
            # 常见别名映射
            '广西壮族自治区': '广西', '内蒙古自治区': '内蒙古', '西藏自治区': '西藏',
            '宁夏回族自治区': '宁夏', '新疆维吾尔自治区': '新疆',
            '香港特别行政区': '香港', '澳门特别行政区': '澳门'
        }

        # 数据验证和清洗函数
        def validate_and_clean_value(raw_value, default_value=0):
            """验证和清洗数值，确保返回有效数字"""
            try:
                # 处理None、空字符串等情况
                if raw_value is None or raw_value == '':
                    return default_value

                # 尝试转换为浮点数
                if isinstance(raw_value, (int, float)):
                    # 检查是否为NaN或无穷大
                    if str(raw_value).lower() in ['nan', 'inf', '-inf'] or raw_value != raw_value:
                        return default_value
                    return float(raw_value)

                # 处理字符串类型
                if isinstance(raw_value, str):
                    # 移除空白字符
                    clean_str = raw_value.strip()
                    if not clean_str:
                        return default_value

                    # 尝试转换为数字
                    try:
                        num_value = float(clean_str)
                        # 检查是否为NaN或无穷大
                        if str(num_value).lower() in ['nan', 'inf', '-inf'] or num_value != num_value:
                            return default_value
                        return num_value
                    except (ValueError, TypeError):
                        return default_value

                # 其他类型尝试转换
                return float(raw_value) if raw_value is not None else default_value

            except (ValueError, TypeError, OverflowError):
                return default_value

        # 将地区数据转换为地图数据格式
        map_data = []
        processed_regions = set()  # 记录已处理的省份

        # 获取所有标准省份名称
        all_provinces = set(province_mapping.values())

        # 创建省份数据字典，初始化所有省份为0
        province_data = {province: 0 for province in all_provinces}

        # 处理输入数据
        if data:
            for item in data:
                region_raw = item.get('region', '')
                if not region_raw:
                    continue

                # 移除省、市、自治区等后缀进行标准化
                region_clean = region_raw.replace('省', '').replace('市', '').replace('自治区', '').replace('特别行政区', '').replace('维吾尔', '').replace('壮族', '').replace('回族', '')

                # 使用映射表标准化名称
                region_name = province_mapping.get(region_clean, region_clean)

                # 如果标准化后的名称在我们的省份列表中，则更新数据
                if region_name in all_provinces:
                    # 验证和清洗数值
                    raw_value = item.get('value')
                    clean_value = validate_and_clean_value(raw_value, 0)
                    province_data[region_name] = clean_value
                    processed_regions.add(region_name)
                else:
                    # 如果不在标准列表中，尝试模糊匹配
                    for std_province in all_provinces:
                        if region_clean in std_province or std_province in region_clean:
                            raw_value = item.get('value')
                            clean_value = validate_and_clean_value(raw_value, 0)
                            province_data[std_province] = clean_value
                            processed_regions.add(std_province)
                            break

        # 将字典转换为ECharts需要的格式
        map_data = [{'name': province, 'value': value} for province, value in province_data.items()]

        # 计算数据范围 - 只使用有效数值
        valid_values = [item['value'] for item in map_data if isinstance(item['value'], (int, float)) and item['value'] == item['value']]  # 排除NaN

        if valid_values:
            max_value = max(valid_values)
            min_value = min(valid_values)
            # 确保范围合理
            if max_value == min_value:
                max_value = min_value + 100  # 避免范围为0
        else:
            # 如果没有有效数值，使用默认范围
            max_value = 1000
            min_value = 0

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'top': 20,
                'textStyle': {
                    'fontSize': 20,
                    'fontWeight': 'bold',
                    'color': '#333'
                }
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{b}<br/>农业产值: {c}万元',
                'backgroundColor': 'rgba(0,0,0,0.8)',
                'borderColor': '#ccc',
                'borderWidth': 1,
                'textStyle': {
                    'color': '#fff',
                    'fontSize': 14
                }
            },
            'visualMap': {
                'min': min_value,
                'max': max_value,
                'left': 20,
                'bottom': 20,
                'text': ['高', '低'],
                'calculable': True,
                'orient': 'vertical',
                'inRange': {
                    'color': ['#e0f3ff', '#a4d3ff', '#6bb6ff', '#3399ff', '#006edd']
                },
                'textStyle': {
                    'color': '#333'
                }
            },
            'geo': {
                'map': 'china',
                'roam': True,
                'scaleLimit': {
                    'min': 0.8,
                    'max': 3
                },
                'itemStyle': {
                    'borderColor': '#fff',
                    'borderWidth': 1
                },
                'emphasis': {
                    'itemStyle': {
                        'borderColor': '#389BB7',
                        'borderWidth': 2
                    }
                }
            },
            'series': [{
                'name': '农业数据',
                'type': 'map',
                'map': 'china',
                'geoIndex': 0,
                'data': map_data,
                'itemStyle': {
                    'borderColor': '#fff',
                    'borderWidth': 0.5
                },
                'emphasis': {
                    'itemStyle': {
                        'areaColor': '#389BB7',
                        'borderColor': '#fff',
                        'borderWidth': 2
                    },
                    'label': {
                        'show': True,
                        'color': '#fff',
                        'fontSize': 12,
                        'fontWeight': 'bold'
                    }
                },
                'select': {
                    'itemStyle': {
                        'areaColor': '#ff6b6b'
                    }
                }
            }],
            'backgroundColor': theme.get('backgroundColor', '#fff')
        }

    def _generate_enhanced_pie_config(self, data, params, theme):
        """生成增强版饼图配置"""
        pie_data = [{'value': item.get('value', 0), 'name': item.get('region', '地区')} for item in data]

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {
                    'fontSize': 20,
                    'fontWeight': 'bold',
                    'color': '#333'
                }
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{a}<br/>{b}: {c} ({d}%)'
            },
            'legend': {
                'type': 'scroll',
                'orient': 'vertical',
                'right': 10,
                'top': 20,
                'bottom': 20
            },
            'series': [{
                'name': '数据分布',
                'type': 'pie',
                'radius': ['30%', '80%'],
                'roseType': 'radius',  # 玫瑰图
                'data': pie_data,
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 20,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                },
                'animationType': 'scale',
                'animationEasing': 'elasticOut'
            }],
            'color': theme['colors'],
            'backgroundColor': theme['backgroundColor']
        }

    def _generate_multi_series_line_config(self, data, params, theme):
        """生成多系列折线图配置"""
        # 假设数据格式: [{'date': '2024-01', 'series1': 100, 'series2': 200}, ...]
        if not data:
            return {}

        dates = [item.get('date', '') for item in data]
        series_names = [key for key in data[0].keys() if key != 'date']

        series_list = []
        for i, series_name in enumerate(series_names):
            series_data = [item.get(series_name, 0) for item in data]
            series_list.append({
                'name': series_name,
                'type': 'line',
                'data': series_data,
                'smooth': True,
                'itemStyle': {'color': theme['colors'][i % len(theme['colors'])]},
                'lineStyle': {'width': 3}
            })

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {
                    'fontSize': 18,
                    'fontWeight': 'bold',
                    'color': '#333'
                }
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'legend': {
                'data': series_names,
                'top': 30
            },
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': True
            },
            'xAxis': {
                'type': 'category',
                'data': dates,
                'name': '时间'
            },
            'yAxis': {
                'type': 'value',
                'name': '数值'
            },
            'series': series_list,
            'color': theme['colors'],
            'backgroundColor': theme['backgroundColor']
        }

    def _generate_chart_script(self, chart_config):
        """生成图表脚本"""
        return f"""
var myChart = echarts.init(document.getElementById('agri-chart'));
var option = {json.dumps(chart_config, ensure_ascii=False, indent=2)};
myChart.setOption(option);

// 响应式处理
window.addEventListener('resize', function() {{
    myChart.resize();
}});
        """.strip()

    def _generate_regional_bar_config(self, data, params, theme):
        """生成地区柱状图配置（地图的替代方案）"""
        # 数据验证和清洗
        def validate_value(raw_value):
            try:
                if raw_value is None or raw_value == '':
                    return 0
                if isinstance(raw_value, str):
                    clean_str = raw_value.strip()
                    if not clean_str or clean_str.lower() in ['nan', 'null', 'undefined']:
                        return 0
                    return float(clean_str)
                return float(raw_value) if raw_value == raw_value else 0  # 排除NaN
            except (ValueError, TypeError):
                return 0

        # 处理数据
        regions = []
        values = []

        for item in data:
            region = item.get('region', '未知地区')
            value = validate_value(item.get('value'))
            regions.append(region)
            values.append(value)

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {'fontSize': 18, 'fontWeight': 'bold', 'color': '#333'}
            },
            'tooltip': {
                'trigger': 'axis',
                'formatter': '{b}<br/>农业产值: {c}万元'
            },
            'xAxis': {
                'type': 'category',
                'data': regions,
                'axisLabel': {'rotate': 45}
            },
            'yAxis': {
                'type': 'value',
                'name': '产值(万元)'
            },
            'series': [{
                'name': '农业产值',
                'type': 'bar',
                'data': values,
                'itemStyle': {
                    'color': theme['colors'][0]
                }
            }],
            'backgroundColor': theme['backgroundColor']
        }

    def _generate_regional_pie_config(self, data, params, theme):
        """生成地区饼图配置（地图的替代方案）"""
        # 数据验证和清洗
        def validate_value(raw_value):
            try:
                if raw_value is None or raw_value == '':
                    return 0
                if isinstance(raw_value, str):
                    clean_str = raw_value.strip()
                    if not clean_str or clean_str.lower() in ['nan', 'null', 'undefined']:
                        return 0
                    return float(clean_str)
                return float(raw_value) if raw_value == raw_value else 0
            except (ValueError, TypeError):
                return 0

        # 处理数据
        pie_data = []
        for item in data:
            region = item.get('region', '未知地区')
            value = validate_value(item.get('value'))
            if value > 0:  # 只显示有数值的地区
                pie_data.append({'name': region, 'value': value})

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {'fontSize': 18, 'fontWeight': 'bold', 'color': '#333'}
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{a}<br/>{b}: {c}万元 ({d}%)'
            },
            'legend': {
                'type': 'scroll',
                'orient': 'vertical',
                'right': 10,
                'top': 20,
                'bottom': 20
            },
            'series': [{
                'name': '农业产值',
                'type': 'pie',
                'radius': '50%',
                'data': pie_data,
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }],
            'backgroundColor': theme['backgroundColor']
        }

    def _generate_regional_line_config(self, data, params, theme):
        """生成地区趋势图配置（地图的替代方案）"""
        # 数据验证和清洗
        def validate_value(raw_value):
            try:
                if raw_value is None or raw_value == '':
                    return 0
                if isinstance(raw_value, str):
                    clean_str = raw_value.strip()
                    if not clean_str or clean_str.lower() in ['nan', 'null', 'undefined']:
                        return 0
                    return float(clean_str)
                return float(raw_value) if raw_value == raw_value else 0
            except (ValueError, TypeError):
                return 0

        # 处理数据
        regions = []
        values = []

        for item in data:
            region = item.get('region', '未知地区')
            value = validate_value(item.get('value'))
            regions.append(region)
            values.append(value)

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {'fontSize': 18, 'fontWeight': 'bold', 'color': '#333'}
            },
            'tooltip': {
                'trigger': 'axis',
                'formatter': '{b}<br/>农业产值: {c}万元'
            },
            'xAxis': {
                'type': 'category',
                'data': regions,
                'axisLabel': {'rotate': 45}
            },
            'yAxis': {
                'type': 'value',
                'name': '产值(万元)'
            },
            'series': [{
                'name': '农业产值',
                'type': 'line',
                'data': values,
                'smooth': True,
                'itemStyle': {
                    'color': theme['colors'][0]
                },
                'lineStyle': {
                    'color': theme['colors'][0]
                }
            }],
            'backgroundColor': theme['backgroundColor']
        }

    def _generate_regional_scatter_config(self, data, params, theme):
        """生成地区散点图配置（地图的替代方案）"""
        # 数据验证和清洗
        def validate_value(raw_value):
            try:
                if raw_value is None or raw_value == '':
                    return 0
                if isinstance(raw_value, str):
                    clean_str = raw_value.strip()
                    if not clean_str or clean_str.lower() in ['nan', 'null', 'undefined']:
                        return 0
                    return float(clean_str)
                return float(raw_value) if raw_value == raw_value else 0
            except (ValueError, TypeError):
                return 0

        # 处理数据 - 散点图需要[x, y]格式
        scatter_data = []
        for i, item in enumerate(data):
            region = item.get('region', f'地区{i+1}')
            value = validate_value(item.get('value'))
            scatter_data.append([i, value, region])  # [x坐标, y坐标, 地区名]

        return {
            'title': {
                'text': params['title'],
                'left': 'center',
                'textStyle': {'fontSize': 18, 'fontWeight': 'bold', 'color': '#333'}
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{c}<br/>农业产值: {c}万元'
            },
            'xAxis': {
                'type': 'value',
                'name': '地区序号'
            },
            'yAxis': {
                'type': 'value',
                'name': '产值(万元)'
            },
            'series': [{
                'name': '农业产值',
                'type': 'scatter',
                'data': scatter_data,
                'symbolSize': 20,
                'itemStyle': {
                    'color': theme['colors'][0]
                }
            }],
            'backgroundColor': theme['backgroundColor']
        }

def function_template(template_name):
    """函数模板占位符"""
    templates = {
        'weather_tooltip': "function(params) { return params[0].name + '<br/>温度: ' + params[0].value + '°C'; }",
        'seasonal_colors': "function(params) { var colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666']; return colors[params.dataIndex % colors.length]; }"
    }
    return templates.get(template_name, "function() { return ''; }")

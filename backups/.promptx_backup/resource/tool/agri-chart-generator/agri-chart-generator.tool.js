/**
 * 农业数据可视化工具
 * 基于ECharts生成农业领域专用图表配置
 */

module.exports = {
  getDependencies() {
    return [
      'lodash@^4.17.21',
      'moment@^2.29.4'
    ];
  },

  getMetadata() {
    return {
      name: 'agri-chart-generator',
      description: '专业的农业数据可视化工具，基于ECharts生成农业领域专用的图表配置',
      version: '1.0.0',
      category: 'visualization',
      author: '鲁班',
      tags: ['agriculture', 'echarts', 'visualization', 'charts'],
      manual: '@manual://agri-chart-generator'
    };
  },

  getSchema() {
    return {
      type: 'object',
      properties: {
        chart_type: {
          type: 'string',
          enum: ['price_trend', 'weather_forecast', 'yield_analysis', 'seasonal_comparison', 'regional_comparison'],
          description: '图表类型'
        },
        data: {
          type: 'array',
          items: {
            type: 'object'
          },
          minItems: 1,
          description: '图表数据'
        },
        title: {
          type: 'string',
          default: '农业数据图表',
          description: '图表标题'
        },
        theme: {
          type: 'string',
          enum: ['agriculture', 'green', 'blue', 'default'],
          default: 'agriculture',
          description: '图表主题'
        },
        width: {
          type: 'number',
          minimum: 100,
          maximum: 2000,
          default: 800,
          description: '图表宽度（像素）'
        },
        height: {
          type: 'number',
          minimum: 100,
          maximum: 2000,
          default: 400,
          description: '图表高度（像素）'
        },
        time_range: {
          type: 'object',
          properties: {
            start: { type: 'string', format: 'date' },
            end: { type: 'string', format: 'date' }
          },
          description: '时间范围配置'
        },
        region_filter: {
          type: 'array',
          items: { type: 'string' },
          default: [],
          description: '地区筛选'
        },
        annotations: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              date: { type: 'string' },
              event: { type: 'string' },
              type: { type: 'string' }
            }
          },
          default: [],
          description: '农时标注'
        },
        responsive: {
          type: 'boolean',
          default: true,
          description: '是否响应式'
        },
        export_format: {
          type: 'string',
          enum: ['json', 'html', 'both'],
          default: 'json',
          description: '导出格式'
        }
      },
      required: ['chart_type', 'data']
    };
  },

  validate(params) {
    const errors = [];
    const _ = require('lodash');
    
    // 验证数据格式
    const requiredFields = this._getRequiredFields(params.chart_type);
    const sampleData = params.data[0];
    
    requiredFields.forEach(field => {
      if (!sampleData.hasOwnProperty(field)) {
        errors.push(`${params.chart_type} 类型图表需要 ${field} 字段`);
      }
    });
    
    // 验证时间范围
    if (params.time_range) {
      const start = new Date(params.time_range.start);
      const end = new Date(params.time_range.end);
      if (start > end) {
        errors.push('开始时间不能晚于结束时间');
      }
    }
    
    // 验证数据一致性
    const inconsistentData = params.data.some(item => {
      return !requiredFields.every(field => item.hasOwnProperty(field));
    });
    
    if (inconsistentData) {
      errors.push('数据项字段不一致，请确保所有数据项包含必要字段');
    }
    
    return {
      valid: errors.length === 0,
      errors: errors
    };
  },

  async execute(params) {
    const startTime = Date.now();
    
    try {
      // 数据预处理
      const processedData = this._preprocessData(params.data, params);
      
      // 生成图表配置
      const chartConfig = this._generateChartConfig(params, processedData);
      
      // 应用主题
      this._applyTheme(chartConfig, params.theme);
      
      // 添加农时标注
      if (params.annotations && params.annotations.length > 0) {
        this._addAnnotations(chartConfig, params.annotations);
      }
      
      // 设置响应式
      if (params.responsive) {
        this._makeResponsive(chartConfig);
      }
      
      // 生成HTML和脚本
      const htmlOutput = this._generateHTML(chartConfig, params);
      const scriptOutput = this._generateScript(chartConfig, params);
      
      const result = {
        success: true,
        data: {
          chart_config: chartConfig,
          metadata: {
            chart_type: params.chart_type,
            data_points: processedData.length,
            generation_time: new Date().toISOString(),
            theme: params.theme,
            responsive: params.responsive
          }
        }
      };
      
      // 根据导出格式添加相应内容
      if (params.export_format === 'html' || params.export_format === 'both') {
        result.data.chart_html = htmlOutput;
        result.data.chart_script = scriptOutput;
      }
      
      return result;
      
    } catch (error) {
      return {
        success: false,
        error: {
          code: this._getErrorCode(error),
          message: error.message,
          details: {
            chart_type: params.chart_type,
            data_count: params.data.length,
            processing_time: Date.now() - startTime
          },
          suggestions: this._getErrorSuggestions(error, params)
        }
      };
    }
  },

  // 获取图表类型所需字段
  _getRequiredFields(chartType) {
    const fieldMap = {
      'price_trend': ['date', 'price'],
      'weather_forecast': ['date', 'temperature', 'weather'],
      'yield_analysis': ['year', 'yield', 'crop'],
      'seasonal_comparison': ['month', 'value'],
      'regional_comparison': ['region', 'value']
    };
    
    return fieldMap[chartType] || ['date', 'value'];
  },

  // 数据预处理
  _preprocessData(data, params) {
    const _ = require('lodash');
    const moment = require('moment');
    
    let processedData = _.cloneDeep(data);
    
    // 时间范围筛选
    if (params.time_range) {
      processedData = processedData.filter(item => {
        const itemDate = moment(item.date);
        return itemDate.isBetween(params.time_range.start, params.time_range.end, null, '[]');
      });
    }
    
    // 地区筛选
    if (params.region_filter && params.region_filter.length > 0) {
      processedData = processedData.filter(item => 
        params.region_filter.includes(item.region)
      );
    }
    
    // 数据排序
    if (processedData[0].date) {
      processedData.sort((a, b) => new Date(a.date) - new Date(b.date));
    }
    
    return processedData;
  },

  // 生成图表配置
  _generateChartConfig(params, data) {
    const generators = {
      'price_trend': this._generatePriceTrendConfig,
      'weather_forecast': this._generateWeatherForecastConfig,
      'yield_analysis': this._generateYieldAnalysisConfig,
      'seasonal_comparison': this._generateSeasonalComparisonConfig,
      'regional_comparison': this._generateRegionalComparisonConfig
    };
    
    const generator = generators[params.chart_type];
    if (!generator) {
      throw new Error(`不支持的图表类型: ${params.chart_type}`);
    }
    
    return generator.call(this, params, data);
  },

  // 生成价格趋势图配置
  _generatePriceTrendConfig(params, data) {
    const _ = require('lodash');
    
    const dates = data.map(item => item.date);
    const prices = data.map(item => item.price);
    const products = _.uniq(data.map(item => item.product || '农产品'));
    
    return {
      title: {
        text: params.title,
        left: 'center',
        textStyle: {
          fontSize: 18,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: function(params) {
          let result = params[0].name + '<br/>';
          params.forEach(param => {
            result += `${param.seriesName}: ${param.value} 元/斤<br/>`;
          });
          return result;
        }
      },
      legend: {
        data: products,
        top: 30
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      toolbox: {
        feature: {
          saveAsImage: {
            title: '保存图片'
          },
          dataZoom: {
            title: {
              zoom: '区域缩放',
              back: '区域缩放还原'
            }
          }
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dates,
        name: '时间',
        nameLocation: 'middle',
        nameGap: 30
      },
      yAxis: {
        type: 'value',
        name: '价格(元/斤)',
        nameLocation: 'middle',
        nameGap: 50
      },
      series: [{
        name: products[0],
        type: 'line',
        stack: 'Total',
        data: prices,
        smooth: true,
        itemStyle: {
          color: '#52c41a'
        },
        areaStyle: {
          opacity: 0.3
        }
      }],
      dataZoom: [{
        type: 'inside',
        start: 0,
        end: 100
      }, {
        start: 0,
        end: 100,
        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23.1h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        handleStyle: {
          color: '#fff',
          shadowBlur: 3,
          shadowColor: 'rgba(0, 0, 0, 0.6)',
          shadowOffsetX: 2,
          shadowOffsetY: 2
        }
      }]
    };
  },

  // 生成天气预报图配置
  _generateWeatherForecastConfig(params, data) {
    const dates = data.map(item => item.date);
    const temperatures = data.map(item => item.temperature);
    const weathers = data.map(item => item.weather);
    
    return {
      title: {
        text: params.title,
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: function(params) {
          const dataIndex = params[0].dataIndex;
          return `${params[0].name}<br/>温度: ${params[0].value}°C<br/>天气: ${weathers[dataIndex]}`;
        }
      },
      xAxis: {
        type: 'category',
        data: dates,
        name: '日期'
      },
      yAxis: {
        type: 'value',
        name: '温度(°C)'
      },
      series: [{
        name: '温度',
        type: 'line',
        data: temperatures,
        smooth: true,
        itemStyle: {
          color: '#1890ff'
        }
      }]
    };
  },

  // 生成产量分析图配置
  _generateYieldAnalysisConfig(params, data) {
    const _ = require('lodash');
    
    const years = _.uniq(data.map(item => item.year)).sort();
    const crops = _.uniq(data.map(item => item.crop));
    
    const series = crops.map(crop => {
      const cropData = years.map(year => {
        const item = data.find(d => d.year === year && d.crop === crop);
        return item ? item.yield : 0;
      });
      
      return {
        name: crop,
        type: 'bar',
        data: cropData
      };
    });
    
    return {
      title: {
        text: params.title,
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: crops,
        top: 30
      },
      xAxis: {
        type: 'category',
        data: years,
        name: '年份'
      },
      yAxis: {
        type: 'value',
        name: '产量(吨/亩)'
      },
      series: series
    };
  },

  // 生成季节对比图配置
  _generateSeasonalComparisonConfig(params, data) {
    const months = data.map(item => `${item.month}月`);
    const values = data.map(item => item.value);
    
    return {
      title: {
        text: params.title,
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      xAxis: {
        type: 'category',
        data: months,
        name: '月份'
      },
      yAxis: {
        type: 'value',
        name: '数值'
      },
      series: [{
        name: '月度数据',
        type: 'bar',
        data: values,
        itemStyle: {
          color: function(params) {
            const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#5470c6', '#91cc75', '#fac858'];
            return colors[params.dataIndex % colors.length];
          }
        }
      }]
    };
  },

  // 生成地区对比图配置
  _generateRegionalComparisonConfig(params, data) {
    const regions = data.map(item => item.region);
    const values = data.map(item => item.value);
    
    return {
      title: {
        text: params.title,
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      series: [{
        name: '地区数据',
        type: 'pie',
        radius: '50%',
        data: data.map(item => ({
          value: item.value,
          name: item.region
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    };
  },

  // 应用主题
  _applyTheme(config, theme) {
    const themes = {
      agriculture: {
        color: ['#52c41a', '#faad14', '#1890ff', '#f5222d', '#722ed1'],
        backgroundColor: '#fafafa'
      },
      green: {
        color: ['#52c41a', '#73d13d', '#95de64', '#b7eb8f', '#d9f7be'],
        backgroundColor: '#f6ffed'
      },
      blue: {
        color: ['#1890ff', '#40a9ff', '#69c0ff', '#91d5ff', '#bae7ff'],
        backgroundColor: '#f0f8ff'
      }
    };
    
    if (themes[theme]) {
      Object.assign(config, themes[theme]);
    }
  },

  // 添加农时标注
  _addAnnotations(config, annotations) {
    if (!config.graphic) {
      config.graphic = [];
    }
    
    annotations.forEach((annotation, index) => {
      config.graphic.push({
        type: 'text',
        left: `${20 + index * 100}px`,
        top: '10px',
        style: {
          text: `${annotation.event}(${annotation.date})`,
          fontSize: 12,
          fill: '#666'
        }
      });
    });
  },

  // 设置响应式
  _makeResponsive(config) {
    config.responsive = true;
    config.maintainAspectRatio = false;
  },

  // 生成HTML
  _generateHTML(config, params) {
    return `<div id="agri-chart" style="width:${params.width}px;height:${params.height}px;"></div>`;
  },

  // 生成脚本
  _generateScript(config, params) {
    return `
var myChart = echarts.init(document.getElementById('agri-chart'));
var option = ${JSON.stringify(config, null, 2)};
myChart.setOption(option);

// 响应式处理
if (${params.responsive}) {
  window.addEventListener('resize', function() {
    myChart.resize();
  });
}
    `.trim();
  },

  // 获取错误代码
  _getErrorCode(error) {
    if (error.message.includes('不支持的图表类型')) {
      return 'UNSUPPORTED_CHART_TYPE';
    } else if (error.message.includes('字段')) {
      return 'INVALID_DATA_FORMAT';
    } else {
      return 'GENERATION_ERROR';
    }
  },

  // 获取错误建议
  _getErrorSuggestions(error, params) {
    const suggestions = [];
    
    if (error.message.includes('字段')) {
      suggestions.push('检查数据字段是否完整');
      suggestions.push('确认数据格式符合图表类型要求');
      suggestions.push('参考文档中的数据示例');
    } else if (error.message.includes('图表类型')) {
      suggestions.push('使用支持的图表类型');
      suggestions.push('检查chart_type参数值');
    } else {
      suggestions.push('检查输入参数格式');
      suggestions.push('简化数据结构重试');
    }
    
    return suggestions;
  }
};

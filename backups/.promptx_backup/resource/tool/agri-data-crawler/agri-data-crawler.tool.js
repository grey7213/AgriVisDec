/**
 * 农业数据爬虫工具
 * 支持从多个农业网站采集结构化数据
 */

const axios = require('axios');
const cheerio = require('cheerio');
const { URL } = require('url');

module.exports = {
  getDependencies() {
    return [
      'axios@^1.6.0',
      'cheerio@^1.0.0-rc.12',
      'user-agents@^1.0.1'
    ];
  },

  getMetadata() {
    return {
      name: 'agri-data-crawler',
      description: '专业的农业数据爬虫工具，支持从种子交易网、天气网、农机网等多个农业数据源自动采集结构化数据',
      version: '1.0.0',
      category: 'data-collection',
      author: '鲁班',
      tags: ['agriculture', 'crawler', 'data-collection'],
      manual: '@manual://agri-data-crawler'
    };
  },

  getSchema() {
    return {
      type: 'object',
      properties: {
        website: {
          type: 'string',
          enum: ['seed_trade', 'weather', 'farm_machine'],
          description: '目标网站类型'
        },
        data_type: {
          type: 'string',
          enum: ['price', 'weather_forecast', 'product_info'],
          description: '需要采集的数据类型'
        },
        region: {
          type: 'string',
          default: '全国',
          description: '数据采集的地区范围'
        },
        date_range: {
          type: 'object',
          properties: {
            start: { type: 'string', format: 'date' },
            end: { type: 'string', format: 'date' }
          },
          description: '采集数据的时间范围'
        },
        max_pages: {
          type: 'number',
          minimum: 1,
          maximum: 100,
          default: 10,
          description: '最大采集页数'
        },
        delay: {
          type: 'number',
          minimum: 1000,
          default: 2000,
          description: '请求间隔时间（毫秒）'
        },
        output_format: {
          type: 'string',
          enum: ['json', 'csv'],
          default: 'json',
          description: '输出数据格式'
        },
        save_to_db: {
          type: 'boolean',
          default: false,
          description: '是否直接保存到数据库'
        },
        db_config: {
          type: 'object',
          properties: {
            host: { type: 'string' },
            database: { type: 'string' },
            table: { type: 'string' }
          },
          description: '数据库连接配置'
        }
      },
      required: ['website', 'data_type']
    };
  },

  validate(params) {
    const errors = [];
    
    // 验证网站类型和数据类型的匹配
    const validCombinations = {
      'seed_trade': ['price', 'product_info'],
      'weather': ['weather_forecast'],
      'farm_machine': ['product_info', 'price']
    };
    
    if (!validCombinations[params.website]?.includes(params.data_type)) {
      errors.push(`数据类型 ${params.data_type} 与网站类型 ${params.website} 不匹配`);
    }
    
    // 验证日期范围
    if (params.date_range) {
      const start = new Date(params.date_range.start);
      const end = new Date(params.date_range.end);
      if (start > end) {
        errors.push('开始日期不能晚于结束日期');
      }
    }
    
    // 验证数据库配置
    if (params.save_to_db && !params.db_config) {
      errors.push('启用数据库保存时必须提供数据库配置');
    }
    
    return {
      valid: errors.length === 0,
      errors: errors
    };
  },

  async execute(params) {
    const startTime = Date.now();
    
    try {
      // 初始化爬虫配置
      const config = this._initCrawlerConfig(params);
      
      // 执行数据采集
      const crawlResults = await this._crawlData(config);
      
      // 数据清洗和验证
      const cleanedData = await this._cleanData(crawlResults, params);
      
      // 保存到数据库（如果需要）
      if (params.save_to_db) {
        await this._saveToDatabase(cleanedData, params.db_config);
      }
      
      // 计算数据质量分数
      const qualityScore = this._calculateQualityScore(cleanedData);
      
      return {
        success: true,
        data: {
          total_records: cleanedData.length,
          crawled_pages: config.actualPages,
          data_records: cleanedData,
          metadata: {
            crawl_time: new Date().toISOString(),
            website: params.website,
            data_quality_score: qualityScore,
            processing_time: Date.now() - startTime
          }
        }
      };
      
    } catch (error) {
      return {
        success: false,
        error: {
          code: this._getErrorCode(error),
          message: error.message,
          details: {
            website: params.website,
            processing_time: Date.now() - startTime,
            error_type: error.constructor.name
          },
          suggestions: this._getErrorSuggestions(error)
        }
      };
    }
  },

  // 初始化爬虫配置
  _initCrawlerConfig(params) {
    const UserAgent = require('user-agents');
    const userAgent = new UserAgent();
    
    const websiteConfigs = {
      seed_trade: {
        baseUrl: 'https://www.114seeds.com',
        selectors: {
          price: '.price-item',
          product_name: '.product-name',
          variety: '.variety-name'
        }
      },
      weather: {
        baseUrl: 'http://www.weather.com.cn',
        selectors: {
          temperature: '.tem',
          weather: '.wea',
          date: '.date'
        }
      },
      farm_machine: {
        baseUrl: 'https://www.nongjx.com',
        selectors: {
          product_name: '.product-title',
          price: '.price-info',
          specs: '.spec-info'
        }
      }
    };
    
    return {
      ...websiteConfigs[params.website],
      userAgent: userAgent.toString(),
      delay: params.delay,
      maxPages: params.max_pages,
      region: params.region,
      dataType: params.data_type,
      actualPages: 0
    };
  },

  // 执行数据采集
  async _crawlData(config) {
    const results = [];
    
    for (let page = 1; page <= config.maxPages; page++) {
      try {
        // 构建页面URL
        const url = this._buildPageUrl(config, page);
        
        // 发送HTTP请求
        const response = await axios.get(url, {
          headers: {
            'User-Agent': config.userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
          },
          timeout: 10000
        });
        
        // 解析页面数据
        const pageData = this._parsePage(response.data, config);
        results.push(...pageData);
        
        config.actualPages = page;
        
        // 请求间隔
        if (page < config.maxPages) {
          await this._sleep(config.delay);
        }
        
      } catch (error) {
        console.warn(`页面 ${page} 采集失败:`, error.message);
        break;
      }
    }
    
    return results;
  },

  // 构建页面URL
  _buildPageUrl(config, page) {
    const baseUrl = config.baseUrl;
    const params = new URLSearchParams({
      page: page,
      region: config.region,
      type: config.dataType
    });
    
    return `${baseUrl}/search?${params.toString()}`;
  },

  // 解析页面数据
  _parsePage(html, config) {
    const $ = cheerio.load(html);
    const results = [];
    
    // 根据网站类型解析不同的数据结构
    if (config.dataType === 'price') {
      $(config.selectors.price).each((index, element) => {
        const item = {
          product_name: $(element).find(config.selectors.product_name).text().trim(),
          variety: $(element).find(config.selectors.variety).text().trim(),
          price: this._parsePrice($(element).find('.price').text()),
          unit: $(element).find('.unit').text().trim(),
          region: $(element).find('.region').text().trim(),
          date: new Date().toISOString().split('T')[0],
          source_url: $(element).find('a').attr('href')
        };
        
        if (item.product_name && item.price) {
          results.push(item);
        }
      });
    }
    
    return results;
  },

  // 数据清洗
  async _cleanData(rawData, params) {
    return rawData.filter(item => {
      // 过滤无效数据
      if (!item.product_name || !item.price) return false;
      
      // 价格合理性检查
      if (typeof item.price === 'number' && (item.price <= 0 || item.price > 10000)) {
        return false;
      }
      
      return true;
    }).map(item => {
      // 数据标准化
      return {
        ...item,
        product_name: item.product_name.replace(/\s+/g, ' ').trim(),
        price: typeof item.price === 'string' ? this._parsePrice(item.price) : item.price,
        region: item.region || params.region
      };
    });
  },

  // 解析价格字符串
  _parsePrice(priceStr) {
    if (typeof priceStr === 'number') return priceStr;
    const match = priceStr.match(/(\d+\.?\d*)/);
    return match ? parseFloat(match[1]) : null;
  },

  // 计算数据质量分数
  _calculateQualityScore(data) {
    if (data.length === 0) return 0;
    
    let validCount = 0;
    data.forEach(item => {
      if (item.product_name && item.price && item.region) {
        validCount++;
      }
    });
    
    return Math.round((validCount / data.length) * 100) / 100;
  },

  // 保存到数据库（模拟实现）
  async _saveToDatabase(data, dbConfig) {
    // 这里应该实现真实的数据库保存逻辑
    console.log(`模拟保存 ${data.length} 条记录到数据库 ${dbConfig.database}.${dbConfig.table}`);
    return true;
  },

  // 获取错误代码
  _getErrorCode(error) {
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      return 'NETWORK_ERROR';
    } else if (error.response && error.response.status >= 400) {
      return 'HTTP_ERROR';
    } else if (error.message.includes('timeout')) {
      return 'TIMEOUT_ERROR';
    } else {
      return 'UNKNOWN_ERROR';
    }
  },

  // 获取错误建议
  _getErrorSuggestions(error) {
    const suggestions = [];
    
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      suggestions.push('检查网络连接');
      suggestions.push('确认目标网站是否正常运行');
    } else if (error.response && error.response.status === 429) {
      suggestions.push('降低请求频率');
      suggestions.push('增加请求间隔时间');
    } else if (error.message.includes('timeout')) {
      suggestions.push('增加请求超时时间');
      suggestions.push('检查网络稳定性');
    }
    
    suggestions.push('稍后重试');
    return suggestions;
  },

  // 延时函数
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
};

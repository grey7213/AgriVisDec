<manual>
<identity>
## 工具名称
@tool://agri-chart-generator

## 简介

专业的农业数据可视化工具，基于ECharts生成农业领域专用的图表配置，支持价格趋势、天气预报、产量分析等多种农业图表类型
`</identity>`

<purpose>
⚠️ **AI重要提醒**: 调用此工具前必须完整阅读本说明书，理解工具功能边界、参数要求和使用限制。禁止在不了解工具功能的情况下盲目调用。

## 核心问题定义

解决农业数据可视化复杂、图表配置繁琐的问题，为农业数据平台提供专业的图表生成能力，让农户能够直观地理解农业数据趋势和规律。

## 价值主张

- 🎯 **解决什么痛点**：农业数据复杂难懂，手动配置ECharts图表耗时费力，缺乏农业领域专业的图表模板
- 🚀 **带来什么价值**：一键生成专业农业图表，提升数据可读性80%，减少图表开发时间90%
- 🌟 **独特优势**：内置农业领域专业图表模板，支持农时标注、季节性分析、地域对比等农业特色功能

## 应用边界

- ✅ **适用场景**：
  - 农产品价格趋势图表
  - 天气预报可视化看板
  - 农作物产量分析图
  - 农事日历时间轴
  - 地区农业数据对比
  - 农业风险评估图表
- ❌ **不适用场景**：
  - 非农业领域的通用图表
  - 需要复杂交互的动态图表
  - 实时数据流图表
  - 3D立体图表
    `</purpose>`

<usage>
## 使用时机
- 农业数据看板开发时需要图表配置
- 农业分析报告需要可视化展示
- 为农户提供直观的数据展示界面
- 农业决策支持系统的图表需求

## 操作步骤

1. **准备阶段**：

   - 整理需要可视化的农业数据
   - 确定图表类型和展示需求
   - 准备图表的标题、单位等基础信息
2. **执行阶段**：

   - 选择合适的农业图表类型
   - 配置数据字段映射
   - 设置图表样式和主题
   - 生成ECharts配置代码
3. **验证阶段**：

   - 在ECharts环境中测试图表配置
   - 检查数据展示是否准确
   - 验证图表在不同设备上的显示效果

## 最佳实践

- 🎯 **效率提升技巧**：

  - 使用预设的农业图表模板
  - 批量生成多个相关图表
  - 利用图表主题保持视觉一致性
  - 设置合理的数据更新频率
- ⚠️ **常见陷阱避免**：

  - 避免在单个图表中展示过多数据维度
  - 注意农业数据的季节性特征
  - 考虑农户的阅读习惯和理解能力
  - 确保图表在移动端的可读性
- 🔧 **故障排除指南**：

  - 图表不显示：检查数据格式和字段映射
  - 样式异常：验证ECharts版本兼容性
  - 性能问题：减少数据点数量或使用数据采样
  - 移动端适配：调整图表尺寸和字体大小

## 注意事项

- **数据准确性**：确保输入数据的准确性和时效性
- **用户体验**：考虑农户的使用习惯，保持界面简洁直观
- **性能优化**：大数据量时使用数据缩放和懒加载
- **响应式设计**：确保图表在各种设备上正常显示
- **颜色选择**：使用对色盲友好的颜色方案
  `</usage>`

<parameter>
## 必需参数
| 参数名 | 类型 | 描述 | 示例 |
|--------|------|------|------|
| chart_type | string | 图表类型 | "price_trend", "weather_forecast", "yield_analysis" |
| data | array | 图表数据 | [{"date": "2024-01", "price": 45.8}] |

## 可选参数

| 参数名        | 类型    | 默认值         | 描述             |
| ------------- | ------- | -------------- | ---------------- |
| title         | string  | "农业数据图表" | 图表标题         |
| theme         | string  | "agriculture"  | 图表主题         |
| width         | number  | 800            | 图表宽度（像素） |
| height        | number  | 400            | 图表高度（像素） |
| time_range    | object  | null           | 时间范围配置     |
| region_filter | array   | []             | 地区筛选         |
| annotations   | array   | []             | 农时标注         |
| responsive    | boolean | true           | 是否响应式       |
| export_format | string  | "json"         | 导出格式         |

## 参数约束

- **chart_type**: 必须是支持的农业图表类型
- **data**: 数组不能为空，每个数据项必须包含必要字段
- **width/height**: 范围100-2000像素
- **theme**: 支持"agriculture", "green", "blue", "default"
- **time_range**: 开始时间不能晚于结束时间

## 参数示例

```json
{
  "chart_type": "price_trend",
  "data": [
    {"date": "2024-01", "product": "玉米", "price": 2.8, "region": "山东"},
    {"date": "2024-02", "product": "玉米", "price": 2.9, "region": "山东"}
  ],
  "title": "玉米价格趋势分析",
  "theme": "agriculture",
  "width": 1000,
  "height": 500,
  "time_range": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  },
  "annotations": [
    {"date": "2024-03", "event": "春播期", "type": "farming_season"}
  ],
  "responsive": true,
  "export_format": "json"
}
```

</parameter>

<outcome>
## 成功返回格式
```json
{
  "success": true,
  "data": {
    "chart_config": {
      "title": {
        "text": "玉米价格趋势分析",
        "left": "center"
      },
      "tooltip": {
        "trigger": "axis",
        "formatter": "农业数据提示格式"
      },
      "xAxis": {
        "type": "category",
        "data": ["2024-01", "2024-02"]
      },
      "yAxis": {
        "type": "value",
        "name": "价格(元/斤)"
      },
      "series": [{
        "name": "玉米价格",
        "type": "line",
        "data": [2.8, 2.9],
        "itemStyle": {
          "color": "#52c41a"
        }
      }]
    },
    "chart_html": "<div id='chart' style='width:1000px;height:500px;'></div>",
    "chart_script": "var myChart = echarts.init(document.getElementById('chart'));",
    "metadata": {
      "chart_type": "price_trend",
      "data_points": 2,
      "generation_time": "2024-01-15T10:30:00Z",
      "theme": "agriculture",
      "responsive": true
    }
  }
}
```

## 错误处理格式

```json
{
  "success": false,
  "error": {
    "code": "INVALID_DATA_FORMAT",
    "message": "数据格式不符合图表类型要求",
    "details": {
      "chart_type": "price_trend",
      "required_fields": ["date", "price"],
      "missing_fields": ["price"],
      "data_sample": {"date": "2024-01"}
    },
    "suggestions": [
      "检查数据字段是否完整",
      "确认数据格式符合图表类型要求",
      "参考文档中的数据示例"
    ]
  }
}
```

## 结果解读指南

- **图表配置使用**：chart_config 可直接用于ECharts初始化
- **HTML集成**：chart_html 和 chart_script 提供完整的页面集成代码
- **响应式支持**：responsive=true时图表会自动适配容器大小
- **主题一致性**：使用相同theme确保多个图表视觉统一

## 后续动作建议

- **成功生成后**：

  - 将chart_config集成到前端页面
  - 测试图表在不同设备上的显示效果
  - 设置数据更新机制保持图表实时性
  - 添加用户交互功能（缩放、筛选等）
- **生成失败时**：

  - 根据错误提示调整数据格式
  - 检查图表类型与数据的匹配性
  - 简化数据结构重新尝试
  - 参考成功案例调整参数
- **优化建议**：

  - 根据用户反馈调整图表样式
  - 添加更多农业特色的标注信息
  - 考虑数据钻取和联动功能
  - 建立图表模板库便于复用
    `</outcome>`
    `</manual>`

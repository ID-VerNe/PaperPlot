# 02_Chart_Types - 图表类型

本目录展示 PaperPlot 支持的各种图表类型。每个示例文件都专注于一种或一类相关的图表。

##文件列表

### 基础图表

- **`bar_charts.py`** - 柱状图变体
  - 分组柱状图（Grouped Bar Chart）
  - 堆叠柱状图（Stacked Bar Chart）
  - 适用于：类别比较、多系列数据

- **`line_charts.py`** - 折线图
  - 多线图（Multi-Line Chart）
  - 适用于：趋势分析、时间序列数据

- **`pie_and_donut.py`** - 圆形图表
  - 饼图（Pie Chart）
  - 环形图（Donut Chart）
  - 嵌套环形图（Nested Donut Chart）
  - 适用于：比例展示、层级数据

### 专用图表

- **`heatmaps.py`** - 热图
  - 热图与共享颜色条
  - 适用于：矩阵数据、相关性分析

- **`waterfall.py`** - 瀑布图
  - 阶梯瀑布图
  - 适用于：累积效应分析、财务数据

- **`candlestick.py`** - K线图（蜡烛图）
  - 金融K线图
  - 适用于：股票价格、交易数据

- **`polar_plots.py`** - 极坐标图
  - 极坐标柱状图
  - 适用于：周期性数据、方向数据

### 统计图表

- **`statistical_plots.py`** - 统计图
  - 小提琴图（Violin Plot）
  - 箱线图（Box Plot）
  - 蜂群图（Swarm Plot）
  - 统计检验标注
  - 适用于：分布分析、组间比较

- **`regression_plots.py`** - 回归图
  - 回归分析图
  - 适用于：相关性分析、预测建模

## 学习路径

**初学者**：
1. `bar_charts.py` → `line_charts.py` → `pie_and_donut.py`
2. 了解基础图表类型和用法

**进阶**：
1. `statistical_plots.py` - 学习数据分析图表
2. `heatmaps.py` - 掌握矩阵数据可视化
3. `candlestick.py`, `waterfall.py` - 探索专业领域图表

## 快速参考

### 选择合适的图表类型

| 数据类型 | 推荐图表 | 示例文件 |
|---------|---------|---------|
| 类别对比 | 柱状图 | `bar_charts.py` |
| 时间序列 | 折线图 | `line_charts.py` |
| 比例关系 | 饼图/环形图 | `pie_and_donut.py` |
| 分布分析 | 箱线图/小提琴图 | `statistical_plots.py` |
| 矩阵数据 | 热图 | `heatmaps.py` |
| 财务数据 | K线图/瀑布图 | `candlestick.py`, `waterfall.py` |
| 相关性 | 回归图 | `regression_plots.py` |

## 使用提示

1. **数据准备**：确保数据格式符合图表要求（DataFrame、列名等）
2. **颜色配置**：使用 `style` 参数选择合适的主题
3. **图例管理**：使用 `labels` 参数自定义图例文本
4. **组合使用**：可以在一个布局中组合多种图表类型

## 下一步

- 学习布局管理：[../03_Layout_Management/](../03_Layout_Management/)
- 添加注释标注：[../06_Annotations/](../06_Annotations/)
- 定制样式主题：[../05_Styling_and_Themes/](../05_Styling_and_Themes/)

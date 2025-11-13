---
id: mixins-generic
title: GenericPlotsMixin API
sidebar_label: 通用图表
---

## 概述

`GenericPlotsMixin` 包含所有通用的、与特定领域无关的图表类型。这些方法是构建复杂图表的基础。

- **统一数据输入**:
  - **DataFrame 模式 (推荐)**: `data=df, x='col_name', y='col_name'`。这种方式便于数据缓存和后续的统计修饰。
  - **数组模式**: `x=[...], y=[...]`。方法内部会自动将其转换为 DataFrame。

---

### `add_line`
- **签名**: `add_line(data?, x, y, tag?, ax?, **kwargs)`
- **用途**: 绘制线图，封装 `matplotlib.axes.Axes.plot`。
- **核心参数**:
  - `data`: `pd.DataFrame` (可选)。
  - `x`, `y`: `str` (列名) 或 `array-like` (数据)。
  - `**kwargs`: 透传到 `Axes.plot`，如 `color`, `linestyle`, `marker`, `label`。
- **示例**: `plotter.add_line(data=df, x='time', y='value', label='Series A')`

---

### `add_bar`
- **签名**: `add_bar(data?, x, y, y_err?, tag?, ax?, **kwargs)`
- **用途**: 绘制柱状图，封装 `matplotlib.axes.Axes.bar`，支持误差条。
- **核心参数**:
  - `x`, `y`: 分类/位置和高度。
  - `y_err`: (可选) 误差条数据或列名。
- **示例**: `plotter.add_bar(data=df, x='category', y='value', y_err='std_dev')`

---

### `add_grouped_bar`
- **签名**: `add_grouped_bar(data, x, ys, labels?, width?, yerr?, ...)`
- **用途**: 在同一分类上并排绘制多系列分组柱状图。
- **核心参数**:
  - `data`: `pd.DataFrame`。
  - `x`: `str`, 分类列名。
  - `ys`: `List[str]`, 多个系列的高度列名。
  - `labels`: `Dict[str, str]` (可选), 系列列名到图例标签的映射。
- **示例**: `plotter.add_grouped_bar(data=df, x='year', ys=['sales_q1', 'sales_q2'])`

---

### `add_multi_line`
- **签名**: `add_multi_line(data, x, ys, labels?, ...)`
- **用途**: 在同一子图上轻松绘制多条折线。
- **核心参数**:
  - `data`: `pd.DataFrame`。
  - `x`: `str`, 共享的 x 轴列名。
  - `ys`: `List[str]`, 多个 y 轴系列的列名。
- **示例**: `plotter.add_multi_line(data=df, x='time', ys=['sensor_1', 'sensor_2'])`

---

### `add_stacked_bar`
- **签名**: `add_stacked_bar(data, x, ys, labels?, ...)`
- **用途**: 在同一分类上纵向堆叠多个系列，展示组成结构。
- **核心参数**:
  - `data`: `pd.DataFrame`。
  - `x`: `str`, 分类列名。
  - `ys`: `List[str]`, 多个系列列名，按列表顺序从下到上堆叠。
- **示例**: `plotter.add_stacked_bar(data=df, x='region', ys=['product_a', 'product_b'])`

---

### `add_polar_bar`
- **签名**: `add_polar_bar(data, theta, r, width?, ...)`
- **用途**: 在极坐标轴上绘制径向柱状图。
- **轴要求**: 目标轴必须是极坐标投影 (通过 `ax_configs` 在 `Plotter` 初始化时设置)。
- **核心参数**:
  - `theta`: `str`, 角度列名 (弧度)。
  - `r`: `str`, 半径列名。
- **示例**: `plotter.add_polar_bar(data=df, theta='direction', r='magnitude')`

---

### `add_pie` / `add_donut` / `add_nested_donut`
- **用途**: 绘制饼图、环形图和嵌套环形图。
- **核心参数**:
  - `add_pie(data, sizes, labels?, ...)`
  - `add_donut(data, sizes, labels?, width?, ...)`
  - `add_nested_donut(outer, inner, ...)`: `outer` 和 `inner` 是包含 `data`, `sizes` 的字典。
- **示例**: `plotter.add_donut(data=df, sizes='market_share', width=0.4)`

---

### `add_waterfall`
- **签名**: `add_waterfall(data, x, deltas, baseline?, ...)`
- **用途**: 绘制瀑布图，累计展示各阶段的增减变化。
- **核心参数**:
  - `x`: `str`, 阶段列名。
  - `deltas`: `str`, 变化值列名。
  - `baseline`: `float` (可选), 初始值。
- **示例**: `plotter.add_waterfall(data=df, x='stage', deltas='change', baseline=100)`

---

### `add_candlestick`
- **签名**: `add_candlestick(data, time, open, high, low, close, ...)`
- **用途**: 绘制金融K线图（蜡烛图）。
- **核心参数**:
  - `time`, `open`, `high`, `low`, `close`: `str`, 对应数据列名。
- **示例**: `plotter.add_candlestick(data=df, time='date', ...)`

---

### `add_scatter`
- **签名**: `add_scatter(data?, x, y, s?, c?, ...)`
- **用途**: 绘制散点图，支持按列控制点的大小和颜色。
- **核心参数**:
  - `s`, `c`: (可选) `str` (列名) 或 `array-like`。
- **示例**: `plotter.add_scatter(data=df, x='pc1', y='pc2', c='cluster_id', cmap='viridis')`

---

### `add_hist`
- **签名**: `add_hist(data?, x, ...)`
- **用途**: 绘制直方图。
- **核心参数**: `x` (数据或列名), `bins`, `density` 等 `Axes.hist` 参数。
- **示例**: `plotter.add_hist(data=df, x='value', bins=30, density=True)`

---

### `add_box`
- **签名**: `add_box(data?, x, y, hue?, ...)`
- **用途**: 绘制箱线图，封装 `seaborn.boxplot`。
- **核心参数**: `x` (分类), `y` (数值), `hue` (可选分组)。
- **示例**: `plotter.add_box(data=tips, x='day', y='total_bill', hue='smoker')`

---

### `add_heatmap`
- **签名**: `add_heatmap(data, cbar?, ...)`
- **用途**: 绘制热图，封装 `seaborn.heatmap`。
- **智能样式**: 若未指定 `cmap`，会根据当前样式主色自动生成一个连续色图。
- **核心参数**: `data` (`pd.DataFrame`), `annot`, `fmt`, `cbar`。
- **示例**: `plotter.add_heatmap(data=corr_matrix, annot=True, fmt='.2f')`

---

### `add_seaborn`
- **签名**: `add_seaborn(plot_func, data?, x?, y?, hue?, ...)`
- **用途**: 通用 Seaborn 绘制入口，允许调用任何接受 `data` 和 `ax` 的 Seaborn 函数。
- **核心参数**: `plot_func` (`Callable`), 如 `sns.violinplot`。
- **示例**: `plotter.add_seaborn(plot_func=sns.stripplot, data=df, x='group', y='value')`

---

### `add_blank`
- **签名**: `add_blank(tag?)`
- **用途**: 在指定子图位置创建空白区域并关闭坐标轴，用于布局占位。
- **示例**: `plotter.add_blank(tag='ax12')`

---

### `add_regplot`
- **签名**: `add_regplot(data?, x, y, ...)`
- **用途**: 绘制散点与线性回归拟合，封装 `seaborn.regplot`。
- **核心参数**: `scatter_kws`, `line_kws` (字典) 用于分别定制散点和线的样式。
- **示例**: `plotter.add_regplot(data=df, x='x', y='y', order=2)` (二阶多项式回归)

---

### `add_conditional_scatter`
- **签名**: `add_conditional_scatter(data?, x, y, condition, ...)`
- **用途**: 根据布尔条件在散点图上高亮特定数据点。
- **核心参数**:
  - `condition`: `str` (布尔列名) 或 `bool Series`。
  - `s_normal`, `c_normal`, `s_highlight`, `c_highlight` 等用于分别定义普通点和高亮点的样式。
- **示例**: `plotter.add_conditional_scatter(data=df, x='x', y='y', condition='is_outlier')`

---

### `add_figure`
- **签名**: `add_figure(image_path, fit_mode, align, padding, zoom, ...)`
- **用途**: 将一个外部图像文件作为子图的全部内容进行绘制。
- **核心参数**:
  - `image_path`: `str`, 图像文件路径。
  - `fit_mode`: `str` (可选), `'fit'` (默认), `'cover'`, `'stretch'`。
    - `'fit'`: 保持宽高比，适应子图，可能留白。
    - `'cover'`: 保持宽高比，填满子图，可能裁剪。
    - `'stretch'`: 拉伸以完全填满子图。
  - `align`: `str` (可选), 当 `fit_mode='fit'` 时，图片在留白区域的对齐方式，如 `'center'`, `'top_left'`。
  - `padding`: `float` (可选), 图像与子图边界的内边距 (0到0.5)。
  - `zoom`: `float` (可选), 从图像中心放大的比例 (0到0.5)。
- **示例**: `plotter.add_figure('logo.png', fit_mode='fit', align='bottom_right', padding=0.1)`
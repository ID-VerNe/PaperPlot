---
id: mixins-generic
title: GenericPlotsMixin API
sidebar_label: 通用图表
---

概述
- 通用图表类型：折线、散点、柱状、堆叠/分组、饼/环/嵌套环、瀑布、K 线、热图、回归、条件高亮等。
- 统一数据输入：
  - 方式 A：`data=df` + 列名字符串（推荐，便于缓存与后续修饰器）
  - 方式 B：直接数组，如 `x=[...]`、`y=[...]`（方法将自动组装 DataFrame）

add_line
- 签名：`add_line(data?, x, y, tag?, ax?, **kwargs) -> 'Plotter'`
- 用途：在子图上绘制线图（封装 `matplotlib.axes.Axes.plot`）。
- 参数：
  - `data`（可选）：`pd.DataFrame`。提供时，`x/y` 为列名；否则 `x/y` 直接为数组。
  - `x`：`str | array-like`。横轴数据或列名。
  - `y`：`str | array-like`。纵轴数据或列名。
  - `tag`/`ax`：与其他方法一致。
  - `**kwargs`：透传到 `Axes.plot`，如 `color`、`linestyle`、`marker`、`label`、`linewidth` 等。
- 默认样式：`plot_defaults_key='line'`（`linewidth=2`）。若提供 `label` 且未设置 `color`，将使用 `ColorManager` 分配稳定颜色。
- 数据准备：`data_keys=['x','y']`。
- 示例：`add_line(data=df, x='time', y='value', label='Series A')`
 - 示例（DataFrame 模式）：
 ```python
 plotter.add_line(data=df, x='time', y='value', label='Series A', linewidth=2)
 ```
 - 示例（数组模式）：
 ```python
 plotter.add_line(x=[1,2,3], y=[2.0, 3.1, 2.8], label='Series A')
 ```
 - 示例（链式修饰）：
 ```python
 (
   plotter
   .add_line(data=df, x='time', y='value', label='Series A')
   .set_title('Line Example')
   .set_legend()
 )
 ```

add_bar
- 签名：`add_bar(data?, x, y, y_err?, tag?, ax?, **kwargs) -> 'Plotter'`
- 用途：在子图上绘制条形图（封装 `matplotlib.axes.Axes.bar`），支持误差条与链式修饰器。
- 参数：
  - `data`（可选）：`pd.DataFrame`。当提供 `data` 时，其他数据键必须为列名字符串；否则应直接传数组。
  - `x`：`str | array-like`。分类或位置；`data` 模式下为列名；数组模式下为数据序列。
  - `y`：`str | array-like`。高度；`data` 模式下为列名；数组模式下为数据序列。
  - `y_err`（可选）：`str | array-like`。误差条；`data` 模式下必须为列名；数组模式下可直接为数组。
  - `tag`（可选）：`str | int`。绘制目标子图标签；省略时按顺序或复用最后活动子图。
  - `ax`（可选）：`plt.Axes`。直接指定轴对象；优先级高于 `tag`。
  - `**kwargs`：透传到 `Axes.bar` 的关键字参数，如 `color`、`width`、`align`、`label`、`alpha` 等。
- 返回：`Plotter`。支持链式调用（如后续 `.set_legend()`、`.set_title()`）。
- 行为与数据准备：
  - 通过统一工作流 `_execute_plot` 解析轴与 `tag`，准备数据并缓存到 `data_cache[tag]`，更新 `last_active_tag`。
  - `data_keys=['x','y','y_err']`：当 `data` 为 `DataFrame` 时，`x/y/y_err` 必须是列名字符串；当 `data=None` 时，`x/y/y_err` 直接为数组。
  - 绘制时将 `yerr=y_err`（若存在）传入 `Axes.bar`。
- 默认样式：
  - 合并默认 `bar` 样式：`alpha=0.8`。可通过 `**kwargs` 覆盖。
  - 颜色：若传入 `label` 且未显式给出 `color`，会使用 `ColorManager` 基于系列名分配稳定颜色。
- 注意事项：
  - 当 `data` 为 `DataFrame` 时，`y_err` 必须是列名；如果要使用数组误差条，请采用数组模式（`data=None` 且 `x,y,y_err` 直接为数组）。
  - `x` 为分类字符串时，Matplotlib 会根据类别位置放置柱；可配合 `set_xticklabels` 自定义标签格式。
  - 方法本身不返回 mappable；若需 colorbar，请选择支持 mappable 的图（如 `add_heatmap` 或在散点中用 `c=` 列）。
- 示例（DataFrame 列名模式）：
```
plotter.add_bar(
  data=df,
  x='category',
  y='value',
  y_err='std',
  label='Series A',
  width=0.6,
  tag='B'
).set_legend('B')
```
- 示例（数组模式，含误差条为数组）：
```
plotter.add_bar(
  x=['A','B','C'],
  y=[10, 12, 9],
  y_err=[1.2, 0.8, 1.5],
  label='Series A',
  alpha=0.7
)
```
- 示例（与修饰器链式组合）：
```
(
  plotter
  .add_bar(data=df, x='cat', y='height', y_err='err', label='A', tag='ax00')
  .set_title('Bar with Error', tag='ax00')
  .set_ylabel('Height', tag='ax00')
  .set_legend('ax00')
)
```

add_grouped_bar
- 签名：`add_grouped_bar(data, x, ys, labels?, width?, yerr?, tag?, ax?, **kwargs)`
- 用途：在同一分类上并排绘制多系列分组柱状图。
- 参数：
  - `data`：`pd.DataFrame`。需包含 `x` 与各系列列。
  - `x`：`str`。分类列名（用于 x 轴刻度标签）。
  - `ys`：`List[str]`。多个系列列名。
  - `labels`（可选）：`Dict[str,str]`。系列列名到图例标签的映射；触发稳定配色。
  - `width`（可选）：`float`。分组总宽度，默认 `0.8`。
  - `yerr`（可选）：`Dict[str,array-like]`。每系列误差条，键为列名。
  - `alpha`（可选）：透明度，默认 `0.8`。
  - `tag`/`ax`/`**kwargs`：标准参数，`kwargs` 透传到 `Axes.bar`。
- 数据准备：`data_keys=[]`，内部从 `kwargs` 读取 `x/ys`，并直接使用完整 `data` 作为缓存，避免丢失系列列。
- 绘制逻辑：自动计算每组内柱的偏移；`labels` 触发 `ColorManager`；设置 `xticks` 为分类索引并显示分类标签。
- 示例：`add_grouped_bar(data=df, x='category', ys=['s1','s2'], labels={'s1':'A','s2':'B'})`
 - 示例（标准用法）：
 ```python
 plotter.add_grouped_bar(data=df, x='category', ys=['s1','s2','s3'], labels={'s1':'A','s2':'B','s3':'C'}, width=0.8)
 plotter.set_legend()
 ```
 - 示例（带误差条）：
 ```python
 yerr = {'s1': df['s1_std'], 's2': df['s2_std']}
 plotter.add_grouped_bar(data=df, x='category', ys=['s1','s2'], yerr=yerr)
 ```
 - 示例（链式修饰）：
 ```python
 (
   plotter
   .add_grouped_bar(data=df, x='cat', ys=['s1','s2'], labels={'s1':'A','s2':'B'}, tag='G')
   .set_title('Grouped Bar', tag='G')
   .set_legend('G')
 )
 ```

add_multi_line
- 签名：`add_multi_line(data, x, ys, labels?, tag?, ax?, **kwargs)`
- 用途：在同一子图绘制多条折线，适合多变量随时间的比较。
- 参数：
  - `data`：`pd.DataFrame`。含 `x` 与多个 `ys` 列。
  - `x`：`str`。横轴列名。
  - `ys`：`List[str]`。系列列名列表。
  - `labels`（可选）：`Dict[str,str]`。系列列名到图例标签的映射。
  - `linewidth`（可选）：`float`。默认 `2`。
  - `tag`/`ax`/`**kwargs`：透传到 `Axes.plot`。
- 数据准备：`data_keys=[]`；从 `kwargs` 读取列名，缓存完整 `data`。
- 颜色与图例：每系列 `label` 触发 `ColorManager`；叠加后可用 `set_legend`。
- 示例：`add_multi_line(data=df, x='time', ys=['line1','line2'], labels={'line1':'A'})`
 - 示例（标准用法）：
 ```python
 plotter.add_multi_line(data=df, x='t', ys=['y1','y2'], labels={'y1':'Line A','y2':'Line B'}, linewidth=2)
 plotter.set_legend()
 ```
 - 示例（链式修饰）：
 ```python
 (
   plotter
   .add_multi_line(data=df, x='t', ys=['v','i'])
   .set_title('Multi Line')
   .set_legend()
 )
 ```

add_stacked_bar
- 签名：`add_stacked_bar(data, x, ys, labels?, width?, tag?, ax?, **kwargs)`
- 用途：同一分类上纵向堆叠多个系列，展示组成结构。
- 参数：
  - `data`：`pd.DataFrame`；`x` 分类列，`ys` 系列列。
  - `x`：`str`；`ys`：`List[str]`（堆叠顺序按列表）。
  - `labels`（可选）：`Dict[str,str]`；`width`（默认 `0.8`）；`alpha`（默认 `0.8`）。
  - `tag`/`ax`/`**kwargs`：透传到 `Axes.bar`。
- 数据准备：`data_keys=[]`。
- 行为：逐列累计 `bottoms`；设置分类刻度与标签；颜色由 `ColorManager` 基于 `labels` 或列名分配。
- 示例：`add_stacked_bar(data=df, x='category', ys=['part1','part2','part3'])`
 - 示例（标准用法）：
 ```python
 plotter.add_stacked_bar(data=df, x='cat', ys=['p1','p2','p3'], labels={'p1':'A','p2':'B','p3':'C'})
 plotter.set_legend()
 ```
 - 示例（链式修饰）：
 ```python
 (
   plotter
   .add_stacked_bar(data=df, x='cat', ys=['p1','p2'])
   .set_title('Stacked Bar')
   .set_legend()
 )
 ```

add_polar_bar
- 签名：`add_polar_bar(data, theta, r, width?, bottom?, tag?, ax?, **kwargs)`
- 用途：在极坐标轴上绘制径向柱状图。
- 轴要求：目标轴必须为极坐标投影（初始化时 `ax_configs={'P': {'projection':'polar'}}`）。
- 参数：
  - `data`：`pd.DataFrame`；`theta` 为角度列（弧度），`r` 为半径列。
  - `width`（可选）：`float`。若未指定，将根据排序后的 `theta` 间距的中位数估算；单点时默认 `0.1`。
  - `bottom`（可选）：`float`，起始半径，默认 `0.0`。
  - `tag`/`ax`/`**kwargs`：透传到 `Axes.bar`。
- 数据准备与缓存：内部直接解析 `data` 与列名，缓存 `data[[theta,r]]` 至 `data_cache[tag]`。
- 示例：`add_polar_bar(data=df, theta='theta', r='radius', tag='P', label='Series A')`
 - 示例（极坐标轴）：
 ```python
 plotter = Plotter(layout=[['P']], ax_configs={'P': {'projection': 'polar'}})
 plotter.add_polar_bar(data=df, theta='theta', r='r', tag='P', label='Series A')
 ```
 - 示例（与极坐标孪生轴）：
 ```python
 plotter.add_polar_bar(data=df1, theta='theta', r='r', tag='P', label='A')
 plotter.add_polar_twin('P').target_twin('P').add_polar_bar(data=df2, theta='theta', r='r2', label='B')
 plotter.target_primary('P').set_legend('P')
 ```

add_pie
- 签名：`add_pie(data, sizes, labels?, tag?, ax?, **kwargs)`
- 用途：绘制饼图；适合占比展示。
- 参数：
  - `data`：`pd.DataFrame`；`sizes` 数值列名。
  - `labels`（可选）：`Sequence[str]`；若提供将显示扇区标签。
  - `tag`/`ax`/`**kwargs`：透传到 `Axes.pie`（如 `autopct`、`startangle` 等）。
- 数据准备：`data_keys=['sizes']`。
- 示例：`add_pie(data=df, sizes='value', labels=['A','B','C'])`
 - 示例（基本饼图）：
 ```python
 plotter.add_pie(data=df, sizes='sizes', labels=['A','B','C'], autopct='%1.1f%%', startangle=90)
 ```

add_donut
- 签名：`add_donut(data, sizes, labels?, width?, radius?, tag?, ax?, **kwargs)`
- 用途：环形图（饼图加空心），通过 `wedgeprops` 控制厚度。
- 参数：
  - `data`：`pd.DataFrame`；`sizes` 列名。
  - `labels`（可选）：序列。
  - `width`（可选）：`float`，环厚度，默认 `0.4`。
  - `radius`（可选）：`float`，外半径，默认 `1.0`。
  - `tag`/`ax`/`**kwargs`：透传到 `Axes.pie`。
- 数据准备：`data_keys=['sizes']`。
- 示例：`add_donut(data=df, sizes='value', labels=['A','B'], width=0.5, radius=1.0)`
 - 示例（环形图）：
 ```python
 plotter.add_donut(data=df, sizes='sizes', labels=['A','B','C'], width=0.4, radius=1.0)
 ```

add_nested_donut
- 签名：`add_nested_donut(outer, inner, tag?, ax?, **kwargs)`
- 用途：双层嵌套环形图，外圈与内圈分别绘制。
- 参数：
  - `outer`：`dict`，必须包含 `data: DataFrame` 与 `sizes: str`；`labels` 可选。
  - `inner`：`dict`，必须包含 `data: DataFrame` 与 `sizes: str`；`labels` 可选。
  - `tag`/`ax`/`**kwargs`：标准参数。
- 数据准备：`data_keys=[]`；内部强制 `kwargs.setdefault('data', pd.DataFrame())` 以满足统一工作流参数要求，但实际数据来源为 `outer/inner`。
- 示例：`add_nested_donut(outer={'data':df_o,'sizes':'size'}, inner={'data':df_i,'sizes':'size'})`
 - 示例（双层嵌套）：
 ```python
 plotter.add_nested_donut(
   outer={'data': df_outer, 'sizes': 'sizes', 'labels': ['A','B','C']},
   inner={'data': df_inner, 'sizes': 'sizes', 'labels': ['a','b','c']}
 )
 ```

add_waterfall
- 签名：`add_waterfall(data, x, deltas, baseline?, colors?, connectors?, width?, tag?, ax?, **kwargs)`
- 用途：以柱状累计展示各阶段增减的瀑布图，支持连接线。
- 参数：
  - `data`：`pd.DataFrame`；`x` 阶段列，`deltas` 变化值列。
  - `baseline`（可选）：初始值，默认 `0.0`。
  - `colors`（可选）：`(pos_color, neg_color)`，默认 `("#2ca02c", "#d62728")`。
  - `connectors`（可选）：是否绘制连接线，默认 `True`。
  - `width`（可选）：柱宽，默认 `0.8`。
  - `tag`/`ax`/`**kwargs`：标准参数。
- 数据准备：`data_keys=['x','deltas']`。
- 行为：计算 `bottoms` 与 `heights`；根据正负选择颜色；设置分类刻度与标签。
- 示例：`add_waterfall(data=df, x='stage', deltas='delta', baseline=100)`
 - 示例（含连接线与颜色）：
 ```python
 plotter.add_waterfall(data=df, x='stage', deltas='delta', baseline=100, colors=("#2ca02c", "#d62728"), connectors=True)
 ```

add_candlestick
- 签名：`add_candlestick(data, time, open, high, low, close, width?, up_color?, down_color?, tag?, ax?, **kwargs)`
- 用途：绘制金融 K 线图（蜡烛与上下影线），自动调整轴范围保证可见。
- 参数：
  - `data`：`pd.DataFrame`；必须包含 `time/open/high/low/close` 列。
  - `width`（可选）：蜡烛宽度，默认 `0.6`。
  - `up_color`（可选）：上涨颜色，默认 `#2ca02c`。
  - `down_color`（可选）：下跌颜色，默认 `#d62728`。
  - `tag`/`ax`/`**kwargs`：标准参数。
- 数据准备：`data_keys=['time','open','high','low','close']`。
- 行为：逐条绘制影线与矩形蜡烛；当实体高度为 0 时使用极小高避免不可见；设置 `xticks` 为时间序列；调用 `ax.relim(); ax.autoscale_view()`。
- 示例：`add_candlestick(data=df, time='date', open='open', high='high', low='low', close='close')`
 - 示例（K 线图）：
 ```python
 plotter.add_candlestick(data=df, time='date', open='open', high='high', low='low', close='close', up_color='#2ca02c', down_color='#d62728')
 ```

add_scatter
- 签名：`add_scatter(data?, x, y, s?, c?, tag?, ax?, **kwargs)`
- 用途：散点图；按列控制点大小（`s`）与颜色（`c`）。
- 参数：
  - `data`（可选）：`pd.DataFrame`；`x/y` 必须是列名；若 `s/c` 为字符串则视为列名并参与数据准备。
  - `x/y`：`str | array-like`。
  - `s/c`（可选）：`str | array-like`；字符串表示数据列；数组模式直接使用数组。
  - `tag`/`ax`/`**kwargs`：透传到 `Axes.scatter`（如 `cmap`、`alpha`、`marker` 等）。
- 默认样式：`plot_defaults_key='scatter'`（`s=30, alpha=0.7`）。
- 返回：`mappable`（`PathCollection`），便于后续 `fig.colorbar`。
- 数据准备：`data_keys=['x','y']`，若 `s/c` 在 `kwargs` 中且为字符串，则动态加入数据键。
- 示例：`add_scatter(data=df, x='x', y='y', c='z', cmap='viridis')`
 - 示例（按列着色与大小）：
 ```python
 plotter.add_scatter(data=df, x='x', y='y', c='z', s='size', cmap='viridis', alpha=0.8)
 ```
 - 示例（数组模式）：
 ```python
 plotter.add_scatter(x=[1,2,3], y=[3,2,4], s=30)
 ```

add_hist
- 签名：`add_hist(data?, x, tag?, ax?, **kwargs)`
- 用途：直方图。
- 参数：
  - `data`（可选）：`pd.DataFrame`；`x` 为列名；否则 `x` 为数组。
  - `x`：`str | array-like`。
  - `tag`/`ax`/`**kwargs`：透传到 `Axes.hist`（如 `bins`、`range`、`density`、`color`）。
- 默认样式：`plot_defaults_key='hist'`（`bins=20, alpha=0.75`）。
- 数据准备：`data_keys=['x']`。
- 示例：`add_hist(data=df, x='value', bins=30)`
 - 示例（基本）：
 ```python
 plotter.add_hist(data=df, x='value', bins=30, density=True, alpha=0.7)
 ```
 - 示例（数组模式）：
 ```python
 plotter.add_hist(x=np.random.randn(1000), bins=40)
 ```

add_box
- 签名：`add_box(data?, x, y, hue?, tag?, ax?, **kwargs)`
- 用途：箱线图（封装 `seaborn.boxplot`）。
- 参数：
  - `data`：`pd.DataFrame`；`x/y` 为列名；`hue` 为可选分组列。
  - `tag`/`ax`/`**kwargs`：透传到 `sns.boxplot`（如 `order`、`palette`、`linewidth`）。
- 数据准备：`data_keys=['x','y','hue']`（`hue` 可选）。
- 示例：`add_box(data=df, x='group', y='value', hue='cond')`
 - 示例（分组箱线图）：
 ```python
 plotter.add_box(data=df, x='group', y='value', hue='cond', palette='Set2')
 ```

add_heatmap
- 签名：`add_heatmap(data, tag?, ax?, cbar?, **kwargs)`
- 用途：热图（封装 `seaborn.heatmap`）。
- 参数：
  - `data`：`pd.DataFrame`（二维矩阵）。
  - `cbar`（可选）：`bool` 是否绘制颜色条，默认 `True`。
  - `tag`/`ax`/`**kwargs`：透传 `sns.heatmap`（如 `cmap`、`annot`、`fmt`、`linewidths`）。
- 智能样式：若未指定 `cmap`，根据当前样式的主色自动生成连续色图（`sns.light_palette`）。
- 返回：第一个 `ax.collections` 作为 `mappable`；便于 `cleanup_heatmaps` 与共享色条。
- 数据准备：`data_keys=[]`（直接使用传入的矩阵 DataFrame）。
- 示例：`add_heatmap(data=matrix_df, annot=True)`
 - 示例（自动 cmap 与注释）：
 ```python
 plotter.add_heatmap(data=matrix_df, annot=True, fmt='.2f')
 ```

add_seaborn
- 签名：`add_seaborn(plot_func, data?, x?, y?, hue?, tag?, ax?, **kwargs)`
- 用途：通用 Seaborn 绘制入口；传入任意接受 `data` 与 `ax` 的 Seaborn 函数。
- 参数：
  - `plot_func`：`Callable`（必需），如 `sns.violinplot`、`sns.scatterplot` 等。
  - `data`：`pd.DataFrame`；`x/y/hue/size/style/col/row` 等键根据需要提供。
  - `tag`/`ax`/`**kwargs`：透传到 `plot_func`。
- 数据准备：动态 `data_keys`（从可能键列表与 `kwargs` 对齐）。
- 返回：通常 `None`（多数 Seaborn 函数不返回 mappable）。
- 示例：`add_seaborn(plot_func=sns.violinplot, data=df, x='group', y='value')`
 - 示例（通用 Seaborn）：
 ```python
 import seaborn as sns
 plotter.add_seaborn(plot_func=sns.violinplot, data=df, x='group', y='value', hue='cond')
 ```

add_blank
- 签名：`add_blank(tag?) -> 'Plotter'`
- 用途：在指定或下一个可用子图位置创建空白区域（关闭坐标轴），用于布局占位与排版。
- 参数：`tag`（可选）：目标子图标签；省略时按顺序或复用最后活动子图。
- 行为：解析轴并关闭坐标轴；更新 `last_active_tag`。
 - 示例：
 ```python
 plotter.add_blank(tag='A')
 ```

add_regplot
- 签名：`add_regplot(data?, x, y, tag?, ax?, scatter_kws?, line_kws?, **kwargs)`
- 用途：绘制散点与线性回归拟合（封装 `seaborn.regplot`）。
- 参数：
  - `data`：`pd.DataFrame`；`x/y` 列名。
  - `scatter_kws`（可选）：传给底层散点的参数（会与通用 `scatter` 默认合并，如 `s=30, alpha=0.7`）。
  - `line_kws`（可选）：传给回归线的参数。
  - `tag`/`ax`/`**kwargs`：透传到 `sns.regplot`（如 `order` 用于多项式回归）。
- 数据准备：`data_keys=['x','y']`。
- 返回：`None`。
- 示例：`add_regplot(data=df, x='x', y='y')`
 - 示例（回归拟合）：
 ```python
 plotter.add_regplot(data=df, x='x', y='y', scatter_kws={'s':40}, line_kws={'color':'black'})
 ```

add_conditional_scatter
- 签名：`add_conditional_scatter(data?, x, y, condition, tag?, ax?, **kwargs)`
- 用途：根据布尔条件在散点图上高亮特定数据点，普通点与高亮点样式可独立配置。
- 参数：
  - `data`：`pd.DataFrame`；`x/y` 列名；`condition` 为布尔列或布尔序列。
  - 普通点样式：`s_normal`、`c_normal`、`alpha_normal`、`label_normal`（默认基于 `scatter`）。
  - 高亮点样式：`s_highlight`、`c_highlight`、`alpha_highlight`、`label_highlight`。
  - 其余通用 `scatter` 关键字将同时应用于两组点。
  - `tag`/`ax`：标准参数。
- 数据准备：`data_keys=['x','y','condition']`。
- 返回：高亮点的 `mappable`（便于图例或颜色条）。
- 示例：`add_conditional_scatter(data=df, x='x', y='y', condition='flag')`
 - 示例（高亮条件）：
 ```python
 plotter.add_conditional_scatter(
   data=df, x='x', y='y', condition='flag',
   s_normal=20, c_normal='gray',
   s_highlight=60, c_highlight='red',
   label_highlight='Selected'
 )
 plotter.set_legend()
 ```

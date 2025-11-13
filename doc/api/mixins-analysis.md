---
id: mixins-analysis
title: DataAnalysisPlotsMixin API
sidebar_label: 数据分析
---

add_binned_plot
- 签名：`add_binned_plot(data, x, y, bins?, agg_func?, error_func?, plot_type?, tag?, ax?, **kwargs)`
- 用途：对 `x` 分箱，聚合每箱内 `y` 值（均值/中位数等），并以误差条绘制聚合结果。
- 参数：
  - `data`：`pd.DataFrame`；包含 `x` 与 `y` 列。
  - `x`/`y`：`str` 列名。
  - `bins`（可选）：`int | list` 箱数量或边界，默认 `10`。
  - `agg_func`（可选）：`str` 聚合函数，如 `'mean'|'median'`，默认 `'mean'`。
  - `error_func`（可选）：`str | None` 误差函数，如 `'std'|'sem'`；`None` 不绘制误差，默认 `'std'`。
  - `plot_type`（可选）：目前支持 `'errorbar'`，默认 `'errorbar'`。
  - `tag`/`ax`/`**kwargs`：透传至 `Axes.errorbar`（如 `fmt`）。
- 默认：`fmt='o-'`。
- 数据准备：`data_keys=['x','y']`。
- 示例：
```python
plotter.add_binned_plot(data=df, x='x', y='y', bins=20, agg_func='median', error_func='sem', fmt='o-')
```

add_distribution_fit
- 签名：`add_distribution_fit(data?, x, dist_name?, tag?, ax?, **kwargs)`
- 用途：在当前直方图上拟合数据到指定概率分布并绘制其 PDF 曲线。
- 参数：
  - `data`（可选）：`pd.DataFrame`；`x` 为列名；否则 `x` 可为数组（将组装 DataFrame）。
  - `x`：`str | array-like`。
  - `dist_name`（可选）：要拟合的分布名（`scipy.stats`），默认 `'norm'`。
  - `tag`/`ax`/`**kwargs`：透传至 `Axes.plot`（如 `color`、`linestyle`、`label`）。
- 行为：使用 `scipy.stats.<dist>`，`fit` 得到参数，按当前轴 `xlim` 生成密度曲线并绘制；自动生成易读的图例标签（对于 `'norm'` 显示 μ/σ）。
- 数据准备：`data_keys=['x']`。
- 示例：
```python
plotter.add_hist(data=df, x='x', bins=40)
plotter.add_distribution_fit(data=df, x='x', dist_name='lognorm')
plotter.set_legend()
```

---
id: mixins-analysis
title: DataAnalysisPlotsMixin API
sidebar_label: 数据分析
---

## 概述

`DataAnalysisPlotsMixin` 包含用于常见数据分析任务的绘图方法，如数据分箱和分布拟合。

---

### `add_binned_plot`
- **签名**: `add_binned_plot(data, x, y, bins?, agg_func?, error_func?, plot_type?, ...)`
- **用途**: 对数据进行分箱、聚合，并以误差条的形式绘制聚合结果。这对于观察一个变量在另一个变量的不同区间内的趋势非常有用。
- **核心参数**:
  - `data`: `pd.DataFrame`, 包含绘图数据。
  - `x`: `str`, 要进行分箱的数值列名。
  - `y`: `str`, 要进行聚合的数值列名。
  - `bins`: `int` 或 `list` (可选), 分箱的数量或自定义的箱体边界。默认为 `10`。
  - `agg_func`: `str` (可选), 用于聚合Y值的函数名，如 `'mean'`, `'median'`。默认为 `'mean'`。
  - `error_func`: `str` (可选), 用于计算误差的函数名，如 `'std'` (标准差), `'sem'` (标准误差)。如果为 `None`，则不绘制误差条。默认为 `'std'`。
  - `plot_type`: `str` (可选), 目前仅支持 `'errorbar'`。
- **默认样式**: `fmt='o-'` (带点的实线)。
- **示例**:
```python
# 将 'x' 分为20个箱，计算每个箱内 'y' 的中位数和标准误差，并绘制
plotter.add_binned_plot(
    data=df, x='x_values', y='y_values', 
    bins=20, agg_func='median', error_func='sem'
)
```

---

### `add_distribution_fit`
- **签名**: `add_distribution_fit(data?, x, dist_name?, ...)`
- **用途**: 在现有的直方图上，拟合数据到指定的概率分布并绘制其概率密度函数（PDF）曲线。这对于检验数据是否符合某种理论分布非常有用。
- **使用前提**: 通常在调用 `add_hist` 之后使用。
- **核心参数**:
  - `x`: `str` 或 `array-like`, 要拟合的数据或 `data` 中的列名。
  - `dist_name`: `str` (可选), 要拟合的 `scipy.stats` 中的分布名称，如 `'norm'`, `'lognorm'`, `'gamma'` 等。默认为 `'norm'` (正态分布)。
  - `**kwargs`: 其他传递给 `ax.plot` 的关键字参数，用于定制PDF曲线的样式（如 `color`, `linestyle`）。
- **智能图例**: 方法会自动生成包含拟合参数的图例标签，例如 `Fitted norm (μ=..., σ=...)`。
- **示例**:
```python
# 先绘制直方图
plotter.add_hist(data=df, x='data_samples', bins=40, density=True)
# 在同一子图上添加对数正态分布的拟合曲线
plotter.add_distribution_fit(data=df, x='data_samples', dist_name='lognorm')
plotter.set_legend()
```
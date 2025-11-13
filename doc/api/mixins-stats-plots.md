---
id: mixins-stats-plots
title: StatsPlotsMixin API
sidebar_label: 统计图（Seaborn）
---

## 概述

`StatsPlotsMixin` 提供了基于 Seaborn 库的常用统计图表，用于探索性数据分析和分布可视化。

---

### `add_violin`
- **签名**: `add_violin(data?, x, y, hue?, ...)`
- **用途**: 绘制小提琴图，它结合了箱形图和核密度估计图的特点，用于展示数值数据的分布并进行比较。
- **核心参数**:
  - `data`: `pd.DataFrame` (可选)。
  - `x`: `str` 或 `array-like`, 分类变量。
  - `y`: `str` 或 `array-like`, 数值变量。
  - `hue`: `str` (可选), 用于进一步分组的第二个分类变量。
  - `**kwargs`: 其他传递给 `seaborn.violinplot` 的参数，如 `order`, `palette`, `cut`, `scale`。
- **示例**:
```python
import seaborn as sns
tips = sns.load_dataset("tips")
plotter.add_violin(data=tips, x='day', y='total_bill', hue='smoker')
```

---

### `add_swarm`
- **签名**: `add_swarm(data?, x, y, hue?, ...)`
- **用途**: 绘制蜂群图，这是一种分类散点图，其中点被调整以避免重叠。它能很好地展示值的分布情况。
- **使用建议**: 常与 `add_violin` 或 `add_box` 叠加使用，以同时显示分布的摘要和单个数据点。
- **核心参数**:
  - `data`, `x`, `y`, `hue`: 与 `add_violin` 类似。
  - `**kwargs`: 其他传递给 `seaborn.swarmplot` 的参数，如 `size`, `palette`。
- **示例**:
```python
# 在小提琴图上叠加蜂群图
plotter.add_violin(data=tips, x='day', y='total_bill')
plotter.add_swarm(data=tips, x='day', y='total_bill', color='black', size=3)
```

---

### `add_joint`
- **签名**: `add_joint(data, x, y, **kwargs)`
- **用途**: 绘制联合分布图，用于可视化两个变量的联合分布和各自的边缘分布。
- **警告**: 此方法会创建一个**新的 Figure** 并替换 `Plotter` 实例中原有的 `fig` 和 `axes`。调用此方法后，之前的所有子图都将被清除。
- **核心参数**:
  - `data`: `pd.DataFrame`。
  - `x`, `y`: `str`, 要分析的两个变量的列名。
  - `kind`: `str` (可选), `'scatter'` (默认), `'kde'`, `'hist'`, `'hex'`, `'reg'`, `'resid'`。
  - `height`: `float` (可选), 图形的高度。
- **示例**:
```python
# 这个调用会替换整个画布
plotter.add_joint(data=iris, x='sepal_width', y='sepal_length', kind='kde')
```

---

### `add_pair`
- **签名**: `add_pair(data, **kwargs)`
- **用途**: 绘制数据集中多个变量两两之间的关系网格。对角线通常是单个变量的分布图（直方图或KDE），非对角线是两个变量的散点图。
- **警告**: 与 `add_joint` 类似，此方法也会**替换整个 Figure**。由于其创建的是一个复杂的 `PairGrid`，后续的链式修饰器可能无法准确定位到某个子图。
- **核心参数**:
  - `data`: `pd.DataFrame`。
  - `hue`: `str` (可选), 用于按类别着色的列名。
  - `kind`: `str` (可选), 非对角线图的类型, `'scatter'` (默认) 或 `'reg'`。
  - `diag_kind`: `str` (可选), 对角线图的类型, `'auto'` (默认), `'hist'`, `'kde'`。
- **示例**:
```python
# 这个调用会替换整个画布
plotter.add_pair(data=iris, hue='species')
```
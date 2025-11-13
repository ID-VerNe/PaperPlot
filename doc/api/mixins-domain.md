---
id: mixins-domain
title: DomainSpecificPlotsMixin API
sidebar_label: 领域图表
---

概述
- 面向电力系统、机器学习分类等常见领域的专用图表封装，均遵循统一数据输入范式（DataFrame 列名模式优先、数组模式次选）。

add_spectra
- 签名：`add_spectra(data?, x, y_cols, offset?, tag?, ax?, **kwargs)`
- 用途：在同一子图绘制多条光谱并按 `offset` 垂直偏移，避免重叠比较多个谱线。
- 参数：
  - `data`（可选）：`pd.DataFrame`；`x` 为列名；`y_cols` 为列名列表。
  - `x`：`str | array-like`；`y_cols`：`List[str] | List[array-like]`。
  - `offset`（可选）：`float`，各谱线的垂直间距，默认 `0`。
  - `tag`/`ax`/`**kwargs`：透传至 `Axes.plot`（如 `color`、`linestyle` 等）。
- 数据准备：当 `data=None` 时，`y_cols` 支持数组列表；内部自动组装缓存 DataFrame。
- 示例（DataFrame 模式）：
```python
plotter.add_spectra(data=df, x='wavenumber', y_cols=['s1','s2','s3'], offset=0.2)
plotter.set_legend()
```
- 示例（数组模式）：
```python
plotter.add_spectra(x=wn, y_cols=[spec1, spec2], offset=0.1)
```

add_concentration_map
- 签名：`add_concentration_map(data, tag?, ax?, cbar?, xlabel?, ylabel?, **kwargs)`
- 用途：浓度图/SERS Mapping 热图，封装 `sns.heatmap` 并设置领域默认。
- 参数：
  - `data`：`pd.DataFrame`（二维矩阵）。
  - `cbar`（可选）：`bool`，默认 `True`。
  - `xlabel`/`ylabel`（可选）：默认 `'X (μm)'`、`'Y (μm)'`。
  - `tag`/`ax`/`**kwargs`：透传至 `sns.heatmap`（如 `annot`、`fmt`）。
- 默认样式：`cmap='inferno'`。
- 返回：第一个 `ax.collections` 作为 mappable（便于 colorbar）。
- 示例：
```python
plotter.add_concentration_map(data=matrix_df, annot=True)
```

add_confusion_matrix
- 签名：`add_confusion_matrix(matrix, class_names, normalize?, tag?, ax?, **kwargs)`
- 用途：分类任务的混淆矩阵可视化；支持归一化显示比例。
- 参数：
  - `matrix`：`array-like`，形状 `(n_classes, n_classes)`。
  - `class_names`：`List[str]` 行列标签。
  - `normalize`（可选）：`bool`，默认 `False`；为 `True` 时按行归一化并使用 `fmt='.2f'`。
  - `tag`/`ax`/`**kwargs`：透传至 `sns.heatmap`（如 `cmap`、`annot`、`fmt`）。
- 默认：`annot=True`、`fmt='d'`、`cmap='Blues'`。
- 示例：
```python
plotter.add_confusion_matrix(matrix=cm, class_names=['A','B','C'], normalize=True)
```

add_roc_curve
- 签名：`add_roc_curve(fpr, tpr, roc_auc, tag?, ax?, **kwargs)`
- 用途：多分类 ROC 曲线；自动添加对角参考线与标题、范围、图例。
- 参数：
  - `fpr`/`tpr`：`Dict[str, np.ndarray]`，键为类别名。
  - `roc_auc`：`Dict[str, float]` AUC 分数。
  - `tag`/`ax`/`**kwargs`：透传至 `Axes.plot`（主曲线）。
- 行为：每类构造 `label='{class} (AUC=...)'` 并绘制，加入 `[0,1]` 对角线，设置坐标范围与标签。
- 示例：
```python
plotter.add_roc_curve(fpr=fpr_dict, tpr=tpr_dict, roc_auc=auc_dict)
```

add_pca_scatter
- 签名：`add_pca_scatter(data?, x_pc, y_pc, hue?, tag?, ax?, **kwargs)`
- 用途：PCA 结果散点图，封装 `sns.scatterplot`。
- 参数：
  - `data`：`pd.DataFrame`；`x_pc`、`y_pc` 为列名；`hue` 可选分组列。
  - `tag`/`ax`/`**kwargs`：透传至 `sns.scatterplot`。
- 返回：`PathCollection` 作为 mappable（若存在）。
- 示例：
```python
plotter.add_pca_scatter(data=df, x_pc='PC1', y_pc='PC2', hue='label')
plotter.set_legend()
```

add_power_timeseries
- 签名：`add_power_timeseries(data, x, y_cols, events?, tag?, ax?, **kwargs)`
- 用途：电力系统动态仿真变量时序图，支持事件标记。
- 参数：
  - `data`：`pd.DataFrame`；`x` 时间列；`y_cols` 变量列列表。
  - `events`（可选）：`Dict[str, float]` 事件标签到时间位置。
  - `tag`/`ax`/`**kwargs`：透传至 `Axes.plot`（线样式等）。
- 行为：循环绘制各变量线，自动生成图例与轴标签；若提供 `events`，调用 `add_event_markers` 添加竖线与文本。
- 示例：
```python
plotter.add_power_timeseries(data=df, x='t', y_cols=['v','i'], events={'Trip':0.5, 'Reclose':1.2})
plotter.set_legend()
```

add_phasor_diagram
- 签名：`add_phasor_diagram(magnitudes, angles, labels?, angle_unit?, tag?, ax?, **kwargs)`
- 用途：在极坐标子图上绘制相量（箭头注释）与文本标签，生成图例。
- 轴要求：目标轴为极坐标；可通过 `ax_configs` 设置。
- 参数：
  - `magnitudes`：`List[float]` 幅值。
  - `angles`：`List[float]` 角度。
  - `labels`（可选）：`List[str]`。
  - `angle_unit`（可选）：`'degrees' | 'radians'`，默认 `'degrees'`。
  - `tag`/`ax`/`**kwargs`：透传至 `ax.text`（文本风格）。
- 行为：设置极坐标方向，转换角度为弧度，绘制箭头与文本偏移，组装 `Line2D` 用于图例。
- 示例：
```python
plotter = Plotter(layout=[['P']], ax_configs={'P': {'projection': 'polar'}})
plotter.add_phasor_diagram(magnitudes=[1.0, 0.8], angles=[0, 120], labels=['V','I'], tag='P')
```

add_bifurcation_diagram
- 签名：`add_bifurcation_diagram(data?, x, y, tag?, ax?, **kwargs)`
- 用途：电力系统稳定性分析的分岔图（散点）。
- 参数：
  - `data`（可选）：`pd.DataFrame`；`x/y` 列名；或数组模式。
  - `tag`/`ax`/`**kwargs`：透传至 `Axes.scatter`。
- 默认样式：`plot_defaults_key='bifurcation'`（如 `s=0.5, alpha=0.1, marker='.', color='black', rasterized=True`）。
- 行为：绘制散点与默认轴标题；通常不返回 mappable。
- 示例：
```python
plotter.add_bifurcation_diagram(data=df, x='param', y='state')
plotter.set_title('Bifurcation')
plotter.set_xlabel('Bifurcation Parameter')
plotter.set_ylabel('State Variable')
```

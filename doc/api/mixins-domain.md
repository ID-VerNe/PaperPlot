---
id: mixins-domain
title: DomainSpecificPlotsMixin API
sidebar_label: 领域图表
---

## 概述

`DomainSpecificPlotsMixin` 提供了一系列封装好的、面向特定科研或工程领域的专用图表。这些方法通常有更具体的参数名，并内置了符合领域惯例的默认样式和行为。

---

### `add_spectra`
- **签名**: `add_spectra(data?, x, y_cols, offset?, ...)`
- **用途**: 在同一子图上绘制多条光谱，并通过 `offset` 参数将它们垂直偏移，便于比较。常用于拉曼光谱、红外光谱等。
- **核心参数**:
  - `x`: `str` 或 `array-like`, 光谱的X轴（如波数、波长）。
  - `y_cols`: `List[str]` 或 `List[array-like]`, 包含多条光谱强度数据的列名或数组列表。
  - `offset`: `float` (可选), 每条光谱之间的垂直偏移量。
- **示例**: `plotter.add_spectra(data=df, x='wavenumber', y_cols=['sample1', 'sample2'], offset=0.5)`

---

### `add_concentration_map`
- **签名**: `add_concentration_map(data, cbar?, xlabel?, ylabel?, ...)`
- **用途**: 绘制浓度图或SERS Mapping图。本质上是 `sns.heatmap` 的一个封装，但带有领域特定的默认值（如 `cmap='inferno'` 和坐标轴标签）。
- **核心参数**:
  - `data`: `pd.DataFrame`, 二维矩阵数据。
  - `xlabel`/`ylabel`: (可选) 坐标轴标签，默认为 `'X (μm)'` 和 `'Y (μm)'`。
- **示例**: `plotter.add_concentration_map(data=matrix_df, annot=True, cbar_kws={'label': 'Intensity'})`

---

### `add_confusion_matrix`
- **签名**: `add_confusion_matrix(matrix, class_names, normalize?, ...)`
- **用途**: 可视化分类模型的混淆矩阵。
- **核心参数**:
  - `matrix`: `array-like`, 形状为 `(n_classes, n_classes)` 的混淆矩阵。
  - `class_names`: `List[str]`, 类别名称，用于矩阵的行和列标签。
  - `normalize`: `bool` (可选), 如果为 `True`，则将矩阵按行归一化以显示百分比。
- **示例**: `plotter.add_confusion_matrix(matrix=cm, class_names=['Cat', 'Dog'], normalize=True)`

---

### `add_roc_curve`
- **签名**: `add_roc_curve(fpr, tpr, roc_auc, ...)`
- **用途**: 绘制一个或多个分类的ROC（接收者操作特征）曲线。该方法会自动添加对角参考线和包含AUC分数的图例。
- **核心参数**:
  - `fpr`: `Dict[str, np.ndarray]`, 键为类别名，值为假正率数组。
  - `tpr`: `Dict[str, np.ndarray]`, 键为类别名，值为真正率数组。
  - `roc_auc`: `Dict[str, float]`, 键为类别名，值为AUC分数。
- **示例**: `plotter.add_roc_curve(fpr=fpr_dict, tpr=tpr_dict, roc_auc=auc_dict)`

---

### `add_pca_scatter`
- **签名**: `add_pca_scatter(data?, x_pc, y_pc, hue?, ...)`
- **用途**: 绘制主成分分析（PCA）结果的散点图，是 `sns.scatterplot` 的一个简单封装。
- **核心参数**:
  - `x_pc`, `y_pc`: `str` 或 `array-like`, 通常是第一和第二主成分。
  - `hue`: `str` (可选), 用于分组着色的分类变量列名。
- **示例**: `plotter.add_pca_scatter(data=df, x_pc='PC1', y_pc='PC2', hue='cluster')`

---

### `add_power_timeseries`
- **签名**: `add_power_timeseries(data, x, y_cols, events?, ...)`
- **用途**: 绘制电力系统动态仿真结果的时间序列图，并支持自动标记事件点。
- **核心参数**:
  - `x`: `str`, 时间列名。
  - `y_cols`: `List[str]`, 要绘制的一个或多个变量的列名。
  - `events`: `Dict[str, float]` (可选), 键是事件描述，值是事件发生的时间点。
- **示例**: `plotter.add_power_timeseries(data=df, x='time', y_cols=['Voltage', 'Frequency'], events={'Fault': 1.0})`

---

### `add_phasor_diagram`
- **签名**: `add_phasor_diagram(magnitudes, angles, labels?, angle_unit?, ...)`
- **用途**: 在极坐标子图上绘制相量图，常用于电气工程。
- **轴要求**: 目标轴必须是极坐标投影。
- **核心参数**:
  - `magnitudes`: `List[float]`, 相量幅值列表。
  - `angles`: `List[float]`, 相量角度列表。
  - `angle_unit`: `'degrees'` (默认) 或 `'radians'`。
- **示例**: `plotter.add_phasor_diagram(magnitudes=[1.0, 0.8], angles=[0, -90], labels=['V', 'I'])`

---

### `add_bifurcation_diagram`
- **签名**: `add_bifurcation_diagram(data?, x, y, ...)`
- **用途**: 绘制分岔图，常用于非线性系统和稳定性分析。这本质上是一个经过优化的散点图，使用小而半透明的点来揭示系统的动态行为。
- **默认样式**: `plot_defaults_key='bifurcation'` (使用 `s=0.5, alpha=0.1, marker='.', rasterized=True`)，以获得最佳视觉效果。
- **核心参数**:
  - `x`: `str` 或 `array-like`, 分岔参数。
  - `y`: `str` 或 `array-like`, 系统状态变量。
- **示例**: `plotter.add_bifurcation_diagram(data=df, x='r', y='x_steady_state')`
---
id: mixins-three-d
title: ThreeDPlotsMixin API
sidebar_label: 3D 图表
---

## 概述

`ThreeDPlotsMixin` 提供了用于创建三维图表的方法。要使用这些方法，必须在 `Plotter` 初始化时通过 `ax_configs` 参数将目标子图的投影设置为 `'3d'`。

```python
# 初始化一个带3D子图的Plotter
plotter = Plotter(
    layout=(1, 2), 
    ax_configs={
        'ax00': {'projection': '3d'}, 
        'ax01': {'projection': '3d'}
    }
)
```

---

### `add_scatter3d`
- **签名**: `add_scatter3d(data?, x, y, z, tag?, ax?, **kwargs)`
- **用途**: 在3D子图上绘制散点图。
- **核心参数**:
  - `data`: `pd.DataFrame` (可选)。
  - `x`, `y`, `z`: `str` (列名) 或 `array-like` (数据)。
  - `**kwargs`: 其他传递给 `Axes.scatter` 的参数，如 `c` (颜色), `s` (大小), `cmap`, `marker`。
- **返回**: 返回 `mappable` 对象，可用于创建颜色条。
- **示例**:
```python
plotter.add_scatter3d(
    data=df, x='x_coord', y='y_coord', z='z_coord', 
    c='value', cmap='viridis', tag='ax00'
)
```

---

### `add_line3d`
- **签名**: `add_line3d(data?, x, y, z, tag?, ax?, **kwargs)`
- **用途**: 在3D子图上绘制线图。
- **核心参数**:
  - `data`: `pd.DataFrame` (可选)。
  - `x`, `y`, `z`: `str` (列名) 或 `array-like` (数据)。
  - `**kwargs`: 其他传递给 `Axes.plot` 的参数，如 `color`, `linestyle`, `marker`。
- **示例**:
```python
plotter.add_line3d(
    data=df_trajectory, x='x', y='y', z='z', 
    color='blue', tag='ax00'
)
```

---

### `add_surface`
- **签名**: `add_surface(X, Y, Z, tag?, ax?, **kwargs)`
- **用途**: 在3D子图上绘制表面图。此方法需要二维网格数组作为输入。
- **核心参数**:
  - `X`, `Y`, `Z`: `np.ndarray`, 二维数组，分别表示表面的x, y, z坐标。通常由 `np.meshgrid` 生成。
  - `**kwargs`: 其他传递给 `Axes.plot_surface` 的参数，如 `cmap`, `rstride`, `cstride`。
- **返回**: 返回 `mappable` 对象。
- **示例**:
```python
X, Y = np.meshgrid(x_range, y_range)
Z = calculate_z(X, Y)
plotter.add_surface(X=X, Y=Y, Z=Z, cmap='viridis', tag='ax01')
```

---

### `add_wireframe`
- **签名**: `add_wireframe(X, Y, Z, tag?, ax?, **kwargs)`
- **用途**: 在3D子图上绘制线框图。
- **核心参数**:
  - `X`, `Y`, `Z`: `np.ndarray`, 二维网格数组。
  - `**kwargs`: 其他传递给 `Axes.plot_wireframe` 的参数，如 `color`, `rstride`, `cstride`。
- **示例**:
```python
plotter.add_wireframe(X=X, Y=Y, Z=Z, color='gray', tag='ax01')
```
---
id: mixins-three-d
title: ThreeDPlotsMixin API
sidebar_label: 3D 图表
---

概述
- 3D 投影的散点、线、表面与线框。目标轴需在初始化指定 `projection='3d'`。

add_scatter3d
- 签名：`add_scatter3d(data?, x, y, z, tag?, ax?, **kwargs)`
- 用途：3D 散点，封装 `Axes.scatter`；返回 mappable。
- 参数：
  - `data`（可选）：`pd.DataFrame`；`x/y/z` 列名；或数组模式。
  - `tag`/`ax`/`**kwargs`：如 `c`、`s`、`cmap`、`marker`、`alpha`。
- 轴要求：非 3D 投影将抛出类型错误。
- 示例：
```python
plotter = Plotter(layout=(1,1), ax_configs={'ax00': {'projection':'3d'}})
plotter.add_scatter3d(data=df, x='x', y='y', z='z', c='z', cmap='viridis')
```

add_line3d
- 签名：`add_line3d(data?, x, y, z, tag?, ax?, **kwargs)`
- 用途：3D 线；封装 `Axes.plot`。
- 参数：同上。
- 示例：
```python
plotter.add_line3d(data=df, x='x', y='y', z='z', color='tab:blue')
```

add_surface
- 签名：`add_surface(X, Y, Z, tag?, ax?, **kwargs)`
- 用途：3D 表面；输入为二维数组，封装 `Axes.plot_surface`。
- 参数：
  - `X/Y/Z`：`np.ndarray`，二维网格与高度。
  - `tag`/`ax`/`**kwargs`：如 `cmap='viridis'`。
- 示例：
```python
plotter.add_surface(X=Xp, Y=Yp, Z=Zp, cmap='viridis')
```

add_wireframe
- 签名：`add_wireframe(X, Y, Z, tag?, ax?, **kwargs)`
- 用途：3D 线框；输入为二维数组，封装 `Axes.plot_wireframe`。
- 示例：
```python
plotter.add_wireframe(X=Xp, Y=Yp, Z=Zp, color='gray')
```

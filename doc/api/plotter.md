---
id: plotter
title: Plotter 类 API
sidebar_label: Plotter
---

概述
- `paperplot.core.Plotter` 是入口类，负责画布创建、布局解析、轴对象与状态管理、样式应用。
- 支持简单网格、马赛克布局与嵌套布局；支持在初始化时为特定子图设置投影（如极坐标、3D）。

构造函数
- 签名：`Plotter(layout, style='marin_kitagawa', figsize=None, subplot_aspect=None, ax_configs=None, layout_engine='constrained', **fig_kwargs)`
- 参数：
  - `layout`：`(rows, cols)` 简单网格，或 `List[List[str]]` 马赛克布局，或嵌套 `dict`
  - `style`：样式名称，对应 `paperplot/styles/*.mplstyle`
  - `figsize`：画布尺寸 `(width, height)` 英寸。与 `subplot_aspect` 互斥
  - `subplot_aspect`：单元格宽高比 `(w, h)`，提供时自动计算整体 `figsize`
  - `ax_configs`：按 tag 或 `(row,col)` 设置子图参数，如 `{'P': {'projection': 'polar'}}`
  - `layout_engine`：Matplotlib 布局引擎，默认 `'constrained'`
  - `**fig_kwargs`：透传给 `plt.figure`
- 行为：
  - 创建 `fig`、`axes` 与 `tag_to_ax`
  - 解析马赛克或嵌套布局，注册各子图；简单网格以 `axRC` 命名（如 `ax01`）
  - 维护 `last_active_tag`、`data_cache`、`tag_to_mappable` 等状态
  - 颜色管理器：`self.color_manager` 用于系列颜色一致性

公共方法
- `get_ax(tag) -> plt.Axes`
  - 说明：按标签获取子图轴对象；若不存在抛出 `TagNotFoundError`
- `get_ax_by_name(name: str) -> plt.Axes`
  - 说明：在马赛克/嵌套布局中按名称获取轴；名称为布局定义中的字符串键

工作流要点
- 所有 `add_*` 方法统一通过内部 `_execute_plot`：解析轴、准备数据（DataFrame 列或原生数组）、合并默认样式、执行绘制、缓存数据与 mappable、更新活动 tag
- 与修饰器链式组合：如 `set_title`、`set_legend`、`cleanup`、`save`

示例
```
from paperplot import Plotter
import pandas as pd

df = pd.DataFrame({'time':[1,2,3], 'value':[2,4,3]})
(
  Plotter(layout=(1,2), style='marin_kitagawa')
  .add_line(data=df, x='time', y='value', tag='ax00', label='Series A')
  .set_title('Line', tag='ax00')
  .add_hist(data=df, x='value', tag='ax01')
  .set_title('Hist', tag='ax01')
  .cleanup(align_labels=True)
  .save('example.png')
)
```


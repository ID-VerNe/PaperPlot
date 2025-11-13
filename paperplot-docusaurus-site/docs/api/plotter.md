---
id: plotter
title: Plotter 类 API
sidebar_label: Plotter
---

## 概述

`paperplot.core.Plotter` 是整个库的入口点和核心控制器。它负责：
- **画布与布局管理**: 根据用户定义创建 Matplotlib 的 Figure 和 Axes 对象。支持简单网格、马赛克布局和声明式嵌套布局。
- **状态维护**: 追踪当前活动的子图 (`last_active_tag`)、缓存每个子图使用的数据 (`data_cache`)、管理孪生轴 (`twin_axes`) 和其他状态。
- **样式应用**: 在初始化时应用全局样式表。
- **链式调用**: 所有绘图和修饰方法都返回 `self`，以实现流畅的链式API。

## 构造函数

- **签名**: `Plotter(layout, style='marin_kitagawa', figsize=None, subplot_aspect=None, ax_configs=None, layout_engine='constrained', **fig_kwargs)`
- **参数**:
  - `layout` (`Union[Tuple[int, int], List[List[str]], Dict]`): 定义子图布局。
    - **简单网格**: `(rows, cols)` 元组，如 `(2, 3)`。
    - **马赛克布局**: `List[List[str]]`，如 `[['A', 'A', 'B'], ['C', 'D', 'B']]`。
    - **嵌套布局**: `Dict`，使用 `'main'` 和 `'subgrids'` 键来定义层级结构。
  - `style` (`str`, optional): 样式名称，对应 `paperplot/styles/*.mplstyle` 文件。默认为 `'marin_kitagawa'`。
  - `figsize` (`Tuple[float, float]`, optional): 画布尺寸 `(width, height)`，单位为英寸。与 `subplot_aspect` 互斥。
  - `subplot_aspect` (`Tuple[float, float]`, optional): **单个子图单元格**的宽高比 `(width, height)`。如果提供此参数，`figsize` 将被自动计算以保证子图比例，这对于确保图表专业性非常有用。
  - `ax_configs` (`Dict`, optional): 按 `tag` 或 `(row,col)` 为特定子图预设参数，如 `{'polar_plot': {'projection': 'polar'}}` 或 `{'ax01': {'projection': '3d'}}`。
  - `layout_engine` (`str`, optional): Matplotlib 的布局引擎，如 `'constrained'` 或 `'tight'`。默认为 `'constrained'`。
  - `**fig_kwargs`: 其他任何传递给 `matplotlib.pyplot.figure` 的关键字参数。

## 核心公共方法

### `get_ax(tag)`
- **说明**: 通过标签（tag）获取对应的 Matplotlib `Axes` 对象。这是进行高级定制或使用原生 Matplotlib API 的“逃生舱口”。
- **参数**: `tag` (`Union[str, int]`) - 子图的唯一标识符。
- **返回**: `plt.Axes` 对象。
- **抛出**: `TagNotFoundError` - 如果指定的 `tag` 未找到。

### `get_ax_by_name(name)`
- **说明**: 在马赛克或嵌套布局中，通过布局时定义的**名称**获取对应的 `Axes` 对象。
- **参数**: `name` (`str`) - 布局定义中的字符串键。
- **返回**: `plt.Axes` 对象。
- **抛出**: `ValueError` - 如果布局中不存在指定的名称。

## 工作流与内部机制

- **统一绘图入口 `_execute_plot`**: 所有 `add_*` 方法都通过此内部方法执行。它负责解析目标轴、准备数据、合并默认样式、调用具体绘图逻辑、缓存结果并更新活动 `tag`。
- **数据准备 `_prepare_data`**: 无论输入是 `data=df, x='col'` 还是 `x=[...], y=[...]`，此方法都会将其统一为 Pandas `DataFrame` 和 `Series`，以便后续处理和缓存。
- **颜色管理 `ColorManager`**: `Plotter` 实例包含一个 `ColorManager`。当绘图方法传入 `label` 且未指定 `color` 时，管理器会为该 `label` 分配一个稳定、可复用的颜色，确保在不同子图中同一系列的颜色一致。
- **延迟绘制队列 `_draw_on_save_queue`**: 像 `add_subplot_labels` 这样的功能，其位置依赖于最终的画布布局。为了确保准确性，它们的绘制操作被添加到一个队列中，直到调用 `save()` 方法时才执行。

## 示例

```python
import paperplot as pp
import pandas as pd

# 示例1: 简单网格
plotter = pp.Plotter(layout=(1, 2), figsize=(10, 4))
plotter.add_line(..., tag='ax00').set_title('Left Plot')
plotter.add_scatter(..., tag='ax01').set_title('Right Plot')
plotter.save('simple_grid.png')

# 示例2: 马赛克布局与固定宽高比
layout = [['A', 'A'], ['B', 'C']]
plotter_mosaic = pp.Plotter(layout=layout, subplot_aspect=(4, 3))
plotter_mosaic.add_heatmap(..., tag='A')
plotter_mosaic.add_bar(..., tag='B')
plotter_mosaic.save('mosaic_aspect.png')

# 示例3: 嵌套布局
nested_layout = {
    'main': [['overview', 'details']],
    'subgrids': {
        'details': {'layout': [['detail1'], ['detail2']]}
    }
}
plotter_nested = pp.Plotter(layout=nested_layout)
plotter_nested.add_line(..., tag='overview')
plotter_nested.add_line(..., tag='details.detail1') # 使用层级tag
plotter_nested.save('nested_plot.png')
```
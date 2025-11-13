---
id: mixins-modifiers
title: ModifiersMixin API
sidebar_label: 修饰与轴管理
---

## 概述

`ModifiersMixin` 包含了大量用于修饰、装饰和最终确定图表的方法。这些方法分为几类：子图和画布层面的标注、坐标轴管理、图例控制、孪生轴、嵌入内容以及收尾工具。

---

## 子图标签与分组

### `add_subplot_labels`
- **用途**: 为子图添加自动编号的学术风格标签，如 `(a)`, `(b)`, `(c)`。
- **延迟绘制**: 为了确保标签位置在最终布局中是准确的，其实际绘制操作被延迟到调用 `.save()` 时执行。
- **核心参数**:
  - `tags`: `List` (可选), 要标记的子图 `tag` 列表。若为 `None`，则自动标记所有已绘图的子图。
  - `label_style`: `str`, `'alpha'` (默认), `'numeric'`, `'roman'`。
  - `case`: `str`, `'lower'` (默认) 或 `'upper'`。
  - `template`: `str`, 格式化模板，如 `'({label})'` (默认)。
  - `position`: `Tuple[float, float]`, 标签相对于子图左上角的位置 (在 `ax.transAxes` 坐标系中)。默认为 `(-0.01, 1.01)`。
- **示例**: `plotter.add_subplot_labels(label_style='roman', case='upper')`

### `add_grouped_labels`
- **用途**: 为逻辑上分组的多个子图添加一个共享的、统一的标签。
- **核心参数**:
  - `groups`: `Dict[str, List[str]]`, 字典的键是标签文本，值是属于该组的子图 `tag` 列表。
  - `position`: `str`, 标签相对于组合边界框的位置，如 `'top_left'` (默认)。
  - `padding`: `float`, 标签与边界框的间距。
- **示例**: `plotter.add_grouped_labels(groups={'Fig. 1': ['ax00', 'ax01']})`

---

## 标题与轴标签

- `set_title(label, tag?, **kwargs)`: 设置子图标题。
- `set_xlabel(label, tag?, **kwargs)`: 设置X轴标签。
- `set_ylabel(label, tag?, **kwargs)`: 设置Y轴标签。
- `set_zlabel(label, tag?, **kwargs)`: 设置3D子图的Z轴标签。
- `set_suptitle(title, **kwargs)`: 设置整个画布的**主标题**。

---

## 范围、刻度与视角

- `set_xlim(*args, tag?, **kwargs)`: 设置X轴范围。
- `set_ylim(*args, tag?, **kwargs)`: 设置Y轴范围。
- `tick_params(axis='both', tag?, **kwargs)`: 设置刻度线和刻度标签的样式，如旋转角度 `labelrotation=45`。
- `view_init(elev?, azim?, tag?)`: 设置3D子图的观察角度（仰角和方位角）。

---

## 图例

### `set_legend`
- **用途**: 为指定子图添加图例。**自动处理双Y轴**，合并主轴和孪生轴的图例项。
- **示例**: `plotter.set_legend(tag='my_plot', loc='best', frameon=False)`

### `add_global_legend`
- **用途**: 在画布的统一位置为多个子图创建一个全局图例。
- **核心参数**:
  - `tags`: `List` (可选), 指定从哪些子图收集图例项。若为 `None`，则从所有子图收集。
  - `remove_sub_legends`: `bool` (默认 `True`), 是否移除原始子图的图例。
- **示例**: `plotter.add_global_legend(loc='upper right')`

---

## 画布级标注 (Figure-Level)

这些方法在整个画布的坐标系（0,0为左下角，1,1为右上角）中进行操作。

- `fig_add_text(x, y, text, **kwargs)`: 在画布任意位置添加文本。
- `fig_add_line(x_coords, y_coords, **kwargs)`: 在画布上绘制一条线。
- `fig_add_box(tags, padding?, **kwargs)`: 围绕一个或多个子图的组合边界绘制一个矩形框。
- `fig_add_boundary_box(padding?, **kwargs)`: 围绕**所有**子图的总体边界绘制一个矩形框（延迟绘制）。
- `fig_add_label(tags, text, position?, padding?, **kwargs)`: 在一组子图的组合边界框外侧添加标签（延迟绘制）。

---

## 孪生轴 (Twin-Axis)

### `add_twinx` / `add_polar_twin`
- **用途**: 创建一个共享X轴但拥有独立Y轴的“双Y轴”图，或为极坐标创建孪生轴。
- **行为**: 调用后，Plotter会进入“孪生轴模式”，后续的绘图和修饰命令将作用于新创建的孪生轴。**颜色循环会自动偏移**，确保与主轴的颜色不同。
- **示例**:
```python
plotter.add_line(..., tag='A', label='Temp')  # 主轴
plotter.add_twinx(tag='A')                    # 创建孪生轴
plotter.add_bar(..., label='Rainfall')        # 在孪生轴上绘图
```

### `target_primary` / `target_twin`
- **用途**: 在主轴和孪生轴上下文之间切换。
- **`target_primary(tag?)`**: 将后续操作的目标切换回主轴。
- **`target_twin(tag?)`**: 将后续操作的目标切换到孪生轴。
- **示例**:
```python
plotter.add_twinx(tag='A')
plotter.add_bar(...) # 作用于孪生轴
plotter.target_primary(tag='A')
plotter.add_hline(...) # 作用于主轴
```

---

## 子图内元素

- `add_hline(y, ...)` / `add_vline(x, ...)`: 添加水平/垂直参考线。
- `add_text(x, y, text, ...)`: 在子图的数据坐标系上添加文本。
- `add_patch(patch_object, ...)`: 添加任意 Matplotlib `Patch` 对象（如 `Rectangle`, `Circle`）。
- `add_highlight_box(x_range, y_range, ...)`: 根据数据坐标高亮一个矩形区域。

---

## 嵌入与缩放

### `add_inset_image`
- **用途**: 在子图内部的指定位置嵌入一张图片。
- **核心参数**: `image_path`, `rect` (`[x, y, width, height]`)。

### `add_zoom_inset`
- **用途**: 创建一个放大主图特定区域的嵌入式子图。
- **核心参数**:
  - `rect`: `[x, y, width, height]`, 内嵌图相对于父轴的位置和大小。
  - `x_range`: `(xmin, xmax)`, 要放大的X轴数据范围。
  - `y_range`: (可选) 要放大的Y轴数据范围。若为 `None`，则根据 `x_range` 内的数据自动计算。
  - `draw_source_box`: `bool` (可选), 是否在源图上绘制高亮框。

### `add_zoom_connectors`
- **用途**: 为 `add_zoom_inset` 创建的缩放图手动添加连接线。
- **核心参数**: `connections` (`List[Tuple[int, int]]`), 定义源区域角点到内嵌图角点的连接。角点编码: 1-右上, 2-左上, 3-左下, 4-右下。
- **示例**: `plotter.add_zoom_connectors([(2, 1), (3, 4)])`

---

## 特征标记

- `add_peak_highlights(peaks_x, x_col, y_col, ...)`: 在曲线上高亮并标注特征峰，使用 `adjustText` 避免标签重叠。
- `add_event_markers(event_dates, labels?, ...)`: 在时间序列图上标记垂直事件线和标签。

---

## 收尾与保存

### `cleanup`
- **用途**: 自动共享坐标轴并对齐标签，使图表更整洁。
- **核心参数**:
  - `share_y_on_rows`: `List[int]`, 指定哪些行共享Y轴。
  - `share_x_on_cols`: `List[int]`, 指定哪些列共享X轴。
  - `auto_share`: `bool` 或 `str` (`'x'`, `'y'`), 自动共享所有行/列的轴。
  - `align_labels`: `bool` (默认 `True`), 对齐整个图表的X和Y轴标签。

### `cleanup_heatmaps`
- **用途**: 为指定的一组热图创建共享的、统一范围的颜色条。
- **核心参数**: `tags` (`List[str]`), 包含热图 `tag` 的列表。

### `save`
- **用途**: 将当前图形保存到文件。在保存前，会执行所有延迟绘制的操作。
- **核心参数**: `filename`, `dpi` (默认 `300`), `bbox_inches` (默认 `'tight'`)。
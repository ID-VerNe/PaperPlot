---
id: mixins-modifiers
title: ModifiersMixin API
sidebar_label: 修饰与轴管理
---

## 概述

`ModifiersMixin` 包含了大量用于修饰、装饰和最终确定图表的方法。这些方法分为几类：子图和画布层面的标注、坐标轴管理、图例控制、孪生轴、嵌入内容以及收尾工具。

---

## 布局控制

### `set_padding`
- **签名**: `set_padding(left?, bottom?, right?, top?)`
- **用途**: 手动设置图形的边距（padding）。调用此方法会自动禁用 `constrained_layout` 或 `tight_layout`，以确保手动设置生效。
- **核心参数**:
  - `left`: `float` (可选), 左边距 (0-1)。
  - `bottom`: `float` (可选), 下边距 (0-1)。
  - `right`: `float` (可选), 右边距 (0-1)。
  - `top`: `float` (可选), 上边距 (0-1)。
- **示例**: `plotter.set_padding(left=0.1, bottom=0.1, right=0.9, top=0.9)`

### `set_spacing`
- **签名**: `set_spacing(wspace?, hspace?)`
- **用途**: 手动设置子图之间的间距。调用此方法会自动禁用 `constrained_layout` 或 `tight_layout`，以确保手动设置生效。
- **核心参数**:
  - `wspace`: `float` (可选), 子图之间的水平间距（以子图宽度的分数表示）。
  - `hspace`: `float` (可选), 子图之间的垂直间距（以子图高度的分数表示）。
- **示例**: `plotter.set_spacing(wspace=0.3, hspace=0.3)`

---

## 子图标签与分组

### `add_subplot_labels`
- **签名**: `add_subplot_labels(tags?, label_style?, case?, template?, position?, start_at?, **text_kwargs)`
- **用途**: 为子图添加自动编号的学术风格标签，如 `(a)`, `(b)`, `(c)`。此方法会自动检测要标记的子图，并根据指定的样式生成标签。
- **注意**: 实际的绘制操作将延迟到调用 `.save()` 方法时执行，以确保在最终布局上计算标签位置的准确性。
- **核心参数**:
  - `tags`: `List[Union[str, int]]` (可选), 要添加标签的子图 `tag` 列表。如果为 `None`，则会自动检测已绘图的子图并为其添加标签。默认为 `None`。
  - `label_style`: `str` (可选), 标签的编号样式。可选值为 `'alpha'`, `'numeric'`, `'roman'`。默认为 `'alpha'`。
  - `case`: `str` (可选), 标签的大小写 (`'lower'` 或 `'upper'`)。对 `'numeric'` 样式无效。默认为 `'lower'`。
  - `template`: `str` (可选), 格式化标签的模板字符串。默认为 `'({label})'`。
  - `position`: `Tuple[float, float]` (可选), 标签相对于每个子图左上角的位置，坐标系为 `ax.transAxes`。默认为 `(-0.01, 1.01)`。
  - `start_at`: `int` (可选), 标签编号的起始数字（0-indexed）。例如，`start_at=0` 对应 'a', 1, 'I'。默认为 `0`。
  - `**text_kwargs`: 其他传递给 `fig.text` 的关键字参数，用于定制文本样式，如 `fontsize`, `weight`, `color`。
- **示例**: `plotter.add_subplot_labels(label_style='roman', case='upper', fontsize=14, weight='bold')`

### `add_grouped_labels`
- **签名**: `add_grouped_labels(groups, position?, padding?, **text_kwargs)`
- **用途**: 为逻辑上分组的多个子图添加一个共享的、统一的标签。此方法计算多个子图的组合边界框，并将标签放置在该边界框的指定相对位置。
- **注意**: 实际的绘制操作将延迟到调用 `.save()` 方法时执行。
- **核心参数**:
  - `groups`: `Dict[str, List[Union[str, int]]]`, 一个字典，其中键是标签文本（例如 `'(a)'`），值是属于该组的子图 `tag` 列表（例如 `['ax00', 'ax01']`）。
  - `position`: `str` (可选), 标签相对于组合边界框的相对位置。默认为 `'top_left'`。
  - `padding`: `float` (可选), 标签与组合边界框之间的间距。默认为 `0.01`。
  - `**text_kwargs`: 其他传递给底层 `fig.text` 的关键字参数，用于定制文本样式，如 `fontsize`, `weight`, `color`。
- **示例**: `plotter.add_grouped_labels(groups={'Figure 1': ['A', 'B']}, position='top_center')`

---

## 标题与轴标签

### `set_title`
- **签名**: `set_title(label, tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图设置标题。
- **核心参数**:
  - `label`: `str`, 标题文本。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.set_title` 的其他参数。
- **示例**: `plotter.set_title('My Plot Title', tag='A', fontsize=16)`

### `set_xlabel`
- **签名**: `set_xlabel(label, tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图设置X轴标签。
- **核心参数**:
  - `label`: `str`, X轴标签文本。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.set_xlabel` 的其他参数。
- **示例**: `plotter.set_xlabel('Time (s)')`

### `set_ylabel`
- **签名**: `set_ylabel(label, tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图设置Y轴标签。
- **核心参数**:
  - `label`: `str`, Y轴标签文本。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.set_ylabel` 的其他参数。
- **示例**: `plotter.set_ylabel('Value')`

### `set_zlabel`
- **签名**: `set_zlabel(label, tag?, **kwargs)`
- **用途**: 为指定或当前活动的3D子图设置Z轴标签。
- **核心参数**:
  - `label`: `str`, Z轴标签文本。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.set_zlabel` 的其他参数。
- **示例**: `plotter.set_zlabel('Depth (m)')`

### `set_suptitle`
- **签名**: `set_suptitle(title, **kwargs)`
- **用途**: 为整个画布（Figure）设置一个主标题。
- **核心参数**:
  - `title`: `str`, 主标题文本。
  - `**kwargs`: 传递给 `fig.suptitle` 的其他参数。
- **示例**: `plotter.set_suptitle('Overall Experiment Results', fontsize=20)`

---

## 范围、刻度与视角

### `set_xlim`
- **签名**: `set_xlim(*args, tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图设置X轴的显示范围。
- **核心参数**:
  - `*args`: 同 `ax.set_xlim` 的位置参数 (例如 `(min, max)`)。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.set_xlim` 的其他参数 (例如 `xmin=0, xmax=1`)。
- **示例**: `plotter.set_xlim(0, 100)`

### `set_ylim`
- **签名**: `set_ylim(*args, tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图设置Y轴的显示范围。
- **核心参数**:
  - `*args`: 同 `ax.set_ylim` 的位置参数 (例如 `(min, max)`)。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.set_ylim` 的其他参数 (例如 `ymin=0, ymax=1`)。
- **示例**: `plotter.set_ylim(ymin=0)`

### `tick_params`
- **签名**: `tick_params(axis='both', tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图的刻度线、刻度标签和网格线设置参数。
- **核心参数**:
  - `axis`: `str` (可选), 要操作的轴 ('x', 'y', 'both')。默认为 `'both'`。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.tick_params` 的其他参数。
- **示例**: `plotter.tick_params(axis='x', labelrotation=45, labelsize=10)`

### `view_init`
- **签名**: `view_init(elev?, azim?, tag?)`
- **用途**: 设置3D子图的观察角度。
- **核心参数**:
  - `elev`: `float` (可选), 仰角（绕x轴旋转）。
  - `azim`: `float` (可选), 方位角（绕z轴旋转）。
- **示例**: `plotter.view_init(elev=30, azim=45)`

---

## 图例

### `set_legend`
- **签名**: `set_legend(tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图添加图例。此方法能够自动处理双Y轴（twinx）图，合并主轴和孪生轴的图例项。
- **核心参数**:
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.legend` 的其他参数。
- **示例**: `plotter.set_legend(tag='my_plot', loc='best', frameon=False)`

### `add_global_legend`
- **签名**: `add_global_legend(tags?, remove_sub_legends?, **kwargs)`
- **用途**: 在画布的统一位置为多个子图创建一个全局图例。
- **核心参数**:
  - `tags`: `List[str]` (可选), 指定从哪些子图收集图例项。若为 `None`，则从所有子图收集。
  - `remove_sub_legends`: `bool` (可选), 是否移除原始子图的图例。默认为 `True`。
  - `**kwargs`: 传递给 `fig.legend` 的其他参数。
- **示例**: `plotter.add_global_legend(loc='upper right')`

---

## 画布级标注 (Figure-Level)

这些方法在整个画布的坐标系（(0,0)为左下角，(1,1)为右上角）中进行操作。

### `fig_add_text`
- **签名**: `fig_add_text(x, y, text, **kwargs)`
- **用途**: 在整个画布（Figure）的指定位置添加文本。
- **核心参数**:
  - `x`: `float`, 文本的X坐标，范围从0到1。
  - `y`: `float`, 文本的Y坐标，范围从0到1。
  - `text`: `str`, 要添加的文本内容。
  - `**kwargs`: 其他传递给 `matplotlib.figure.Figure.text` 的关键字参数。
- **示例**: `plotter.fig_add_text(0.5, 0.95, 'Figure-level Text', ha='center')`

### `fig_add_line`
- **签名**: `fig_add_line(x_coords, y_coords, **kwargs)`
- **用途**: 在整个画布（Figure）上绘制一条线，连接指定的坐标点。
- **核心参数**:
  - `x_coords`: `List[float]`, 线的X坐标列表，范围从0到1。
  - `y_coords`: `List[float]`, 线的Y坐标列表，范围从0到1。
  - `**kwargs`: 其他传递给 `matplotlib.lines.Line2D` 的关键字参数。
- **示例**: `plotter.fig_add_line([0.1, 0.9], [0.5, 0.5], color='black', linestyle='--')`

### `fig_add_box`
- **签名**: `fig_add_box(tags, padding?, **kwargs)`
- **用途**: 围绕一个或多个子图的组合边界绘制一个矩形框。
- **注意**: 实际的绘制操作将延迟到调用 `.save()` 方法时执行。
- **核心参数**:
  - `tags`: `List[Union[str, int]]`, 要包含在框内的子图 `tag` 列表。
  - `padding`: `float` (可选), 框与子图边界之间的间距。默认为 `0.01`。
  - `**kwargs`: 其他传递给 `matplotlib.patches.Rectangle` 的关键字参数。
- **示例**: `plotter.fig_add_box(tags=['A', 'B'], edgecolor='red', linestyle='--')`

### `fig_add_boundary_box`
- **签名**: `fig_add_boundary_box(padding?, **kwargs)`
- **用途**: 围绕**所有**子图的总体边界绘制一个矩形框。
- **注意**: 实际的绘制操作将延迟到调用 `.save()` 方法时执行。
- **核心参数**:
  - `padding`: `float` (可选), 框与子图边界之间的间距。默认为 `0.01`。
  - `**kwargs`: 其他传递给 `matplotlib.patches.Rectangle` 的关键字参数。
- **示例**: `plotter.fig_add_boundary_box(padding=0.03, edgecolor='blue')`

### `fig_add_label`
- **签名**: `fig_add_label(tags, text, position?, padding?, **kwargs)`
- **用途**: 在一组子图的组合边界框外侧添加标签。
- **注意**: 实际的绘制操作将延迟到调用 `.save()` 方法时执行。
- **核心参数**:
  - `tags`: `List[Union[str, int]]`, 要包含在标签组内的子图 `tag` 列表。
  - `text`: `str`, 要添加的标签文本。
  - `position`: `str` (可选), 标签相对于组合边界框的相对位置。默认为 `'top_center'`。
  - `padding`: `float` (可选), 标签与组合边界框之间的间距。默认为 `0.01`。
  - `**kwargs`: 其他传递给底层 `fig.text` 的关键字参数。
- **示例**: `plotter.fig_add_label(tags=['A', 'B'], text='Group 1', position='left_center')`

---

## 孪生轴 (Twin-Axis)

### `add_twinx`
- **签名**: `add_twinx(tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图创建一个共享X轴但拥有独立Y轴的“双Y轴”图。调用此方法后，Plotter会进入“孪生轴模式”，后续的绘图操作（如 `add_line`, `add_bar` 等）将作用于新创建的孪生轴。颜色循环会自动偏移以确保颜色不同。
- **核心参数**:
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.twinx` 的其他参数。
- **示例**:
  ```python
  plotter.add_line(..., tag='A', label='Temp')  # 主轴
  plotter.add_twinx(tag='A')                    # 创建孪生轴
  plotter.add_bar(..., label='Rainfall')        # 在孪生轴上绘图
  ```

### `add_polar_twin`
- **签名**: `add_polar_twin(tag?, **kwargs)`
- **用途**: 为指定或当前活动的子图创建一个共享角度轴但拥有独立径向轴的“双极坐标轴”图。调用此方法后，Plotter会进入“孪生轴模式”，后续的绘图操作将作用于新创建的孪生轴。颜色循环会自动偏移以确保颜色不同。
- **核心参数**:
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 传递给 `ax.twinx` 的其他参数。
- **示例**:
  ```python
  plotter.add_polar_line(..., tag='B', label='Magnitude') # 主轴
  plotter.add_polar_twin(tag='B')                         # 创建孪生极坐标轴
  plotter.add_polar_scatter(..., label='Phase')           # 在孪生极坐标轴上绘图
  ```

### `target_primary`
- **签名**: `target_primary(tag?)`
- **用途**: 将当前绘图目标切换回指定子图的主轴。
- **核心参数**:
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
- **示例**:
  ```python
  plotter.add_twinx(tag='A').add_bar(...) # 作用于孪生轴
  plotter.target_primary(tag='A').add_hline(...) # 切换回主轴
  ```

### `target_twin`
- **签名**: `target_twin(tag?)`
- **用途**: 将当前绘图目标切换到指定子图的孪生轴。如果该子图没有孪生轴，则会创建一个。
- **核心参数**:
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
- **示例**:
  ```python
  plotter.target_primary(tag='A').add_line(...) # 作用于主轴
  plotter.target_twin(tag='A').add_bar(...)     # 切换到孪生轴
  ```


---

## 子图内元素

这些方法在子图的数据坐标系中添加各种元素。

### `add_hline`
- **签名**: `add_hline(y, tag?, **kwargs)`
- **用途**: 在指定或当前活动的子图上添加一条水平参考线。
- **核心参数**:
  - `y`: `float`, 水平线在Y轴上的位置。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `ax.axhline` 的关键字参数。
- **示例**: `plotter.add_hline(0, color='red', linestyle='--')`

### `add_vline`
- **签名**: `add_vline(x, tag?, **kwargs)`
- **用途**: 在指定或当前活动的子图上添加一条垂直参考线。
- **核心参数**:
  - `x`: `float`, 垂直线在X轴上的位置。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `ax.axvline` 的关键字参数。
- **示例**: `plotter.add_vline(50, color='green')`


### `add_text`
- **签名**: `add_text(x, y, text, tag?, **kwargs)`
- **用途**: 在指定或当前活动的子图的数据坐标系上添加文本。
- **核心参数**:
  - `x`: `float`, 文本的X数据坐标。
  - `y`: `float`, 文本的Y数据坐标。
  - `text`: `str`, 要添加的文本内容。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `ax.text` 的关键字参数。
- **示例**: `plotter.add_text(10, 20, 'Important Point')`

### `add_patch`
- **签名**: `add_patch(patch_object, tag?)`
- **用途**: 在指定或当前活动的子图上添加任意 Matplotlib `Patch` 对象（如 `Rectangle`, `Circle`）。
- **核心参数**:
  - `patch_object`: `matplotlib.patches.Patch`, 要添加的 Matplotlib `Patch` 对象。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
- **示例**: `plotter.add_patch(plt.Circle((0.5, 0.5), 0.1, color='blue'))`

### `add_highlight_box`
- **签名**: `add_highlight_box(x_range, y_range, tag?, **kwargs)`
- **用途**: 在指定或当前活动的子图上，根据数据坐标高亮一个矩形区域。
- **核心参数**:
  - `x_range`: `Tuple[float, float]`, 要高亮的X轴数据范围 `(xmin, xmax)`。
  - `y_range`: `Tuple[float, float]`, 要高亮的Y轴数据范围 `(ymin, ymax)`。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `ax.axvspan` 或 `ax.axhspan` 的关键字参数。
- **示例**: `plotter.add_highlight_box(x_range=(2, 5), y_range=(10, 20), facecolor='yellow', alpha=0.3)`

---

## 嵌入与缩放

### `add_inset_image`
- **签名**: `add_inset_image(image_path, rect, host_tag?, **kwargs)`
- **用途**: 在指定或当前活动的子图内部的指定位置嵌入一张图片。
- **核心参数**:
  - `image_path`: `str`, 要嵌入的图片文件路径。
  - `rect`: `List[float]`, 定义嵌入位置和大小的列表 `[x, y, width, height]`，坐标相对于宿主子图的 `Axes` 坐标系。
  - `host_tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `matplotlib.axes.Axes.imshow` 的关键字参数。
- **示例**: `plotter.add_inset_image('logo.png', rect=[0.6, 0.6, 0.3, 0.3])`

### `add_zoom_inset`
- **签名**: `add_zoom_inset(rect, x_range, y_range?, source_tag?, draw_source_box?, **kwargs)`
- **用途**: 创建一个放大主图特定区域的嵌入式子图。
- **核心参数**:
  - `rect`: `List[float]`, 内嵌图相对于父轴的位置和大小 `[x, y, width, height]`，坐标系为 `figure.bbox`。
  - `x_range`: `Tuple[float, float]`, 要放大的X轴数据范围 `(xmin, xmax)`。
  - `y_range`: `Optional[Tuple[float, float]]` (可选), 要放大的Y轴数据范围。若为 `None`，则自动计算。
  - `source_tag`: `Optional[Union[str, int]]` (可选), 原始子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `draw_source_box`: `bool` (可选), 是否在原始子图上绘制一个框来指示放大区域。默认为 `True`。
  - `**kwargs`: 其他传递给 `mpl_toolkits.axes_grid1.inset_locator.inset_axes` 的关键字参数。
- **示例**: `plotter.add_zoom_inset(rect=[0.5, 0.5, 0.4, 0.4], x_range=(2, 3))`

### `add_zoom_connectors`
- **签名**: `add_zoom_connectors(connections, source_tag?, **kwargs)`
- **用途**: 为 `add_zoom_inset` 创建的缩放图手动添加连接线。
- **核心参数**:
  - `connections`: `List[Tuple[int, int]]`, 连接定义列表，如 `[(2, 1), (3, 4)]`。角点编码: 1-右上, 2-左上, 3-左下, 4-右下。
  - `source_tag`: `Optional[Union[str, int]]` (可选), 原始子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `matplotlib.patches.ConnectionPatch` 的关键字参数。
- **示例**: `plotter.add_zoom_connectors([(2, 1), (3, 4)], color='gray', linestyle='--')`

---

## 特征标记

### `add_peak_highlights`
- **签名**: `add_peak_highlights(peaks_x, x_col, y_col, label_peaks?, tag?, **kwargs)`
- **用途**: 在指定或当前活动的子图上，高亮并标注特征峰，使用 `adjustText` 避免标签重叠。
- **核心参数**:
  - `peaks_x`: `List[float]`, 特征峰的X轴位置列表。
  - `x_col`: `str`, X轴数据在缓存DataFrame中的列名。
  - `y_col`: `str`, Y轴数据在缓存DataFrame中的列名。
  - `label_peaks`: `bool` (可选), 是否为峰值添加文本标签。默认为 `True`。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `ax.plot` (用于标记峰值) 和 `ax.text` (用于标签) 的关键字参数。
- **示例**: `plotter.add_peak_highlights(peaks_x=[1600, 2200], x_col='wavenumber', y_col='intensity')`

### `add_event_markers`
- **签名**: `add_event_markers(event_dates, labels?, tag?, **kwargs)`
- **用途**: 在指定或当前活动的子图上，标记垂直事件线和标签。
- **核心参数**:
  - `event_dates`: `List[Union[float, datetime]]`, 事件的X轴位置列表。可以是数值或 `datetime` 对象。
  - `labels`: `Optional[List[str]]` (可选), 与每个事件对应的标签列表。如果为 `None`，则不显示标签。
  - `tag`: `Optional[Union[str, int]]` (可选), 目标子图的 `tag`。如果为 `None`，则使用最后一次绘图的子图。
  - `**kwargs`: 其他传递给 `ax.axvline` (用于事件线) 和 `ax.text` (用于标签) 的关键字参数。
- **示例**: `plotter.add_event_markers(event_dates=['2023-01-01'], labels=['Failure'])`

---

## 收尾与保存

### `cleanup`
- **签名**: `cleanup(share_y_on_rows?, share_x_on_cols?, align_labels?, auto_share?)`
- **用途**: 自动共享坐标轴并对齐标签，移除多余刻度，使图表更整洁。
- **核心参数**:
  - `share_y_on_rows`: `Optional[List[int]]` (可选), 指定哪些行共享Y轴。例如 `[0, 1]` 表示第0行和第1行共享Y轴。
  - `share_x_on_cols`: `Optional[List[int]]` (可选), 指定哪些列共享X轴。例如 `[0, 1]` 表示第0列和第1列共享X轴。
  - `align_labels`: `bool` (可选), 是否对齐所有子图的X和Y轴标签。默认为 `True`。
  - `auto_share`: `Union[bool, str]` (可选), 自动共享所有行/列的轴。
    - `True`: 自动共享所有行和列的X和Y轴。
    - `'x'`: 自动共享所有列的X轴。
    - `'y'`: 自动共享所有行的Y轴。
    - `False`: 不自动共享。
    默认为 `False`。
- **示例**: `plotter.cleanup(auto_share=True)`

### `cleanup_heatmaps`
- **签名**: `cleanup_heatmaps(tags)`
- **用途**: 为指定的一组热图创建共享的、统一范围的颜色条。
- **核心参数**:
  - `tags`: `List[Union[str, int]]`, 包含热图 `tag` 的列表。
- **示例**: `plotter.cleanup_heatmaps(tags=['heatmap1', 'heatmap2'])`

### `save`
- **签名**: `save(filename, **kwargs)`
- **用途**: 将当前图形保存到文件。在保存前，会执行所有延迟绘制的操作。
- **核心参数**:
  - `filename`: `str`, 输出文件的路径和名称。
  - `**kwargs`: 传递给 `matplotlib.figure.Figure.savefig` 的其他参数，如 `dpi`, `bbox_inches`, `transparent`。
- **示例**: `plotter.save('my_figure.png', dpi=300)`
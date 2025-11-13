---
id: mixins-modifiers
title: ModifiersMixin API
sidebar_label: 修饰与轴管理
---

概述
- 子图和画布层面的修饰方法：标题、轴标签、刻度、图例、孪生轴、文本/线/框、嵌入图片、缩放 inset、峰值与事件标记、收尾与保存。

子图标题与轴标签
- `set_title(label, tag?, **kwargs)` 设置子图标题
  - 示例：`plotter.set_title('Accuracy', tag='A')`
- `set_xlabel(label, tag?, **kwargs)` 设置 X 轴标签
  - 示例：`plotter.set_xlabel('Time (s)', tag='A')`
- `set_ylabel(label, tag?, **kwargs)` 设置 Y 轴标签
  - 示例：`plotter.set_ylabel('Value', tag='A')`
- `set_zlabel(label, tag?, **kwargs)` 设置 Z 轴标签（3D）
  - 示例：`plotter.set_zlabel('Z', tag='A')`
- `tick_params(axis='both', tag?, **kwargs)` 设置刻度样式
  - 示例：`plotter.tick_params(axis='x', tag='A', labelrotation=45)`

范围与视角
- `set_xlim(*args, tag?, **kwargs)` / `set_ylim(*args, tag?, **kwargs)` 设置轴范围
  - 示例：`plotter.set_xlim(0, 10).set_ylim(-1, 1)`
- `view_init(elev?, azim?, tag?)` 设置 3D 视角
  - 示例：`plotter.view_init(elev=30, azim=45, tag='A')`

图例
- `set_legend(tag?, **kwargs)` 子图图例（合并主/孪生轴）
  - 示例：`plotter.set_legend('A', loc='best')`
- `add_global_legend(tags?, remove_sub_legends=True, **kwargs)` 在画布统一位置创建全局图例
  - 示例：`plotter.add_global_legend(tags=['A','B'])`

画布级元素
- `set_suptitle(title, **kwargs)` 设置全局标题
  - 示例：`plotter.set_suptitle('Experiment Results')`
- `fig_add_text(x, y, text, **kwargs)` 在画布坐标系添加文字
  - 示例：`plotter.fig_add_text(0.02, 0.98, 'Draft', fontsize=10)`
- `fig_add_line(x_coords, y_coords, **kwargs)` 在画布坐标系添加线
  - 示例：`plotter.fig_add_line([0.1,0.9],[0.1,0.1], color='black')`
- `fig_add_box(tags, padding=0.01, **kwargs)` 围出一组子图的组合边框
  - 示例：`plotter.fig_add_box(tags=['A','B'], padding=0.02)`
- `fig_add_boundary_box(padding=0.02, **kwargs)` 画布边界框
  - 示例：`plotter.fig_add_boundary_box(padding=0.02)`
- `fig_add_label(tags, text, position='top_left', padding=0.01, **kwargs)` 画布级区域标签
  - 示例：`plotter.fig_add_label(tags=['A','B'], text='Group 1', position='top_left')`

孪生轴与上下文
- `add_twinx(tag?, **kwargs)` 创建右 Y 孪生轴
  - 示例：
  ```python
  plotter.add_line(data=df, x='t', y='y', tag='A', label='Line')
  plotter.add_twinx('A').target_twin('A').add_bar(data=df2, x='t', y='b', label='Bar')
  plotter.target_primary('A').set_legend('A')
  ```
- `add_polar_twin(tag?, frameon=False)` 为极坐标创建孪生轴
  - 示例：见 `mixins-generic.md / add_polar_bar` 的孪生轴示例
- `target_primary(tag?)` 切回主轴上下文
- `target_twin(tag?)` 切至孪生轴上下文

子图元素
- `add_hline(y, tag?, **kwargs)` 水平线
  - 示例：`plotter.add_hline(0.0, color='gray', linestyle='--')`
- `add_vline(x, tag?, **kwargs)` 垂直线
  - 示例：`plotter.add_vline(1.25, color='red')`
- `add_text(x, y, text, tag?, **kwargs)` 在子图坐标系添加文字
  - 示例：`plotter.add_text(0.5, 0.5, 'Center', fontsize=10)`
- `add_patch(patch_object, tag?)` 添加任意 Matplotlib Patch
  - 示例：
  ```python
  from matplotlib.patches import Rectangle
  plotter.add_patch(Rectangle((0.2,0.2), 0.4, 0.3, fill=False))
  ```
- `add_highlight_box(x_range, y_range, tag?, **kwargs)` 区域高亮
  - 示例：`plotter.add_highlight_box((1,3),(2,5), alpha=0.2, color='yellow')`

嵌入与缩放
- `add_inset_image(image_path, rect, host_tag?, **kwargs)` 子图中嵌入图片
  - 示例：`plotter.add_inset_image('logo.png', rect=[0.7,0.7,0.2,0.2])`
- `add_zoom_inset(rect, zoom_level=2, ...)` 缩放 inset（支持同步框选主轴区域）
  - 示例：`plotter.add_zoom_inset(rect=[0.6,0.6,0.35,0.35], zoom_level=2)`

特征标记
- `add_peak_highlights(peaks_x, x_col, y_col, ...)` 标记峰值位置
  - 示例：`plotter.add_peak_highlights(peaks_x=[1.1, 2.3], x_col='x', y_col='y')`
- `add_event_markers(event_dates, labels?, ...)` 时间事件标记（竖线+文本）
  - 示例：`plotter.add_event_markers(event_dates=[0.5,1.2], labels=['Trip','Reclose'])`

收尾与保存
- `cleanup(share_y_on_rows?, share_x_on_cols?, align_labels=True, auto_share=False)` 自动共享坐标、对齐标签
  - 示例：`plotter.cleanup(align_labels=True, auto_share=True)`
- `cleanup_heatmaps(tags)` 为多张热图统一颜色范围并创建共享色条
  - 示例：`plotter.cleanup_heatmaps(tags=['H1','H2','H3'])`
- `save(filename, **kwargs)` 保存图片（执行延迟绘制队列，默认 `dpi=300`, `bbox_inches='tight'`）
  - 示例：`plotter.save('out.png', dpi=300)`

示例（孪生轴组合）
```
plotter.add_line(data=df, x='t', y='y', tag='A', label='L')
plotter.add_twinx('A').target_twin('A').add_bar(data=df2, x='t', y='b', label='B')
plotter.target_primary('A').set_legend('A')
```

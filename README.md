<p align="center">
  <img src="logo.svg" alt="PaperPlot Logo">
</p>


[![PyPI version](https://badge.fury.io/py/paperplotter.svg)](https://badge.fury.io/py/paperplotter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一个为科研论文设计的声明式 Matplotlib 封装库，让复杂图表的创建变得简单直观。**

`PaperPlot` 的诞生是为了解决在准备学术论文时，使用 Matplotlib 创建高质量、布局复杂的图表所面临的繁琐问题。它通过引入声明式的链式 API 和基于标签（tag）的对象管理，让你能够用更少的代码，更清晰的逻辑，构建从简单网格到复杂组合的各类图表。

## 核心理念与特性

*   **🎨 声明式链式调用**: 像写句子一样构建你的图表，例如 `plotter.add_line(...).set_title(...).set_xlabel(...)`。绘图后，后续修饰器会自动作用于最后一个活动的子图，无需重复指定目标。
*   **🏷️ 基于标签的控制**: 给每个子图一个独一无二的 `tag`，之后就可以随时通过 `tag` 对其进行任何修改，告别混乱的 `axes[i][j]` 索引。
*   **🧩 强大的布局系统**: 无论是简单的 `(行, 列)` 网格，还是使用 `mosaic` 实现的跨行跨列复杂布局，都能轻松定义。
*   **🧱 声明式嵌套布局**: 通过一个字典即可一次性定义包含子网格的复杂层级布局，并使用 `'容器.子图'` 这样的直观路径进行引用，完美实现“图中图”。
*   **📐 数据驱动的尺寸控制**: 除了传统的 `figsize`，还可以通过 `subplot_aspect` 指定子图单元格的宽高比，让 `PaperPlot` 自动计算最合适的画布尺寸，确保图表比例的专业性。
*   **🖼️ 灵活的图像集成**: 使用 `add_figure()` 方法，可以轻松地将外部图像文件作为子图内容，并提供了 `fit`, `cover`, `stretch` 等多种填充模式，以及对齐、内边距和缩放控制。
*   **✨ 内置科研主题与调色板**: 提供多种专业美观的内置样式（如 `publication`）和丰富的动漫游戏主题调色板，一键切换图表风格和颜色方案，保证全局一致性。
*   **🌐 全局图层级标注**: 提供了在整个画布（Figure）上添加文本、线条、方框和标签的 API，非常适合添加全局注释或高亮一组图表。
*   **🔢 子图自动编号与分组**: 通过 `add_subplot_labels()` 和 `add_grouped_labels()` 方法，可以一键为子图添加 `(a)`, `(b)`... 等学术编号，或为逻辑分组添加共享标签，并支持高度定制化。
*   **🔗 优雅的双Y轴（Twin-Axis）**: 彻底解决了 Matplotlib 双Y轴操作繁琐的问题。通过 `add_twinx()` 进入孪生轴上下文，然后可以继续使用链式调用进行绘图和修饰，最后通过 `target_primary()` 切回主轴。
*   **🔬 丰富的领域专用图表**: 内置了科研中常用的图表类型，如光谱图、混淆矩阵、ROC 曲线、学习曲线、分岔图、相量图等。
*   **🔧 智能美化工具**: `cleanup()` 方法可以智能地共享坐标轴、对齐标签；`cleanup_heatmaps()` 可以为多个热图创建共享的颜色条。

## 安装

```bash
pip install paperplotter
```

## 快速开始

只需几行代码，就可以创建一个包含两个子图的 1x2 网格图。

```python
import paperplot as pp
import pandas as pd
import numpy as np

# 1. 准备数据
df_line = pd.DataFrame({
    'time': np.linspace(0, 10, 50),
    'signal': np.cos(np.linspace(0, 10, 50))
})
df_scatter = pd.DataFrame({
    'x': np.random.rand(50) * 10,
    'y': np.random.rand(50) * 10
})

# 2. 初始化 Plotter 并通过链式调用绘图和修饰
(
    pp.Plotter(layout=(1, 2), figsize=(10, 4))
    
    # --- 绘制并修饰左图 ---
    # add_line 将 'time_series' 设为活动tag
    .add_line(data=df_line, x='time', y='signal', tag='time_series')
    # 后续的修饰器会自动应用到 'time_series' 上
    .set_title('Time Series Data')
    .set_xlabel('Time (s)')
    .set_ylabel('Signal')
    
    # --- 绘制并修饰右图 ---
    # add_scatter 将 'scatter_plot' 设为新的活动tag
    .add_scatter(data=df_scatter, x='x', y='y', tag='scatter_plot')
    # 后续的修饰器会自动应用到 'scatter_plot' 上
    .set_title('Scatter Plot')
    .set_xlabel('X Value')
    .set_ylabel('Y Value')
    
    # --- 保存图像 ---
    .save("quick_start_figure.png")
)
```

## 通过示例学习 (Learn from Examples)

掌握 `PaperPlot` 最好的方法就是探索我们提供的丰富示例。每个示例都专注于一个核心功能，并附有详细的代码和注释。

### 布局 (Layout)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **声明式嵌套布局**<br/> `Layout/declarative_nested_layout_example.py` | 使用字典来声明式地定义一个包含子网格的复杂、多层级布局，实现“图中图”的效果。 | `layout={...}`<br/> `tag='容器.子图'` |
| **高级布局 (跨列)**<br/> `Layout/advanced_layout_example.py` | 展示如何使用列表定义一个跨列的复杂布局。 | `layout=[['A', 'B', 'B'], ...]`<br/>`get_ax_by_name()` |
| **高级布局 (跨行)**<br/> `Layout/row_span_example.py` | 创建一个图表，其中某个子图跨越多行。 | `layout=[['A', 'B'], ['A', 'C']]` |
| **高级布局 (块跨越)**<br/> `Layout/block_span_example.py` | 创建一个图表，其中某个子图同时跨越多行和多列。 | `layout=[['A', 'A', 'B'], ['A', 'A', 'C']]` |
| **固定子图宽高比**<br/> `Layout/aspect_ratio_example.py` | 通过 `subplot_aspect` 保证每个子图单元格的宽高比，Plotter 会自动计算画布大小，无需指定 `figsize`。 | `subplot_aspect=(16, 9)` |
| **组合图与图像集成**<br/> `Features_Customization/add_figure_alignment_example.py` | 在一个复杂的马赛克布局中集成外部图像，并演示 `fit`, `cover`, `stretch` 等多种对齐和填充模式。 | `add_figure()`<br/>`fit_mode`, `align`, `padding`, `zoom` |
| **双Y轴 (Twin-Axis)**<br/> `Layout/twinx_chaining_example.py` | 演示如何通过上下文切换，流畅地在主轴和孪生轴上进行绘图和修饰。 | `add_twinx()`, `target_primary()`, `target_twin()` |

### 功能与定制化 (Features & Customization)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **多图网格**<br/> `Features_Customization/multi_plot_grid.py` | 在一个网格中通过链式调用混合绘制不同类型的图表。 | `plotter.add_...().add_...()` |
| **缩放嵌入图 (Zoom Inset)**<br/> `Features_Customization/zoom_inset_example.py` | 在主图上创建一个放大特定区域的嵌入式子图，并自动添加连接线。 | `add_zoom_inset()` |
| **共享颜色条**<br/> `Features_Customization/heatmap_colorbar_example.py` | 为多个热图创建一个共享的、能反映全局数据范围的颜色条。 | `add_heatmap(cbar=False)`, `cleanup_heatmaps()` |
| **高级定制**<br/> `Features_Customization/advanced_customization.py` | 演示如何使用 `get_ax()` "逃生舱口" 来获取原生的 Matplotlib `Axes` 对象，并添加任意 `Patch`（如椭圆）。 | `get_ax()`, `add_patch()` |
| **全局控制**<br/> `Features_Customization/global_controls_example.py` | 展示如何设置全局标题 (`suptitle`) 和创建全局图例。 | `set_suptitle()`, `add_global_legend()` |
| **智能清理**<br/> `Features_Customization/cleanup_demonstration.py` | 演示 `cleanup()` 函数如何动态地为指定行/列的子图共享 X/Y 轴，并自动隐藏多余的刻度标签。 | `cleanup(auto_share=True)` |
| **错误处理**<br/> `Features_Customization/error_handling_test.py` | 展示 `PaperPlot` 的自定义异常，如 `DuplicateTagError`, `TagNotFoundError`, `PlottingSpaceError`。 | `try...except pp.PaperPlotError` |

### 标注、高亮与标签 (Annotation, Highlighting & Labeling)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **自动子图标签 (马赛克)**<br/>`Labeling/example_1_auto_mosaic.py` | 自动为马赛克布局中所有已绘制的子图添加 `(a)`, `(b)` 等顺序标签。 | `add_subplot_labels()` |
| **分组标签**<br/>`Labeling/example_2_grouped.py` | 为一组逻辑子图添加一个共享标签，并将其放置在组合边界框的外部。 | `add_grouped_labels()` |
| **嵌套布局标签**<br/>`Labeling/example_3_nested.py` | 演示如何在复杂的嵌套布局中，为顶层和子网格内部添加不同层级的标签。 | `add_grouped_labels()`, `add_subplot_labels(tags=...)` |
| **高度自定义标签**<br/>`Labeling/example_4_custom.py` | 展示子图标签的丰富定制选项，包括样式、模板、颜色、字体和位置。 | `add_subplot_labels(...)` |
| **画布级标注**<br/>`Features_Customization/fig_annotation_example.py`| 演示添加跨越多个子图的画布级注解，如方框、标签和线条。| `fig_add_box()`, `fig_add_label()`, `fig_add_line()`, `fig_add_text()`|
| **区域高亮**<br/>`Features_Customization/highlighting_example.py` | 展示如何在子图内部高亮特定的数据区域，并为整个图表添加边框。| `add_highlight_box()`, `fig_add_boundary_box()` |
| **通用工具函数**<br/> `Data_Analysis_Utils/utility_functions_example.py` | 展示更多通用的修饰函数，如在高光谱上高亮特征峰和在时间序列上标记事件。 | `add_peak_highlights()`, `add_event_markers()` |

### 风格与美化 (Styles & Aesthetics)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **风格画廊**<br/> `Styles_Aesthetics/style_gallery_example.py` | 循环遍历所有内置的绘图风格，并为每种风格生成一个示例图。 | `Plotter(style='...')` |
| **统计标注**<br/> `Styles_Aesthetics/statistical_annotation_example.py` | 在箱线图上自动进行多组成对统计检验（如 t-test），并智能堆叠显著性标记。 | `add_box()`, `add_pairwise_tests()` |
| **美学与处理**<br/> `Styles_Aesthetics/aesthetic_and_processing_example.py` | 对数据进行平滑处理或根据条件高亮特定数据点。 | `utils.moving_average()`, `add_conditional_scatter()` |
| **统计图组合**<br/> `Features_Customization/statistical_plots_example.py` | 演示如何组合小提琴图和蜂群图，以及在箱线图上添加统计检验。 | `add_violin()`, `add_swarm()`, `add_box()`, `add_stat_test()` |

### 领域专用图 (Domain-Specific Plots)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **领域专用图合集**<br/> `Domain_Specific_Plots/domain_specific_plots_example.py` | 一站式展示多种领域专用图，包括 SERS 光谱图、混淆矩阵、ROC 曲线和 PCA 散点图。 | `add_spectra()`, `add_confusion_matrix()`, `add_roc_curve()`, `add_pca_scatter()` |
| **3D 绘图**<br/> `Domain_Specific_Plots/3d_plots_example.py` | 展示如何创建 3D 线图和表面图。 | `ax_configs={'...': {'projection': '3d'}}`, `add_line3d()`, `add_surface()` |
| **学习曲线**<br/> `Domain_Specific_Plots/learning_curve_example.py` | 绘制机器学习模型的学习曲线，帮助诊断过拟合或欠拟合问题。 | `add_learning_curve()` |
| **SERS 浓度图**<br/> `Domain_Specific_Plots/concentration_map_example.py` | 绘制 SERS Mapping 浓度图，本质上是带有专业美化的热图。 | `add_concentration_map()` |
| **电力系统时间序列**<br/> `Domain_Specific_Plots/power_timeseries_example.py` | 绘制电力系统动态仿真结果，并自动标记故障、切除等事件。 | `add_power_timeseries()` |
| **相量图**<br/> `Domain_Specific_Plots/phasor_diagram_example.py` | 在极坐标上绘制电气工程中的相量图。 | `add_phasor_diagram()` |
| **分岔图**<br/> `Domain_Specific_Plots/bifurcation_diagram_example.py` | 绘制常用于非线性系统和稳定性分析的分岔图。 | `add_bifurcation_diagram()` |

### 数据分析工具 (Data Analysis Utils)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **数据分析工具集**<br/> `Data_Analysis_Utils/data_analysis_utils_example.py` | 演示如何对数据进行分布拟合和数据分箱绘图。 | `add_distribution_fit()`, `add_binned_plot()` |

---

## 贡献

欢迎任何形式的贡献！如果你有好的想法、发现了 bug，或者想要添加新的功能，请随时提交 Pull Request 或创建 Issue。

## 许可证

本项目采用 [MIT License](LICENSE)授权。

# PaperPlot

[![PyPI version](https://badge.fury.io/py/paperplotter.svg)](https://badge.fury.io/py/paperplotter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一个为科研论文设计的声明式 Matplotlib 封装库，让复杂图表的创建变得简单直观。**

`PaperPlot` 的诞生是为了解决在准备学术论文时，使用 Matplotlib 创建高质量、布局复杂的图表所面临的繁琐问题。它通过引入声明式的链式 API 和基于标签（tag）的对象管理，让你能够用更少的代码，更清晰的逻辑，构建从简单网格到复杂组合的各类图表。

## 核心理念与特性

*   **🎨 声明式链式调用**: 像写句子一样构建你的图表，例如 `plotter.add_line(...).set_title(...).set_xlabel(...)`。
*   **🏷️ 基于标签的控制**: 给每个子图一个独一无二的 `tag`，之后就可以随时通过 `tag` 对其进行任何修改，告别混乱的 `axes[i][j]` 索引。
*   **🧩 强大的布局系统**: 无论是简单的 `(行, 列)` 网格，还是使用 `mosaic` 实现的跨行跨列复杂布局，都能轻松定义。
*   **📐 灵活的尺寸控制**: 除了传统的 `figsize`，还可以通过 `subplot_aspect` 指定子图单元格的宽高比，让 `PaperPlot` 自动计算最合适的画布尺寸。
*   **✨ 内置科研主题**: 提供多种专业美观的内置样式，如 `publication`, `presentation` 等，一键切换图表风格。
*   **🌐 全局图层级标注**: 提供了在整个画布（Figure）上添加文本、线条、方框和标签的 API，非常适合添加全局注释或高亮一组图表。
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

# 2. 初始化 Plotter 并绘图
plotter = pp.Plotter(layout=(1, 2), figsize=(10, 4))

# 3. 添加图表并使用 tag 标记
plotter.add_line(data=df_line, x='time', y='signal', tag='time_series')
plotter.add_scatter(data=df_scatter, x='x', y='y', tag='scatter_plot')

# 4. 通过 tag 设置标题和标签
plotter.set_title('time_series', 'Time Series Data')
plotter.set_xlabel('time_series', 'Time (s)')
plotter.set_ylabel('time_series', 'Signal')

plotter.set_title('scatter_plot', 'Scatter Plot')
plotter.set_xlabel('scatter_plot', 'X Value')
plotter.set_ylabel('scatter_plot', 'Y Value')

# 5. 保存图像
plotter.save("quick_start_figure.png")
```


## 通过示例学习 (Learn from Examples)

掌握 `PaperPlot` 最好的方法就是探索我们提供的丰富示例。每个示例都专注于一个核心功能，并附有详细的代码和注释。

### 布局 (Layout)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **高级布局**<br/> `Layout/advanced_layout_example.py` | 展示如何使用列表定义一个跨列的复杂布局。 | `layout=[['A', 'B', 'B'], ...]`<br/>`get_ax_by_name()` |
| **行跨越**<br/> `Layout/row_span_example.py` | 创建一个图表，其中某个子图跨越多行。 | `layout=[['A', 'B'], ['A', 'C']]` |
| **块跨越**<br/> `Layout/block_span_example.py` | 创建一个图表，其中某个子图同时跨越多行和多列。 | `layout=[['A', 'A', 'B'], ['A', 'A', 'C']]` |
| **固定子图宽高比**<br/> `Layout/aspect_ratio_example.py` | 在不指定 `figsize` 的情况下，通过 `subplot_aspect` 保证每个子图单元格的宽高比，Plotter 会自动计算画布大小。 | `subplot_aspect=(16, 9)` |

### 功能与定制化 (Features & Customization)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **多图网格**<br/> `Features_Customization/multi_plot_grid.py` | 在一个网格中混合绘制不同类型的图表（线图、柱状图、散点图、热图）。 | `add_line()`, `add_bar()`, `add_scatter()`, `add_heatmap()` |
| **高级定制**<br/> `Features_Customization/advanced_customization.py` | 演示如何使用 `get_ax()` "逃生舱口" 来获取原生的 Matplotlib `Axes` 对象，并添加任意 `Patch`（如椭圆）。 | `get_ax()`, `ax.add_patch()` |
| **全局控制**<br/> `Features_Customization/global_controls_example.py` | 展示如何设置全局标题 (`suptitle`) 和创建全局图例。 | `set_suptitle()`, `add_global_legend()` |
| **共享颜色条**<br/> `Features_Customization/heatmap_colorbar_example.py` | 为多个热图创建一个共享的、能反映全局数据范围的颜色条。 | `add_heatmap(cbar=False)`, `cleanup_heatmaps()` |
| **智能清理**<br/> `Features_Customization/cleanup_demonstration.py` | 演示 `cleanup()` 函数如何动态地为指定行/列的子图共享 X/Y 轴，并自动隐藏多余的刻度标签。 | `cleanup(auto_share=True)` |
| **组合图与内嵌图**<br/> `Features_Customization/composite_figure_example.py` | 创建一个 L 型的复杂图表，并在其中一个子图内部嵌入一张图片。 | `layout=[['A', 'A'], ['B', '.']]`, `add_inset_image()` |
| **功能扩展**<br/> `Features_Customization/feature_expansion_example.py` | 演示双Y轴 (`add_twinx`)、回归图 (`add_regplot`)、参考线 (`add_hline`) 和文本标注 (`add_text`) 等高级功能。 | `add_twinx()`, `add_regplot()`, `add_hline()`, `add_text()` |
| **错误处理**<br/> `Features_Customization/error_handling_test.py` | 展示 `PaperPlot` 的自定义异常，如 `DuplicateTagError`, `TagNotFoundError`, `PlottingSpaceError`。 | `try...except pp.PaperPlotError` |

### 标注与高亮 (Annotation & Highlighting)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **图层级标注**<br/>`Features_Customization/fig_annotation_example.py`| 演示添加跨越多个子图的画布级注解，如方框、标签和线条。| `fig_add_box()`, `fig_add_label()`, `fig_add_line()`, `fig_add_text()`|
| **区域高亮**<br/>`Features_Customization/highlighting_example.py` | 展示如何在子图内部高亮特定的数据区域，并为整个图表添加边框。| `add_highlight_box()`, `fig_add_boundary_box()` |

### 风格与美化 (Styles & Aesthetics)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **风格画廊**<br/> `Styles_Aesthetics/style_gallery_example.py` | 循环遍历所有内置的绘图风格，并为每种风格生成一个示例图。 | `Plotter(style='...')` |
| **统计标注**<br/> `Styles_Aesthetics/statistical_annotation_example.py` | 在箱线图上自动进行多组成对统计检验（如 t-test），并智能堆叠显著性标记。 | `add_box()`, `utils.add_pairwise_tests()` |
| **美学与处理**<br/> `Styles_Aesthetics/aesthetic_and_processing_example.py` | 使用 `utils` 模块中的函数对数据进行平滑处理或根据条件高亮特定数据点。 | `utils.moving_average()`, `utils.highlight_points()` |

### 领域专用图 (Domain-Specific Plots)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **领域专用图合集**<br/> `Domain_Specific_Plots/domain_specific_plots_example.py` | 一站式展示多种领域专用图，包括 SERS 光谱图、混淆矩阵、ROC 曲线和 PCA 散点图。 | `add_spectra()`, `add_confusion_matrix()`, `add_roc_curve()`, `add_pca_scatter()` |
| **学习曲线**<br/> `Domain_Specific_Plots/learning_curve_example.py` | 绘制机器学习模型的学习曲线，帮助诊断过拟合或欠拟合问题。 | `utils.plot_learning_curve()` |
| **SERS 浓度图**<br/> `Domain_Specific_Plots/concentration_map_example.py` | 绘制 SERS Mapping 浓度图，本质上是带有专业美化的热图。 | `add_concentration_map()` |
| **电力系统时间序列**<br/> `Domain_Specific_Plots/power_timeseries_example.py` | 绘制电力系统动态仿真结果，并自动标记故障、切除等事件。 | `add_power_timeseries()` |
| **相量图**<br/> `Domain_Specific_Plots/phasor_diagram_example.py` | 在极坐标上绘制电气工程中的相量图。 | `add_phasor_diagram()` |
| **分岔图**<br/> `Domain_Specific_Plots/bifurcation_diagram_example.py` | 绘制常用于非线性系统和稳定性分析的分岔图。 | `add_scatter(rasterized=True)` |

### 数据分析工具 (Data Analysis Utils)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **数据分析工具集**<br/> `Data_Analysis_Utils/data_analysis_utils_example.py` | 演示如何对数据进行分布拟合 (`fit_and_plot_distribution`) 和数据分箱 (`bin_data`)。 | `utils.fit_and_plot_distribution()`, `utils.bin_data()` |
| **通用工具函数**<br/> `Data_Analysis_Utils/utility_functions_example.py` | 展示更多通用的 `utils` 函数，如在高光谱上高亮特征峰 (`highlight_peaks`) 和在时间序列上标记事件 (`add_event_markers`)。 | `utils.highlight_peaks()`, `utils.add_event_markers()` |

---

## 贡献

欢迎任何形式的贡献！如果你有好的想法、发现了 bug，或者想要添加新的功能，请随时提交 Pull Request 或创建 Issue。

## 许可证

本项目采用 [MIT License](LICENSE)授权。
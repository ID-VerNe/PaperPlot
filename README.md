<p align="center">
  <img src="logo.svg" alt="PaperPlot Logo">
</p>


[![PyPI version](https://badge.fury.io/py/paperplotter.svg)](https://badge.fury.io/py/paperplotter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一个为科研论文设计的声明式 Matplotlib 封装库，让复杂图表的创建变得简单直观。**

`PaperPlot` 的诞生是为了解决在准备学术论文时，使用 Matplotlib 创建高质量、布局复杂的图表所面临的繁琐问题。它通过引入声明式的链式 API 和基于标签（tag）的对象管理，让你能够用更少的代码，更清晰的逻辑，构建从简单网格到复杂组合的各类图表。

## 核心理念与特性

*   **🚀 v0.1.11 新特性**:
    *   **分类变量防御**: `add_bar` 自动处理数值型 X 轴，确保柱状图等宽等距。
    *   **智能配色引擎**: 颜色耗尽时自动通过 HLS 变换扩展调色板，保证系列颜色唯一。
    *   **统一间距控制**: `set_padding` 集成 `wspace`/`hspace`，实现一键式布局微调。
    *   **双 Y 轴便捷 API**: 新增 `add_twinx_line`，一步完成双轴图表绘制。
    *   **高层统计工具**: `add_errorbar_from_raw` 直接从重复实验原始数据生成均值与误差棒。
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
*   **📏 精确的手动布局控制**: 当自动布局无法满足需求时，提供了 `set_padding()` 和 `set_spacing()` 方法，让你能够精确控制图表的边距和子图间距，实现像素级的布局微调。
*   **🔌 元数据导出**: 通过 `get_layout_metadata()` 导出图表的完整布局信息（像素位置、数据范围），为 GUI 工具开发和交互式可视化提供基础支持。

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

掌握 `PaperPlot` 最好的方法就是探索我们提供的丰富示例。所有示例已按功能分类组织在 `examples/` 目录下。

> 💡 **提示**：建议从 `01_Basic_Usage` 开始，然后根据需求探索其他类别。每个目录都有详细的 README 文档。

### 📁 示例目录结构
```
examples/
├── README.md                    # 📖 示例总览和学习路径
├── 01_Basic_Usage/              # 🎯 基础用法：快速入门
├── 02_Chart_Types/              # 📊 图表类型：各种图表演示
│   └── README.md                # 图表类型选择指南
├── 03_Layout_Management/        # 🧩 布局管理：复杂子图布局
├── 04_Twin_Axes/                # 🔗 孪生轴：双Y轴图表
│   └── README.md                # 孪生轴使用指南
├── 05_Styling_and_Themes/       # 🎨 样式主题：定制图表外观
├── 06_Annotations/              # 📍 注释标注：添加说明元素
│   ├── README.md                # 注释功能总览
│   ├── text_and_labels/         # 文本和子图标签
│   ├── shapes_and_regions/      # 形状和高亮区域
│   └── statistical/             # 统计检验标注
├── 07_Images_and_Composition/   # 🖼️ 图像组合：图像集成
├── 08_Domain_Specific/          # 🔬 领域特定：专用图表类型
├── 09_Data_Utils/               # 🛠️ 数据工具：辅助功能
├── 10_Metadata_Export/          # 🔌 元数据导出：GUI 开发基础
└── assets/                      # 📦 示例资源文件
```

### 🚀 快速开始示例

```bash
# 克隆或下载项目后，进入 examples 目录
cd examples

# 查看完整的示例索引和学习路径
cat README.md

# 运行基础示例
python 01_Basic_Usage/error_handling.py
python 02_Chart_Types/bar_charts.py

# 探索更多功能
python 06_Annotations/text_and_labels/subplot_labels_auto.py
```

### 01. 基础用法 (Basic Usage)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **多图网格**<br/> `multi_plot_grid.py` | 在一个网格中通过链式调用混合绘制不同类型的图表。 | `plotter.add_...().add_...()` |
| **错误处理**<br/> `error_handling.py` | 展示 `PaperPlot` 的自定义异常处理。 | `try...except pp.PaperPlotError` |

> 💡 更多图表类型示例请参见 [`02_Chart_Types/`](examples/02_Chart_Types/)

### 02. 图表类型 (Chart Types)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **柱状图**<br/> `bar_charts.py` | 分组柱状图和堆叠柱状图。 | `add_grouped_bar()`, `add_stacked_bar()` |
| **折线图**<br/> `line_charts.py` | 多线图演示。 | `add_multi_line()` |
| **饼图与环形图**<br/> `pie_and_donut.py` | 饼图、环形图、嵌套环形图。 | `add_pie()`, `add_donut()`, `add_nested_donut()` |
| **热图与颜色条**<br/> `heatmaps.py` | 为多个热图创建共享的颜色条。 | `add_heatmap()`, `cleanup_heatmaps()` |
| **统计图组合**<br/> `statistical_plots.py` | 组合小提琴图、蜂群图和箱线图。 | `add_violin()`, `add_swarm()`, `add_box()` |
| **瀑布图**<br/> `waterfall.py` | 阶梯瀑布图。 | `add_waterfall()` |
| **K线图**<br/> `candlestick.py` | 金融K线图（蜡烛图）。 | `add_candlestick()` |
| **极坐标图**<br/> `polar_plots.py` | 极坐标柱状图。 | `add_polar_bar()` |
| **回归图**<br/> `regression_plots.py` | 回归分析图。 | `add_regplot()` |

> 📖 详细图表类型选择指南请查看 [`examples/02_Chart_Types/README.md`](examples/02_Chart_Types/README.md)

### 02. 布局管理 (Layout Management)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **布局展示**<br/> `layout_showcase.py` | 全面展示各种布局能力。 | 多种 `layout` 配置 |
| **声明式嵌套布局**<br/> `nested_layout.py` | 使用字典声明式定义包含子网格的复杂多层级布局。 | `layout={...}`, `tag='容器.子图'` |
| **高级布局**<br/> `advanced_layout.py` | 展示跨列的复杂布局。 | `layout=[['A', 'B', 'B'], ...]` |
| **块跨越**<br/> `block_span.py` | 子图同时跨越多行和多列。 | `layout=[['A', 'A', 'B'], ['A', 'A', 'C']]` |
| **行跨越**<br/> `row_span.py` | 子图跨越多行。 | `layout=[['A', 'B'], ['A', 'C']]` |
| **固定宽高比**<br/> `aspect_ratio.py` | 通过 `subplot_aspect` 保证子图单元格宽高比。 | `subplot_aspect=(16, 9)` |
| **手动布局控制**<br/> `manual_layout_demo.py` | 手动设置图表边距和子图间距，覆盖自动布局。 | `set_padding()`, `set_spacing()` |

### 03. 孪生轴 (Twin Axes)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **双Y轴基础**<br/> `basic_twin_axes.py` | 演示如何流畅地在主轴和孪生轴上绘图。 | `add_twinx()`, `target_primary()`, `target_twin()` |
| **颜色循环同步**<br/> `twin_axes_color_cycle.py` | 确保双轴的颜色循环同步。 | 颜色循环管理 |
| **极坐标双轴** <br/> `polar_twin_axes.py` | 在极坐标系统中使用双轴。 | `add_polar_twin()` |

> 📖 完整的孪生轴使用指南请查看 [`examples/04_Twin_Axes/README.md`](examples/04_Twin_Axes/README.md)

### 04. 样式与主题 (Styling and Themes)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **风格画廊**<br/> `theme_gallery.py` | 循环遍历所有内置绘图风格。 | `Plotter(style='...')` |
| **自定义主题**<br/> `custom_theme.py` | 演示如何使用 `get_ax()` 获取原生 Matplotlib Axes 并自定义。 | `get_ax()`, `add_patch()` |
| **全局样式控制**<br/> `global_styling.py` | 设置全局标题和创建全局图例。 | `set_suptitle()`, `add_global_legend()` |
| **智能清理**<br/> `cleanup_functions.py` | 演示 `cleanup()` 动态共享坐标轴和隐藏多余标签。 | `cleanup(auto_share=True)` |
| **数据处理**<br/> `data_processing.py` | 数据平滑处理和条件高亮。 | `utils.moving_average()`, `add_conditional_scatter()` |

### 05. 标注与标签 (Annotations)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **📝 文本和标签** (`text_and_labels/`) |
| **自动子图标签**<br/> `subplot_labels_auto.py` | 自动为子图添加 `(a)`, `(b)` 等顺序标签。 | `add_subplot_labels()` |
| **分组标签**<br/> `subplot_labels_grouped.py` | 为一组子图添加共享标签。 | `add_grouped_labels()` |
| **嵌套布局标签**<br/> `subplot_labels_nested.py` | 在复杂嵌套布局中添加多层级标签。 | `add_grouped_labels()`, `add_subplot_labels(tags=...)` |
| **自定义标签**<br/> `subplot_labels_custom.py` | 展示标签的丰富定制选项。 | `add_subplot_labels(...)` |
| **图形文本**<br/> `figure_text.py` | 在画布上添加文本注释。 | `fig_add_text()` |
| **🎨 形状和区域** (`shapes_and_regions/`) |
| **画布级标注**<br/> `shapes_and_boxes.py` | 添加跨越多个子图的方框、标签和线条。 | `fig_add_box()`, `fig_add_label()`, `fig_add_line()` |
| **缩放嵌入图**<br/> `zoom_insets.py` | 创建放大特定区域的嵌入式子图。 | `add_zoom_inset()` |
| **区域高亮**<br/> `highlighting.py` | 高亮特定数据区域并添加边框。 | `add_highlight_box()`, `fig_add_boundary_box()` |
| **📊 统计注释** (`statistical/`) |
| **统计标注**<br/> `statistical_annotation.py` | 在箱线图上自动添加统计检验标记。 | `add_box()`, `add_pairwise_tests()` |

> 📖 完整的注释功能指南请查看 [`examples/06_Annotations/README.md`](examples/06_Annotations/README.md)

### 06. 图像集成与组合 (Images and Composition)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **嵌入图像**<br/> `embedding_images.py` | 将外部图像文件作为子图内容。 | `add_figure()` |
| **图像对齐**<br/> `image_alignment.py` | 演示 `fit`, `cover`, `stretch` 等对齐模式。 | `add_figure(fit_mode=..., align=...)` |
| **组合图形**<br/> `composite_figures.py` | 创建包含图像和图表的复杂组合图形。 | `add_figure()`, `add_zoom_inset()` |

### 07. 领域专用图表 (Domain-Specific Plots)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **领域专用图合集**<br/> `domain_specific_plots_example.py` | 展示多种领域专用图（光谱图、混淆矩阵、ROC曲线、PCA散点图）。 | `add_spectra()`, `add_confusion_matrix()`, `add_roc_curve()` |
| **3D 绘图**<br/> `3d_plots_example.py` | 创建 3D 线图和表面图。 | `ax_configs={'projection': '3d'}`, `add_line3d()`, `add_surface()` |
| **学习曲线**<br/> `learning_curve_example.py` | 绘制机器学习模型学习曲线。 | `add_learning_curve()` |
| **浓度图**<br/> `concentration_map_example.py` | 绘制 SERS Mapping 浓度图。 | `add_concentration_map()` |
| **电力时间序列**<br/> `power_timeseries_example.py` | 绘制电力系统动态仿真结果。 | `add_power_timeseries()` |
| **相量图**<br/> `phasor_diagram_example.py` | 在极坐标上绘制相量图。 | `add_phasor_diagram()` |
| **分岔图**<br/> `bifurcation_diagram_example.py` | 绘制非线性系统分岔图。 | `add_bifurcation_diagram()` |

### 08. 数据分析工具 (Data Analysis Utils)

| 示例 | 描述 | 关键功能 |
| :--- | :--- | :--- |
| **数据分析工具集**<br/> `data_analysis_utils_example.py` | 分布拟合和数据分箱绘图。 | `add_distribution_fit()`, `add_binned_plot()` |
| **通用工具函数**<br/> `utility_functions_example.py` | 高亮特征峰和标记事件。 | `add_peak_highlights()`, `add_event_markers()` |

---

## 贡献

欢迎任何形式的贡献！如果你有好的想法、发现了 bug，或者想要添加新的功能，请随时提交 Pull Request 或创建 Issue。

## 许可证

本项目采用 [MIT License](LICENSE)授权。

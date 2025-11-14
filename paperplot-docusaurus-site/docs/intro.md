# PaperPlotter 技术文档

## 1. 项目概述

### 项目名称与版本
- 名称：PaperPlotter
- 版本：0.1.10 (内部开发版)

### 项目简介
PaperPlotter 是一个面向科研论文图表制作的声明式绘图库，对 Matplotlib 进行结构化封装，提供统一的布局管理、数据准备、样式控制与后处理能力。通过可读性极高的链式 API，用户可以快速搭建复杂的网格/马赛克/嵌套布局，在同一画布上组合多种图表类型，并使用统一的颜色与图例管理、共享坐标轴、自动标注与收尾工具，将分散的绘图细节收敛到简洁一致的工作流中。PaperPlotter 强调工程化的可维护性，让通用绘图逻辑复用到不同图表类型上，使图的复现、审稿修改与团队协作更加顺畅。

### 主要功能特性
- **统一绘图工作流**: 所有绘图 API 通过 `_execute_plot` 统一处理布局、数据准备、默认样式、缓存与状态。
- **灵活布局**: 支持简单网格 `(R, C)`、马赛克 `List[List[str]]` 和声明式嵌套 `Dict` 布局。
- **数据驱动尺寸**: 支持通过 `subplot_aspect` 指定子图宽高比，自动计算 `figsize`。
- **图像集成**: `add_figure` 支持将外部图片作为子图内容，并提供多种填充和对齐模式。
- **颜色一致性**: `ColorManager` 基于系列 `label` 在多子图间保持颜色稳定。
- **优雅双轴**: `add_twinx` 与 `add_polar_twin` 支持在主轴和孪生轴上链式绘图，并自动合并图例。
- **丰富的图表类型**: 内置折线、散点、柱状、热图、统计图，以及领域专用图表。
- **智能收尾工具**: `cleanup` 自动共享坐标轴、`cleanup_heatmaps` 创建共享颜色条、`add_subplot_labels` 和 `add_grouped_labels` 实现学术风格的自动编号。

### 技术栈说明
- Python 3.8+
- Matplotlib, NumPy, Pandas, Seaborn, SciPy, adjustText

---

## 2. 安装指南

### 系统要求
- Python：3.8 及以上
- 操作系统：Windows、Linux、macOS

### 依赖安装步骤
```bash
pip install paperplotter
```

---

## 3. 使用说明

### 核心功能操作流程
1. 创建 `Plotter`，指定布局（网格/马赛克/嵌套）、样式和尺寸 (`figsize` 或 `subplot_aspect`)。
2. 通过 `add_*` 系列方法绘图，使用 `tag` 参数定位子图。
3. 使用修饰器方法（如 `set_title`, `set_xlabel`）对最后活动的子图进行修饰。
4. 使用 `cleanup` 或 `fig_add_*` 等方法进行全局美化。
5. 调用 `save` 输出图片。

```python
from paperplot import Plotter
import pandas as pd

# 示例：创建一个复杂的嵌套布局
layout = {
    'main': [['A', 'B'], ['C', 'C']],
    'subgrids': {
        'B': {'layout': [['B1'], ['B2']]}
    }
}
df = pd.DataFrame({'x':[1,2,3], 'y':[2,3,4]})

(
  Plotter(layout=layout, subplot_aspect=(16, 9))
  .add_line(data=df, x='x', y='y', tag='A', label='series-1')
  .set_title('Plot A')
  .add_bar(data=df, x='x', y='y', tag='C')
  .set_title('Plot C')
  .add_scatter(data=df, x='x', y='y', tag='B.B1') # 使用层级tag
  .set_title('Subplot B1')
  .cleanup(auto_share=True)
  .save('demo.png')
)
```

### 核心配置参数
- `Plotter(layout, style, figsize, subplot_aspect, ax_configs, layout_engine)`
  - `layout`: `(rows, cols)`、马赛克 `List[List[str]]` 或嵌套 `dict`。
  - `style`: 样式名，对应 `paperplot/styles`。
  - `subplot_aspect`: 子图单元格宽高比，如 `(16, 9)`，与 `figsize` 互斥。
  - `ax_configs`: 按 tag 指定 `projection='polar'` 或 `projection='3d'` 等。
- 通用绘图方法遵循：`add_xxx(data=df, ..., tag='TAG')` 并通过 `_execute_plot` 实现统一流程。

---

## 4. 开发指南

### 项目目录结构
```
paperplot/
├── core.py             # Plotter 核心类
├── exceptions.py       # 自定义异常
├── utils.py            # 实用工具和 ColorManager
├── mixins/             # 按功能划分的绘图和修饰方法
│   ├── generic.py
│   ├── domain.py
│   └── ...
└── styles/             # Matplotlib 样式文件 (*.mplstyle)
```

### 代码规范
- 新增绘图 API 必须通过 `_execute_plot` 封装，以复用核心逻辑。
- 优先使用 `data=df` + 列名字符串作为输入，以利用缓存和后续修饰器。
- 为每个公共方法编写完整的中文 docstring，包含参数、返回值和示例。
- 使用 `label` 触发 `ColorManager` 实现颜色一致性。

### 构建和测试
- 运行所有测试: `pytest`
- 运行所有示例: `python run_all_examples.py`

---

## 5. API 参考（按 Mixin 分组）

### Core Plotter (`core.py`)
- `Plotter(layout, style, figsize, subplot_aspect, ax_configs, ...)`: 构造函数。
- `get_ax(tag)`: 按标签获取子图轴对象。
- `get_ax_by_name(name)`: 在马赛克/嵌套布局中按名称获取轴。

### GenericPlotsMixin (`mixins/generic.py`)
- `add_line(data?, x, y, ...)`: 折线图。
- `add_bar(data?, x, y, y_err?, ...)`: 柱状图（支持误差条）。
- `add_grouped_bar(data, x, ys, ...)`: 分组柱状图。
- `add_multi_line(data, x, ys, ...)`: 多线图。
- `add_stacked_bar(data, x, ys, ...)`: 堆叠柱状图。
- `add_polar_bar(data, theta, r, ...)`: 极坐标柱状图。
- `add_pie(data, sizes, ...)`: 饼图。
- `add_donut(data, sizes, ...)`: 环形图。
- `add_nested_donut(outer, inner, ...)`: 嵌套环形图。
- `add_waterfall(data, x, deltas, ...)`: 瀑布图。
- `add_candlestick(data, time, open, high, low, close, ...)`: K线图。
- `add_scatter(data?, x, y, s?, c?, ...)`: 散点图（`s`/`c`支持列名）。
- `add_hist(data?, x, ...)`: 直方图。
- `add_box(data?, x, y, hue?, ...)`: 箱线图 (Seaborn)。
- `add_heatmap(data, ...)`: 热图，智能匹配 `cmap`。
- `add_seaborn(plot_func, ...)`: 通用 Seaborn 绘制入口。
- `add_blank(tag?)`: 空白占位（关闭坐标轴）。
- `add_regplot(data?, x, y, ...)`: 回归拟合+散点。
- `add_conditional_scatter(data?, x, y, condition, ...)`: 条件高亮散点。
- `add_figure(image_path, fit_mode, align, padding, zoom, ...)`: 将图像文件作为子图内容。

### DomainSpecificPlotsMixin (`mixins/domain.py`)
- `add_spectra(data?, x, y_cols, offset?, ...)`: 多光谱垂直偏移对比。
- `add_concentration_map(data, ...)`: 浓度/SERS Mapping 热图。
- `add_confusion_matrix(matrix, class_names, ...)`: 混淆矩阵。
- `add_roc_curve(fpr, tpr, roc_auc, ...)`: ROC 曲线。
- `add_pca_scatter(data?, x_pc, y_pc, hue?, ...)`: PCA 散点图。
- `add_power_timeseries(data, x, y_cols, events?, ...)`: 电力仿真时序+事件标记。
- `add_phasor_diagram(magnitudes, angles, ...)`: 相量图（极坐标）。
- `add_bifurcation_diagram(data?, x, y, ...)`: 分岔图。

### DataAnalysisPlotsMixin (`mixins/analysis_plots.py`)
- `add_binned_plot(data, x, y, bins?, ...)`: 分箱聚合误差条图。
- `add_distribution_fit(data?, x, dist_name?, ...)`: 在直方图上拟合分布PDF。

### MachineLearningPlotsMixin (`mixins/ml_plots.py`)
- `add_learning_curve(train_sizes, train_scores, test_scores, ...)`: 学习曲线。

### StatsPlotsMixin (`mixins/stats_plots.py`)
- `add_violin(data?, x, y, hue?, ...)`: 小提琴图。
- `add_swarm(data?, x, y, hue?, ...)`: 蜂群图。
- `add_joint(data, x, y, ...)`: 联合分布图（替换整张图）。
- `add_pair(data, ...)`: 成对关系网格（替换整张图）。

### StatsModifiersMixin (`mixins/stats_modifiers.py`)
- `add_stat_test(x, y, group1, group2, ...)`: 两组比较并标注显著性。
- `add_pairwise_tests(x, y, comparisons, ...)`: 多组成对比较并堆叠标注。

### ThreeDPlotsMixin (`mixins/three_d_plots.py`)
- `add_scatter3d(data?, x, y, z, ...)`: 3D散点图。
- `add_line3d(data?, x, y, z, ...)`: 3D线图。
- `add_surface(X, Y, Z, ...)`: 3D表面图。
- `add_wireframe(X, Y, Z, ...)`: 3D线框图。

### ModifiersMixin (`mixins/modifiers.py`)
- **子图标签**: `add_subplot_labels(...)`, `add_grouped_labels(...)`
- **轴与标题**: `set_title(...)`, `set_xlabel(...)`, `set_ylabel(...)`, `set_zlabel(...)`, `tick_params(...)`
- **范围与视角**: `set_xlim(...)`, `set_ylim(...)`, `view_init(...)`
- **图例**: `set_legend(...)`, `add_global_legend(...)`
- **画布级**: `set_suptitle(...)`, `fig_add_text(...)`, `fig_add_line(...)`, `fig_add_box(...)`, `fig_add_boundary_box(...)`, `fig_add_label(...)`
- **孪生轴**: `add_twinx(...)`, `add_polar_twin(...)`, `target_primary(...)`, `target_twin(...)`
- **子图元素**: `add_hline(...)`, `add_vline(...)`, `add_text(...)`, `add_patch(...)`, `add_highlight_box(...)`
- **嵌入与缩放**: `add_inset_image(...)`, `add_zoom_inset(...)`, `add_zoom_connectors(...)`
- **特征标记**: `add_peak_highlights(...)`, `add_event_markers(...)`
- **收尾**: `cleanup(...)`, `cleanup_heatmaps(...)`, `save(...)`

---

## 6. 常见问题（FAQ）

### 已知问题及解决方案
- **无法导入 `paperplot`**: 请确保从项目根目录运行，或已将项目安装到Python环境中。
- **双轴颜色相同**: 请为每个系列传入不同的 `label`，`ColorManager` 会按系列名分配稳定颜色。
- **K 线图不显示**: 确保 `time` 列是可排序的，并且 `open`, `high`, `low`, `close` 是数值类型。

### 故障排除指南
- **样式异常**: 使用 `paperplot.utils.list_available_styles()` 查看所有可用样式名。
- **布局异常**: 检查马赛克布局是否为矩形块，嵌套布局字典结构是否正确。
- **双轴图例重复**: 调用 `set_legend('tag')`，库会在主轴上自动合并并去重图例。

---

## 7. 版本历史
- **0.1.10 **: 
  - 新增 `add_figure` 用于集成外部图像。
  - 增强 `add_twinx` 和 `add_polar_twin` 的颜色循环同步。
  - 完善 `add_subplot_labels` 和 `add_grouped_labels` 的延迟绘制机制。
  - 统一并简化了内部 `_execute_plot` 工作流。
- **0.1.7**: 新增10类图表API（分组柱状图、K线图等），修复双轴颜色一致性问题。

> 更多历史记录见 `doc/changelog.md`。
---
id: utils
title: Utils & ColorManager API
sidebar_label: 工具与颜色
---

## 概述

`paperplot.utils` 模块提供了一系列辅助函数和类，用于支持 `Plotter` 的核心功能，例如样式管理、布局解析和颜色管理。

---

## 样式管理

### `get_style_path(style_name)`
- **签名**: `get_style_path(style_name: str) -> str`
- **用途**: 获取预定义样式文件的绝对路径。它首先在 `paperplot/styles` 目录中查找，如果找不到，则作为包资源回退查找。
- **参数**: `style_name` (`str`) - 样式名称，不带 `.mplstyle` 扩展名。
- **返回**: 样式文件的绝对路径。
- **抛出**: `FileNotFoundError` - 如果找不到指定的样式。
- **示例**:
 ```python
 from paperplot import utils
 path = utils.get_style_path('marin_kitagawa')
 plt.style.use(path)
 ```

### `list_available_styles()`
- **签名**: `list_available_styles() -> List[str]`
- **用途**: 列出 `paperplot/styles` 目录下所有可用的内置样式名称。
- **返回**: 一个包含所有样式名称的字符串列表。
- **示例**:
 ```python
 from paperplot import utils
 available_styles = utils.list_available_styles()
 print(available_styles)
 # ['dehya', 'escoffier', 'flat', 'furina', ...]
 ```

---

## 布局与数据处理

### `parse_mosaic_layout(layout)`
- **签名**: `parse_mosaic_layout(layout: List[List[str]]) -> Tuple[Dict, Tuple[int, int]]`
- **用途**: (内部使用) 解析 ASCII 艺术风格的马赛克布局定义，将其转换为结构化的字典，包含每个命名区域的位置和尺寸。
- **返回**: 一个元组，包含 (1) 解析后的布局字典 和 (2) 布局的总行数和总列数。

### `moving_average(data_series, window_size)`
- **签名**: `moving_average(data_series: pd.Series, window_size: int) -> pd.Series`
- **用途**: 对 Pandas Series 数据进行中心对齐的滚动平均，常用于平滑噪声数据。
- **示例**:
 ```python
 smoothed_signal = utils.moving_average(df['noisy_signal'], window_size=10)
 plotter.add_line(x=df['time'], y=smoothed_signal)
 ```

---

## 颜色管理

### `ColorManager` 类
- **用途**: 在 `Plotter` 实例内部用于在多个子图中维护系列颜色的一致性。
- **机制**:
  1. 在 `Plotter` 初始化时，`ColorManager` 会从当前 Matplotlib 样式中加载颜色循环。
  2. 当一个绘图方法（如 `add_line`）被调用时，如果提供了 `label` 参数但没有提供 `color` 参数，`Plotter` 会调用 `color_manager.get_color(label)`。
  3. `get_color` 方法会检查该 `label` 是否已经有关联的颜色。
     - 如果有，则返回缓存的颜色。
     - 如果没有，则从颜色循环中分配一个新颜色，缓存它，然后返回。
  4. 如果颜色循环用尽，它会自动从头开始，实现循环使用。

- **直接使用 (不推荐, 但可行)**:
 ```python
 from paperplot.utils import ColorManager
 cm = ColorManager()
 color1 = cm.get_color('Series A') # 分配第一个颜色
 color2 = cm.get_color('Series B') # 分配第二个颜色
 color3 = cm.get_color('Series A') # 返回与第一次相同的颜色
 print(color1 == color3) # True
 ```
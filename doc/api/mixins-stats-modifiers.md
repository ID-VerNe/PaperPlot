---
id: mixins-stats-modifiers
title: StatsModifiersMixin API
sidebar_label: 统计标注
---

## 概述

`StatsModifiersMixin` 提供在图表上添加统计检验结果标注的功能。这些方法通常在绘制了箱线图、柱状图等分类数据图表之后使用。

---

### `add_stat_test`
- **签名**: `add_stat_test(x, y, group1, group2, test?, text_offset?, y_level?, ...)`
- **用途**: 在两组数据之间执行统计检验，并在图上用横线和星号（如 `*`, `**`, `***`）标注显著性水平。
- **使用前提**: 必须先调用一个绘图方法（如 `add_box`）来填充 `data_cache` 并设置坐标轴。
- **核心参数**:
  - `x`: `str`, 用于分组的分类变量的列名。
  - `y`: `str`, 用于比较的数值变量的列名。
  - `group1`, `group2`: `str`, `x` 列中表示要比较的两组的标签值。
  - `test`: `str` (可选), 要执行的统计检验。
    - `'t-test_ind'`: 独立样本t检验 (Welch's t-test，默认)。
    - `'mannwhitneyu'`: Mann-Whitney U 检验。
  - `text_offset`: `float` (可选), 当 `y_level` 未指定时，标注线相对于数据最高点的垂直偏移比例。默认为 `0.1`。
  - `y_level`: `float` (可选), 强制指定标注线的绝对Y轴位置。
- **星号含义**:
  - `ns`: p > 0.05 (不显著, 不绘制)
  - `*`: p <= 0.05
  - `**`: p <= 0.01
  - `***`: p <= 0.001
- **示例**:
```python
plotter.add_box(data=df, x='group', y='value', tag='my_box')
plotter.add_stat_test(
    x='group', y='value', 
    group1='A', group2='B', 
    tag='my_box'
)
```

---

### `add_pairwise_tests`
- **签名**: `add_pairwise_tests(x, y, comparisons, test?, text_offset_factor?, ...)`
- **用途**: 自动执行多组成对比较，并在图上智能地堆叠显著性标注，避免重叠。
- **核心参数**:
  - `x`, `y`: 同 `add_stat_test`。
  - `comparisons`: `List[Tuple[str, str]]`, 一个比较对的列表，例如 `[('A', 'B'), ('A', 'C'), ('B', 'C')]`。
  - `test`: `str` (可选), 应用于所有比较的统计检验。
  - `text_offset_factor`: `float` (可选), 每层标注线之间的垂直间距占Y轴范围的比例。默认为 `0.05`。
- **行为**:
  1. 循环调用 `add_stat_test` 执行每次比较。
  2. 自动计算并提升每次标注的 `y_level` 以防止重叠。
  3. 最终自动调整Y轴的上限，以确保所有标注都可见。
- **示例**:
```python
plotter.add_box(data=df, x='group', y='value', tag='my_box')
plotter.add_pairwise_tests(
    x='group', y='value',
    comparisons=[('A', 'B'), ('B', 'C')],
    tag='my_box'
)
```
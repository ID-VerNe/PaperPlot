---
id: mixins-stats-modifiers
title: StatsModifiersMixin API
sidebar_label: 统计标注
---

add_stat_test
- 签名：`add_stat_test(x, y, group1, group2, test?, text_offset?, y_level?, tag?, **kwargs)`
- 用途：在两组数据间执行统计检验并标注显著性星号（如 `*`、`**`、`***`）。
- 参数：
  - `x`：分类列名，用于分组。
  - `y`：数值列名，用于比较。
  - `group1`/`group2`：两组的标签值（与 X 轴刻度标签一致）。
  - `test`（可选）：`'t-test_ind'|'mannwhitneyu'`，默认 `'t-test_ind'`（Welch t-test）。
  - `text_offset`（可选）：当未指定 `y_level` 时，相对最高值的垂直偏移比例，默认 `0.1`。
  - `y_level`（可选）：显著性横线与文本的绝对 Y 位置；未指定时自动计算。
  - `tag`/`**kwargs`：用于 `ax.plot` 与 `ax.text` 的样式参数（如 `color`、`lw`）。
- 行为：
  - 使用当前子图缓存数据与刻度标签构建标签到位置映射；执行检验并将结果转换为星号。
  - 若不显著或为 `ns` 则不绘制；否则绘制横线与星号文本，并记录最近的 Y 位置供后续堆叠使用。
- 示例：
```python
plotter.add_box(data=df, x='group', y='value')
plotter.add_stat_test(x='group', y='value', group1='A', group2='B', test='t-test_ind')
```

add_pairwise_tests
- 签名：`add_pairwise_tests(x, y, comparisons, test?, text_offset_factor?, tag?, **kwargs)`
- 用途：执行多组成对比较并堆叠显著性标注，智能提升 y 轴上限以容纳所有标注。
- 参数：
  - `x`/`y`：列名。
  - `comparisons`：`List[Tuple[str,str]]`，如 `[('A','B'),('A','C')]`。
  - `test`（可选）：同上，默认 `'t-test_ind'`。
  - `text_offset_factor`（可选）：每层标注之间的垂直间距比例，默认 `0.05`。
  - `tag`/`**kwargs`：传递给 `add_stat_test` 并用于绘制样式。
- 行为：循环调用 `add_stat_test` 并逐层提升 `y_level`；最终调整 y 轴上限以展示全部标注；清理临时变量。
- 示例：
```python
plotter.add_pairwise_tests(
  x='group', y='value',
  comparisons=[('A','B'),('B','C')],
  test='t-test_ind', text_offset_factor=0.05
)
```

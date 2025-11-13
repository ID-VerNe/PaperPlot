---
id: mixins-stats-plots
title: StatsPlotsMixin API
sidebar_label: 统计图（Seaborn）
---

add_violin
- 签名：`add_violin(data?, x, y, hue?, tag?, ax?, **kwargs)`
- 用途：小提琴图，封装 `seaborn.violinplot`。
- 参数：
  - `data`：`pd.DataFrame`；`x/y` 列名；`hue` 可选分组列。
  - `tag`/`ax`/`**kwargs`：透传至 `sns.violinplot`（如 `order`、`hue_order`、`palette`、`cut`、`scale`）。
- 数据准备：`data_keys=['x','y','hue']`（`hue` 可选）。
- 示例：
```python
plotter.add_violin(data=df, x='group', y='value', hue='cond', palette='Set2')
```

add_swarm
- 签名：`add_swarm(data?, x, y, hue?, tag?, ax?, **kwargs)`
- 用途：蜂群图，封装 `seaborn.swarmplot`，通过抖动避免散点重叠展示分布。
- 参数：同上。
- 示例：
```python
plotter.add_swarm(data=df, x='group', y='value', hue='cond', size=4)
```

add_joint
- 签名：`add_joint(data, x, y, **kwargs)`
- 用途：联合分布图，封装 `seaborn.jointplot`，替换当前 `Plotter` 的 `fig` 与子图集合。
- 参数：
  - `data`：`pd.DataFrame`；`x/y` 列名。
  - `**kwargs`：如 `kind='scatter'|'kde'|'hist'`、`height`、`color` 等。
- 注意：调用后之前的子图被清除；新 `fig` 与 `axes` 由 `jointplot` 管理。
- 示例：
```python
plotter.add_joint(data=df, x='x', y='y', kind='kde', height=6)
```

add_pair
- 签名：`add_pair(data, **kwargs)`
- 用途：成对关系图网格，封装 `seaborn.pairplot`，替换当前 `fig`。
- 参数：
  - `data`：`pd.DataFrame`。
  - `**kwargs`：如 `hue`、`kind`、`palette`、`markers`、`diag_kind` 等。
- 注意：生成复杂网格；调用后链式修饰器可能无法准确定位到某个子图。
- 示例：
```python
plotter.add_pair(data=df, hue='label', diag_kind='kde')
```

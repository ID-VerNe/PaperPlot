---
id: mixins-ml
title: MachineLearningPlotsMixin API
sidebar_label: 机器学习
---

add_learning_curve
- 签名：`add_learning_curve(train_sizes, train_scores, test_scores, tag?, ax?, title?, xlabel?, ylabel?, train_color?, test_color?, **kwargs)`
- 用途：绘制模型学习曲线，显示训练/验证得分的均值与标准差带。
- 参数：
  - `train_sizes`：`array-like`，一维，长度为刻度数。
  - `train_scores`：`array-like`，二维 `(n_ticks, n_folds)`。
  - `test_scores`：`array-like`，二维 `(n_ticks, n_folds)`。
  - `title`（可选）：默认 `'Learning Curve'`。
  - `xlabel`/`ylabel`（可选）：默认 `'Training examples'`、`'Score'`。
  - `train_color`/`test_color`（可选）：曲线与填充颜色，默认 `'r'`、`'g'`。
  - `tag`/`ax`/`**kwargs`：透传至 `Axes.plot`（如 `linestyle`、`marker`）。
- 行为：计算每个刻度的均值与标准差，绘制填充带与折线，设置标题与轴标签，显示图例。
- 示例：
```python
plotter.add_learning_curve(
  train_sizes=sizes,
  train_scores=train_scores,
  test_scores=test_scores,
  title='Model Learning Curve',
  train_color='tab:blue',
  test_color='tab:orange'
)
```

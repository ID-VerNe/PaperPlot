---
id: mixins-ml
title: MachineLearningPlotsMixin API
sidebar_label: 机器学习
---

## 概述

`MachineLearningPlotsMixin` 提供了用于可视化机器学习模型性能的专用图表。

---

### `add_learning_curve`
- **签名**: `add_learning_curve(train_sizes, train_scores, test_scores, tag?, ax?, title?, xlabel?, ylabel?, ...)`
- **用途**: 绘制模型的学习曲线，用于诊断模型的偏差-方差问题（即欠拟合或过拟合）。它会显示训练得分和交叉验证得分随训练样本数量变化的趋势，并用阴影区域表示得分的标准差范围。
- **核心参数**:
  - `train_sizes`: `array-like`, 一维数组，表示用于生成学习曲线的训练样本数量的刻度。
  - `train_scores`: `array-like`, 二维数组，形状为 `(n_ticks, n_folds)`，表示模型在训练集上的得分。
  - `test_scores`: `array-like`, 二维数组，形状与 `train_scores` 相同，表示模型在交叉验证集上的得分。
  - `title`: `str` (可选), 图表标题。默认为 `'Learning Curve'`。
  - `xlabel`/`ylabel`: `str` (可选), 坐标轴标签。默认为 `'Training examples'` 和 `'Score'`。
  - `train_color`/`test_color`: `str` (可选), 分别用于训练得分和验证得分曲线的颜色。
- **示例**:
```python
from sklearn.model_selection import learning_curve

# 假设 model, X, y 已经定义
train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=5, n_jobs=-1, 
    train_sizes=np.linspace(.1, 1.0, 5)
)

plotter.add_learning_curve(
  train_sizes=train_sizes,
  train_scores=train_scores,
  test_scores=test_scores,
  title='Learning Curve for My Model'
)
```
# paperplot/mixins/ml_plots.py

from typing import Optional, Union
import numpy as np
import matplotlib.pyplot as plt

class MachineLearningPlotsMixin:
    """
    包含机器学习相关绘图方法的 Mixin 类。
    """
    def add_learning_curve(self, train_sizes: np.ndarray, train_scores: np.ndarray, test_scores: np.ndarray,
                           tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上可视化模型的学习曲线，帮助判断模型是过拟合还是欠拟合。

        Args:
            train_sizes (np.ndarray): 训练样本数量的数组。
            train_scores (np.ndarray): 训练得分矩阵，维度为 (n_ticks, n_folds)。
            test_scores (np.ndarray): 交叉验证得分矩阵，维度为 (n_ticks, n_folds)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `ax.plot` 和 `ax.fill_between` 的关键字参数。
                      可以包含 'title', 'xlabel', 'ylabel' 来自定义标签。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)

        _ax.grid(True)

        # Extract specific kwargs for title, xlabel, ylabel
        title = kwargs.pop('title', 'Learning Curve')
        xlabel = kwargs.pop('xlabel', "Training examples")
        ylabel = kwargs.pop('ylabel', "Score")

        # Extract specific colors, so they are not passed to plot/fill_between
        train_color = kwargs.pop('train_color', 'r')
        test_color = kwargs.pop('test_color', 'g')

        # 绘制训练得分曲线和标准差区域
        _ax.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color=train_color)
        _ax.plot(train_sizes, train_scores_mean, 'o-', color=train_color,
                 label="Training score", **kwargs)

        # 绘制交叉验证得分曲线和标准差区域
        _ax.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color=test_color)
        _ax.plot(train_sizes, test_scores_mean, 'o-', color=test_color,
                 label="Cross-validation score", **kwargs)

        _ax.legend(loc="best")
        
        # Set title, xlabel, ylabel using Plotter's methods
        self.set_title(title, tag=resolved_tag)
        self.set_xlabel(xlabel, tag=resolved_tag)
        self.set_ylabel(ylabel, tag=resolved_tag)
        
        self.last_active_tag = resolved_tag
        return self

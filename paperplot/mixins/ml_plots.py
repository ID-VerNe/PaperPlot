# paperplot/mixins/ml_plots.py

from typing import Optional, Union
import numpy as np
import matplotlib.pyplot as plt

class MachineLearningPlotsMixin:
    """
    包含机器学习相关绘图方法的 Mixin 类。
    """
    def add_learning_curve(self, **kwargs) -> 'Plotter':
        """
        在子图上可视化模型的学习曲线。
        所有参数通过 `kwargs` 传入。

        必需参数: `train_sizes`, `train_scores`, `test_scores`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            # 多维数组直接从 p_kwargs (即 final_kwargs) 中获取
            train_scores = p_kwargs.pop('train_scores')
            test_scores = p_kwargs.pop('test_scores')
            # 一维数组从 data_map 中获取
            train_sizes = data_map['train_sizes']

            train_scores_mean = np.mean(train_scores, axis=1)
            train_scores_std = np.std(train_scores, axis=1)
            test_scores_mean = np.mean(test_scores, axis=1)
            test_scores_std = np.std(test_scores, axis=1)

            ax.grid(True)

            title = p_kwargs.pop('title', 'Learning Curve')
            xlabel = p_kwargs.pop('xlabel', "Training examples")
            ylabel = p_kwargs.pop('ylabel', "Score")
            train_color = p_kwargs.pop('train_color', 'r')
            test_color = p_kwargs.pop('test_color', 'g')

            ax.fill_between(train_sizes, train_scores_mean - train_scores_std,
                             train_scores_mean + train_scores_std, alpha=0.1,
                             color=train_color)
            ax.plot(train_sizes, train_scores_mean, 'o-', color=train_color,
                     label="Training score", **p_kwargs)

            ax.fill_between(train_sizes, test_scores_mean - test_scores_std,
                             test_scores_mean + test_scores_std, alpha=0.1,
                             color=test_color)
            ax.plot(train_sizes, test_scores_mean, 'o-', color=test_color,
                     label="Cross-validation score", **p_kwargs)

            ax.legend(loc="best")
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['train_sizes'],
            plot_defaults_key=None,
            **kwargs
        )

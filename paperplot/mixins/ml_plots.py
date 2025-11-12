# paperplot/mixins/ml_plots.py

from typing import Optional, Union
import numpy as np
import matplotlib.pyplot as plt

class MachineLearningPlotsMixin:
    """包含机器学习相关绘图方法的 Mixin 类。"""
    def add_learning_curve(self, **kwargs) -> 'Plotter':
        """在子图上可视化模型的学习曲线。

        此方法绘制了训练集和交叉验证集的得分随训练样本数量变化的曲线，
        并填充了得分的标准差范围，以展示模型的学习性能。

        Args:
            train_sizes (array-like):
                用于生成学习曲线的训练样本数量的一维数组。
            train_scores (array-like):
                在训练集上的得分，形状为 `(n_ticks, n_folds)`，
                其中 `n_ticks` 是 `train_sizes` 的长度。
            test_scores (array-like):
                在交叉验证集上的得分，形状与 `train_scores` 相同。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            title (str, optional): 图表标题。默认为 'Learning Curve'。
            xlabel (str, optional): X轴标签。默认为 'Training examples'。
            ylabel (str, optional): Y轴标签。默认为 'Score'。
            train_color (str, optional): 训练得分曲线的颜色。默认为 'r'。
            test_color (str, optional): 验证得分曲线的颜色。默认为 'g'。
            **kwargs: 其他传递给 `ax.plot` 的关键字参数。

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
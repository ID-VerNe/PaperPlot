from typing import Optional, Union, Callable
import seaborn as sns

class WrapperPlotsMixin:
    def add_seaborn(self, **kwargs) -> 'Plotter':
        """在子图上使用任意指定的Seaborn函数进行绘图。

        这是一个通用包装器，允许调用任何 Seaborn 绘图函数。

        Args:
            **kwargs:
                核心参数:
                - plot_func (Callable): Seaborn 绘图函数 (e.g., `sns.violinplot`)。
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x, y, hue, size, style, col, row (str, optional): 映射到 Seaborn 函数的数据列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - ... 其他传递给 `plot_func` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果未提供 `plot_func`。
        """
        plot_func = kwargs.pop('plot_func', None)
        if plot_func is None:
            raise ValueError("`add_seaborn` requires a 'plot_func' argument (e.g., sns.violinplot).")

        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            plot_func(data=cache_df, ax=ax, **data_names, **p_kwargs)
            return None

        possible_keys = ['x', 'y', 'hue', 'size', 'style', 'col', 'row']
        data_keys = [key for key in possible_keys if key in kwargs]

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=data_keys,
            plot_defaults_key=None,
            **kwargs
        )

    def add_regplot(self, **kwargs) -> 'Plotter':
        """在子图上绘制散点图和线性回归模型拟合 (封装 `seaborn.regplot`)。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str): x轴数据列名。
                - y (str): y轴数据列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - scatter_kws (Dict, optional): 传递给散点图的参数。
                - line_kws (Dict, optional): 传递给回归线的参数。
                - ci (int, optional): 置信区间大小 (0-100)。
                - ... 其他传递给 `sns.regplot` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            scatter_kws = p_kwargs.pop('scatter_kws', {})
            line_kws = p_kwargs.pop('line_kws', {})
            
            default_scatter_kwargs = self._get_plot_defaults('scatter')
            scatter_kws = {**default_scatter_kwargs, **scatter_kws}

            sns.regplot(data=cache_df, x=data_names['x'], y=data_names['y'], ax=ax, 
                        scatter_kws=scatter_kws, line_kws=line_kws, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y'],
            plot_defaults_key=None,
            **kwargs
        )

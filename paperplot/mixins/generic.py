# paperplot/mixins/generic.py

from typing import Optional, Union, List, Callable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ..exceptions import DuplicateTagError
from ..utils import _data_to_dataframe

class GenericPlotsMixin:
    """
    包含通用绘图方法的 Mixin 类。
    这些方法是常见图表类型（如线图、散点图、柱状图等）的直接封装。
    """

    def add_line(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list, np.ndarray, pd.Series]] = None, 
                 y: Optional[Union[str, list, np.ndarray, pd.Series]] = None, 
                 tag: Optional[Union[str, int]] = None,
                 ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制线图。
        支持两种数据传入方式:
        1. data=df, x='col_name', y='col_name'
        2. x=[...], y=[...]

        Args:
            data (Optional[pd.DataFrame]): 包含绘图数据的数据框。
            x: x轴数据。可以是列名(str)或数据本身(array-like)。
            y: y轴数据。可以是列名(str)或数据本身(array-like)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_map, cache_df = self._prepare_data(data=data, x=x, y=y)

        final_kwargs = {**self._get_plot_defaults('line'), **kwargs}
        _ax.plot(data_map['x'], data_map['y'], **final_kwargs)
        
        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_bar(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                y: Optional[Union[str, list]] = None, y_err: Optional[Union[str, list]] = None,
                tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制柱状图。
        支持灵活的数据输入。

        Args:
            data (Optional[pd.DataFrame]): 数据框。
            x: x轴数据 (列名或array-like)。
            y: y轴数据 (列名或array-like)。
            y_err (Optional): y轴误差数据 (列名或array-like)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.bar` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_map, cache_df = self._prepare_data(data=data, x=x, y=y)
        x_data, y_data = data_map['x'], data_map['y']
        
        y_error_values = None
        if y_err is not None:
            if isinstance(data, pd.DataFrame):
                if not isinstance(y_err, str):
                    raise ValueError("If 'data' is a DataFrame, 'y_err' must be a string.")
                y_error_values = data[y_err]
                if y_err not in cache_df.columns:
                    cache_df = pd.concat([cache_df, data[[y_err]]], axis=1)
            else:
                y_error_values = y_err

        final_kwargs = {**self._get_plot_defaults('bar'), **kwargs}
        _ax.bar(x_data, y_data, yerr=y_error_values, **final_kwargs)
        
        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_scatter(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                    y: Optional[Union[str, list]] = None, tag: Optional[Union[str, int]] = None,
                    ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制散点图。
        支持灵活的数据输入，并支持将列映射到大小(`s`)和颜色(`c`)。

        Args:
            data (Optional[pd.DataFrame]): 数据框。
            x: x轴数据 (列名或array-like)。
            y: y轴数据 (列名或array-like)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.scatter` 的参数。
                      如果 's' 或 'c' 的值是字符串，则会从 `data` 中获取该列。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

        data_kwargs = {'x': x, 'y': y}
        plot_kwargs = kwargs.copy()

        s_col = plot_kwargs.get('s')
        c_col = plot_kwargs.get('c')
        if isinstance(s_col, str):
            data_kwargs['s'] = s_col
        if isinstance(c_col, str):
            data_kwargs['c'] = c_col

        data_map, cache_df = self._prepare_data(data=data, **data_kwargs)
        x_data, y_data = data_map.pop('x'), data_map.pop('y')

        if isinstance(s_col, str):
            plot_kwargs['s'] = data_map.pop('s')
        if isinstance(c_col, str):
            plot_kwargs['c'] = data_map.pop('c')
        
        final_kwargs = {**self._get_plot_defaults('scatter'), **plot_kwargs}
        scatter_mappable = _ax.scatter(x_data, y_data, **final_kwargs)
        
        if 'c' in final_kwargs and final_kwargs['c'] is not None:
             self.tag_to_mappable[resolved_tag] = scatter_mappable

        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_hist(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                 tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                 **kwargs) -> 'Plotter':
        """
        在子图上绘制直方图。

        Args:
            data (Optional[pd.DataFrame]): 数据框。
            x: 用于绘制直方图的数据 (列名或array-like)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.hist` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_map, cache_df = self._prepare_data(data=data, x=x)

        final_kwargs = {**self._get_plot_defaults('hist'), **kwargs}
        _ax.hist(data_map['x'], **final_kwargs)
        
        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_box(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                y: Optional[Union[str, list]] = None, hue: Optional[Union[str, list]] = None,
                tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                **kwargs) -> 'Plotter':
        """
        在子图上绘制箱线图 (封装 `seaborn.boxplot`)。

        Args:
            data: 数据框 (推荐) 或 None。
            x, y, hue: 列名或array-like数据。
            tag: 目标子图的tag。
            ax: 目标Axes。
            **kwargs: 其他传递给 `seaborn.boxplot` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_to_plot = data
        plot_kwargs = kwargs.copy()
        
        if data is None:
            df_kwargs = {}
            if x is not None: df_kwargs['x'] = x
            if y is not None: df_kwargs['y'] = y
            if hue is not None: df_kwargs['hue'] = hue
            
            data_to_plot = _data_to_dataframe(**df_kwargs)
            
            plot_kwargs['x'] = 'x' if x is not None else None
            plot_kwargs['y'] = 'y' if y is not None else None
            plot_kwargs['hue'] = 'hue' if hue is not None else None
        else:
            plot_kwargs['x'] = x
            plot_kwargs['y'] = y
            plot_kwargs['hue'] = hue

        sns.boxplot(data=data_to_plot, ax=_ax, **plot_kwargs)
        self.data_cache[resolved_tag] = data_to_plot
        self.last_active_tag = resolved_tag
        return self

    def add_heatmap(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                    **kwargs) -> 'Plotter':
        """
        在子图上绘制热图 (封装 `seaborn.heatmap`)。
        此方法要求输入为DataFrame。

        Args:
            data (pd.DataFrame): 用于绘制热图的二维数据。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 其他传递给 `seaborn.heatmap` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

        create_cbar = kwargs.pop('cbar', True)
        sns.heatmap(data, ax=_ax, cbar=create_cbar, **kwargs)

        if hasattr(_ax, 'collections') and _ax.collections:
            self.tag_to_mappable[resolved_tag] = _ax.collections[0]

        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

    def add_seaborn(self, plot_func: Callable, data: Optional[pd.DataFrame] = None,
                    tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                    **kwargs) -> 'Plotter':
        """
        在子图上使用指定的Seaborn函数进行绘图。

        Args:
            plot_func (Callable): 要调用的Seaborn绘图函数 (例如 `sns.violinplot`)。
            data (Optional[pd.DataFrame]): 数据框。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 传递给 `plot_func` 的参数 (例如 x, y, hue)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_to_plot = data
        plot_kwargs = kwargs.copy()

        if data is None:
            # 从kwargs中提取可能是数据系列的内容
            array_like_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, (list, np.ndarray, pd.Series))}
            data_to_plot = _data_to_dataframe(**array_like_kwargs)
            
            # 更新kwargs，将列名传递给seaborn函数
            for k in array_like_kwargs:
                plot_kwargs[k] = k
        
        plot_func(data=data_to_plot, ax=_ax, **plot_kwargs)
        
        if data_to_plot is not None:
            self.data_cache[resolved_tag] = data_to_plot

        self.last_active_tag = resolved_tag
        return self

    def add_blank(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        在指定或下一个可用的子图位置创建一个空白区域并关闭坐标轴。

        Args:
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag)
        _ax.axis('off')
        self.last_active_tag = resolved_tag
        return self

    def add_regplot(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                    y: Optional[Union[str, list]] = None, tag: Optional[str] = None, 
                    ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制散点图和线性回归模型拟合 (封装 `seaborn.regplot`)。

        Args:
            data: 数据框 (推荐) 或 None。
            x, y: 列名或array-like数据。
            tag: 目标子图的tag。
            ax: 目标Axes。
            **kwargs: 其他传递给 `seaborn.regplot` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_to_plot = data
        x_col, y_col = x, y
        
        if data is None:
            data_to_plot = _data_to_dataframe(x=x, y=y)
            x_col, y_col = 'x', 'y'

        # Extract scatter_kws and line_kws from kwargs
        scatter_kws = kwargs.pop('scatter_kws', {})
        line_kws = kwargs.pop('line_kws', {})

        # Merge default scatter plot arguments into scatter_kws
        default_scatter_kwargs = self._get_plot_defaults('scatter')
        scatter_kws = {**default_scatter_kwargs, **scatter_kws}

        # Pass remaining kwargs directly to sns.regplot (e.g., color, marker, etc.)
        # Note: sns.regplot also accepts 'color' directly for both scatter and line.
        # If 'color' is in kwargs, it will apply to both.
        # If 'color' is in scatter_kws or line_kws, it will override.

        sns.regplot(data=data_to_plot, x=x_col, y=y_col, ax=_ax, 
                    scatter_kws=scatter_kws, line_kws=line_kws, **kwargs)
        
        self.data_cache[resolved_tag] = data_to_plot
        self.last_active_tag = resolved_tag
        return self

    def add_conditional_scatter(self, data: pd.DataFrame, x: str, y: str, condition: pd.Series, 
                                tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在散点图上根据条件突出显示特定的数据点。
        此方法要求输入为DataFrame。

        Args:
            data (pd.DataFrame): 包含绘图数据的DataFrame。
            x (str): X轴数据的列名。
            y (str): Y轴数据的列名。
            condition (pd.Series): 一个布尔值的Series，与data的行数相同。
                                   为True的数据点将被高亮。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 传递给 `ax.scatter` 的关键字参数。
                      可以为高亮和非高亮状态分别设置参数，
                      例如 `s_highlight=50`, `c_highlight='red'`, `s_normal=10`。
        
        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

        base_defaults = self._get_plot_defaults('scatter')
        
        normal_kwargs = {
            's': kwargs.pop('s_normal', base_defaults.get('s', 20)),
            'c': kwargs.pop('c_normal', 'gray'),
            'alpha': kwargs.pop('alpha_normal', base_defaults.get('alpha', 0.5)),
            'label': kwargs.pop('label_normal', 'Other points')
        }
        highlight_kwargs = {
            's': kwargs.pop('s_highlight', 60),
            'c': kwargs.pop('c_highlight', 'red'),
            'alpha': kwargs.pop('alpha_highlight', 1.0),
            'label': kwargs.pop('label_highlight', 'Highlighted')
        }
        
        normal_kwargs.update(kwargs)
        highlight_kwargs.update(kwargs)

        _ax.scatter(data.loc[~condition, x], data.loc[~condition, y], **normal_kwargs)
        _ax.scatter(data.loc[condition, x], data.loc[condition, y], **highlight_kwargs)
        
        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

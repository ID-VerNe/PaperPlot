# paperplot/mixins/generic.py
import colorsys
from typing import Optional, Union, List, Callable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

from ..exceptions import DuplicateTagError
from ..utils import _data_to_dataframe

class GenericPlotsMixin:
    """
    包含通用绘图方法的 Mixin 类。
    这些方法是常见图表类型（如线图、散点图、柱状图等）的直接封装。
    """

    def add_line(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制线图。
        所有参数通过 `kwargs` 传入，支持 `data`, `x`, `y`, `tag`, `ax` 以及
        所有 `matplotlib.axes.Axes.plot` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        plot_logic = lambda ax, data_map, cache_df, data_names, **p_kwargs: ax.plot(data_map['x'], data_map['y'], **p_kwargs)
        
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y'],
            plot_defaults_key='line',
            **kwargs
        )

    def add_bar(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制条形图 (封装 `matplotlib.axes.Axes.bar`)。
        所有参数通过 `kwargs` 传入。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            y_err = p_kwargs.pop('y_err', None)
            ax.bar(data_map['x'], data_map['y'], yerr=y_err, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'y_err'],
            plot_defaults_key='bar',
            **kwargs
        )

    def add_scatter(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制散点图。
        所有参数通过 `kwargs` 传入，支持 `data`, `x`, `y`, `s`, `c`, `tag`, `ax` 以及
        所有 `matplotlib.axes.Axes.scatter` 的参数。
        如果 `s` 或 `c` 的值是字符串，它们将被解释为 `data` DataFrame 中的列名。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def _plot_scatter_logic(ax, data_map, cache_df, data_names, **plot_kwargs):
            # 检查 's' 和 'c' 是否需要从 data_map 中获取
            if 's' in plot_kwargs and isinstance(plot_kwargs['s'], str):
                plot_kwargs['s'] = data_map.get(plot_kwargs['s'])
            if 'c' in plot_kwargs and isinstance(plot_kwargs['c'], str):
                plot_kwargs['c'] = data_map.get(plot_kwargs['c'])
            
            mappable = ax.scatter(data_map['x'], data_map['y'], **plot_kwargs)
            return mappable

        # 包含所有可能的数据列名
        data_keys = ['x', 'y']
        if 's' in kwargs and isinstance(kwargs['s'], str):
            data_keys.append('s')
        if 'c' in kwargs and isinstance(kwargs['c'], str):
            data_keys.append('c')

        return self._execute_plot(
            plot_func=_plot_scatter_logic,
            data_keys=data_keys,
            plot_defaults_key='scatter',
            **kwargs
        )

    def add_hist(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制直方图。
        所有参数通过 `kwargs` 传入，支持 `data`, `x`, `tag`, `ax` 以及
        所有 `matplotlib.axes.Axes.hist` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        plot_logic = lambda ax, data_map, cache_df, data_names, **p_kwargs: ax.hist(data_map['x'], **p_kwargs)
        
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x'],
            plot_defaults_key='hist',
            **kwargs
        )

    def add_box(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制箱线图 (封装 `seaborn.boxplot`)。
        所有参数通过 `kwargs` 传入。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue')
            sns.boxplot(data=cache_df, x=data_names['x'], y=data_names['y'], hue=hue_col, ax=ax, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'hue'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_heatmap(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制热图 (封装 `seaborn.heatmap`)。
        此方法会自动检测当前样式中的调色板，并用其创建一个匹配的
        连续色图(Colormap)，除非用户手动指定了 `cmap` 参数。
        新的版本会自动将调色板中的颜色按亮度排序，以创建
        一个视觉上更直观的颜色梯度。
        """

        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            # 1. 智能匹配 cmap 的逻辑
            if 'cmap' not in p_kwargs:
                try:
                    # 1a. 获取当前样式颜色循环中的第一个颜色作为主色
                    primary_color = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
                    
                    # 1b. 使用 seaborn 的 light_palette 基于主色创建一个平滑的连续色图
                    #      这是一个从浅(白)到深(主色)的渐变
                    custom_cmap = sns.light_palette(primary_color, as_cmap=True)
                    
                    p_kwargs['cmap'] = custom_cmap
                except (KeyError, IndexError):
                    # 1c. 如果获取主色失败（例如，样式文件中没有定义颜色循环），
                    #     则优雅地回退到一个标准的、高质量的色图
                    p_kwargs.setdefault('cmap', 'viridis')

            # --- 错误修正：将以下代码块移入 plot_logic 函数内部 ---
            create_cbar = p_kwargs.pop('cbar', True)
            sns.heatmap(cache_df, ax=ax, cbar=create_cbar, **p_kwargs)

            if hasattr(ax, 'collections') and ax.collections:
                return ax.collections[0]
            return None
            # --- 修正结束 ---

        # _execute_plot 的调用保持不变
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key=None,
            **kwargs
        )

    def add_seaborn(self, **kwargs) -> 'Plotter':
        """
        在子图上使用指定的Seaborn函数进行绘图。
        """
        plot_func = kwargs.pop('plot_func', None)
        if plot_func is None:
            raise ValueError("`add_seaborn` requires a 'plot_func' argument (e.g., sns.violinplot).")

        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            # 这里的 cache_df 已经是准备好的数据
            # data_names 包含了 x, y, hue 等的原始列名
            plot_func(data=cache_df, ax=ax, **data_names, **p_kwargs)
            # 大多数 seaborn 函数不直接返回 mappable，所以返回 None
            return None

        # 动态确定需要准备的数据键
        possible_keys = ['x', 'y', 'hue', 'size', 'style', 'col', 'row']
        data_keys = [key for key in possible_keys if key in kwargs]

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=data_keys,
            plot_defaults_key=None,
            **kwargs
        )

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

    def add_regplot(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制散点图和线性回归模型拟合 (封装 `seaborn.regplot`)。
        所有参数通过 `kwargs` 传入。
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
            plot_defaults_key=None, # regplot 有自己的样式逻辑
            **kwargs
        )

    def add_conditional_scatter(self, **kwargs) -> 'Plotter':
        """
        在散点图上根据条件突出显示特定的数据点。
        所有参数通过 `kwargs` 传入。

        必需参数: `x`, `y`, `condition` (布尔 Series 或列名)。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            x_col = data_names['x']
            y_col = data_names['y']
            condition_col = data_names['condition']
            condition = cache_df[condition_col] # 获取布尔 Series

            base_defaults = self._get_plot_defaults('scatter')
            
            # 提取并设置普通点样式
            normal_kwargs = {
                's': p_kwargs.pop('s_normal', base_defaults.get('s', 20)),
                'c': p_kwargs.pop('c_normal', 'gray'),
                'alpha': p_kwargs.pop('alpha_normal', base_defaults.get('alpha', 0.5)),
                'label': p_kwargs.pop('label_normal', 'Other points')
            }
            # 提取并设置高亮点样式
            highlight_kwargs = {
                's': p_kwargs.pop('s_highlight', 60),
                'c': p_kwargs.pop('c_highlight', 'red'),
                'alpha': p_kwargs.pop('alpha_highlight', 1.0),
                'label': p_kwargs.pop('label_highlight', 'Highlighted')
            }
            
            # 将剩余的通用 kwargs 应用到两者
            normal_kwargs.update(p_kwargs)
            highlight_kwargs.update(p_kwargs)

            # 绘制非高亮点
            ax.scatter(cache_df.loc[~condition, x_col], cache_df.loc[~condition, y_col], **normal_kwargs)
            # 绘制高亮点
            mappable = ax.scatter(cache_df.loc[condition, x_col], cache_df.loc[condition, y_col], **highlight_kwargs)
            
            # 返回高亮点的 mappable
            return mappable

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'condition'],
            plot_defaults_key=None, # 样式在 plot_logic 中手动处理
            **kwargs
        )

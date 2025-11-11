# paperplot/mixins/stats_plots.py

from typing import Optional, Union
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ..exceptions import PlottingError

class StatsPlotsMixin:
    """
    包含基于Seaborn的统计绘图方法的 Mixin 类。
    """
    def add_violin(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制小提琴图 (封装 `seaborn.violinplot`)。
        所有参数通过 `kwargs` 传入。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue') 
            sns.violinplot(data=cache_df, x=data_names['x'], y=data_names['y'], hue=hue_col, ax=ax, **p_kwargs)
            return None # 小提琴图不返回 mappable

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'hue'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_swarm(self, **kwargs) -> 'Plotter':
        """
        在子图上绘制蜂群图 (封装 `seaborn.swarmplot`)。
        所有参数通过 `kwargs` 传入。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue')
            sns.swarmplot(data=cache_df, x=data_names['x'], y=data_names['y'], hue=hue_col, ax=ax, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'hue'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_joint(self, **kwargs) -> 'Plotter':
        """
        绘制一个联合分布图，它会占据整个画布。
        所有参数通过 `kwargs` 传入。
        
        警告：此方法会清除画布上所有现有的子图。

        必需参数: `data`, `x`, `y`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        data = kwargs.pop('data')
        x = kwargs.pop('x')
        y = kwargs.pop('y')

        if self.axes:
            self.fig.clf() # 清除整个画布
            self.axes.clear()
            self.tag_to_ax.clear()

        g = sns.jointplot(data=data, x=x, y=y, **kwargs)
        
        # jointplot创建了自己的figure，我们需要替换掉Plotter的figure
        plt.close(self.fig) # 关闭旧的figure
        self.fig = g.fig
        
        # jointplot有多个axes，我们只将主ax设为活动ax
        self.axes = [g.ax_joint] + list(self.fig.axes)
        self.tag_to_ax = {'joint': g.ax_joint, 'marg_x': g.ax_marg_x, 'marg_y': g.ax_marg_y}
        self.last_active_tag = 'joint'
        self.data_cache['joint'] = data
        
        return self

    def add_pair(self, **kwargs) -> 'Plotter':
        """
        绘制一个展示数据集中成对关系图，它会占据整个画布。
        所有参数通过 `kwargs` 传入。

        警告：此方法会清除画布上所有现有的子图。

        必需参数: `data`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        data = kwargs.pop('data')

        if self.axes:
            self.fig.clf()
            self.axes.clear()
            self.tag_to_ax.clear()

        g = sns.pairplot(data=data, **kwargs)
        
        plt.close(self.fig)
        self.fig = g.fig
        
        # pairplot创建了多个axes，我们无法简单地选择一个作为活动ax
        # 因此，调用此方法后，链式修饰器可能无法正常工作
        self.axes = list(g.axes.flatten())
        self.last_active_tag = None # 没有明确的活动ax
        self.data_cache['pairplot'] = data

        return self

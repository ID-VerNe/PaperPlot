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
    def add_violin(self, data: pd.DataFrame, x: str, y: str,
                   tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制小提琴图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): X轴数据的列名。
            y (str): Y轴数据的列名。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `seaborn.violinplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        sns.violinplot(data=data, x=x, y=y, ax=_ax, **kwargs)
        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

    def add_swarm(self, data: pd.DataFrame, x: str, y: str,
                  tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制蜂群图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): X轴数据的列名。
            y (str): Y轴数据的列名。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `seaborn.swarmplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        sns.swarmplot(data=data, x=x, y=y, ax=_ax, **kwargs)
        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

    def add_joint(self, data: pd.DataFrame, x: str, y: str, **kwargs) -> 'Plotter':
        """
        绘制一个联合分布图，它会占据整个画布。
        
        警告：此方法会清除画布上所有现有的子图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): X轴数据的列名。
            y (str): Y轴数据的列名。
            **kwargs: 其他传递给 `seaborn.jointplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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

    def add_pair(self, data: pd.DataFrame, **kwargs) -> 'Plotter':
        """
        绘制一个展示数据集中成对关系图，它会占据整个画布。

        警告：此方法会清除画布上所有现有的子图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            **kwargs: 其他传递给 `seaborn.pairplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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

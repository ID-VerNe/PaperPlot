# paperplot/mixins/stats_plots.py

from typing import Optional, Union
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ..exceptions import PlottingError

class StatsPlotsMixin:
    """包含基于Seaborn的统计绘图方法的 Mixin 类。"""
    def add_violin(self, **kwargs) -> 'Plotter':
        """在子图上绘制小提琴图 (封装 `seaborn.violinplot`)。

        小提琴图是箱形图和核密度估计图的结合。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名，通常是分类变量。
            y (str or array-like): y轴数据或 `data` 中的列名，通常是数值变量。
            hue (str, optional): 用于产生不同颜色小提琴的分类变量的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `seaborn.violinplot` 的关键字参数，
                      例如 `order`, `hue_order`, `palette`, `cut`, `scale` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue') 
            sns.violinplot(data=cache_df, x=data_names.get('x'), y=data_names.get('y'), hue=hue_col, ax=ax, **p_kwargs)
            return None # 小提琴图不返回 mappable

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'hue'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_swarm(self, **kwargs) -> 'Plotter':
        """在子图上绘制蜂群图 (封装 `seaborn.swarmplot`)。

        蜂群图是一种散点图，其中点被调整以避免重叠，
        可以很好地展示值的分布。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名，通常是分类变量。
            y (str or array-like): y轴数据或 `data` 中的列名，通常是数值变量。
            hue (str, optional): 用于产生不同颜色点的分类变量的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `seaborn.swarmplot` 的关键字参数，
                      例如 `order`, `hue_order`, `palette`, `size` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue')
            sns.swarmplot(data=cache_df, x=data_names.get('x'), y=data_names.get('y'), hue=hue_col, ax=ax, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'hue'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_joint(self, **kwargs) -> 'Plotter':
        """绘制一个联合分布图，该图会占据并替换整个当前画布。

        此方法封装了 `seaborn.jointplot`，用于可视化两个变量的联合分布
        和各自的边缘分布。

        警告:
            此方法会创建一个新的Figure对象并替换掉 `Plotter` 实例中
            原有的 `fig` 和 `axes`。调用此方法后，之前的所有子图都将
            被清除。后续的链式调用将作用于此方法新创建的子图上。

        Args:
            data (pd.DataFrame): 包含绘图数据的DataFrame。
            x (str): `data` 中表示x轴数据的列名。
            y (str): `data` 中表示y轴数据的列名。
            **kwargs: 其他传递给 `seaborn.jointplot` 的关键字参数，
                      例如 `kind` ('scatter', 'kde', 'hist'), `color`, `height` 等。

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
        """绘制数据集中成对关系的图，该图会占据并替换整个当前画布。

        此方法封装了 `seaborn.pairplot`，用于在一个网格中展示数据集中
        多个变量两两之间的关系。

        警告:
            此方法会创建一个新的Figure对象并替换掉 `Plotter` 实例中
            原有的 `fig` 和 `axes`。调用此方法后，之前的所有子图都将
            被清除。由于 `pairplot` 创建了一个复杂的Grid，后续的链式
            修饰器方法可能无法准确定位到某个子图。

        Args:
            data (pd.DataFrame): 包含绘图数据的DataFrame。
            **kwargs: 其他传递给 `seaborn.pairplot` 的关键字参数，
                      例如 `hue`, `kind`, `palette`, `markers`, `diag_kind` 等。

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
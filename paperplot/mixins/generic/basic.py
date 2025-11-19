from typing import Optional, Union
import matplotlib.pyplot as plt
import seaborn as sns

class BasicPlotsMixin:
    def add_line(self, **kwargs) -> 'Plotter':
        """在子图上绘制线图 (封装 `matplotlib.axes.Axes.plot`)。"""
        plot_logic = lambda ax, data_map, cache_df, data_names, **p_kwargs: ax.plot(data_map['x'], data_map['y'], **p_kwargs)
        
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y'],
            plot_defaults_key='line',
            **kwargs
        )

    def add_bar(self, **kwargs) -> 'Plotter':
        """在子图上绘制条形图 (封装 `matplotlib.axes.Axes.bar`)。"""
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            y_err_data = data_map.get('y_err')
            ax.bar(data_map['x'], data_map['y'], yerr=y_err_data, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'y_err'],
            plot_defaults_key='bar',
            **kwargs
        )

    def add_scatter(self, **kwargs) -> 'Plotter':
        """在子图上绘制散点图 (封装 `matplotlib.axes.Axes.scatter`)。"""
        def _plot_scatter_logic(ax, data_map, cache_df, data_names, **plot_kwargs):
            if 's' in plot_kwargs and isinstance(plot_kwargs['s'], str):
                plot_kwargs['s'] = data_map.get(plot_kwargs['s'])
            if 'c' in plot_kwargs and isinstance(plot_kwargs['c'], str):
                plot_kwargs['c'] = data_map.get(plot_kwargs['c'])
            
            mappable = ax.scatter(data_map['x'], data_map['y'], **plot_kwargs)
            return mappable

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
        """在子图上绘制直方图 (封装 `matplotlib.axes.Axes.hist`)。"""
        plot_logic = lambda ax, data_map, cache_df, data_names, **p_kwargs: ax.hist(data_map['x'], **p_kwargs)
        
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x'],
            plot_defaults_key='hist',
            **kwargs
        )

    def add_box(self, **kwargs) -> 'Plotter':
        """在子图上绘制箱线图 (封装 `seaborn.boxplot`)。"""
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue')
            sns.boxplot(data=cache_df, x=data_names.get('x'), y=data_names.get('y'), hue=hue_col, ax=ax, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'hue'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_heatmap(self, **kwargs) -> 'Plotter':
        """在子图上绘制热图 (封装 `seaborn.heatmap`)。"""
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            if 'cmap' not in p_kwargs:
                try:
                    primary_color = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
                    custom_cmap = sns.light_palette(primary_color, as_cmap=True)
                    p_kwargs['cmap'] = custom_cmap
                except (KeyError, IndexError):
                    p_kwargs.setdefault('cmap', 'viridis')

            create_cbar = p_kwargs.pop('cbar', True)
            sns.heatmap(cache_df, ax=ax, cbar=create_cbar, **p_kwargs)

            if hasattr(ax, 'collections') and ax.collections:
                return ax.collections[0]
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key=None,
            **kwargs
        )

    def add_blank(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """在指定或下一个可用的子图位置创建一个空白区域并关闭坐标轴。"""
        _ax, resolved_tag = self._resolve_ax_and_tag(tag)
        _ax.axis('off')
        self.last_active_tag = resolved_tag
        return self

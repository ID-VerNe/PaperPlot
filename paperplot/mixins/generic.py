# paperplot/mixins/generic.py
import colorsys
from typing import Optional, Union, List, Callable, Dict, Sequence
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import image as mpimg
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

from ..exceptions import DuplicateTagError
from ..utils import _data_to_dataframe

class GenericPlotsMixin:
    """包含通用绘图方法的 Mixin 类。 这些方法是常见图表类型（如线图、散点图、柱状图等）的直接封装。"""

    def add_line(self, **kwargs) -> 'Plotter':
        """在子图上绘制线图 (封装 `matplotlib.axes.Axes.plot`)。

        此方法是 `_execute_plot` 的一个包装器，用于处理线图的通用逻辑。
        数据可以通过 `data` DataFrame 和列名或直接作为关键字参数传入。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名。
            y (str or array-like): y轴数据或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数，
                      例如 `color`, `linestyle`, `marker`, `label` 等。

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
        """在子图上绘制条形图 (封装 `matplotlib.axes.Axes.bar`)。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名 (类别)。
            y (str or array-like): y轴数据或 `data` 中的列名 (高度)。
            y_err (str or array-like, optional): y轴的误差条。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.bar` 的关键字参数，
                      例如 `color`, `width`, `align`, `label` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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

    def add_grouped_bar(self, **kwargs) -> 'Plotter':
        """在子图上绘制多系列分组柱状图。

        Args:
            data (pd.DataFrame): 数据表。
            x (str): 分类列名。
            ys (List[str]): 系列列名列表。
            labels (Dict[str, str], optional): 系列到图例名映射。
            width (float, optional): 分组总宽度，默认 0.8。
            yerr (Dict[str, array-like], optional): 每个系列的误差条。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            x_col = p_kwargs.pop('x')
            y_cols = p_kwargs.pop('ys')
            labels = p_kwargs.pop('labels', {})
            width = p_kwargs.pop('width', 0.8)
            yerr = p_kwargs.pop('yerr', None)
            alpha = p_kwargs.pop('alpha', 0.8)

            x_vals = cache_df[x_col]
            n = len(y_cols)
            base = np.arange(len(x_vals))
            bar_w = width / max(n, 1)

            for i, col in enumerate(y_cols):
                offs = base - width / 2 + i * bar_w + bar_w / 2
                lbl = labels[col] if isinstance(labels, dict) and col in labels else col
                color = self.color_manager.get_color(lbl)
                err = (yerr.get(col) if isinstance(yerr, dict) else None)
                ax.bar(offs, cache_df[col], yerr=err, width=bar_w, label=lbl, color=color, alpha=alpha)

            ax.set_xticks(base)
            ax.set_xticklabels(x_vals)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key='bar',
            **kwargs
        )

    def add_multi_line(self, **kwargs) -> 'Plotter':
        """在子图上绘制多条折线。

        Args:
            data (pd.DataFrame): 数据表。
            x (str): 横轴列名。
            ys (List[str]): 多个系列列名。
            labels (Dict[str, str], optional): 系列到图例名映射。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            x_col = p_kwargs.pop('x')
            x_vals = cache_df[x_col]
            y_cols = p_kwargs.pop('ys')
            labels = p_kwargs.pop('labels', {})
            linewidth = p_kwargs.pop('linewidth', 2)

            for col in y_cols:
                lbl = labels[col] if isinstance(labels, dict) and col in labels else col
                color = self.color_manager.get_color(lbl)
                ax.plot(x_vals, cache_df[col], label=lbl, color=color, linewidth=linewidth)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key='line',
            **kwargs
        )

    def add_stacked_bar(self, **kwargs) -> 'Plotter':
        """在子图上绘制多系列堆叠柱状图。

        Args:
            data (pd.DataFrame): 数据表。
            x (str): 分类列名。
            ys (List[str]): 多个系列列名，按顺序堆叠。
            labels (Dict[str, str], optional): 系列到图例名映射。
            width (float, optional): 柱宽，默认 0.8。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            x_col = p_kwargs.pop('x')
            x_vals = cache_df[x_col]
            base = np.arange(len(x_vals))
            y_cols = p_kwargs.pop('ys')
            labels = p_kwargs.pop('labels', {})
            width = p_kwargs.pop('width', 0.8)
            alpha = p_kwargs.pop('alpha', 0.8)

            bottoms = np.zeros(len(x_vals))
            for col in y_cols:
                lbl = labels[col] if isinstance(labels, dict) and col in labels else col
                color = self.color_manager.get_color(lbl)
                ax.bar(base, cache_df[col], bottom=bottoms, width=width, label=lbl, color=color, alpha=alpha)
                bottoms = bottoms + np.array(cache_df[col])
            ax.set_xticks(base)
            ax.set_xticklabels(x_vals)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key='bar',
            **kwargs
        )

    def add_polar_bar(self, **kwargs) -> 'Plotter':
        """在极坐标轴上绘制柱状图。

        Args:
            data (pd.DataFrame): 数据表。
            theta (str): 角度列名，单位为弧度。
            r (str): 半径列名。
            width (float, optional): 柱宽，默认自动根据角度间距估算。
            bottom (float, optional): 起始半径，默认 0。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        data = kwargs.pop('data', None)
        theta_key = kwargs.pop('theta')
        r_key = kwargs.pop('r')
        width = kwargs.pop('width', None)
        bottom = kwargs.pop('bottom', 0.0)
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != 'polar':
            raise TypeError("Axis is not polar. Create with ax_configs={'tag': {'projection': 'polar'}}.")
        if isinstance(data, pd.DataFrame):
            theta = data[theta_key]
            r = data[r_key]
            if width is None:
                if len(theta) > 1:
                    d = np.diff(np.sort(theta))
                    w = np.median(d)
                else:
                    w = 0.1
            else:
                w = width
            _ax.bar(theta, r, width=w, bottom=bottom, **kwargs)
            cache_df = data[[theta_key, r_key]]
        else:
            raise TypeError("'data' must be a pandas DataFrame for polar bar.")
        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_pie(self, **kwargs) -> 'Plotter':
        """绘制饼图。

        Args:
            data (pd.DataFrame): 数据表。
            sizes (str): 数值列名。
            labels (Sequence[str], optional): 标签。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            sizes_col = data_names['sizes']
            labels = p_kwargs.pop('labels', None)
            ax.pie(cache_df[sizes_col], labels=labels if isinstance(labels, Sequence) else None, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['sizes'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_donut(self, **kwargs) -> 'Plotter':
        """绘制环形图。

        Args:
            data (pd.DataFrame): 数据表。
            sizes (str): 数值列名。
            labels (Sequence[str], optional): 标签。
            width (float, optional): 环的厚度，默认 0.4。
            radius (float, optional): 外半径，默认 1.0。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            sizes_col = data_names['sizes']
            labels = p_kwargs.pop('labels', None)
            width = p_kwargs.pop('width', 0.4)
            radius = p_kwargs.pop('radius', 1.0)
            ax.pie(cache_df[sizes_col], labels=labels if isinstance(labels, Sequence) else None, radius=radius, wedgeprops={"width": width}, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['sizes'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_nested_donut(self, **kwargs) -> 'Plotter':
        """绘制嵌套环形图。

        Args:
            outer (dict): 外圈配置，包含 `data`、`sizes`、可选 `labels`。
            inner (dict): 内圈配置，包含 `data`、`sizes`、可选 `labels`。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        kwargs.setdefault('data', pd.DataFrame())

        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            outer = p_kwargs.pop('outer')
            inner = p_kwargs.pop('inner')
            if not (isinstance(outer, dict) and isinstance(inner, dict)):
                raise TypeError("'outer' and 'inner' must be dicts with keys: data, sizes, labels.")
            od = outer['data']
            os_key = outer['sizes']
            ol = outer.get('labels')
            idf = inner['data']
            is_key = inner['sizes']
            il = inner.get('labels')
            ax.pie(od[os_key], labels=ol if isinstance(ol, Sequence) else None, radius=1.0, wedgeprops={"width": 0.4})
            ax.pie(idf[is_key], labels=il if isinstance(il, Sequence) else None, radius=0.6, wedgeprops={"width": 0.4})
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key=None,
            **kwargs
        )

    def add_waterfall(self, **kwargs) -> 'Plotter':
        """绘制阶梯瀑布图。

        Args:
            data (pd.DataFrame): 数据表。
            x (str): 阶段列名。
            deltas (str): 变化值列名。
            baseline (float, optional): 初始值，默认 0.0。
            colors (Tuple[str, str], optional): 正负颜色。
            connectors (bool, optional): 是否绘制连接线，默认 True。
            width (float, optional): 柱宽，默认 0.8。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            x_col = data_names['x']
            d_col = data_names['deltas']
            baseline = p_kwargs.pop('baseline', 0.0)
            colors = p_kwargs.pop('colors', ("#2ca02c", "#d62728"))
            connectors = p_kwargs.pop('connectors', True)
            width = p_kwargs.pop('width', 0.8)

            x_vals = cache_df[x_col]
            d = cache_df[d_col].to_numpy()
            cum = np.zeros_like(d, dtype=float)
            total = baseline
            bottoms, heights = [], []
            for i, delta in enumerate(d):
                bottoms.append(total)
                heights.append(delta)
                total += delta
                cum[i] = total
            base = np.arange(len(x_vals))
            pos_color, neg_color = colors
            bar_colors = [pos_color if h >= 0 else neg_color for h in heights]
            ax.bar(base, heights, bottom=bottoms, width=width, color=bar_colors)
            if connectors:
                for i in range(1, len(base)):
                    x0 = base[i-1] + width/2
                    x1 = base[i] - width/2
                    y0 = bottoms[i-1] + heights[i-1]
                    y1 = bottoms[i]
                    ax.plot([x0, x1], [y0, y1], color='gray', linewidth=1)
            ax.set_xticks(base)
            ax.set_xticklabels(x_vals)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'deltas'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_candlestick(self, **kwargs) -> 'Plotter':
        """绘制K线图。

        Args:
            data (pd.DataFrame): 数据表。
            time (str): 时间列名。
            open (str): 开盘列名。
            high (str): 最高列名。
            low (str): 最低列名。
            close (str): 收盘列名。
            width (float, optional): 蜡烛宽度，默认 0.6。
            up_color (str, optional): 上涨颜色，默认绿色。
            down_color (str, optional): 下跌颜色，默认红色。
            tag (Optional[Union[str, int]]): 子图标签。
            ax (Optional[plt.Axes]): 指定轴。

        Returns:
            Plotter: 返回实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            t_col = data_names['time']
            o_col = data_names['open']
            h_col = data_names['high']
            l_col = data_names['low']
            c_col = data_names['close']
            width = p_kwargs.pop('width', 0.6)
            up_color = p_kwargs.pop('up_color', '#2ca02c')
            down_color = p_kwargs.pop('down_color', '#d62728')

            x_vals = np.arange(len(cache_df))
            for i in range(len(cache_df)):
                o = float(cache_df.iloc[i][o_col])
                h = float(cache_df.iloc[i][h_col])
                l = float(cache_df.iloc[i][l_col])
                c = float(cache_df.iloc[i][c_col])
                color = up_color if c >= o else down_color
                ax.add_line(Line2D([x_vals[i], x_vals[i]], [l, h], color=color, linewidth=1))
                rect_y = min(o, c)
                rect_h = abs(c - o)
                if rect_h == 0:
                    rect_h = 0.001
                ax.add_patch(Rectangle((x_vals[i] - width/2, rect_y), width, rect_h, facecolor=color, edgecolor=color))
            ax.set_xticks(x_vals)
            ax.set_xticklabels(list(cache_df[t_col]))
            ax.relim()
            ax.autoscale_view()
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['time', 'open', 'high', 'low', 'close'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_scatter(self, **kwargs) -> 'Plotter':
        """在子图上绘制散点图 (封装 `matplotlib.axes.Axes.scatter`)。

        如果 `s` (size) 或 `c` (color) 的值是字符串，它们将被解释为
        `data` DataFrame 中的列名，从而实现按数据列控制点的大小或颜色。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名。
            y (str or array-like): y轴数据或 `data` 中的列名。
            s (str or array-like, optional): 点的大小或 `data` 中的列名。
            c (str or array-like, optional): 点的颜色或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.scatter` 的关键字参数，
                      例如 `cmap`, `alpha`, `marker`, `label` 等。

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
        """在子图上绘制直方图 (封装 `matplotlib.axes.Axes.hist`)。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): 用于绘制直方图的数据或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.hist` 的关键字参数，
                      例如 `bins`, `range`, `density`, `color` 等。

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
        """在子图上绘制箱线图 (封装 `seaborn.boxplot`)。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名，通常是分类变量。
            y (str or array-like): y轴数据或 `data` 中的列名，通常是数值变量。
            hue (str, optional): 用于产生不同颜色箱体的分类变量的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `seaborn.boxplot` 的关键字参数，
                      例如 `order`, `palette`, `linewidth` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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
        """在子图上绘制热图 (封装 `seaborn.heatmap`)。

        此方法会自动检测当前样式中的调色板，并用其创建一个匹配的
        连续色图(Colormap)，除非用户手动指定了 `cmap` 参数。
        新的版本会自动将调色板中的颜色按亮度排序，以创建一个
        视觉上更直观的颜色梯度。

        Args:
            data (pd.DataFrame): 用于绘制热图的二维矩形数据。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            cbar (bool, optional): 是否绘制颜色条。默认为 `True`。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数，
                      例如 `cmap`, `annot`, `fmt`, `linewidths` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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
        """在子图上使用任意指定的Seaborn函数进行绘图。

        这是一个灵活的接口，允许用户调用任何接受 `data` 和 `ax` 参数的
        Seaborn绘图函数。

        Args:
            plot_func (Callable): 要使用的Seaborn绘图函数，
                例如 `sns.violinplot`。
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like, optional): x轴数据或 `data` 中的列名。
            y (str or array-like, optional): y轴数据或 `data` 中的列名。
            hue (str, optional): 用于分组的色调变量或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `plot_func` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果没有提供 `plot_func` 参数。
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
        """在指定或下一个可用的子图位置创建一个空白区域并关闭坐标轴。

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
        """在子图上绘制散点图和线性回归模型拟合 (封装 `seaborn.regplot`)。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名。
            y (str or array-like): y轴数据或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            scatter_kws (dict, optional): 传递给底层散点图的关键字参数。
            line_kws (dict, optional): 传递给回归线的关键字参数。
            **kwargs: 其他传递给 `seaborn.regplot` 的关键字参数，
                      例如 `color`, `marker`, `order` (用于多项式回归) 等。

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
            plot_defaults_key=None, # regplot 有自己的样式逻辑
            **kwargs
        )

    def add_conditional_scatter(self, **kwargs) -> 'Plotter':
        """根据条件在散点图上突出显示特定的数据点。

        此方法绘制两组散点：一组是满足条件的点（高亮），另一组是不满足
        条件的点（普通）。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名。
            y (str or array-like): y轴数据或 `data` 中的列名。
            condition (str or bool Series): 布尔序列或 `data` 中包含布尔值的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            s_normal (float, optional): 普通点的大小。
            c_normal (str, optional): 普通点的颜色。
            alpha_normal (float, optional): 普通点的透明度。
            label_normal (str, optional): 普通点的图例标签。
            s_highlight (float, optional): 高亮的大小。
            c_highlight (str, optional): 高亮点的颜色。
            alpha_highlight (float, optional): 高亮点的透明度。
            label_highlight (str, optional): 高亮点的图例标签。
            **kwargs: 其他通用的 `scatter` 关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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

    def add_figure(self, image_path: str, fit_mode: str = 'fit', align: str = 'center', padding: float = 0.0, zoom: float = 0.0, **kwargs) -> 'Plotter':
        """
        将一个图像文件作为子图的全部内容进行绘制。

        此方法会加载指定的图像，并根据 fit_mode 将其显示在子图区域内。
        它会自动关闭该子图的坐标轴刻度和边框。

        Args:
            image_path (str): 要显示的图像文件的路径。
            fit_mode (str, optional): 图像的填充模式。默认为 'fit'。
                - 'stretch': 拉伸图像以完全填满子图的矩形区域，可能会改变图像的原始宽高比。
                - 'fit': 保持图像的原始宽高比，缩放图像以适应子图区域，可能会在某一边留下空白。
                - 'cover': 保持图像的原始宽高比，缩放图像以完全覆盖子图区域，可能会裁剪掉图像的一部分。
            align (str, optional): 当 `fit_mode` 为 'fit' 时，图片在空白区域的对齐方式。
                                   可选值：'center', 'top_left', 'top_right', 'bottom_left', 'bottom_right'。
                                   默认为 'center'。
            padding (float, optional): 图像与子图边界之间的内边距，范围从0到1。
                                       例如，0.05 表示 5% 的边距。默认为 0.0。
            zoom (float, optional): 从图像中心放大/裁剪的比例，范围从0到0.5（不含）。
                                    例如，0.1 表示从中心放大10%。默认为 0.0。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 matplotlib.axes.Axes.imshow 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(kwargs.pop('tag', None))

        # 定义绘图目标轴
        draw_ax = _ax

        # 如果有 padding，则创建内嵌轴
        if padding > 0:
            if not (0.0 <= padding < 0.5):
                raise ValueError(f"Padding must be between 0.0 and 0.5 (exclusive of 0.5), but got {padding}.")
            draw_ax = _ax.inset_axes([padding, padding, 1 - 2 * padding, 1 - 2 * padding])
            _ax.axis('off') # 关闭原始轴的刻度和边框，使其成为透明容器

        # 参数校验
        if fit_mode not in ['stretch', 'fit', 'cover']:
            raise ValueError(f"Invalid fit_mode '{fit_mode}'. Available modes are 'stretch', 'fit', 'cover'.")
        if align not in ['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']:
            raise ValueError(f"Invalid align '{align}'. Available aligns are 'center', 'top_left', 'top_right', 'bottom_left', 'bottom_right'.")
        if not (0.0 <= zoom < 0.5):
            raise ValueError(f"Zoom must be between 0.0 and 0.5 (exclusive of 0.5), but got {zoom}.")

        # 读取图像文件
        try:
            img = mpimg.imread(image_path)
        except FileNotFoundError:
            raise ValueError(f"Image file '{image_path}' not found.")

        # 总是关闭坐标轴
        draw_ax.axis('off')
        draw_ax.set_xticks([])
        draw_ax.set_yticks([])

        # 准备传递给 imshow 的参数
        imshow_kwargs = kwargs.copy()
        imshow_kwargs.setdefault('aspect', 'auto')

        # 绘制图像
        draw_ax.imshow(img, **imshow_kwargs)

        # 获取图像和子图的尺寸信息
        img_height, img_width = img.shape[0], img.shape[1]
        img_aspect = img_width / img_height
        
        # 强制重绘以获取准确的 bbox
        self.fig.canvas.draw()
        bbox = draw_ax.get_window_extent()
        subplot_aspect = bbox.width / bbox.height if bbox.height > 0 else 1

        # 必须是 auto 才能独立设置 xlim 和 ylim
        draw_ax.set_aspect('auto') 

        xlim, ylim = (0, img_width), (img_height, 0) # 默认全图显示

        if fit_mode == 'stretch':
            # 拉伸模式，只应用 zoom
            pass # xlim, ylim 保持默认，zoom 在后面统一处理

        else: # fit 和 cover 模式都需要计算比例和裁剪
            if fit_mode == 'fit':
                # fit 模式：保持图像比例，缩放以适应子图
                if img_aspect > subplot_aspect: # 图像比子图宽，需要添加垂直留白
                    view_w = img_width
                    view_h = view_w / subplot_aspect
                    pad_y = (view_h - img_height)
                    
                    # 根据 align 参数决定如何分配 pad_y
                    if align == 'center':
                        ylim = (img_height + pad_y / 2, -pad_y / 2)
                    elif align == 'top_left' or align == 'top_right':
                        ylim = (view_h, 0)
                    elif align == 'bottom_left' or align == 'bottom_right':
                        ylim = (img_height, img_height - view_h)
                    xlim = (0, view_w) # xlim 保持不变

                else: # 图像比子图高，需要添加水平留白
                    view_h = img_height
                    view_w = view_h * subplot_aspect
                    pad_x = (view_w - img_width)
                    
                    # 根据 align 参数决定如何分配 pad_x
                    if align == 'center':
                        xlim = (-pad_x / 2, view_w - pad_x / 2)
                    elif align == 'top_left' or align == 'bottom_left':
                        xlim = (0, view_w)
                    elif align == 'top_right' or align == 'bottom_right':
                        xlim = (img_width - view_w, img_width)
                    ylim = (view_h, 0) # ylim 保持不变
            
            elif fit_mode == 'cover':
                # cover 模式：保持图像比例，缩放以填满子图
                if img_aspect > subplot_aspect: # 图像比子图宽，需裁剪左右
                    view_h = img_height
                    view_w = view_h * subplot_aspect
                    crop_x = (img_width - view_w) / 2
                    xlim, ylim = (crop_x, img_width - crop_x), (img_height, 0)
                else: # 图像比子图高，需裁剪上下
                    view_w = img_width
                    view_h = view_w / subplot_aspect
                    crop_y = (img_height - view_h) / 2
                    xlim, ylim = (0, img_width), (img_height - crop_y, crop_y)

        # 应用 zoom (在所有计算之后)
        total_w = xlim[1] - xlim[0]
        total_h = ylim[0] - ylim[1] # ylim 是 (top, bottom)，所以是反的

        xlim = (xlim[0] + total_w * zoom, xlim[1] - total_w * zoom)
        ylim = (ylim[0] - total_h * zoom, ylim[1] + total_h * zoom)

        draw_ax.set_xlim(xlim)
        draw_ax.set_ylim(ylim)

        self.last_active_tag = resolved_tag
        return self

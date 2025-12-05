import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

class AdvancedPlotsMixin:
    def add_grouped_bar(self, orientation: str = 'vertical', **kwargs) -> 'Plotter':
        """在子图上绘制多系列分组柱状图。

        Args:
            orientation (str, optional): 'vertical' 或 'horizontal'。默认为 'vertical'。
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str): x轴数据（类别）。如果是字符串，则为 `data` 中的列名。
                - ys (List[str]): y轴数据列名列表，每个列对应一个分组。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - labels (Dict[str, str], optional): 列名到图例标签的映射字典。
                - width/height (float, optional): 整个分组的总宽度/高度 (0-1)。默认为 0.8。
                - yerr/xerr (Dict[str, Any], optional): 列名到误差数据的映射字典。
                - alpha (float, optional): 透明度。默认为 0.8。
                - ... 其他传递给 `ax.bar` 或 `ax.barh` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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
                
                if orientation == 'horizontal':
                    ax.barh(offs, cache_df[col], xerr=err, height=bar_w, label=lbl, color=color, alpha=alpha)
                else:
                    ax.bar(offs, cache_df[col], yerr=err, width=bar_w, label=lbl, color=color, alpha=alpha)

            if orientation == 'horizontal':
                ax.set_yticks(base)
                ax.set_yticklabels(x_vals)
            else:
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
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str): x轴数据。如果是字符串，则为 `data` 中的列名。
                - ys (List[str]): y轴数据列名列表，每个列对应一条线。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - labels (Dict[str, str], optional): 列名到图例标签的映射字典。
                - linewidth (float, optional): 线宽。默认为 2。
                - ... 其他传递给 `ax.plot` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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

    def add_stacked_bar(self, orientation: str = 'vertical', **kwargs) -> 'Plotter':
        """在子图上绘制多系列堆叠柱状图。

        Args:
            orientation (str, optional): 'vertical' 或 'horizontal'。默认为 'vertical'。
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str): x轴数据（类别）。如果是字符串，则为 `data` 中的列名。
                - ys (List[str]): y轴数据列名列表，每个列对应一个堆叠层。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - labels (Dict[str, str], optional): 列名到图例标签的映射字典。
                - width/height (float, optional): 柱状图宽度/高度。默认为 0.8。
                - alpha (float, optional): 透明度。默认为 0.8。
                - ... 其他传递给 `ax.bar` 或 `ax.barh` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            x_col = p_kwargs.pop('x')
            x_vals = cache_df[x_col]
            base = np.arange(len(x_vals))
            y_cols = p_kwargs.pop('ys')
            labels = p_kwargs.pop('labels', {})
            width = p_kwargs.pop('width', 0.8)
            alpha = p_kwargs.pop('alpha', 0.8)

            lefts = np.zeros(len(x_vals))
            for col in y_cols:
                lbl = labels[col] if isinstance(labels, dict) and col in labels else col
                color = self.color_manager.get_color(lbl)
                
                if orientation == 'horizontal':
                    ax.barh(base, cache_df[col], left=lefts, height=width, label=lbl, color=color, alpha=alpha)
                    lefts = lefts + np.array(cache_df[col])
                else:
                    ax.bar(base, cache_df[col], bottom=lefts, width=width, label=lbl, color=color, alpha=alpha)
                    lefts = lefts + np.array(cache_df[col])
            
            if orientation == 'horizontal':
                ax.set_yticks(base)
                ax.set_yticklabels(x_vals)
            else:
                ax.set_xticks(base)
                ax.set_xticklabels(x_vals)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key='bar',
            **kwargs
        )

    def add_waterfall(self, **kwargs) -> 'Plotter':
        """绘制阶梯瀑布图，常用于展示数值的累积变化。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str): x轴数据（类别）。如果是字符串，则为 `data` 中的列名。
                - deltas (str): 变化量数据列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - baseline (float, optional): 起始基准值。默认为 0.0。
                - colors (Tuple[str, str], optional): (正值颜色, 负值颜色)。默认为 ("#2ca02c", "#d62728")。
                - connectors (bool, optional): 是否绘制连接线。默认为 True。
                - width (float, optional): 柱状图宽度。默认为 0.8。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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
        """绘制K线图 (Candlestick Chart)。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - time (str): 时间轴数据列名。
                - open (str): 开盘价列名。
                - high (str): 最高价列名。
                - low (str): 最低价列名。
                - close (str): 收盘价列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - width (float, optional): 蜡烛宽度。默认为 0.6。
                - up_color (str, optional): 上涨颜色。默认为 '#2ca02c'。
                - down_color (str, optional): 下跌颜色。默认为 '#d62728'。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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

    def add_conditional_scatter(self, **kwargs) -> 'Plotter':
        """根据条件在散点图上突出显示特定的数据点。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str): x轴数据列名。
                - y (str): y轴数据列名。
                - condition (str): 布尔条件列名。True 为高亮，False 为普通。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                普通点样式 (后缀 _normal):
                - s_normal (float): 大小。
                - c_normal (str): 颜色。
                - alpha_normal (float): 透明度。
                - label_normal (str): 图例标签。
                
                高亮点样式 (后缀 _highlight):
                - s_highlight (float): 大小。
                - c_highlight (str): 颜色。
                - alpha_highlight (float): 透明度。
                - label_highlight (str): 图例标签。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            x_col = data_names['x']
            y_col = data_names['y']
            condition_col = data_names['condition']
            condition = cache_df[condition_col]

            base_defaults = self._get_plot_defaults('scatter')
            
            normal_kwargs = {
                's': p_kwargs.pop('s_normal', base_defaults.get('s', 20)),
                'c': p_kwargs.pop('c_normal', 'gray'),
                'alpha': p_kwargs.pop('alpha_normal', base_defaults.get('alpha', 0.5)),
                'label': p_kwargs.pop('label_normal', 'Other points')
            }
            highlight_kwargs = {
                's': p_kwargs.pop('s_highlight', 60),
                'c': p_kwargs.pop('c_highlight', 'red'),
                'alpha': p_kwargs.pop('alpha_highlight', 1.0),
                'label': p_kwargs.pop('label_highlight', 'Highlighted')
            }
            
            normal_kwargs.update(p_kwargs)
            highlight_kwargs.update(p_kwargs)

            ax.scatter(cache_df.loc[~condition, x_col], cache_df.loc[~condition, y_col], **normal_kwargs)
            mappable = ax.scatter(cache_df.loc[condition, x_col], cache_df.loc[condition, y_col], **highlight_kwargs)
            
            return mappable

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'condition'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_dumbbell(self, **kwargs) -> 'Plotter':
        """绘制哑铃图 (Dumbbell Plot) 或棒棒糖图 (Lollipop Plot)。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame): 数据源 DataFrame。
                - y (str): 类别轴数据列名 (Y轴)。
                - x1 (str): 第一个数值轴数据列名 (X轴)。
                - x2 (str, optional): 第二个数值轴数据列名 (X轴)。如果提供，则绘制哑铃图；否则绘制棒棒糖图。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - color (str, optional): 统一颜色。
                - color1 (str, optional): x1 点的颜色。
                - color2 (str, optional): x2 点的颜色。
                - line_color (str, optional): 连接线的颜色。默认为 'gray'。
                - s (float, optional): 点的大小。
                - ... 其他传递给 `ax.scatter` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            y_col = data_names['y']
            x1_col = data_names['x1']
            x2_col = data_names.get('x2') # Optional
            
            y_vals = cache_df[y_col]
            x1_vals = cache_df[x1_col]
            
            # Defaults
            s = p_kwargs.pop('s', 60)
            line_color = p_kwargs.pop('line_color', 'gray')
            alpha = p_kwargs.pop('alpha', 1.0)
            
            # Determine colors
            c1 = p_kwargs.pop('color1', p_kwargs.get('color', self.color_manager.get_color(x1_col)))
            
            if x2_col:
                # Dumbbell Plot
                x2_vals = cache_df[x2_col]
                c2 = p_kwargs.pop('color2', p_kwargs.get('color', self.color_manager.get_color(x2_col)))
                
                # Draw lines
                ax.hlines(y=y_vals, xmin=x1_vals, xmax=x2_vals, color=line_color, alpha=0.5)
                
                # Draw points
                ax.scatter(x1_vals, y_vals, color=c1, s=s, alpha=alpha, label=x1_col, zorder=3)
                ax.scatter(x2_vals, y_vals, color=c2, s=s, alpha=alpha, label=x2_col, zorder=3)
            else:
                # Lollipop Plot
                # Draw lines from 0 to x1
                ax.hlines(y=y_vals, xmin=0, xmax=x1_vals, color=line_color, alpha=0.5)
                
                # Draw points
                ax.scatter(x1_vals, y_vals, color=c1, s=s, alpha=alpha, label=x1_col, zorder=3)
            
            return None

        data_keys = ['y', 'x1']
        if 'x2' in kwargs:
            data_keys.append('x2')

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=data_keys,
            plot_defaults_key='scatter',
            **kwargs
        )


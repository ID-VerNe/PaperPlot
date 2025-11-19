import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

class AdvancedPlotsMixin:
    def add_grouped_bar(self, **kwargs) -> 'Plotter':
        """在子图上绘制多系列分组柱状图。"""
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
        """在子图上绘制多条折线。"""
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
        """在子图上绘制多系列堆叠柱状图。"""
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

    def add_waterfall(self, **kwargs) -> 'Plotter':
        """绘制阶梯瀑布图。"""
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
        """绘制K线图。"""
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
        """根据条件在散点图上突出显示特定的数据点。"""
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

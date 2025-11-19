from typing import Optional, Union, Sequence
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CircularPlotsMixin:
    def add_polar_bar(self, **kwargs) -> 'Plotter':
        """在极坐标轴上绘制柱状图。"""
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
        """绘制饼图。"""
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
        """绘制环形图。"""
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
        """绘制嵌套环形图。"""
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

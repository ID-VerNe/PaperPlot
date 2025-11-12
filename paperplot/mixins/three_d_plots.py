# paperplot/mixins/three_d_plots.py

from typing import Optional, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ThreeDPlotsMixin:
    """包含3D绘图方法的 Mixin 类。"""
    def add_scatter3d(self, **kwargs) -> 'Plotter':
        """在3D子图上绘制散点图。

        此方法是 `_execute_plot` 的一个包装器，用于处理3D散点图的通用逻辑。
        数据可以通过 `data` DataFrame 和列名或直接作为关键字参数传入。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名。
            y (str or array-like): y轴数据或 `data` 中的列名。
            z (str or array-like): z轴数据或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.scatter` 的关键字参数，
                      例如 `c`, `s`, `cmap`, `marker`, `alpha` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TypeError: 如果目标子图不是3D投影。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            if ax.name != '3d':
                raise TypeError(f"Plotting method add_scatter3d requires a 3D projection, but the axis is '{ax.name}'.")
            
            mappable = ax.scatter(data_map['x'], data_map['y'], data_map['z'], **p_kwargs)
            return mappable

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'z'],
            plot_defaults_key='scatter', # 沿用 scatter 的默认样式
            **kwargs
        )

    def add_surface(self, **kwargs) -> 'Plotter':
        """在3D子图上绘制表面图。

        此方法直接调用 `matplotlib.axes.Axes.plot_surface`。
        它需要二维数组作为输入。

        Args:
            X (np.ndarray): 一个二维数组，表示表面上的x坐标。
            Y (np.ndarray): 一个二维数组，表示表面上的y坐标。
            Z (np.ndarray): 一个二维数组，表示表面上的z坐标（高度）。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot_surface` 的关键字参数，
                      例如 `cmap`, `rstride`, `cstride`, `color`, `linewidth` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TypeError: 如果目标子图不是3D投影。
        """
        # 由于 X, Y, Z 是 2D 数组，不适合通过 _prepare_data 处理，我们直接在方法内部处理
        X = kwargs.pop('X')
        Y = kwargs.pop('Y')
        Z = kwargs.pop('Z')
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != '3d':
            raise TypeError(f"Plotting method add_surface requires a 3D projection, but the axis '{resolved_tag}' is '{_ax.name}'.")

        kwargs.setdefault('cmap', 'viridis')
        mappable = _ax.plot_surface(X, Y, Z, **kwargs)
        
        # 缓存 mappable
        self.tag_to_mappable[resolved_tag] = mappable
        self.last_active_tag = resolved_tag
        return self

    def add_wireframe(self, **kwargs) -> 'Plotter':
        """在3D子图上绘制线框图。

        此方法直接调用 `matplotlib.axes.Axes.plot_wireframe`。
        它需要二维数组作为输入。

        Args:
            X (np.ndarray): 一个二维数组，表示线框上的x坐标。
            Y (np.ndarray): 一个二维数组，表示线框上的y坐标。
            Z (np.ndarray): 一个二维数组，表示线框上的z坐标（高度）。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot_wireframe` 的关键字参数，
                      例如 `rstride`, `cstride`, `color`, `linewidth` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TypeError: 如果目标子图不是3D投影。
        """
        X = kwargs.pop('X')
        Y = kwargs.pop('Y')
        Z = kwargs.pop('Z')
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != '3d':
            raise TypeError(f"Plotting method add_wireframe requires a 3D projection, but the axis '{resolved_tag}' is '{_ax.name}'.")

        _ax.plot_wireframe(X, Y, Z, **kwargs)
        self.last_active_tag = resolved_tag
        return self

    def add_line3d(self, **kwargs) -> 'Plotter':
        """在3D子图上绘制3D线图。

        此方法是 `_execute_plot` 的一个包装器，用于处理3D线图的通用逻辑。
        数据可以通过 `data` DataFrame 和列名或直接作为关键字参数传入。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据或 `data` 中的列名。
            y (str or array-like): y轴数据或 `data` 中的列名。
            z (str or array-like): z轴数据或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数，
                      例如 `color`, `marker`, `linestyle`, `linewidth` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TypeError: 如果目标子图不是3D投影。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            if ax.name != '3d':
                raise TypeError(f"Plotting method add_line3d requires a 3D projection, but the axis is '{ax.name}'.")
            
            mappable = ax.plot(data_map['x'], data_map['y'], data_map['z'], **p_kwargs)
            # ax.plot 返回一个列表，我们返回第一个元素作为 mappable
            return mappable[0] if mappable else None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'z'],
            plot_defaults_key='line', # 沿用 line 的默认样式
            **kwargs
        )
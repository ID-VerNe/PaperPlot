# paperplot/mixins/three_d_plots.py

from typing import Optional, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ThreeDPlotsMixin:
    """
    包含3D绘图方法的 Mixin 类。
    """
    def add_scatter3d(self, data: pd.DataFrame, x: str, y: str, z: str,
                      tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在3D子图上绘制散点图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): X轴数据的列名。
            y (str): Y轴数据的列名。
            z (str): Z轴数据的列名。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `ax.scatter` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != '3d':
            raise TypeError(f"Plotting method add_scatter3d requires a 3D projection, but the axis '{resolved_tag}' is '{_ax.name}'.")
        
        _ax.scatter(data[x], data[y], data[z], **kwargs)
        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

    def add_surface(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
                    tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在3D子图上绘制表面图。

        Args:
            X (np.ndarray): 2D数组，代表X坐标网格。
            Y (np.ndarray): 2D数组，代表Y坐标网格。
            Z (np.ndarray): 2D数组，代表Z坐标（高度）。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `ax.plot_surface` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != '3d':
            raise TypeError(f"Plotting method add_surface requires a 3D projection, but the axis '{resolved_tag}' is '{_ax.name}'.")

        kwargs.setdefault('cmap', 'viridis')
        _ax.plot_surface(X, Y, Z, **kwargs)
        self.last_active_tag = resolved_tag
        return self

    def add_wireframe(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
                      tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在3D子图上绘制线框图。

        Args:
            X (np.ndarray): 2D数组，代表X坐标网格。
            Y (np.ndarray): 2D数组，代表Y坐标网格。
            Z (np.ndarray): 2D数组，代表Z坐标（高度）。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `ax.plot_wireframe` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != '3d':
            raise TypeError(f"Plotting method add_wireframe requires a 3D projection, but the axis '{resolved_tag}' is '{_ax.name}'.")

        _ax.plot_wireframe(X, Y, Z, **kwargs)
        self.last_active_tag = resolved_tag
        return self

    def add_line3d(self, data: pd.DataFrame, x: str, y: str, z: str,
                   tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在3D子图上绘制3D线图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): X轴数据的列名。
            y (str): Y轴数据的列名。
            z (str): Z轴数据的列名。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 其他传递给 `ax.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != '3d':
            raise TypeError(f"Plotting method add_line3d requires a 3D projection, but the axis '{resolved_tag}' is '{_ax.name}'.")
        
        _ax.plot(data[x], data[y], data[z], **kwargs)
        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

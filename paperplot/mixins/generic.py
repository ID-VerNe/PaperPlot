# paperplot/mixins/generic.py

from typing import Optional, Union, List, Callable
import pandas as pd
import matplotlib.pyplot as plt
from ..exceptions import DuplicateTagError

class GenericPlotsMixin:
    """
    包含通用绘图方法的 Mixin 类。
    这些方法是常见图表类型（如线图、散点图、柱状图等）的直接封装。
    """

    def add_line(self, data: pd.DataFrame, x: str, y: str, tag: Optional[Union[str, int]] = None,
                 ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """在子图上绘制线图。"""
        _ax = self._resolve_ax(tag, ax)
        _ax.plot(data[x], data[y], **kwargs)
        return self

    def add_bar(self, data: pd.DataFrame, x: str, y: str, y_err: Optional[str] = None,
                tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """在子图上绘制柱状图。"""
        _ax = self._resolve_ax(tag, ax)
        y_error_values = data[y_err] if y_err and y_err in data else None
        _ax.bar(data[x], data[y], yerr=y_error_values, **kwargs)
        return self

    def add_scatter(self, data: pd.DataFrame, x: str, y: str, tag: Optional[Union[str, int]] = None,
                    ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """在子图上绘制散点图。"""
        _ax = self._resolve_ax(tag, ax)

        resolved_kwargs = kwargs.copy()
        for param in ['s', 'c']:
            if param in resolved_kwargs and isinstance(resolved_kwargs[param], str):
                column_name = resolved_kwargs[param]
                if column_name in data.columns:
                    resolved_kwargs[param] = data[column_name]

        _ax.scatter(data[x], data[y], **resolved_kwargs)
        return self

    def add_hist(self, data: pd.DataFrame, x: str, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                 **kwargs) -> 'Plotter':
        """在子图上绘制直方图。"""
        _ax = self._resolve_ax(tag, ax)
        _ax.hist(data[x], **kwargs)
        return self

    def add_box(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                **kwargs) -> 'Plotter':
        """在子图上绘制箱线图。"""
        _ax = self._resolve_ax(tag, ax)
        import seaborn as sns
        sns.boxplot(data=data, ax=_ax, **kwargs)
        return self

    def add_heatmap(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                    **kwargs) -> 'Plotter':
        """在子图上绘制热图。"""
        _ax = self._resolve_ax(tag, ax)

        create_cbar = kwargs.pop('cbar', True)
        import seaborn as sns
        sns.heatmap(data, ax=_ax, cbar=create_cbar, **kwargs)

        # 确保 tag 被正确赋值以便后续使用
        resolved_tag = tag if tag is not None else [k for k, v in self.tag_to_ax.items() if v is _ax][-1]

        if resolved_tag and hasattr(_ax, 'collections') and _ax.collections:
            self.tag_to_mappable[resolved_tag] = _ax.collections[0]

        return self

    def add_seaborn(self, plot_func: Callable, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None,
                    **kwargs) -> 'Plotter':
        """在子图上绘制Seaborn图。"""
        _ax = self._resolve_ax(tag, ax)
        plot_func(ax=_ax, **kwargs)
        return self

    def add_blank(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """在下一个可用的子图位置创建一个空白区域。"""
        _ax = self._resolve_ax(tag)
        _ax.axis('off')
        return self

    def add_regplot(self, data: pd.DataFrame, x: str, y: str, tag: Optional[str] = None, ax: Optional[plt.Axes] = None,
                    **kwargs) -> 'Plotter':
        """绘制散点图和线性回归趋势线。"""
        _ax = self._resolve_ax(tag, ax)
        import seaborn as sns
        sns.regplot(data=data, x=x, y=y, ax=_ax, **kwargs)
        return self
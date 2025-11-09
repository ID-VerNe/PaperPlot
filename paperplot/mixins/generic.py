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
    def add_line(self, data: pd.DataFrame, x: str, y: str, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制线图。
        """
        if ax is None:
            ax, _ = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        ax.plot(data[x], data[y], **kwargs)
        return self

    def add_bar(self, data: pd.DataFrame, x: str, y: str, y_err: Optional[str] = None, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制柱状图。
        """
        if ax is None:
            ax, _ = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        y_error_values = data[y_err] if y_err and y_err in data else None
        ax.bar(data[x], data[y], yerr=y_error_values, **kwargs)
        return self
        
    def add_scatter(self, data: pd.DataFrame, x: str, y: str, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制散点图。
        """
        if ax is None:
            ax, _ = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        resolved_kwargs = kwargs.copy()
        for param in ['s', 'c']:
            if param in resolved_kwargs and isinstance(resolved_kwargs[param], str):
                column_name = resolved_kwargs[param]
                if column_name in data.columns:
                    resolved_kwargs[param] = data[column_name]

        ax.scatter(data[x], data[y], **resolved_kwargs)
        return self

    def add_hist(self, data: pd.DataFrame, x: str, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制直方图。
        """
        if ax is None:
            ax, _ = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        ax.hist(data[x], **kwargs)
        return self

    def add_box(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制箱线图。
        """
        if ax is None:
            ax, _ = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        import seaborn as sns
        sns.boxplot(data=data, ax=ax, **kwargs)
        return self

    def add_heatmap(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制热图。
        """
        if ax is None:
            ax, tag = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        create_cbar = kwargs.pop('cbar', True)
        
        import seaborn as sns
        sns.heatmap(data, ax=ax, cbar=create_cbar, **kwargs)
        
        if tag and hasattr(ax, 'collections') and ax.collections:
            self.tag_to_mappable[tag] = ax.collections[0]

        return self

    def add_seaborn(self, plot_func: Callable, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制Seaborn图。
        """
        if ax is None:
            ax, _ = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        plot_func(ax=ax, **kwargs)
        return self

    def add_blank(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        在下一个可用的子图位置创建一个空白区域。
        """
        ax, _ = self._get_next_ax_and_assign_tag(tag)
        ax.axis('off')
        return self

    def add_regplot(self, data: pd.DataFrame, x: str, y: str, tag: Optional[str] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制散点图和线性回归趋势线。
        """
        if ax is None:
            ax, _ = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        import seaborn as sns
        sns.regplot(data=data, x=x, y=y, ax=ax, **kwargs)
        return self

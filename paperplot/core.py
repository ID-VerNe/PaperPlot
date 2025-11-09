import logging
logger = logging.getLogger(__name__)
from typing import Optional, Union, List, Tuple, Callable, Dict
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from . import utils
from .exceptions import TagNotFoundError, DuplicateTagError, PlottingSpaceError


from .mixins.domain import DomainSpecificPlotsMixin
from .mixins.generic import GenericPlotsMixin
from .mixins.modifiers import ModifiersMixin


class Plotter(GenericPlotsMixin, ModifiersMixin, DomainSpecificPlotsMixin):
    def __init__(self, layout: Union[Tuple[int, int], List[List[str]]], 
                 style: str = 'publication', 
                 figsize: Optional[Tuple[float, float]] = None, 
                 subplot_aspect: Optional[Tuple[float, float]] = None,
                 ax_configs: Optional[Dict[Union[str, Tuple[int, int]], Dict]] = None,
                 **fig_kwargs):
        """
        初始化一个绘图管理器，创建画布和子图网格。

        Args:
            layout (Union[Tuple[int, int], List[List[str]]]):
                定义子图布局。
                - 如果是 `(n_rows, n_cols)` 元组，将创建一个简单的 `n_rows` 行 `n_cols` 列的网格。
                - 如果是 `List[List[str]]` (马赛克布局)，则允许创建复杂、跨行/跨列的布局。
            style (str, optional): 要应用的Matplotlib样式名称。默认为 'publication'。
            figsize (Optional[Tuple[float, float]], optional): 整个画布的尺寸 (宽度, 高度) 英寸。
                                                               与 `subplot_aspect` 互斥。
            subplot_aspect (Optional[Tuple[float, float]], optional): 
                单个子图单元的宽高比 (宽, 高)，例如 (16, 9)。
                如果提供此参数，`figsize` 将被自动计算以保证子图比例。
                与 `figsize` 互斥。
            ax_configs (Optional[Dict[Union[str, Tuple[int, int]], Dict]], optional):
                一个字典，键是子图的tag（对于马赛克布局）或`(row, col)`元组（对于简单网格），
                值是传递给 `fig.add_subplot` 的关键字参数字典（例如 `{'projection': 'polar'}`）。
                默认为None。
            **fig_kwargs: 其他传递给 `matplotlib.pyplot.figure` 的关键字参数。

        Raises:
            ValueError: 如果布局定义无效，或者 `figsize` 和 `subplot_aspect` 被同时指定。
        """
        if figsize is not None and subplot_aspect is not None:
            raise ValueError("Cannot specify both 'figsize' and 'subplot_aspect'. Choose one.")

        plt.style.use(utils.get_style_path(style))
        self.layout = layout
        self.ax_configs = ax_configs if ax_configs is not None else {}
        
        calculated_figsize = figsize
        processed_layout = layout # 用于计算 figsize

        # 如果用户提供了 subplot_aspect，则进入自动计算模式
        if subplot_aspect is not None:
            if isinstance(layout, tuple) and len(layout) == 2:
                n_rows, n_cols = layout
            else: # Mosaic layout, need to parse to get total rows/cols
                _, (n_rows, n_cols) = utils.parse_mosaic_layout(layout)
            
            aspect_w, aspect_h = subplot_aspect
            
            # 定义基本单元格和间距的物理尺寸（英寸）
            base_cell_width = 4.0  # 基准值
            base_cell_height = base_cell_width * (aspect_h / aspect_w)

            # 估算间距和边距
            col_spacing_in = 0.3
            row_spacing_in = 0.3
            figure_padding_in = 1.5

            # 计算总宽度和总高度
            total_width = (n_cols * base_cell_width) + ((n_cols - 1) * col_spacing_in) + figure_padding_in
            total_height = (n_rows * base_cell_height) + ((n_rows - 1) * row_spacing_in) + figure_padding_in
            
            calculated_figsize = (total_width, total_height)

        # 设置最终的 figsize
        if calculated_figsize is not None:
            fig_kwargs.setdefault('figsize', calculated_figsize)
        
        fig_kwargs.setdefault('layout', 'constrained')
        self.fig = plt.figure(**fig_kwargs)
        
        self.axes_dict: Dict[Union[str, int], plt.Axes] = {}
        self.axes: List[plt.Axes] = []

        if isinstance(layout, tuple) and len(layout) == 2:
            n_rows, n_cols = layout
            for r in range(n_rows):
                for c in range(n_cols):
                    tag = f'ax{r}{c}'
                    subplot_kwargs = self.ax_configs.get(tag, {}) # Use tag for simple grid configs
                    ax = self.fig.add_subplot(n_rows, n_cols, r * n_cols + c + 1, **subplot_kwargs)
                    self.axes_dict[tag] = ax
                    self.axes.append(ax)
        elif isinstance(layout, list) and all(isinstance(row, list) for row in layout):
            parsed_layout, (n_rows, n_cols) = utils.parse_mosaic_layout(layout)
            gs = self.fig.add_gridspec(n_rows, n_cols) # Pass fig_kwargs to gridspec for layout
            
            for tag, spec in parsed_layout.items():
                subplot_kwargs = self.ax_configs.get(tag, {}) # Use tag for mosaic configs
                ax = self.fig.add_subplot(gs[spec['row_start']:spec['row_start']+spec['row_span'], 
                                            spec['col_start']:spec['col_start']+spec['col_span']], 
                                            **subplot_kwargs)
                self.axes_dict[tag] = ax
                self.axes.append(ax)
        else:
            raise ValueError("Invalid layout format. Must be (rows, cols) tuple or list of lists for mosaic.")

        self.tag_to_ax: Dict[Union[str, int], plt.Axes] = {} # This will store user-assigned tags to actual axes
        self.tag_to_mappable: Dict[Union[str, int], plt.cm.ScalarMappable] = {}
        self.current_ax_index: int = 0
        self.next_default_tag: int = 1

    def _get_ax_by_tag(self, tag: Union[str, int]) -> plt.Axes:
        """
        通过tag获取对应的Axes对象。

        Args:
            tag (Union[str, int]): 子图的唯一标识符。

        Returns:
            matplotlib.axes.Axes: 对应的Axes对象。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        if tag not in self.tag_to_ax:
            raise TagNotFoundError(tag, list(self.tag_to_ax.keys()))
        return self.tag_to_ax[tag]

    def _get_next_ax_and_assign_tag(self, tag: Optional[Union[str, int]] = None) -> Tuple[plt.Axes, Union[str, int]]:
        """
        获取下一个可用的Axes对象，并为其分配一个tag。
        """
        claimed_axes = set(self.tag_to_ax.values())

        ax_to_use = None
        while self.current_ax_index < len(self.axes):
            potential_ax = self.axes[self.current_ax_index]
            if potential_ax not in claimed_axes:
                ax_to_use = potential_ax
                break
            self.current_ax_index += 1

        if ax_to_use is None:
            raise PlottingSpaceError(len(self.axes))

        current_tag = tag if tag is not None else self.next_default_tag
        if current_tag in self.tag_to_ax:
            raise DuplicateTagError(current_tag)
            
        if tag is None:
            self.next_default_tag += 1
            
        self.tag_to_ax[current_tag] = ax_to_use
        self.current_ax_index += 1
        return ax_to_use, current_tag

    def get_ax(self, tag: Union[str, int]) -> plt.Axes:
        """
        通过tag获取对应的Axes对象。
        """
        return self._get_ax_by_tag(tag)

    def get_ax_by_name(self, name: str) -> plt.Axes:
        """
        通过布局时定义的名字获取对应的Axes对象。
        """
        if not isinstance(self.axes_dict, dict) or name not in self.axes_dict:
            available_names = list(self.axes_dict.keys()) if isinstance(self.axes_dict, dict) else []
            raise ValueError(f"Name '{name}' not found in layout. Available names are: {available_names}")
        return self.axes_dict[name]

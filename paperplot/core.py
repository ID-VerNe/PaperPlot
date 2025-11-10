import logging

from matplotlib.gridspec import GridSpecFromSubplotSpec

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
                 layout_engine: Optional[str] = 'constrained',
                 **fig_kwargs):
        """
        初始化一个绘图管理器，创建画布和子图网格。

        Args:
            layout (Union[Tuple[int, int], List[List[str]]]):
                定义子图布局。
                - 如果是 `(n_rows, n_cols)` 元组，将创建一个简单的 `n_rows` 行 `n_cols` 列的网格。
                - 如果是 `List[List[str]]` (马赛克布局)，则允许创建复杂、跨行/跨列的布局。
                - 如果是 `Dict`，则允许创建复杂、嵌套的布局。
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
            layout_engine (Optional[str], optional): 布局引擎。默认为 'constrained'。
            **fig_kwargs: 其他传递给 `matplotlib.pyplot.figure` 的关键字参数。

        Raises:
            ValueError: 如果布局定义无效，或者 `figsize` 和 `subplot_aspect` 被同时指定。
        """
        super().__init__()

        if layout_engine:
            fig_kwargs.setdefault('layout', layout_engine)

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

        if isinstance(layout, dict):
            self._create_nested_layout(layout)
        elif isinstance(layout, tuple) and len(layout) == 2:
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

        # self.tag_to_ax: Dict[Union[str, int], plt.Axes] = {} # This will store user-assigned tags to actual axes
        self.tag_to_ax = self.axes_dict.copy()

        self.tag_to_mappable: Dict[Union[str, int], plt.cm.ScalarMappable] = {}
        self.current_ax_index: int = 0
        self.next_default_tag: int = 1

    def _create_nested_layout(self, layout_def: Dict):
        """
        [私有] 根据声明式定义，递归创建嵌套布局。
        """
        main_layout_list = layout_def['main']
        subgrids_def = layout_def.get('subgrids', {})

        # 1. 创建主网格
        parsed_main_layout, (n_rows, n_cols) = utils.parse_mosaic_layout(main_layout_list)
        main_gs = self.fig.add_gridspec(n_rows, n_cols)

        # 2. 遍历主网格中的所有命名区域
        for name, spec in parsed_main_layout.items():

            # 检查这个区域是否需要被进一步划分为子网格
            if name in subgrids_def:
                # --- 是一个容器，需要创建子网格 ---
                subgrid_info = subgrids_def[name]
                sub_layout_list = subgrid_info['layout']
                subgrid_kwargs = {k: v for k, v in subgrid_info.items() if k != 'layout'}

                # 创建 GridSpecFromSubplotSpec
                main_subplot_spec = main_gs[spec['row_start']:spec['row_start'] + spec['row_span'],
                                    spec['col_start']:spec['col_start'] + spec['col_span']]

                parsed_sub_layout, (sub_rows, sub_cols) = utils.parse_mosaic_layout(sub_layout_list)
                sub_gs = GridSpecFromSubplotSpec(sub_rows, sub_cols, subplot_spec=main_subplot_spec, **subgrid_kwargs)

                # 在子网格中创建最终的 Axes
                for sub_name, sub_spec in parsed_sub_layout.items():
                    # 生成层级名称，例如：'heatmap_container.nh2_map'
                    hierarchical_name = f"{name}.{sub_name}"

                    ax = self.fig.add_subplot(sub_gs[sub_spec['row_start']:sub_spec['row_start'] + sub_spec['row_span'],
                                              sub_spec['col_start']:sub_spec['col_start'] + sub_spec['col_span']])

                    self.axes_dict[hierarchical_name] = ax
                    self.axes.append(ax)

            else:
                ax = self.fig.add_subplot(main_gs[spec['row_start']:spec['row_start'] + spec['row_span'],
                                          spec['col_start']:spec['col_start'] + spec['col_span']])
                self.axes_dict[name] = ax
                self.axes.append(ax)

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
        此方法用于顺序绘图模式。
        """
        # 步骤 1: 检查索引是否已经超出了可用 Axes 的范围。
        if self.current_ax_index >= len(self.axes):
            raise PlottingSpaceError(len(self.axes))

        # 步骤 2: 根据当前索引直接获取下一个 Axes。
        # 我们不再检查它是否已被“认领”，因为我们就是要覆盖或赋予它新标签。
        ax_to_use = self.axes[self.current_ax_index]

        # 步骤 3: 处理并检查新标签是否重复。
        current_tag = tag if tag is not None else self.next_default_tag
        if current_tag in self.tag_to_ax:
            # 顺序绘图模式下，一个已经存在的标签意味着重复，这是不允许的。
            # 声明式模式会在 _resolve_ax 中被提前捕获，不会进入此方法。
            raise DuplicateTagError(current_tag)

        if tag is None:
            self.next_default_tag += 1

        # 步骤 4: 将新标签与选定的 Axes 关联起来。
        self.tag_to_ax[current_tag] = ax_to_use

        # 步骤 5: 将索引向前移动，为下一次调用做准备。
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

    def _resolve_ax(self, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
        """[私有] 智能解析并返回正确的 Axes 对象。"""
        _ax: plt.Axes
        if ax is not None:
            _ax = ax
            # 如果用户同时提供了 ax 和 tag，需要注册这个关联
            if tag is not None:
                # 检查是否存在冲突
                if tag in self.tag_to_ax and self.tag_to_ax[tag] is not _ax:
                    raise DuplicateTagError(tag)
                self.tag_to_ax[tag] = _ax
        elif tag is not None and tag in self.tag_to_ax:
            # tag 在布局时已定义，直接使用
            _ax = self.tag_to_ax[tag]
        else:
            # ax 未提供，tag 也是新的或 None，按顺序分配
            _ax, _ = self._get_next_ax_and_assign_tag(tag)
        return _ax
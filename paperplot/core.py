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


from .mixins.generic import GenericPlotsMixin
from .mixins.domain import DomainSpecificPlotsMixin
from .mixins.three_d_plots import ThreeDPlotsMixin
from .mixins.modifiers import ModifiersMixin
from .mixins.ml_plots import MachineLearningPlotsMixin
from .mixins.analysis_plots import DataAnalysisPlotsMixin
from .mixins.stats_plots import StatsPlotsMixin
from .mixins.stats_modifiers import StatsModifiersMixin
from .utils import ColorManager


class Plotter(GenericPlotsMixin, DomainSpecificPlotsMixin, ThreeDPlotsMixin, MachineLearningPlotsMixin, 
              DataAnalysisPlotsMixin, StatsPlotsMixin, StatsModifiersMixin, ModifiersMixin):
    def __init__(self, layout: Union[Tuple[int, int], List[List[str]]],
                 style: str = 'marin_kitagawa',
                 figsize: Optional[Tuple[float, float]] = None,
                 subplot_aspect: Optional[Tuple[float, float]] = None,
                 ax_configs: Optional[Dict[Union[str, Tuple[int, int]], Dict]] = None,
                 layout_engine: Optional[str] = 'constrained',
                 **fig_kwargs):
        """初始化一个绘图管理器，创建画布和子图网格。

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
        
        # 如果用户提供了 subplot_aspect，则自动计算 figsize
        if subplot_aspect is not None:
            if isinstance(layout, tuple) and len(layout) == 2:
                n_rows, n_cols = layout
            else: # Mosaic layout
                _, (n_rows, n_cols) = utils.parse_mosaic_layout(layout)
            
            aspect_w, aspect_h = subplot_aspect
            
            base_cell_width = 4.0
            base_cell_height = base_cell_width * (aspect_h / aspect_w)

            col_spacing_in = 0.3
            row_spacing_in = 0.3
            figure_padding_in = 1.5

            total_width = (n_cols * base_cell_width) + ((n_cols - 1) * col_spacing_in) + figure_padding_in
            total_height = (n_rows * base_cell_height) + ((n_rows - 1) * row_spacing_in) + figure_padding_in
            
            calculated_figsize = (total_width, total_height)

        if calculated_figsize is not None:
            fig_kwargs.setdefault('figsize', calculated_figsize)
        
        self.fig = plt.figure(**fig_kwargs)
        
        self.axes_dict: Dict[Union[str, int], plt.Axes] = {}
        self.axes: List[plt.Axes] = []

        # 根据布局类型创建布局
        if isinstance(layout, dict):
            self._create_nested_layout(layout, parent_spec=None, prefix='')
        elif isinstance(layout, tuple) and len(layout) == 2:
            n_rows, n_cols = layout
            for r in range(n_rows):
                for c in range(n_cols):
                    tag = f'ax{r}{c}'
                    subplot_kwargs = self.ax_configs.get(tag, {})
                    ax = self.fig.add_subplot(n_rows, n_cols, r * n_cols + c + 1, **subplot_kwargs)
                    self.axes_dict[tag] = ax
                    self.axes.append(ax)
        elif isinstance(layout, list) and all(isinstance(row, list) for row in layout):
            parsed_layout, (n_rows, n_cols) = utils.parse_mosaic_layout(layout)
            gs = self.fig.add_gridspec(n_rows, n_cols)
            
            for tag, spec in parsed_layout.items():
                subplot_kwargs = self.ax_configs.get(tag, {})
                ax = self.fig.add_subplot(gs[spec['row_start']:spec['row_start']+spec['row_span'], 
                                            spec['col_start']:spec['col_start']+spec['col_span']], 
                                            **subplot_kwargs)
                self.axes_dict[tag] = ax
                self.axes.append(ax)
        else:
            raise ValueError("Invalid layout format. Must be (rows, cols) tuple or list of lists for mosaic.")

        self.tag_to_ax = self.axes_dict.copy()
        self.tag_to_mappable: Dict[Union[str, int], plt.cm.ScalarMappable] = {}
        self.current_ax_index: int = 0
        self.next_default_tag: int = 1
        
        # 用于追踪最后一个被操作的子图
        self.last_active_tag: Optional[Union[str, int]] = None
        # 用于缓存每个子图使用的数据
        self.data_cache: Dict[Union[str, int], pd.DataFrame] = {}
        
        # 存储已创建的孪生轴
        self.twin_axes: Dict[Union[str, int], plt.Axes] = {}
        # 标记当前的活动目标是主轴还是孪生轴
        self.active_target: str = 'primary' # 默认是 'primary'

        self.plotted_axes: set[plt.Axes] = set()

        self.color_manager = ColorManager()


    def _get_plot_defaults(self, plot_type: str) -> dict:
        """[私有] 根据绘图类型获取默认的样式参数。

        此方法为不同的绘图类型提供了一组预定义的、一致的样式关键字参数。
        返回一个字典的副本，以防止在外部修改默认值。

        Args:
            plot_type (str): 绘图类型的标识符，例如 'scatter', 'line'。

        Returns:
            dict: 包含适用于该绘图类型的默认关键字参数的字典。
                  如果绘图类型未找到，则返回一个空字典。
        """
        defaults = {
            'scatter': {'s': 30, 'alpha': 0.7},
            'line': {'linewidth': 2},
            'hist': {'bins': 20, 'alpha': 0.75},
            'bar': {'alpha': 0.8},
            'bifurcation': {'s': 0.5, 'alpha': 0.1, 'marker': '.', 'rasterized': True, 'color': 'black'},
            'surface': {'cmap': 'viridis'},
        }
        return defaults.get(plot_type, {}).copy() # 返回副本以防外部修改

    def _create_nested_layout(self, layout_def: Dict, parent_spec=None, prefix=''):
        """[私有] 根据声明式定义，递归创建嵌套布局。

        此方法能够解析一个包含 'main' 布局和可选 'subgrids' 的字典，
        从而构建出复杂的、可以无限嵌套的子图网格。

        Args:
            layout_def (Dict):
                定义布局的字典。必须包含一个 'main' 键，其值为一个
                马赛克布局列表（`List[List[str]]`）。可以包含一个可选的
                'subgrids' 键，其值为一个字典，将 'main' 布局中的名称
                映射到更深层次的子布局定义。
            parent_spec (GridSpecFromSubplotSpec, optional):
                父级 GridSpec，用于将当前布局嵌入到更大的网格中。
                在递归调用时使用。默认为 None，表示顶级布局。
            prefix (str, optional):
                用于构建层级式子图名称的前缀。在递归调用时，会将父级
                名称添加为前缀。默认为空字符串。

        Raises:
            ValueError: 如果 `layout_def` 字典中缺少 'main' 键。
            TypeError: 如果为子网格指定了不支持的布局类型。
        """
        main_layout_list = layout_def.get('main')
        if main_layout_list is None:
            raise ValueError("Nested layout definition must include a 'main' key.")
            
        subgrids_def = layout_def.get('subgrids', {})

        parsed_main_layout, (n_rows, n_cols) = utils.parse_mosaic_layout(main_layout_list)
        
        if parent_spec:
            gs = GridSpecFromSubplotSpec(n_rows, n_cols, subplot_spec=parent_spec)
        else:
            gs = self.fig.add_gridspec(n_rows, n_cols)

        for name, spec in parsed_main_layout.items():
            hierarchical_name = f"{prefix}{name}"
            current_spec = gs[spec['row_start']:spec['row_start'] + spec['row_span'],
                              spec['col_start']:spec['col_start'] + spec['col_span']]

            if name in subgrids_def:
                subgrid_info = subgrids_def[name]
                sub_layout = subgrid_info['layout']
                
                # Pass any extra kwargs (like hspace) to the sub-grid creation
                subgrid_kwargs = {k: v for k, v in subgrid_info.items() if k != 'layout'}

                if isinstance(sub_layout, dict):
                    # Recursive call for deeper nesting
                    self._create_nested_layout(sub_layout, parent_spec=current_spec, prefix=f"{hierarchical_name}.")
                elif isinstance(sub_layout, tuple) and len(sub_layout) == 2:
                    # Sub-layout is a simple grid
                    sub_rows, sub_cols = sub_layout
                    sub_gs = GridSpecFromSubplotSpec(sub_rows, sub_cols, subplot_spec=current_spec, **subgrid_kwargs)
                    for r in range(sub_rows):
                        for c in range(sub_cols):
                            sub_hierarchical_name = f"{hierarchical_name}.ax{r}{c}"
                            ax = self.fig.add_subplot(sub_gs[r, c])
                            self.axes_dict[sub_hierarchical_name] = ax
                            self.axes.append(ax)
                elif isinstance(sub_layout, list):
                    # Sub-layout is a mosaic
                    parsed_sub_layout, (sub_rows, sub_cols) = utils.parse_mosaic_layout(sub_layout)
                    sub_gs = GridSpecFromSubplotSpec(sub_rows, sub_cols, subplot_spec=current_spec, **subgrid_kwargs)
                    for sub_name, sub_spec_item in parsed_sub_layout.items():
                        sub_hierarchical_name = f"{hierarchical_name}.{sub_name}"
                        ax = self.fig.add_subplot(sub_gs[sub_spec_item['row_start']:sub_spec_item['row_start'] + sub_spec_item['row_span'],
                                                  sub_spec_item['col_start']:sub_spec_item['col_start'] + sub_spec_item['col_span']])
                        self.axes_dict[sub_hierarchical_name] = ax
                        self.axes.append(ax)
                else:
                    raise TypeError(f"Unsupported subgrid layout type for '{hierarchical_name}': {type(sub_layout)}. "
                                    "Must be a (rows, cols) tuple, a list of lists (mosaic), or a dict (nested layout).")
            else:
                ax = self.fig.add_subplot(current_spec)
                self.axes_dict[hierarchical_name] = ax
                self.axes.append(ax)

    def _get_ax_by_tag(self, tag: Union[str, int]) -> plt.Axes:
        """通过tag获取对应的Axes对象。

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

    def _get_active_ax(self, tag: Optional[Union[str, int]] = None) -> plt.Axes:
        """根据提供的tag或最后一个活动的tag获取当前的Axes对象。

        这使得修饰器方法可以在绘图方法之后被调用，而无需显式传递`tag`。

        Args:
            tag (Optional[Union[str, int]], optional): 子图的tag。
                如果为None，则使用最后一个被激活的子图。默认为None。

        Returns:
            plt.Axes: Matplotlib的Axes对象。

        Raises:
            ValueError: 如果之前没有任何绘图操作，且未指定tag。
        """
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("操作失败。之前没有任何绘图操作，且未指定'tag'。")
        
        # 新增: 检查是否处于孪生轴上下文
        if self.active_target == 'twin':
            if active_tag in self.twin_axes:
                return self.twin_axes[active_tag]
            else:
                # 如果用户尝试在没有孪生轴的图上操作，给出清晰的错误提示
                raise ValueError(f"No twin axis found for tag '{active_tag}'. Did you call add_twinx() first?")
        
        # 如果 active_target 不是 'twin'，则执行原有逻辑
        return self._get_ax_by_tag(active_tag)

    def _resolve_ax_and_tag(self, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None) -> Tuple[plt.Axes, Union[str, int]]:
        """[私有] 智能解析并返回正确的Axes对象及其最终的tag。

        这是将绘图操作与子图(Axes)关联的核心逻辑。
        解析优先级如下:
        1. 如果提供了`ax`对象，则直接使用它。
        2. 如果提供了`tag`且该tag已存在，则使用对应的Axes。
        3. 如果`tag`是新的或为`None`，则按顺序获取下一个可用的Axes并分配tag。

        Args:
            tag (Optional[Union[str, int]], optional): 期望用于绘图的tag。
                如果为None，将分配一个默认的数字tag。默认为None。
            ax (Optional[plt.Axes], optional): 一个特定的Axes对象。
                如果提供，它将覆盖任何基于tag的解析。默认为None。

        Returns:
            Tuple[plt.Axes, Union[str, int]]: 一个元组，包含解析后的Axes对象和分配给它的最终tag。

        Raises:
            PlottingSpaceError: 如果所有子图都已被使用。
            DuplicateTagError: 如果提供的新`tag`已存在但未在优先级2中被解析
                               (例如，在顺序模式下)。
        """
        # 检查是否处于孪生轴上下文
        if self.active_target == 'twin':
            # 在孪生轴模式下，绘图总是发生在“最后一个活动主轴”对应的孪生轴上
            active_primary_tag = self.last_active_tag
            if active_primary_tag is None:
                raise ValueError("Twin mode is active, but no primary plot context is set. Please plot on a primary axis first.")
            
            if active_primary_tag not in self.twin_axes:
                raise ValueError(f"Twin mode is active for tag '{active_primary_tag}', but no twin axis exists. Did you call add_twinx()?")

            # 获取孪生轴对象
            _ax = self.twin_axes[active_primary_tag]
            
            # 决定此图的 tag：优先使用用户传入的 tag，否则复用主轴的 tag
            resolved_tag = tag if tag is not None else active_primary_tag

            # 如果用户提供了新的 tag，必须检查它是否已存在，并进行注册
            if tag is not None:
                if tag in self.tag_to_ax and self.tag_to_ax[tag] is not _ax:
                    # 如果 tag 已存在且指向的不是当前这个孪生轴，则为重复
                    raise DuplicateTagError(tag)
                
                # 将新 tag 与这个孪生轴关联起来
                self.tag_to_ax[tag] = _ax
            
            # 将这个孪生轴标记为已绘图（如果需要）
            self.plotted_axes.add(_ax)
            
            return _ax, resolved_tag

        _ax: plt.Axes
        resolved_tag: Union[str, int]

        # 模式1: 显式提供了ax对象 (最高优先级)
        if ax is not None:
            _ax = ax
            if tag is not None:
                if tag in self.tag_to_ax and self.tag_to_ax[tag] is not _ax:
                    raise DuplicateTagError(tag)
                self.tag_to_ax[tag] = _ax
                resolved_tag = tag
            else:
                existing_tags = [t for t, a in self.tag_to_ax.items() if a is _ax]
                if existing_tags:
                    resolved_tag = existing_tags[0]
                else:
                    resolved_tag = self.next_default_tag
                    self.tag_to_ax[resolved_tag] = _ax
                    self.next_default_tag += 1

        # 模式2: 提供了已存在的tag (无论是来自布局还是动态创建)
        elif tag is not None and tag in self.tag_to_ax:
            _ax = self.tag_to_ax[tag]
            resolved_tag = tag
            # 移除对已存在 tag 的子图占用检查，允许叠加绘图。

        # 模式3: 隐式叠加 (未提供tag或ax，但在同一个子图上继续绘图)
        elif tag is None and self.last_active_tag is not None:
            # 用户没有提供新tag，且我们知道上一个活动的子图是哪个
            # 这意味着用户想在同一个子图上叠加绘制
            resolved_tag = self.last_active_tag
            _ax = self._get_ax_by_tag(resolved_tag)

        # 模式4: 顺序模式 (寻找下一个未被占用的ax)
        else:
            # 遍历所有子图，找到第一个未被绘图指令占用的
            next_ax = None
            for axis in self.axes:
                if axis not in self.plotted_axes:
                    next_ax = axis
                    break

            if next_ax is None:
                raise PlottingSpaceError(len(self.axes))

            _ax = next_ax

            resolved_tag = tag if tag is not None else self.next_default_tag
            if resolved_tag in self.tag_to_ax:
                raise DuplicateTagError(resolved_tag)

            if tag is None:
                self.next_default_tag += 1

            self.tag_to_ax[resolved_tag] = _ax

        # 无论通过何种方式，一旦一个ax被用于绘图，就将其加入占用集合
        self.plotted_axes.add(_ax)

        return _ax, resolved_tag

    def _prepare_data(self, data: Optional[pd.DataFrame] = None, **kwargs: dict) -> Tuple[dict, pd.DataFrame]:
        """[私有] 准备绘图数据，将多种输入格式统一为可用的数据系列和用于缓存的DataFrame。

        支持两种主要模式:
        1. `data` 是一个DataFrame, `kwargs` 的值是列名 (str)。
           例如: `_prepare_data(data=df, x='time', y='value')`
        2. `data` 是None, `kwargs` 的值是数据本身 (array-like)。
           例如: `_prepare_data(data=None, x=[1,2,3], y=[4,5,6])`

        Args:
            data (Optional[pd.DataFrame]): 包含数据的DataFrame，或None。
            **kwargs: 关键字参数，表示绘图所需的数据维度 (例如 x, y, hue)。

        Returns:
            Tuple[dict, pd.DataFrame]:
                - 一个字典，键是kwargs的键，值是Pandas Series格式的数据。
                - 一个DataFrame，用于在`self.data_cache`中缓存。
        """
        from .utils import _data_to_dataframe

        if isinstance(data, pd.DataFrame):
            # 模式1: data是DataFrame, kwargs的值应该是列名
            if not all(isinstance(v, str) for v in kwargs.values()):
                raise ValueError(
                    "If 'data' is a DataFrame, all other data arguments (e.g., 'x', 'y') must be strings representing column names."
                )
            
            # 提取数据系列
            data_series = {key: data[val] for key, val in kwargs.items()}
            
            # 创建一个仅包含所需列的DataFrame用于缓存
            used_columns = list(kwargs.values())
            
            if used_columns:
                cache_df = data[used_columns]
            else:
                # 如果没有指定数据列（例如 add_heatmap），则缓存整个 DataFrame
                cache_df = data
            
            return data_series, cache_df
            
        elif data is None:
            # 模式2: data是None, kwargs的值是数据本身
            df = _data_to_dataframe(**kwargs)
            data_series = {key: df[key] for key in kwargs}
            cache_df = df
            return data_series, cache_df
            
        else:
            raise TypeError(f"The 'data' argument must be a pandas DataFrame or None, but got {type(data)}.")

    def _execute_plot(self, plot_func: Callable, data_keys: List[str], 
                        plot_defaults_key: Optional[str], **kwargs):
        """[私有] 封装和执行标准绘图工作流的核心方法。

        该方法负责处理所有绘图方法共有的重复逻辑，包括：
        1. 解析目标子图 (`_resolve_ax_and_tag`)。
        2. 从用户参数中分离出数据列名/数据系列。
        3. 准备数据 (`_prepare_data`)，统一为 `data_map` 和 `cache_df`。
        4. 合并默认样式和用户自定义样式。
        5. 调用具体的绘图逻辑 (`plot_func`)。
        6. 缓存 Mappable 对象和数据。
        7. 更新活动状态。

        Args:
            plot_func (Callable): 具体的绘图函数。签名必须为
                                  `plot_func(ax, data_map, cache_df, data_names, **p_kwargs)`，
                                  并返回一个 `mappable` 对象或 `None`。
            data_keys (List[str]): 需要从用户参数中提取并准备的数据键列表 (例如 ['x', 'y', 'hue'])。
            plot_defaults_key (Optional[str]): 用于获取默认样式的键 (例如 'line', 'scatter')。
            **kwargs: 转发自调用方法的全部关键字参数，包括 `data`, `tag`, `ax` 和绘图样式。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 从 kwargs 中提取核心参数
        data = kwargs.pop('data', None)
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        # 步骤 1: 解析子图
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

        # 步骤 2: 分离数据准备参数
        data_prep_kwargs = {}
        for key in data_keys:
            if key in kwargs:
                data_prep_kwargs[key] = kwargs.pop(key)
        
        # 步骤 3: 准备数据
        data_map, cache_df = self._prepare_data(data=data, **data_prep_kwargs)

        # 步骤 4: 合并样式
        final_kwargs = kwargs
        if plot_defaults_key:
            defaults = self._get_plot_defaults(plot_defaults_key)
            final_kwargs = {**defaults, **kwargs}
            
        # 检查用户是否提供了系列标签 (label)，并且没有手动指定颜色
        series_label = final_kwargs.get('label')
        if series_label and 'color' not in final_kwargs:
            assigned_color = self.color_manager.get_color(series_label)
            final_kwargs['color'] = assigned_color
        # 优先级 2: (隐式) 如果不满足上述条件，则不向 final_kwargs 添加 'color'。
        #            这会将颜色选择的决策权交还给 Matplotlib 的 Axes 对象本身。
        #            - 对于普通轴，它会使用自己的标准颜色循环。
        #            - 对于 twinx 轴，它会使用我们已在 add_twinx 中配置好的、偏移过的颜色循环。

        # 步骤 5: 执行绘图
        mappable = plot_func(_ax, data_map, cache_df, data_prep_kwargs, **final_kwargs)

        # 步骤 6: 缓存 Mappable
        if mappable is not None:
            self.tag_to_mappable[resolved_tag] = mappable

        # 步骤 7: 缓存数据
        if cache_df is not None and not cache_df.empty:
            self.data_cache[resolved_tag] = cache_df

        # 步骤 8: 更新状态
        self.last_active_tag = resolved_tag

        # 步骤 9: 返回实例
        return self

    def get_ax(self, tag: Union[str, int]) -> plt.Axes:
        """通过提供的标签（tag）获取对应的Matplotlib Axes对象。

        这是 `_get_ax_by_tag` 方法的一个公共接口。

        Args:
            tag (Union[str, int]): 要获取的子图的唯一标识符。

        Returns:
            plt.Axes: 与标签对应的Matplotlib Axes对象。

        Raises:
            TagNotFoundError: 如果在绘图仪中找不到指定的标签。
        """
        return self._get_ax_by_tag(tag)

    def get_ax_by_name(self, name: str) -> plt.Axes:
        """通过在布局时定义的名称获取对应的Matplotlib Axes对象。

        这对于在马赛克布局或嵌套布局中按名称引用子图特别有用。

        Args:
            name (str): 在布局定义中为子图指定的名称。

        Returns:
            plt.Axes: 与名称对应的Matplotlib Axes对象。

        Raises:
            ValueError: 如果布局中不存在指定的名称。
        """
        if not isinstance(self.axes_dict, dict) or name not in self.axes_dict:
            available_names = list(self.axes_dict.keys()) if isinstance(self.axes_dict, dict) else []
            raise ValueError(f"Name '{name}' not found in layout. Available names are: {available_names}")
        return self.axes_dict[name]

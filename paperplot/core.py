import logging
logger = logging.getLogger(__name__)
from typing import Optional, Union, List, Tuple, Callable
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from . import utils
from .exceptions import TagNotFoundError, DuplicateTagError, PlottingSpaceError


class Plotter:
    def __init__(self, layout: Union[Tuple[int, int], List[List[str]]], 
                 style: str = 'publication', 
                 figsize: Optional[Tuple[float, float]] = None, 
                 subplot_aspect: Optional[Tuple[float, float]] = None, 
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
            **fig_kwargs: 其他传递给 `matplotlib.pyplot.subplot_mosaic` 的关键字参数。

        Raises:
            ValueError: 如果布局定义无效，或者 `figsize` 和 `subplot_aspect` 被同时指定。
        """
        if figsize is not None and subplot_aspect is not None:
            raise ValueError("Cannot specify both 'figsize' and 'subplot_aspect'. Choose one.")

        plt.style.use(utils.get_style_path(style))
        self.layout = layout
        
        # 统一处理布局为 mosaic 形式
        processed_layout = layout
        if isinstance(layout, tuple) and len(layout) == 2:
            n_rows, n_cols = layout
            processed_layout = [[f'ax{r}{c}' for c in range(n_cols)] for r in range(n_rows)]

        calculated_figsize = figsize
        # 如果用户提供了 subplot_aspect，则进入自动计算模式
        if subplot_aspect is not None:
            _, (n_rows, n_cols) = utils.parse_mosaic_layout(processed_layout)
            
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

        self.fig, self.axes_dict = plt.subplot_mosaic(processed_layout, **fig_kwargs)
        
        if isinstance(self.axes_dict, dict):
            self.axes = [self.axes_dict[key] for key in sorted(self.axes_dict.keys())]
        else:
            self.axes = np.atleast_1d(self.axes_dict).flatten()

        self.tag_to_ax: dict[Union[str, int], plt.Axes] = {}
        self.tag_to_mappable: dict[Union[str, int], plt.cm.ScalarMappable] = {}
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

    def _get_next_ax_and_assign_tag(self, tag: Optional[Union[str, int]] = None) -> plt.Axes:
        """
        获取下一个可用的Axes对象，并为其分配一个tag。

        如果tag未指定，则自动生成一个数字tag。
        此方法会智能跳过已被其他绘图操作（通过`ax=`参数）占用的Axes。

        Args:
            tag (Optional[Union[str, int]], optional): 要分配给Axes的唯一标识符。
                                                       如果为None，将自动生成。默认为None。

        Returns:
            matplotlib.axes.Axes: 下一个可用的Axes对象。

        Raises:
            PlottingSpaceError: 如果没有更多可用的子图空间。
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
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
        return ax_to_use

    # --- 添加绘图的方法 (Verbs) ---
    def add_line(self, data: pd.DataFrame, x: str, y: str, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制线图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名。
            y (str): 数据框中用于Y轴的列名。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        ax.plot(data[x], data[y], **kwargs)
        return self

    def add_bar(self, data: pd.DataFrame, x: str, y: str, y_err: Optional[str] = None, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制柱状图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名。
            y (str): 数据框中用于Y轴的列名。
            y_err (Optional[str], optional): 数据框中用于Y轴误差棒的列名。默认为None。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.bar` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
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

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名。
            y (str): 数据框中用于Y轴的列名。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.scatter` 的关键字参数。
                      支持将 's' (大小) 和 'c' (颜色) 参数指定为DataFrame的列名。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
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

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.hist` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        ax.hist(data[x], **kwargs)
        return self

    def add_box(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制箱线图。

        这是一个 `seaborn.boxplot` 的封装。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `seaborn.boxplot` 的关键字参数 (例如 x, y, hue)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
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

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。
                      默认情况下会创建颜色条（`cbar=True`），但可以通过 `cbar=False` 禁用。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        create_cbar = kwargs.pop('cbar', True)
        
        import seaborn as sns
        sns.heatmap(data, ax=ax, cbar=create_cbar, **kwargs)
        
        if tag and ax.collections:
            self.tag_to_mappable[tag] = ax.collections[0]

        return self

    def add_seaborn(self, plot_func: Callable, tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在子图上绘制Seaborn图。

        此方法允许用户直接传入一个Seaborn绘图函数，并在Plotter管理的Axes上执行。

        Args:
            plot_func (Callable): 要调用的Seaborn绘图函数（例如 `sns.scatterplot`, `sns.lineplot`）。
                                  该函数必须接受 `ax` 参数。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `plot_func` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        plot_func(ax=ax, **kwargs)
        return self

    def add_blank(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        在下一个可用的子图位置创建一个空白区域。

        此方法会消耗掉一个子图位置，但不会在上面绘制任何内容，
        而是直接将其坐标轴和背景设为不可见。

        Args:
            tag (Optional[Union[str, int]], optional): 空白区域的唯一标识符。
                                                       如果提供，后续可以引用此区域。
                                                       默认为None。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_next_ax_and_assign_tag(tag)
        ax.axis('off')
        return self

    def add_spectra(self, data: pd.DataFrame, x: str, y_cols: List[str], 
                    tag: Optional[Union[str, int]] = None, 
                    ax: Optional[plt.Axes] = None, 
                    offset: float = 0, **kwargs) -> 'Plotter':
        """
        在同一个子图上绘制多条带垂直偏移的光谱。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名（如 'wavenumber'）。
            y_cols (List[str]): 一个包含多个Y轴列名的列表，每一列代表一条光谱。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            offset (float, optional): 连续光谱之间的垂直偏移量。默认为 0。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax

        for i, y_col in enumerate(y_cols):
            label = kwargs.pop('label', y_col) # 如果用户没有提供label，则使用列名
            ax.plot(data[x], data[y_col] + i * offset, label=label, **kwargs)
        
        return self

    def add_concentration_map(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, 
                              ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制 SERS Mapping 图像，本质上是一个带有专业颜色映射和坐标轴的热图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。通常是二维数据，索引和列代表空间坐标。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。
                      默认情况下会创建颜色条（`cbar=True`），但可以通过 `cbar=False` 禁用。
                      默认 `cmap` 为 'inferno'。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        create_cbar = kwargs.pop('cbar', True)
        kwargs.setdefault('cmap', 'inferno') # 默认使用 inferno 颜色映射
        
        import seaborn as sns
        sns.heatmap(data, ax=ax, cbar=create_cbar, **kwargs)
        
        if tag and ax.collections:
            self.tag_to_mappable[tag] = ax.collections[0]

        ax.set_xlabel(kwargs.pop('xlabel', 'X (μm)'))
        ax.set_ylabel(kwargs.pop('ylabel', 'Y (μm)'))

        return self

    def add_confusion_matrix(self, matrix: Union[np.ndarray, pd.DataFrame], 
                             class_names: List[str], 
                             tag: Optional[Union[str, int]] = None, 
                             ax: Optional[plt.Axes] = None, 
                             normalize: bool = False, **kwargs) -> 'Plotter':
        """
        可视化分类模型的混淆矩阵。

        Args:
            matrix (Union[np.ndarray, pd.DataFrame]): 混淆矩阵。
            class_names (List[str]): 类别的名称列表。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            normalize (bool, optional): 如果为True，则将矩阵值归一化为百分比。默认为False。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax

        if normalize:
            matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
            fmt = '.2f'
        else:
            fmt = 'd'
        
        df_cm = pd.DataFrame(matrix, index=class_names, columns=class_names)

        import seaborn as sns
        kwargs.setdefault('annot', True)
        kwargs.setdefault('fmt', fmt)
        kwargs.setdefault('cmap', 'Blues')
        
        sns.heatmap(df_cm, ax=ax, **kwargs)

        ax.set_xlabel('Predicted Label')
        ax.set_ylabel('True Label')
        
        return self

    def add_roc_curve(self, fpr: dict, tpr: dict, roc_auc: dict, 
                      tag: Optional[Union[str, int]] = None, 
                      ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制多分类或单分类的ROC曲线。

        Args:
            fpr (dict): 一个字典，键是类别名，值是假正率 (False Positive Rate) 数组。
            tpr (dict): 一个字典，键是类别名，值是真正率 (True Positive Rate) 数组。
            roc_auc (dict): 一个字典，键是类别名，值是AUC分数。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax

        # 绘制每个类别的ROC曲线
        for key in fpr.keys():
            label = f'{key} (AUC = {roc_auc[key]:.2f})'
            ax.plot(fpr[key], tpr[key], label=label, **kwargs)

        # 绘制对角参考线
        ax.plot([0, 1], [0, 1], 'k--', lw=2)
        
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('Receiver Operating Characteristic (ROC) Curve')
        ax.legend(loc="lower right")
        
        return self

    def add_pca_scatter(self, data: pd.DataFrame, x_pc: str, y_pc: str, 
                        tag: Optional[Union[str, int]] = None, 
                        ax: Optional[plt.Axes] = None, 
                        hue: Optional[str] = None, **kwargs) -> 'Plotter':
        """
        绘制PCA降维结果的散点图，并可根据类别进行着色。

        Args:
            data (pd.DataFrame): 包含PCA结果的数据框。
            x_pc (str): 代表X轴主成分的列名 (例如 'PC1')。
            y_pc (str): 代表Y轴主成分的列名 (例如 'PC2')。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            hue (Optional[str], optional): 用于对散点进行分组和着色的列名。
            **kwargs: 其他传递给 `seaborn.scatterplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        import seaborn as sns
        sns.scatterplot(data=data, x=x_pc, y=y_pc, hue=hue, ax=ax, **kwargs)
        
        return self

    def add_power_timeseries(self, data: pd.DataFrame, x: str, y_cols: List[str], 
                             tag: Optional[Union[str, int]] = None, 
                             ax: Optional[plt.Axes] = None, 
                             events: Optional[dict] = None, **kwargs) -> 'Plotter':
        """
        绘制电力系统动态仿真结果，并可选择性地标记事件。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名（通常是 'time'）。
            y_cols (List[str]): 一个包含多个Y轴列名的列表，每一列代表一个信号。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            events (Optional[dict], optional): 一个字典，用于标记事件。
                                              例如 `{'Fault': 1.0, 'Clear': 1.1}`，
                                              键是事件名，值是时间点。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax

        # 绘制时间序列线
        for y_col in y_cols:
            label = kwargs.pop('label', y_col)
            ax.plot(data[x], data[y_col], label=label, **kwargs)

        # 标记事件
        if events and isinstance(events, dict):
            utils.add_event_markers(
                ax=ax,
                event_dates=list(events.values()),
                labels=list(events.keys())
            )
        
        # 设置默认标签和图例
        ax.set_xlabel(kwargs.pop('xlabel', 'Time (s)'))
        ax.set_ylabel(kwargs.pop('ylabel', 'Value'))
        if any(ax.get_legend_handles_labels()):
             ax.legend()

        return self

    # --- 修改子图的方法 (Modifiers) ---
    def set_title(self, tag: Union[str, int], label: str, **kwargs) -> 'Plotter':
        """
        为指定子图设置标题。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            label (str): 要设置的标题文本。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.set_title` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self._get_ax_by_tag(tag).set_title(label, **kwargs)
        return self

    def set_xlabel(self, tag: Union[str, int], label: str, **kwargs) -> 'Plotter':
        """
        为指定子图设置X轴标签。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            label (str): 要设置的X轴标签文本。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.set_xlabel` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self._get_ax_by_tag(tag).set_xlabel(label, **kwargs)
        return self

    def set_ylabel(self, tag: Union[str, int], label: str, **kwargs) -> 'Plotter':
        """
        为指定子图设置Y轴标签。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            label (str): 要设置的Y轴标签文本。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.set_ylabel` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self._get_ax_by_tag(tag).set_ylabel(label, **kwargs)
        return self

    def set_xlim(self, tag: Union[str, int], *args, **kwargs) -> 'Plotter':
        """
        为指定子图设置X轴的显示范围。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            *args: 传递给 `matplotlib.axes.Axes.set_xlim` 的位置参数，通常是 `(xmin, xmax)`。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.set_xlim` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self._get_ax_by_tag(tag).set_xlim(*args, **kwargs)
        return self

    def set_ylim(self, tag: Union[str, int], *args, **kwargs) -> 'Plotter':
        """
        为指定子图设置Y轴的显示范围。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            *args: 传递给 `matplotlib.axes.Axes.set_ylim` 的位置参数，通常是 `(ymin, ymax)`。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.set_ylim` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self._get_ax_by_tag(tag).set_ylim(*args, **kwargs)
        return self
        
    def tick_params(self, tag: Union[str, int], axis: str = 'both', **kwargs) -> 'Plotter':
        """
        为指定子图的刻度线、刻度标签和网格线设置参数。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            axis (str, optional): 要应用参数的轴。可以是 'x', 'y', 或 'both'。默认为 'both'。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.tick_params` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self._get_ax_by_tag(tag).tick_params(axis=axis, **kwargs)
        return self

    def set_legend(self, tag: Union[str, int], **kwargs) -> 'Plotter':
        """
        为指定子图添加图例。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.legend` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self._get_ax_by_tag(tag).legend(**kwargs)
        return self

    def set_suptitle(self, title: str, **kwargs):
        """
        为整个画布（Figure）设置一个主标题。

        Args:
            title (str): 要设置的主标题文本。
            **kwargs: 其他传递给 `matplotlib.figure.Figure.suptitle` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        self.fig.suptitle(title, **kwargs)
        return self

    def add_global_legend(self, tags: list = None, remove_sub_legends: bool = True, **kwargs):
        """
        创建一个作用于整个画布的全局图例。

        它会收集指定（或所有）子图的图例项，去重后生成一个统一的图例。

        Args:
            tags (list, optional): 一个包含子图tag的列表，指定从哪些子图收集图例。
                                   如果为None，则从所有子图收集。默认为None。
            remove_sub_legends (bool, optional): 如果为True，在创建全局图例后，
                                                 将移除被收集的子图自身的独立图例。
                                                 默认为True。
            **kwargs: 其他传递给 `matplotlib.figure.Figure.legend` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        handles, labels = [], []
        ax_to_process = []

        target_tags = tags if tags is not None else self.tag_to_ax.keys()

        for tag in target_tags:
            ax = self._get_ax_by_tag(tag)
            h, l = ax.get_legend_handles_labels()
            if h and l:
                handles.extend(h)
                labels.extend(l)
                ax_to_process.append(ax)

        # 去重
        from collections import OrderedDict
        by_label = OrderedDict(zip(labels, handles))

        if by_label:
            self.fig.legend(by_label.values(), by_label.keys(), **kwargs)

            if remove_sub_legends:
                for ax in ax_to_process:
                    if ax.get_legend() is not None:
                        ax.get_legend().remove()
        
        return self

    def add_twinx(self, tag: str, **kwargs) -> plt.Axes:
        """
        为一个已存在的子图创建一个共享X轴但拥有独立Y轴的“双Y轴”图。

        Args:
            tag (str): 现有子图的tag，新创建的twinx轴将与此子图共享X轴。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.twinx` 的关键字参数。

        Returns:
            matplotlib.axes.Axes: 新创建的 `Axes` 对象，用于绘制第二个Y轴的数据。
                                  用户可以直接在这个返回的Axes对象上调用绘图方法。
        """
        ax1 = self._get_ax_by_tag(tag)
        ax2 = ax1.twinx(**kwargs)
        return ax2

    def add_regplot(self, data: pd.DataFrame, x: str, y: str, tag: Optional[str] = None, ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制散点图和线性回归趋势线。

        内部调用 `seaborn.regplot`。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名。
            y (str): 数据框中用于Y轴的列名。
            tag (str, optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (plt.Axes, optional): 要在其上绘图的Matplotlib Axes对象。
                                     如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `seaborn.regplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        
        import seaborn as sns
        sns.regplot(data=data, x=x, y=y, ax=ax, **kwargs)
        return self

    def add_hline(self, tag: str, y: float, **kwargs) -> 'Plotter':
        """
        在指定子图上添加一条水平参考线。

        Args:
            tag (str): 目标子图的tag。
            y (float): 水平线在Y轴上的位置。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.axhline` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_ax_by_tag(tag)
        ax.axhline(y, **kwargs)
        return self

    def add_vline(self, tag: str, x: float, **kwargs) -> 'Plotter':
        """
        在指定子图上添加一条垂直参考线。

        Args:
            tag (str): 目标子图的tag。
            x (float): 垂直线在X轴上的位置。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.axvline` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_ax_by_tag(tag)
        ax.axvline(x, **kwargs)
        return self

    def add_text(self, tag: str, x: float, y: float, text: str, **kwargs) -> 'Plotter':
        """
        在指定子图的数据坐标系上添加文本。

        Args:
            tag (str): 目标子图的tag。
            x (float): 文本在X轴上的数据坐标。
            y (float): 文本在Y轴上的数据坐标。
            text (str): 要添加的文本内容。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.text` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_ax_by_tag(tag)
        ax.text(x, y, text, **kwargs)
        return self

    def add_patch(self, tag: str, patch_object) -> 'Plotter':
        """
        将一个Matplotlib的Patch对象（如Rectangle, Circle, Arrow）添加到指定子图。

        Args:
            tag (str): 目标子图的tag。
            patch_object: 要添加的Matplotlib Patch对象实例。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_ax_by_tag(tag)
        ax.add_patch(patch_object)
        return self

    def add_inset_image(self, host_tag: Union[str, int], image_path: str, rect: List[float], **kwargs) -> 'Plotter':
        """
        在指定子图内部嵌入一张图片。

        Args:
            host_tag (Union[str, int]): 目标子图的标签。
            image_path (str): 要嵌入的图片的文件路径。
            rect (List[float]): 一个形如 `[x, y, width, height]` 的列表，
                                定义了图片在宿主子图内部的位置和大小。
                                这些坐标是相对坐标（0到1之间）。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.imshow` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            FileNotFoundError: 如果图片文件未找到。
            TagNotFoundError: 如果指定的host_tag未找到。
        """
        host_ax = self._get_ax_by_tag(host_tag)
        
        try:
            img = mpimg.imread(image_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found at: {image_path}")

        inset_ax = host_ax.inset_axes(rect)
        inset_ax.imshow(img, **kwargs)
        inset_ax.axis('off')

        return self

    def add_phasor_diagram(self, magnitudes: List[float], angles: List[float],
                           labels: Optional[List[str]] = None, tag: Union[str, int] = None,
                           angle_unit: str = 'degrees', **kwargs) -> 'Plotter':
        """
        在指定子图上绘制相量图。

        如果目标子图不是极坐标投影，它将被替换为一个新的极坐标子图。

        Args:
            magnitudes (List[float]): 相量的幅值列表。
            angles (List[float]): 相量的角度列表。
            labels (Optional[List[str]], optional): 相量的标签列表。默认为None。
            tag (Union[str, int], optional): 目标子图的tag。如果未提供，将自动分配。
            angle_unit (str, optional): 角度的单位，'degrees' 或 'radians'。默认为 'degrees'。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 或 `matplotlib.axes.Axes.annotate` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果幅值和角度列表长度不匹配。
            TagNotFoundError: 如果指定的tag未找到。
        """
        if len(magnitudes) != len(angles):
            raise ValueError("Magnitudes and angles lists must have the same length.")

        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax

        # 获取目标轴
        target_ax = self._get_ax_by_tag(tag)

        # 如果轴不是极坐标投影，则替换它
        if target_ax.projection != 'polar':
            logger.info(f"Axis '{tag}' is not polar. Replacing with a polar axis.")
            # 获取当前轴的位置
            bbox = target_ax.get_position()
            # 从图中删除当前轴
            self.fig.delaxes(target_ax)
            # 在相同位置创建一个新的极坐标轴
            polar_ax = self.fig.add_axes(bbox, projection='polar')
            # 更新Plotter内部的轴引用
            self.axes_dict[tag] = polar_ax
            # 还需要更新self.axes列表，找到并替换
            for i, ax_in_list in enumerate(self.axes):
                if ax_in_list == target_ax:
                    self.axes[i] = polar_ax
                    break
            target_ax = polar_ax
        
        # 设置极坐标轴的常见电气工程约定
        target_ax.set_theta_zero_location('right') # 0度在右侧
        target_ax.set_theta_direction(-1) # 角度顺时针增加

        # 转换角度为弧度
        if angle_unit == 'degrees':
            angles_rad = np.deg2rad(angles)
        else:
            angles_rad = np.array(angles)

        # 绘制相量
        for i, (mag, ang_rad) in enumerate(zip(magnitudes, angles_rad)):
            # 绘制向量 (从原点到 (mag, ang_rad))
            # 使用 plot 绘制线段，并用 marker='->' 表示箭头
            line_kwargs = kwargs.copy()
            label = labels[i] if labels and i < len(labels) else f'Phasor {i+1}'
            line_kwargs.setdefault('label', label)
            line_kwargs.setdefault('color', plt.cm.viridis(i / len(magnitudes))) # 默认颜色
            line_kwargs.setdefault('linewidth', 2)
            line_kwargs.setdefault('marker', '>') # 箭头标记
            line_kwargs.setdefault('markersize', 8)
            line_kwargs.setdefault('markevery', [1]) # 只在末端显示箭头

            target_ax.plot([0, ang_rad], [0, mag], **line_kwargs)

            # 添加标签
            if labels and i < len(labels):
                text_kwargs = kwargs.copy()
                text_kwargs.setdefault('ha', 'center')
                text_kwargs.setdefault('va', 'bottom')
                text_kwargs.setdefault('fontsize', 10)
                # 稍微偏移标签，避免与箭头重叠
                text_offset_mag = mag * 0.1 
                target_ax.text(ang_rad, mag + text_offset_mag, labels[i], **text_kwargs)

        # 设置极径（幅值）范围
        max_mag = max(magnitudes) if magnitudes else 1
        target_ax.set_rlim(0, max_mag * 1.2) # 留出一些空间

        # 设置角度网格线（例如每30度）
        target_ax.set_thetagrids(np.arange(0, 360, 30))
        
        # 设置径向刻度标签
        target_ax.set_rticks(np.linspace(0, max_mag, 3)) # 3个径向刻度

        target_ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1)) # 将图例放在外面

        return self

    # --- 收尾与美化 ---
    def get_ax(self, tag: Union[str, int]) -> plt.Axes:
        """
        通过tag获取对应的Axes对象。

        这是一个公共方法，方便用户直接获取Axes对象进行更高级的Matplotlib操作。

        Args:
            tag (Union[str, int]): 子图的唯一标识符。

        Returns:
            matplotlib.axes.Axes: 对应的Axes对象。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        return self._get_ax_by_tag(tag)

    def get_ax_by_name(self, name: str) -> plt.Axes:
        """
        通过布局时定义的名字获取对应的Axes对象。

        此方法主要用于马赛克布局，允许用户通过布局字符串中定义的名称来访问特定的子图。

        Args:
            name (str): 在布局定义（例如 `[['A', 'B'], ['C', 'D']]`）中为子图指定的名称。

        Returns:
            matplotlib.axes.Axes: 对应的Axes对象。

        Raises:
            ValueError: 如果指定的名称未在布局中找到。
        """
        if not isinstance(self.axes_dict, dict) or name not in self.axes_dict:
            available_names = list(self.axes_dict.keys()) if isinstance(self.axes_dict, dict) else []
            raise ValueError(f"Name '{name}' not found in layout. Available names are: {available_names}")
        return self.axes_dict[name]

    def hide_axes(self, x: bool = False, y: bool = False) -> 'Plotter':
        """
        隐藏所有子图的X轴或Y轴。

        Args:
            x (bool, optional): 如果为True，则隐藏所有子图的X轴。默认为False。
            y (bool, optional): 如果为True，则隐藏所有子图的Y轴。默认为False。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        for ax in self.axes:
            if x:
                ax.get_xaxis().set_visible(False)
            if y:
                ax.get_yaxis().set_visible(False)
        return self

    def cleanup(self, share_y_on_rows: list[int] = None, share_x_on_cols: list[int] = None, align_labels: bool = True):
        """
        根据指定对行或列进行坐标轴共享和清理，并可选择对齐轴标签。

        Args:
            share_y_on_rows (list[int], optional): 
                需要共享Y轴的行号列表（从0开始）。该行除最左侧子图外，
                其余子图的Y轴刻度和标签将被隐藏。
            share_x_on_cols (list[int], optional): 
                需要共享X轴的列号列表（从0开始）。该列除最下方子图外，
                其余子图的X轴刻度和标签将被隐藏。
            align_labels (bool, optional): 
                如果为True，将尝试自动对齐所有子图的轴标签，
                使布局更整齐。默认为True。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 获取网格尺寸，为后续计算做准备
        try:
            # 尝试从布局中获取行列数
            if isinstance(self.layout, tuple):
                n_rows, n_cols = self.layout
            else:
                n_rows = len(self.layout)
                n_cols = len(self.layout[0]) if n_rows > 0 else 0
        except:
            n_rows, n_cols = 1, len(self.axes)

        # 创建一个从 (row, col) 到 ax 的映射，方便查找
        # 注意：这个映射对于复杂布局可能不准确，但对于简单的行列共享足够
        ax_map = {}
        if isinstance(self.axes_dict, dict):
             for name, ax in self.axes_dict.items():
                try:
                    # 尝试从gridspec获取位置
                    gs = ax.get_gridspec()
                    loc = ax.get_subplotspec().get_geometry()
                    # 这部分逻辑比较复杂，暂时用一个简化版
                    # 真正的行列映射需要更复杂的解析
                except:
                    pass # 回退到简单映射
        
        # 简化版映射，适用于简单网格
        if not ax_map:
             ax_map = {(i // n_cols, i % n_cols): ax for i, ax in enumerate(self.axes) if i < n_rows * n_cols}


        # --- 处理Y轴共享 ---
        if share_y_on_rows:
            for row_idx in share_y_on_rows:
                # 对于复杂布局，我们需要更可靠地找到行内的axes
                # 暂时使用简化逻辑
                row_axes = [ax_map.get((row_idx, col_idx)) for col_idx in range(n_cols)]
                row_axes = [ax for ax in row_axes if ax]

                if not row_axes or len(row_axes) < 2:
                    continue

                leader_ax = row_axes[0]
                for follower_ax in row_axes[1:]:
                    follower_ax.sharey(leader_ax)
                    follower_ax.tick_params(axis='y', labelleft=False)
                    follower_ax.set_ylabel("")

        # --- 处理X轴共享 ---
        if share_x_on_cols:
            for col_idx in share_x_on_cols:
                col_axes = [ax_map.get((row_idx, col_idx)) for row_idx in range(n_rows)]
                col_axes = [ax for ax in col_axes if ax]

                if not col_axes or len(col_axes) < 2:
                    continue

                leader_ax = col_axes[-1]
                for follower_ax in col_axes[:-1]:
                    follower_ax.sharex(leader_ax)
                    follower_ax.tick_params(axis='x', labelbottom=False)
                    follower_ax.set_xlabel("")
        
        if align_labels:
            try:
                self.fig.align_labels()
            except Exception:
                # 在某些复杂情况下，align_labels可能会失败，我们不希望因此中断程序
                pass

        return self

    def cleanup_heatmaps(self, tags: List[Union[str, int]]) -> 'Plotter':
        """
        为指定的一组热图创建共享的颜色条。

        此方法会统一指定热图的颜色映射范围，并在最后一个热图旁边添加一个共享的颜色条。

        Args:
            tags (List[Union[str, int]]): 一个包含热图tag的列表，这些热图将共享一个颜色条。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果tags列表为空，或者没有找到与给定tags对应的有效热图。
        """
        if not tags or not isinstance(tags, list):
            raise ValueError("'tags' must be a list of heatmap tags.")

        # 1. 检索所有相关的ax和颜色映射对象
        mappables = [self.tag_to_mappable.get(tag) for tag in tags]
        mappables = [m for m in mappables if m]
        if not mappables:
            raise ValueError("No valid heatmaps found for the given tags. Did you provide correct tags and ensure they were created with this Plotter instance?")

        # 2. 找到全局的数据范围 (min/max)
        try:
            global_vmin = min(m.get_clim()[0] for m in mappables)
            global_vmax = max(m.get_clim()[1] for m in mappables)
        except (AttributeError, IndexError):
             raise ValueError("Could not retrieve color limits from the provided heatmap tags.")

        # 3. 将所有热图的颜色范围统一为全局范围
        for m in mappables:
            m.set_clim(vmin=global_vmin, vmax=global_vmax)

        # 4. 创建并定位新的颜色条
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        # 找到最后一幅热图的ax，颜色条将画在它的右边
        last_ax = self._get_ax_by_tag(tags[-1])

        # 使用axes_grid1工具包来创建一个紧挨着last_ax的新ax，用于放置颜色条
        divider = make_axes_locatable(last_ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        # 5. 在新的cax上绘制颜色条
        self.fig.colorbar(mappables[-1], cax=cax)

        return self
    def save(self, filename: str, **kwargs) -> None:
        """
        将当前图形保存到文件。

        Args:
            filename (str): 保存文件的路径和名称（例如 'my_plot.png'）。
            **kwargs: 其他传递给 `matplotlib.figure.Figure.savefig` 的关键字参数。
                      默认参数为 `dpi=300` 和 `bbox_inches='tight'`。
        """
        defaults = {'dpi': 300, 'bbox_inches': 'tight'}
        defaults.update(kwargs)
        self.fig.savefig(filename, **defaults)
        plt.close(self.fig)
        logger.info(f"Figure saved to {filename}")

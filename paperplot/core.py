# paperplot/core.py

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .utils import get_style_path
from .exceptions import TagNotFoundError, DuplicateTagError, PlottingSpaceError



class Plotter:
    def __init__(self, layout, style: str = 'publication', figsize: tuple = None, **fig_kwargs):
        plt.style.use(get_style_path(style))

        # 内部布局定义
        self.layout = layout
        processed_layout = layout

        # 为了向后兼容，如果传入的是(rows, cols)元组，则自动生成布局
        if isinstance(layout, tuple) and len(layout) == 2:
            n_rows, n_cols = layout
            if figsize is None: figsize = (5 * n_cols, 4 * n_rows)
            # 生成一个简单的二维列表作为布局
            processed_layout = [[f'({r},{c})' for c in range(n_cols)] for r in range(n_rows)]
        
        fig_kwargs.setdefault('layout', 'constrained')
        if figsize is not None:
            fig_kwargs.setdefault('figsize', figsize)

        self.fig, self.axes_dict = plt.subplot_mosaic(processed_layout, **fig_kwargs)
        
        # 创建一个扁平化的、按名称排序的axes列表，以保持顺序绘图功能
        # np.atleast_1d().flatten() 用于处理单个子图的情况
        if isinstance(self.axes_dict, dict):
            self.axes = [self.axes_dict[key] for key in sorted(self.axes_dict.keys())]
        else: # 单个子图时，matplotlib返回的不是字典
            self.axes = np.atleast_1d(self.axes_dict).flatten()

        # 内部状态
        self.tag_to_ax = {}
        self.tag_to_mappable = {}
        self.current_ax_index = 0
        self.next_default_tag = 1

    def _get_ax_by_tag(self, tag):
        if tag not in self.tag_to_ax:
            raise TagNotFoundError(tag, list(self.tag_to_ax.keys()))
        return self.tag_to_ax[tag]

    def _get_next_ax_and_assign_tag(self, tag=None):
        # 获取所有已经被tag占据的axes
        claimed_axes = set(self.tag_to_ax.values())

        # 从当前索引开始，寻找第一个未被占据的ax
        ax_to_use = None
        while self.current_ax_index < len(self.axes):
            potential_ax = self.axes[self.current_ax_index]
            if potential_ax not in claimed_axes:
                ax_to_use = potential_ax
                break
            self.current_ax_index += 1

        if ax_to_use is None:
            raise PlottingSpaceError(len(self.axes))

        # 为这个新找到的空闲ax分配tag
        current_tag = tag if tag is not None else self.next_default_tag
        if current_tag in self.tag_to_ax:
            # 理论上不应该发生，因为我们已经跳过了所有claimed_axes
            raise DuplicateTagError(current_tag)
            
        if tag is None:
            self.next_default_tag += 1
            
        self.tag_to_ax[current_tag] = ax_to_use
        self.current_ax_index += 1 # 为下一次寻找做准备
        return ax_to_use

    # --- 添加绘图的方法 (Verbs) ---
    def add_line(self, data: pd.DataFrame, x: str, y: str, tag=None, ax: plt.Axes = None, **kwargs):
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        ax.plot(data[x], data[y], **kwargs)
        return self

    def add_bar(self, data: pd.DataFrame, x: str, y: str, y_err: str = None, tag=None, ax: plt.Axes = None, **kwargs):
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        y_error_values = data[y_err] if y_err and y_err in data else None
        ax.bar(data[x], data[y], yerr=y_error_values, **kwargs)
        return self
        
    def add_scatter(self, data: pd.DataFrame, x: str, y: str, tag=None, ax: plt.Axes = None, **kwargs):
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

    def add_hist(self, data: pd.DataFrame, x: str, tag=None, ax: plt.Axes = None, **kwargs):
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        ax.hist(data[x], **kwargs)
        return self

    def add_box(self, data: pd.DataFrame, tag=None, ax: plt.Axes = None, **kwargs):
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        import seaborn as sns
        sns.boxplot(data=data, ax=ax, **kwargs)
        return self

    def add_heatmap(self, data: pd.DataFrame, tag=None, ax: plt.Axes = None, **kwargs):
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

    def add_seaborn(self, plot_func, tag=None, ax: plt.Axes = None, **kwargs):
        if ax is None:
            ax = self._get_next_ax_and_assign_tag(tag)
        elif tag is not None:
            if tag in self.tag_to_ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = ax
        plot_func(ax=ax, **kwargs)
        return self

    # --- 修改子图的方法 (Modifiers) ---
    def set_title(self, tag, label: str, **kwargs):
        self._get_ax_by_tag(tag).set_title(label, **kwargs)
        return self

    def set_xlabel(self, tag, label: str, **kwargs):
        self._get_ax_by_tag(tag).set_xlabel(label, **kwargs)
        return self

    def set_ylabel(self, tag, label: str, **kwargs):
        self._get_ax_by_tag(tag).set_ylabel(label, **kwargs)
        return self

    def set_xlim(self, tag, *args, **kwargs):
        self._get_ax_by_tag(tag).set_xlim(*args, **kwargs)
        return self

    def set_ylim(self, tag, *args, **kwargs):
        self._get_ax_by_tag(tag).set_ylim(*args, **kwargs)
        return self
        
    def tick_params(self, tag, axis='both', **kwargs):
        self._get_ax_by_tag(tag).tick_params(axis=axis, **kwargs)
        return self

    def set_legend(self, tag, **kwargs):
        self._get_ax_by_tag(tag).legend(**kwargs)
        return self

    # --- 收尾与美化 ---
    def get_ax(self, tag):
        return self._get_ax_by_tag(tag)

    def get_ax_by_name(self, name: str):
        """通过布局时定义的名字获取对应的Axes对象。"""
        if not isinstance(self.axes_dict, dict) or name not in self.axes_dict:
            available_names = list(self.axes_dict.keys()) if isinstance(self.axes_dict, dict) else []
            raise ValueError(f"Name '{name}' not found in layout. Available names are: {available_names}")
        return self.axes_dict[name]

    def hide_axes(self, x: bool = False, y: bool = False):
        """隐藏所有子图的X轴或Y轴。"""
        for ax in self.axes:
            if x:
                ax.get_xaxis().set_visible(False)
            if y:
                ax.get_yaxis().set_visible(False)
        return self

    def cleanup(self, share_y_on_rows: list[int] = None, share_x_on_cols: list[int] = None):
        """
        根据指定对行或列进行坐标轴共享和清理。

        Args:
            share_y_on_rows (list[int], optional): 需要共享Y轴的行号列表。
            share_x_on_cols (list[int], optional): 需要共享X轴的列号列表。
        """
        # 获取网格尺寸，为后续计算做准备
        try:
            gs = self.axes[0].get_gridspec()
            n_rows, n_cols = gs.nrows, gs.ncols
        except:
            n_rows, n_cols = 1, len(self.axes)

        # 创建一个从 (row, col) 到 ax 的映射，方便查找
        ax_map = {(i // n_cols, i % n_cols): ax for i, ax in enumerate(self.axes) if i < n_rows * n_cols}

        # --- 处理Y轴共享 ---
        if share_y_on_rows:
            for row_idx in share_y_on_rows:
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
        
        return self

    def cleanup_heatmaps(self, tags: list[str]):
        """
        为指定的一组热图创建共享的颜色条。
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
    def save(self, filename: str, **kwargs):
        defaults = {'dpi': 300, 'bbox_inches': 'tight'}
        defaults.update(kwargs)
        self.fig.savefig(filename, **defaults)
        plt.close(self.fig)
        print(f"Figure saved to {filename}")

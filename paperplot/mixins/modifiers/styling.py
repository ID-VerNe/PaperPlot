from typing import Optional, Union, Tuple, Dict
import matplotlib.pyplot as plt

class StylingMixin:
    def set_title(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """为指定或当前活动的子图设置标题。

        Args:
            label (str): 标题文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.set_title` 的参数 (e.g., fontsize, loc, color)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_title(label, **kwargs)
        return self

    def set_xlabel(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """设置子图 X 轴标签。

        Args:
            label (str): 标签文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.set_xlabel` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_xlabel(label, **kwargs)
        return self

    def set_ylabel(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """设置子图 Y 轴标签。

        Args:
            label (str): 标签文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.set_ylabel` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_ylabel(label, **kwargs)
        return self
    
    def set_zlabel(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """设置子图 Z 轴标签 (仅限 3D 图)。

        Args:
            label (str): 标签文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.set_zlabel` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        if ax.name == '3d':
            ax.set_zlabel(label, **kwargs)
        return self

    def view_init(self, elev: float, azim: float, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """设置 3D 子图的视角。

        Args:
            elev (float): 仰角 (elevation angle)。
            azim (float): 方位角 (azimuth angle)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        if ax.name == '3d':
            ax.view_init(elev=elev, azim=azim)
        return self

    def set_xlim(self, left: Optional[float] = None, right: Optional[float] = None, 
                 tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """设置子图 X 轴范围。

        Args:
            left (float, optional): X轴下限。
            right (float, optional): X轴上限。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.set_xlim` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_xlim(left=left, right=right, **kwargs)
        return self

    def set_ylim(self, bottom: Optional[float] = None, top: Optional[float] = None, 
                 tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """设置子图 Y 轴范围。

        Args:
            bottom (float, optional): Y轴下限。
            top (float, optional): Y轴上限。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.set_ylim` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_ylim(bottom=bottom, top=top, **kwargs)
        return self

    def tick_params(self, axis: str = 'both', tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """设置刻度参数 (封装 `ax.tick_params`)。

        Args:
            axis (str, optional): 应用轴 ('x', 'y', 'both')。默认为 'both'。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.tick_params` 的参数 (e.g., labelsize, direction, length, width, colors)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.tick_params(axis=axis, **kwargs)
        return self

    def hide_axes(self, tag: Optional[Union[str, int]] = None,
                  x_axis=False, y_axis=False,
                  x_ticks=False, y_ticks=False,
                  x_tick_labels=False, y_tick_labels=False,
                  x_label=False, y_label=False,
                  spines: list[str] = None) -> 'Plotter':
        """精细化地隐藏指定或当前活动子图的坐标轴元素。

        Args:
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            x_axis (bool): 如果为 True，隐藏整个 X 轴（包括标签、刻度等）。
            y_axis (bool): 如果为 True，隐藏整个 Y 轴。
            x_ticks (bool): 如果为 True，仅隐藏 X 轴的刻度线。
            y_ticks (bool): 如果为 True，仅隐藏 Y 轴的刻度线。
            x_tick_labels (bool): 如果为 True，仅隐藏 X 轴的刻度标签。
            y_tick_labels (bool): 如果为 True，仅隐藏 Y 轴的刻度标签。
            x_label (bool): 如果为 True，仅隐藏 X 轴的标签文本。
            y_label (bool): 如果为 True，仅隐藏 Y 轴的标签文本。
            spines (List[str]): 一个包含 'top', 'bottom', 'left', 'right' 的列表，
                                 指定要隐藏的轴线。
        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)

        if x_axis:
            ax.get_xaxis().set_visible(False)
        if y_axis:
            ax.get_yaxis().set_visible(False)

        if x_ticks:
            ax.tick_params(axis='x', bottom=False)
        if y_ticks:
            ax.tick_params(axis='y', left=False)

        if x_tick_labels:
            ax.tick_params(axis='x', labelbottom=False)
        if y_tick_labels:
            ax.tick_params(axis='y', labelleft=False)

        if x_label:
            ax.xaxis.label.set_visible(False)
        if y_label:
            ax.yaxis.label.set_visible(False)

        if spines:
            for spine in spines:
                ax.spines[spine].set_visible(False)

        return self

    def cleanup(self, share_y_on_rows: list[int] = None, share_x_on_cols: list[int] = None, align_labels: bool = True, auto_share: Union[bool, str] = False) -> 'Plotter':
        """根据指定的行或列共享坐标轴，并对齐标签。

        这是一个方便的函数，用于在绘图完成后统一调整子图网格的外观，
        移除多余的刻度和标签，使图形更整洁。

        Args:
            share_y_on_rows (list[int], optional):
                一个整数列表，指定哪些行应该共享Y轴。
                例如 `[0, 1]` 会使第0行和第1行内部各自共享Y轴。
                默认为 `None`。
            share_x_on_cols (list[int], optional):
                一个整数列表，指定哪些列应该共享X轴。
                例如 `[0]` 会使第0列的所有子图共享X轴。
                默认为 `None`。
            align_labels (bool, optional): 如果为 `True`，则尝试对齐
                整个图表的X和Y轴标签。默认为 `True`。
            auto_share (Union[bool, str], optional):
                如果为 `True`，则自动共享所有行/列的轴。
                如果为 'x'，仅自动共享X轴。
                如果为 'y'，仅自动共享Y轴。
                默认为 `False`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        try:
            if isinstance(self.layout, tuple):
                n_rows, n_cols = self.layout
            else:
                n_rows = len(self.layout)
                n_cols = len(self.layout[0]) if n_rows > 0 else 0
        except:
            n_rows, n_cols = 1, len(self.axes)

        # Implement auto_share logic
        if auto_share is True or auto_share == 'y':
            if share_y_on_rows is None:
                share_y_on_rows = list(range(n_rows))
        
        if auto_share is True or auto_share == 'x':
            if share_x_on_cols is None:
                share_x_on_cols = list(range(n_cols))

        ax_map = {(i // n_cols, i % n_cols): ax for i, ax in enumerate(self.axes) if i < n_rows * n_cols}

        if share_y_on_rows:
            for row_idx in share_y_on_rows:
                row_axes = [ax_map.get((row_idx, col_idx)) for col_idx in range(n_cols)]
                row_axes = [ax for ax in row_axes if ax]
                if not row_axes or len(row_axes) < 2: continue
                leader_ax = row_axes[0]
                for follower_ax in row_axes[1:]:
                    follower_ax.sharey(leader_ax)
                    follower_ax.tick_params(axis='y', labelleft=False)
                    follower_ax.set_ylabel("")

        if share_x_on_cols:
            for col_idx in share_x_on_cols:
                col_axes = [ax_map.get((row_idx, col_idx)) for row_idx in range(n_rows)]
                col_axes = [ax for ax in col_axes if ax]
                if not col_axes or len(col_axes) < 2: continue
                leader_ax = col_axes[-1]
                for follower_ax in col_axes[:-1]:
                    follower_ax.sharex(leader_ax)
                    follower_ax.tick_params(axis='x', labelbottom=False)
                    follower_ax.set_xlabel("")
        
        if align_labels:
            try:
                self.fig.align_labels()
            except Exception:
                pass
        return self

    def cleanup_heatmaps(self, tags: list[Union[str, int]]) -> 'Plotter':
        """为指定的一组热图创建共享的、统一的颜色条（colorbar）。

        此方法会找到所有指定热图的全局颜色范围（vmin, vmax），
        将所有热图的颜色范围设置为该全局范围，然后在最后一个
        指定的热图旁边创建一个共享的颜色条。

        Args:
            tags (List[Union[str, int]]): 一个包含热图子图 `tag` 的列表。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果 `tags` 不是一个列表，或者在给定的 `tags`
                        中找不到有效的热图。
        """
        if not tags or not isinstance(tags, list):
            raise ValueError("'tags' must be a list of heatmap tags.")

        mappables = [self.tag_to_mappable.get(tag) for tag in tags]
        mappables = [m for m in mappables if m]
        if not mappables:
            raise ValueError("No valid heatmaps found for the given tags.")

        try:
            global_vmin = min(m.get_clim()[0] for m in mappables)
            global_vmax = max(m.get_clim()[1] for m in mappables)
        except (AttributeError, IndexError):
             raise ValueError("Could not retrieve color limits from the provided heatmap tags.")

        for m in mappables:
            m.set_clim(vmin=global_vmin, vmax=global_vmax)

        from mpl_toolkits.axes_grid1 import make_axes_locatable
        last_ax = self._get_ax_by_tag(tags[-1])
        divider = make_axes_locatable(last_ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        self.fig.colorbar(mappables[-1], cax=cax)
        return self

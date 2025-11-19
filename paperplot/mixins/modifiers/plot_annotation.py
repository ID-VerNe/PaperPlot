from typing import Optional, Union, Tuple, List, Dict
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
try:
    from adjustText import adjust_text
except ImportError:
    adjust_text = None

class PlotAnnotationMixin:
    def _get_corner_fig_coords(self, ax: plt.Axes, corner: str, x_range=None, y_range=None) -> Tuple[float, float]:
        """[私有] 获取子图指定角落的 Figure 坐标。"""
        # 如果提供了数据范围，我们需要先转换数据坐标到 Figure 坐标
        if x_range is not None and y_range is not None:
            # corner is int 1-4: 1=UR, 2=UL, 3=LL, 4=LR
            # But here corner is passed as int from add_zoom_connectors
            # Logic in add_zoom_connectors passes 1, 2, 3, 4
            # 1: Upper Right, 2: Upper Left, 3: Lower Left, 4: Lower Right
            
            x, y = 0, 0
            if corner == 1: # UR
                x, y = x_range[1], y_range[1]
            elif corner == 2: # UL
                x, y = x_range[0], y_range[1]
            elif corner == 3: # LL
                x, y = x_range[0], y_range[0]
            elif corner == 4: # LR
                x, y = x_range[1], y_range[0]
                
            # Transform data coords to figure coords
            return self.fig.transFigure.inverted().transform(ax.transData.transform((x, y)))
        
        # Fallback to bbox corners if no range provided (or for inset ax which uses 0-1 if not data?)
        # Actually inset ax usually has data coords too.
        # But let's stick to the original logic found in modifiers.py if possible.
        # Wait, I don't have the original _get_corner_fig_coords implementation in front of me for the range part.
        # Let me infer from usage in add_zoom_connectors.
        
        bbox = ax.get_position()
        if corner == 'top-left' or corner == 2:
            return bbox.x0, bbox.y1
        elif corner == 'top-right' or corner == 1:
            return bbox.x1, bbox.y1
        elif corner == 'bottom-left' or corner == 3:
            return bbox.x0, bbox.y0
        elif corner == 'bottom-right' or corner == 4:
            return bbox.x1, bbox.y0
        return bbox.x0, bbox.y1

    def add_hline(self, y: float, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """在指定或当前活动的子图上添加一条水平参考线。

        Args:
            y (float): 水平线的y轴位置。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.axhline` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.axhline(y, **kwargs)
        return self

    def add_vline(self, x: float, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """在指定或当前活动的子图上添加一条垂直参考线。

        Args:
            x (float): 垂直线的x轴位置。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.axvline` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.axvline(x, **kwargs)
        return self

    def add_text(self, x: float, y: float, text: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """在指定或当前活动的子图的数据坐标系上添加文本。

        Args:
            x (float): 文本的x坐标。
            y (float): 文本的y坐标。
            text (str): 要添加的文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.text` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.text(x, y, text, **kwargs)
        return self

    def add_patch(self, patch_object, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """将一个Matplotlib的Patch对象添加到指定或当前活动的子图。

        Args:
            patch_object: 一个Matplotlib Patch对象 (例如 `plt.Circle`)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.add_patch(patch_object)
        return self

    def add_highlight_box(self, x_range: tuple[float, float], y_range: tuple[float, float], tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """在指定或当前活动的子图上，根据数据坐标绘制一个高亮矩形区域。

        Args:
            x_range (tuple[float, float]): 高亮区域的X轴范围 (xmin, xmax)。
            y_range (tuple[float, float]): 高亮区域的Y轴范围 (ymin, ymax)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `matplotlib.patches.Rectangle` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        
        width = x_range[1] - x_range[0]
        height = y_range[1] - y_range[0]
        
        kwargs.setdefault('facecolor', 'yellow')
        kwargs.setdefault('alpha', 0.3)
        kwargs.setdefault('edgecolor', 'none')
        kwargs.setdefault('zorder', 0)

        rect = plt.Rectangle((x_range[0], y_range[0]), width, height, **kwargs)
        ax.add_patch(rect)
        return self

    def add_inset_image(self, image_path: str, rect: List[float], host_tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """在指定或当前活动的子图内部嵌入一张图片。

        Args:
            image_path (str): 要嵌入的图片文件路径。
            rect (List[float]): 一个定义嵌入位置和大小的列表 `[x, y, width, height]`，
                                坐标是相对于宿主子图的。
            host_tag (Optional[Union[str, int]], optional): 宿主子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.imshow` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        host_ax = self._get_active_ax(host_tag)
        
        try:
            img = mpimg.imread(image_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"图片文件未找到: {image_path}")

        inset_ax = host_ax.inset_axes(rect)
        inset_ax.imshow(img, **kwargs)
        inset_ax.axis('off')

        return self

    def add_zoom_inset(self, rect: List[float], x_range: Tuple[float, float],
                       y_range: Optional[Tuple[float, float]] = None,
                       source_tag: Optional[Union[str, int]] = None,
                       draw_source_box: bool = True,
                       source_box_kwargs: Optional[dict] = None) -> 'Plotter':
        """在指定或当前活动的子图上添加一个缩放指示（inset plot）。

        Args:
            rect (List[float]): 一个定义内嵌图位置和大小的列表 `[x, y, width, height]`，
                                坐标是相对于**父坐标轴**的 (0到1)。
            x_range (Tuple[float, float]): 内嵌图的X轴范围 (xmin, xmax)。
            y_range (Optional[Tuple[float, float]], optional): 内嵌图的Y轴范围 (ymin, ymax)。
                                                                如果为 `None`，将根据 `x_range` 自动计算。
            source_tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            draw_source_box (bool, optional): 是否在源图上绘制一个矩形框来表示缩放范围。
            source_box_kwargs (Optional[dict], optional): 传递给 `ax.add_patch` 的关键字参数，用于定制源图矩形框的样式。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 步骤 1: 获取源 Axes 和其缓存的数据
        source_ax = self._get_active_ax(source_tag)
        active_tag = source_tag if source_tag is not None else self.last_active_tag

        if active_tag not in self.data_cache:
            raise ValueError(f"未能为源子图 '{active_tag}' 找到缓存数据以创建缩放图。")

        source_data = self.data_cache[active_tag]
        # 假设缓存的DataFrame中，前两列分别是X和Y数据
        x_col, y_col = source_data.columns[0], source_data.columns[1]

        # 步骤 2: 创建内嵌图 Axes
        # 注意：inset_axes 的 rect 是相对于父轴的坐标系
        inset_ax = source_ax.inset_axes(rect)
        self.inset_axes[active_tag] = inset_ax # <-- 添加这一行

        # 步骤 3: 筛选出仅在放大范围内的数据
        zoomed_data = source_data[
            (source_data[x_col] >= x_range[0]) & (source_data[x_col] <= x_range[1])
            ]

        # 实现自动 y_range 逻辑
        resolved_y_range = y_range
        if resolved_y_range is None:
            if not zoomed_data.empty:
                min_y = zoomed_data[y_col].min()
                max_y = zoomed_data[y_col].max()
                padding = (max_y - min_y) * 0.05  # 增加 5% 的垂直边距
                resolved_y_range = (min_y - padding, max_y + padding)
            else:
                # 如果范围内没有数据，则退回使用源图的Y轴范围
                resolved_y_range = source_ax.get_ylim()

        # 步骤 4: 在内嵌图中只绘制筛选后的数据子集
        # 我们从源图中获取第一条线的颜色，以保持样式一致
        line_color = source_ax.lines[0].get_color() if source_ax.lines else 'blue'
        inset_ax.plot(zoomed_data[x_col], zoomed_data[y_col], color=line_color)

        # 步骤 5: 为内嵌图设置精确的缩放范围和样式
        inset_ax.set_xlim(x_range)
        inset_ax.set_ylim(resolved_y_range) # 使用 resolved_y_range

        # 步骤 6: 优化内嵌图的可读性
        inset_ax.grid(True, linestyle='--', alpha=0.6)  # 添加网格线
        inset_ax.tick_params(axis='both', which='major', labelsize=8)
        
        # 步骤 8: 保存源区域的数据范围
        self.source_zoom_ranges[active_tag] = (x_range, resolved_y_range)

        # 步骤 9: 根据参数决定是否在源图上绘制高亮框
        if draw_source_box:
            # 准备高亮框的样式参数
            final_box_kwargs = {'facecolor': 'gray', 'alpha': 0.2, 'zorder': 0}
            if source_box_kwargs:
                final_box_kwargs.update(source_box_kwargs)

            # 复用已有的 add_highlight_box 方法来绘制矩形
            # 我们需要确保操作的目标是 source_ax，可以通过 tag 来指定
            self.add_highlight_box(
                x_range=x_range,
                y_range=resolved_y_range,  # 使用已计算好的Y轴范围
                tag=active_tag,
                **final_box_kwargs
            )

        return self

    def add_zoom_connectors(self, connections: List[Tuple[int, int]],
                            source_tag: Optional[Union[str, int]] = None,
                            **kwargs) -> 'Plotter':
        """为缩放内嵌图手动添加自定义的连接线。

        此方法提供了对连接线的完全控制，允许你指定连接线
        从源区域的哪个角连接到内嵌图的哪个角。

        Args:
            connections (List[Tuple[int, int]]):
                一个连接定义的列表。每个定义是一个 (source_loc, inset_loc) 元组。
                例如, `[(2, 1), (3, 4)]` 表示:
                - 画一条线从源区域的左上角(2)到内嵌图的右上角(1)。
                - 画另一条线从源区域的左下角(3)到内嵌图的右下角(4)。
            source_tag (Optional[Union[str, int]], optional):
                源子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs:
                传递给 `self.fig_add_line` 的关键字参数，用于定制线的样式，
                例如 `color='gray'`, `linestyle='--'`, `linewidth=1`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        active_tag = source_tag if source_tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("没有为缩放连接线指定源子图。")

        source_ax = self._get_ax_by_tag(active_tag)
        if active_tag not in self.inset_axes:
            raise ValueError(f"没有找到tag为 '{active_tag}' 的内嵌图。请先调用 add_zoom_inset()。")
        inset_ax = self.inset_axes[active_tag]

        if active_tag not in self.source_zoom_ranges:
            raise ValueError(f"没有找到tag为 '{active_tag}' 的源区域缩放范围。请先调用 add_zoom_inset()。")
        
        source_x_range, source_y_range = self.source_zoom_ranges[active_tag]

        self.fig.canvas.draw()

        for source_loc, inset_loc in connections:
            start_coords = self._get_corner_fig_coords(source_ax, source_loc, source_x_range, source_y_range)
            end_coords = self._get_corner_fig_coords(inset_ax, inset_loc)

            self.fig_add_line(
                [start_coords[0], end_coords[0]],
                [start_coords[1], end_coords[1]],
                **kwargs
            )

        return self

    def add_peak_highlights(self, peaks_x: list, x_col: str, y_col: str,
                            label_peaks: bool = True, 
                            prefer_direction: str = 'up',
                            use_bbox: bool = True,
                            label_positions: dict = None,
                            tag: Optional[Union[str, int]] = None,
                            **kwargs) -> 'Plotter':
        """在一条已绘制的光谱或曲线上，自动高亮并（可选地）标注出特征峰的位置。 使用 adjustText 库来避免标签重叠。

        Args:
            peaks_x (list): 一个包含特征峰X轴位置的列表。
            x_col (str): 缓存的DataFrame中包含X轴数据的列名。
            y_col (str): 缓存的DataFrame中包含Y轴数据的列名。
            label_peaks (bool, optional): 如果为True，则在峰顶附近标注X轴值。默认为True。
            prefer_direction (str, optional): 自动布局时文本的初始放置方向, 'up' 或 'down'。默认为 'up'。
            use_bbox (bool, optional): 如果为True，为文本添加一个半透明的背景框。默认为True。
            label_positions (dict, optional): 一个字典，用于手动指定标签位置。
                                              键是峰值的X坐标，值是(x, y)元组。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.axvline` 和 `ax.text` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        active_tag = tag if tag is not None else self.last_active_tag
        
        if active_tag not in self.data_cache:
            raise ValueError(f"未能为子图 '{active_tag}' 找到缓存的数据。")
        
        data = self.data_cache[active_tag]
        x = data[x_col]
        y = data[y_col]

        text_kwargs = kwargs.copy()
        vline_kwargs = {
            'color': text_kwargs.pop('color', 'gray'),
            'linestyle': text_kwargs.pop('linestyle', '--')
        }
        
        if use_bbox:
            text_kwargs.setdefault('bbox', dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))

        auto_texts = []
        for peak in peaks_x:
            idx = np.abs(x - peak).argmin()
            peak_x_val = x.iloc[idx]
            peak_y_val = y.iloc[idx]
            
            ax.axvline(x=peak_x_val, **vline_kwargs)
            
            if label_peaks:
                label_text = f'{peak_x_val:.0f}'
                if label_positions and peak in label_positions:
                    pos = label_positions[peak]
                    ax.text(pos[0], pos[1], label_text, **text_kwargs)
                else:
                    y_offset = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.05
                    initial_y = peak_y_val + y_offset if prefer_direction == 'up' else peak_y_val - y_offset
                    auto_texts.append(ax.text(peak_x_val, initial_y, label_text, **text_kwargs))
                
        if auto_texts and adjust_text:
            adjust_text(auto_texts, ax=ax, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
        
        return self

    def add_event_markers(self, event_dates: list, labels: list = None, 
                          use_bbox: bool = True, 
                          label_positions: dict = None,
                          tag: Optional[Union[str, int]] = None,
                          **kwargs) -> 'Plotter':
        """在时间序列图上标记重要的垂直事件。 使用 adjustText 库来避免标签重叠。

        Args:
            event_dates (list): 包含事件X轴位置的列表。
            labels (list, optional): 与每个事件对应的标签列表。如果提供，将在事件线上方显示。
            use_bbox (bool, optional): 如果为True，为文本添加一个半透明的背景框。默认为True。
            label_positions (dict, optional): 一个字典，用于手动指定标签位置。
                                              键是事件的X坐标，值是(x, y)元组。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 其他传递给 `ax.axvline` 和 `ax.text` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)

        vline_kwargs = kwargs.copy()
        vline_kwargs.setdefault('color', 'red')
        vline_kwargs.setdefault('linestyle', '-.')
        
        text_kwargs = kwargs.copy()
        if use_bbox:
            text_kwargs.setdefault('bbox', dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))

        auto_texts = []
        for event_date in event_dates:
            ax.axvline(x=event_date, **vline_kwargs)
        
        if labels:
            for i, event_date in enumerate(event_dates):
                if i < len(labels):
                    label_text = labels[i]
                    if label_positions and event_date in label_positions:
                        pos = label_positions[event_date]
                        ax.text(pos[0], pos[1], label_text, **text_kwargs)
                    else:
                        y_pos = ax.get_ylim()[1] * 0.95
                        auto_texts.append(ax.text(event_date, y_pos, label_text, **text_kwargs))
        
        if auto_texts and adjust_text:
            adjust_text(auto_texts, ax=ax, arrowprops=dict(arrowstyle='->', color='red'))
        
        return self

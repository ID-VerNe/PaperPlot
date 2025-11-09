# paperplot/mixins/modifiers.py

from typing import Optional, Union, List
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import logging
logger = logging.getLogger(__name__)

class ModifiersMixin:
    """
    包含用于修改、装饰和收尾图表的方法的 Mixin 类。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #确保调用父类的__init__
        self._draw_on_save_queue = []

    def set_title(self, tag: Union[str, int], label: str, **kwargs) -> 'Plotter':
        """
        为指定子图设置标题。
        """
        self._get_ax_by_tag(tag).set_title(label, **kwargs)
        return self

    def set_xlabel(self, tag: Union[str, int], label: str, **kwargs) -> 'Plotter':
        """
        为指定子图设置X轴标签。
        """
        self._get_ax_by_tag(tag).set_xlabel(label, **kwargs)
        return self

    def set_ylabel(self, tag: Union[str, int], label: str, **kwargs) -> 'Plotter':
        """
        为指定子图设置Y轴标签。
        """
        self._get_ax_by_tag(tag).set_ylabel(label, **kwargs)
        return self

    def set_xlim(self, tag: Union[str, int], *args, **kwargs) -> 'Plotter':
        """
        为指定子图设置X轴的显示范围。
        """
        self._get_ax_by_tag(tag).set_xlim(*args, **kwargs)
        return self

    def set_ylim(self, tag: Union[str, int], *args, **kwargs) -> 'Plotter':
        """
        为指定子图设置Y轴的显示范围。
        """
        self._get_ax_by_tag(tag).set_ylim(*args, **kwargs)
        return self
        
    def tick_params(self, tag: Union[str, int], axis: str = 'both', **kwargs) -> 'Plotter':
        """
        为指定子图的刻度线、刻度标签和网格线设置参数。
        """
        self._get_ax_by_tag(tag).tick_params(axis=axis, **kwargs)
        return self

    def set_legend(self, tag: Union[str, int], **kwargs) -> 'Plotter':
        """
        为指定子图添加图例。
        """
        self._get_ax_by_tag(tag).legend(**kwargs)
        return self

    def set_suptitle(self, title: str, **kwargs):
        """
        为整个画布（Figure）设置一个主标题。
        """
        self.fig.suptitle(title, **kwargs)
        return self

    def fig_add_text(self, x: float, y: float, text: str, **kwargs) -> 'Plotter':
        """
        在整个画布（Figure）的指定位置添加文本。

        Args:
            x (float): 文本的X坐标，范围从0到1（图的左下角为(0,0)，右上角为(1,1)）。
            y (float): 文本的Y坐标，范围从0到1。
            text (str): 要添加的文本内容。
            **kwargs: 其他传递给 `matplotlib.figure.Figure.text` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        self.fig.text(x, y, text, **kwargs)
        return self

    def fig_add_line(self, x_coords: List[float], y_coords: List[float], **kwargs) -> 'Plotter':
        """
        在整个画布（Figure）上绘制一条线。

        Args:
            x_coords (List[float]): 线的X坐标列表，范围从0到1（图的左下角为(0,0)，右上角为(1,1)）。
            y_coords (List[float]): 线的Y坐标列表，范围从0到1。
            **kwargs: 其他传递给 `matplotlib.lines.Line2D` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        line = plt.Line2D(x_coords, y_coords, transform=self.fig.transFigure, **kwargs)
        self.fig.add_artist(line)
        return self

    def fig_add_box(self, tags: Union[str, int, List[Union[str, int]]], padding: float = 0.01, **kwargs) -> 'Plotter':
        """
        在整个画布（Figure）上，围绕一个或多个指定的子图绘制一个矩形框。

        Args:
            tags (Union[str, int, List[Union[str, int]]]): 
                一个或多个子图的tag，这些子图将被框选。
            padding (float, optional): 
                矩形框相对于子图边界的额外填充（以Figure坐标为单位）。默认为0.01。
            **kwargs: 其他传递给 `matplotlib.patches.Rectangle` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
        """
        self.fig.canvas.draw() # 强制重绘以获取准确的坐标

        if not isinstance(tags, list):
            tags = [tags]

        min_x, min_y, max_x, max_y = 1.0, 1.0, 0.0, 0.0

        for tag in tags:
            ax = self._get_ax_by_tag(tag)
            bbox = ax.get_position() # Bounding box in figure coordinates

            min_x = min(min_x, bbox.x0)
            min_y = min(min_y, bbox.y0)
            max_x = max(max_x, bbox.x1)
            max_y = max(max_y, bbox.y1)
        
        # Apply padding
        min_x -= padding
        min_y -= padding
        max_x += padding
        max_y += padding

        width = max_x - min_x
        height = max_y - min_y

        # Default kwargs for the rectangle
        kwargs.setdefault('facecolor', 'none')
        kwargs.setdefault('edgecolor', 'black')
        kwargs.setdefault('linewidth', 1.5)
        kwargs.setdefault('linestyle', '--')
        kwargs.setdefault('clip_on', False) # Ensure the box is drawn even if it slightly extends beyond figure limits

        rect = plt.Rectangle((min_x, min_y), width, height,
                             transform=self.fig.transFigure, **kwargs)
        self.fig.add_artist(rect)
        return self

    def _draw_fig_boundary_box(self, padding: float = 0.02, **kwargs):
        """
        [私有] 实际执行绘制画布边框的逻辑。
        """
        all_tags = list(self.tag_to_ax.keys())
        if not all_tags:
            return

        # Default kwargs for the boundary box
        kwargs.setdefault('facecolor', 'none')
        kwargs.setdefault('edgecolor', 'black')
        kwargs.setdefault('linewidth', 1)
        kwargs.setdefault('clip_on', False)
        
        # Re-use the logic from fig_add_box, but don't return self
        self.fig.canvas.draw()
        min_x, min_y, max_x, max_y = 1.0, 1.0, 0.0, 0.0
        for tag in all_tags:
            ax = self._get_ax_by_tag(tag)
            bbox = ax.get_position()
            min_x = min(min_x, bbox.x0)
            min_y = min(min_y, bbox.y0)
            max_x = max(max_x, bbox.x1)
            max_y = max(max_y, bbox.y1)

        min_x -= padding
        min_y -= padding
        max_x += padding
        max_y += padding

        width = max_x - min_x
        height = max_y - min_y

        rect = plt.Rectangle((min_x, min_y), width, height,
                             transform=self.fig.transFigure, **kwargs)
        self.fig.add_artist(rect)

    def fig_add_boundary_box(self, padding: float = 0.02, **kwargs) -> 'Plotter':
        """
        请求在整个画布（Figure）上，围绕所有子图的组合边界框绘制一个矩形边框。
        实际的绘制操作将延迟到调用 .save() 方法时执行，以确保所有其他元素都已就位。
        """
        self._draw_on_save_queue.append(
            {'func': self._draw_fig_boundary_box, 'kwargs': {'padding': padding, **kwargs}}
        )
        return self

    def fig_add_label(self, tags: Union[str, int, List[Union[str, int]]], text: str, position: str = 'top_left', padding: float = 0.01, **kwargs) -> 'Plotter':
        """
        在整个画布（Figure）上，相对于一个或多个指定的子图放置一个文本标签。

        Args:
            tags (Union[str, int, List[Union[str, int]]]): 
                一个或多个子图的tag，标签的位置将相对于这些子图的组合边界框。
            text (str): 要添加的标签文本内容。
            position (str, optional):
                标签相对于组合边界框的相对位置。
                可选值：'top_left', 'top_right', 'bottom_left', 'bottom_right', 
                        'center', 'top_center', 'bottom_center', 'left_center', 'right_center'。
                默认为 'top_left'。
            padding (float, optional): 
                标签文本与组合边界框之间的额外间距（以Figure坐标为单位）。默认为0.01。
            **kwargs: 其他传递给 `matplotlib.figure.Figure.text` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TagNotFoundError: 如果指定的tag未找到。
            ValueError: 如果`position`参数无效。
        """
        self.fig.canvas.draw() # 强制重绘以获取准确的坐标

        if not isinstance(tags, list):
            tags = [tags]

        min_x, min_y, max_x, max_y = 1.0, 1.0, 0.0, 0.0

        for tag in tags:
            ax = self._get_ax_by_tag(tag)
            bbox = ax.get_position() # Bounding box in figure coordinates

            min_x = min(min_x, bbox.x0)
            min_y = min(min_y, bbox.y0)
            max_x = max(max_x, bbox.x1)
            max_y = max(max_y, bbox.y1)
        
        # Calculate center and corners of the combined bounding box
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        x, y, ha, va = center_x, center_y, 'center', 'center' # Default to center

        if position == 'top_left':
            x, y, ha, va = min_x - padding, max_y + padding, 'right', 'bottom'
        elif position == 'top_right':
            x, y, ha, va = max_x + padding, max_y + padding, 'left', 'bottom'
        elif position == 'bottom_left':
            x, y, ha, va = min_x - padding, min_y - padding, 'right', 'top'
        elif position == 'bottom_right':
            x, y, ha, va = max_x + padding, min_y - padding, 'left', 'top'
        elif position == 'top_center':
            x, y, ha, va = center_x, max_y + padding, 'center', 'bottom'
        elif position == 'bottom_center':
            x, y, ha, va = center_x, min_y - padding, 'center', 'top'
        elif position == 'left_center':
            x, y, ha, va = min_x - padding, center_y, 'right', 'center'
        elif position == 'right_center':
            x, y, ha, va = max_x + padding, center_y, 'left', 'center'
        elif position == 'center':
            pass # Already default
        else:
            raise ValueError(f"Invalid position: {position}. Must be one of 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'center', 'top_center', 'bottom_center', 'left_center', 'right_center'.")

        kwargs.setdefault('ha', ha)
        kwargs.setdefault('va', va)
        kwargs.setdefault('fontsize', 12)
        kwargs.setdefault('weight', 'bold')

        self.fig.text(x, y, text, **kwargs)
        return self

    def add_global_legend(self, tags: list = None, remove_sub_legends: bool = True, **kwargs):
        """
        创建一个作用于整个画布的全局图例。
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
        """
        ax1 = self._get_ax_by_tag(tag)
        ax2 = ax1.twinx(**kwargs)
        return ax2

    def add_hline(self, tag: str, y: float, **kwargs) -> 'Plotter':
        """
        在指定子图上添加一条水平参考线。
        """
        ax = self._get_ax_by_tag(tag)
        ax.axhline(y, **kwargs)
        return self

    def add_vline(self, tag: str, x: float, **kwargs) -> 'Plotter':
        """
        在指定子图上添加一条垂直参考线。
        """
        ax = self._get_ax_by_tag(tag)
        ax.axvline(x, **kwargs)
        return self

    def add_text(self, tag: str, x: float, y: float, text: str, **kwargs) -> 'Plotter':
        """
        在指定子图的数据坐标系上添加文本。
        """
        ax = self._get_ax_by_tag(tag)
        ax.text(x, y, text, **kwargs)
        return self

    def add_patch(self, tag: str, patch_object) -> 'Plotter':
        """
        将一个Matplotlib的Patch对象添加到指定子图。
        """
        ax = self._get_ax_by_tag(tag)
        ax.add_patch(patch_object)
        return self

    def add_highlight_box(self, tag: Union[str, int], x_range: tuple[float, float], y_range: tuple[float, float], **kwargs) -> 'Plotter':
        """
        在指定子图上，根据数据坐标绘制一个高亮矩形区域。

        Args:
            tag (Union[str, int]): 目标子图的tag。
            x_range (tuple[float, float]): 高亮区域的X轴范围 (xmin, xmax)，使用数据坐标。
            y_range (tuple[float, float]): 高亮区域的Y轴范围 (ymin, ymax)，使用数据坐标。
            **kwargs: 其他传递给 `matplotlib.patches.Rectangle` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_ax_by_tag(tag)
        
        width = x_range[1] - x_range[0]
        height = y_range[1] - y_range[0]
        
        # 设置高亮框的默认样式
        kwargs.setdefault('facecolor', 'yellow')
        kwargs.setdefault('alpha', 0.3)
        kwargs.setdefault('edgecolor', 'none')
        kwargs.setdefault('zorder', 0) # 将高亮框置于底层

        rect = plt.Rectangle((x_range[0], y_range[0]), width, height, **kwargs)
        ax.add_patch(rect)
        return self

    def add_inset_image(self, host_tag: Union[str, int], image_path: str, rect: List[float], **kwargs) -> 'Plotter':
        """
        在指定子图内部嵌入一张图片。
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

    def hide_axes(self, x: bool = False, y: bool = False) -> 'Plotter':
        """
        隐藏所有子图的X轴或Y轴。
        """
        for ax in self.axes:
            if x:
                ax.get_xaxis().set_visible(False)
            if y:
                ax.get_yaxis().set_visible(False)
        return self

    def cleanup(self, share_y_on_rows: list[int] = None, share_x_on_cols: list[int] = None, align_labels: bool = True, auto_share: Union[bool, str] = False):
        """
        根据指定对行或列进行坐标轴共享和清理。
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

    def cleanup_heatmaps(self, tags: List[Union[str, int]]) -> 'Plotter':
        """
        为指定的一组热图创建共享的颜色条。
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

    def save(self, filename: str, **kwargs) -> None:
        """
        将当前图形保存到文件。
        在保存前，会先执行所有通过 `_draw_on_save_queue` 队列请求的延迟绘图操作。
        """
        # 执行所有延迟的绘图操作
        for task in self._draw_on_save_queue:
            task['func'](**task['kwargs'])
        
        # 清空队列
        self._draw_on_save_queue.clear()

        defaults = {'dpi': 300, 'bbox_inches': 'tight'}
        defaults.update(kwargs)
        self.fig.savefig(filename, **defaults)
        plt.close(self.fig)
        logger.info(f"Figure saved to {filename}")

from typing import Optional, Union, List, Dict
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class FigureAnnotationMixin:
    def set_suptitle(self, title: str, **kwargs) -> 'Plotter':
        """为整个画布（Figure）设置一个主标题。

        Args:
            title (str): 标题文本。
            **kwargs: 其他传递给 `fig.suptitle` 的参数 (e.g., fontsize, fontweight, y)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        self.fig.suptitle(title, **kwargs)
        return self

    def fig_add_text(self, x: float, y: float, text: str, **kwargs) -> 'Plotter':
        """在整个画布（Figure）的指定位置添加文本。

        Args:
            x (float): 文本的X坐标，范围从0到1（图的左下角为(0,0)，右上角为(1,1)）。
            y (float): 文本的Y坐标，范围从0到1。
            text (str): 要添加的文本内容。
            **kwargs: 其他传递给 `matplotlib.figure.Figure.text` 的关键字参数 (e.g., fontsize, color, ha, va)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        self.fig.text(x, y, text, **kwargs)
        return self

    def fig_add_line(self, x_coords: List[float], y_coords: List[float], **kwargs) -> 'Plotter':
        """在整个画布（Figure）上绘制一条线。

        Args:
            x_coords (List[float]): 线的X坐标列表，范围从0到1（图的左下角为(0,0)，右上角为(1,1)）。
            y_coords (List[float]): 线的Y坐标列表，范围从0到1。
            **kwargs: 其他传递给 `matplotlib.lines.Line2D` 的关键字参数 (e.g., linewidth, color, linestyle)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        line = plt.Line2D(x_coords, y_coords, transform=self.fig.transFigure, **kwargs)
        self.fig.add_artist(line)
        return self

    def fig_add_box(self, tags: Union[str, int, List[Union[str, int]]], padding: float = 0.01, **kwargs) -> 'Plotter':
        """在整个画布（Figure）上，围绕一个或多个指定的子图绘制一个矩形框。

        Args:
            tags (Union[str, int, List[Union[str, int]]]):
                一个或多个子图的tag，这些子图将被框选。
            padding (float, optional):
                矩形框相对于子图边界的额外填充（以Figure坐标为单位）。默认为0.01。
            **kwargs: 其他传递给 `matplotlib.patches.Rectangle` 的关键字参数 (e.g., edgecolor, facecolor, linestyle, linewidth)。

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
        """[私有] 实际执行绘制画布边框的逻辑。"""
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
        """请求在整个画布（Figure）上，围绕所有子图的组合边界框绘制一个矩形边框。 
        
        实际的绘制操作将延迟到调用 .save() 方法时执行，以确保所有其他元素都已就位。

        Args:
            padding (float, optional): 边框内边距。默认为 0.02。
            **kwargs: 其他传递给 `matplotlib.patches.Rectangle` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        self._draw_on_save_queue.append(
            {'func': self._draw_fig_boundary_box, 'kwargs': {'padding': padding, **kwargs}}
        )
        return self

    def _draw_fig_label(self, tags: Union[str, int, List[Union[str, int]]], text: str, position: str, padding: float, **kwargs):
        """[私有] 实际执行在画布上添加标签的逻辑。 此方法在 .save() 期间被调用。"""
        if not isinstance(tags, list):
            tags = [tags]

        min_x, min_y, max_x, max_y = 1.0, 1.0, 0.0, 0.0

        for tag in tags:
            ax = self._get_ax_by_tag(tag)
            bbox = ax.get_position()

            min_x = min(min_x, bbox.x0)
            min_y = min(min_y, bbox.y0)
            max_x = max(max_x, bbox.x1)
            max_y = max(max_y, bbox.y1)
        
        center_x, center_y = (min_x + max_x) / 2, (min_y + max_y) / 2
        x, y, ha, va = center_x, center_y, 'center', 'center'

        position_map = {
            'top_left': (min_x - padding, max_y + padding, 'right', 'bottom'),
            'top_right': (max_x + padding, max_y + padding, 'left', 'bottom'),
            'bottom_left': (min_x - padding, min_y - padding, 'right', 'top'),
            'bottom_right': (max_x + padding, min_y - padding, 'left', 'top'),
            'top_center': (center_x, max_y + padding, 'center', 'bottom'),
            'bottom_center': (center_x, min_y - padding, 'center', 'top'),
            'left_center': (min_x - padding, center_y, 'right', 'center'),
            'right_center': (max_x + padding, center_y, 'left', 'center'),
            'center': (center_x, center_y, 'center', 'center')
        }
        
        if position in position_map:
            x, y, ha, va = position_map[position]
        else:
            raise ValueError(f"Invalid position: {position}.")

        kwargs.setdefault('ha', ha)
        kwargs.setdefault('va', va)
        kwargs.setdefault('fontsize', 12)
        kwargs.setdefault('weight', 'bold')

        self.fig.text(x, y, text, **kwargs)

    def fig_add_label(self, tags: Union[str, int, List[Union[str, int]]], text: str, position: str = 'top_left', padding: float = 0.01, **kwargs) -> 'Plotter':
        """在整个画布（Figure）上，相对于一个或多个指定的子图放置一个文本标签。 
        
        注意：实际的绘制操作将延迟到调用 .save() 方法时执行，以确保布局计算的准确性。

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
        """
        draw_kwargs = {
            'tags': tags,
            'text': text,
            'position': position,
            'padding': padding,
            **kwargs
        }
        self._draw_on_save_queue.append(
            {'func': self._draw_fig_label, 'kwargs': draw_kwargs}
        )
        return self

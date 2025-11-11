# paperplot/mixins/modifiers.py

from typing import Optional, Union, List, Tuple
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import logging
import numpy as np
from adjustText import adjust_text
from collections import OrderedDict
logger = logging.getLogger(__name__)

class ModifiersMixin:
    """
    包含用于修改、装饰和收尾图表的方法的 Mixin 类。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #确保调用父类的__init__
        self._draw_on_save_queue = []

    def _to_roman(self, number: int) -> str:
        """将整数转换为罗马数字。"""
        if not 0 < number < 4000:
            # 对于超出范围的数字，可以返回空字符串或原始数字的字符串形式
            return str(number)
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "I", "IX", "V", "IV",
            "I"
        ]
        roman_num = ''
        i = 0
        while number > 0:
            for _ in range(number // val[i]):
                roman_num += syb[i]
                number -= val[i]
            i += 1
        return roman_num

    def _draw_subplot_label(self, fig: plt.Figure, ax: plt.Axes, text: str, position: Tuple[float, float], **kwargs):
        """
        [私有] 实际执行在子图上添加标签的逻辑。
        此方法在 .save() 期间被调用。
        """
        # 获取子图在画布坐标系中的最终位置
        transform = ax.transAxes + fig.transFigure.inverted()

        # 使用这个变换来计算标签在画布上的最终位置
        label_x, label_y = transform.transform(position)

        # 使用 fig.text 在计算出的画布坐标上绘制文本
        fig.text(label_x, label_y, text, **kwargs)

    def add_subplot_labels(
        self,
        tags: Optional[List[Union[str, int]]] = None,
        label_style: str = 'alpha',
        case: str = 'lower',
        template: str = '({label})',
        position: Tuple[float, float] = (-0.01, 1.01),
        start_at: int = 0,
        **text_kwargs
    ) -> 'Plotter':
        """
        为子图添加自动编号标签，如 (a), (b), (c)。
        注意：实际的绘制操作将延迟到调用 .save() 方法时执行，以确保布局计算的准确性。
        """
        # 1. 确定标注目标
        target_tags_or_names = []
        if tags is not None:
            target_tags_or_names = tags
        else:
            if isinstance(self.layout, dict):
                main_layout_def = self.layout.get('main', [])
                if main_layout_def:
                    unique_top_level_tags = OrderedDict.fromkeys(
                        tag for row in main_layout_def for tag in row if tag != '.'
                    )
                    target_tags_or_names = list(unique_top_level_tags.keys())
            elif isinstance(self.layout, list):
                unique_tags = OrderedDict()
                for r, row_list in enumerate(self.layout):
                    for c, tag in enumerate(row_list):
                        if tag != '.' and tag not in unique_tags:
                            unique_tags[tag] = (r, c)
                target_tags_or_names = list(unique_tags.keys())
            else:
                target_tags_or_names = list(self.axes_dict.keys())

        target_axes = []
        for tag in target_tags_or_names:
            try:
                ax = self._get_ax_by_tag(tag)
                if tags is None and ax not in self.plotted_axes:
                    continue
                target_axes.append(ax)
            except Exception:
                continue
        
        if not target_axes:
            logger.warning("No plotted axes found to label in auto mode.")
            return self

        # 2. 生成标签序列
        labels = []
        for i in range(len(target_axes)):
            num = i + start_at
            if label_style == 'alpha':
                label = chr(ord('a') + num)
            elif label_style == 'numeric':
                label = str(num + 1)
            elif label_style == 'roman':
                label = self._to_roman(num + 1)
            else:
                raise ValueError("label_style must be 'alpha', 'numeric', or 'roman'")
            
            if case == 'upper':
                label = label.upper()
            labels.append(label)

        # 3. 设置默认文本样式并与用户输入合并
        final_kwargs = {
            'fontsize': 14, 'weight': 'bold', 'ha': 'right', 'va': 'bottom',
        }
        final_kwargs.update(text_kwargs)

        # 4. 将绘图操作添加到队列
        for i, ax in enumerate(target_axes):
            label_text = template.format(label=labels[i])
            draw_kwargs = {
                'fig': self.fig,
                'ax': ax,
                'text': label_text,
                'position': position,
                **final_kwargs
            }
            self._draw_on_save_queue.append(
                {'func': self._draw_subplot_label, 'kwargs': draw_kwargs}
            )

        return self

    def add_grouped_labels(
        self,
        groups: "Dict[str, List[Union[str, int]]]",
        position: str = 'top_left',
        padding: float = 0.01,
        **text_kwargs
    ) -> 'Plotter':
        """
        为逻辑上分组的子图添加统一的标签。

        此方法利用 `fig_add_label` 的能力，计算多个子图的组合边界框，
        并将标签放置在该边界框的相对位置。

        Args:
            groups (Dict[str, List[Union[str, int]]]): 
                一个字典，其中键是标签文本（例如 `'(a)'`），
                值是属于该组的子图 `tag` 列表（例如 `['ax00', 'ax01']`）。
            position (str, optional): 
                标签相对于组合边界框的相对位置。
                默认为 'top_left'。
            padding (float, optional): 
                标签与组合边界框之间的间距。默认为 0.01。
            **text_kwargs: 
                其他传递给底层 `fig.text` 的关键字参数，
                用于定制文本样式，如 `fontsize`, `weight`, `color` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        for label_text, tags_in_group in groups.items():
            self.fig_add_label(
                tags=tags_in_group,
                text=label_text,
                position=position,
                padding=padding,
                **text_kwargs
            )
        return self


    def set_title(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图设置标题。

        Args:
            label (str): 标题文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.set_title` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_title(label, **kwargs)
        return self

    def set_xlabel(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图设置X轴标签。

        Args:
            label (str): X轴标签文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.set_xlabel` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_xlabel(label, **kwargs)
        return self

    def set_ylabel(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图设置Y轴标签。

        Args:
            label (str): Y轴标签文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.set_ylabel` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_ylabel(label, **kwargs)
        return self

    def set_zlabel(self, label: str, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的3D子图设置Z轴标签。

        Args:
            label (str): Z轴标签文本。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.set_zlabel` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        if ax.name != '3d':
            raise TypeError(f"Cannot set z-label for a non-3D axis. Axis '{self.last_active_tag}' is of type '{ax.name}'.")
        ax.set_zlabel(label, **kwargs)
        return self

    def view_init(self, elev: Optional[float] = None, azim: Optional[float] = None, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        设置3D子图的观察角度。

        Args:
            elev (Optional[float], optional): 仰角（绕x轴旋转）。
            azim (Optional[float], optional): 方位角（绕z轴旋转）。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        if ax.name != '3d':
            raise TypeError(f"Cannot set view angle for a non-3D axis. Axis '{self.last_active_tag}' is of type '{ax.name}'.")
        ax.view_init(elev=elev, azim=azim)
        return self

    def set_xlim(self, *args, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图设置X轴的显示范围。

        Args:
            *args: 同 `ax.set_xlim` 的位置参数 (例如 `(min, max)`)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.set_xlim` 的其他参数 (例如 `xmin=0, xmax=1`)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_xlim(*args, **kwargs)
        return self

    def set_ylim(self, *args, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图设置Y轴的显示范围。

        Args:
            *args: 同 `ax.set_ylim` 的位置参数 (例如 `(min, max)`)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.set_ylim` 的其他参数 (例如 `ymin=0, ymax=1`)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.set_ylim(*args, **kwargs)
        return self
        
    def tick_params(self, axis: str = 'both', tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图的刻度线、刻度标签和网格线设置参数。

        Args:
            axis (str, optional): 要操作的轴 ('x', 'y', 'both')。默认为 'both'。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.tick_params` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        ax = self._get_active_ax(tag)
        ax.tick_params(axis=axis, **kwargs)
        return self

    def set_legend(self, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图添加图例。
        此方法能够自动处理双Y轴（twinx）图，合并主轴和孪生轴的图例项。

        Args:
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.legend` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("No active plot to add a legend to. Please plot something first or specify a 'tag'.")

        # 1. 获取主轴并收集其图例项
        ax_primary = self._get_ax_by_tag(active_tag)
        h1, l1 = ax_primary.get_legend_handles_labels()

        # 2. 检查是否存在孪生轴，并收集其图例项
        h2, l2 = [], []
        if active_tag in self.twin_axes:
            ax_twin = self.twin_axes[active_tag]
            h2, l2 = ax_twin.get_legend_handles_labels()
            if ax_twin.get_legend():
                ax_twin.get_legend().remove() # 清理孪生轴上可能存在的旧图例

        # 3. 合并并使用 OrderedDict 去重
        handles = h1 + h2
        labels = l1 + l2
        if not handles: # 如果没有任何图例项，直接返回
            return self
            
        by_label = OrderedDict(zip(labels, handles))
        
        # 4. 在主轴上创建统一的图例
        ax_primary.legend(by_label.values(), by_label.keys(), **kwargs)
        
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

    def _draw_fig_label(self, tags: Union[str, int, List[Union[str, int]]], text: str, position: str, padding: float, **kwargs):
        """
        [私有] 实际执行在画布上添加标签的逻辑。
        此方法在 .save() 期间被调用。
        """
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
        """
        在整个画布（Figure）上，相对于一个或多个指定的子图放置一个文本标签。
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

    def add_twinx(self, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为指定或当前活动的子图创建一个共享X轴但拥有独立Y轴的“双Y轴”图，
        并切换Plotter的活动目标到新创建的孪生轴，以支持链式调用。

        Args:
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.twinx` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Warning:
            调用此方法后，Plotter会进入“孪生轴模式”。所有后续的绘图和修饰
            命令都将作用于新创建的孪生轴。若要返回操作主轴或切换到其他
            子图，必须显式调用 :meth:`target_primary` 方法。
        """
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("Cannot create twin axis: No active plot found.")
            
        if active_tag in self.twin_axes:
            raise ValueError(f"Tag '{active_tag}' already has a twin axis. Cannot create another one.")

        # 始终获取主轴，避免在孪生轴上创建孪生轴的错误
        ax1 = self._get_ax_by_tag(active_tag)
        ax2 = ax1.twinx(**kwargs)
        
        # 存储孪生轴并切换上下文
        self.twin_axes[active_tag] = ax2
        self.active_target = 'twin'
        
        return self

    def target_primary(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        将后续操作的目标切换回主坐标轴（primary axis）。

        Args:
            tag (Optional[Union[str, int]], optional): 
                如果提供，将确保 `last_active_tag` 指向该主轴，并切换上下文。
                如果为None，则只切换上下文到 'primary'。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        self.active_target = 'primary'
        if tag is not None:
            # 确保 last_active_tag 指向的是我们想操作的主轴
            # _get_ax_by_tag 会隐式校验tag存在性
            _ = self._get_ax_by_tag(tag) 
            self.last_active_tag = tag
        return self

    def target_twin(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        将后续操作的目标切换到孪生坐标轴（twin axis）。

        Args:
            tag (Optional[Union[str, int]], optional): 
                如果提供，将确保 `last_active_tag` 指向该主轴，并切换上下文。
                如果为None，则只切换上下文到 'twin'，使用当前的 `last_active_tag`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果在没有孪生轴的子图上尝试切换到 'twin' 模式。
        """
        self.active_target = 'twin'
        
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("Cannot switch to twin mode: No active plot found and no tag specified.")

        if active_tag not in self.twin_axes:
            raise ValueError(f"Cannot switch to twin mode for tag '{active_tag}': No twin axis found. Did you call add_twinx() first?")

        # 如果提供了 tag，更新 last_active_tag
        if tag is not None:
            # 确保 tag 对应的主轴存在
            _ = self._get_ax_by_tag(tag)
            self.last_active_tag = tag
            
        return self

    def add_hline(self, y: float, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        在指定或当前活动的子图上添加一条水平参考线。

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
        """
        在指定或当前活动的子图上添加一条垂直参考线。

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
        """
        在指定或当前活动的子图的数据坐标系上添加文本。

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
        """
        将一个Matplotlib的Patch对象添加到指定或当前活动的子图。

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
        """
        在指定或当前活动的子图上，根据数据坐标绘制一个高亮矩形区域。

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
        """
        在指定或当前活动的子图内部嵌入一张图片。

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

    def add_zoom_inset(self, rect: List[float], zoom_level: float = 2,
                       connector_locs: Optional[Tuple[int, int]] = (1, 2),
                       source_tag: Optional[Union[str, int]] = None,
                       inset_ax_kwargs: Optional[dict] = None,
                       mark_inset_kwargs: Optional[dict] = None) -> 'Plotter':
        """
        在指定或当前活动的子图上添加一个缩放指示（inset plot）。

        Args:
            rect (List[float]): 一个定义内嵌图位置和大小的列表 `[x, y, width, height]`，
                                坐标是相对于整个 Figure 的 (0到1)。
            zoom_level (float, optional): 缩放级别。默认为2。
            connector_locs (Optional[Tuple[int, int]], optional): 连接线的起始和结束位置，
                                                                  使用Matplotlib的loc代码 (例如 (1, 2) 表示右上角到左上角)。
                                                                  默认为 (1, 2)。
            source_tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            inset_ax_kwargs (Optional[dict]): 传递给 `zoomed_inset_axes` 的额外关键字参数。
            mark_inset_kwargs (Optional[dict]): 传递给 `mark_inset` 的额外关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
        source_ax = self._get_active_ax(source_tag)

        if inset_ax_kwargs is None:
            inset_ax_kwargs = {}
        if mark_inset_kwargs is None:
            mark_inset_kwargs = {}

        # Create the zoomed inset axes
        # loc='center' positions the inset_ax within the bbox_to_anchor rectangle
        # bbox_to_anchor and bbox_transform define the absolute position and size of the inset axes on the figure.
        inset_ax = zoomed_inset_axes(source_ax, zoom_level, loc='center',
                                     bbox_to_anchor=rect, bbox_transform=self.fig.transFigure,
                                     **inset_ax_kwargs)

        # Mark the region in the parent axes and draw connecting lines
        mark_inset(source_ax, inset_ax, loc1=connector_locs[0], loc2=connector_locs[1],
                   **mark_inset_kwargs)

        return self

    def hide_axes(self, tag: Optional[Union[str, int]] = None,
                  x_axis=False, y_axis=False,
                  x_ticks=False, y_ticks=False,
                  x_tick_labels=False, y_tick_labels=False,
                  x_label=False, y_label=False,
                  spines: List[str] = None) -> 'Plotter':
        """
        精细化地隐藏指定或当前活动子图的坐标轴元素。

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

    def add_peak_highlights(self, peaks_x: list, x_col: str, y_col: str,
                            label_peaks: bool = True, 
                            prefer_direction: str = 'up',
                            use_bbox: bool = True,
                            label_positions: dict = None,
                            tag: Optional[Union[str, int]] = None,
                            **kwargs) -> 'Plotter':
        """
        在一条已绘制的光谱或曲线上，自动高亮并（可选地）标注出特征峰的位置。
        使用 adjustText 库来避免标签重叠。

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
                
        if auto_texts:
            adjust_text(auto_texts, ax=ax, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
        
        return self

    def add_event_markers(self, event_dates: list, labels: list = None, 
                          use_bbox: bool = True, 
                          label_positions: dict = None,
                          tag: Optional[Union[str, int]] = None,
                          **kwargs) -> 'Plotter':
        """
        在时间序列图上标记重要的垂直事件。
        使用 adjustText 库来避免标签重叠。

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
        
        if auto_texts:
            adjust_text(auto_texts, ax=ax, arrowprops=dict(arrowstyle='->', color='red'))
        
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
        # 强制执行一次绘图，以确保所有布局都已最终确定
        self.fig.canvas.draw()

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

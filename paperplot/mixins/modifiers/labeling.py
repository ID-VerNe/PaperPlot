from typing import Optional, Union, List, Dict, Tuple
import matplotlib.pyplot as plt
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

class LabelingMixin:
    def _to_roman(self, number: int) -> str:
        """将整数转换为罗马数字。"""
        if not 0 < number < 4000:
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
        """[私有] 实际执行在子图上添加标签的逻辑。 此方法在 .save() 期间被调用。"""
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
        """为子图添加自动编号的标签，如 (a), (b), (c)。

        此方法会自动检测要标记的子图，并根据指定的样式生成标签。
        注意：实际的绘制操作将延迟到调用 `.save()` 方法时执行，
        以确保在最终布局上计算标签位置的准确性。

        Args:
            tags (Optional[List[Union[str, int]]], optional):
                要添加标签的子图 `tag` 列表。如果为 `None`，则会自动
                检测已绘图的子图并为其添加标签。默认为 `None`。
            label_style (str, optional): 标签的编号样式。
                可选值为 'alpha', 'numeric', 'roman'。默认为 'alpha'。
            case (str, optional): 标签的大小写 ('lower' 或 'upper')。
                对 'numeric' 样式无效。默认为 'lower'。
            template (str, optional): 格式化标签的模板字符串。
                默认为 '({label})'。
            position (Tuple[float, float], optional): 标签相对于每个子图
                左上角的位置，坐标系为 `ax.transAxes`。默认为 (-0.01, 1.01)。
            start_at (int, optional): 标签编号的起始数字（0-indexed）。
                例如，`start_at=0` 对应 'a', 1, 'I'。默认为 0。
            **text_kwargs: 其他传递给 `fig.text` 的关键字参数，
                             用于定制文本样式，如 `fontsize`, `weight`, `color`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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
        groups: Dict[str, List[Union[str, int]]],
        position: str = 'top_left',
        padding: float = 0.01,
        **text_kwargs
    ) -> 'Plotter':
        """为逻辑上分组的子图添加统一的标签。

        此方法计算多个子图的组合边界框，并将标签放置在该边界框的指定相对位置。
        这对于标记一个由多个子图组成的复合图非常有用。
        注意：实际的绘制操作将延迟到调用 `.save()` 方法时执行。

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

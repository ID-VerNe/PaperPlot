# paperplot/mixins/stats_modifiers.py

from typing import Optional, Union, List
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

def _p_to_stars(p_value: float) -> str:
    """[私有] 将p值转换为显著性星号。"""
    if p_value > 0.05:
        return 'ns'
    elif p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    return ''

class StatsModifiersMixin:
    """
    包含用于在图表上添加统计标注的 Mixin 类。
    """
    def add_stat_test(self, **kwargs) -> 'Plotter':
        """
        在两组数据之间自动进行统计检验，并在图上标注显著性。
        此方法会自动从缓存中获取当前子图使用的数据。

        Args:
            x (str): 分组变量的列名。
            y (str): 数值变量的列名。
            group1 (str): 第一个组的名称。
            group2 (str): 第二个组的名称。
            test (str, optional): 要执行的统计检验。
                                  可选值为 't-test_ind' (独立样本t检验) 
                                  和 'mannwhitneyu' (Mann-Whitney U检验)。
                                  默认为 't-test_ind'。
            text_offset (float, optional): 标注线与数据最高点之间的垂直距离比例。默认为 0.1。
            y_level (Optional[float], optional): 如果提供，则强制标注线和文本的y轴位置。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.plot` 和 `ax.text` 的额外参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 从 kwargs 中提取参数
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        group1 = kwargs.pop('group1')
        group2 = kwargs.pop('group2')
        test = kwargs.pop('test', 't-test_ind')
        text_offset = kwargs.pop('text_offset', 0.1)
        y_level = kwargs.pop('y_level', None)
        tag = kwargs.pop('tag', None)

        ax = self._get_active_ax(tag)
        active_tag = tag if tag is not None else self.last_active_tag
        
        if active_tag not in self.data_cache:
            raise ValueError(f"未能为子图 '{active_tag}' 找到缓存的数据。请确保在此方法前调用的绘图方法已缓存其数据。")
        
        data = self.data_cache[active_tag]

        group1_str = str(group1)
        group2_str = str(group2)

        # 提前构建标签到位置的映射和前置校验 (Bug 2 修复)
        # Get the positions of the categories on the x-axis
        # This is more robust for categorical axes than relying on xtick_labels.index
        x_tick_positions = ax.get_xticks()
        x_tick_labels_obj = ax.get_xticklabels()
        
        # Create a mapping from label text to its numerical position
        label_to_pos = {}
        for label, pos in zip(x_tick_labels_obj, x_tick_positions):
            text = str(label.get_text()) # Explicitly convert to string to ensure hashability
            label_to_pos[text] = pos

        # 显式的前置校验
        if group1_str not in label_to_pos:
            raise ValueError(
                f"组 '{group1_str}' 在X轴刻度标签中未找到。可用标签: {list(label_to_pos.keys())}"
            )
        if group2_str not in label_to_pos:
            raise ValueError(
                f"组 '{group2_str}' 在X轴刻度标签中未找到。可用标签: {list(label_to_pos.keys())}"
            )

        # 直接获取位置 (因为我们已经确认它们存在)
        x1_pos = label_to_pos[group1_str]
        x2_pos = label_to_pos[group2_str]

        # Ensure the column used for comparison is of a hashable type (e.g., string or category)
        # This is a defensive measure against potential issues with object dtypes containing lists
        comparison_col = data[x].astype(str) 

        data1 = data.loc[comparison_col == group1_str, y]
        data2 = data.loc[comparison_col == group2_str, y]

        if test == 't-test_ind':
            stat, p_value = stats.ttest_ind(data1, data2, equal_var=False) # Welch's t-test
        elif test == 'mannwhitneyu':
            stat, p_value = stats.mannwhitneyu(data1, data2)
        else:
            raise ValueError(f"未知的检验: {test}。可用检验为 't-test_ind' 和 'mannwhitneyu'。")

        p_text = _p_to_stars(p_value)
        if not p_text or p_text == 'ns':
            return self

        if y_level is None:
            y_max = max(data1.max(), data2.max())
            y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
            bar_y = y_max + y_range * text_offset
            text_y = bar_y + y_range * 0.02
        else:
            bar_y = y_level
            text_y = y_level + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02

        line_kwargs = {'color': 'black', 'lw': 1.5}
        line_kwargs.update(kwargs)
        ax.plot([x1_pos, x1_pos, x2_pos, x2_pos], [bar_y, text_y, text_y, bar_y], **line_kwargs)
        
        text_kwargs = {'ha': 'center', 'va': 'bottom', 'color': 'black'}
        text_kwargs.update(kwargs)
        ax.text((x1_pos + x2_pos) * 0.5, text_y, p_text, **text_kwargs)
        
        # 存储最新的Y位置，供 add_pairwise_tests 使用
        self._last_stat_y = text_y
        
        return self

    def add_pairwise_tests(self, **kwargs) -> 'Plotter':
        """
        执行多组统计比较，并在图上标注显著性，智能堆叠标注线。
        所有参数通过 `kwargs` 传入。

        Args:
            x (str): 分组变量的列名。
            y (str): 数值变量的列名。
            comparisons (list[tuple]): 一个列表，每个元素是一个包含两个组名的元组，例如 [('A', 'B'), ('A', 'C')]。
            test (str, optional): 要执行的统计检验。默认为 't-test_ind'。
            text_offset_factor (float, optional): 每层标注线之间的垂直间距比例。默认为 0.05。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `add_stat_test` 的额外参数。
        
        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 从 kwargs 中提取参数
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        comparisons = kwargs.pop('comparisons')
        test = kwargs.pop('test', 't-test_ind')
        text_offset_factor = kwargs.pop('text_offset_factor', 0.05)
        tag = kwargs.pop('tag', None)
        
        # 复制剩余的 kwargs，因为它们需要传递给 add_stat_test
        stat_test_kwargs = kwargs.copy()

        ax = self._get_active_ax(tag)
        active_tag = tag if tag is not None else self.last_active_tag
        
        if active_tag not in self.data_cache:
            raise ValueError(f"未能为子图 '{active_tag}' 找到缓存的数据。")
            
        data = self.data_cache[active_tag]
        
        all_groups_max_y = data.groupby(x)[y].max().max()
        y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
        
        current_y_level = all_groups_max_y + y_range * text_offset_factor

        for group1, group2 in comparisons:
            # 准备传递给 add_stat_test 的参数
            stat_test_params = {
                'x': x, 'y': y,
                'group1': group1, 'group2': group2,
                'test': test,
                'y_level': current_y_level,
                'tag': active_tag,
                **stat_test_kwargs
            }
            
            self.add_stat_test(**stat_test_params)
            
            # 更新下一个标注的Y位置
            if hasattr(self, '_last_stat_y'):
                current_y_level = self._last_stat_y + y_range * text_offset_factor
            else: # 如果上一个检验不显著，则保持相同level
                current_y_level += y_range * text_offset_factor

        # 调整y轴上限以容纳所有标注
        ax.set_ylim(top=current_y_level)
        
        # 清理临时变量
        if hasattr(self, '_last_stat_y'):
            del self._last_stat_y

        return self

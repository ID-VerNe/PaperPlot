# tests/test_stats_modifiers.py

import pytest
import pandas as pd
from paperplot import Plotter

def test_add_stat_test_raises_error_for_invalid_group():
    """测试 add_stat_test 在传入无效分组名时是否能正确抛出 ValueError， 并提供友好的错误信息。"""
    # 1. 准备数据和图表
    data = pd.DataFrame({
        'category': ['Group A', 'Group A', 'Group B', 'Group B'],
        'value': [1, 2, 3, 4]
    })
    # 使用 add_box 来确保 Matplotlib 已经设置了 X 轴刻度标签
    p = Plotter((1, 1))
    p.add_box(data=data, x='category', y='value')

    # 2. 使用 pytest.raises 捕获预期的异常
    # 匹配我们设计的错误信息模板
    with pytest.raises(ValueError, match="在X轴刻度标签中未找到"):
        # 3. 尝试使用一个无效的分组名调用方法
        p.add_stat_test(
            x='category', 
            y='value',
            group1='Group A',
            group2='Group C' # 'Group C' does not exist
        )

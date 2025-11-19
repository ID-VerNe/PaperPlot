import pytest
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import paperplot as pp
from paperplot import Plotter
import pandas as pd
import numpy as np
import os

# Helper function to save and check if file exists
def save_and_check(plotter, tmp_path, test_name):
    filepath = tmp_path / f"{test_name}.png"
    plotter.save(str(filepath))
    assert filepath.exists()
    plt.close(plotter.fig)

def test_add_subplot_labels_mosaic_auto(tmp_path):
    """测试 add_subplot_labels 在马赛克布局下的自动标注 (FR2)。"""
    layout = [['A', 'A', 'B'], ['C', 'C', 'C']]
    plotter = Plotter(layout=layout)

    # 绘制一些内容，确保 axes 被标记为 plotted_axes
    plotter.add_line(data=pd.DataFrame({'x':[1,2], 'y':[1,2]}), x='x', y='y', tag='A')
    plotter.add_line(data=pd.DataFrame({'x':[1,2], 'y':[1,2]}), x='x', y='y', tag='B')
    plotter.add_line(data=pd.DataFrame({'x':[1,2], 'y':[1,2]}), x='x', y='y', tag='C')

    plotter.add_subplot_labels(fontsize=16, weight='bold')

    # 验证标签是否被添加
    ax_a = plotter.get_ax('A')
    ax_b = plotter.get_ax('B')
    ax_c = plotter.get_ax('C')

    # 检查 A, B, C 是否有标签
    # 标签位置 (-0.1, 1.1) 是相对于轴的坐标，所以文本对象应该在轴的 transform 下
    # 并且文本内容应该是 (a), (b), (c)
    assert any(t.get_text() == '(a)' for t in ax_a.texts)
    assert any(t.get_text() == '(b)' for t in ax_b.texts)
    assert any(t.get_text() == '(c)' for t in ax_c.texts)

    # 检查样式是否应用
    label_a = next(t for t in ax_a.texts if t.get_text() == '(a)')
    assert label_a.get_fontsize() == 16
    assert label_a.get_weight() == 'bold'

    save_and_check(plotter, tmp_path, "test_mosaic_auto_labels")

def test_add_grouped_labels(tmp_path):
    """测试 add_grouped_labels (FR3)。"""
    plotter = Plotter(layout=(2, 3)) # 包含 ax00, ax01, ..., ax12

    # 绘制一些内容，确保 axes 被标记为 plotted_axes
    for r in range(2):
        for c in range(3):
            tag = f'ax{r}{c}'
            plotter.add_line(data=pd.DataFrame({'x':[1,2], 'y':[1,2]}), x='x', y='y', tag=tag)

    groups = {
        '(a)': ['ax00', 'ax01'],
        '(b)': ['ax02'],
        '(c)': ['ax10', 'ax11', 'ax12']
    }
    plotter.add_grouped_labels(groups=groups, position='top_left', padding=0.02, fontsize=18, color='blue')

    # 验证标签是否被添加
    # 对于 (a) 组
    # fig_add_label 会在 figure 级别添加文本，所以我们需要检查 fig.texts
    fig_texts = [t for t in plotter.fig.texts if t.get_text() in ['(a)', '(b)', '(c)']]
    
    assert any(t.get_text() == '(a)' for t in fig_texts)
    assert any(t.get_text() == '(b)' for t in fig_texts)
    assert any(t.get_text() == '(c)' for t in fig_texts)

    # 检查样式是否应用
    label_a = next(t for t in fig_texts if t.get_text() == '(a)')
    assert label_a.get_fontsize() == 18
    assert label_a.get_color() == 'blue'

    save_and_check(plotter, tmp_path, "test_grouped_labels")


import pytest
import pandas as pd
import matplotlib.pyplot as plt
from paperplot import Plotter
import os

def test_categorical_bar_fix():
    """验证 add_bar 的 categorical=True 修复。
    如果不强制转换为 str，数值型 X 轴可能导致柱子消失或坐标轴异常。
    """
    data = pd.DataFrame({
        'year': [2020, 2021, 2022],
        'value': [10, 20, 15]
    })
    
    # 默认应该启用 categorical=True
    plotter = Plotter(layout=(1, 1))
    plotter.add_bar(data=data, x='year', y='value')
    
    ax = plotter.get_ax(1)
    # 检查 tick labels 是否被设为字符串
    # Matplotlib 在绘图后会更新 ticks
    plotter.fig.canvas.draw()
    labels = [t.get_text() for t in ax.get_xticklabels()]
    # 去除空标签（matplotlib 可能会生成额外的空标签）
    labels = [l for l in labels if l]
    
    assert '2020' in labels
    assert '2021' in labels
    assert '2022' in labels
    
    plt.close(plotter.fig)

if __name__ == "__main__":
    test_categorical_bar_fix()

import numpy as np
import pandas as pd

import paperplot as pp

heatmap_data_1 = pd.DataFrame(np.random.rand(8, 50))
heatmap_data_2 = pd.DataFrame(np.random.rand(8, 50))
heatmap_data_3 = pd.DataFrame(np.random.rand(8, 50))

heatmap_data_4 = pd.DataFrame(np.random.rand(8, 50))
heatmap_data_5 = pd.DataFrame(np.random.rand(8, 50))
heatmap_data_6 = pd.DataFrame(np.random.rand(8, 50))

df_line_1_1 = pd.DataFrame({'x': np.linspace(0, 2 * np.pi, 100), 'y': np.sin(np.linspace(0, 2 * np.pi, 100))})

df_line_1_2 = pd.DataFrame({'x': np.linspace(0, 2 * np.pi, 100), 'y': np.sin(np.linspace(0, 2 * np.pi, 100))})

df_line_2_1 = pd.DataFrame({'x': np.linspace(0, 2 * np.pi, 100), 'y': np.cos(np.linspace(0, 2 * np.pi, 100))})

df_line_2_2 = pd.DataFrame({'x': np.linspace(0, 2 * np.pi, 100), 'y': np.cos(np.linspace(0, 2 * np.pi, 100))})

nested_layout = {  # 'main' 定义了顶层 1x2 布局
    'main': [['A', 'B', 'C', 'D'],
             ['E', 'F', 'F', 'F'],
             ['I', 'J', 'K', 'L'],
             ],  # 'subgrids' 定义了 'heatmap_group' 区域如何被再次划分
    'subgrids': {'A': {  # 'layout' 定义了 3x1 的内部网格，并为每个单元命名
        'layout': [['a1'], ['a2'], ['a3']],  # 'hspace' 控制这个子网格内部的垂直间距，使其紧凑
        'hspace': 0.05}, 'B': {'layout': [['b1'], ['b2'], ['b3']], 'hspace': 0.05}}}

y_labels = ['~NH2', 'v(C-N-C)', 'v(C-C)ring']

plotter = pp.Plotter(layout=nested_layout, layout_engine=None, subplot_aspect=(4, 3))
plotter.set_suptitle("Declarative Nested Layout Example", fontsize=16, weight='bold')

plotter.add_heatmap(data=heatmap_data_1, tag="A.a1").set_ylabel(y_labels[0])
plotter.add_heatmap(data=heatmap_data_2, tag="A.a2").set_ylabel(y_labels[1])
plotter.add_heatmap(data=heatmap_data_3, tag="A.a3").set_ylabel(y_labels[2])

plotter.add_heatmap(data=heatmap_data_4, tag="B.b1").set_ylabel(y_labels[0])
plotter.add_heatmap(data=heatmap_data_5, tag="B.b2").set_ylabel(y_labels[1])
plotter.add_heatmap(data=heatmap_data_6, tag="B.b3").set_ylabel(y_labels[2])

plotter.hide_axes(tag="A.a1", x_ticks=True, x_tick_labels=True, y_ticks=True, y_tick_labels=True)
plotter.hide_axes(tag="A.a2", x_ticks=True, x_tick_labels=True, y_ticks=True, y_tick_labels=True)
plotter.hide_axes(tag="A.a3", x_ticks=True, x_tick_labels=True, y_ticks=True, y_tick_labels=True)

plotter.set_xlabel(label='Time (min)', tag='A.a3', fontsize=14, weight='bold')

plotter.hide_axes(tag="B.b1", x_ticks=True, x_tick_labels=True, y_ticks=True, y_tick_labels=True)
plotter.hide_axes(tag="B.b2", x_ticks=True, x_tick_labels=True, y_ticks=True, y_tick_labels=True)
plotter.hide_axes(tag="B.b3", x_ticks=True, x_tick_labels=True, y_ticks=True, y_tick_labels=True)

plotter.set_xlabel(label='Time (min)', tag='B.b3', fontsize=14, weight='bold')

plotter.add_line(data=df_line_1_1, x='x', y='y', tag='C', label='sin(x)')
plotter.add_twinx()
plotter.add_line(data=df_line_1_2, x='x', y='y', label='sin(x)').target_primary()

plotter.add_line(data=df_line_2_1, x='x', y='y', tag='D', label='cos(x)')
plotter.add_twinx()
plotter.add_line(data=df_line_2_2, x='x', y='y', label='cos(x)').target_primary()

plotter.add_line(data=df_line_2_1, x='x', y='y', tag='E', label='cos(x)')
plotter.add_line(data=df_line_2_1, x='x', y='y', tag='F', label='cos(x)')

plotter.add_line(data=df_line_2_1, x='x', y='y', tag='I', label='cos(x)')
plotter.add_line(data=df_line_2_1, x='x', y='y', tag='J', label='cos(x)')
plotter.add_line(data=df_line_2_1, x='x', y='y', tag='K', label='cos(x)')
plotter.add_line(data=df_line_2_1, x='x', y='y', tag='L', label='cos(x)')

plotter.fig.tight_layout(pad=1.1)

groups = {
    '(a)': ['A.a1', 'A.a2', 'A.a3', 'B.b1', 'B.b2', 'B.b3'],
    '(b)': ['C', 'D'],
    '(c)': ['E'],
    '(d)': ['F'],
    '(e)': ['I', 'J', 'K'],
    '(f)': ['L']
}
plotter.add_grouped_labels(groups=groups, position='top_left', fontsize=16)

plotter.save("layout_example.png")

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
cats = ['A', 'B', 'C']
df_bar = pd.DataFrame({
    'cat': cats,
    's1': [1, 3, 2],
    's2': [2, 2, 3],
    's3': [0, 1, 2]
})

df_line = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y1': [1, 2, 3, 4],
    'y2': [2, 1, 3, 2]
})

df_pie = pd.DataFrame({'sizes': [3, 2, 5]})
df_donut = df_pie.copy()
df_nested_inner = pd.DataFrame({'sizes': [2, 3]})

df_waterfall = pd.DataFrame({
    'x': ['start', 'a', 'b', 'c'],
    'deltas': [10, -3, 5, -2]
})

df_kline = pd.DataFrame({
    't': ['t1', 't2', 't3', 't4'],
    'open': [10, 12, 11, 13],
    'high': [12, 13, 12, 14],
    'low': [9, 11, 10, 12],
    'close': [11, 11, 12, 12]
})

theta = np.linspace(0, 2 * np.pi, 10)
r = np.linspace(1, 10, 10)
df_polar = pd.DataFrame({'theta': theta, 'r': r})

try:
    # 布局：3行4列，包含10种图示例
    layout = [
        ['GB', 'ML', 'SB', 'WF'],
        ['PIE', 'DONUT', 'ND', 'K'],
        ['POLAR', '.', '.', '.']
    ]

    plotter = pp.Plotter(
        layout=layout,
        figsize=(14, 10),
        ax_configs={'POLAR': {'projection': 'polar'}}
    )

    plotter.set_suptitle("Basic Chart Types", fontsize=16, weight='bold')

    # 1. 多系列柱状图
    plotter.add_grouped_bar(
        data=df_bar, x='cat', ys=['s1', 's2', 's3'], labels={'s1': 'Series 1', 's2': 'Series 2', 's3': 'Series 3'}, tag='GB'
    ).set_title('Grouped Bar', tag='GB').set_legend('GB')

    # 2. 多线折线图
    plotter.add_multi_line(
        data=df_line, x='x', ys=['y1', 'y2'], labels={'y1': 'Line A', 'y2': 'Line B'}, tag='ML'
    ).set_title('Multi-Line', tag='ML').set_legend('ML')

    # 3. 堆叠柱状图
    plotter.add_stacked_bar(
        data=df_bar, x='cat', ys=['s1', 's2', 's3'], labels={'s1': 'Part 1', 's2': 'Part 2', 's3': 'Part 3'}, tag='SB'
    ).set_title('Stacked Bar', tag='SB').set_legend('SB')

    # 4. 阶梯瀑布图
    plotter.add_waterfall(
        data=df_waterfall, x='x', deltas='deltas', tag='WF'
    ).set_title('Waterfall', tag='WF')

    # 5. 饼图
    plotter.add_pie(
        data=df_pie, sizes='sizes', labels=['X', 'Y', 'Z'], tag='PIE'
    ).set_title('Pie', tag='PIE')

    # 6. 环形图
    plotter.add_donut(
        data=df_donut, sizes='sizes', labels=['X', 'Y', 'Z'], width=0.4, radius=1.0, tag='DONUT'
    ).set_title('Donut', tag='DONUT')

    # 7. 嵌套环形图
    plotter.add_nested_donut(
        outer={'data': df_donut, 'sizes': 'sizes', 'labels': ['X', 'Y', 'Z']},
        inner={'data': df_nested_inner, 'sizes': 'sizes', 'labels': ['I1', 'I2']},
        tag='ND'
    ).set_title('Nested Donut', tag='ND')

    # 8. K 线图
    plotter.add_candlestick(
        data=df_kline, time='t', open='open', high='high', low='low', close='close', tag='K'
    ).set_title('Candlestick', tag='K')

    # 9. 极坐标柱状图
    plotter.add_polar_bar(
        data=df_polar, theta='theta', r='r', tag='POLAR'
    ).set_title('Polar Bar', tag='POLAR')

    # 收尾与保存
    plotter.cleanup(align_labels=True)
    plotter.save("chart_types_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'chart_types_example.png' was generated.")

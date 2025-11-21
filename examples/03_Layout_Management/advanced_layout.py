# examples/advanced_layout_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
def generate_data(num_points, scale=1, offset=0):
    return pd.DataFrame({
        'x': np.arange(num_points),
        'y': np.sin(np.arange(num_points) / (num_points / 10)) * scale + np.random.randn(num_points) * 0.2 + offset
    })

# --- 2. 定义一个跨列的复杂布局 ---
# 我们想要一个2x3的网格，但第一行的第二个图要占据2个列的位置
# 我们用字母'B'重复出现来表示它跨越了多个格子
layout = [
    ['A', 'B', 'B'],
    ['C', 'D', 'E']
]

# --- 3. 使用新布局初始化Plotter ---
try:
    print(f"Creating a plot with a complex layout: {layout}")
    # 注意，我们现在直接将layout列表传给Plotter
    plotter = pp.Plotter(layout=layout, figsize=(12, 6))

    # --- 4. 在跨列的“大图”B上绘图 ---
    print("Drawing on the spanning plot 'B'...")
    # a. 通过名字 'B' 获取目标ax
    ax_b = plotter.get_ax_by_name('B')
    # b. 使用 ax 参数指定在该ax上绘图
    plotter.add_line(data=generate_data(200), x='x', y='y', ax=ax_b, tag='spanning_plot'
    ).set_title('Plot B (Spanning two columns)')

    # --- 5. 在其他子图上顺序绘图 ---
    # Plotter会自动按 A, C, D, E 的顺序填充剩下的格子
    print("Drawing sequentially on the remaining plots...")
    plotter.add_scatter(data=generate_data(50), x='x', y='y', tag='plot_A'
    ).set_title('Plot A')

    plotter.add_scatter(data=generate_data(50, offset=2), x='x', y='y', tag='plot_C'
    ).set_title('Plot C')

    plotter.add_scatter(data=generate_data(50, offset=4), x='x', y='y', tag='plot_D'
    ).set_title('Plot D')

    plotter.add_scatter(data=generate_data(50, offset=6), x='x', y='y', tag='plot_E'
    ).set_title('Plot E')

    # --- 6. 演示 hide_axes() 功能 ---
    # 为了让布局更紧凑，我们隐藏所有X轴
    print("Hiding all X-axes using hide_axes(x_axis=True)...")
    plotter.hide_axes(x_axis=True, y_axis=True)

    # --- 7. 保存图像 ---
    plotter.save("advanced_layout_figure.png")

except (pp.PaperPlotError, ValueError) as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'advanced_layout_figure.png' was generated.")

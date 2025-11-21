# examples/row_span_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
def generate_data(num_points, scale=1, offset=0):
    return pd.DataFrame({
        'x': np.linspace(0, 100, num_points),
        'y': np.random.randn(num_points).cumsum() * scale + offset
    })

# --- 2. 定义一个跨行的复杂布局 ---
# 我们想要一个2x3的网格，其中第一列的图'A'要跨越两行
layout = [
    ['A', 'B', 'C'],
    ['A', 'D', 'E']
]

# --- 3. 使用新布局初始化Plotter ---
try:
    print(f"Creating a plot with a row-spanning layout: {layout}")
    plotter = pp.Plotter(layout=layout, figsize=(10, 6))

    # --- 4. 在跨行的“大图”A上绘图 ---
    print("Drawing on the row-spanning plot 'A'...")
    ax_A = plotter.get_ax_by_name('A')
    plotter.add_line(data=generate_data(200, scale=5), x='x', y='y', ax=ax_A, tag='spanning_plot'
    ).set_title('Plot A (Spanning two rows)'
    ).set_ylabel('Value')

    # --- 5. 在其他子图上顺序绘图 ---
    # Plotter会自动按 B, C, D, E 的顺序填充剩下的格子
    print("Drawing sequentially on the remaining plots...")
    plotter.add_scatter(data=generate_data(50), x='x', y='y', tag='plot_B'
    ).set_title('Plot B')

    plotter.add_scatter(data=generate_data(50, offset=20), x='x', y='y', tag='plot_C'
    ).set_title('Plot C')

    plotter.add_scatter(data=generate_data(50, offset=40), x='x', y='y', tag='plot_D'
    ).set_title('Plot D'
    ).set_xlabel('Index') # 只在底部的图上加x标签

    plotter.add_scatter(data=generate_data(50, offset=60), x='x', y='y', tag='plot_E'
    ).set_title('Plot E'
    ).set_xlabel('Index')

    # --- 6. 使用cleanup来美化布局 ---
    # 共享B和C的Y轴，D和E的Y轴，以及上下对应的X轴
    plotter.cleanup(share_y_on_rows=[0, 1], share_x_on_cols=[1, 2])

    # --- 7. 保存图像 ---
    plotter.save("row_span_figure.png")

except (pp.PaperPlotError, ValueError) as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'row_span_figure.png' was generated.")

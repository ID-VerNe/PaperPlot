# examples/block_span_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
def generate_heatmap_data(vmin, vmax, size=20):
    return pd.DataFrame(np.random.rand(size, size) * (vmax - vmin) + vmin)

def generate_line_data(num_points):
    return pd.DataFrame({
        'x': np.arange(num_points),
        'y': np.random.randn(num_points).cumsum()
    })

# --- 2. 定义一个块区域跨越的复杂布局 ---
# 我们想要一个2x3的网格，其中左侧是一个2x2的大图'A'
# 右侧是两个独立的图'B'和'C'
layout = [
    ['A', 'A', 'B'],
    ['A', 'A', 'C']
]

# --- 3. 使用新布局初始化Plotter ---
try:
    print(f"Creating a plot with a block-spanning layout: {layout}")
    plotter = pp.Plotter(layout=layout, figsize=(10, 6))

    # --- 4. 在跨2x2区域的“大图”A上绘制热图 ---
    print("Drawing a heatmap on the 2x2 spanning plot 'A'...")
    ax_A = plotter.get_ax_by_name('A')
    # 对于热图，我们让它自己生成一个颜色条，因为它不与别的图共享
    plotter.add_heatmap(data=generate_heatmap_data(0, 20), ax=ax_A, tag='main_heatmap', cbar=True)
    plotter.set_title('main_heatmap', 'Plot A (2x2 Span)')

    # --- 5. 在右侧的B和C上顺序绘图 ---
    # Plotter会自动按 B, C 的顺序填充剩下的格子
    print("Drawing sequentially on the remaining plots 'B' and 'C'...")
    plotter.add_line(data=generate_line_data(100), x='x', y='y', tag='plot_B')
    plotter.set_title('plot_B', 'Plot B')

    plotter.add_line(data=generate_line_data(100), x='x', y='y', tag='plot_C')
    plotter.set_title('plot_C', 'Plot C')

    # --- 6. 使用cleanup来美化布局 ---
    # 共享B和C的X轴
    plotter.cleanup(share_x_on_cols=[2])

    # --- 7. 保存图像 ---
    plotter.save("block_span_figure.png")

except (pp.PaperPlotError, ValueError) as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'block_span_figure.png' was generated.")

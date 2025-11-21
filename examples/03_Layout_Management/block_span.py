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
layout = [
    ['A', 'A', 'B'],
    ['A', 'A', 'C']
]

# --- 3. 使用新布局初始化Plotter ---
try:
    print(f"Creating a plot with a block-spanning layout: {layout}")
    plotter = pp.Plotter(layout=layout, figsize=(10, 6))

    # --- 4. 在跨2x2区域的“大图”A上绘制热图 ---
    # 使用布局中定义的tag 'A' 来指定位置
    print("Drawing a heatmap on the 2x2 spanning plot 'A'...")
    plotter.add_heatmap(
        data=generate_heatmap_data(0, 20),
        tag='A',  # <--- 使用布局中的tag 'A'
        cbar=True
    ).set_title('Plot A (2x2 Span)')

    # --- 5. 在右侧的B和C上绘图 ---
    # 同样，使用布局中定义的tag 'B' 和 'C'
    print("Drawing on plots 'B' and 'C' using their layout tags...")
    plotter.add_line(
        data=generate_line_data(100),
        x='x',
        y='y',
        tag='B'  # <--- 使用布局中的tag 'B'
    ).set_title('Plot B')

    plotter.add_line(
        data=generate_line_data(100),
        x='x',
        y='y',
        tag='C'  # <--- 使用布局中的tag 'C'
    ).set_title('Plot C')

    # --- 6. 使用cleanup来美化布局 ---
    # 这里的逻辑也需要调整，因为 'B' 和 'C' 不在同一列
    # 如果想共享B和C的X轴，可以这样做，但它们是对齐的，可能不需要
    # plotter.get_ax_by_name('C').sharex(plotter.get_ax_by_name('B'))
    # plotter.hide_axes(tag='B', x_tick_labels=True) # 如果共享，隐藏上面图的x刻度标签

    # 由于它们在同一列，我们可以直接对这一列进行操作
    # 在这个布局中，B和C在第2列 (索引从0开始)
    # 但是，由于'A'跨越了0和1列，所以'B'和'C'实际上在第2列
    # Matplotlib的GridSpec会将'A'放在(0,0)，'B'放在(0,2)，'C'放在(1,2)
    # 因此它们不在同一列，不能用share_x_on_cols
    # 我们需要手动共享
    ax_b = plotter.get_ax('B')
    ax_c = plotter.get_ax('C')
    ax_c.sharex(ax_b)
    plotter.hide_axes(tag='B', x_tick_labels=True)
    plotter.set_xlabel("", tag='B') # 移除B的x轴标签

    # --- 7. 保存图像 ---
    plotter.save("block_span_figure.png")

except (pp.PaperPlotError, ValueError) as e:
    import traceback
    print(f"\nA PaperPlot error occurred:\n{e}")
    traceback.print_exc()
except Exception as e:
    import traceback
    print(f"An unexpected error occurred: {e}")
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'block_span_figure.png' was generated.")
# examples/global_controls_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
def generate_data(label):
    x = np.linspace(0, 10, 40)
    y = np.sin(x + np.random.rand() * 5) * np.random.rand() + np.random.randn(40) * 0.1
    return pd.DataFrame({'x': x, 'y': y, 'label': label})

df1 = generate_data('Series A')
df2 = generate_data('Series B')
df3 = generate_data('Series C')
df4 = generate_data('Series D')

# --- 2. 创建一个2x2的简单网格 ---
try:
    # 使用 (2, 2) 元组来创建一个简单的2x2布局
    plotter = pp.Plotter(layout=(2, 2), figsize=(10, 8))

    # --- 3. 填充图表 ---
    # 注意我们为每条线都设置了label，以便全局图例能收集到它们
    plotter.add_line(data=df1, x='x', y='y', tag='tl', label='Series A', color='blue').set_title('Top-Left Plot')
    plotter.add_line(data=df2, x='x', y='y', tag='tr', label='Series B', color='red').set_title('Top-Right Plot')
    plotter.add_line(data=df3, x='x', y='y', tag='bl', label='Series C', color='green').set_title('Bottom-Left Plot')
    plotter.add_line(data=df4, x='x', y='y', tag='br', label='Series D', color='purple').set_title('Bottom-Right Plot')

    # --- 4. 使用新的全局控制功能 ---
    
    # a. 设置一个全局主标题
    print("Setting a global suptitle...")
    plotter.set_suptitle("Global Figure Title (Suptitle)", fontsize=20, weight='bold')

    # c. 创建一个全局图例
    # 它会自动收集所有子图的'label'，并移除子图自身的图例
    print("Adding a global legend...")
    plotter.add_global_legend(loc='upper right')

    # d. 使用增强的cleanup功能
    # 我们共享所有行和列的轴，并确保标签对齐
    print("Running cleanup with label alignment...")
    plotter.cleanup(share_y_on_rows=[0, 1], share_x_on_cols=[0, 1], align_labels=True)

    # --- 5. 保存图像 ---
    plotter.save("global_controls_figure.png")

except (pp.PaperPlotError, ValueError) as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'global_controls_figure.png' was generated.")

# examples/heatmap_colorbar_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备三组数据范围不同的热图数据 ---
def generate_heatmap_data(vmin, vmax, size=5):
    return pd.DataFrame(np.random.rand(size, size) * (vmax - vmin) + vmin)

df1 = generate_heatmap_data(0, 10)
df2 = generate_heatmap_data(5, 15)
df3 = generate_heatmap_data(-5, 5)

# --- 2. 演示共享颜色条功能 ---
try:
    print("Creating 3 heatmaps with a shared colorbar...")
    plotter = pp.Plotter(layout=(1, 3), figsize=(12, 4))

    # --- 3. 添加热图，并明确指定 cbar=False ---
    # 这是关键一步：我们告诉plotter不要为每个热图单独创建颜色条
    plotter.add_heatmap(data=df1, tag='h1', cbar=False, annot=True, fmt='.0f').set_title('Range 0-10')
    plotter.add_heatmap(data=df2, tag='h2', cbar=False, annot=True, fmt='.0f').set_title('Range 5-15')
    plotter.add_heatmap(data=df3, tag='h3', cbar=False, annot=True, fmt='.0f').set_title('Range -5-5')

    # --- 5. 调用 cleanup_heatmaps 来创建共享颜色条 ---
    # 函数会自动找到所有热图的全局数据范围 (-5 到 15)
    # 并创建一个能代表这个全局范围的颜色条
    plotter.cleanup_heatmaps(tags=['h1', 'h2', 'h3'])
    
    # 我们也可以顺便清理一下Y轴，让它们对齐
    plotter.cleanup(share_y_on_rows=[0])

    # --- 6. 保存图像 ---
    plotter.save("heatmap_shared_colorbar_figure.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

# --- 7. 作为对比，创建一个带独立颜色条的热图 ---
try:
    print("\nCreating a single heatmap with its own colorbar (default behavior)...")
    plotter_single = pp.Plotter(layout=(1, 1))
    # 默认调用，不加 cbar 参数，会自动创建颜色条
    plotter_single.add_heatmap(data=df1, tag='single').set_title('Default Behavior with cbar=True')
    plotter_single.save("heatmap_default_figure.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
finally:
    plt.close('all')


print(f"\n--- Finished Example: {__file__} ---")
print("Two files were generated: 'heatmap_shared_colorbar_figure.png' and 'heatmap_default_figure.png'")

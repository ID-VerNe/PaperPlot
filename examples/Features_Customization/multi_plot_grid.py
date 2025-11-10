# examples/multi_plot_grid.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from paperplot import Plotter

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备多样化的数据 ---
# Scatter plot data
df_scatter = pd.DataFrame({
    'x_val': np.random.rand(50) * 10,
    'y_val': np.random.rand(50) * 10,
    'size': np.random.rand(50) * 100
})

# Bar plot data
df_bar = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'mean': [15, 22, 18, 25],
    'std': [2, 3, 2.5, 4]
})

# Line plot data
df_line = pd.DataFrame({
    'time': np.linspace(0, 10, 50),
    'signal': np.cos(np.linspace(0, 10, 50)) + np.random.randn(50) * 0.1
})

# Heatmap data
heatmap_data = np.random.rand(10, 10)
df_heatmap = pd.DataFrame(heatmap_data, columns=[f'col_{i}' for i in range(10)])

# --- 2. 初始化一个 2x2 的共享坐标轴画布 ---
try:
    print("Creating a 2x2 plot with shared axes...")
    # sharex=True, sharey=True 是关键
    plotter = Plotter(layout=(2, 2), figsize=(10, 8), style='flat')

    # --- 3. 在网格中填充不同的图表 ---
    print("Populating the grid with different plot types...")
    plotter.add_scatter(
        data=df_scatter, x='x_val', y='y_val', s='size', 
        tag='scatter', alpha=0.6
    ).set_title('Scatter Plot'
    ).set_xlabel('X Value'
    ).set_ylabel('Y Value')

    plotter.add_bar(
        data=df_bar, x='category', y='mean', y_err='std',
        tag='bar_chart', capsize=5
    ).set_title('Bar Chart'
    ).set_xlabel('Category'
    ).set_ylabel('Mean Value')

    plotter.add_line(
        data=df_line, x='time', y='signal',
        tag='time_series'
    ).set_title('Time Series'
    ).set_xlabel('Time (s)'
    ).set_ylabel('Signal')

    plotter.add_heatmap(
        data=df_heatmap,
        tag='heatmap'
    ).set_title('Heatmap'
    ).set_xlabel('Column'
    ).set_ylabel('Row'
    ).tick_params(axis='x', rotation=90)

    # --- 5. 应用默认美化并保存 ---
    # print("Applying cleanup for shared axes and saving...")
    # plotter.cleanup(auto_share=True)
    plotter.save("multi_plot_grid_figure.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # 确保即使出错也关闭图像
    plt.close('all')

print(f"--- Finished Example: {__file__} ---")

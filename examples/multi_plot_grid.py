# examples/multi_plot_grid.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    plotter = pp.Plotter(n_rows=2, n_cols=2, figsize=(10, 8), sharex=False, sharey=False)

    # --- 3. 在网格中填充不同的图表 ---
    print("Populating the grid with different plot types...")
    plotter.add_scatter(
        data=df_scatter, x='x_val', y='y_val', s='size', 
        tag='scatter', alpha=0.6
    ).add_bar(
        data=df_bar, x='category', y='mean', y_err='std',
        tag='bar_chart', capsize=5
    ).add_line(
        data=df_line, x='time', y='signal',
        tag='time_series'
    ).add_heatmap(
        data=df_heatmap,
        tag='heatmap'
    )

    # --- 4. 对部分图表进行单独设置 ---
    print("Customizing individual plots...")
    plotter.set_title('scatter', 'Scatter Plot')
    plotter.set_xlabel('scatter', 'X Value')
    plotter.set_ylabel('scatter', 'Y Value')

    plotter.set_title('bar_chart', 'Bar Chart')
    plotter.set_xlabel('bar_chart', 'Category')
    plotter.set_ylabel('bar_chart', 'Mean Value')

    plotter.set_title('time_series', 'Time Series')
    plotter.set_xlabel('time_series', 'Time (s)')
    plotter.set_ylabel('time_series', 'Signal')

    plotter.set_title('heatmap', 'Heatmap')
    plotter.set_xlabel('heatmap', 'Column')
    plotter.set_ylabel('heatmap', 'Row')
    plotter.tick_params('heatmap', axis='x', rotation=90)

    # --- 5. 应用默认美化并保存 ---
    plotter.save("multi_plot_grid_figure.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # 确保即使出错也关闭图像
    plt.close('all')

print(f"--- Finished Example: {__file__} ---")

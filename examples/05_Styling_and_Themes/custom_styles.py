# examples/advanced_customization.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

print(f"--- Running Example: {__file__} ---")

# --- 1. 定义一个自定义美化模板 ---
def custom_template(fig, axes):
    """
    一个自定义模板，它会给图表加上一个灰色背景，并用虚线绘制网格。
    Args:
        fig (plt.Figure): The main figure object.
        axes (list[plt.Axes]): A list of axes to apply the template to.
    """
    print("\nApplying CUSTOM cleanup template...")
    for ax in axes:
        ax.set_facecolor('#f0f0f0') # 设置背景颜色
        ax.grid(True, linestyle='--', color='white', linewidth=1.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('gray')
        ax.spines['bottom'].set_color('gray')

# --- 2. 准备数据 ---
df = pd.DataFrame({
    'x': np.random.gumbel(size=100),
    'y': np.random.gumbel(size=100)
})

# --- 3. 初始化并绘图 ---
try:
    plotter = pp.Plotter(figsize=(6, 6), layout=(1, 1))

    # 注册我们的自定义模板
    print("Registering custom cleanup template named 'gray_grid'...")
    # plotter.register_cleanup_template('gray_grid', custom_template)

    plotter.add_scatter(
        data=df, x='x', y='y', tag='gumbel_dist'
    ).set_title('Gumbel Distribution with Ellipse'
    ).set_xlabel('X value'
    ).set_ylabel('Y value')

    # --- 4. 使用 "逃生舱口" get_ax() 进行高级定制 ---
    print("Using get_ax() for advanced customization...")
    # 假设我们要添加一个matplotlib原生对象，比如一个椭圆
    ax = plotter.get_ax('gumbel_dist')

    # 创建一个椭圆 Patch
    ellipse = Ellipse(xy=(0, 0), width=2, height=4, angle=30, 
                      facecolor='none', edgecolor='red', linestyle='--', lw=2)
    ax.add_patch(ellipse)
    
    # --- 5. 使用自定义模板进行美化并保存 ---
    plotter.cleanup()
    plotter.save("advanced_customization_figure.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"--- Finished Example: {__file__} ---")

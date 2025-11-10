# examples/concentration_map_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 模拟一个SERS浓度图数据
np.random.seed(42)
grid_size = 20
x_coords = np.arange(grid_size)
y_coords = np.arange(grid_size)
X, Y = np.meshgrid(x_coords, y_coords)

# 创建一个中心有高浓度，边缘浓度逐渐降低的模拟数据
center_x, center_y = grid_size / 2, grid_size / 2
sigma = 5
concentration = np.exp(-((X - center_x)**2 + (Y - center_y)**2) / (2 * sigma**2))
concentration += np.random.rand(grid_size, grid_size) * 0.1 # 添加一些噪声

# 转换为DataFrame
df_concentration = pd.DataFrame(concentration, index=y_coords, columns=x_coords)

# --- 2. 创建绘图 ---
try:
    plotter = pp.Plotter(layout=(1, 1), figsize=(7, 6))
    
    # 使用新的 add_concentration_map 方法，并链式调用 set_title
    (
        plotter.add_concentration_map(
            data=df_concentration,
            tag='sers_map',
            cbar_kws={'label': 'Concentration (a.u.)'} # 自定义颜色条标签
        )
        .set_title('SERS Concentration Map Example')
    )
    
    # X, Y 轴标签已由 add_concentration_map 默认设置，但可以覆盖
    # plotter.set_xlabel('sers_map', 'Position X (µm)')
    # plotter.set_ylabel('sers_map', 'Position Y (µm)')

    # --- 4. 清理和保存 ---
    plotter.cleanup()
    plotter.save("concentration_map_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'concentration_map_example.png' was generated.")

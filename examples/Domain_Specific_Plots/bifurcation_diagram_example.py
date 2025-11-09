# examples/bifurcation_diagram_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 模拟一个典型分岔图的数据（逻辑斯蒂映射）
def logistic_map(r, x):
    return r * x * (1 - x)

n_steps = 1000
n_transient = 200 # 忽略前面的瞬态过程
r_values = np.linspace(2.5, 4.0, 2000)
x_values = []
bifurcation_param = []

for r in r_values:
    x = 0.1 # 初始值
    # 迭代瞬态过程
    for _ in range(n_transient):
        x = logistic_map(r, x)
    # 记录稳定后的值
    for _ in range(n_steps):
        x = logistic_map(r, x)
        x_values.append(x)
        bifurcation_param.append(r)

df_bifurcation = pd.DataFrame({
    'r': bifurcation_param,
    'x': x_values
})


# --- 2. 创建绘图 ---
try:
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 6))
    # 使用 plotter.add_scatter 直接绘图，并指定 tag=1
    # 这会自动处理坐标轴的获取和标签的注册
    plotter.add_scatter(
        data=df_bifurcation,
        x='r',
        y='x',
        tag=1,  # 显式指定 tag
        s=0.001,
        alpha=0.2,
        marker='.',
        rasterized=True  # 对于有大量数据点的图，设为True可以提高渲染性能
    )
    
    # --- 3. 设置标题和标签 ---
    # 现在 tag=1 已经被正确注册，可以安全使用
    plotter.set_title(1, 'Bifurcation Diagram of the Logistic Map')
    plotter.set_xlabel(1, 'Parameter r')
    plotter.set_ylabel(1, 'State x')

    # --- 4. 清理和保存 ---
    plotter.cleanup()
    plotter.save("bifurcation_diagram_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'bifurcation_diagram_example.png' was generated.")

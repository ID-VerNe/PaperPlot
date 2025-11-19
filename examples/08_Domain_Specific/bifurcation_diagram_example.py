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


# --- 2. 创建绘图 (使用新API) ---
try:
    (
        pp.Plotter(layout=(1, 1), figsize=(8, 6))
        .add_bifurcation_diagram(
            data=df_bifurcation,
            x='r',
            y='x',
            s=0.001, # 调小点的大小以获得更好的视觉效果
            alpha=0.2
        )
        .set_title('Bifurcation Diagram of the Logistic Map')
        .set_xlabel('Parameter r')
        .set_ylabel('State x')
        .save("bifurcation_diagram_example.png")
    )

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'bifurcation_diagram_example.png' was generated.")

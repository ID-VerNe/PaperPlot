# examples/Domain_Specific_Plots/3d_plots_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---

# 3D散点图数据 (Lorenz Attractor)
def lorenz(xyz, *, s=10, r=28, b=2.667):
    x, y, z = xyz
    dxdt = s * (y - x)
    dydt = r * x - y - x * z
    dzdt = x * y - b * z
    return np.array([dxdt, dydt, dzdt])

dt = 0.01
num_steps = 10000
xyzs = np.empty((num_steps + 1, 3))
xyzs[0] = (0., 1., 1.05)
for i in range(num_steps):
    xyzs[i + 1] = xyzs[i] + lorenz(xyzs[i]) * dt
df_lorenz = pd.DataFrame(xyzs, columns=['x', 'y', 'z'])

# 3D表面图数据
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# --- 2. 创建绘图 ---
try:
    # 创建一个包含两个3D子图的布局
    # 注意: 必须在 ax_configs 中指定 projection='3d'
    (
        pp.Plotter(
            layout=(1, 2), 
            figsize=(14, 6),
            ax_configs={
                'ax00': {'projection': '3d'},
                'ax01': {'projection': '3d'}
            }
        )
        .set_suptitle("3D Plotting Demonstration", fontsize=16, weight='bold')

        # --- 左图: 3D线图 ---
        .add_line3d(data=df_lorenz, x='x', y='y', z='z', tag='lorenz', alpha=0.7)
        .set_title("3D Line Plot (Lorenz Attractor)")
        .set_xlabel("X Axis")
        .set_ylabel("Y Axis")
        .set_zlabel("Z Axis")
        .view_init(elev=20, azim=-60) # 设置观察角度

        # --- 右图: 3D表面图 ---
        .add_surface(X=X, Y=Y, Z=Z, tag='surface', cmap='viridis')
        .set_title("3D Surface Plot")
        .set_xlabel("X")
        .set_ylabel("Y")
        .set_zlabel("Z")
        .view_init(elev=45, azim=45)

        # --- 保存 ---
        .save("3d_plots_example.png")
    )

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file '3d_plots_example.png' was generated.")

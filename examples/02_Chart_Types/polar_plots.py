import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
theta = np.linspace(0, 2 * np.pi, 10)
r = np.linspace(1, 10, 10)
df_polar = pd.DataFrame({'theta': theta, 'r': r})

try:
    # 创建极坐标子图
    plotter = pp.Plotter(
        layout=[['POLAR']], 
        ax_configs={'POLAR': {'projection': 'polar'}},
        figsize=(6, 6)
    )
    
    plotter.set_suptitle("Polar Bar Chart", fontsize=16, weight='bold')
    
    # 极坐标柱状图
    plotter.add_polar_bar(
        data=df_polar, theta='theta', r='r', tag='POLAR'
    ).set_title('Polar Bar Chart', tag='POLAR')
    
    # 保存
    plotter.cleanup()
    plotter.save("polar_plots_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'polar_plots_example.png' was generated.")

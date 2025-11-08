# examples/phasor_diagram_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 示例相量数据
magnitudes = [1.0, 0.8, 1.2]
angels = [0, 90, -45] # 角度，单位为度
labels = ['V_ref', 'I_load', 'V_bus']

# --- 2. 创建绘图 ---
try:
    # 初始化Plotter，创建一个普通的笛卡尔轴
    # add_phasor_diagram 会自动将其转换为极坐标
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 8))
    
    # 添加相量图
    plotter.add_phasor_diagram(
        magnitudes=[1.0, 0.8, 1.2],
        angles=[0, 90, -45],
        labels=['V_ref', 'I_load', 'V_bus'],
        tag='phasor_ax',
        angle_unit='degrees'
    )
    
    # 获取极坐标轴并设置标题
    ax = plotter.get_ax('phasor_ax')
    ax.set_title('Phasor Diagram Example', va='bottom')

    # --- 3. 清理和保存 ---
    plotter.cleanup()
    plotter.save("phasor_diagram_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'phasor_diagram_example.png' was generated.")

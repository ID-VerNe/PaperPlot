import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
theta = np.linspace(0, 2 * np.pi, 16)
series_a = 5 + 2 * np.sin(theta)
series_b = 4 + 2 * np.cos(theta)
df = pd.DataFrame({'theta': theta, 'a': series_a, 'b': series_b})

try:
    plotter = pp.Plotter(layout=[['P']], ax_configs={'P': {'projection': 'polar'}}, figsize=(6, 6))

    # 主极坐标轴绘制第一个系列
    (
        plotter
        .add_polar_bar(data=df, theta='theta', r='a', tag='P', alpha=0.6, label='Series A')
        .set_title('Polar Twin Example', tag='P')
    )

    # 创建孪生极坐标轴并绘制第二个系列
    (
        plotter
        .add_polar_twin(tag='P')
        .add_polar_bar(data=df, theta='theta', r='b', alpha=0.6, label='Series B')
        .target_primary(tag='P')
        .set_legend(tag='P', loc='upper right')
    )

    plotter.save("polar_twin_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'polar_twin_example.png' was generated.")

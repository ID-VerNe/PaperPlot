# examples/cleanup_demonstration.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from paperplot import Plotter

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备一组适合共享坐标轴的数据 ---
# 假设我们有4个实验条件，每个条件下都有一条相似的时间序列数据
def generate_data(offset):
    time = np.linspace(0, 10, 50)
    signal = np.sin(time) + np.random.randn(50) * 0.3 + offset
    return pd.DataFrame({'time': time, 'signal': signal})

df1 = generate_data(offset=0)
df2 = generate_data(offset=0.5)
df3 = generate_data(offset=-0.5)
df4 = generate_data(offset=1)

# --- 2. 初始化一个 2x2 的独立坐标轴画布 ---
# 注意：这里我们特意将 sharex 和 sharey 设置为 False
# 目的是为了后续演示 cleanup 函数如何动态地创建共享关系
try:
    print("Creating a 2x2 plot with INDEPENDENT axes...")
    plotter = Plotter(layout=(2, 2), figsize=(10, 8), style='flat')

    # --- 3. 填充图表 ---
    plotter.add_line(data=df1, x='time', y='signal', tag='cond1').set_title('Condition 1').set_ylabel('Signal')
    plotter.add_line(data=df2, x='time', y='signal', tag='cond2').set_title('Condition 2')
    plotter.add_line(data=df3, x='time', y='signal', tag='cond3').set_title('Condition 3').set_xlabel('Time (s)').set_ylabel('Signal')
    plotter.add_line(data=df4, x='time', y='signal', tag='cond4').set_title('Condition 4').set_xlabel('Time (s)')
    
    # --- 5. 使用 cleanup 函数进行智能清理 ---
    print("\nApplying cleanup() to dynamically share axes...")
    # 我们指令cleanup函数：
    # - 对第0行和第1行的Y轴进行共享和清理
    # - 对第0列和第1列的X轴进行共享和清理
    plotter.cleanup(auto_share=True)

    # --- 6. 保存图像 ---
    plotter.save("cleanup_demonstration_figure.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"--- Finished Example: {__file__} ---")
print("A new file 'cleanup_demonstration_figure.png' was generated.")

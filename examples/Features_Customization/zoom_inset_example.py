# examples/Features_Customization/zoom_inset_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 创建一个基础的正弦信号
x = np.linspace(0, 10, 1000)
y = np.sin(x)

# 在一个很小的区域 (x=4.5 to 5.5) 叠加一个高频信号
high_freq_burst = np.sin(x * 50) * np.exp(-((x - 5)**2) / 0.05)
y += high_freq_burst

# --- 2. 使用 Plotter 绘图 ---
try:
    print("Creating a plot with a zoomed inset region...")
    
    # 使用新实现的灵活数据输入功能，直接传入numpy数组
    (
        pp.Plotter(layout=(1, 1), figsize=(10, 6))
        
        # 添加主曲线
        .add_line(
            x=x, 
            y=y, 
            label='Signal with High-Frequency Burst'
        )
        
        # 使用链式调用设置主图的属性
        .set_title('Demonstration of Zoom Inset')
        .set_xlabel('Time (s)')
        .set_ylabel('Amplitude')
        .set_xlim(0, 10)
        .set_ylim(-2, 2.0)
        .set_legend(loc='upper left')

        # 添加缩放指示图 (inset)
        # rect=[x, y, width, height] 定义了 inset 在 Figure 上的位置和大小
        # source_tag 会自动使用上一个活动的 tag
        .add_zoom_inset(
            rect=[0.65, 0.1, 0.3, 0.3],  # 内嵌图的位置和大小 (相对于父坐标轴)
            x_range=(4.5, 5.5),  # 指定要放大的X轴范围
            # y_range 参数现在是可选的，如果省略，将根据 x_range 自动计算
            source_box_kwargs={'facecolor': 'red', 'edgecolor': 'black', 'alpha': 0.15}
        )
        # 手动添加连接线
        .add_zoom_connectors(
            [(1, 2), (4, 3)], # 从源区域的右上角到内嵌图的左上角，从源区域的右下角到内嵌图的左下角
            color='red', linestyle=':', linewidth=1.5
        )
        
        # # 示例：添加一个没有连接线的缩放内嵌图，并手动指定 y_range
        # .add_zoom_inset(
        #     rect=[0.05, 0.1, 0.3, 0.3],  # 另一个内嵌图的位置和大小
        #     x_range=(4.5, 5.5),  # 指定要放大的X轴范围
        #     y_range=(-0.5, 0.5), # 手动指定Y轴范围
        # )

        # 保存图像
        .save("zoom_inset_example.png")
    )

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'zoom_inset_example.png' was generated.")

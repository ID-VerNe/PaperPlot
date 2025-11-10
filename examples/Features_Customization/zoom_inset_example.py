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
        .set_ylim(-1.5, 2.0)
        .set_legend(loc='upper left')

        # 添加一个高亮框，以在主图上标示出将被放大的区域
        .add_highlight_box(
            x_range=(4.5, 5.5),
            y_range=(-1.5, 2.0),
            facecolor='gray',
            alpha=0.2
        )

        # 添加缩放指示图 (inset)
        # rect=[x, y, width, height] 定义了 inset 在 Figure 上的位置和大小
        # zoom_level 定义了缩放的倍数
        # source_tag 会自动使用上一个活动的 tag
        # mark_inset_kwargs 用于定制连接框和线的样式
        .add_zoom_inset(
            rect=[0.55, 0.6, 0.35, 0.35],  # 将 inset 放置在右上角
            zoom_level=4,
            connector_locs=(3, 4),  # 左下角 -> 右下角
            mark_inset_kwargs={'edgecolor': 'red', 'facecolor': 'none', 'linewidth': 1.5}
        )
        
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
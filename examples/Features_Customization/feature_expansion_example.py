# examples/feature_expansion_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 主Y轴数据：温度
df_temp = pd.DataFrame({
    'time': np.linspace(0, 24, 50),
    'temperature': 20 + 5 * np.sin(np.linspace(0, 2 * np.pi, 50)) + np.random.randn(50) * 0.5
})

# 次Y轴数据：降雨量
df_rain = pd.DataFrame({
    'time': np.linspace(0, 24, 10),
    'rainfall': np.random.rand(10) * 10 + 5
})

# 回归数据
df_scatter = pd.DataFrame({
    'x_val': np.random.rand(100) * 10,
    'y_val': 2 * np.random.rand(100) * 10 + 5 + np.random.randn(100) * 2
})

# --- 2. 创建一个1x2的网格 ---
try:
    plotter = pp.Plotter(layout=(1, 2), figsize=(12, 5))

    # --- 左侧子图：双Y轴示例 ---
    # 1. 绘制主Y轴（温度）
    (
        plotter.add_line(
        data=df_temp, x='time', y='temperature', tag='weather_plot', label='Temperature (°C)', color='red')
     .set_title('Hourly Weather Data')
     .set_xlabel('Time (hours)')
     .set_ylabel('Temperature (°C)', color='red')
     .tick_params(axis='y', labelcolor='red')

     # --- 切换到孪生轴上下文 ---
     .add_twinx()  # 从这里开始，所有命令都作用于孪生轴

     # --- 在孪生轴上绘图和设置 ---
     .add_bar(x=df_rain['time'], y=df_rain['rainfall'], width=0.8, alpha=0.3, color='blue', label='Rainfall (mm)')
     .set_ylabel('Rainfall (mm)', color='blue')
     .tick_params(axis='y', labelcolor='blue')

     # --- 关键步骤：切回主轴上下文 ---
     .target_primary()

     # --- 现在可以在主轴上继续添加修饰 ---
     .add_hline(y=25, linestyle='--', color='red', label='Avg Temp')
     .add_text(x=22, y=26, text='High Temp Zone', color='red', ha='center')
     )  # 链式调用在这里结束


    # 4. 添加一个Patch (例如，一个表示夜间的矩形)
    night_rect = Rectangle((20, 0), 4, 30, facecolor='gray', alpha=0.2, transform=plotter.get_ax('weather_plot').transData)
    plotter.add_patch(night_rect, tag='weather_plot')

    # --- 右侧子图：回归图示例 ---
    plotter.add_regplot(
        data=df_scatter, x='x_val', y='y_val', tag='reg_plot', color='green', scatter_kws={'alpha':0.6}
    ).set_title('Regression Analysis'
    ).set_xlabel('Independent Variable'
    ).set_ylabel('Dependent Variable'
    ).add_vline(x=5, linestyle=':', color='gray', label='Threshold'
    ).add_text(x=5, y=25, text='Critical Point', color='gray', ha='left', va='bottom')

    # --- 全局美化 ---
    plotter.set_suptitle("Advanced Plotting Features Demonstration", fontsize=16, weight='bold', y=1.02)
    # 注意：全局图例需要手动收集twinx轴的label
    # 或者，我们可以让add_twinx返回的ax2也注册到tag_to_ax，这样add_global_legend就能自动收集
    # 但目前add_twinx只返回ax2，所以需要手动处理
    # 暂时不添加全局图例，因为twinx的图例收集需要更复杂的逻辑
    # plotter.add_global_legend(loc='upper right') 
    plotter.cleanup(align_labels=True)

    # --- 5. 保存图像 ---
    plotter.save("feature_expansion_figure.png")

except (pp.PaperPlotError, ValueError) as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'feature_expansion_figure.png' was generated.")

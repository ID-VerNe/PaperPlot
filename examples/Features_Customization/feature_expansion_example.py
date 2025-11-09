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
    plotter.add_line(data=df_temp, x='time', y='temperature', tag='weather_plot', label='Temperature (°C)', color='red')
    plotter.set_title('weather_plot', 'Hourly Weather Data')
    plotter.set_xlabel('weather_plot', 'Time (hours)')
    plotter.set_ylabel('weather_plot', 'Temperature (°C)', color='red')
    plotter.tick_params('weather_plot', axis='y', labelcolor='red')

    # 2. 创建twinx轴并绘制次Y轴（降雨量）
    ax2 = plotter.add_twinx('weather_plot')
    ax2.bar(df_rain['time'], df_rain['rainfall'], width=0.8, alpha=0.3, color='blue', label='Rainfall (mm)')
    ax2.set_ylabel('Rainfall (mm)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # 3. 添加参考线和文本
    plotter.add_hline('weather_plot', y=25, linestyle='--', color='red', label='Avg Temp')
    plotter.add_text('weather_plot', x=12, y=26, text='High Temp Zone', color='red', ha='center')

    # 4. 添加一个Patch (例如，一个表示夜间的矩形)
    night_rect = Rectangle((20, 0), 4, 30, facecolor='gray', alpha=0.2, transform=plotter.get_ax('weather_plot').transData)
    plotter.add_patch('weather_plot', night_rect)

    # --- 右侧子图：回归图示例 ---
    plotter.add_regplot(data=df_scatter, x='x_val', y='y_val', tag='reg_plot', color='green', scatter_kws={'alpha':0.6})
    plotter.set_title('reg_plot', 'Regression Analysis')
    plotter.set_xlabel('reg_plot', 'Independent Variable')
    plotter.set_ylabel('reg_plot', 'Dependent Variable')
    plotter.add_vline('reg_plot', x=5, linestyle=':', color='gray', label='Threshold')
    plotter.add_text('reg_plot', x=5, y=25, text='Critical Point', color='gray', ha='left', va='bottom')

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

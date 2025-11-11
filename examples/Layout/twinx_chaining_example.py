from matplotlib.patches import Rectangle

import paperplot as pp
import pandas as pd
import numpy as np

# 1. 准备模拟数据
np.random.seed(42)
hours = np.arange(24)
temperature = 20 + 5 * np.sin(hours / 24 * 2 * np.pi) + np.random.randn(24) * 0.5
rainfall = np.random.rand(24) * 10

df_temp = pd.DataFrame({
    'time': hours,
    'temperature': temperature
})

df_rain = pd.DataFrame({
    'time': hours,
    'rainfall': rainfall
})

# 2. 创建 Plotter 并执行链式调用
# layout=(1, 1) 创建一个子图
plotter = pp.Plotter(layout=(1, 1), figsize=(8, 5))

(
    plotter
    # --- 1. 在主轴上绘图和设置 ---
    .add_line(data=df_temp, x='time', y='temperature', tag='weather_plot', label='Temperature (°C)', color='red')
    .set_title('Hourly Weather Data')
    .set_xlabel('Time (hours)')
    .set_ylabel('Temperature (°C)', color='red')
    .tick_params(axis='y', labelcolor='red')

    # --- 2. 切换到孪生轴上下文 ---
    # 创建孪生轴，并将 active_target 切换为 'twin'
    .add_twinx(tag='weather_plot')

    # --- 3. 在孪生轴上绘图和设置 ---
    # 绘图操作会自动作用于孪生轴
    .add_bar(data=df_rain, x='time', y='rainfall', label='Rainfall (mm)', color='blue', alpha=0.3)

    # --- 4. 切换轴，来添加更多修饰 ---
    .target_primary(tag='weather_plot') # 切换回主轴，并确保 last_active_tag 仍是 'weather_plot'
    .add_hline(y=25, linestyle='--', color='red', label='Avg Temp')

    .target_twin(tag='weather_plot') # 切换回孪生轴
    .tick_params(axis='y', labelcolor='blue')
    .set_ylabel('Rainfall (mm)', color='blue')

    .target_primary(tag='weather_plot') # 切换回主轴
    # --- 5. 收尾工作 ---
    # set_legend 会自动收集主轴和孪生轴的图例项并合并
    .set_legend(loc='upper left')
)

night_rect = Rectangle((20, 0), 4, 30, facecolor='gray', alpha=0.2, transform=plotter.get_ax('weather_plot').transData)
plotter.add_patch(night_rect, tag='weather_plot').save("twinx_chaining_example.png")

print("twinx_chaining_example.py executed successfully.")

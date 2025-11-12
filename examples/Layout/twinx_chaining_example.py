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
    .add_line(data=df_temp, x='time', y='temperature', tag='weather_plot', label='Temperature (°C)')
    .set_title('Hourly Weather Data with Automated Color Cycling')
    .set_xlabel('Time (hours)')
    .set_ylabel('Temperature (°C)')
    .tick_params(axis='y')

    # --- 2. 切换到孪生轴上下文 ---
    # 创建孪生轴，它会自动继承主轴的颜色循环状态
    .add_twinx(tag='weather_plot')

    # --- 3. 在孪生轴上绘图和设置 ---
    # add_bar 会自动使用颜色循环中的下一个颜色
    .add_bar(data=df_rain, x='time', y='rainfall', label='Rainfall (mm)', alpha=0.5)
    .set_ylabel('Rainfall (mm)')
    .tick_params(axis='y')

    # --- 4. 切换回主轴，添加更多修饰 ---
    .target_primary(tag='weather_plot')
    .add_hline(y=25, linestyle='--', color='gray', label='High Temp Threshold') # 手动指定颜色，不影响颜色循环

    # --- 5. 收尾工作 ---
    # set_legend 会自动收集主轴和孪生轴的图例项并合并
    .set_legend(loc='upper left')
)

# 演示：即便是链式调用结束后，我们仍然可以通过 get_ax() 进行修改
weather_ax = plotter.get_ax('weather_plot')
# 自动获取主轴和孪生轴的颜色并应用到Y轴标签上，增强可读性
y1_color = weather_ax.lines[0].get_color()
y2_color = plotter.twin_axes['weather_plot'].patches[0].get_facecolor()

plotter.set_ylabel('Temperature (°C)', color=y1_color, tag='weather_plot')
plotter.tick_params(axis='y', labelcolor=y1_color, tag='weather_plot')

plotter.target_twin('weather_plot')
plotter.set_ylabel('Rainfall (mm)', color=y2_color)
plotter.tick_params(axis='y', labelcolor=y2_color)

# 保存图像
plotter.save("twinx_chaining_and_color_sync_test.png")

print("twinx_chaining_example.py executed successfully.")
print("A new file 'twinx_chaining_and_color_sync_test.png' was generated.")
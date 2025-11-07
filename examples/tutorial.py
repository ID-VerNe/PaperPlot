# examples/tutorial.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 准备数据 ---
df_line = pd.DataFrame({
    'time': np.arange(10), 
    'value': np.sin(np.arange(10) * 0.5) + np.random.rand(10) * 0.2
})
df_hist = pd.DataFrame({'score': np.random.normal(10, 2, 200)})

# --- 2. 初始化一个 1x2 的画布 ---
# 使用 try...except 捕获我们自定义的异常
try:
    print("Creating a 1x2 plot...")
    plotter = pp.Plotter(n_rows=1, n_cols=2, style='publication', figsize=(10, 4.5), sharey=True)

    # --- 3. 添加绘图内容 ---
    print("Adding plots to the canvas...")
    plotter.add_line(
        data=df_line, x='time', y='value', 
        tag='timeseries',
        label='Measurement',
        marker='o'
    ).add_hist(
        data=df_hist, x='score',
        tag='distribution',
        bins=20,
        color='#ff7f0e', # 使用另一种颜色
        alpha=0.7
    )

    # --- 4. 通过tag进行精细修改 ---
    print("Customizing individual plots by tag...")
    # 修改第一个图
    plotter.set_title('timeseries', 'Sensor Readings Over Time')
    plotter.set_xlabel('timeseries', 'Time (seconds)', fontsize=10)
    plotter.set_ylabel('timeseries', 'Signal Value')
    plotter.set_ylim('timeseries', top=2.0) # 调整上限以适应数据
    plotter.set_legend('timeseries', loc='lower left')

    # 修改第二个图
    plotter.set_title('distribution', 'Score Distribution')
    plotter.set_xlabel('distribution', 'Score')
    # 由于Y轴共享，不需要单独设置Y轴标签
    # plotter.tick_params('distribution', axis='x', rotation=15)

    # --- 5. 全局美化并保存 ---
    print("Applying cleanup template and saving the figure...")
    plotter.cleanup(template='default') # 应用默认美化模板
    plotter.save('tutorial.png')

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
    # 确保在出错时关闭未完成的图像，防止内存泄漏
    plt.close('all')
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    plt.close('all')


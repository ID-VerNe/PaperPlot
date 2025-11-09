# examples/aesthetic_and_processing_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 数据平滑示例数据
np.random.seed(0)
x_smooth = np.linspace(0, 50, 200)
y_noisy = 5 * np.sin(x_smooth / 5) + np.random.randn(200) * 2 + 10
df_smooth = pd.DataFrame({'x': x_smooth, 'y_noisy': y_noisy})

# 高亮数据点示例数据
np.random.seed(42)
df_scatter = pd.DataFrame({
    'x': np.random.rand(100) * 10,
    'y': np.random.rand(100) * 10,
    'p_value': np.random.rand(100)
})
# 定义高亮条件：p-value < 0.05
highlight_condition = df_scatter['p_value'] < 0.05


# --- 2. 创建绘图 ---
try:
    plotter = pp.Plotter(layout=(1, 2), figsize=(12, 5))
    plotter.set_suptitle("Aesthetic and Processing Utilities", fontsize=16, weight='bold')

    # --- 3. 左图: 数据平滑 ---
    ax_smooth = plotter.get_ax_by_name('ax00')
    plotter.tag_to_ax['smooth'] = ax_smooth # 手动关联tag

    # 绘制原始噪声数据
    ax_smooth.plot(df_smooth['x'], df_smooth['y_noisy'], label='Noisy Data', 
                   color='gray', alpha=0.5, linestyle=':')
    
    # 计算并绘制平滑后数据
    y_smoothed = pp.utils.moving_average(df_smooth['y_noisy'], window_size=10)
    ax_smooth.plot(df_smooth['x'], y_smoothed, label='Smoothed Data (window=10)', 
                   color='blue', lw=2)
    
    plotter.set_title('smooth', 'moving_average() Example')
    plotter.set_xlabel('smooth', 'Time')
    plotter.set_ylabel('smooth', 'Signal')
    plotter.set_legend('smooth')

    # --- 4. 右图: 高亮数据点 ---
    ax_highlight = plotter.get_ax_by_name('ax01')
    plotter.tag_to_ax['highlight'] = ax_highlight

    # 使用新函数高亮数据点
    pp.utils.highlight_points(
        ax=ax_highlight,
        data=df_scatter,
        x='x',
        y='y',
        condition=highlight_condition,
        label_normal='p >= 0.05',
        label_highlight='p < 0.05',
        c_highlight='orange',
        s_highlight=80,
        edgecolors='black' # 应用于所有点的额外参数
    )

    plotter.set_title('highlight', 'highlight_points() Example')
    plotter.set_xlabel('highlight', 'X value')
    plotter.set_ylabel('highlight', 'Y value')
    plotter.set_legend('highlight')


    # --- 5. 清理和保存 ---
    plotter.cleanup()
    plotter.save("aesthetic_and_processing_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'aesthetic_and_processing_example.png' was generated.")

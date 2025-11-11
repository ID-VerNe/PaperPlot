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
df_scatter['is_significant'] = highlight_condition


# --- 2. 创建绘图 ---
try:
    plotter = pp.Plotter(layout=(1, 2), figsize=(12, 5))
    plotter.set_suptitle("Aesthetic and Processing Utilities", fontsize=16, weight='bold')

    # --- 3. 左图: 数据平滑 ---
    # 绘制原始噪声数据
    plotter.add_line(
        data=df_smooth, x='x', y='y_noisy', tag='smooth', label='Noisy Data', 
        color='gray', alpha=0.5, linestyle=':', ax=plotter.get_ax_by_name('ax00')
    )
    
    # 计算并绘制平滑后数据
    y_smoothed = pp.utils.moving_average(df_smooth['y_noisy'], window_size=10)
    # 由于 add_line 会更新 last_active_tag，这里需要再次指定 ax
    plotter.add_line(
        x=df_smooth['x'], y=y_smoothed, label='Smoothed Data (window=10)', 
        color='blue', linewidth=2, ax=plotter.get_ax_by_name('ax00')
    ).set_title('moving_average() Example'
    ).set_xlabel('Time'
    ).set_ylabel('Signal'
    ).set_legend()

    # --- 4. 右图: 高亮数据点 ---
    # 使用新函数高亮数据点
    plotter.add_conditional_scatter(
        data=df_scatter,
        x='x',
        y='y',
        condition='is_significant',
        tag='highlight',
        ax=plotter.get_ax_by_name('ax01'),
        label_normal='p >= 0.05',
        label_highlight='p < 0.05',
        c_highlight='orange',
        s_highlight=80,
        edgecolors='black' # 应用于所有点的额外参数
    ).set_title('highlight_points() Example'
    ).set_xlabel('X value'
    ).set_ylabel('Y value'
    ).set_legend()


    # --- 5. 清理和保存 ---
    plotter.cleanup()
    plotter.save("aesthetic_and_processing_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'aesthetic_and_processing_example.png' was generated.")

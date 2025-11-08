# examples/data_analysis_utils_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 分布拟合示例数据
np.random.seed(42)
normal_data = np.random.normal(loc=0, scale=1, size=1000)
df_dist = pd.DataFrame({'value': normal_data})

# 数据分箱示例数据
x_bin = np.linspace(0, 10, 200)
y_bin = 2 * x_bin + np.random.normal(loc=0, scale=2, size=200)
df_bin = pd.DataFrame({'x': x_bin, 'y': y_bin})


# --- 2. 创建绘图 ---
try:
    plotter = pp.Plotter(layout=(1, 2), figsize=(12, 5))
    plotter.set_suptitle("Data Analysis Utilities", fontsize=16, weight='bold')

    # --- 3. 左图: 分布拟合 ---
    ax_dist = plotter.get_ax_by_name('ax00')
    plotter.tag_to_ax['dist'] = ax_dist # 手动关联tag

    # 绘制直方图
    ax_dist.hist(df_dist['value'], bins=30, density=True, alpha=0.6, color='skyblue', label='Data Histogram')
    
    # 拟合并绘制正态分布
    pp.utils.fit_and_plot_distribution(
        ax=ax_dist,
        data_series=df_dist['value'],
        dist_name='norm',
        color='red',
        linestyle='--',
        lw=2
    )
    
    plotter.set_title('dist', 'fit_and_plot_distribution() Example')
    plotter.set_xlabel('dist', 'Value')
    plotter.set_ylabel('dist', 'Density')
    plotter.set_legend('dist')

    # --- 4. 右图: 数据分箱 ---
    ax_bin = plotter.get_ax_by_name('ax01')
    plotter.tag_to_ax['bin'] = ax_bin

    # 绘制原始散点图
    ax_bin.scatter(df_bin['x'], df_bin['y'], alpha=0.3, label='Raw Data')

    # 分箱数据
    binned_df = pp.utils.bin_data(df_bin, x='x', y='y', bins=5)
    
    # 绘制分箱后的结果（带误差棒的线图）
    ax_bin.errorbar(binned_df['bin_center'], binned_df['y_agg'], 
                     yerr=binned_df['y_error'], fmt='-o', color='green', 
                     capsize=5, label='Binned Data (Mean ± Std)')

    plotter.set_title('bin', 'bin_data() Example')
    plotter.set_xlabel('bin', 'X Value')
    plotter.set_ylabel('bin', 'Y Value')
    plotter.set_legend('bin')


    # --- 5. 清理和保存 ---
    plotter.cleanup()
    plotter.save("data_analysis_utils_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'data_analysis_utils_example.png' was generated.")

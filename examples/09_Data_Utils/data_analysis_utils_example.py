# examples/data_analysis_utils_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    # 使用新的 API 进行绘图和修饰
    (
        pp.Plotter(layout=(1, 2), figsize=(12, 5))
        .set_suptitle("Data Analysis Utilities (New API)", fontsize=16, weight='bold')

        # --- 左图: 分布拟合 ---
        .add_hist(data=df_dist, x='value', tag='dist', bins=30, density=True, alpha=0.6, color='skyblue', label='Data Histogram')
        .add_distribution_fit(data=df_dist, x='value', dist_name='norm', color='red', linestyle='--', lw=2, tag='dist')
        .set_title("add_distribution_fit() Example", tag='dist')
        .set_xlabel("Value", tag='dist')
        .set_ylabel("Density", tag='dist')
        .set_legend(tag='dist')

        # --- 右图: 数据分箱 ---
        .add_scatter(data=df_bin, x='x', y='y', tag='bin', alpha=0.3, label='Raw Data')
        .add_binned_plot(data=df_bin, x='x', y='y', bins=5, plot_type='errorbar',
                         color='green', fmt='-o', capsize=5, label='Binned Data (Mean ± Std)', tag='bin')
        .set_title("add_binned_plot() Example", tag='bin')
        .set_xlabel("X Value", tag='bin')
        .set_ylabel("Y Value", tag='bin')
        .set_legend(tag='bin')

        # --- 清理和保存 ---
        .cleanup()
        .save("data_analysis_utils_example.png")
    )

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    # 在调试时，取消下面的注释可以打印更详细的错误信息
    # import traceback
    # traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'data_analysis_utils_example.png' was generated with the new API.")

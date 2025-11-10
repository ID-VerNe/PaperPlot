# examples/Features_Customization/statistical_plots_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 使用 seaborn 自带的 'tips' 数据集
tips = sns.load_dataset("tips")

# --- 2. 创建绘图 ---
try:
    (
        pp.Plotter(layout=(1, 2), figsize=(12, 6))
        .set_suptitle("Statistical Plots Demonstration", fontsize=16, weight='bold')

        # --- 左图: 小提琴图 + 蜂群图 ---
        .add_violin(data=tips, x="day", y="total_bill", tag='ax00', inner=None)
        .add_swarm(data=tips, x="day", y="total_bill", color="k", alpha=0.8, size=3, tag='ax00')
        .set_title("Violin Plot with Swarm Plot Overlay", tag='ax00')
        .set_xlabel("Day of the Week", tag='ax00')
        .set_ylabel("Total Bill ($)", tag='ax00')

        # --- 右图: 箱线图 + 统计检验 ---
        .add_box(data=tips, x="time", y="total_bill", tag='ax01')
        .set_title("Box Plot with Statistical Annotation", tag='ax01')
        .set_xlabel("Time of Day", tag='ax01')
        .set_ylabel("Total Bill ($)", tag='ax01')
        # 添加统计检验
        .add_stat_test(
            tag='ax01',
            x="time", 
            y="total_bill", 
            group1='Lunch',
            group2='Dinner'
        )
        # 调整Y轴范围以确保统计标注可见
        .set_ylim(None, tips['total_bill'].max() * 1.2, tag='ax01')

        # --- 保存 ---
        .save("statistical_plots_example.png")
    )

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'statistical_plots_example.png' was generated.")

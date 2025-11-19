import paperplot as pp
import pandas as pd
import numpy as np

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 为主轴准备4条线的数据，以耗尽一个有4种颜色的循环
x_data = np.linspace(0, 10, 100)
df_lines = pd.DataFrame({'x': x_data})
for i in range(5):
    # 使用不同的相位和偏移量，让线条清晰可辨
    df_lines[f'y_{i}'] = np.sin(x_data + i * np.pi / 2) + (i * 2.5)

# 为孪生轴准备柱状图数据
df_bar = pd.DataFrame({
    'category': ['Alpha', 'Beta', 'Gamma'],
    'value': [10, 15, 12]
})

# --- 2. 初始化 Plotter ---
# 明确使用您的主题，以确保颜色循环是4种颜色
plotter = pp.Plotter(layout=(1, 1), figsize=(10, 6), style='marin_kitagawa')

# --- 3. 执行绘图 ---
(
    plotter
    .set_suptitle("Test: Twin-Axis Color Cycle Wrap-Around", fontsize=16, weight='bold')

    # --- 在主轴上绘制4条线来耗尽颜色循环 ---
    .add_line(data=df_lines, x='x', y='y_0', label='Primary Line 1 (Color 1: Pink)')
    .add_line(data=df_lines, x='x', y='y_1', label='Primary Line 2 (Color 2: Teal)')
    .add_line(data=df_lines, x='x', y='y_2', label='Primary Line 3 (Color 3: Gold)')
    .add_line(data=df_lines, x='x', y='y_3', label='Primary Line 4 (Color 4: Purple)')
    .add_line(data=df_lines, x='x', y='y_4', label='Primary Line 5 (Color 5:)')
    .set_ylabel("Primary Axis Value (Lines)")
    .set_xlabel("X-axis")

    # --- 创建孪生轴 ---
    # 此时，主轴已用完4种颜色。孪生轴的颜色循环应从头开始。
    .add_twinx()

    # --- 在孪生轴上绘图 ---
    # 这个柱状图应该自动使用颜色循环的第1个颜色（粉色）
    .add_bar(data=df_bar, x='category', y='value', label='Twin Bar Plot (Should be Color 1: Pink)', alpha=0.6)
    .set_ylabel("Twin Axis Value (Bars)")

    # --- 合并图例并保存 ---
    .target_primary()
    .set_legend(loc='upper left')
    .save("twinx_color_cycle_wrap_test.png")
)

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'twinx_color_cycle_wrap_test.png' was generated.")
print("Check this file to confirm that the bar plot color has wrapped around to the first color of the cycle.")
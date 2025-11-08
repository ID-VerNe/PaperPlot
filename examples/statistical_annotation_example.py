# examples/statistical_annotation_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 创建一个适合箱形图的数据集
np.random.seed(42)
data = {
    'value': np.concatenate([
        np.random.normal(loc=10, scale=2, size=30),
        np.random.normal(loc=15, scale=2.5, size=30),
        np.random.normal(loc=12, scale=2, size=30)
    ]),
    'group': ['A'] * 30 + ['B'] * 30 + ['C'] * 30
}
df = pd.DataFrame(data)

# --- 2. 创建绘图 ---
try:
    # 使用新的 add_box 方法
    plotter = pp.Plotter(layout=(1, 1), figsize=(6, 5))
    plotter.add_box(data=df, x='group', y='value', tag='box')
    
    # --- 3. 添加统计标注 ---
    ax = plotter.get_ax('box')
    
    # 在 A 组和 B 组之间进行 t-test 并添加标注
    pp.utils.add_stat_test(
        ax=ax,
        data=df,
        x='group',
        y='value',
        group1='A',
        group2='B',
        test='t-test_ind'
    )
    
    # --- 4. 设置标题和标签 ---
    plotter.set_title('box', 'Statistical Annotation Example')
    plotter.set_xlabel('box', 'Group')
    plotter.set_ylabel('box', 'Value')

    # --- 5. 清理和保存 ---
    plotter.cleanup()
    plotter.save("statistical_annotation_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'statistical_annotation_example.png' was generated.")

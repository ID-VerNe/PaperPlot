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
        np.random.normal(loc=12, scale=2, size=30),
        np.random.normal(loc=16, scale=2.2, size=30)  # 新增组 D
    ]),
    'group': ['A'] * 30 + ['B'] * 30 + ['C'] * 30 + ['D'] * 30
}
df = pd.DataFrame(data)

# --- 2. 创建绘图 ---
try:
    # 使用 add_box 方法
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 6))
    plotter.add_box(data=df, x='group', y='value', tag='box'
                    ).set_title('Statistical Annotation Example (Multiple Comparisons)'
                                ).set_xlabel('Group'
                                             ).set_ylabel('Value')

    # --- 3. 添加统计标注 ---
    # 定义比较对
    comparisons = [
        ('A', 'B'),
        ('C', 'D'),
        ('A', 'C')  # 也可以添加更多比较
    ]

    # 使用 add_pairwise_tests 进行多组比较
    # 注意：这里移除了 data=df 参数
    plotter.add_pairwise_tests(
        tag='box',  # 指定要操作的子图
        x='group',
        y='value',
        comparisons=comparisons,
        test='t-test_ind',
        text_offset_factor=0.05  # 控制标注线之间的间距
    )

    # --- 5. 清理和保存 ---
    plotter.cleanup()
    plotter.save("statistical_annotation_example.png")

except Exception as e:
    # 打印更详细的错误信息以便调试
    import traceback

    print(f"An unexpected error occurred: {e}")
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'statistical_annotation_example.png' was generated.")
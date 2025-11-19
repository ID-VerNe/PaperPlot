import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
cats = ['A', 'B', 'C']
df_bar = pd.DataFrame({
    'cat': cats,
    's1': [1, 3, 2],
    's2': [2, 2, 3],
    's3': [0, 1, 2]
})

try:
    # 布局：1行2列，展示分组和堆叠柱状图
    plotter = pp.Plotter(layout=(1, 2), figsize=(10, 5))
    
    plotter.set_suptitle("Bar Chart Types", fontsize=16, weight='bold')
    
    # 1. 分组柱状图（Grouped Bar）
    plotter.add_grouped_bar(
        data=df_bar, x='cat', ys=['s1', 's2', 's3'], 
        labels={'s1': 'Series 1', 's2': 'Series 2', 's3': 'Series 3'}, 
        tag='ax00'
    ).set_title('Grouped Bar Chart', tag='ax00'
    ).set_xlabel('Category', tag='ax00'
    ).set_ylabel('Value', tag='ax00'
    ).set_legend('ax00')
    
    # 2. 堆叠柱状图（Stacked Bar）
    plotter.add_stacked_bar(
        data=df_bar, x='cat', ys=['s1', 's2', 's3'], 
        labels={'s1': 'Part 1', 's2': 'Part 2', 's3': 'Part 3'}, 
        tag='ax01'
    ).set_title('Stacked Bar Chart', tag='ax01'
    ).set_xlabel('Category', tag='ax01'
    ).set_ylabel('Total Value', tag='ax01'
    ).set_legend('ax01')
    
    # 保存
    plotter.cleanup(align_labels=True)
    plotter.save("bar_charts_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'bar_charts_example.png' was generated.")

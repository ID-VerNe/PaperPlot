import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
df_line = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y1': [1, 2, 3, 4],
    'y2': [2, 1, 3, 2]
})

try:
    # 创建单个子图
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 5))
    
    plotter.set_suptitle("Multi-Line Chart", fontsize=16, weight='bold')
    
    # 多线折线图
    plotter.add_multi_line(
        data=df_line, x='x', ys=['y1', 'y2'], 
        labels={'y1': 'Line A', 'y2': 'Line B'}
    ).set_title('Multi-Line Chart'
    ).set_xlabel('X Value'
    ).set_ylabel('Y Value'
    ).set_legend()
    
    # 保存
    plotter.cleanup(align_labels=True)
    plotter.save("line_charts_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'line_charts_example.png' was generated.")

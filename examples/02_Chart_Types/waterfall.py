import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
df_waterfall = pd.DataFrame({
    'x': ['start', 'a', 'b', 'c'],
    'deltas': [10, -3, 5, -2]
})

try:
    # 创建单个子图
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 5))
    
    plotter.set_suptitle("Waterfall Chart", fontsize=16, weight='bold')
    
    # 瀑布图
    plotter.add_waterfall(
        data=df_waterfall, x='x', deltas='deltas'
    ).set_title('Waterfall Chart'
    ).set_xlabel('Steps'
    ).set_ylabel('Value')
    
    # 保存
    plotter.cleanup()
    plotter.save("waterfall_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'waterfall_example.png' was generated.")

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
df_pie = pd.DataFrame({'sizes': [3, 2, 5]})
df_donut = df_pie.copy()
df_nested_inner = pd.DataFrame({'sizes': [2, 3]})

try:
    # 布局：1行3列，展示饼图、环形图、嵌套环形图
    plotter = pp.Plotter(layout=(1, 3), figsize=(12, 4))
    
    plotter.set_suptitle("Pie and Donut Charts", fontsize=16, weight='bold')
    
    # 1. 饼图
    plotter.add_pie(
        data=df_pie, sizes='sizes', labels=['X', 'Y', 'Z'], tag='ax00'
    ).set_title('Pie Chart', tag='ax00')
    
    # 2. 环形图
    plotter.add_donut(
        data=df_donut, sizes='sizes', labels=['X', 'Y', 'Z'], 
        width=0.4, radius=1.0, tag='ax01'
    ).set_title('Donut Chart', tag='ax01')
    
    # 3. 嵌套环形图
    plotter.add_nested_donut(
        outer={'data': df_donut, 'sizes': 'sizes', 'labels': ['X', 'Y', 'Z']},
        inner={'data': df_nested_inner, 'sizes': 'sizes', 'labels': ['I1', 'I2']},
        tag='ax02'
    ).set_title('Nested Donut Chart', tag='ax02')
    
    # 保存
    plotter.cleanup()
    plotter.save("pie_and_donut_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'pie_and_donut_example.png' was generated.")

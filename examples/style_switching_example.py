# examples/style_switching_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'ProductA_Sales': [150, 160, 175, 180, 195, 210],
    'ProductB_Sales': [80, 85, 82, 90, 95, 100]
}
df_sales = pd.DataFrame(data)

# --- 2. 使用默认的 'publication' 样式 ---
print("\nGenerating plot with 'publication' style...")
try:
    plotter_pub = pp.Plotter(n_rows=1, n_cols=1, style='publication', figsize=(7, 5))
    
    # 第一条线，创建子图并标记为 'sales'
    plotter_pub.add_line(
        data=df_sales, x='Month', y='ProductA_Sales', 
        tag='sales', label='Product A', marker='o'
    )
    
    # 获取刚刚创建的子图的ax对象
    ax_pub = plotter_pub.get_ax('sales')

    # 第二条线，使用 ax 参数在同一个子图上绘制
    plotter_pub.add_line(
        data=df_sales, x='Month', y='ProductB_Sales', 
        ax=ax_pub,
        label='Product B', marker='s', color='#ff7f0e'
    )

    plotter_pub.set_title('sales', 'Monthly Sales Figures (Publication Style)')
    plotter_pub.set_xlabel('sales', 'Month')
    plotter_pub.set_ylabel('sales', 'Units Sold')
    plotter_pub.set_legend('sales')
    plotter_pub.cleanup()

    plotter_pub.save('publication_style_figure.png')

except pp.PaperPlotError as e:
    print(f"An error occurred: {e}")
finally:
    plt.close('all')

# --- 3. 切换到 'presentation' 样式 ---
print("\nGenerating plot with 'presentation' style...")
try:
    # 在初始化时，通过 style 参数切换样式
    plotter_pres = pp.Plotter(n_rows=1, n_cols=1, style='presentation', figsize=(8, 6))
    
    # 同样的操作，但使用新的plotter实例
    plotter_pres.add_line(
        data=df_sales, x='Month', y='ProductA_Sales', 
        tag='sales_pres', label='Product A', marker='o'
    )
    ax_pres = plotter_pres.get_ax('sales_pres')
    plotter_pres.add_line(
        data=df_sales, x='Month', y='ProductB_Sales', 
        ax=ax_pres,
        label='Product B', marker='s'
    )

    plotter_pres.set_title('sales_pres', 'Monthly Sales Figures (Presentation Style)')
    plotter_pres.set_xlabel('sales_pres', 'Month')
    plotter_pres.set_ylabel('sales_pres', 'Units Sold')
    plotter_pres.set_legend('sales_pres')
    # presentation样式文件已经处理了背景色和spines，所以cleanup()可以不用
    # plotter_pres.cleanup()

    plotter_pres.save('presentation_style_figure.png')

except pp.PaperPlotError as e:
    print(f"An error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("Two files were generated: 'publication_style_figure.pdf' and 'presentation_style_figure.pdf'")

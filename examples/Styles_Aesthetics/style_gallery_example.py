# examples/style_gallery_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备一份用于演示的标准数据 ---
def generate_demo_data():
    """Generates a simple dataframe for plotting."""
    x = np.linspace(0, 10, 30)
    y1 = np.sin(x) + np.random.randn(30) * 0.1
    y2 = np.cos(x) + np.random.randn(30) * 0.1
    return pd.DataFrame({'x': x, 'y1': y1, 'y2': y2})

df_demo = generate_demo_data()

# --- 2. 定义一个函数，用于为指定风格创建图表 ---
def create_plot_for_style(style_name: str):
    """Creates and saves a plot for a given style name."""
    print(f"Generating plot for style: '{style_name}'...")
    try:
        # 使用 (1, 1) 元组来初始化一个简单的1x1网格
        plotter = pp.Plotter(layout=(1, 1), style=style_name, figsize=(8, 6))

        # 在图上绘制两条线
        plotter.add_line(data=df_demo, x='x', y='y1', tag='demo', label='Sine-like', marker='o')
        ax = plotter.get_ax('demo') # Get the ax for the first line
        plotter.add_line(data=df_demo, x='x', y='y2', ax=ax, label='Cosine-like', marker='^'
        ).set_title(f"Style: '{style_name}'"
        ).set_xlabel('X-axis'
        ).set_ylabel('Y-axis'
        ).set_legend()

        # 保存图像
        filename = f"style_gallery_{style_name}.png"
        plotter.save(filename)
        print(f"  -> Saved {filename}")

    except (pp.PaperPlotError, ValueError, FileNotFoundError) as e:
        print(f"  -> Error generating plot for style '{style_name}': {e}")
    except Exception as e:
        print(f"  -> An unexpected error occurred: {e}")
    finally:
        plt.close('all')

# --- 3. 循环遍历所有可用风格并生成图表 ---
# 我们目前拥有的所有风格
styles_to_showcase = [
    'publication', 
    'presentation', 
    'flat', 
    'nord', 
    'solarized_light'
]

for style in styles_to_showcase:
    create_plot_for_style(style)

print(f"\n--- Finished Example: {__file__} ---")

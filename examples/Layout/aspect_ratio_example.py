# examples/aspect_ratio_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 场景 1: 简单网格与固定宽高比 ---
print("\n--- Scene 1: Simple 2x3 grid with 16:9 aspect ratio ---")
try:
    # 我们不指定 figsize，而是指定 subplot_aspect
    # Plotter 会自动计算出最佳的 figsize
    plotter1 = pp.Plotter(layout=(2, 3), subplot_aspect=(16, 9))
    plotter1.set_suptitle("2x3 Grid with 16:9 Subplot Aspect Ratio", fontsize=16)

    # 填充所有子图
    for i, ax in enumerate(plotter1.axes):
        tag = f'ax{i//plotter1.layout[1]}{i%plotter1.layout[1]}' # Correct tag for simple grid
        plotter1.add_line(
            data=pd.DataFrame({'x': [0, 1], 'y': [0, 1]}), 
            x='x', y='y', 
            ax=ax, 
            tag=tag
        ).set_title(f'Plot {i+1} (16:9)')

    plotter1.save("aspect_ratio_simple_grid.png")
    print("Generated 'aspect_ratio_simple_grid.png'")

except (ValueError, NotImplementedError) as e:
    print(f"An error occurred: {e}")
finally:
    plt.close('all')


# --- 场景 2: 复杂 Mosaic 布局与固定宽高比 ---
print("\n--- Scene 2: Complex mosaic layout with 1:1 aspect ratio cells ---")
try:
    layout = [
        ['A', 'A', 'B'],
        ['C', 'D', 'B']
    ]
    # 我们要求每个基本单元格都是正方形 (1:1)
    plotter2 = pp.Plotter(layout=layout, subplot_aspect=(1, 1))
    plotter2.set_suptitle("Mosaic Layout with 1:1 Aspect Ratio Cells", fontsize=16)

    # 填充子图
    # 区域 'A' 跨越 1x2 个单元格，所以它的实际比例应该是 1:2
    plotter2.add_line(data=pd.DataFrame({'x': [0, 1], 'y': [0, 1]}), x='x', y='y', ax=plotter2.get_ax_by_name('A'), tag='A'
    ).set_title("Area 'A' (1x2 cells)")

    # 区域 'B' 跨越 2x1 个单元格，所以它的实际比例应该是 2:1
    plotter2.add_line(data=pd.DataFrame({'x': [0, 1], 'y': [0, 1]}), x='x', y='y', ax=plotter2.get_ax_by_name('B'), tag='B'
    ).set_title("Area 'B' (2x1 cells)")

    # 区域 'C' 和 'D' 都是 1x1 的正方形
    plotter2.add_line(data=pd.DataFrame({'x': [0, 1], 'y': [0, 1]}), x='x', y='y', ax=plotter2.get_ax_by_name('C'), tag='C'
    ).set_title("Area 'C' (1x1 cell)")
    plotter2.add_line(data=pd.DataFrame({'x': [0, 1], 'y': [0, 1]}), x='x', y='y', ax=plotter2.get_ax_by_name('D'), tag='D'
    ).set_title("Area 'D' (1x1 cell)")

    plotter2.save("aspect_ratio_mosaic.png")
    print("Generated 'aspect_ratio_mosaic.png'")

except (ValueError, NotImplementedError) as e:
    print(f"An error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")

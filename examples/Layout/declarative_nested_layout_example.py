# examples/Layout/declarative_nested_layout_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 主图数据
df_line = pd.DataFrame({
    'x': np.linspace(0, 2 * np.pi, 100),
    'y': np.sin(np.linspace(0, 2 * np.pi, 100))
})
# 子网格的热图数据
heatmap_data_1 = pd.DataFrame(np.random.rand(8, 50))
heatmap_data_2 = pd.DataFrame(np.random.rand(8, 50))
heatmap_data_3 = pd.DataFrame(np.random.rand(8, 50))
# Y轴标签
y_labels = ['~NH₂', 'v(C-N-C)', 'v(C-C)ring']
all_heatmap_data = [heatmap_data_1, heatmap_data_2, heatmap_data_3]

try:
    # --- 2. 使用字典声明式地定义整个嵌套布局 ---
    # 这是新API的核心：一个字典描述了所有层级和结构
    nested_layout = {
        # 'main' 定义了顶层 1x2 布局
        'main': [
            ['main_plot', 'heatmap_group']
        ],
        # 'subgrids' 定义了 'heatmap_group' 区域如何被再次划分
        'subgrids': {
            'heatmap_group': {
                # 'layout' 定义了 3x1 的内部网格，并为每个单元命名
                'layout': [
                    ['nh2_map'],
                    ['cnc_map'],
                    ['ring_map']
                ],
                # 'hspace' 控制这个子网格内部的垂直间距，使其紧凑
                'hspace': 0.05
            }
        }
    }

    # --- 3. 初始化 Plotter ---
    # 直接将定义好的字典传给 layout 参数
    # layout_engine=None 确保我们可以手动控制间距
    plotter = pp.Plotter(layout=nested_layout, figsize=(12, 6), layout_engine=None)
    plotter.set_suptitle("Declarative Nested Layout Example", fontsize=16, weight='bold')

    # --- 4. 填充主图区域 ---
    # 直接使用顶层布局中定义的名字 'main_plot' 作为 tag
    plotter.add_line(data=df_line, x='x', y='y', tag='main_plot'
    ).set_title('Standard Plot'
    ).set_xlabel('X-axis'
    ).set_ylabel('Y-axis')

    # --- 5. 填充子网格区域 ---
    # 使用 '容器名.子图名' 的层级结构来直接引用嵌套的子图
    subgrid_names = ['nh2_map', 'cnc_map', 'ring_map']
    for i, sub_name in enumerate(subgrid_names):
        # 构造层级 tag, e.g., 'heatmap_group.nh2_map'
        hierarchical_tag = f"heatmap_group.{sub_name}"

        plotter.add_heatmap(data=all_heatmap_data[i], tag=hierarchical_tag
        ).set_ylabel(y_labels[i], fontsize=14, weight='bold')

    # --- 6. 对子网格进行精细化设置 ---
    # a. 只在最顶部的子图上添加标题
    plotter.set_title(label='Nested Heatmap Group', tag='heatmap_group.nh2_map', fontsize=14)

    # b. 同时隐藏X轴、Y轴刻度线、Y轴刻度数字
    plotter.hide_axes('heatmap_group.nh2_map', x_axis=True, y_ticks=True, y_tick_labels=True)
    plotter.hide_axes('heatmap_group.cnc_map', x_axis=True, y_ticks=True, y_tick_labels=True)
    plotter.hide_axes('heatmap_group.ring_map', x_axis=True, y_ticks=True, y_tick_labels=True)

    # c. 只在最底部的子图上添加 X 轴标签
    plotter.set_xlabel(label='Time (min)', tag='heatmap_group.ring_map', fontsize=14, weight='bold')

    # --- 7. 保存图像 ---
    plotter.save("declarative_nested_layout.png")

except (pp.PaperPlotError, ValueError, KeyError) as e:
    print(f"\nAn error occurred:\n{e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'declarative_nested_layout.png' was generated.")
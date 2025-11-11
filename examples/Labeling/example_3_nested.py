# examples/Labeling/example_3_nested.py
import paperplot as pp
import pandas as pd

# 1. 定义一个嵌套布局
nested_layout = {
    'main': [['overview', 'details_group']],
    'subgrids': {
        'details_group': {'layout': [['detail_A'], ['detail_B']]}
    }
}

# 2. 初始化 Plotter
plotter = pp.Plotter(layout=nested_layout, figsize=(10, 5))

# 3. 绘制所有子图
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[0,1]}), x='x', y='y', tag='overview')
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[1,0]}), x='x', y='y', tag='details_group.detail_A')
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[0.5,0.5]}), x='x', y='y', tag='details_group.detail_B')

# 4. 标注顶层布局
# 对于复杂的嵌套布局，推荐使用 add_grouped_labels 来清晰地定义顶层分组
plotter.add_grouped_labels(
    groups={
        '(a)': ['overview'],
        '(b)': ['details_group.detail_A', 'details_group.detail_B']
    },
    position='top_left', padding=0.03, fontsize=16
)

# 5. 手动标注子网格内部
# 使用 add_subplot_labels 并明确指定 tags
plotter.add_subplot_labels(
    tags=['details_group.detail_A', 'details_group.detail_B'],
    label_style='numeric',
    template='{label}.',
    position=(0,1),
    fontsize=14
)

# 6. 添加标题并保存
# plotter.set_suptitle("FR4: Nested Layout Labeling", fontsize=16, weight='bold')
plotter.save("example_3_nested.png")

print("Generated example_3_nested.png")

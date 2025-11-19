# examples/Labeling/example_2_grouped.py
import paperplot as pp
import pandas as pd

# 1. 定义一个简单的 2x3 网格布局
plotter = pp.Plotter(layout=(2, 3), figsize=(10, 6))

# 2. 绘制所有子图
for r in range(2):
    for c in range(3):
        tag = f'ax{r}{c}'
        plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[0,1]}), x='x', y='y', tag=tag)

# 3. 定义逻辑分组
# 键是标签文本，值是属于该组的子图 tag 列表
groups = {
    '(a)': ['ax00', 'ax01'],      # 第1、2个子图属于 a 组
    '(b)': ['ax02'],               # 第3个子图属于 b 组
    '(c)': ['ax10', 'ax11', 'ax12'] # 底下一整行属于 c 组
}

# 4. 调用分组标注功能
# add_grouped_labels 会在每组子图的组合边界框外添加标签
plotter.add_grouped_labels(groups=groups, position='top_left', fontsize=16)

# 5. 添加标题并保存
# plotter.set_suptitle("FR3: Logically Grouped Labels", fontsize=16, weight='bold')
plotter.save("example_2_grouped.png")

print("Generated example_2_grouped.png")

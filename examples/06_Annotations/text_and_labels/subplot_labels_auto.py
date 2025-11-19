# examples/Labeling/example_1_auto_mosaic.py
import paperplot as pp
import pandas as pd

# 1. 定义一个马赛克布局
layout = [['A', 'A', 'B'], ['C', 'C', 'C']]

# 2. 初始化 Plotter
# 使用 style='publication' 以获得更清晰的出版风格外观
plotter = pp.Plotter(layout=layout, figsize=(8, 5))

# 3. 在每个区域绘制内容，以激活它们
# 只有被绘制过的子图才会被自动标注
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[0,1]}), x='x', y='y', tag='A')
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[1,0]}), x='x', y='y', tag='B')
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[0.5,0.5]}), x='x', y='y', tag='C')

# 4. 调用自动标注功能
# 在不提供 'tags' 参数时，add_subplot_labels 会自动为所有已绘制的子图按顺序编号
plotter.add_subplot_labels(
    # position=(0, 1),
)

# 5. 添加标题并保存
# plotter.set_suptitle("FR2: Auto-labeling a Mosaic Layout", fontsize=16, weight='bold')
plotter.save("example_1_auto_mosaic.png")

print("Generated example_1_auto_mosaic.png")

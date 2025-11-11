# examples/Labeling/example_4_custom.py
import paperplot as pp
import pandas as pd

# 1. 创建一个简单的 1x2 布局
plotter = pp.Plotter(layout=(1, 2), figsize=(10, 4))

# 2. 绘制子图
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[0,1]}), x='x', y='y', tag='ax00')
plotter.add_line(data=pd.DataFrame({'x':[0,1], 'y':[1,0]}), x='x', y='y', tag='ax01')

# 3. 对第一个子图进行高度可定制化的标注
plotter.add_subplot_labels(
    tags=['ax00'],
    label_style='roman',
    case='upper',
    template='Fig. {label}',
    position=(-0.15, 1.1),
    fontsize=20,
    weight='heavy',
    color='darkred',
    fontfamily='serif',
    # 添加一个半透明的背景框
    bbox=dict(boxstyle='round,pad=0.3', fc='wheat', alpha=0.5)
)
plotter.set_title("Customized Label", tag='ax00')

# 4. 对第二个子图使用不同的自定义样式
plotter.add_subplot_labels(
    tags=['ax01'],
    start_at=1, # 从 'b' 开始
    label_style='alpha',
    template='Panel {label}',
    position=(0.5, 0.5), # 放置在中间
    ha='center', # 水平居中
    va='center', # 垂直居中
    fontsize=24,
    color='blue',
    alpha=0.6
)
plotter.set_title("Another Style", tag='ax01')


# 5. 添加标题并保存
plotter.set_suptitle("FR5: Highly Customized Labels", fontsize=16, weight='bold')
plotter.save("example_4_custom.png")

print("Generated example_4_custom.png")

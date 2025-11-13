# 伪代码/示例代码
# 在 add_figure_example.py 中

# 假设你在 examples/Features_Customization/resources/ 目录下有一张 placeholder_image.png

import paperplot as pp

plotter = pp.Plotter(layout=(2, 4), subplot_aspect=(4,3))
# plotter.set_suptitle("Demonstration of add_figure()", fontsize=16)

for i in range(7):
    image_path = f'add_figure_example_{i+1}.png' # 示例图片路径
    plotter.add_figure(image_path, tag=i+1)

plotter.add_blank(tag=8)
plotter.save("add_figure_example.png")
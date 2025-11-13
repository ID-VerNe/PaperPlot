# 伪代码/示例代码
# 在 add_figure_example.py 中

# 假设你在 examples/Features_Customization/resources/ 目录下有一张 placeholder_image.png

import paperplot as pp

plotter = pp.Plotter(layout=(1, 3), subplot_aspect=(21, 9))
plotter.set_suptitle("Demonstration of add_figure()", fontsize=16)

image_path = './resources/DSC09157.jpg' # 示例图片路径

# 模式一: stretch
plotter.add_figure(image_path=image_path, fit_mode='stretch', tag='ax00')
plotter.set_title("Mode: 'stretch'", tag='ax00')

# 模式二: fit (默认)
plotter.add_figure(image_path=image_path, fit_mode='fit', tag='ax01')
plotter.set_title("Mode: 'fit'", tag='ax01')

# 模式三: cover (如果实现了高级逻辑)
plotter.add_figure(image_path=image_path, fit_mode='cover', tag='ax02')
plotter.set_title("Mode: 'cover'", tag='ax02')

plotter.save("add_figure_example.png")
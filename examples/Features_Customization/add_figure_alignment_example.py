import matplotlib.pyplot as plt
from paperplot import Plotter

# 确保图片路径正确
IMAGE_PATH = 'resources/DSC09157.jpg'

if __name__ == '__main__':
    # 创建一个2x2的布局，figsize设为方形以强制产生留白
    p = Plotter(layout=[['A', 'B'], ['C', 'D']], figsize=(8, 8))

    # 1. 左上对齐
    p.add_figure(IMAGE_PATH, fit_mode='fit', align='top_left', tag='A')
    p.set_title("Align: top_left", tag='A')

    # 2. 右上对齐
    p.add_figure(IMAGE_PATH, fit_mode='fit', align='top_right', tag='B')
    p.set_title("Align: top_right", tag='B')

    # 3. 左下对齐
    p.add_figure(IMAGE_PATH, fit_mode='fit', align='bottom_left', tag='C')
    p.set_title("Align: bottom_left", tag='C')

    # 4. 右下对齐
    p.add_figure(IMAGE_PATH, fit_mode='fit', align='bottom_right', tag='D')
    p.set_title("Align: bottom_right", tag='D')
    
    # 为了美观，可以统一调整一下布局
    # p.fig.tight_layout(pad=3.0)
    p.save("figure_alignment_demonstration.png")

    print("对齐功能演示图已生成。")

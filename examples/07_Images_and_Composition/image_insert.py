import os
import sys
import matplotlib.pyplot as plt
from paperplot import Plotter


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'assets')

# Define the image list
# 文件名为0.5 · DISTANCE 2026 VOL. 01_Page_01.png，只改变page_01后面的计数，一共9张
IMAGE_LIST = [os.path.join(ASSETS_DIR, f'0.5 · DISTANCE 2026 VOL. 01_Page_{i:02d}.png') for i in range(1, 10)]

# Create a plotter object
plotter = Plotter(layout=(3, 3), subplot_aspect=(2, 3))

# 遍历1-9，然后插入图片到plotter对象中
for i in range(1, 10):
    plotter.add_figure(IMAGE_LIST[i-1], fit_mode='fit', tag=f'image{i}')

plotter.save('example.png')
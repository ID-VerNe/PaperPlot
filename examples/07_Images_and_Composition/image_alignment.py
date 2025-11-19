# -*- coding: utf-8 -*-
# examples/image_alignment_example.py

import os
import sys
import matplotlib.pyplot as plt
from paperplot import Plotter

# 获取 assets 目录的绝对路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'assets')
IMAGE_PATH = os.path.join(ASSETS_DIR, 'DSC09157.jpg')

# 检查图片是否存在
if not os.path.exists(IMAGE_PATH):
    print(f"错误：图片文件不存在: {IMAGE_PATH}")
    print(f"请确保 {ASSETS_DIR} 目录下有 DSC09157.jpg 文件")
    sys.exit(1)

p = Plotter(layout=[['A', 'B'], ['C', 'D']], figsize=(8, 8))

p.add_figure(IMAGE_PATH, fit_mode='fit', align='top_left', tag='A')
p.set_title('Top Left', tag='A')

p.add_figure(IMAGE_PATH, fit_mode='fit', align='top_right', tag='B')
p.set_title('Top Right', tag='B')

p.add_figure(IMAGE_PATH, fit_mode='fit', align='bottom_left', tag='C')
p.set_title('Bottom Left', tag='C')

p.add_figure(IMAGE_PATH, fit_mode='fit', align='bottom_right', tag='D')
p.set_title('Bottom Right', tag='D')

p.save('image_alignment_test.png')
plt.close('all')

print("图像对齐示例已保存为 'image_alignment_test.png'")

# -*- coding: utf-8 -*-
# examples/embedding_images_example.py
"""
演示如何使用 add_figure() 方法将图片嵌入到 Plotter 的子图中。
这个示例使用 assets 目录中的 placeholder_image.png。
"""

import os
import sys
import matplotlib.pyplot as plt
import paperplot as pp

# 获取 assets 目录的绝对路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'assets')
IMAGE_PATH = os.path.join(ASSETS_DIR, 'placeholder_image.png')

# 检查图片是否存在
if not os.path.exists(IMAGE_PATH):
    print(f"错误：图片文件不存在: {IMAGE_PATH}")
    print(f"请确保 {ASSETS_DIR} 目录下有 placeholder_image.png 文件")
    sys.exit(1)

print(f"--- Running Example: {__file__} ---")

try:
    # 创建一个 2x2 的网格
    plotter = pp.Plotter(layout=(2, 2), figsize=(10, 10))
    plotter.set_suptitle("Demonstration of add_figure()", fontsize=16)

    # 在 4 个子图中嵌入相同的图片，使用不同的填充模式
    plotter.add_figure(IMAGE_PATH, tag='ax00', fit_mode='fit').set_title('Fit Mode', tag='ax00')
    plotter.add_figure(IMAGE_PATH, tag='ax01', fit_mode='cover').set_title('Cover Mode', tag='ax01')
    plotter.add_figure(IMAGE_PATH, tag='ax10', fit_mode='stretch').set_title('Stretch Mode', tag='ax10')
    plotter.add_figure(IMAGE_PATH, tag='ax11', fit_mode='fit', align='top_left').set_title('Fit + Align', tag='ax11')

    # 保存结果
    plotter.save("embedding_images_example.png")
    print("图像嵌入示例已保存为 'embedding_images_example.png'")

except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")

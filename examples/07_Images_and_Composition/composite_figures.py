# -*- coding: utf-8 -*-
# examples/composite_figure_example.py

import os
import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
def generate_spectra_data(label):
    x = np.linspace(400, 1800, 200)
    y = 10 * np.exp(-((x - 1000)**2) / 50000) + np.random.randn(200) * 0.5
    return pd.DataFrame({'x': x, 'y': y, 'label': label})

df1 = generate_spectra_data('Sample A')
df2 = generate_spectra_data('Sample B')

# PCA 数据
df_pca = pd.DataFrame({
    'PC1': np.random.randn(50),
    'PC2': np.random.randn(50),
    'group': ['Group 1'] * 25 + ['Group 2'] * 25
})

# --- 2. 定义 L 型布局 ---
layout = [
    ['SERS_Spectra', 'SERS_Spectra'],
    ['PCA_Result', '.' ]
]

try:
    # --- 3. 创建 Plotter ---
    plotter = pp.Plotter(layout=layout, figsize=(12, 8))
    plotter.set_suptitle("Composite Figure: SERS Spectra + PCA Analysis", fontsize=16, weight='bold')

    # --- 4. 在 SERS_Spectra 区域绘制光谱数据 ---
    ax_sers = plotter.get_ax_by_name('SERS_Spectra')
    
    # 添加两条光谱线
    plotter.add_line(data=df1, x='x', y='y', ax=ax_sers, tag='spectra_A', label='Sample A')
    plotter.add_line(data=df2, x='x', y='y', ax=ax_sers, tag='spectra_B', label='Sample B')
    
    plotter.set_title('SERS Spectra Comparison', tag='spectra_A')
    plotter.set_xlabel('Raman Shift (cm$ ^{-1} $)', tag='spectra_A')
    plotter.set_ylabel('Intensity (a.u.)', tag='spectra_A')
    plotter.set_legend(tag='spectra_A')

    # --- 5. 在 PCA_Result 区域绘制 PCA 散点图 ---
    ax_pca = plotter.get_ax_by_name('PCA_Result')
    
    # 使用 seaborn 的 scatterplot 来绘制分组散点图
    import seaborn as sns
    plotter.add_seaborn(
        plot_func=sns.scatterplot,
        data=df_pca,
        x='PC1',
        y='PC2',
        hue='group',
        ax=ax_pca,
        tag='pca'
    ).set_title('PCA of Spectral Data'
    ).set_xlabel('Principal Component 1'
    ).set_ylabel('Principal Component 2')

    # --- 6. 添加 inset 图像到 SERS_Spectra 子图 ---
    print("Adding an inset image to the 'SERS_Spectra' plot...")
    
    # 获取 assets 目录的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')
    image_path = os.path.join(assets_dir, 'placeholder_image.png')
    
    # 检查图片是否存在
    if os.path.exists(image_path):
        # 添加 inset 作为 zoom_inset（演示目的）
        # 注意：使用正确的 tag 'spectra_A'，这是我们之前创建的 tag
        inset_rect = [0.6, 0.6, 0.25, 0.25]  # [x, y, width, height] in axes coordinates
        inset_ax = plotter.fig.add_axes(inset_rect)
        
        # 在 inset 中显示图片
        import matplotlib.image as mpimg
        img = mpimg.imread(image_path)
        inset_ax.imshow(img)
        inset_ax.axis('off')
        inset_ax.set_title('Inset Image', fontsize=8)
    else:
        print(f"Note: Placeholder image not found at {image_path}, skipping inset.")

    # --- 7. 保存图像 ---
    plotter.save("composite_figure.png")

except Exception as e:
    print(f"\nAn error occurred:\n{e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'composite_figure.png' was generated.")
print("Check for the L-shaped layout and the inset image in the top-right plot.")

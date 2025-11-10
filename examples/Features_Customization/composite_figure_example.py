# examples/composite_figure_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
def generate_spectra_data(label):
    x = np.linspace(400, 1800, 200)
    peak_pos = np.random.uniform(600, 1600)
    peak_width = np.random.uniform(50, 150)
    peak_intensity = np.random.uniform(0.5, 1)
    y = peak_intensity * np.exp(-((x - peak_pos)**2) / (2 * peak_width**2)) + np.random.rand(200) * 0.1
    return pd.DataFrame({'wavenumber': x, 'intensity': y, 'label': label})

df1 = generate_spectra_data('Sample A')
df2 = generate_spectra_data('Sample B')

df_pca = pd.DataFrame({
    'PC1': np.random.randn(50),
    'PC2': np.random.randn(50),
    'cluster': np.random.choice(['Group 1', 'Group 2', 'Group 3'], 50)
})

# --- 2. 定义一个带空白占位符的复杂布局 ---
# 我们创建一个 L 型布局，右下角是空白的
layout = [
    ['SERS_Spectra', 'SERS_Spectra'],
    ['PCA_Result', '.']  # '.' 代表空白区域
]

try:
    plotter = pp.Plotter(layout=layout, figsize=(10, 8))
    plotter.set_suptitle("Composite Figure with Inset Image", fontsize=16, weight='bold')

    # --- 3. 在 SERS 图区域绘图 ---
    # 由于 'SERS_Spectra' 占据了两个单元格，我们通过 get_ax_by_name 获取合并后的 Axes
    ax_sers = plotter.get_ax_by_name('SERS_Spectra')
    # 在同一个 Axes 上绘制两条光谱
    plotter.add_line(data=df1, x='wavenumber', y='intensity', ax=ax_sers, tag='spectra_A', label='Sample A')
    plotter.add_line(data=df2, x='wavenumber', y='intensity', ax=ax_sers, tag='spectra_B', label='Sample B'
    ).set_title('SERS Spectra of Samples'  # The last plot call sets the active context
    ).set_xlabel('Wavenumber (cm⁻¹)'
    ).set_ylabel('Intensity (a.u.)'
    ).set_legend()

    # --- 4. 在 SERS 图上嵌入占位符图片 ---
    print("Adding an inset image to the 'SERS_Spectra' plot...")
    try:
        # 给run_all_examples.py的专用路径，防止报错找不到插入的图片
        plotter.add_inset_image(
            host_tag='spectra_A',
            image_path='./examples/Features_Customization/resources/placeholder_image.png',
            rect=[0.7, 0.65, 0.28, 0.28] # [x, y, width, height] in relative coordinates
        )
    except:
        plotter.add_inset_image(
            host_tag='spectra_A',
            image_path='./resources/placeholder_image.png',
            rect=[0.7, 0.65, 0.28, 0.28]  # [x, y, width, height] in relative coordinates
        )

    # --- 5. 在 PCA 图区域绘图 ---
    ax_pca = plotter.get_ax_by_name('PCA_Result')
    # 使用 add_seaborn 绘制分组散点图
    import seaborn as sns
    plotter.add_seaborn(
        plot_func=sns.scatterplot, 
        data=df_pca, 
        x='PC1', 
        y='PC2', 
        hue='cluster',
        ax=ax_pca, 
        tag='pca'
    ).set_title('PCA of Spectral Data'
    ).set_xlabel('Principal Component 1'
    ).set_ylabel('Principal Component 2')

    # --- 6. 清理和保存 ---
    plotter.cleanup(align_labels=True)
    plotter.save("composite_figure.png")

except (pp.PaperPlotError, FileNotFoundError, ValueError) as e:
    print(f"\nAn error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'composite_figure.png' was generated.")
print("Check for the L-shaped layout and the inset image in the top-right plot.")

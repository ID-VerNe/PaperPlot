# examples/domain_specific_plots_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.decomposition import PCA

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---

# SERS 光谱数据
def generate_spectra_data(num_spectra=3):
    x = np.linspace(400, 1800, 500)
    df = pd.DataFrame({'wavenumber': x})
    for i in range(num_spectra):
        peak_pos = np.random.uniform(600, 1600)
        peak_width = np.random.uniform(50, 150)
        peak_intensity = np.random.uniform(0.5, 1)
        noise = np.random.rand(500) * 0.05
        y = peak_intensity * np.exp(-((x - peak_pos)**2) / (2 * peak_width**2)) + noise
        df[f'Sample_{i+1}'] = y
    return df

spectra_df = generate_spectra_data()

# 机器学习数据
y_true = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])
y_score = np.random.rand(12, 3) # 模拟分类器的得分输出
y_pred = np.argmax(y_score, axis=1)
class_names = ['Class A', 'Class B', 'Class C']

# 混淆矩阵
cm = confusion_matrix(y_true, y_pred)

# ROC 曲线数据
y_true_bin = label_binarize(y_true, classes=[0, 1, 2])
n_classes = y_true_bin.shape[1]
fpr, tpr, roc_auc = dict(), dict(), dict()
for i in range(n_classes):
    fpr[class_names[i]], tpr[class_names[i]], _ = roc_curve(y_true_bin[:, i], y_score[:, i])
    roc_auc[class_names[i]] = auc(fpr[class_names[i]], tpr[class_names[i]])

# PCA 数据
pca_data = np.random.rand(50, 10)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(pca_data)
pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
pca_df['Category'] = np.random.choice(['Group X', 'Group Y'], 50)


# --- 2. 创建一个 2x2 的布局 ---
try:
    plotter = pp.Plotter(layout=(2, 2), figsize=(12, 10))
    plotter.set_suptitle("Domain-Specific Plotting Functions", fontsize=16, weight='bold')

    # --- Top-Left: SERS 光谱 ---
    y_cols = [col for col in spectra_df.columns if col.startswith('Sample')]
    plotter.add_spectra(
        data=spectra_df, x='wavenumber', y_cols=y_cols, tag='spectra', offset=0.5
    ).set_title('SERS Spectra with Offset'
    ).set_xlabel('Wavenumber (cm⁻¹)'
    ).set_ylabel('Intensity (a.u.)'
    ).set_legend()

    # --- Top-Right: 混淆矩阵 ---
    plotter.add_confusion_matrix(
        matrix=cm, class_names=class_names, tag='cm', normalize=True
    ).set_title('Normalized Confusion Matrix')

    # --- Bottom-Left: ROC 曲线 ---
    # add_roc_curve 已经设置了大部分标题和标签，我们也可以覆盖它们
    plotter.add_roc_curve(
        fpr=fpr, tpr=tpr, roc_auc=roc_auc, tag='roc'
    ).set_title('Multi-Class ROC Curves')

    # --- Bottom-Right: PCA 散点图 ---
    plotter.add_pca_scatter(
        data=pca_df, x_pc='PC1', y_pc='PC2', hue='Category', tag='pca'
    ).set_title('PCA Scatter Plot'
    ).set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]:.1%})'
    ).set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]:.1%})')


    # --- 5. 清理和保存 ---
    plotter.cleanup(align_labels=True)
    plotter.save("domain_specific_plots.png")

except (pp.PaperPlotError, ValueError) as e:
    print(f"\nAn error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("An updated file 'domain_specific_plots.png' was generated with 4 plots.")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 消融实验数据：3 个部件，组合数 = 4 (全集 + 逐个移除)
# 组合顺序约定: [全集, 移除 Transfer, 移除 Contrastive, 移除 Pretrain]
components = ['Transfer', 'Contrastive', 'Pretrain']
scores = [
    [0.92, 0.88, 0.85, 0.78],  # Accuracy
    [0.75, 0.70, 0.68, 0.61],  # F1
]
metrics = ['Accuracy', 'F1']

try:
    # 布局 1x3：两个指标面板 + 一个图例面板 (figures4papers 式 1×(N+1) 布局)
    # 使用 figures4papers 主题：无衬线、无网格、粗 spine
    plotter = pp.Plotter(layout=(1, 3), figsize=(14, 5), style='figures4papers')
    plotter.set_suptitle("Ablation Study (alpha encodes method completeness)", fontsize=16, weight='bold')

    # 语义调色板：蓝 = 本文方法 (proposed)
    plotter.set_palette(pp.SEMANTIC_PALETTE_LIST)

    # 一次调用画两个指标面板，alpha 从深(全集)到浅(消融最多)
    plotter.add_ablation_barh(
        components=components,
        scores=scores,
        metrics=metrics,
        tags=['m1', 'm2'],
        baseline_label='Full model',
        edgecolor='black',
        linewidth=1.5,
    )

    # 第三个子图作图例专用面板：关闭坐标轴，合并两个指标面板的图例
    plotter.add_legend_panel(tag='ax02', source_tag=['m1', 'm2'], fontsize=14)

    plotter.save("ablation_barh_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'ablation_barh_example.png' was generated.")

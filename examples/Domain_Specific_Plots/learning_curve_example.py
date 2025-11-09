# examples/learning_curve_example.py

import paperplot as pp
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 模拟 scikit-learn 中 learning_curve 函数的输出
np.random.seed(0)
train_sizes = np.linspace(.1, 1.0, 5)
n_folds = 5
n_ticks = len(train_sizes)

# 模拟一个欠拟合模型的得分
train_scores_underfit = np.random.rand(n_ticks, n_folds) * 0.1 + 0.6
test_scores_underfit = np.random.rand(n_ticks, n_folds) * 0.1 + 0.55

# 模拟一个理想模型的得分
train_scores_good = 0.95 - np.logspace(-1, -2, n_ticks)[:, np.newaxis] * (0.1 + np.random.rand(n_ticks, n_folds) * 0.1)
test_scores_good = 0.9 - np.logspace(-1, -2, n_ticks)[:, np.newaxis] * (0.1 + np.random.rand(n_ticks, n_folds) * 0.1)

# 模拟一个过拟合模型的得分
train_scores_overfit = np.ones((n_ticks, n_folds)) * 0.99 - np.random.rand(n_ticks, n_folds) * 0.01
test_scores_overfit = 0.7 - np.linspace(0, 0.2, n_ticks)[:, np.newaxis] + np.random.rand(n_ticks, n_folds) * 0.05


# --- 2. 创建绘图 ---
try:
    plotter = pp.Plotter(layout=(1, 3), figsize=(18, 5))
    plotter.set_suptitle("Learning Curve Examples", fontsize=16, weight='bold')

    # --- 3. 绘制三个学习曲线 ---
    # 理想模型
    ax_good = plotter.get_ax_by_name('ax00')
    pp.utils.plot_learning_curve(
        ax=ax_good,
        train_sizes=train_sizes * 1000, # 假设最多1000个样本
        train_scores=train_scores_good,
        test_scores=test_scores_good,
        title='Good Fit',
        color='blue'
    )
    plotter.tag_to_ax['good_fit'] = ax_good # 手动关联tag

    # 欠拟合模型
    ax_underfit = plotter.get_ax_by_name('ax01')
    pp.utils.plot_learning_curve(
        ax=ax_underfit,
        train_sizes=train_sizes * 1000,
        train_scores=train_scores_underfit,
        test_scores=test_scores_underfit,
        title='Underfitting',
        color='orange'
    )
    plotter.tag_to_ax['underfit'] = ax_underfit

    # 过拟合模型
    ax_overfit = plotter.get_ax_by_name('ax02')
    pp.utils.plot_learning_curve(
        ax=ax_overfit,
        train_sizes=train_sizes * 1000,
        train_scores=train_scores_overfit,
        test_scores=test_scores_overfit,
        title='Overfitting',
        color='red'
    )
    plotter.tag_to_ax['overfit'] = ax_overfit
    
    # --- 4. 统一Y轴范围以便比较 ---
    plotter.set_ylim('good_fit', 0.4, 1.05)
    plotter.set_ylim('underfit', 0.4, 1.05)
    plotter.set_ylim('overfit', 0.4, 1.05)

    # --- 5. 清理和保存 ---
    plotter.cleanup()
    plotter.save("learning_curve_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'learning_curve_example.png' was generated.")

# examples/Styles_Aesthetics/style_gallery_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from paperplot.utils import list_available_styles

print(f"--- Running Example: {__file__} ---")


# --- 1. 准备更多样化的数据，以更好地展示不同图表 ---
def generate_demo_data():
    """为不同图表类型生成多样化的数据。"""
    np.random.seed(42)  # 确保每次运行数据都一样

    # 线图数据 (5条线，以展示更多颜色)
    x_line = np.linspace(0, 10, 50)
    df_line = pd.DataFrame({'x': x_line})
    for i in range(5):
        df_line[f'y{i}'] = np.sin(x_line + i * np.pi / 4) + np.random.randn(50) * 0.1

    # 柱状图数据
    df_bar = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'value': np.random.rand(5) * 10 + 5,
        'error': np.random.rand(5) * 2
    })

    # 散点图 和 小提琴图 共用数据
    df_dist = pd.DataFrame({
        'x_dim': np.random.randn(150),
        'y_dim': np.random.randn(150) * 1.5 + 2,
        'group': np.random.choice(['G1', 'G2', 'G3'], 150)
    })

    # 热图数据
    df_heatmap = pd.DataFrame(np.random.rand(8, 12))

    return df_line, df_bar, df_dist, df_heatmap


# --- 2. 定义一个函数，为指定风格创建一个全面的展示图表 ---
def create_plot_for_style(style_name: str, df_line, df_bar, df_dist, df_heatmap):
    """为给定的样式名称创建一个 2x3 的组合展示图并保存。"""
    print(f"Generating comprehensive 2x3 plot for style: '{style_name}'...")
    try:
        plotter = pp.Plotter(layout=(2, 3), style=style_name, figsize=(18, 10))
        plotter.set_suptitle(f"Style Showcase: '{style_name}'", fontsize=22, weight='bold')

        # --- 在网格中填充所有图表 ---

        # Top-Left (ax00): Line Plot
        y_cols = [f'y{i}' for i in range(5)]
        plotter.add_spectra(data=df_line, x='x', y_cols=y_cols, tag='ax00', offset=0)
        plotter.set_title('Line Plot', tag='ax00').set_xlabel('X-axis').set_ylabel('Y-axis').set_legend()

        # Top-Middle (ax01): Bar Chart
        plotter.add_bar(data=df_bar, x='category', y='value', y_err='error', tag='ax01', capsize=4)
        plotter.set_title('Bar Chart', tag='ax01').set_xlabel('Category').set_ylabel('Value')



        # Top-Right (ax02): Heatmap
        plotter.add_heatmap(data=df_heatmap, tag='ax02', cbar=True)
        plotter.set_title('Heatmap', tag='ax02').set_xlabel('Column').set_ylabel('Row')

        # Bottom-Left (ax10): Scatter Plot
        import seaborn as sns
        plotter.add_seaborn(
            plot_func=sns.scatterplot,
            data=df_dist, x='x_dim', y='y_dim', hue='group',
            tag='ax10'
        )
        plotter.set_title('Scatter Plot (with Hue)', tag='ax10').set_xlabel('X Dim').set_ylabel('Y Dim')

        # Bottom-Middle (ax11): Violin Plot
        plotter.add_violin(data=df_dist, x='group', y='y_dim', tag='ax11')
        plotter.set_title('Violin Plot', tag='ax11').set_xlabel('Group').set_ylabel('Value Distribution')

        # Bottom-Right (ax12): Color Palette
        ax_palette = plotter.get_ax('ax12')
        ax_palette.set_title('Color Palette')

        try:
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

            for i, color in enumerate(colors):
                rect = plt.Rectangle((0.1, 0.9 - i * 0.08), 0.2, 0.06, facecolor=color)
                ax_palette.add_patch(rect)
                ax_palette.text(0.35, 0.9 - i * 0.08 + 0.03, f'Color {i}: {color}',
                                va='center', fontsize=12)

            ax_palette.set_xlim(0, 1)
            ax_palette.set_ylim(0, 1)
            ax_palette.axis('off')

        except KeyError:
            ax_palette.text(0.5, 0.5, 'No color cycle found\nin this style.',
                            ha='center', va='center', style='italic')
            ax_palette.axis('off')

        # --- 保存图像 ---
        filename = f"style_gallery_{style_name}.png"
        plotter.save(filename)
        print(f"  -> Saved {filename}")

    except Exception as e:
        print(f"  -> An unexpected error occurred for style '{style_name}': {e}")
    finally:
        plt.close('all')


# --- 主程序 ---
# 1. 一次性生成所有需要的数据
df_line, df_bar, df_dist, df_heatmap = generate_demo_data()

# 2. 获取所有可用的样式
styles_to_showcase = list_available_styles()
print(f"Found {len(styles_to_showcase)} styles to showcase: {styles_to_showcase}")


styles_not_to_showcase = [
    'publication',
    'presentation',
    'flat',
    'nord',
    'solarized_light'
]

# 3. 循环为每个样式创建展示图
for style in styles_to_showcase:
    # 跳过不要的样式
    if style in styles_not_to_showcase:
        continue
    create_plot_for_style(style, df_line, df_bar, df_dist, df_heatmap)

print(f"\n--- Finished Example: {__file__} ---")
import pandas as pd
import numpy as np
import paperplot as pp
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")


# 步骤 1: 准备模拟数据
def prepare_data():
    """创建三组模拟数据"""
    # 主分析图 (Plot A) 数据: 带噪声的正弦波
    time = np.linspace(0, 10, 100)
    signal = np.sin(time * 1.2) * np.exp(-time / 5) + np.random.normal(0, 0.05, 100)
    df_main = pd.DataFrame({'time': time, 'signal': signal})

    # 双Y轴图 (Plot B) 数据: 温度和压力
    time_b = np.linspace(0, 10, 50)
    temperature = 20 + 5 * np.cos(time_b) + np.random.normal(0, 0.5, 50)
    pressure = 101.3 + 2 * np.sin(time_b * 2) + np.random.normal(0, 0.3, 50)
    df_temp = pd.DataFrame({'time': time_b, 'temperature': temperature})
    df_pressure = pd.DataFrame({'time': time_b, 'pressure': pressure})

    # 子网格 (Plot C1, C2) 数据
    # C1: 柱状图数据
    categories = ['Alpha', 'Beta', 'Gamma', 'Delta']
    counts = [30, 45, 25, 55]
    df_bar = pd.DataFrame({'category': categories, 'count': counts})

    # C2: 散点图数据
    x_val = np.random.rand(40) * 10
    y_val = 0.5 * x_val + np.random.normal(0, 1.5, 40)
    df_scatter = pd.DataFrame({'x_val': x_val, 'y_val': y_val})

    return df_main, df_temp, df_pressure, df_bar, df_scatter


try:
    # 步骤 2: 定义布局
    nested_layout = {
        'main': [
            ['main_plot', 'side_plots']
        ],
        'subgrids': {
            'side_plots': {
                # The layout for 'side_plots' is another nested layout
                'layout': {
                    'main': [
                        ['twin_axis_plot'],
                        ['subgrid_group']
                    ],
                    'subgrids': {
                        'subgrid_group': {
                            'layout': [['detail_A', 'detail_B']],
                            'wspace': 0.02
                        }
                    }
                },
                'hspace': 0.4,
                'height_ratios': [1, 1]
            }
        },
        'col_ratios': [2, 1.5]
    }

    # 获取数据
    df_main, df_temp, df_pressure, df_bar, df_scatter = prepare_data()

    # 步骤 3 & 4: 初始化 Plotter, 绘制并标注
    plotter = pp.Plotter(layout=nested_layout, figsize=(12, 7))

    (
        plotter
        .set_suptitle("Advanced Layout Showcase: Mosaic, Nesting, and Twin-Axis", fontsize=18, weight='bold')

        # 绘制主图 (Plot A)
        .add_line(data=df_main, x='time', y='signal', tag='main_plot')
        .set_title('Main Analysis: Time-Series Signal', tag='main_plot')
        .set_xlabel('Time (s)', tag='main_plot')
        .set_ylabel('Signal Value', tag='main_plot')

        # 绘制双Y轴图 (Plot B)
        .add_line(data=df_temp, x='time', y='temperature', tag='side_plots.twin_axis_plot', label='Temperature')
        .set_title('Correlated Variables (Twin-Axis)', tag='side_plots.twin_axis_plot')
        .set_ylabel('Temperature (°C)', tag='side_plots.twin_axis_plot')
        .tick_params(axis='y', tag='side_plots.twin_axis_plot')
        .add_twinx(tag='side_plots.twin_axis_plot')
        .add_line(data=df_pressure, x='time', y='pressure', label='Pressure')
        .set_ylabel('Pressure (kPa)')
        .tick_params(axis='y')
        .target_primary(tag='side_plots.twin_axis_plot')
        .set_legend(frameon=False, tag='side_plots.twin_axis_plot')

        # 绘制子网格 (Plot C1, C2)
        .add_bar(data=df_bar, x='category', y='count', tag='side_plots.subgrid_group.detail_A')
        .set_title('Category Counts', tag='side_plots.subgrid_group.detail_A')
        .set_xlabel('Category', tag='side_plots.subgrid_group.detail_A')
        .set_ylabel('Count', tag='side_plots.subgrid_group.detail_A')

        .add_scatter(data=df_scatter, x='x_val', y='y_val', tag='side_plots.subgrid_group.detail_B', alpha=0.7)
        .set_title('Detail Scatter', tag='side_plots.subgrid_group.detail_B')
        .set_xlabel('X Value', tag='side_plots.subgrid_group.detail_B')
        .set_ylabel('Y Value', tag='side_plots.subgrid_group.detail_B')

        # 步骤 5: 添加标注与收尾
        .add_grouped_labels(groups={'a': ['main_plot'],
                                    'b': ['side_plots.twin_axis_plot', 'side_plots.subgrid_group.detail_A',
                                          'side_plots.subgrid_group.detail_B']}, fontsize=14)
        .add_subplot_labels(tags=['side_plots.twin_axis_plot', 'side_plots.subgrid_group.detail_A',
                                  'side_plots.subgrid_group.detail_B'],
                            label_style='numeric',
                            template='{label}.',
                            position=(0.05, 1),
                            )

        # .cleanup(auto_share=True)
    )

    # 使用 "逃生舱口" get_ax() 进行高级定制
    main_ax = plotter.get_ax('main_plot')
    main_ax.grid(True, linestyle='--', alpha=0.6)

    # 保存图像
    plotter.save("1_layout_showcase.png")


except (pp.PaperPlotError, ValueError, KeyError) as e:
    print(f"\nAn error occurred:\n{e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file '1_layout_showcase.png' was generated in the root directory.")

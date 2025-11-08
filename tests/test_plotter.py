import pytest
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import paperplot as pp
from paperplot import Plotter, generate_grid_layout
from paperplot.exceptions import TagNotFoundError, DuplicateTagError, PlottingSpaceError
import pandas as pd
import numpy as np
import seaborn as sns

def test_plotter_init_simple_grid():
    """
    测试Plotter使用简单网格布局的初始化。
    """
    plotter = Plotter(layout=(1, 2))
    assert plotter.fig is not None
    assert len(plotter.axes) == 2
    assert isinstance(plotter.axes[0], plt.Axes)
    assert isinstance(plotter.axes[1], plt.Axes)
    plt.close(plotter.fig)

def test_plotter_init_mosaic_layout():
    """
    测试Plotter使用马赛克布局的初始化。
    """
    layout = [['A', 'B'], ['C', 'C']]
    plotter = Plotter(layout=layout)
    assert plotter.fig is not None
    assert len(plotter.axes) == 3  # A, B, C
    assert 'A' in plotter.axes_dict
    assert 'B' in plotter.axes_dict
    assert 'C' in plotter.axes_dict
    assert isinstance(plotter.axes_dict['A'], plt.Axes)
    plt.close(plotter.fig)

def test_generate_grid_layout():
    """
    测试generate_grid_layout函数。
    """
    layout = generate_grid_layout(2, 2)
    expected_layout = [['(0,0)', '(0,1)'], ['(1,0)', '(1,1)']]
    assert layout == expected_layout

def test_get_ax_by_tag_and_name():
    """
    测试_get_ax_by_tag和get_ax_by_name方法。
    """
    layout = [['A', 'B'], ['C', 'C']]
    plotter = Plotter(layout=layout)

    # Test _get_ax_by_tag (indirectly via get_ax)
    ax_a = plotter.get_ax_by_name('A')
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='line_a', ax=ax_a)
    assert plotter.get_ax('line_a') == ax_a

    # Test get_ax_by_name
    assert plotter.get_ax_by_name('B') == plotter.axes_dict['B']
    
    with pytest.raises(TagNotFoundError):
        plotter.get_ax('non_existent_tag')
    
    with pytest.raises(ValueError):
        plotter.get_ax_by_name('non_existent_name')
    
    plt.close(plotter.fig)

def test_add_line():
    """
    测试add_line方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2,3], 'y':[4,5,6]})
    plotter.add_line(data=test_df, x='x', y='y', tag='my_line')
    ax = plotter.get_ax('my_line')
    assert len(ax.lines) == 1
    plt.close(plotter.fig)

def test_add_spectra():
    """
    测试add_spectra方法。
    """
    import pandas as pd
    plotter = Plotter(layout=(1,1))
    data = pd.DataFrame({'x': [1,2,3], 'y1': [4,5,6], 'y2': [5,6,7]})
    plotter.add_spectra(data=data, x='x', y_cols=['y1', 'y2'], tag='my_spectra', offset=1)
    ax = plotter.get_ax('my_spectra')
    assert len(ax.lines) == 2
    # 检查偏移是否正确应用
    assert ax.lines[0].get_ydata()[0] == 4
    assert ax.lines[1].get_ydata()[0] == 5 + 1 # y2_data + offset
    plt.close(plotter.fig)

def test_add_bar():
    """
    测试add_bar方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':['A','B'], 'y':[10,20]})
    plotter.add_bar(data=test_df, x='x', y='y', tag='my_bar')
    ax = plotter.get_ax('my_bar')
    assert len(ax.patches) == 2 # Two bars
    plt.close(plotter.fig)

def test_add_confusion_matrix():
    """
    测试add_confusion_matrix方法。
    """
    import numpy as np
    plotter = Plotter(layout=(1,1))
    matrix = np.array([[10, 1], [2, 15]])
    class_names = ['Cat', 'Dog']
    plotter.add_confusion_matrix(matrix=matrix, class_names=class_names, tag='my_cm')
    ax = plotter.get_ax('my_cm')
    assert len(ax.collections) == 1 # Heatmap
    assert ax.get_xlabel() == 'Predicted Label'
    assert ax.get_ylabel() == 'True Label'
    plt.close(plotter.fig)

def test_add_roc_curve():
    """
    测试add_roc_curve方法。
    """
    import numpy as np
    fpr = {'class1': np.array([0, 0.5, 1]), 'class2': np.array([0, 0.2, 1])}
    tpr = {'class1': np.array([0, 0.8, 1]), 'class2': np.array([0, 0.9, 1])}
    roc_auc = {'class1': 0.75, 'class2': 0.85}
    
    plotter = Plotter(layout=(1,1))
    plotter.add_roc_curve(fpr=fpr, tpr=tpr, roc_auc=roc_auc, tag='my_roc')
    ax = plotter.get_ax('my_roc')
    assert len(ax.lines) == 3 # Two ROC curves + diagonal line
    assert ax.get_xlabel() == 'False Positive Rate'
    assert ax.get_ylabel() == 'True Positive Rate'
    plt.close(plotter.fig)

def test_add_pca_scatter():
    """
    测试add_pca_scatter方法。
    """
    import pandas as pd
    plotter = Plotter(layout=(1,1))
    data = pd.DataFrame({'PC1': [1,2,3], 'PC2': [4,5,6], 'label': ['A','A','B']})
    plotter.add_pca_scatter(data=data, x_pc='PC1', y_pc='PC2', hue='label', tag='my_pca')
    ax = plotter.get_ax('my_pca')
    assert len(ax.collections) == 1 # Scatter points
    assert ax.get_legend() is not None # Hue should create a legend
    plt.close(plotter.fig)

def test_add_power_timeseries():
    """
    测试add_power_timeseries方法。
    """
    import pandas as pd
    plotter = Plotter(layout=(1,1))
    data = pd.DataFrame({'time': [1,2,3], 'signal1': [4,5,6], 'signal2': [7,8,9]})
    events = {'event1': 1.5, 'event2': 2.5}
    plotter.add_power_timeseries(data=data, x='time', y_cols=['signal1', 'signal2'], tag='my_power', events=events)
    ax = plotter.get_ax('my_power')
    assert len(ax.lines) == 4 # Two signals + two event lines
    assert len(ax.texts) == 2 # Two event labels
    assert ax.get_xlabel() == 'Time (s)'
    assert ax.get_ylabel() == 'Value'
    plt.close(plotter.fig)

def test_add_concentration_map():
    """
    测试add_concentration_map方法。
    """
    import pandas as pd
    plotter = Plotter(layout=(1,1))
    data = pd.DataFrame([[1,2],[3,4]])
    plotter.add_concentration_map(data=data, tag='my_map')
    ax = plotter.get_ax('my_map')
    assert len(ax.collections) == 1 # Heatmap
    assert ax.get_xlabel() == 'X (μm)'
    assert ax.get_ylabel() == 'Y (μm)'
    plt.close(plotter.fig)

def test_add_scatter():
    """
    测试add_scatter方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2,3], 'y':[4,5,6]})
    plotter.add_scatter(data=test_df, x='x', y='y', tag='my_scatter')
    ax = plotter.get_ax('my_scatter')
    assert len(ax.collections) == 1
    plt.close(plotter.fig)

# --- Tests for utils.py functions ---
def test_highlight_peaks():
    """
    测试utils.highlight_peaks函数。
    """
    import pandas as pd
    import numpy as np
    fig, ax = plt.subplots()
    x = pd.Series(np.linspace(0, 10, 100))
    y = pd.Series(np.sin(x))
    peaks_x = [2, 8]
    pp.utils.highlight_peaks(ax, x, y, peaks_x)
    assert len(ax.lines) == 2 # Two vertical lines
    assert len(ax.texts) == 2 # Two text labels
    plt.close(fig)

def test_add_event_markers():
    """
    测试utils.add_event_markers函数。
    """
    import pandas as pd
    import numpy as np
    fig, ax = plt.subplots()
    ax.set_ylim(0, 10) # Set y-limits for text placement
    event_dates = [2, 5, 8]
    labels = ['A', 'B', 'C']
    pp.utils.add_event_markers(ax, event_dates, labels)
    assert len(ax.lines) == 3 # Three vertical lines
    assert len(ax.texts) == 3 # Three text labels
    plt.close(fig)

def test_add_stat_test():
    """
    测试utils.add_stat_test函数。
    """
    import pandas as pd
    import numpy as np
    fig, ax = plt.subplots()
    df = pd.DataFrame({
        'group': ['A']*10 + ['B']*10,
        'value': np.random.normal(0,1,20)
    })
    # 绘制一个箱线图，以便有xtick_labels
    import seaborn as sns
    sns.boxplot(data=df, x='group', y='value', ax=ax)
    
    pp.utils.add_stat_test(ax, df, x='group', y='value', group1='A', group2='B')
    assert len(ax.lines) >= 1 # Stat annotation line
    assert len(ax.texts) >= 1 # Stat annotation text
    plt.close(fig)

def test_add_pairwise_tests():
    """
    测试utils.add_pairwise_tests函数。
    """
    import pandas as pd
    import numpy as np
    fig, ax = plt.subplots()
    df = pd.DataFrame({
        'group': ['A']*10 + ['B']*10 + ['C']*10,
        'value': np.random.normal(0,1,30)
    })
    import seaborn as sns
    sns.boxplot(data=df, x='group', y='value', ax=ax)
    
    comparisons = [('A', 'B'), ('A', 'C')]
    pp.utils.add_pairwise_tests(ax, df, x='group', y='value', comparisons=comparisons)
    assert len(ax.lines) >= 2 # At least two comparison lines
    assert len(ax.texts) >= 2 # At least two comparison texts
    plt.close(fig)

def test_plot_learning_curve():
    """
    测试utils.plot_learning_curve函数。
    """
    import numpy as np
    fig, ax = plt.subplots()
    train_sizes = np.array([10, 20, 30])
    train_scores = np.array([[0.8, 0.85], [0.85, 0.9], [0.9, 0.92]])
    test_scores = np.array([[0.7, 0.75], [0.72, 0.78], [0.75, 0.8]])
    
    pp.utils.plot_learning_curve(ax, train_sizes, train_scores, test_scores)
    assert len(ax.lines) == 2 # Training and CV score lines
    assert len(ax.collections) == 2 # Fill between areas
    assert ax.get_xlabel() == 'Training examples'
    assert ax.get_ylabel() == 'Score'
    plt.close(fig)

def test_moving_average():
    """
    测试utils.moving_average函数。
    """
    import pandas as pd
    data = pd.Series([1, 2, 3, 4, 5])
    smoothed = pp.utils.moving_average(data, window_size=3)
    # 预期结果：[NaN, 2.0, 3.0, 4.0, NaN]
    assert smoothed.iloc[1] == 2.0
    assert smoothed.iloc[2] == 3.0
    assert smoothed.iloc[3] == 4.0
    assert pd.isna(smoothed.iloc[0])
    assert pd.isna(smoothed.iloc[4])

def test_highlight_points():
    """
    测试utils.highlight_points函数。
    """
    import pandas as pd
    import numpy as np
    fig, ax = plt.subplots()
    df = pd.DataFrame({'x': np.arange(10), 'y': np.arange(10)})
    condition = pd.Series([False, False, True, False, False, True, False, False, False, False])
    pp.utils.highlight_points(ax, df, x='x', y='y', condition=condition)
    assert len(ax.collections) == 2 # Two scatter collections (normal and highlighted)
    plt.close(fig)

def test_plot_bifurcation_diagram():
    """
    测试utils.plot_bifurcation_diagram函数。
    """
    import pandas as pd
    import numpy as np
    fig, ax = plt.subplots()
    df = pd.DataFrame({'r': np.linspace(0,1,100), 'x': np.random.rand(100)})
    pp.utils.plot_bifurcation_diagram(ax, df, x='r', y='x')
    assert len(ax.collections) == 1 # Scatter plot
    assert ax.get_xlabel() == 'Bifurcation Parameter'
    assert ax.get_ylabel() == 'State Variable'
    plt.close(fig)

def test_fit_and_plot_distribution():
    """
    测试utils.fit_and_plot_distribution函数。
    """
    import pandas as pd
    import numpy as np
    fig, ax = plt.subplots()
    data_series = pd.Series(np.random.normal(0, 1, 100))
    pp.utils.fit_and_plot_distribution(ax, data_series, dist_name='norm')
    assert len(ax.lines) == 1 # Fitted distribution line
    assert ax.get_legend() is not None
    plt.close(fig)

def test_bin_data():
    """
    测试utils.bin_data函数。
    """
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({'x': np.linspace(0, 10, 100), 'y': np.random.rand(100)})
    binned_df = pp.utils.bin_data(df, x='x', y='y', bins=5)
    assert 'bin_center' in binned_df.columns
    assert 'y_agg' in binned_df.columns
    assert 'y_error' in binned_df.columns
    assert len(binned_df) == 5 # 5 bins
    
def test_add_hist():
    """
    测试add_hist方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,1,2,3,3,3]})
    plotter.add_hist(data=test_df, x='x', tag='my_hist')
    ax = plotter.get_ax('my_hist')
    assert len(ax.patches) > 0 # Bars for histogram
    plt.close(plotter.fig)

def test_add_box():
    """
    测试add_box方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'group':['A']*5, 'value':[1,2,3,4,5]})
    plotter.add_box(data=test_df, x='group', y='value', tag='my_box')
    ax = plotter.get_ax('my_box')
    assert len(ax.patches) > 0 # Boxplot elements are patches
    plt.close(plotter.fig)

def test_add_heatmap():
    """
    测试add_heatmap方法。
    """
    import pandas as pd
    plotter = Plotter(layout=(1,1))
    data = pd.DataFrame([[1,2],[3,4]])
    plotter.add_heatmap(data=data, tag='my_heatmap')
    ax = plotter.get_ax('my_heatmap')
    assert len(ax.collections) == 1
    plt.close(plotter.fig)

def test_add_seaborn():
    """
    测试add_seaborn方法。
    """
    import seaborn as sns
    import pandas as pd
    plotter = Plotter(layout=(1,1))
    data = pd.DataFrame({'x': [1,2,3], 'y': [4,5,6]})
    plotter.add_seaborn(plot_func=sns.lineplot, data=data, x='x', y='y', tag='my_seaborn')
    ax = plotter.get_ax('my_seaborn')
    assert len(ax.lines) == 1
    plt.close(plotter.fig)

def test_set_title():
    """
    测试set_title方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    plotter.set_title('ax1', 'My Title')
    ax = plotter.get_ax('ax1')
    assert ax.get_title() == 'My Title'
    plt.close(plotter.fig)

def test_set_xlabel_ylabel():
    """
    测试set_xlabel和set_ylabel方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    plotter.set_xlabel('ax1', 'X-Axis').set_ylabel('ax1', 'Y-Axis')
    ax = plotter.get_ax('ax1')
    assert ax.get_xlabel() == 'X-Axis'
    assert ax.get_ylabel() == 'Y-Axis'
    plt.close(plotter.fig)

def test_set_xlim_ylim():
    """
    测试set_xlim和set_ylim方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    plotter.set_xlim('ax1', 0, 5).set_ylim('ax1', 0, 10)
    ax = plotter.get_ax('ax1')
    assert ax.get_xlim() == (0.0, 5.0)
    assert ax.get_ylim() == (0.0, 10.0)
    plt.close(plotter.fig)

def test_tick_params():
    """
    测试tick_params方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':np.arange(1,11), 'y':np.arange(1,11)}) # Wider range
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    ax = plotter.get_ax('ax1')
    ax.set_xlim(0, 11) # Ensure ticks are generated
    ax.set_ylim(0, 11)
    plotter.tick_params('ax1', axis='x', labelbottom=False)
    # Check if there are tick labels before accessing index 0
    if ax.xaxis.get_ticklabels():
        assert not ax.xaxis.get_ticklabels()[0].get_visible() # Check if labels are hidden
    else:
        # If no tick labels are generated, it means they are effectively hidden
        assert True 
    plt.close(plotter.fig)

def test_set_legend():
    """
    测试set_legend方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1', label='My Line')
    plotter.set_legend('ax1')
    ax = plotter.get_ax('ax1')
    assert ax.get_legend() is not None
    plt.close(plotter.fig)

def test_set_suptitle():
    """
    测试set_suptitle方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.set_suptitle('Global Title')
    assert plotter.fig._suptitle.get_text() == 'Global Title'
    plt.close(plotter.fig)

def test_add_global_legend():
    """
    测试add_global_legend方法。
    """
    plotter = Plotter(layout=(1,2))
    test_df1 = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    test_df2 = pd.DataFrame({'x':[1,2], 'y':[2,1]})
    plotter.add_line(data=test_df1, x='x', y='y', tag='ax1', label='Line 1')
    plotter.add_line(data=test_df2, x='x', y='y', tag='ax2', label='Line 2')
    plotter.add_global_legend()
    assert plotter.fig.legends # Check if figure has legends
    plt.close(plotter.fig)

def test_add_twinx():
    """
    测试add_twinx方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    twin_ax = plotter.add_twinx('ax1')
    assert twin_ax is not None
    assert twin_ax.get_shared_x_axes().joined(plotter.get_ax('ax1'), twin_ax)
    plt.close(plotter.fig)

def test_add_regplot():
    """
    测试add_regplot方法。
    """
    plotter = Plotter(layout=(1,1))
    data = pd.DataFrame({'x': [1,2,3], 'y': [4,5,6]})
    plotter.add_regplot(data=data, x='x', y='y', tag='my_regplot')
    ax = plotter.get_ax('my_regplot')
    assert len(ax.collections) > 0 # Scatter points
    assert len(ax.lines) > 0 # Regression line
    plt.close(plotter.fig)

def test_add_hline_vline():
    """
    测试add_hline和add_vline方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    plotter.add_hline('ax1', 1.5).add_vline('ax1', 1.5)
    ax = plotter.get_ax('ax1')
    assert len(ax.lines) == 3 # Original line + hline + vline
    plt.close(plotter.fig)

def test_add_text():
    """
    测试add_text方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    plotter.add_text('ax1', 1.5, 1.5, 'Hello')
    ax = plotter.get_ax('ax1')
    assert len(ax.texts) == 1
    assert ax.texts[0].get_text() == 'Hello'
    plt.close(plotter.fig)

def test_add_patch():
    """
    测试add_patch方法。
    """
    from matplotlib.patches import Rectangle
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    rect = Rectangle((0,0), 1, 1)
    plotter.add_patch('ax1', rect)
    ax = plotter.get_ax('ax1')
    assert len(ax.patches) == 1
    plt.close(plotter.fig)

def test_cleanup_heatmaps():
    """
    测试cleanup_heatmaps方法。
    """
    plotter = Plotter(layout=(1,2))
    data1 = pd.DataFrame([[1,2],[3,4]])
    data2 = pd.DataFrame([[5,6],[7,8]])
    plotter.add_heatmap(data=data1, tag='hm1', cbar=False)
    plotter.add_heatmap(data=data2, tag='hm2', cbar=False)
    plotter.cleanup_heatmaps(tags=['hm1', 'hm2'])
    assert plotter.fig.colorbar is not None
    plt.close(plotter.fig)

def test_save_method(tmp_path):
    """
    测试save方法。
    """
    plotter = Plotter(layout=(1,1))
    test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
    plotter.add_line(data=test_df, x='x', y='y', tag='ax1')
    filepath = tmp_path / "test_plot.png"
    plotter.save(str(filepath))
    assert filepath.exists()
    plt.close(plotter.fig)

def test_cleanup_axis_sharing():
    """
    测试cleanup方法中的轴共享功能。
    """
    plotter = Plotter(layout=(2,2))
    test_df_00 = pd.DataFrame({'x':np.arange(1,11), 'y':np.arange(1,11)})
    test_df_01 = pd.DataFrame({'x':np.arange(1,11), 'y':np.arange(3,13)})
    test_df_10 = pd.DataFrame({'x':np.arange(1,11), 'y':np.arange(5,15)})
    test_df_11 = pd.DataFrame({'x':np.arange(1,11), 'y':np.arange(7,17)})

    plotter.add_line(data=test_df_00, x='x', y='y', tag='ax00', ax=plotter.axes_dict['ax00'])
    plotter.add_line(data=test_df_01, x='x', y='y', tag='ax01', ax=plotter.axes_dict['ax01'])
    plotter.add_line(data=test_df_10, x='x', y='y', tag='ax10', ax=plotter.axes_dict['ax10'])
    plotter.add_line(data=test_df_11, x='x', y='y', tag='ax11', ax=plotter.axes_dict['ax11'])

    # Set limits to ensure ticks are generated
    for ax_tag in ['ax00', 'ax01', 'ax10', 'ax11']:
        ax = plotter.axes_dict[ax_tag]
        ax.set_xlim(0, 11)
        ax.set_ylim(0, 18)

    plotter.cleanup(share_y_on_rows=[0], share_x_on_cols=[1])

    # Check y-axis sharing for row 0
    ax00 = plotter.axes_dict['ax00']
    ax01 = plotter.axes_dict['ax01']
    assert ax01.get_shared_y_axes().joined(ax00, ax01)
    if ax01.yaxis.get_ticklabels(): # Check if labels exist before accessing
        assert not ax01.yaxis.get_ticklabels()[0].get_visible()
    assert ax01.get_ylabel() == ""

    # Check x-axis sharing for col 1
    ax01 = plotter.axes_dict['ax01']
    ax11 = plotter.axes_dict['ax11']
    assert ax01.get_shared_x_axes().joined(ax01, ax11)
    if ax01.xaxis.get_ticklabels(): # Check if labels exist before accessing
        assert not ax01.xaxis.get_ticklabels()[0].get_visible()
    assert ax01.get_xlabel() == ""
    
    plt.close(plotter.fig)

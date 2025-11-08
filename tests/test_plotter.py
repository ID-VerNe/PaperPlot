import pytest
import matplotlib.pyplot as plt
from paperplot import Plotter, generate_grid_layout
from paperplot.exceptions import TagNotFoundError, DuplicateTagError, PlottingSpaceError

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
    plotter.add_line(x=[1,2], y=[1,2], tag='line_a', ax=ax_a)
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
    plotter.add_line(x=[1,2,3], y=[4,5,6], tag='my_line')
    ax = plotter.get_ax('my_line')
    assert len(ax.lines) == 1
    plt.close(plotter.fig)

def test_add_bar():
    """
    测试add_bar方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_bar(x=['A','B'], y=[10,20], tag='my_bar')
    ax = plotter.get_ax('my_bar')
    assert len(ax.patches) == 2 # Two bars
    plt.close(plotter.fig)

def test_add_scatter():
    """
    测试add_scatter方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_scatter(x=[1,2,3], y=[4,5,6], tag='my_scatter')
    ax = plotter.get_ax('my_scatter')
    assert len(ax.collections) == 1
    plt.close(plotter.fig)

def test_add_hist():
    """
    测试add_hist方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_hist(x=[1,1,2,3,3,3], tag='my_hist')
    ax = plotter.get_ax('my_hist')
    assert len(ax.patches) > 0 # Bars for histogram
    plt.close(plotter.fig)

def test_add_box():
    """
    测试add_box方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_box(data=[1,2,3,4,5], tag='my_box')
    ax = plotter.get_ax('my_box')
    assert len(ax.artists) > 0 # Boxplot elements
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
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
    plotter.set_title('ax1', 'My Title')
    ax = plotter.get_ax('ax1')
    assert ax.get_title() == 'My Title'
    plt.close(plotter.fig)

def test_set_xlabel_ylabel():
    """
    测试set_xlabel和set_ylabel方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
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
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
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
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
    plotter.tick_params('ax1', axis='x', labelbottom=False)
    ax = plotter.get_ax('ax1')
    assert not ax.xaxis.get_ticklabels()[0].get_visible() # Check if labels are hidden
    plt.close(plotter.fig)

def test_set_legend():
    """
    测试set_legend方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1', label='My Line')
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
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1', label='Line 1')
    plotter.add_line(x=[1,2], y=[2,1], tag='ax2', label='Line 2')
    plotter.add_global_legend()
    assert plotter.fig.legends # Check if figure has legends
    plt.close(plotter.fig)

def test_add_twinx():
    """
    测试add_twinx方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
    twin_ax = plotter.add_twinx('ax1')
    assert twin_ax is not None
    assert twin_ax.get_shared_x_axes().joined(plotter.get_ax('ax1'), twin_ax)
    plt.close(plotter.fig)

def test_add_regplot():
    """
    测试add_regplot方法。
    """
    import pandas as pd
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
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
    plotter.add_hline('ax1', 1.5).add_vline('ax1', 1.5)
    ax = plotter.get_ax('ax1')
    assert len(ax.lines) == 3 # Original line + hline + vline
    plt.close(plotter.fig)

def test_add_text():
    """
    测试add_text方法。
    """
    plotter = Plotter(layout=(1,1))
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
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
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
    rect = Rectangle((0,0), 1, 1)
    plotter.add_patch('ax1', rect)
    ax = plotter.get_ax('ax1')
    assert len(ax.patches) == 1
    plt.close(plotter.fig)

def test_cleanup_heatmaps():
    """
    测试cleanup_heatmaps方法。
    """
    import pandas as pd
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
    plotter.add_line(x=[1,2], y=[1,2], tag='ax1')
    filepath = tmp_path / "test_plot.png"
    plotter.save(str(filepath))
    assert filepath.exists()
    plt.close(plotter.fig)

def test_cleanup_axis_sharing():
    """
    测试cleanup方法中的轴共享功能。
    """
    plotter = Plotter(layout=(2,2))
    plotter.add_line(x=[1,2], y=[1,2], tag='ax00', ax=plotter.axes_dict['ax00'])
    plotter.add_line(x=[1,2], y=[3,4], tag='ax01', ax=plotter.axes_dict['ax01'])
    plotter.add_line(x=[1,2], y=[5,6], tag='ax10', ax=plotter.axes_dict['ax10'])
    plotter.add_line(x=[1,2], y=[7,8], tag='ax11', ax=plotter.axes_dict['ax11'])

    plotter.cleanup(share_y_on_rows=[0], share_x_on_cols=[1])

    # Check y-axis sharing for row 0
    ax00 = plotter.axes_dict['ax00']
    ax01 = plotter.axes_dict['ax01']
    assert ax01.get_shared_y_axes().joined(ax00, ax01)
    assert not ax01.yaxis.get_ticklabels()[0].get_visible()
    assert ax01.get_ylabel() == ""

    # Check x-axis sharing for col 1
    ax01 = plotter.axes_dict['ax01']
    ax11 = plotter.axes_dict['ax11']
    assert ax01.get_shared_x_axes().joined(ax01, ax11)
    assert not ax01.xaxis.get_ticklabels()[0].get_visible()
    assert ax01.get_xlabel() == ""
    
    plt.close(plotter.fig)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from paperplot import Plotter


def test_color_manager_public_apis():
    p = Plotter(layout=(1, 1))
    p.set_palette(['#111111', '#222222']).bind_color({'A': '#ff0000'})
    p.add_line(x=[0, 1], y=[1, 2], label='A')
    p.add_line(x=[0, 1], y=[2, 3], label='B')
    ax = p.get_ax(1)
    colors = [line.get_color() for line in ax.lines]
    assert colors[0] == '#ff0000'
    assert colors[1] in ('#111111', '#222222')
    p.reset_color_cycle()
    plt.close(p.fig)


def test_reference_line_and_interval_shading():
    p = Plotter(layout=(1, 1))
    p.add_line(x=[0, 1, 2], y=[1, 2, 3]).add_reference_line(y='mean', annotate=True).add_interval_shading([0, 1, 2])
    ax = p.get_ax(1)
    assert len(ax.lines) >= 2
    assert len(ax.patches) >= 2
    assert any(t.get_text().startswith('Avg:') for t in ax.texts)
    plt.close(p.fig)


def test_context_managers_on_primary_and_twin():
    df = pd.DataFrame({'x': [0, 1], 'y1': [1, 2], 'y2': [3, 4]})
    p = Plotter(layout=(1, 1))
    p.add_line(data=df, x='x', y='y1', tag='A').add_twinx(tag='A')
    with p.on_twin('A'):
        p.add_line(data=df, x='x', y='y2', label='twin-y2')
    with p.on_primary('A'):
        p.add_line(data=df, x='x', y='y1', label='pri-y1')
    assert len(p.get_ax('A').lines) == 2
    assert len(p.twin_axes['A'].lines) == 1
    plt.close(p.fig)


def test_metadata_axis_dedup_with_alias_tags():
    p = Plotter(layout=(1, 1))
    p.add_line(x=[0, 1], y=[1, 2], tag='A')
    p.add_line(x=[0, 1], y=[2, 3], tag='aliasA', ax=p.get_ax('A'))
    md = p.get_layout_metadata()
    entries = list(md['subplots'].values())
    main_axes = [e for e in entries if 'A' in e.get('tags', []) or 'aliasA' in e.get('tags', [])]
    assert len(main_axes) == 1
    assert set(main_axes[0]['tags']) >= {'A', 'aliasA'}
    plt.close(p.fig)


def test_domain_level_helpers():
    df = pd.DataFrame({
        't': [0, 1, 2],
        'peak1': [2.0, 2.5, 3.0],
        'peak2': [1.0, 1.2, 1.5],
        'base': [1.0, 1.0, 1.0],
    })
    p = Plotter(layout=(1, 3))
    p.add_peak_ratio_kinetics(data=df, x='t', peaks=['peak1', 'peak2'], baseline='base', tag='ax00')
    p.add_ros_timebar(data=df.assign(cat=['a', 'b', 'c']), x='cat', ys=['peak1', 'peak2'], tag='ax01')
    p.add_sers_dualpeak_dualaxis(data=df, x='t', left_peak='peak1', right_peak='peak2', tag='ax02')
    assert len(p.get_ax('ax00').lines) == 2
    assert len(p.get_ax('ax01').patches) == 6
    assert 'ax02' in p.twin_axes
    plt.close(p.fig)

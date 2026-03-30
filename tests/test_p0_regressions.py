import importlib
import logging

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import pytest

import paperplot
from paperplot import Plotter
from paperplot.exceptions import PlottingError


@pytest.mark.parametrize("alias", ["err", "yerr", "y_err", "y_errs"])
def test_grouped_bar_accepts_error_aliases(alias):
    df = pd.DataFrame(
        {
            "cat": ["A", "B", "C"],
            "v1": [1.0, 2.0, 3.0],
            "v2": [1.2, 1.9, 2.7],
        }
    )
    err_map = {"v1": [0.1, 0.1, 0.2], "v2": [0.2, 0.1, 0.1]}

    plotter = Plotter(layout=(1, 1))
    kwargs = {alias: err_map}
    plotter.add_grouped_bar(data=df, x="cat", ys=["v1", "v2"], **kwargs)
    ax = plotter.get_ax(1)

    assert len(ax.patches) == 6
    plt.close(plotter.fig)

@pytest.mark.parametrize("alias", ["err", "yerr", "y_err", "y_errs"])
def test_line_accepts_error_aliases(alias):
    df = pd.DataFrame({"x": [0, 1, 2], "y": [1.0, 1.5, 2.0], "e": [0.1, 0.2, 0.1]})
    plotter = Plotter(layout=(1, 1))
    kwargs = {alias: "e", "capsize": 3}
    plotter.add_line(data=df, x="x", y="y", **kwargs)
    ax = plotter.get_ax(1)
    assert len(ax.lines) >= 1
    plt.close(plotter.fig)


def test_grouped_bar_rejects_mismatched_err_length():
    df = pd.DataFrame({"cat": ["A", "B", "C"], "v1": [1, 2, 3], "v2": [2, 3, 4]})
    bad_err = {"v1": [0.1, 0.1], "v2": [0.2, 0.2, 0.2]}

    plotter = Plotter(layout=(1, 1))
    with pytest.raises(PlottingError):
        plotter.add_grouped_bar(data=df, x="cat", ys=["v1", "v2"], err=bad_err)
    plt.close(plotter.fig)


def test_add_dual_axis_line_merges_legend_and_binds_axis_colors():
    df = pd.DataFrame({"t": [0, 1, 2], "left": [1.0, 1.2, 1.1], "right": [10, 12, 14]})

    plotter = Plotter(layout=(1, 1))
    plotter.add_blank(tag="main").add_dual_axis_line(
        data=df,
        x="t",
        tag="main",
        left={"y": "left", "label": "Left", "color": "#1f77b4"},
        right={"y": "right", "label": "Right", "color": "#d62728"},
        ylabel_left="L",
        ylabel_right="R",
        legend="merged",
        legend_loc="upper left",
    )

    ax = plotter.get_ax("main")
    twin = plotter.twin_axes["main"]
    legend = ax.get_legend()
    labels = [t.get_text() for t in legend.get_texts()]

    assert "Left" in labels and "Right" in labels
    assert ax.yaxis.label.get_color() == "#1f77b4"
    assert twin.yaxis.label.get_color() == "#d62728"
    plt.close(plotter.fig)


def test_add_bar_labels_formatting():
    df = pd.DataFrame({"x": ["A", "B"], "y": [1.234, 2.345]})
    plotter = Plotter(layout=(1, 1))
    plotter.add_bar(data=df, x="x", y="y").add_bar_labels(fmt="{:.2f}")
    ax = plotter.get_ax(1)

    texts = [t.get_text() for t in ax.texts]
    assert "1.23" in texts
    assert "2.35" in texts
    plt.close(plotter.fig)


def test_import_does_not_call_basicConfig(monkeypatch):
    called = {"n": 0}
    original = logging.basicConfig

    def _counting_basic_config(*args, **kwargs):
        called["n"] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(logging, "basicConfig", _counting_basic_config)
    importlib.reload(paperplot)
    assert called["n"] == 0

# paperplot/utils.py

import os
import numpy as np
from scipy import stats
import pandas as pd
from adjustText import adjust_text


def get_style_path(style_name: str) -> str:
    """
    获取预定义样式文件的绝对路径。
    
    Args:
        style_name (str): 样式名称 (例如 'publication').

    Returns:
        str: .mplstyle 文件的路径。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(current_dir, 'styles', f'{style_name}.mplstyle')
    if not os.path.exists(style_path):
        # 如果在当前目录的styles子目录找不到，尝试作为包资源查找
        try:
            import importlib.resources
            with importlib.resources.path('paperplot.styles', f'{style_name}.mplstyle') as path:
                return str(path)
        except (ImportError, FileNotFoundError):
            raise FileNotFoundError(f"Style '{style_name}' not found as a file or package resource.")
    return style_path


def _p_to_stars(p_value: float) -> str:
    """将p值转换为显著性星号。"""
    if p_value > 0.05:
        return 'ns'
    elif p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    return ''

def add_stat_test(ax, data: pd.DataFrame, x: str, y: str, group1: str, group2: str,
                  test: str = 't-test_ind', text_offset: float = 0.1, **kwargs):
    """
    在两组数据之间自动进行统计检验，并在图上标注显著性。

    Args:
        ax (plt.Axes): 要在其上操作的Matplotlib Axes对象。
        data (pd.DataFrame): 包含绘图数据的DataFrame。
        x (str): 分组变量的列名。
        y (str): 数值变量的列名。
        group1 (str): 第一个组的名称。
        group2 (str): 第二个组的名称。
        test (str, optional): 要执行的统计检验。
                              可选值为 't-test_ind' (独立样本t检验) 
                              和 'mannwhitneyu' (Mann-Whitney U检验)。
                              默认为 't-test_ind'。
        text_offset (float, optional): 标注线与数据最高点之间的垂直距离比例。默认为 0.1。
        **kwargs: 传递给 `ax.plot` 和 `ax.text` 的额外参数。
    """
    # 1. 数据筛选
    data1 = data[data[x] == group1][y]
    data2 = data[data[x] == group2][y]

    # 2. 统计检验
    if test == 't-test_ind':
        stat, p_value = stats.ttest_ind(data1, data2, equal_var=False) # Welch's t-test
    elif test == 'mannwhitneyu':
        stat, p_value = stats.mannwhitneyu(data1, data2)
    else:
        raise ValueError(f"Unknown test: {test}. Available tests are 't-test_ind' and 'mannwhitneyu'.")

    # 3. 转换为星号
    p_text = _p_to_stars(p_value)
    if not p_text:
        return # 如果没有显著性，则不绘制

    # 4. 计算标注位置
    # 找到分组在x轴上的数值位置
    xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
    try:
        x1_pos = xtick_labels.index(group1)
        x2_pos = xtick_labels.index(group2)
    except ValueError:
        raise ValueError(f"Groups '{group1}' or '{group2}' not found in x-axis tick labels: {xtick_labels}")

    y_max = max(data1.max(), data2.max())
    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    bar_y = y_max + y_range * text_offset
    text_y = bar_y + y_range * 0.02

    # 5. 绘制标注
    line_kwargs = {'color': 'black', 'lw': 1.5}
    line_kwargs.update(kwargs)
    ax.plot([x1_pos, x1_pos, x2_pos, x2_pos], [bar_y, text_y, text_y, bar_y], **line_kwargs)
    
    text_kwargs = {'ha': 'center', 'va': 'bottom', 'color': 'black'}
    text_kwargs.update(kwargs)
    ax.text((x1_pos + x2_pos) * 0.5, text_y, p_text, **text_kwargs)


def plot_learning_curve(ax, train_sizes, train_scores, test_scores, **kwargs):
    """
    可视化模型的学习曲线，帮助判断模型是过拟合还是欠拟合。

    Args:
        ax (plt.Axes): 要在其上操作的Matplotlib Axes对象。
        train_sizes (array-like): 训练样本数量的数组。
        train_scores (array-like): 训练得分矩阵，维度为 (n_ticks, n_folds)。
        test_scores (array-like): 交叉验证得分矩阵，维度为 (n_ticks, n_folds)。
        **kwargs: 其他传递给 `ax.plot` 和 `ax.fill_between` 的关键字参数。
    """
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    ax.grid(True)

    # 绘制训练得分曲线和标准差区域
    ax.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color=kwargs.get('color', 'r'))
    ax.plot(train_sizes, train_scores_mean, 'o-', color=kwargs.get('color', 'r'),
             label="Training score")

    # 绘制交叉验证得分曲线和标准差区域
    ax.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1,
                     color=kwargs.get('color', 'g'))
    ax.plot(train_sizes, test_scores_mean, 'o-', color=kwargs.get('color', 'g'),
             label="Cross-validation score")

    ax.set_title(kwargs.get('title', 'Learning Curve'))
    ax.set_xlabel(kwargs.get('xlabel', "Training examples"))
    ax.set_ylabel(kwargs.get('ylabel', "Score"))
    ax.legend(loc="best")


def parse_mosaic_layout(layout: list[list[str]]) -> tuple[dict, tuple[int, int]]:
    """
    解析马赛克布局定义，返回每个命名区域的跨度信息和总网格尺寸。

    Args:
        layout (list[list[str]]): 用户定义的马赛克布局。

    Returns:
        tuple[dict, tuple[int, int]]:
            - 一个字典，键是唯一的子图名称，值是包含其起始位置和跨度的字典。
            - 一个元组，包含总行数和总列数。
    
    Raises:
        ValueError: 如果布局中的某个区域不是矩形。
    """
    if not layout or not isinstance(layout, list) or not isinstance(layout[0], list):
        raise ValueError("Layout must be a list of lists.")

    n_rows = len(layout)
    n_cols = len(layout[0])

    parsed = {}
    visited = set()

    for r in range(n_rows):
        for c in range(n_cols):
            if (r, c) in visited:
                continue

            name = layout[r][c]
            visited.add((r, c))

            if name == '.':
                continue

            # 找到 col_span
            col_span = 1
            while c + col_span < n_cols and layout[r][c + col_span] == name and (r, c + col_span) not in visited:
                col_span += 1

            # 找到 row_span
            row_span = 1
            is_rect = True
            while r + row_span < n_rows:
                row_is_solid = all(c + i < n_cols and layout[r + row_span][c + i] == name for i in range(col_span))
                if not row_is_solid:
                    break
                row_span += 1

            # 验证区域是否为矩形，并标记为已访问
            for i in range(r, r + row_span):
                for j in range(c, c + col_span):
                    if i >= n_rows or j >= n_cols or layout[i][j] != name or (i, j) in visited and (i, j) != (r, c):
                        raise ValueError(f"Layout area '{name}' is not rectangular or is overlapping.")
                    visited.add((i, j))

            parsed[name] = {'row_start': r, 'col_start': c, 'row_span': row_span, 'col_span': col_span}

    return parsed, (n_rows, n_cols)


def highlight_peaks(ax, x: pd.Series, y: pd.Series, peaks_x: list, 
                    label_peaks: bool = True, 
                    prefer_direction: str = 'up',
                    use_bbox: bool = True,
                    label_positions: dict = None,
                    **kwargs):
    """
    在一条已绘制的光谱上，自动高亮并（可选地）标注出特征峰的位置。
    使用 adjustText 库来避免标签重叠，并提供更灵活的放置选项。

    Args:
        ax (plt.Axes): 要在其上操作的Matplotlib Axes对象。
        x (pd.Series): 包含X轴数据的Series。
        y (pd.Series): 包含Y轴数据的Series。
        peaks_x (list): 一个包含特征峰X轴位置的列表。
        label_peaks (bool, optional): 如果为True，则在峰顶附近标注X轴值。默认为True。
        prefer_direction (str, optional): 自动布局时文本的初始放置方向, 'up' 或 'down'。默认为 'up'。
        use_bbox (bool, optional): 如果为True，为文本添加一个半透明的背景框。默认为True。
        label_positions (dict, optional): 一个字典，用于手动指定标签位置。
                                          键是峰值的X坐标，值是(x, y)元组。
                                          未在此字典中指定的峰将自动放置。
        **kwargs: 其他传递给 `ax.axvline` 和 `ax.text` 的关键字参数。
    """
    import numpy as np
    # 分离 axvline 和 text 的参数
    text_kwargs = kwargs.copy()
    vline_kwargs = {
        'color': text_kwargs.pop('color', 'gray'),
        'linestyle': text_kwargs.pop('linestyle', '--')
    }
    
    if use_bbox:
        text_kwargs.setdefault('bbox', dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))

    auto_texts = []
    for peak in peaks_x:
        idx = np.abs(x - peak).argmin()
        peak_x_val = x.iloc[idx]
        peak_y_val = y.iloc[idx]
        
        ax.axvline(x=peak_x_val, **vline_kwargs)
        
        if label_peaks:
            label_text = f'{peak_x_val:.0f}'
            # 检查是否有手动指定的位置
            if label_positions and peak in label_positions:
                pos = label_positions[peak]
                ax.text(pos[0], pos[1], label_text, **text_kwargs)
            else:
                # 自动布局逻辑
                y_offset = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.05
                initial_y = peak_y_val + y_offset if prefer_direction == 'up' else peak_y_val - y_offset
                auto_texts.append(ax.text(peak_x_val, initial_y, label_text, **text_kwargs))
            
    if auto_texts:
        adjust_text(auto_texts, ax=ax, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))


def add_event_markers(ax, event_dates: list, labels: list = None, 
                      use_bbox: bool = True, 
                      label_positions: dict = None,
                      **kwargs):
    """
    在时间序列图上标记重要的垂直事件。
    使用 adjustText 库来避免标签重叠。

    Args:
        ax (plt.Axes): 要在其上操作的Matplotlib Axes对象。
        event_dates (list): 包含事件X轴位置的列表。
        labels (list, optional): 与每个事件对应的标签列表。如果提供，将在事件线上方显示。
        use_bbox (bool, optional): 如果为True，为文本添加一个半透明的背景框。默认为True。
        label_positions (dict, optional): 一个字典，用于手动指定标签位置。
                                          键是事件的X坐标，值是(x, y)元组。
                                          未在此字典中指定的事件将自动放置。
        **kwargs: 其他传递给 `ax.axvline` 和 `ax.text` 的关键字参数。
    """
    vline_kwargs = kwargs.copy()
    vline_kwargs.setdefault('color', 'red')
    vline_kwargs.setdefault('linestyle', '-.')
    
    text_kwargs = kwargs.copy()
    if use_bbox:
        text_kwargs.setdefault('bbox', dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))

    auto_texts = []
    # 首先绘制所有线条
    for event_date in event_dates:
        ax.axvline(x=event_date, **vline_kwargs)
    
    # 然后准备文本
    if labels:
        for i, event_date in enumerate(event_dates):
            if i < len(labels):
                label_text = labels[i]
                # 检查是否有手动指定的位置
                if label_positions and event_date in label_positions:
                    pos = label_positions[event_date]
                    ax.text(pos[0], pos[1], label_text, **text_kwargs)
                else:
                    # 自动布局逻辑
                    y_pos = ax.get_ylim()[1] * 0.95 # 初始放置在顶部
                    auto_texts.append(ax.text(event_date, y_pos, label_text, **text_kwargs))
    
    if auto_texts:
        adjust_text(auto_texts, ax=ax, arrowprops=dict(arrowstyle='->', color='red'))


def moving_average(data_series: pd.Series, window_size: int) -> pd.Series:
    """
    计算数据序列的移动平均值。

    Args:
        data_series (pd.Series): 输入的数据序列。
        window_size (int): 移动平均的窗口大小。

    Returns:
        pd.Series: 平滑后的数据序列。
    """
    return data_series.rolling(window=window_size, center=True).mean()


def highlight_points(ax, data: pd.DataFrame, x: str, y: str, condition: pd.Series, **kwargs):
    """
    在散点图上根据条件突出显示特定的数据点。

    Args:
        ax (plt.Axes): 要在其上操作的Matplotlib Axes对象。
        data (pd.DataFrame): 包含绘图数据的DataFrame。
        x (str): X轴数据的列名。
        y (str): Y轴数据的列名。
        condition (pd.Series): 一个布尔值的Series，与data的行数相同。
                               为True的数据点将被高亮。
        **kwargs: 传递给 `ax.scatter` 的关键字参数。
                  可以为高亮和非高亮状态分别设置参数，
                  例如 `s_highlight=50`, `c_highlight='red'`, `s_normal=10`。
    """
    normal_kwargs = {
        's': kwargs.pop('s_normal', 20),
        'c': kwargs.pop('c_normal', 'gray'),
        'alpha': kwargs.pop('alpha_normal', 0.5),
        'label': kwargs.pop('label_normal', 'Other points')
    }
    highlight_kwargs = {
        's': kwargs.pop('s_highlight', 60),
        'c': kwargs.pop('c_highlight', 'red'),
        'alpha': kwargs.pop('alpha_highlight', 1.0),
        'label': kwargs.pop('label_highlight', 'Highlighted')
    }
    # 将剩余的kwargs应用到两个字典中
    normal_kwargs.update(kwargs)
    highlight_kwargs.update(kwargs)

    ax.scatter(data.loc[~condition, x], data.loc[~condition, y], **normal_kwargs)
    ax.scatter(data.loc[condition, x], data.loc[condition, y], **highlight_kwargs)


def plot_bifurcation_diagram(ax, data: pd.DataFrame, x: str, y: str, **kwargs):
    """
    绘制电力系统稳定性分析中的分岔图。

    这本质上是一个为展示大量数据点密度而优化的散点图。

    Args:
        ax (plt.Axes): 要在其上操作的Matplotlib Axes对象。
        data (pd.DataFrame): 包含绘图数据的DataFrame。
        x (str): X轴数据的列名（通常是分岔参数）。
        y (str): Y轴数据的列名（通常是系统状态变量）。
        **kwargs: 其他传递给 `ax.scatter` 的关键字参数。
    """
    # 为分岔图设置优化的默认参数
    scatter_kwargs = {
        's': 0.5,
        'alpha': 0.1,
        'marker': '.',
        'rasterized': True, # 对大量点的图进行栅格化，减小文件大小
        'color': 'black'
    }
    scatter_kwargs.update(kwargs)
    
    ax.scatter(data[x], data[y], **scatter_kwargs)
    ax.set_xlabel(kwargs.get('xlabel', 'Bifurcation Parameter'))
    ax.set_ylabel(kwargs.get('ylabel', 'State Variable'))
    ax.set_title(kwargs.get('title', 'Bifurcation Diagram'))



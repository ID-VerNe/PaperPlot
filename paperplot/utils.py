# paperplot/utils.py
import os
import glob
from typing import Optional, Union, List, Dict, Tuple
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler


def get_style_path(style_name: str) -> str:
    """获取预定义样式文件的绝对路径。

    首先在 `paperplot/styles` 目录中查找样式文件，如果找不到，
    则尝试作为包资源进行回退查找。

    Args:
        style_name (str): 样式名称 (例如 'publication')，不带扩展名。

    Returns:
        str: 找到的 `.mplstyle` 文件的绝对路径。

    Raises:
        FileNotFoundError: 如果在任何位置都找不到指定的样式文件。
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


def list_available_styles() -> List[str]:
    """列出 paperplot/styles 目录下所有可用的样式名称。

    Returns:
        List[str]: 样式名称列表 (不包含 .mplstyle 扩展名)。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    styles_dir = os.path.join(current_dir, 'styles')

    styles = []
    # 使用 glob 查找所有 .mplstyle 文件
    # 注意：这里使用 os.path.join 来构建路径，确保跨平台兼容性
    for style_file in glob.glob(os.path.join(styles_dir, '*.mplstyle')):
        # 获取文件名，并移除 .mplstyle 扩展名
        style_name = os.path.basename(style_file).replace('.mplstyle', '')
        styles.append(style_name)

    return styles


def parse_mosaic_layout(layout: List[List[str]]) -> Tuple[Dict, Tuple[int, int]]:
    """解析ASCII艺术风格的马赛克布局定义。

    该函数接收一个由字符串组成的列表的列表，并将其转换为一个结构化的
    字典，其中包含每个命名区域的位置和尺寸信息，以及整个网格的尺寸。

    例如:
        [['A', 'A', 'B'],
         ['C', 'C', 'B']]
    将被解析以确定'A', 'B', 'C'各自占据的单元格。

    Args:
        layout (List[List[str]]): 用户定义的马赛克布局，
            其中每个字符串是子图的名称，'.'表示空白区域。

    Returns:
        Tuple[Dict, Tuple[int, int]]:
            - 一个字典，键是唯一的子图名称，值是包含其起始行/列和
              行/列跨度的字典。
            - 一个元组，包含布局的总行数和总列数。

    Raises:
        ValueError: 如果布局为空、格式不正确，或者某个区域不是矩形。
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


def moving_average(data_series: pd.Series, window_size: int) -> pd.Series:
    """计算数据序列的移动平均值。

    Args:
        data_series (pd.Series): 输入的数据序列。
        window_size (int): 移动平均的窗口大小。

    Returns:
        pd.Series: 平滑后的数据序列。
    """
    return data_series.rolling(window=window_size, center=True).mean()


def _data_to_dataframe(data: Optional[pd.DataFrame] = None, **kwargs) -> pd.DataFrame:
    """[私有] 将多种数据输入格式统一转换为Pandas DataFrame。

    此函数处理两种输入情况：
    1. 如果提供了 `data` 参数且其为 DataFrame，则直接返回该 DataFrame。
    2. 如果 `data` 为 None，则将 `kwargs` 中的键值对转换为 DataFrame。

    注意：如果同时提供了 `data` DataFrame 和 `kwargs`，`kwargs` 将被忽略。

    Args:
        data (Optional[pd.DataFrame]): 如果传入的是一个DataFrame，则直接返回它。
        **kwargs: 数据列的键值对，例如 `x=[1, 2, 3], y=[4, 5, 6]`。
                  所有列的长度必须一致。

    Returns:
        pd.DataFrame: 根据输入数据创建的DataFrame。

    Raises:
        TypeError: 如果 `data` 参数不是 `pd.DataFrame` 也不是 `None`。
        ValueError: 如果 `data` 为 `None` 且没有提供 `kwargs`，或者
                    `kwargs` 中的数据列长度不一致。
    """
    if data is not None:
        if isinstance(data, pd.DataFrame):
            return data
        else:
            raise TypeError(f"The 'data' argument must be a pandas DataFrame, but got {type(data)}.")

    if not kwargs:
        raise ValueError(
            "If 'data' is not provided, you must supply data as keyword arguments (e.g., x=[...], y=[...]).")

    # 检查所有输入数据的长度是否一致
    lengths = {key: len(value) for key, value in kwargs.items() if hasattr(value, '__len__')}
    if len(set(lengths.values())) > 1:
        raise ValueError(f"All data columns must have the same length. Found lengths: {lengths}")

    return pd.DataFrame(kwargs)

# --- 在文件末尾添加以下新类 ---

class ColorManager:
    """
    一个用于在多个子图中维护系列颜色一致性的管理器。

    这个类会自动从 Matplotlib 的当前样式配置中加载颜色循环。
    当第一次请求一个系列名称的颜色时，它会从循环中分配一个
    新颜色并缓存起来。后续对同一系列名称的请求将返回缓存的颜色。
    """
    def __init__(self):
        """初始化颜色管理器。"""
        self._color_map: Dict[str, str] = {}
        try:
            # 1. 尝试从 Matplotlib 的当前配置中加载默认的颜色循环
            default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
            self._color_cycler = cycler(color=default_colors)
        except (KeyError, IndexError):
            # 2. 如果加载失败（例如样式文件没有定义颜色），则使用一个健壮的备用颜色列表
            self._color_cycler = cycler(color=[
                '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
                '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', 
                '#bcbd22', '#17becf'
            ])
        
        # 3. 创建一个可迭代对象，用于按顺序提供颜色
        self._cycler_iterator = iter(self._color_cycler)

    def get_color(self, series_name: str) -> str:
        """
        获取指定系列的颜色。

        如果该系列已有预设颜色，则返回该颜色。
        否则，从颜色循环中分配一个新颜色，并为该系列注册它。

        Args:
            series_name (str): 系列的名称 (通常是图例标签)。

        Returns:
            str: 代表颜色的十六进制字符串或名称。
        """
        # 1. 检查缓存中是否已有该系列的颜色
        if series_name in self._color_map:
            return self._color_map[series_name]
        
        # 2. 如果是新系列，从颜色循环器中动态分配一个新颜色
        try:
            new_color = next(self._cycler_iterator)['color']
        except StopIteration:
            # 3. 如果颜色循环用尽，重置迭代器并再次获取，实现“循环”
            self._cycler_iterator = iter(self._color_cycler)
            new_color = next(self._cycler_iterator)['color']
        
        # 4. 缓存新分配的颜色，供将来使用
        self._color_map[series_name] = new_color
        return new_color

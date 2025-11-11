# paperplot/utils.py

import os
import glob
from typing import Optional, Union, List
import pandas as pd


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


def list_available_styles() -> List[str]:
    """
    列出 paperplot/styles 目录下所有可用的样式名称。

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

def _data_to_dataframe(data: Optional[pd.DataFrame] = None, **kwargs: dict) -> pd.DataFrame:
    """
    将各种输入格式统一转换为Pandas DataFrame。

    Args:
        data (Optional[pd.DataFrame]): 如果是DataFrame，直接返回。
        **kwargs: 键值对，其中键是列名，值是类似列表的数据 (list, np.array, pd.Series)。
                  例如 x=[1, 2, 3], y=[4, 5, 6]。

    Returns:
        pd.DataFrame: 转换后的DataFrame。
    
    Raises:
        ValueError: 如果`data`不是DataFrame且没有提供其他数据，或者提供的列长度不一致。
    """
    if data is not None:
        if isinstance(data, pd.DataFrame):
            return data
        else:
            raise TypeError(f"The 'data' argument must be a pandas DataFrame, but got {type(data)}.")

    if not kwargs:
        raise ValueError("If 'data' is not provided, you must supply data as keyword arguments (e.g., x=[...], y=[...]).")

    # 检查所有输入数据的长度是否一致
    lengths = {key: len(value) for key, value in kwargs.items() if hasattr(value, '__len__')}
    if len(set(lengths.values())) > 1:
        raise ValueError(f"All data columns must have the same length. Found lengths: {lengths}")

    return pd.DataFrame(kwargs)

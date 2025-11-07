# paperplot/__init__.py

from .core import Plotter
from .exceptions import PaperPlotError, TagNotFoundError, DuplicateTagError, PlottingSpaceError

def generate_grid_layout(rows: int, cols: int) -> list[list[str]]:
    """
    为Plotter的马赛克布局生成一个简单的网格定义。

    Args:
        rows (int): 网格的行数。
        cols (int): 网格的列数。

    Returns:
        list[list[str]]: 一个可以传递给Plotter的二维列表布局。
    """
    return [[f'({r},{c})' for c in range(cols)] for r in range(rows)]


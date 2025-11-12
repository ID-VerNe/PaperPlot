# paperplot/__init__.py
import logging
import sys
from typing import List

# Configure logging for the package
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

from .core import Plotter
from .exceptions import PaperPlotError, TagNotFoundError, DuplicateTagError, PlottingSpaceError
from . import utils

def generate_grid_layout(rows: int, cols: int) -> List[List[str]]:
    """为Plotter的马赛克布局生成一个简单的网格定义。

    此函数创建一个标准的 `rows` x `cols` 网格布局，其中每个单元格
    都有一个唯一的名称，格式为 `'(r,c)'`。

    Args:
        rows (int): 网格的行数。
        cols (int): 网格的列数。

    Returns:
        List[List[str]]: 一个可以传递给 `Plotter` 构造函数的二维列表布局。
    """
    return [[f'({r},{c})' for c in range(cols)] for r in range(rows)]
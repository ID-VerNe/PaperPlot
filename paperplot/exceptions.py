# paperplot/exceptions.py

from typing import List, Union, Optional

class PaperPlotError(Exception):
    """PaperPlot 库的基础异常类。"""
    pass

class TagNotFoundError(PaperPlotError):
    """当在绘图仪实例中找不到指定的子图标签（tag）时引发。"""
    def __init__(self, tag: Union[str, int], available_tags: List[Union[str, int]]):
        message = (
            f"Tag '{tag}' not found. \n"
            f"Error Cause: You tried to modify a plot using a tag that does not exist. \n"
            f"How to fix: Please use one of the available tags: {available_tags}"
        )
        super().__init__(message)

class DuplicateTagError(PaperPlotError):
    """当尝试分配一个已经被使用的子图标签（tag）时引发。"""
    def __init__(self, tag: Union[str, int], message: Optional[str] = None):
        if message is None:
            message = (
                f"Tag '{tag}' is already in use. \n"
                f"Error Cause: You tried to assign a tag to a new plot, but that tag is already associated with another plot. \n"
                f"How to fix: Tags must be unique. Please choose a different tag."
            )
        super().__init__(message)

class PlottingSpaceError(PaperPlotError):
    """当没有可用的子图空间来创建新图时引发。"""
    def __init__(self, max_plots: int):
        message = (
            f"Cannot add more plots. All {max_plots} subplots are occupied. \n"
            f"Error Cause: You tried to add a new plot, but the grid you initialized is full. \n"
            f"How to fix: Increase the 'rows' or 'cols' when creating the Plotter object layout."
        )
        super().__init__(message)


class PlottingError(PaperPlotError):
    """表示在绘图操作期间发生的一般性错误。"""
    def __init__(self, message: str):
        super().__init__(message)
# paperplot/exceptions.py

from typing import Optional

class PaperPlotError(Exception):
    """PaperPlot 库的基础异常。"""
    pass

class TagNotFoundError(PaperPlotError):
    """当指定的 tag 未找到时抛出。"""
    def __init__(self, tag, available_tags):
        message = (
            f"Tag '{tag}' not found. \n"
            f"Error Cause: You tried to modify a plot using a tag that does not exist. \n"
            f"How to fix: Please use one of the available tags: {available_tags}"
        )
        super().__init__(message)

class DuplicateTagError(PaperPlotError):
    """当尝试使用一个已经存在的 tag 或子图位置已被占用时抛出。"""
    def __init__(self, tag, message: Optional[str] = None):
        if message is None:
            message = (
                f"Tag '{tag}' is already in use. \n"
                f"Error Cause: You tried to assign a tag to a new plot, but that tag is already associated with another plot. \n"
                f"How to fix: Tags must be unique. Please choose a different tag."
            )
        super().__init__(message)

class PlottingSpaceError(PaperPlotError):
    """当没有更多可用子图空间时抛出。"""
    def __init__(self, max_plots):
        message = (
            f"Cannot add more plots. All {max_plots} subplots are occupied. \n"
            f"Error Cause: You tried to add a new plot, but the grid you initialized is full. \n"
            f"How to fix: Increase the 'rows' or 'cols' when creating the Plotter object layout."
        )
        super().__init__(message)


class PlottingError(PaperPlotError):
    """当发生绘图错误时抛出。"""
    def __init__(self, message):
        super().__init__(message)

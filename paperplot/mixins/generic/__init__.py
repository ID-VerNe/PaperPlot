from .basic import BasicPlotsMixin
from .advanced import AdvancedPlotsMixin
from .circular import CircularPlotsMixin
from .wrappers import WrapperPlotsMixin
from .image import ImagePlotsMixin

class GenericPlotsMixin(BasicPlotsMixin, AdvancedPlotsMixin, CircularPlotsMixin, 
                        WrapperPlotsMixin, ImagePlotsMixin):
    """包含通用绘图方法的 Mixin 类。 这些方法是常见图表类型（如线图、散点图、柱状图等）的直接封装。"""
    pass

from typing import Optional
import matplotlib.pyplot as plt
from .labeling import LabelingMixin
from .styling import StylingMixin
from .legend import LegendMixin
from .figure_annotation import FigureAnnotationMixin
from .twin_axes import TwinAxesMixin
from .plot_annotation import PlotAnnotationMixin

from .layout import LayoutMixin

class ModifiersMixin(LabelingMixin, StylingMixin, LegendMixin, 
                     FigureAnnotationMixin, TwinAxesMixin, PlotAnnotationMixin, LayoutMixin):
    """包含所有修饰和注释方法的 Mixin 类。"""
    
    def save(self, filename: str, **kwargs):
        """
        保存图形到文件。
        
        在保存之前，会执行所有延迟的绘制操作（如 `_draw_on_save_queue` 中的函数）。
        这些操作通常依赖于最终的布局和渲染状态（例如 `get_window_extent`）。
        
        Args:
            filename (str): 保存的文件名。
            **kwargs: 传递给 `plt.savefig` 的其他参数。
        """
        # 1. 强制一次绘制，以确保所有对象都有了位置信息 (bbox)
        #    这对于依赖 get_window_extent 的操作（如 fig_add_line, fig_add_box 等）是必须的
        self.fig.canvas.draw()
        
        # 2. 执行所有延迟的绘制操作
        #    这些操作通常是在 add_xxx 方法中定义的，但需要等到 save 时才能准确执行
        while self._draw_on_save_queue:
            item = self._draw_on_save_queue.pop(0)
            if isinstance(item, dict) and 'func' in item:
                func = item['func']
                call_kwargs = item.get('kwargs', {})
                func(**call_kwargs)
            elif callable(item):
                item()
            
        # 3. 再次绘制（如果延迟操作改变了布局，可能需要）
        #    通常 savefig 会自动再次 draw，但为了保险起见，或者如果后续有依赖
        # self.fig.canvas.draw() 

        # 4. 保存文件
        defaults = {'dpi': 300, 'bbox_inches': 'tight'}
        defaults.update(kwargs)
        self.fig.savefig(filename, **defaults)
        
        # 5. 清理/关闭图形，释放内存 (可选，取决于使用习惯，这里为了安全起见不自动关闭，除非用户显式要求)
        # plt.close(self.fig) 
        # 修改：为了防止测试中出现 "NameError: name 'plt' is not defined"，确保 plt 已导入。
        # 另外，通常 save 不应该副作用关闭 figure，除非是脚本模式。
        # 这里我们保持 plt.close(self.fig) 被注释掉，或者如果原逻辑需要关闭，则取消注释。
        # 原代码中有 plt.close(self.fig)，我们保留它但确保 plt 可用。
        plt.close(self.fig)

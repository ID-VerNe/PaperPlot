from typing import Optional
import matplotlib.pyplot as plt

class LayoutMixin:
    """提供手动控制图形布局（边距和间距）的功能。"""

    def set_padding(self, left: Optional[float] = None, bottom: Optional[float] = None, 
                    right: Optional[float] = None, top: Optional[float] = None) -> 'Plotter':
        """手动设置图形的边距（padding）。

        注意：调用此方法会自动禁用 `constrained_layout` 或 `tight_layout`，
        因为手动边距设置与自动布局引擎冲突。

        Args:
            left (float, optional): 左边距 (0-1)。
            bottom (float, optional): 下边距 (0-1)。
            right (float, optional): 右边距 (0-1)。
            top (float, optional): 上边距 (0-1)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 禁用自动布局引擎以允许手动调整
        if self.fig.get_layout_engine() is not None:
            self.fig.set_layout_engine(None)
        
        # 构建参数字典，过滤掉 None 值
        params = {}
        if left is not None: params['left'] = left
        if bottom is not None: params['bottom'] = bottom
        if right is not None: params['right'] = right
        if top is not None: params['top'] = top
        
        if params:
            self.fig.subplots_adjust(**params)
            
        return self

    def set_spacing(self, wspace: Optional[float] = None, hspace: Optional[float] = None) -> 'Plotter':
        """手动设置子图之间的间距。

        注意：调用此方法会自动禁用 `constrained_layout` 或 `tight_layout`，
        因为手动间距设置与自动布局引擎冲突。

        Args:
            wspace (float, optional): 子图之间的水平间距（以子图宽度的分数表示）。
            hspace (float, optional): 子图之间的垂直间距（以子图高度的分数表示）。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 禁用自动布局引擎以允许手动调整
        if self.fig.get_layout_engine() is not None:
            self.fig.set_layout_engine(None)

        params = {}
        if wspace is not None: params['wspace'] = wspace
        if hspace is not None: params['hspace'] = hspace
        
        if params:
            self.fig.subplots_adjust(**params)
            
        return self

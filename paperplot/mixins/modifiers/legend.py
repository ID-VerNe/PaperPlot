from typing import Optional, Union, Dict
import matplotlib.pyplot as plt

class LegendMixin:
    def set_legend(self, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """
        为子图添加图例。
        
        自动处理双轴 (Twin Axis) 的情况，将两个轴的图例合并显示。
        """
        ax = self._get_active_ax(tag)
        
        # 检查是否存在 twin axis
        # 我们需要反向查找：这个 ax 是否是某个 primary ax 的 twin?
        # 或者这个 ax 是否有对应的 twin?
        
        # Case 1: ax 是 primary，检查是否有 twin
        # 我们需要知道当前的 tag
        # 这是一个反向查找 tag 的过程，比较低效，但为了 API 方便
        current_tag = None
        for t, a in self.tag_to_ax.items():
            if a is ax:
                current_tag = t
                break
        
        lines = []
        labels = []
        
        # 收集 Primary Axis 的 handles/labels
        h1, l1 = ax.get_legend_handles_labels()
        lines.extend(h1)
        labels.extend(l1)
        
        # Case 1: ax 是 Primary，检查是否有 Twin
        if current_tag in self.twin_axes:
            twin_ax = self.twin_axes[current_tag]
            h2, l2 = twin_ax.get_legend_handles_labels()
            lines.extend(h2)
            labels.extend(l2)
            
        # Case 2: ax 是 Twin (这种情况比较少见，通常用户会对 Primary 调 legend)
        # 如果用户直接对 twin ax 调 set_legend，我们只显示 twin 的，或者尝试找 primary?
        # 暂时只显示自己的，除非用户明确合并。
        # 为了简单，我们假设用户总是对 Primary Tag 调用 set_legend
        
        if lines:
            ax.legend(lines, labels, **kwargs)
        else:
            # 如果没有 handles，可能是用户想强制显示空的或者自定义的
            ax.legend(**kwargs)
            
        return self

    def add_global_legend(self, loc: str = 'lower center', bbox_to_anchor: tuple = (0.5, 0.0), 
                          ncol: int = 3, **kwargs) -> 'Plotter':
        """
        添加一个全局图例 (Figure-level legend)。
        
        收集所有子图的图例句柄，去重后显示在 Figure 上。
        """
        lines = []
        labels = []
        seen_labels = set()
        
        for ax in self.axes:
            h, l = ax.get_legend_handles_labels()
            for handle, label in zip(h, l):
                if label not in seen_labels and not label.startswith('_'):
                    lines.append(handle)
                    labels.append(label)
                    seen_labels.add(label)
                    
        # 也要检查 twin axes
        for ax in self.twin_axes.values():
            h, l = ax.get_legend_handles_labels()
            for handle, label in zip(h, l):
                if label not in seen_labels and not label.startswith('_'):
                    lines.append(handle)
                    labels.append(label)
                    seen_labels.add(label)
        
        if lines:
            self.fig.legend(lines, labels, loc=loc, bbox_to_anchor=bbox_to_anchor, ncol=ncol, **kwargs)
            
        return self

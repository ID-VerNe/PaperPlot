from typing import Optional, Union
import matplotlib.pyplot as plt
from matplotlib import cycler

class TwinAxesMixin:
    def add_twinx(self, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """为指定或当前活动的子图创建一个共享X轴但拥有独立Y轴的“双Y轴”图， 并切换Plotter的活动目标到新创建的孪生轴，以支持链式调用。

        Args:
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            **kwargs: 传递给 `ax.twinx` 的其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Warning:
            调用此方法后，Plotter会进入“孪生轴模式”。所有后续的绘图和修饰
            命令都将作用于新创建的孪生轴。若要返回操作主轴或切换到其他
            子图，必须显式调用 :meth:`target_primary` 方法。
        """
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("Cannot create twin axis: No active plot found.")
            
        if active_tag in self.twin_axes:
            raise ValueError(f"Tag '{active_tag}' already has a twin axis. Cannot create another one.")

        # 始终获取主轴，避免在孪生轴上创建孪生轴的错误
        ax1 = self._get_ax_by_tag(active_tag)
        ax2 = ax1.twinx(**kwargs)

        # --- 同步颜色循环 ---
        try:
            # 1. 从 rcParams 获取完整的颜色列表
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

            # 2. 估算主轴已使用的颜色数量 (这是一个常用且有效的启发式方法)
            num_colors_used = len(ax1.lines)

            # 3. 计算偏移量，使用模运算确保正确循环
            offset = num_colors_used % len(colors)

            # 4. 创建一个新的、偏移后的颜色列表
            shifted_colors = colors[offset:] + colors[:offset]

            # 5. 为孪生轴设置新的颜色循环
            ax2.set_prop_cycle(cycler(color=shifted_colors))

        except (KeyError, IndexError):
            # 如果样式文件中没有定义颜色循环，则不执行任何操作，保持默认行为
            pass
        # --- 颜色同步逻辑结束 ---
        
        # 存储孪生轴并切换上下文
        self.twin_axes[active_tag] = ax2
        self.active_target = 'twin'
        
        return self

    def add_polar_twin(self, tag: Optional[Union[str, int]] = None, frameon: bool = False) -> 'Plotter':
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("Cannot create polar twin axis: No active plot found.")
        if active_tag in self.twin_axes:
            raise ValueError(f"Tag '{active_tag}' already has a twin axis. Cannot create another one.")
        ax1 = self._get_ax_by_tag(active_tag)
        if ax1.name != 'polar':
            raise TypeError("Axis is not polar.")
        pos = ax1.get_position()
        ax2 = self.fig.add_axes(pos, projection='polar', frameon=frameon)
        ax2.patch.set_alpha(0.0)
        try:
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
            num_used = len(ax1.lines) + len(ax1.containers)
            offset = num_used % len(colors)
            shifted = colors[offset:] + colors[:offset]
            ax2.set_prop_cycle(cycler(color=shifted))
        except (KeyError, IndexError):
            pass
        self.twin_axes[active_tag] = ax2
        self.active_target = 'twin'
        return self

    def target_primary(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """将后续操作的目标切换回主坐标轴（primary axis）。

        Args:
            tag (Optional[Union[str, int]], optional):
                如果提供，将确保 `last_active_tag` 指向该主轴，并切换上下文。
                如果为None，则只切换上下文到 'primary'。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        self.active_target = 'primary'
        if tag is not None:
            # 确保 last_active_tag 指向的是我们想操作的主轴
            # _get_ax_by_tag 会隐式校验tag存在性
            _ = self._get_ax_by_tag(tag) 
            self.last_active_tag = tag
        return self

    def target_twin(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """将后续操作的目标切换到孪生坐标轴（twin axis）。

        Args:
            tag (Optional[Union[str, int]], optional):
                如果提供，将确保 `last_active_tag` 指向该主轴，并切换上下文。
                如果为None，则只切换上下文到 'twin'，使用当前的 `last_active_tag`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果在没有孪生轴的子图上尝试切换到 'twin' 模式。
        """
        self.active_target = 'twin'
        
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("Cannot switch to twin mode: No active plot found and no tag specified.")

        if active_tag not in self.twin_axes:
            raise ValueError(f"Cannot switch to twin mode for tag '{active_tag}': No twin axis found. Did you call add_twinx() first?")

        # 如果提供了 tag，更新 last_active_tag
        if tag is not None:
            # 确保 tag 对应的主轴存在
            _ = self._get_ax_by_tag(tag)
            self.last_active_tag = tag
            
        return self

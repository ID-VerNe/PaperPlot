from typing import Optional, Union, Dict, Any
import logging
import matplotlib.pyplot as plt
from matplotlib import cycler

logger = logging.getLogger(__name__)

class TwinAxesMixin:
    def add_twinx(self, tag: Optional[Union[str, int]] = None, **kwargs) -> 'Plotter':
        """为指定或当前活动的子图创建一个共享X轴但拥有独立Y轴的“双Y轴”图。
        
        并切换Plotter的活动目标到新创建的孪生轴，以支持链式调用。

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
            logger.warning("No axes.prop_cycle colors found; fallback to default twin color cycle.")
            ax2.set_prop_cycle(cycler(color=self.color_manager._default_colors))
        # --- 颜色同步逻辑结束 ---
        
        # 存储孪生轴并切换上下文
        self.twin_axes[active_tag] = ax2
        self.active_target = 'twin'
        
        return self

    def add_polar_twin(self, tag: Optional[Union[str, int]] = None, frameon: bool = False) -> 'Plotter':
        """为指定或当前活动的极坐标子图创建一个孪生轴 (Twin Axis)。

        Args:
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果为None，则使用最后一次绘图的子图。
            frameon (bool, optional): 是否绘制边框。默认为 False。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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
            logger.warning("No axes.prop_cycle colors found; fallback to default polar twin color cycle.")
            ax2.set_prop_cycle(cycler(color=self.color_manager._default_colors))
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

    def add_twinx_line(self, **kwargs) -> 'Plotter':
        """[高层级 API] 一键为当前子图添加孪生轴并绘制线图。
        
        该方法会自动创建孪生轴（如果尚不存在），切换上下文，绘制线条，
        并默认切换回主轴上下文以便后续链式操作。

        Args:
            **kwargs: 转发给 `add_line` 的所有参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 记录当前 tag
        current_tag = kwargs.get('tag') if kwargs.get('tag') is not None else self.last_active_tag
        
        if current_tag not in self.twin_axes:
            self.add_twinx(tag=current_tag)
        else:
            self.target_twin(tag=current_tag)
            
        # 移除 tag 参数，防止 add_line 重新注册 tag 导致 DuplicateTagError
        if 'tag' in kwargs:
            kwargs.pop('tag')

        # 绘图 (此时已经在 twin 模式下)
        self.add_line(**kwargs)
        
        # 绘制完成后通常建议切回 primary，或者保持 twin? 
        # 为了符合 add_line 的直觉，我们保持在当前状态，但提供方便
        return self

    def add_dual_axis_line(
        self,
        data,
        x: str,
        left: Dict[str, Any],
        right: Dict[str, Any],
        ylabel_left: Optional[str] = None,
        ylabel_right: Optional[str] = None,
        tag: Optional[Union[str, int]] = None,
        legend: str = 'merged',
        legend_loc: str = 'best',
        **legend_kwargs,
    ) -> 'Plotter':
        """[高层级 API] 一次性绘制双轴折线图并可自动合并图例。"""
        active_tag = tag if tag is not None else self.last_active_tag
        if active_tag is None:
            raise ValueError("Cannot draw dual axis line: No active plot found and no tag specified.")

        left_cfg = dict(left)
        right_cfg = dict(right)

        left_y = left_cfg.pop('y', None)
        right_y = right_cfg.pop('y', None)
        if left_y is None or right_y is None:
            raise ValueError("Both left and right configs must include key 'y'.")

        left_label = left_cfg.get('label', left_y)
        right_label = right_cfg.get('label', right_y)
        left_color = left_cfg.get('color')
        right_color = right_cfg.get('color')

        prev_target = self.active_target
        prev_tag = self.last_active_tag

        self.target_primary(tag=active_tag)
        self.add_line(data=data, x=x, y=left_y, tag=active_tag, **left_cfg)

        if active_tag not in self.twin_axes:
            self.add_twinx(tag=active_tag)
        else:
            self.target_twin(tag=active_tag)

        self.add_line(data=data, x=x, y=right_y, **right_cfg)

        ax_left = self._get_ax_by_tag(active_tag)
        ax_right = self.twin_axes[active_tag]

        if ylabel_left is not None:
            ax_left.set_ylabel(ylabel_left)
        if ylabel_right is not None:
            ax_right.set_ylabel(ylabel_right)

        if left_color:
            ax_left.yaxis.label.set_color(left_color)
            ax_left.tick_params(axis='y', colors=left_color)
        if right_color:
            ax_right.yaxis.label.set_color(right_color)
            ax_right.tick_params(axis='y', colors=right_color)

        self.target_primary(tag=active_tag)
        if legend == 'merged':
            self.set_legend(tag=active_tag, loc=legend_loc, **legend_kwargs)
        elif legend == 'separate':
            ax_left.legend(loc=legend_loc, **legend_kwargs)
            ax_right.legend(loc=legend_loc, **legend_kwargs)
        elif legend == 'none':
            logger.debug("Dual-axis legend disabled by legend='none'.")
        else:
            raise ValueError("legend must be one of: 'merged', 'separate', 'none'.")

        self.last_active_tag = active_tag if prev_tag is None else active_tag
        self.active_target = prev_target if prev_target in ('primary', 'twin') else 'primary'
        return self

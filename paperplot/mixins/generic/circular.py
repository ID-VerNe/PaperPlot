from typing import Optional, Union, Sequence
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CircularPlotsMixin:
    def add_polar_bar(self, **kwargs) -> 'Plotter':
        """在极坐标轴上绘制柱状图。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame): 数据源 DataFrame (必需)。
                - theta (str): 角度数据列名 (弧度制)。
                - r (str): 半径/高度数据列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                - ax (plt.Axes, optional): 指定 Axes 对象。必须是极坐标轴。
                
                样式参数:
                - width (float or str, optional): 柱宽。如果是字符串，则为 `data` 中的列名。
                - bottom (float or str, optional): 柱底起始位置。默认为 0.0。
                - ... 其他传递给 `ax.bar` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            TypeError: 如果目标轴不是极坐标轴，或 `data` 不是 DataFrame。
        """
        data = kwargs.pop('data', None)
        theta_key = kwargs.pop('theta')
        r_key = kwargs.pop('r')
        width = kwargs.pop('width', None)
        bottom = kwargs.pop('bottom', 0.0)
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        if _ax.name != 'polar':
            raise TypeError("Axis is not polar. Create with ax_configs={'tag': {'projection': 'polar'}}.")
        if isinstance(data, pd.DataFrame):
            theta = data[theta_key]
            r = data[r_key]
            if width is None:
                if len(theta) > 1:
                    d = np.diff(np.sort(theta))
                    w = np.median(d)
                else:
                    w = 0.1
            else:
                w = width
            _ax.bar(theta, r, width=w, bottom=bottom, **kwargs)
            cache_df = data[[theta_key, r_key]]
        else:
            raise TypeError("'data' must be a pandas DataFrame for polar bar.")
        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_pie(self, **kwargs) -> 'Plotter':
        """绘制饼图。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - sizes (str): 数值大小列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - labels (List[str], optional): 标签列表。
                - colors (List[str], optional): 颜色列表。
                - autopct (str or Callable, optional): 数值标签格式。
                - startangle (float, optional): 起始角度。
                - ... 其他传递给 `ax.pie` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            sizes_col = data_names['sizes']
            labels = p_kwargs.pop('labels', None)
            ax.pie(cache_df[sizes_col], labels=labels if isinstance(labels, Sequence) else None, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['sizes'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_donut(self, **kwargs) -> 'Plotter':
        """绘制环形图 (Donut Chart)。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - sizes (str): 数值大小列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - labels (List[str], optional): 标签列表。
                - width (float, optional): 环的宽度 (0-1)。默认为 0.4。
                - radius (float, optional): 外半径。默认为 1.0。
                - colors (List[str], optional): 颜色列表。
                - autopct (str or Callable, optional): 数值标签格式。
                - ... 其他传递给 `ax.pie` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            sizes_col = data_names['sizes']
            labels = p_kwargs.pop('labels', None)
            width = p_kwargs.pop('width', 0.4)
            radius = p_kwargs.pop('radius', 1.0)
            ax.pie(cache_df[sizes_col], labels=labels if isinstance(labels, Sequence) else None, radius=radius, wedgeprops={"width": width}, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['sizes'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_nested_donut(self, **kwargs) -> 'Plotter':
        """绘制嵌套环形图 (Nested Donut Chart)。

        Args:
            **kwargs:
                核心参数:
                - outer (Dict): 外层环配置。包含 'data' (DataFrame), 'sizes' (列名), 'labels' (可选)。
                - inner (Dict): 内层环配置。包含 'data' (DataFrame), 'sizes' (列名), 'labels' (可选)。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - ... 其他传递给 `ax.pie` 的参数 (作用于两层)。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        kwargs.setdefault('data', pd.DataFrame())

        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            outer = p_kwargs.pop('outer')
            inner = p_kwargs.pop('inner')
            if not (isinstance(outer, dict) and isinstance(inner, dict)):
                raise TypeError("'outer' and 'inner' must be dicts with keys: data, sizes, labels.")
            od = outer['data']
            os_key = outer['sizes']
            ol = outer.get('labels')
            idf = inner['data']
            is_key = inner['sizes']
            il = inner.get('labels')
            ax.pie(od[os_key], labels=ol if isinstance(ol, Sequence) else None, radius=1.0, wedgeprops={"width": 0.4})
            ax.pie(idf[is_key], labels=il if isinstance(il, Sequence) else None, radius=0.6, wedgeprops={"width": 0.4})
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key=None,
            **kwargs
        )

    def add_radial_grouped_bar(self, **kwargs) -> 'Plotter':
        """绘制径向分组柱状图 (Radial Grouped Bar Chart)。
        
        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame): 数据源 DataFrame。
                - theta (str): 类别/角度数据列名。
                - r (str): 数值/半径数据列名。
                - hue (str): 分组变量列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - width (float, optional): 整个扇区的总宽度 (弧度)。默认为 0.8 * (2*pi / N)。
                - inner_radius (float, optional): 内圆半径 (用于创建空心效果)。默认为 0.0。
                - bottom (float, optional): 柱底起始位置。默认为 `inner_radius`。
                - alpha (float, optional): 透明度。默认为 0.8。
                - show_grid (bool, optional): 是否显示网格。默认为 True。
                - ... 其他传递给 `ax.bar` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            theta_col = data_names['theta']
            r_col = data_names['r']
            hue_col = data_names['hue']
            
            # Pivot data
            pivot_df = cache_df.pivot(index=theta_col, columns=hue_col, values=r_col)
            categories = pivot_df.index
            groups = pivot_df.columns
            n_cats = len(categories)
            n_groups = len(groups)
            
            # Calculate angles
            angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False)
            sector_width = 2 * np.pi / n_cats
            
            # User specified total width factor (0-1 relative to sector) or absolute
            total_width_rad = p_kwargs.pop('width', sector_width * 0.8)
            bar_width = total_width_rad / n_groups
            
            inner_radius = p_kwargs.pop('inner_radius', 0.0)
            bottom = p_kwargs.pop('bottom', inner_radius)
            alpha = p_kwargs.pop('alpha', 0.8)
            show_grid = p_kwargs.pop('show_grid', True)
            
            # Configure axes
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            ax.set_xticks(angles)
            ax.set_xticklabels(categories)
            ax.set_yticklabels([]) # Hide radial labels by default for cleaner look
            
            if not show_grid:
                ax.grid(False)
                ax.spines['polar'].set_visible(False)
            
            for i, group in enumerate(groups):
                # Calculate offset for this group
                # Center of sector is 'angle'
                # Center of this bar is calculated relative to the sector center
                group_center_offset = (i - (n_groups - 1) / 2) * bar_width
                bar_angles = angles + group_center_offset
                
                values = pivot_df[group].fillna(0)
                label = str(group)
                color = self.color_manager.get_color(label)
                
                ax.bar(bar_angles, values, width=bar_width, bottom=bottom, 
                       label=label, color=color, alpha=alpha, **p_kwargs)
                       
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['theta', 'r', 'hue'],
            plot_defaults_key='bar',
            **kwargs
        )

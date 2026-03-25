from typing import Optional, Union
import matplotlib.pyplot as plt
import seaborn as sns

class BasicPlotsMixin:
    def add_line(self, **kwargs) -> 'Plotter':
        """在子图上绘制线图 (封装 `matplotlib.axes.Axes.plot`)。

        Args:
            **kwargs: 
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str or array-like): x轴数据。如果是字符串，则为 `data` 中的列名。
                - y (str or array-like): y轴数据。如果是字符串，则为 `data` 中的列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                - ax (plt.Axes, optional): 直接指定绘图的目标 Axes 对象。
                
                样式参数 (传递给 `ax.plot`):
                - color (str): 线条颜色。
                - linestyle (str): 线型 (e.g., '-', '--', ':')。
                - linewidth (float): 线宽。
                - label (str): 图例标签。
                - ... 其他 `matplotlib.lines.Line2D` 支持的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        plot_logic = lambda ax, data_map, cache_df, data_names, **p_kwargs: ax.plot(data_map['x'], data_map['y'], **p_kwargs)
        
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y'],
            plot_defaults_key='line',
            **kwargs
        )

    def add_bar(self, orientation: str = 'vertical', categorical: bool = True, **kwargs) -> 'Plotter':
        """在子图上绘制条形图 (封装 `matplotlib.axes.Axes.bar` 或 `barh`)。

        Args:
            orientation (str, optional): 'vertical' (垂直柱状图) 或 'horizontal' (水平条形图)。默认为 'vertical'。
            categorical (bool, optional): 是否强制将坐标轴视为分类变量。
                如果为 True (默认)，则 X/Y 轴数据会被强转为字符串，确保等宽等距。
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str or array-like): x轴数据（类别或位置）。如果是字符串，则为 `data` 中的列名。
                - y (str or array-like): y轴数据（高度）。如果是字符串，则为 `data` 中的列名。
                - y_err (str or array-like, optional): 误差棒数据。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数 (传递给 `ax.bar` 或 `ax.barh`):
                - color (str): 条形颜色。
                - width/height (float): 条形宽度/高度（根据orientation自动选择）。
                - align (str): 对齐方式 ('center' or 'edge')。
                - label (str): 图例标签。
                - ... 其他参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            y_err_data = data_map.get('y_err')
            
            x_data = data_map['x']
            y_data = data_map['y']

            # 如果启用分类防御机制，将坐标轴数据强转为字符串
            if categorical:
                if orientation == 'horizontal':
                    # 水平条形图，y 是类别轴
                    y_data = y_data.astype(str)
                else:
                    # 垂直条形图，x 是类别轴
                    x_data = x_data.astype(str)

            if orientation == 'horizontal':
                # 水平条形图：barh(y=位置, width=长度)
                ax.barh(x_data, y_data, xerr=y_err_data, **p_kwargs)
            else:
                # 垂直柱状图：bar(x=位置, height=高度)
                ax.bar(x_data, y_data, yerr=y_err_data, **p_kwargs)
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'y_err'],
            plot_defaults_key='bar',
            **kwargs
        )

    def add_scatter(self, orientation: str = 'vertical', **kwargs) -> 'Plotter':
        """在子图上绘制散点图 (封装 `matplotlib.axes.Axes.scatter`)。

        Args:
            orientation (str, optional): 如果为 'horizontal'，则交换 x 和 y 数据。默认为 'vertical'。
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str or array-like): x轴数据。如果是字符串，则为 `data` 中的列名。
                - y (str or array-like): y轴数据。如果是字符串，则为 `data` 中的列名。
                - s (str or float or array-like, optional): 点的大小。如果是字符串，则为 `data` 中的列名。
                - c (str or array-like, optional): 点的颜色或序列。如果是字符串，且在 `data` 中存在，则映射该列颜色；否则作为颜色值。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数 (传递给 `ax.scatter`):
                - marker (str): 标记样式。
                - alpha (float): 透明度。
                - cmap (str): 颜色映射表 (当 `c` 为数值序列时使用)。
                - label (str): 图例标签。
                - ... 其他 `matplotlib.collections.PathCollection` 支持的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def _plot_scatter_logic(ax, data_map, cache_df, data_names, **plot_kwargs):
            x_data = data_map['x']
            y_data = data_map['y']
            
            # 如果是水平模式，交换 X 和 Y 的数据
            if orientation == 'horizontal':
                x_data, y_data = y_data, x_data
            
            if 's' in plot_kwargs and isinstance(plot_kwargs['s'], str):
                plot_kwargs['s'] = data_map.get(plot_kwargs['s'])
            if 'c' in plot_kwargs and isinstance(plot_kwargs['c'], str):
                plot_kwargs['c'] = data_map.get(plot_kwargs['c'])
            
            mappable = ax.scatter(x_data, y_data, **plot_kwargs)
            return mappable

        data_keys = ['x', 'y']
        if 's' in kwargs and isinstance(kwargs['s'], str):
            data_keys.append('s')
        if 'c' in kwargs and isinstance(kwargs['c'], str):
            data_keys.append('c')

        return self._execute_plot(
            plot_func=_plot_scatter_logic,
            data_keys=data_keys,
            plot_defaults_key='scatter',
            **kwargs
        )

    def add_hist(self, **kwargs) -> 'Plotter':
        """在子图上绘制直方图 (封装 `matplotlib.axes.Axes.hist`)。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str or array-like): 需要计算直方图的数据。如果是字符串，则为 `data` 中的列名。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数 (传递给 `ax.hist`):
                - bins (int or sequence): 直方图箱数或边界。
                - density (bool): 是否归一化为概率密度。
                - color (str): 填充颜色。
                - alpha (float): 透明度。
                - label (str): 图例标签。
                - ... 其他 `matplotlib.patches.Rectangle` 支持的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        plot_logic = lambda ax, data_map, cache_df, data_names, **p_kwargs: ax.hist(data_map['x'], **p_kwargs)
        
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x'],
            plot_defaults_key='hist',
            **kwargs
        )

    def add_box(self, orientation: str = 'vertical', **kwargs) -> 'Plotter':
        """在子图上绘制箱线图 (封装 `seaborn.boxplot`)。

        Args:
            orientation (str, optional): 'vertical' 或 'horizontal'。默认为 'vertical'。
            **kwargs:
                核心参数:
                - data (pd.DataFrame, optional): 数据源 DataFrame。
                - x (str, optional): x轴变量名（通常用于分组）。
                - y (str, optional): y轴变量名（数值变量）。
                - hue (str, optional): 分组变量名（用于颜色区分）。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数 (传递给 `sns.boxplot`):
                - order, hue_order: 指定类别顺序。
                - color: 颜色。
                - palette: 调色板。
                - ... 其他 `seaborn.boxplot` 支持的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue')
            
            # 映射 orientation 到 seaborn 的 orient 参数 ('v' 或 'h')
            sns_orient = 'h' if orientation == 'horizontal' else 'v'
            
            sns.boxplot(
                data=cache_df, 
                x=data_names.get('x'), 
                y=data_names.get('y'), 
                hue=hue_col, 
                orient=sns_orient,
                ax=ax, 
                **p_kwargs
            )
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y', 'hue'],
            plot_defaults_key=None,
            **kwargs
        )

    def add_heatmap(self, **kwargs) -> 'Plotter':
        """在子图上绘制热图 (封装 `seaborn.heatmap`)。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame): 数据源 DataFrame (必需)。通常是矩阵形式的数据。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数 (传递给 `sns.heatmap`):
                - cmap (str or Colormap): 颜色映射表。
                - annot (bool): 是否在单元格中显示数值。
                - fmt (str): 数值格式化字符串。
                - cbar (bool): 是否显示颜色条。默认为 True。
                - ... 其他 `seaborn.heatmap` 支持的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            if 'cmap' not in p_kwargs:
                try:
                    primary_color = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
                    custom_cmap = sns.light_palette(primary_color, as_cmap=True)
                    p_kwargs['cmap'] = custom_cmap
                except (KeyError, IndexError):
                    p_kwargs.setdefault('cmap', 'viridis')

            create_cbar = p_kwargs.pop('cbar', True)
            sns.heatmap(cache_df, ax=ax, cbar=create_cbar, **p_kwargs)

            if hasattr(ax, 'collections') and ax.collections:
                return ax.collections[0]
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[],
            plot_defaults_key=None,
            **kwargs
        )

    def add_blank(self, tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """在指定或下一个可用的子图位置创建一个空白区域并关闭坐标轴。

        Args:
            tag (Optional[Union[str, int]], optional): 
                指定要设为空白的子图标签。如果不提供，则作用于下一个默认子图。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag)
        _ax.axis('off')
        self.last_active_tag = resolved_tag
        return self

    def add_radar(self, **kwargs) -> 'Plotter':
        """在子图上绘制雷达图/蜘蛛图 (Radar/Spider Chart)。

        Args:
            **kwargs:
                核心参数:
                - data (pd.DataFrame): 数据源 DataFrame。
                - theta (str): 角度/维度数据列名（例如指标名称）。
                - r (str): 半径/数值数据列名。
                - hue (str, optional): 分组变量列名。如果提供，将绘制多个系列对比。
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - fill (bool, optional): 是否填充颜色。默认为 True。
                - alpha (float, optional): 填充透明度。默认为 0.25。
                - linewidth (float, optional): 线宽。
                - ... 其他传递给 `ax.plot` 和 `ax.fill` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
            
        Note:
            目标轴必须是极坐标投影 (projection='polar')。
        """
        import numpy as np
        
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            theta_col = data_names['theta']
            r_col = data_names['r']
            hue_col = data_names.get('hue')
            
            fill = p_kwargs.pop('fill', True)
            alpha = p_kwargs.pop('alpha', 0.25)
            
            if hue_col:
                # 分组绘制多个系列
                groups = cache_df[hue_col].unique()
                for group in groups:
                    group_df = cache_df[cache_df[hue_col] == group]
                    
                    # 获取类别和数值
                    categories = group_df[theta_col].values
                    values = group_df[r_col].values
                    
                    # 计算角度
                    N = len(categories)
                    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
                    
                    # 闭合图形
                    values = np.concatenate((values, [values[0]]))
                    angles += angles[:1]
                    
                    # 获取颜色
                    color = self.color_manager.get_color(group)
                    
                    # 绘制线条和填充
                    ax.plot(angles, values, 'o-', label=group, color=color, **p_kwargs)
                    if fill:
                        ax.fill(angles, values, alpha=alpha, color=color)
                
                # 设置类别标签
                ax.set_xticks(np.linspace(0, 2 * np.pi, N, endpoint=False))
                ax.set_xticklabels(categories)
            else:
                # 单个系列
                categories = cache_df[theta_col].values
                values = cache_df[r_col].values
                
                # 计算角度
                N = len(categories)
                angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
                
                # 闭合图形
                values = np.concatenate((values, [values[0]]))
                angles += angles[:1]
                
                # 绘制线条和填充
                ax.plot(angles, values, 'o-', **p_kwargs)
                if fill:
                    ax.fill(angles, values, alpha=alpha)
                
                # 设置类别标签
                ax.set_xticks(np.linspace(0, 2 * np.pi, N, endpoint=False))
                ax.set_xticklabels(categories)
            
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['theta', 'r', 'hue'],
            plot_defaults_key='line',
            **kwargs
        )

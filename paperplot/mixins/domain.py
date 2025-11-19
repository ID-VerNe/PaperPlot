# paperplot/mixins/domain.py

from typing import Optional, Union, List, Tuple, Callable, Dict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from .. import utils
from ..exceptions import DuplicateTagError
from ..utils import _data_to_dataframe

class DomainSpecificPlotsMixin:
    """包含领域专用绘图方法的 Mixin 类。"""
    def add_spectra(self, **kwargs) -> 'Plotter':
        """在同一个子图上绘制多条带垂直偏移的光谱。

        此方法用于并排比较多条光谱数据（例如拉曼光谱、红外光谱），
        通过垂直偏移避免谱线重叠。

        Args:
            data (Optional[pd.DataFrame], optional): 包含光谱数据的DataFrame。
            x (str or array-like): x轴数据（如波数、波长）或 `data` 中的列名。
            y_cols (List[str] or List[array-like]):
                一个列表，包含y轴数据（强度）或 `data` 中的多个列名。
            offset (float, optional): 每条光谱之间的垂直偏移量。默认为 0。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给每条线的 `ax.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 从 kwargs 中提取参数
        data = kwargs.pop('data', None)
        x = kwargs.pop('x')
        y_cols = kwargs.pop('y_cols')
        offset = kwargs.pop('offset', 0)
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        final_kwargs = {**self._get_plot_defaults('line'), **kwargs}

        x_data, y_data_list, cache_df, y_col_names = None, [], None, []

        if isinstance(data, pd.DataFrame):
            if not isinstance(x, str) or not all(isinstance(yc, str) for yc in y_cols):
                raise ValueError("If 'data' is a DataFrame, 'x' and 'y_cols' must be strings or a list of strings.")
            x_data = data[x]
            y_data_list = [data[yc] for yc in y_cols]
            y_col_names = y_cols
            cache_df = data[[x] + y_cols]
        elif data is None:
            x_data = np.array(x)
            y_data_list = [np.array(yc) for yc in y_cols]
            df_dict = {'x': x_data}
            y_col_names = [f'y_{i}' for i in range(len(y_cols))]
            for i, name in enumerate(y_col_names):
                df_dict[name] = y_data_list[i]
            cache_df = _data_to_dataframe(**df_dict)
        else:
            raise TypeError(f"The 'data' argument must be a pandas DataFrame or None, but got {type(data)}.")

        for i, y_data in enumerate(y_data_list):
            label = final_kwargs.pop('label', y_col_names[i])
            _ax.plot(x_data, y_data + i * offset, label=label, **final_kwargs)
        
        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_concentration_map(self, **kwargs) -> 'Plotter':
        """绘制浓度图或SERS Mapping图。

        本质上是一个带有特定预设（如 'inferno' colormap）的热图，
        常用于可视化表面增强拉曼散射（SERS）的 mapping 数据。

        Args:
            data (pd.DataFrame): 用于绘制热图的二维矩形数据。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            cbar (bool, optional): 是否绘制颜色条。默认为 `True`。
            xlabel (str, optional): X轴标签。默认为 'X (μm)'。
            ylabel (str, optional): Y轴标签。默认为 'Y (μm)'。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            create_cbar = p_kwargs.pop('cbar', True)
            p_kwargs.setdefault('cmap', 'inferno')
            
            # heatmap 直接使用 cache_df (原始的二维 DataFrame)
            sns.heatmap(cache_df, ax=ax, cbar=create_cbar, **p_kwargs)
            
            ax.set_xlabel(p_kwargs.pop('xlabel', 'X (μm)'))
            ax.set_ylabel(p_kwargs.pop('ylabel', 'Y (μm)'))

            # 返回 mappable 对象以支持 colorbar
            if hasattr(ax, 'collections') and ax.collections:
                return ax.collections[0]
            return None

        # 对于 heatmap, data_keys 是空的，因为我们直接使用传入的 data DataFrame
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=[], 
            plot_defaults_key=None,
            **kwargs
        )

    def add_confusion_matrix(self, **kwargs) -> 'Plotter':
        """可视化分类模型的混淆矩阵。

        此方法使用带有计数的着色热图来表示分类模型的性能。

        Args:
            matrix (array-like): 混淆矩阵，形状为 `(n_classes, n_classes)`。
            class_names (List[str]): 类别名称列表，用于矩阵的行和列标签。
            normalize (bool, optional): 如果为 `True`，则将矩阵按行归一化
                以显示百分比。默认为 `False`。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数，
                      例如 `cmap`, `annot`, `fmt`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 从 kwargs 中提取参数
        matrix = kwargs.pop('matrix')
        class_names = kwargs.pop('class_names')
        normalize = kwargs.pop('normalize', False)
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

        if normalize:
            matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
            fmt = '.2f'
        else:
            fmt = 'd'
        
        df_cm = pd.DataFrame(matrix, index=class_names, columns=class_names)

        kwargs.setdefault('annot', True)
        kwargs.setdefault('fmt', fmt)
        kwargs.setdefault('cmap', 'Blues')
        
        sns.heatmap(df_cm, ax=_ax, **kwargs)

        _ax.set_xlabel('Predicted Label')
        _ax.set_ylabel('True Label')
        
        self.data_cache[resolved_tag] = df_cm
        self.last_active_tag = resolved_tag
        return self

    def add_roc_curve(self, **kwargs) -> 'Plotter':
        """绘制一个或多个分类的ROC（接收者操作特征）曲线。

        Args:
            fpr (Dict[str, np.ndarray]):
                一个字典，键是类别名，值是该类别的假正率（False Positive Rate）数组。
            tpr (Dict[str, np.ndarray]):
                一个字典，键是类别名，值是该类别的真正率（True Positive Rate）数组。
            roc_auc (Dict[str, float]):
                一个字典，键是类别名，值是该类别的AUC（曲线下面积）得分。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给每个ROC曲线的 `ax.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 从 kwargs 中提取参数
        fpr = kwargs.pop('fpr')
        tpr = kwargs.pop('tpr')
        roc_auc = kwargs.pop('roc_auc')
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        final_kwargs = {**self._get_plot_defaults('line'), **kwargs}

        for key in fpr.keys():
            label = f'{key} (AUC = {roc_auc[key]:.2f})'
            _ax.plot(fpr[key], tpr[key], label=label, **final_kwargs)

        _ax.plot([0, 1], [0, 1], 'k--', lw=2)
        
        _ax.set_xlim([0.0, 1.0])
        _ax.set_ylim([0.0, 1.05])
        _ax.set_xlabel('False Positive Rate')
        _ax.set_ylabel('True Positive Rate')
        _ax.set_title('Receiver Operating Characteristic (ROC) Curve')
        _ax.legend(loc="lower right")
        
        self.last_active_tag = resolved_tag
        return self

    def add_pca_scatter(self, **kwargs) -> 'Plotter':
        """绘制PCA降维结果的散点图。

        此方法是 `seaborn.scatterplot` 的一个包装器，专门用于可视化
        主成分分析（PCA）的结果。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x_pc (str or array-like): x轴数据（通常是第一主成分）或 `data` 中的列名。
            y_pc (str or array-like): y轴数据（通常是第二主成分）或 `data` 中的列名。
            hue (str, optional): 用于产生不同颜色点的分类变量的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `seaborn.scatterplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            hue_col = data_names.get('hue')
            sns.scatterplot(data=cache_df, x=data_names['x_pc'], y=data_names['y_pc'], 
                            hue=hue_col, ax=ax, **p_kwargs)
            # scatterplot 返回一个 PathCollection，可以作为 mappable
            return ax.collections[0] if ax.collections else None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x_pc', 'y_pc', 'hue'],
            plot_defaults_key='scatter',
            **kwargs
        )

    def add_power_timeseries(self, **kwargs) -> 'Plotter':
        """绘制电力系统动态仿真结果的时间序列图。

        此方法用于可视化一个或多个变量随时间的变化，并可选择性地
        在图上标记重要的事件点。

        Args:
            data (pd.DataFrame): 包含仿真结果的DataFrame。
            x (str): `data` 中表示时间轴的列名。
            y_cols (List[str]): `data` 中要绘制的一个或多个变量的列名列表。
            events (Dict[str, float], optional): 一个字典，键是事件的描述性
                标签，值是事件发生的x轴（时间）位置。默认为 `None`。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `ax.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        # 1. 从 kwargs 中提取参数
        data = kwargs.pop('data')
        x = kwargs.pop('x')
        y_cols = kwargs.pop('y_cols')
        events = kwargs.pop('events', None)
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        # 2. 解析子图和tag
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        self.last_active_tag = resolved_tag # 立即设置活动tag
        
        # 3. 合并样式
        final_kwargs = {**self._get_plot_defaults('line'), **kwargs}
        x_data = data[x]

        # 4. 循环绘制每一条线
        for y_col_name in y_cols:
            y_data = data[y_col_name]
            label = final_kwargs.pop('label', y_col_name) # 为每条线获取独立的label
            _ax.plot(x_data, y_data, label=label, **final_kwargs)

        # 5. 添加事件标记
        if events and isinstance(events, dict):
            self.add_event_markers(
                event_dates=list(events.keys()),
                labels=list(events.values())
            )
        
        # 6. 设置默认标签和图例
        _ax.set_xlabel(final_kwargs.get('xlabel', 'Time (s)'))
        _ax.set_ylabel(final_kwargs.get('ylabel', 'Value'))
        # 检查是否有可显示的图例
        handles, labels = _ax.get_legend_handles_labels()
        if handles:
             _ax.legend()
        
        # 7. 更新状态
        self.data_cache[resolved_tag] = data[[x] + y_cols]
        return self

    def add_phasor_diagram(self, **kwargs) -> 'Plotter':
        """在极坐标子图上绘制相量图。

        此方法用于可视化电力系统中的电压、电流等相量。

        Args:
            magnitudes (List[float]): 相量幅值的列表。
            angles (List[float]): 相量角度的列表。
            labels (List[str], optional): 每个相量的标签列表。
            angle_unit (str, optional): 角度的单位 ('degrees' 或 'radians')。
                默认为 'degrees'。
            tag (Optional[Union[str, int]], optional): 目标子图的标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给标签文本 `ax.text` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果 `magnitudes` 和 `angles` 列表长度不匹配，
                        或者目标子图不是极坐标投影。
        """
        # 从 kwargs 中提取参数
        magnitudes = kwargs.pop('magnitudes')
        angles = kwargs.pop('angles')
        labels = kwargs.pop('labels', None)
        angle_unit = kwargs.pop('angle_unit', 'degrees')
        tag = kwargs.pop('tag', None)
        ax = kwargs.pop('ax', None)

        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

        if len(magnitudes) != len(angles):
            raise ValueError("幅值和角度列表的长度必须相同。")

        if _ax.name != 'polar':
            raise ValueError(
                f"相量图需要一个极坐标轴，但子图 '{resolved_tag}' 是 '{_ax.name}' 类型。 "
                f"请在 Plotter 初始化时配置该子图的投影。"
            )
        
        _ax.set_theta_zero_location('E')
        _ax.set_theta_direction(-1)

        if angle_unit == 'degrees':
            angles_rad = np.deg2rad(angles)
        else:
            angles_rad = np.array(angles)

        legend_handles = []
        for i, (mag, ang_rad) in enumerate(zip(magnitudes, angles_rad)):
            color = plt.cm.viridis(i / len(magnitudes))
            label = labels[i] if labels and i < len(labels) else f'Phasor {i+1}'

            _ax.annotate(
                '', xy=(ang_rad, mag), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=8, shrink=0)
            )

            if labels and i < len(labels):
                text_kwargs = kwargs.copy()
                text_kwargs.setdefault('ha', 'center')
                text_kwargs.setdefault('va', 'bottom')
                text_kwargs.setdefault('fontsize', 10)
                text_offset_mag = mag * 1.1
                _ax.text(ang_rad, text_offset_mag, labels[i], **text_kwargs)
            
            legend_handles.append(plt.Line2D([0], [0], color=color, lw=2, label=label))

        max_mag = max(magnitudes) if magnitudes else 1
        _ax.set_rlim(0, max_mag * 1.2)
        _ax.set_thetagrids(np.arange(0, 360, 30))
        _ax.set_rticks(np.linspace(0, max_mag, 3))
        _ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.05, 1))

        self.last_active_tag = resolved_tag
        return self

    def add_bifurcation_diagram(self, **kwargs) -> 'Plotter':
        """绘制电力系统稳定性分析中的分岔图。

        这本质上是一个散点图，用于显示系统状态变量如何随某个
        分岔参数的变化而变化。

        Args:
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            x (str or array-like): x轴数据（分岔参数）或 `data` 中的列名。
            y (str or array-like): y轴数据（状态变量）或 `data` 中的列名。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `ax.scatter` 的关键字参数。
                      默认使用 'bifurcation' 样式（小、半透明的黑点）。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            ax.scatter(data_map['x'], data_map['y'], **p_kwargs)
            ax.set_xlabel(p_kwargs.get('xlabel', 'Bifurcation Parameter'))
            ax.set_ylabel(p_kwargs.get('ylabel', 'State Variable'))
            ax.set_title(p_kwargs.get('title', 'Bifurcation Diagram'))
            # 分岔图通常没有颜色条，所以返回 None
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y'],
            plot_defaults_key='bifurcation',
            **kwargs
        )
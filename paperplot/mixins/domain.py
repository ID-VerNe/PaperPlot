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
    """
    包含领域专用绘图方法的 Mixin 类。
    """
    def add_spectra(self, **kwargs) -> 'Plotter':
        """
        在同一个子图上绘制多条带垂直偏移的光谱。
        支持灵活的数据输入。
        所有参数通过 `kwargs` 传入。

        必需参数: `x`, `y_cols`。

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
        """
        绘制 SERS Mapping 图像，本质上是一个带有专业颜色映射和坐标轴的热图。
        此方法要求输入为DataFrame。

        Args:
            **kwargs: 包含 `data` (pd.DataFrame) 和其他传递给 `seaborn.heatmap` 的参数。
                      必需参数: `data`。

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
        """
        可视化分类模型的混淆矩阵。
        所有参数通过 `kwargs` 传入。

        必需参数: `matrix`, `class_names`。

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
        """
        绘制多分类或单分类的ROC曲线。
        所有参数通过 `kwargs` 传入。

        必需参数: `fpr`, `tpr`, `roc_auc` (均为字典)。

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
        """
        绘制PCA降维结果的散点图，并可根据类别进行着色。
        所有参数通过 `kwargs` 传入。
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
        """
        绘制电力系统动态仿真结果，并可选择性地标记事件。

        Args:
            **kwargs: 包含 `data`, `x`, `y_cols`, `events` 等参数。

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
                event_dates=list(events.values()),
                labels=list(events.keys())
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
        """
        在指定子图上绘制相量图。
        此方法要求目标子图必须是极坐标投影。
        所有参数通过 `kwargs` 传入。

        必需参数: `magnitudes`, `angles`。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
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
        """
        绘制电力系统稳定性分析中的分岔图。
        所有参数通过 `kwargs` 传入，支持 `data`, `x`, `y`, `tag`, `ax` 以及
        所有 `matplotlib.axes.Axes.scatter` 的参数。

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

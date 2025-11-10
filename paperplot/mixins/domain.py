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
    def add_spectra(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                    y_cols: Optional[Union[List[str], List[list]]] = None, 
                    tag: Optional[Union[str, int]] = None, 
                    ax: Optional[plt.Axes] = None, 
                    offset: float = 0, **kwargs) -> 'Plotter':
        """
        在同一个子图上绘制多条带垂直偏移的光谱。
        支持灵活的数据输入。

        Args:
            data (Optional[pd.DataFrame]): 数据框。
            x: X轴数据 (列名或array-like)。
            y_cols: 包含多个Y轴数据的列表 (列名列表或array-like列表)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            offset (float, optional): 连续光谱之间的垂直偏移量。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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

    def add_concentration_map(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, 
                              ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制 SERS Mapping 图像，本质上是一个带有专业颜色映射和坐标轴的热图。
        此方法要求输入为DataFrame。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。通常是二维数据，索引和列代表空间坐标。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        create_cbar = kwargs.pop('cbar', True)
        kwargs.setdefault('cmap', 'inferno')
        
        sns.heatmap(data, ax=_ax, cbar=create_cbar, **kwargs)
        
        if hasattr(_ax, 'collections') and _ax.collections:
            self.tag_to_mappable[resolved_tag] = _ax.collections[0]

        _ax.set_xlabel(kwargs.pop('xlabel', 'X (μm)'))
        _ax.set_ylabel(kwargs.pop('ylabel', 'Y (μm)'))

        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

    def add_confusion_matrix(self, matrix: Union[np.ndarray, pd.DataFrame], 
                             class_names: List[str], 
                             tag: Optional[Union[str, int]] = None, 
                             ax: Optional[plt.Axes] = None, 
                             normalize: bool = False, **kwargs) -> 'Plotter':
        """
        可视化分类模型的混淆矩阵。

        Args:
            matrix (Union[np.ndarray, pd.DataFrame]): 混淆矩阵。
            class_names (List[str]): 类别的名称列表。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            normalize (bool, optional): 如果为True，则将矩阵值归一化为百分比。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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

    def add_roc_curve(self, fpr: dict, tpr: dict, roc_auc: dict, 
                      tag: Optional[Union[str, int]] = None, 
                      ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制多分类或单分类的ROC曲线。

        Args:
            fpr (dict): 一个字典，键是类别名，值是假正率 (False Positive Rate) 数组。
            tpr (dict): 一个字典，键是类别名，值是真正率 (True Positive Rate) 数组。
            roc_auc (dict): 一个字典，键是类别名，值是AUC分数。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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

    def add_pca_scatter(self, data: Optional[pd.DataFrame] = None, x_pc: Optional[Union[str, list]] = None, 
                        y_pc: Optional[Union[str, list]] = None, hue: Optional[Union[str, list]] = None,
                        tag: Optional[Union[str, int]] = None, ax: Optional[plt.Axes] = None, 
                        **kwargs) -> 'Plotter':
        """
        绘制PCA降维结果的散点图，并可根据类别进行着色。

        Args:
            data: 数据框 (推荐) 或 None。
            x_pc, y_pc, hue: 列名或array-like数据。
            tag: 目标子图的tag。
            ax: 目标Axes。
            **kwargs: 其他传递给 `seaborn.scatterplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_to_plot = data
        x_col, y_col, hue_col = x_pc, y_pc, hue
        
        if data is None:
            df_kwargs = {'x_pc': x_pc, 'y_pc': y_pc}
            if hue is not None: df_kwargs['hue'] = hue
            data_to_plot = _data_to_dataframe(**df_kwargs)
            x_col, y_col = 'x_pc', 'y_pc'
            hue_col = 'hue' if hue is not None else None

        final_kwargs = {**self._get_plot_defaults('scatter'), **kwargs}
        sns.scatterplot(data=data_to_plot, x=x_col, y=y_col, hue=hue_col, ax=_ax, **final_kwargs)
        
        self.data_cache[resolved_tag] = data_to_plot
        self.last_active_tag = resolved_tag
        return self

    def add_power_timeseries(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                             y_cols: Optional[Union[List[str], List[list]]] = None, 
                             tag: Optional[Union[str, int]] = None, 
                             ax: Optional[plt.Axes] = None, 
                             events: Optional[dict] = None, **kwargs) -> 'Plotter':
        """
        绘制电力系统动态仿真结果，并可选择性地标记事件。

        Args:
            data (Optional[pd.DataFrame]): 数据框。
            x: X轴数据 (列名或array-like)。
            y_cols: 包含多个Y轴数据的列表 (列名列表或array-like列表)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            events (Optional[dict], optional): 事件标记字典。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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
            _ax.plot(x_data, y_data, label=label, **final_kwargs)

        if events and isinstance(events, dict):
            self.add_event_markers(
                event_dates=list(events.values()),
                labels=list(events.keys()),
                tag=resolved_tag
            )
        
        _ax.set_xlabel(kwargs.pop('xlabel', 'Time (s)'))
        _ax.set_ylabel(kwargs.pop('ylabel', 'Value'))
        if any(_ax.get_legend_handles_labels()):
             _ax.legend()

        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self

    def add_phasor_diagram(self, magnitudes: List[float], angles: List[float],
                           labels: Optional[List[str]] = None, tag: Optional[Union[str, int]] = None,
                           ax: Optional[plt.Axes] = None,
                           angle_unit: str = 'degrees', **kwargs) -> 'Plotter':
        """
        在指定子图上绘制相量图。
        此方法要求目标子图必须是极坐标投影。

        Args:
            magnitudes (List[float]): 相量的幅值列表。
            angles (List[float]): 相量的角度列表。
            labels (Optional[List[str]], optional): 相量的标签列表。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            angle_unit (str, optional): 角度的单位，'degrees' 或 'radians'。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
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

    def add_bifurcation_diagram(self, data: Optional[pd.DataFrame] = None, x: Optional[Union[str, list]] = None, 
                                y: Optional[Union[str, list]] = None, 
                                tag: Optional[Union[str, int]] = None, 
                                ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制电力系统稳定性分析中的分岔图。

        Args:
            data (Optional[pd.DataFrame]): 数据框。
            x: X轴数据 (列名或array-like)。
            y: Y轴数据 (列名或array-like)。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。
            ax (Optional[plt.Axes], optional): 目标Axes。
            **kwargs: 其他传递给 `ax.scatter` 的关键字参数。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        data_map, cache_df = self._prepare_data(data=data, x=x, y=y)

        scatter_kwargs = {**self._get_plot_defaults('bifurcation'), **kwargs}
        
        _ax.scatter(data_map['x'], data_map['y'], **scatter_kwargs)
        _ax.set_xlabel(kwargs.get('xlabel', 'Bifurcation Parameter'))
        _ax.set_ylabel(kwargs.get('ylabel', 'State Variable'))
        _ax.set_title(kwargs.get('title', 'Bifurcation Diagram'))

        self.data_cache[resolved_tag] = cache_df
        self.last_active_tag = resolved_tag
        return self
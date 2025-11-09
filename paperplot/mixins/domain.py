# paperplot/mixins/domain.py

from typing import Optional, Union, List, Tuple, Callable, Dict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .. import utils
from ..exceptions import DuplicateTagError

class DomainSpecificPlotsMixin:
    """
    包含领域专用绘图方法的 Mixin 类。
    """
    def add_spectra(self, data: pd.DataFrame, x: str, y_cols: List[str], 
                    tag: Optional[Union[str, int]] = None, 
                    ax: Optional[plt.Axes] = None, 
                    offset: float = 0, **kwargs) -> 'Plotter':
        """
        在同一个子图上绘制多条带垂直偏移的光谱。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名（如 'wavenumber'）。
            y_cols (List[str]): 一个包含多个Y轴列名的列表，每一列代表一条光谱。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            offset (float, optional): 连续光谱之间的垂直偏移量。默认为 0。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax = self._resolve_ax(tag, ax)

        for i, y_col in enumerate(y_cols):
            label = kwargs.pop('label', y_col) # 如果用户没有提供label，则使用列名
            _ax.plot(data[x], data[y_col] + i * offset, label=label, **kwargs)
        
        return self

    def add_concentration_map(self, data: pd.DataFrame, tag: Optional[Union[str, int]] = None, 
                              ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        绘制 SERS Mapping 图像，本质上是一个带有专业颜色映射和坐标轴的热图。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。通常是二维数据，索引和列代表空间坐标。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。
                      默认情况下会创建颜色条（`cbar=True`），但可以通过 `cbar=False` 禁用。
                      默认 `cmap` 为 'inferno'。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax = self._resolve_ax(tag, ax)
        
        create_cbar = kwargs.pop('cbar', True)
        kwargs.setdefault('cmap', 'inferno') # 默认使用 inferno 颜色映射
        
        import seaborn as sns
        sns.heatmap(data, ax=_ax, cbar=create_cbar, **kwargs)
        
        if tag and _ax.collections:
            self.tag_to_mappable[tag] = _ax.collections[0]

        _ax.set_xlabel(kwargs.pop('xlabel', 'X (μm)'))
        _ax.set_ylabel(kwargs.pop('ylabel', 'Y (μm)'))

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
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            normalize (bool, optional): 如果为True，则将矩阵值归一化为百分比。默认为False。
            **kwargs: 其他传递给 `seaborn.heatmap` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax = self._resolve_ax(tag, ax)

        if normalize:
            matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
            fmt = '.2f'
        else:
            fmt = 'd'
        
        df_cm = pd.DataFrame(matrix, index=class_names, columns=class_names)

        import seaborn as sns
        kwargs.setdefault('annot', True)
        kwargs.setdefault('fmt', fmt)
        kwargs.setdefault('cmap', 'Blues')
        
        sns.heatmap(df_cm, ax=_ax, **kwargs)

        _ax.set_xlabel('Predicted Label')
        _ax.set_ylabel('True Label')
        
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
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax = self._resolve_ax(tag, ax)

        # 绘制每个类别的ROC曲线
        for key in fpr.keys():
            label = f'{key} (AUC = {roc_auc[key]:.2f})'
            _ax.plot(fpr[key], tpr[key], label=label, **kwargs)

        # 绘制对角参考线
        _ax.plot([0, 1], [0, 1], 'k--', lw=2)
        
        _ax.set_xlim([0.0, 1.0])
        _ax.set_ylim([0.0, 1.05])
        _ax.set_xlabel('False Positive Rate')
        _ax.set_ylabel('True Positive Rate')
        _ax.set_title('Receiver Operating Characteristic (ROC) Curve')
        _ax.legend(loc="lower right")
        
        return self

    def add_pca_scatter(self, data: pd.DataFrame, x_pc: str, y_pc: str, 
                        tag: Optional[Union[str, int]] = None, 
                        ax: Optional[plt.Axes] = None, 
                        hue: Optional[str] = None, **kwargs) -> 'Plotter':
        """
        绘制PCA降维结果的散点图，并可根据类别进行着色。

        Args:
            data (pd.DataFrame): 包含PCA结果的数据框。
            x_pc (str): 代表X轴主成分的列名 (例如 'PC1')。
            y_pc (str): 代表Y轴主成分的列名 (例如 'PC2')。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            hue (Optional[str], optional): 用于对散点进行分组和着色的列名。
            **kwargs: 其他传递给 `seaborn.scatterplot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax = self._resolve_ax(tag, ax)
        
        import seaborn as sns
        sns.scatterplot(data=data, x=x_pc, y=y_pc, hue=hue, ax=_ax, **kwargs)
        
        return self

    def add_power_timeseries(self, data: pd.DataFrame, x: str, y_cols: List[str], 
                             tag: Optional[Union[str, int]] = None, 
                             ax: Optional[plt.Axes] = None, 
                             events: Optional[dict] = None, **kwargs) -> 'Plotter':
        """
        绘制电力系统动态仿真结果，并可选择性地标记事件。

        Args:
            data (pd.DataFrame): 包含绘图数据的数据框。
            x (str): 数据框中用于X轴的列名（通常是 'time'）。
            y_cols (List[str]): 一个包含多个Y轴列名的列表，每一列代表一个信号。
            tag (Optional[Union[str, int]], optional): 子图的唯一标识符。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
            events (Optional[dict], optional): 一个字典，用于标记事件。
                                              例如 `{'Fault': 1.0, 'Clear': 1.1}`，
                                              键是事件名，值是时间点。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax = self._resolve_ax(tag, ax)

        # 绘制时间序列线
        for y_col in y_cols:
            label = kwargs.pop('label', y_col)
            _ax.plot(data[x], data[y_col], label=label, **kwargs)

        # 标记事件
        if events and isinstance(events, dict):
            utils.add_event_markers(
                ax=_ax,
                event_dates=list(events.values()),
                labels=list(events.keys())
            )
        
        # 设置默认标签和图例
        _ax.set_xlabel(kwargs.pop('xlabel', 'Time (s)'))
        _ax.set_ylabel(kwargs.pop('ylabel', 'Value'))
        if any(_ax.get_legend_handles_labels()):
             _ax.legend()

        return self

    def add_phasor_diagram(self, magnitudes: List[float], angles: List[float],
                           labels: Optional[List[str]] = None, tag: Optional[Union[str, int]] = None,
                           ax: Optional[plt.Axes] = None,
                           angle_unit: str = 'degrees', **kwargs) -> 'Plotter':
        """
        在指定子图上绘制相量图。

        如果目标子图不是极坐标投影，它将被替换为一个新的极坐标子图。

        Args:
            magnitudes (List[float]): 相量的幅值列表。
            angles (List[float]): 相量的角度列表。
            labels (Optional[List[str]], optional): 相量的标签列表。默认为None。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。如果未提供，将自动分配。
            ax (Optional[plt.Axes], optional): 要在其上绘图的Matplotlib Axes对象。
                                             如果提供，则在此Axes上绘图；否则，将获取下一个可用Axes。
            angle_unit (str, optional): 角度的单位，'degrees' 或 'radians'。默认为 'degrees'。
            **kwargs: 其他传递给 `matplotlib.axes.Axes.plot` 或 `matplotlib.axes.Axes.annotate` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果幅值和角度列表长度不匹配，或者当`ax`提供时`tag`未提供。
            DuplicateTagError: 如果尝试使用一个已经存在的tag。
            TagNotFoundError: 如果指定的tag未找到。
        """
        _ax = self._resolve_ax(tag, ax)

        if len(magnitudes) != len(angles):
            raise ValueError("Magnitudes and angles lists must have the same length.")

        _target_ax: plt.Axes
        _assigned_tag: Union[str, int]

        if _ax is None:
            _target_ax, _assigned_tag = self._get_next_ax_and_assign_tag(tag)
        else:
            if tag is None:
                raise ValueError("When 'ax' is explicitly provided, a 'tag' must also be provided.")
            if tag in self.tag_to_ax and self.tag_to_ax[tag] != _ax:
                raise DuplicateTagError(tag)
            self.tag_to_ax[tag] = _ax
            _target_ax = _ax
            _assigned_tag = tag

        # 检查轴是否为极坐标投影
        if _target_ax.name != 'polar':
            raise ValueError(
                f"Phasor diagram requires a polar axis, but axis '{_assigned_tag}' is a '{_target_ax.name}' axis. "
                f"Please configure the axis projection in the Plotter constructor using, for example, "
                f"ax_configs={{'{_assigned_tag}': {{'projection': 'polar'}}}}."
            )
        
        # 设置极坐标轴的常见电气工程约定
        _target_ax.set_theta_zero_location('E') # 0度在右侧 (East)
        _target_ax.set_theta_direction(-1) # 角度顺时针增加

        # 转换角度为弧度
        if angle_unit == 'degrees':
            angles_rad = np.deg2rad(angles)
        else:
            angles_rad = np.array(angles)

        # 绘制相量
        legend_handles = []
        for i, (mag, ang_rad) in enumerate(zip(magnitudes, angles_rad)):
            color = plt.cm.viridis(i / len(magnitudes))
            label = labels[i] if labels and i < len(labels) else f'Phasor {i+1}'

            # 使用 annotate 方法绘制一个从原点指向目标点的箭头
            _target_ax.annotate(
                '',  # no text
                xy=(ang_rad, mag),  # 箭头指向的目标点 (angle, radius)
                xytext=(0, 0),  # 箭头开始的点 (origin)
                arrowprops=dict(
                    facecolor=color,
                    edgecolor=color,
                    width=1.5,
                    headwidth=8,
                    shrink=0
                )
            )

            # 添加标签
            if labels and i < len(labels):
                text_kwargs = kwargs.copy()
                text_kwargs.setdefault('ha', 'center')
                text_kwargs.setdefault('va', 'bottom')
                text_kwargs.setdefault('fontsize', 10)
                # 稍微偏移标签，避免与箭头重叠
                text_offset_mag = mag * 1.1
                _target_ax.text(ang_rad, text_offset_mag, labels[i], **text_kwargs)
            
            # 为图例创建代理艺术家
            legend_handles.append(plt.Line2D([0], [0], color=color, lw=2, label=label))

        # 设置极径（幅值）范围
        max_mag = max(magnitudes) if magnitudes else 1
        _target_ax.set_rlim(0, max_mag * 1.2) # 留出一些空间

        # 设置角度网格线（例如每30度）
        _target_ax.set_thetagrids(np.arange(0, 360, 30))
        
        # 设置径向刻度标签
        _target_ax.set_rticks(np.linspace(0, max_mag, 3)) # 3个径向刻度

        _target_ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.05, 1)) # 将图例放在外面

        return self

# paperplot/mixins/analysis_plots.py

from typing import Optional, Union, List
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class DataAnalysisPlotsMixin:
    """
    包含数据分析相关绘图方法的 Mixin 类。
    """
    def _bin_data(self, data: pd.DataFrame, x: str, y: str, bins: Union[int, list] = 10, 
                  agg_func: str = 'mean', error_func: Optional[str] = 'std') -> pd.DataFrame:
        """
        [私有] 将数据按X轴分箱，并计算每个箱内Y值的聚合统计量和误差。
        """
        data_plot = data.copy()
        data_plot['bin'] = pd.cut(data_plot[x], bins=bins)
        
        grouped = data_plot.groupby('bin', observed=False)[y]
        y_agg = grouped.agg(agg_func)
        
        bin_centers = [interval.mid for interval in y_agg.index]

        result_df = pd.DataFrame({
            'bin_center': bin_centers,
            'y_agg': y_agg.values
        })

        if error_func:
            y_error = grouped.agg(error_func)
            result_df['y_error'] = y_error.values
            
        return result_df.dropna()

    def add_binned_plot(self, data: pd.DataFrame, x: str, y: str, 
                        bins: Union[int, list] = 10,
                        agg_func: str = 'mean', 
                        error_func: Optional[str] = 'std',
                        plot_type: str = 'errorbar',
                        tag: Optional[Union[str, int]] = None, 
                        ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        对数据进行分箱、聚合，并绘制聚合后的结果（如误差条图）。

        Args:
            data (pd.DataFrame): 包含绘图数据的DataFrame。
            x (str): X轴数据的列名。
            y (str): Y轴数据的列名。
            bins (Union[int, list], optional): 分箱的数量或自定义分箱边界。默认为 10。
            agg_func (str, optional): 每个箱内Y值的聚合函数 ('mean', 'median', 'sum'等)。默认为 'mean'。
            error_func (Optional[str], optional): 每个箱内Y值的误差计算函数 ('std', 'sem'等)。
                                                  如果为None，则不计算或绘制误差。默认为 'std'。
            plot_type (str, optional): 聚合后数据的绘图类型。目前支持 'errorbar'。默认为 'errorbar'。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 传递给相应绘图函数 (如 `ax.errorbar`) 的额外参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        binned_df = self._bin_data(data, x, y, bins, agg_func, error_func)
        
        if plot_type == 'errorbar':
            y_error = binned_df['y_error'] if 'y_error' in binned_df.columns else None
            kwargs.setdefault('fmt', 'o-') # 默认样式
            _ax.errorbar(binned_df['bin_center'], binned_df['y_agg'], yerr=y_error, **kwargs)
        else:
            raise ValueError(f"Unsupported plot_type: '{plot_type}'. Currently only 'errorbar' is supported.")
        
        self.data_cache[resolved_tag] = data
        self.last_active_tag = resolved_tag
        return self

    def add_distribution_fit(self, data_series: pd.Series, dist_name: str = 'norm',
                               tag: Optional[Union[str, int]] = None, 
                               ax: Optional[plt.Axes] = None, **kwargs) -> 'Plotter':
        """
        在现有直方图上，拟合数据到指定分布并绘制其概率密度函数 (PDF) 曲线。

        通常在此方法之前，应先调用 `add_hist` 并设置 `density=True`。

        Args:
            data_series (pd.Series): 要拟合的数据序列。
            dist_name (str, optional): 要拟合的分布名称，例如 'norm' (正态分布)。
                                       支持 scipy.stats 中的大多数分布。默认为 'norm'。
            tag (Optional[Union[str, int]], optional): 目标子图的tag。默认为None。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象进行绘图。默认为None。
            **kwargs: 传递给 `ax.plot` 的额外参数。
                      可以设置 `color`, `linestyle`, `label` 等。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)
        
        dist = getattr(stats, dist_name)
        params = dist.fit(data_series)
        
        x_min, x_max = _ax.get_xlim()
        x_plot = np.linspace(x_min, x_max, 1000)
        pdf = dist.pdf(x_plot, *params)
        
        # Dynamically generate legend label
        param_str_parts = [f"{p:.2f}" for p in params]
        
        # For 'norm' distribution, we can provide more descriptive labels
        if dist_name == 'norm' and len(params) == 2:
            label = kwargs.pop('label', f'Fitted {dist_name} (μ={params[0]:.2f}, σ={params[1]:.2f})')
        else:
            label = kwargs.pop('label', f'Fitted {dist_name} ({", ".join(param_str_parts)})')

        _ax.plot(x_plot, pdf, label=label, **kwargs)
        _ax.legend()

        self.data_cache[resolved_tag] = data_series.to_frame()
        self.last_active_tag = resolved_tag
        return self

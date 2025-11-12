# paperplot/mixins/analysis_plots.py

from typing import Optional, Union, List
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class DataAnalysisPlotsMixin:
    """包含数据分析相关绘图方法的 Mixin 类。"""
    def _bin_data(self, data: pd.DataFrame, x: str, y: str, bins: Union[int, list] = 10, 
                  agg_func: str = 'mean', error_func: Optional[str] = 'std') -> pd.DataFrame:
        """[私有] 将数据按X轴分箱，并计算每个箱内Y值的聚合统计量和误差。"""
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

    def add_binned_plot(self, **kwargs) -> 'Plotter':
        """对数据进行分箱、聚合，并绘制聚合后的结果。

        此方法首先将数据沿X轴分箱，然后对每个箱内的Y值进行聚合
        （例如计算均值和标准差），最后将聚合结果以误差条图的形式绘制出来。

        Args:
            data (pd.DataFrame): 包含绘图数据的DataFrame。
            x (str): `data` 中要进行分箱的数值列的列名。
            y (str): `data` 中要进行聚合的数值列的列名。
            bins (int or list, optional): 分箱的数量或自定义的箱体边界。
                默认为 10。
            agg_func (str, optional): 用于聚合Y值的函数名（例如 'mean', 'median'）。
                默认为 'mean'。
            error_func (str, optional): 用于计算误差的函数名（例如 'std', 'sem'）。
                如果为 `None`，则不绘制误差条。默认为 'std'。
            plot_type (str, optional): 最终的绘图类型。目前仅支持 'errorbar'。
                默认为 'errorbar'。
            tag (Optional[Union[str, int]], optional): 用于绘图的子图标签。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `ax.errorbar` 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            # 从 p_kwargs 中获取分箱和绘图逻辑所需的参数
            bins = p_kwargs.pop('bins', 10)
            agg_func = p_kwargs.pop('agg_func', 'mean')
            error_func = p_kwargs.pop('error_func', 'std')
            plot_type = p_kwargs.pop('plot_type', 'errorbar')
            
            # cache_df 包含 x 和 y 列，列名是原始列名
            # 从 data_names 字典中获取原始列名
            x_col_name = data_names['x']
            y_col_name = data_names['y']

            binned_df = self._bin_data(cache_df, x_col_name, y_col_name, bins, agg_func, error_func)
            
            if plot_type == 'errorbar':
                y_error = binned_df['y_error'] if 'y_error' in binned_df.columns else None
                p_kwargs.setdefault('fmt', 'o-') # 默认样式
                ax.errorbar(binned_df['bin_center'], binned_df['y_agg'], yerr=y_error, **p_kwargs)
            else:
                raise ValueError(f"Unsupported plot_type: '{plot_type}'. Currently only 'errorbar' is supported.")
            
            # 此图通常不返回 mappable
            return None

        # _execute_plot 需要 'x' 和 'y' 来正确准备数据和缓存
        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x', 'y'],
            plot_defaults_key=None, # 使用 errorbar 的默认样式
            **kwargs
        )

    def add_distribution_fit(self, **kwargs) -> 'Plotter':
        """在现有直方图上，拟合数据到指定分布并绘制其概率密度函数(PDF)。

        此方法从数据中估计指定概率分布的参数（例如正态分布的均值和
        标准差），然后在图上绘制拟合的PDF曲线。通常在调用 `add_hist`
        之后使用。

        Args:
            x (str or array-like): 要拟合的数据或 `data` 中的列名。
            data (Optional[pd.DataFrame], optional): 包含绘图数据的DataFrame。
            dist_name (str, optional): 要拟合的 `scipy.stats` 中的分布名称。
                默认为 'norm' (正态分布)。
            tag (Optional[Union[str, int]], optional): 目标子图的标签。
                如果为 `None`，则使用最后一次绘图的子图。
            ax (Optional[plt.Axes], optional): 直接提供一个Axes对象用于绘图。
            **kwargs: 其他传递给 `ax.plot` (用于绘制PDF曲线) 的关键字参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。
        """
        def plot_logic(ax, data_map, cache_df, data_names, **p_kwargs):
            data_series = data_map['x']
            dist_name = p_kwargs.pop('dist_name', 'norm')
            
            dist = getattr(stats, dist_name)
            params = dist.fit(data_series)
            
            x_min, x_max = ax.get_xlim()
            x_plot = np.linspace(x_min, x_max, 1000)
            pdf = dist.pdf(x_plot, *params)
            
            # Dynamically generate legend label
            param_str_parts = [f"{p:.2f}" for p in params]
            
            # For 'norm' distribution, we can provide more descriptive labels
            if dist_name == 'norm' and len(params) == 2:
                label = p_kwargs.pop('label', f'Fitted {dist_name} (μ={params[0]:.2f}, σ={params[1]:.2f})')
            else:
                label = p_kwargs.pop('label', f'Fitted {dist_name} ({", ".join(param_str_parts)})')

            ax.plot(x_plot, pdf, label=label, **p_kwargs)
            ax.legend()
            
            return None

        return self._execute_plot(
            plot_func=plot_logic,
            data_keys=['x'],
            plot_defaults_key=None,
            **kwargs
        )
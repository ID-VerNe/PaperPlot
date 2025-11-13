---
id: utils
title: Utils & ColorManager API
sidebar_label: 工具与颜色
---

get_style_path
- 签名：`get_style_path(style_name: str) -> str`
- 说明：返回样式文件的绝对路径；优先查找 `paperplot/styles`，其次作为包资源
 - 示例：
 ```python
 from paperplot import utils
 path = utils.get_style_path('marin_kitagawa')
 ```

list_available_styles
- 签名：`list_available_styles() -> List[str]`
- 说明：列出可用样式名（不含扩展名）
 - 示例：
 ```python
 styles = utils.list_available_styles()
 ```

parse_mosaic_layout
- 签名：`parse_mosaic_layout(layout: List[List[str]]) -> Tuple[Dict, Tuple[int,int>]`
- 说明：解析马赛克布局为区域位置与网格大小；验证矩形性与不重叠
 - 示例：
 ```python
 parsed, (rows, cols) = utils.parse_mosaic_layout([['A','A','B'],['C','C','B']])
 ```

moving_average
- 签名：`moving_average(series: pd.Series, window_size: int) -> pd.Series`
- 说明：中心对齐的滚动平均
 - 示例：
 ```python
 df['avg'] = utils.moving_average(df['value'], window_size=5)
 ```

ColorManager
- 目的：在多子图中保持系列颜色稳定；按系列名分配与缓存颜色
- 方法：`get_color(series_name: str) -> str`
- 行为：
  - 首次请求从当前样式颜色循环分配颜色并缓存
  - 颜色用尽将循环重用
- 用法：在绘图方法中传入 `label='系列名'` 即可触发一致颜色；也可直接取得颜色用于自定义绘制
 - 示例：
 ```python
 from paperplot.utils import ColorManager
 cm = ColorManager()
 color = cm.get_color('Series A')
 ```

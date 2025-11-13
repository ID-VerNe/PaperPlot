# 版本历史

## 0.1.7
- 新增图表 API：分组柱、多折线、堆叠柱、极坐标双轴、极坐标柱、阶梯瀑布、饼、环、嵌套环、K 线。
- 统一绘图工作流：所有新增方法改为 `_execute_plot` 封装，合并默认样式与缓存逻辑。
- 颜色一致性：基于 `label` 的 `ColorManager` 在多子图保持系列颜色稳定。
- 图例合并：`set_legend` 自动聚合主/孪生轴的图例项并去重。
- K 线图修复：自动重算范围，确保蜡烛与影线可见。
- 新增示例：`examples/Chart_Types/chart_types_example.py` 与 `polar_twin_example.py`。
- 文档：新增 `doc/README.md`，完善概述、安装、使用、开发、API 与 FAQ。

## 0.1.6
- 布局增强：嵌套子网格与马赛克解析完善，支持更复杂的图表组合。
- 收尾工具：全局图例与共享坐标的自动对齐优化。

## 0.1.5
- 统计绘图：封装 `violin`、`swarm`、`jointplot`、`pairplot` 等。
- 工具集：`utils` 增加移动平均、学习曲线绘制、统计标注等。


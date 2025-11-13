# 版本历史

## 0.1.10 
- **新功能**:
  - 新增 `add_figure` 方法，允许将外部图像文件作为子图内容，并提供 `fit`, `cover`, `stretch` 等多种填充模式及对齐、内边距和缩放控制。
- **功能增强**:
  - `add_twinx` 和 `add_polar_twin` 的颜色循环逻辑得到增强，能够更好地处理颜色耗尽和回绕，确保主轴和孪生轴之间的颜色区分度。
  - `add_subplot_labels` 和 `add_grouped_labels` 的实现得到改进，使用延迟绘制队列，确保标签位置在最终布局渲染后计算，从而更加准确。
  - `add_heatmap` 的 `cmap` 实现智能化，当用户未指定 `cmap` 时，会自动根据当前样式的主色调创建一个平滑的连续色图。
- **内部重构**:
  - 统一并简化了内部 `_execute_plot` 工作流，使其更加健壮和易于扩展。
  - 完善了 `_prepare_data` 的逻辑，更好地处理 DataFrame 和数组输入的混合情况。
- **文档**:
  - 全面更新了主 `README.md` 和 `doc/README.md`，以反映最新的功能和API。
  - 更新了所有 `doc/api/*.md` 文件，确保 API 文档与当前代码实现一致。

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
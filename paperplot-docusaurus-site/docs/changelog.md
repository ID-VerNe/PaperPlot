# 版本历史

## 0.1.19 (2026.03.30)
- **Features**:
  - 新增高阶 API：`add_dual_axis_line`、`add_bar_labels`、`add_reference_line`、`add_interval_shading`。
  - 新增公开配色控制 API：`set_palette`、`bind_color`、`reset_color_cycle`。
  - 新增显式上下文管理：`on_primary(tag)`、`on_twin(tag)`。
  - 新增领域模板 API：`add_peak_ratio_kinetics`、`add_ros_timebar`、`add_sers_dualpeak_dualaxis`。
- **Fixes**:
  - 统一误差棒参数协议：`add_bar/add_grouped_bar/add_line` 兼容 `err/y_err/yerr/y_errs`，并支持 `err_style`。
  - `add_errorbar_from_raw` 重构为复用统一协议，移除重复的手工 `ax.errorbar` 分支。
  - 修复库级日志副作用：移除 `paperplot/__init__.py` 中的 `logging.basicConfig`。
  - 修复图例合并在同轴多 tag 场景下遗漏 twin 项的问题。
  - metadata 导出按 `axis_id` 去重，并保留 `tags` 列表。
- **Changes**:
  - 错误处理收敛：关键路径移除 `print` 与宽泛吞错，改为显式 warning/异常。
  - 新增示例：`examples/09_Data_Utils/unified_error_protocol_demo.py`。
  - 新增/扩展回归测试，覆盖上述协议与高阶 API。

## 0.1.18 (2026.03.26)
- **维护**:
  - **仓库清理**: 移除了开发过程中的临时文件、生成的图像以及非必要的文档，显著减小了包体积。
  - **构建优化**: 重新打包发布，确保 PyPI 包只包含必要的源码、样式文件和核心资源。

## 0.1.17 (2026.03.25)
- **新特性**:
  - **🔬 光谱与结构分析**: 新增 `SpectroscopyMixin`，支持自动寻峰与标注 (`add_peak_labels`)、化学结构式/图片嵌入 (`add_image_box`) 以及光谱范围标注 (`add_bracket`)，专为物理化学领域设计。
- **示例**:
  - 新增 `examples/08_Domain_Specific/spectroscopy_complex_demo.py` 展示复杂光谱分析图表的绘制。

## 0.1.16 (2026.03.25)
- **修复与增强**:
  - **Twin Axes 逻辑修复**: 彻底解决了双 Y 轴上下文切换时的 "Sticky State" 问题。现在，当用户显式指定不同的 `tag` 时，绘图器会正确退出双轴模式，避免了在非双轴子图上查找不存在的 twin axes 导致的错误。
  - **水平条形图数据修正**: 修复了 `add_bar(orientation='horizontal')` 时，数值型数据被错误地作为分类变量处理（转换为字符串）的问题，确保了水平条形图的数据准确性。
  - **布局引擎保护**: 引入了 `_safe_tight_layout` 机制。当用户手动调用 `set_padding` 设置了边距后，库会智能拦截 `tight_layout` 的自动调用（或发出警告），防止手动布局被静默覆盖。
  - **运行时稳健性**: 修复了 `add_twinx_line` 隐式调用 `add_line` 时导致的 `DuplicateTagError`，以及 `add_errorbar_from_raw` 向底层传递不支持参数（如 `capsize`）导致的 `AttributeError`。
- **验证**:
  - 通过了包含 56 个示例脚本的完整回归测试，确保了所有图表类型的稳定性。

## 0.1.15 (2026.03.25)
- **核心逻辑优化**:
  - **分类轴防御机制**: `add_bar` 现在默认启用 `categorical=True`，强制将数值型坐标转换为字符串。这彻底解决了在复杂马赛克布局下，数值型 X 轴导致柱子“消失”或坐标偏移（如 2020.5）的顽疾。
  - **智能配色引擎**: `ColorManager` (由 `utils` 提供) 得到重大升级。当主题预设的颜色循环耗尽时，它不再简单重复，而是通过 HLS 亮度调整自动生成同色系的新变体。这确保了在绘制拥有 10 个以上系列的复杂图表时，每个系列依然拥有唯一的视觉标识。
- **API 增强与整合**:
  - **统一间距控制**: `set_padding` 方法现在集成了 `wspace` 和 `hspace` 参数。开发者可以在一个链式调用中同时完成边距设置和子图间距微调，无需再在 `set_padding` 和 `set_spacing` 之间切换。
  - **双 Y 轴便捷 API**: 新增 `add_twinx_line` 方法。它封装了创建孪生轴、切换上下文和绘制线条的完整流程，实现了“一键式”双轴对比图绘制。
- **高层统计工具**:
  - **原始数据一键绘图**: 新增 `add_errorbar_from_raw` 方法。支持直接传入包含重复实验的原始 DataFrame，自动计算均值和误差棒（支持 std 或 sem），并支持线图和柱状图两种呈现模式。
- **文档与示例**:
  - 更新了所有 API 文档以反映新增参数。
  - 新增测试用例 `tests/test_categorical_bar.py` 和 `tests/test_color_extension.py` 验证健壮性。

## 0.1.10 
- **新功能**:
  - 新增 `add_figure` 方法，允许将外部图像文件作为子图内容，并提供 `fit`, `cover`, `stretch` 等多种填充模式及对齐、内边距和缩放控制。
- **功能增强**:
  - `add_twinx` 和 `add_polar_twin` 的颜色循环逻辑得到增强，能够更好地处理颜色耗尽和回绕，确保主轴 and 孪生轴之间的颜色区分度。
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

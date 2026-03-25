# paperplot 代码审查报告：逻辑缺陷与实战优化缺位分析

基于 `实战后优化建议/` 提供的总结以及对 `paperplot` 核心源码的深度遍历，本报告旨在指出当前代码中存在的逻辑问题、架构局限性以及尚未落地的核心功能。

---

## 1. 核心逻辑缺陷：数据防御机制缺失 (Categorical Safeguard)
*   **现状分析**：在 `paperplot/mixins/generic/basic.py` 的 `add_bar` 方法中，代码直接将 X 轴数据传递给 `matplotlib`。
*   **逻辑风险**：若用户传入数值型（如 `[2020, 2021, 2022]`）而非字符串，`matplotlib` 会将其视为连续坐标。在复杂马赛克布局下，这会导致柱子宽度计算极小甚至“消失”。
*   **修复目标**：在 `add_bar` 方法中增加 `categorical=True` 参数（默认为 True），启用时强制将 X 轴数据转换为字符串。

## 2. 架构瓶颈：静态颜色循环 (Static Color Cycle)
*   **现状分析**：`paperplot/utils.py` 中的 `ColorManager` 在颜色用尽时，简单地通过 `StopIteration` 重置迭代器。
*   **逻辑风险**：当绘制超过 10 个（或主题预设上限）系列时，第 11 个系列将与第 1 个系列完全重色，导致图表信息维度丢失。
*   **修复目标**：引入“智能配色引擎”，当预设颜色耗尽时，通过算法生成同色系的渐变色或互补色。

## 3. API 碎片化：布局与间距控制 (Unified Spacing)
*   **现状分析**：`set_padding` 与 `set_spacing` 割裂在 `paperplot/mixins/modifiers/layout.py` 中。
*   **逻辑冲突**：两者都会直接调用 `fig.set_layout_engine(None)`。这意味着一旦进行微调，库引以为傲的 `constrained_layout` 自动布局将彻底失效，且无法在一个接口内同时控制边距和子图间距（`hspace`/`wspace`）。
*   **修复目标**：在 `set_padding` 中集成 `hspace` 和 `wspace` 参数，并尝试在不完全禁用布局引擎的情况下应用微调。

## 4. 双 Y 轴深度支持不足 (Twin Axes)
*   **现状分析**：虽然 `set_legend` 实现了基础的图例合并逻辑，但 `add_twinx` 的使用依然繁琐。
*   **逻辑缺陷**：目前的上下文切换机制（`active_target`）要求开发者必须显式切换回主轴。
*   **修复目标**：实现 `add_twinx_line()` 这种“一键式”高级封装，自动关联双轴句柄。

## 5. 高级分析工具链断层 (Built-in Utils)
*   **现状分析**：`StatsPlotsMixin` 仅提供了基础封装，缺乏直接从原始数据绘图的高层接口。
*   **修复目标**：新增 `add_errorbar_from_raw` 方法，支持传入重复实验的原始列表，自动计算均值和误差棒。

---

## 总结
当前的 `paperplot` 已经具备了优秀的架构基础，但在**数据健壮性**和**自动化审美**上仍有提升空间。接下来的修复工作将优先围绕上述五个核心维度展开。

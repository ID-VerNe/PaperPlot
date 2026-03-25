# paperplot 优化建议：走向“完美”的学术绘图之路

基于本次 JCIS 项目的深度实战，我建议 `paperplot` 在未来的版本迭代中，可以从以下几个维度进行核心功能的增强。

## 1. 引入自适应动态配色引擎 (Smart Palette)
*   **功能需求**：当绘图系列（Label 数）超过当前主题预设的 `axes.prop_cycle` 长度时，库应能自动通过算法生成同色系的渐变色或互补色，而非简单地重复。
*   **API 建议**：增加 `plotter.extend_palette(n)` 或在 `add_bar`/`add_line` 中提供 `palette='vibrant'` 等参数，内置更多 10 色以上的标准学术调色板。

## 2. 打造智能排版防冲突系统 (Intelligent Layout)
*   **功能需求**：`set_suptitle` 应能智能感知 `fig.legend` 的位置。如果两者都设置在 `upper center`，库应自动调整 `subplots_adjust(top=...)`，为这一对“邻居”预留足够的物理空间。
*   **API 建议**：提供一个 `plotter.standardize_margins()` 方法，根据当前的标题、图例和轴标签的字体大小，自动计算并应用最舒适的边距。

## 3. 统一并增强间距控制接口 (Unified Spacing)
*   **功能需求**：在 `set_padding` 中增加 `hspace` 和 `wspace` 参数的支持，允许在一个方法内完成所有边距和子图间距的设定。
*   **解决痛点**：通过这种方式，可以规避直接调用 `fig.subplots_adjust` 时产生的兼容性警告。

## 4. 深度优化双 Y 轴 (Twin Axes) 的支持
*   **功能需求**：目前的双 Y 轴图例合并过于复杂。建议实现 `plotter.add_twinx_line()`，它不仅能绘制第二条线，还能自动将该线的 `handle` 与主轴关联。
*   **终极目标**：调用 `plotter.set_legend()` 时，应能一键合并左右两个轴的所有图例信息。

## 5. 数据类型防御机制 (Categorical Safeguard)
*   **功能需求**：在 `add_bar` 方法中增加一个显式的 `categorical=True` 参数（默认为 True）。
*   **预期行为**：如果启用，无论数据源是 int 还是 float，库内部都应将其强转为 string，从而确保在 X 轴上呈现等宽、等距的柱状图，彻底解决“柱子消失”的玄学问题。

## 6. 内置常用的数据处理“小挂件” (Built-in Utils)
*   **功能需求**：在绘图前经常需要求均值、标准差或归一化。
*   **API 建议**：提供如 `plotter.add_errorbar_from_raw(data_list)` 这样的高层级方法，让开发者只需传入重复实验的原始列表，库内部自动完成平均值柱子和误差棒的绘制。

---
**展望**：如果上述功能得以实现，`paperplot` 将从一个“好用的工具”进化为一个“会思考的绘图助手”，真正让研究者实现“零排版负担”的创作体验。
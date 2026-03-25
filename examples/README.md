# PaperPlot Examples (示例集)

欢迎来到 PaperPlot 示例库！这个目录包含了 PaperPlot 的各种功能演示，帮助您快速上手并掌握高级用法。

## 📚 目录结构

示例按功能类别组织，建议按以下顺序学习：

### 1️⃣ [01_Basic_Usage](./01_Basic_Usage/) - 基础用法
开始学习的最佳起点，涵盖核心概念和基本操作。
- 简单图表创建
- 多子图网格
- 错误处理

### 2️⃣ [02_Chart_Types](./02_Chart_Types/) - 图表类型
探索 PaperPlot 支持的各种图表类型。
- 柱状图（分组、堆叠）
- 折线图和多线图
- 饼图和环形图
- 热图
- 统计图表（小提琴图、箱线图）
- 瀑布图、K线图
- 极坐标图
- 回归图

### 3️⃣ [03_Layout_Management](./03_Layout_Management/) - 布局管理
学习如何创建复杂的子图布局。
- 简单网格布局
- 马赛克布局
- 跨行/跨列布局
- 嵌套布局
- 综合展示
- 手动布局控制

### 4️⃣ [04_Twin_Axes](./04_Twin_Axes/) - 孪生轴
掌握双Y轴图表的创建和定制。
- 基础孪生轴
- 颜色循环管理
- 极坐标孪生轴

### 5️⃣ [05_Styling_and_Themes](./05_Styling_and_Themes/) - 样式和主题
定制图表外观，打造专业级可视化。
- 主题画廊
- 自定义主题
- 全局样式控制
- Cleanup 函数
- 数据处理和美化

### 6️⃣ [06_Annotations](./06_Annotations/) - 注释和标注
为图表添加说明性元素，提高可读性。
- **文本和标签**：图形级文本、子图自动/自定义/分组/嵌套标注
- **形状和区域**：高亮区域、形状和框、缩放插图
- **统计注释**：统计检验标注

### 7️⃣ [07_Images_and_Composition](./07_Images_and_Composition/) - 图像和组合
创建包含图像的复合图形。
- 复合图形
- 嵌入图像
- 图像对齐

### 8️⃣ [08_Domain_Specific](./08_Domain_Specific/) - 领域特定图表
针对特定领域的专用图表类型。
- 3D 图表
- 分岔图
- 浓度图
- 学习曲线
- 相量图
- 功率时间序列

### 9️⃣ [09_Data_Utils](./09_Data_Utils/) - 数据工具
数据处理和分析辅助功能。
- 数据分析工具
- 实用函数

### 🔟 [10_Metadata_Export](./10_Metadata_Export/) - 元数据导出
导出图表布局元数据，支持 GUI 开发和交互式可视化。
- `get_layout_metadata()` 方法使用
- 像素坐标到数据坐标转换
- 支持所有布局类型（Grid / Mosaic / Nested）
- JSON 格式导出

## 🚀 快速开始

### 运行单个示例

```bash
# 进入 examples 目录
cd examples

# 运行任意示例，例如：
python 01_Basic_Usage/error_handling.py
python 02_Chart_Types/bar_charts.py
python 06_Annotations/text_and_labels/subplot_labels_auto.py
```

### 运行所有示例

推荐使用根目录下的 `run_all_examples.py` 脚本，它支持并行执行并能正确处理环境配置：

```bash
# 在项目根目录下运行
python run_all_examples.py
```

或者使用以下命令（不推荐，可能存在编码或路径问题）：

```bash
# Windows PowerShell
Get-ChildItem -Recurse -Filter "*.py" | ForEach-Object { python $_.FullName }

# Linux/Mac
find . -name "*.py" -type f ! -name "__*" -exec python {} \;
```

## 📖 学习路径建议

**初学者路径**：
1. `01_Basic_Usage/error_handling.py` - 了解基础结构
2. `02_Chart_Types/bar_charts.py` - 学习创建简单图表
3. `03_Layout_Management/` - 掌握多子图布局
4. `05_Styling_and_Themes/theme_gallery.py` - 探索样式选项

**进阶用户路径**：
1. `04_Twin_Axes/` - 创建双Y轴图表
2. `06_Annotations/` - 添加专业级标注
3. `03_Layout_Management/comprehensive_showcase.py` - 学习复杂布局
4. `07_Images_and_Composition/` - 创建复合图形

**特定需求**：
- **科学出版论文** → `06_Annotations/text_and_labels/`, `05_Styling_and_Themes/theme_gallery.py`
- **数据分析报告** → `02_Chart_Types/statistical_plots.py`, `04_Twin_Axes/`
- **金融图表** → `02_Chart_Types/candlestick.py`, `02_Chart_Types/waterfall.py`
- **机器学习** → `08_Domain_Specific/learning_curve.py`

## 💡 提示和技巧

- **链式调用**：大多数示例都展示了方法链式调用的用法，可以让代码更简洁
- **错误处理**：查看 `error_handling.py` 了解如何捕获和处理 PaperPlot 特定的异常
- **性能优化**：对于大型数据集，参考 `09_Data_Utils/` 中的数据处理技巧
- **自定义扩展**：通过 `get_ax()` 方法可以访问底层 matplotlib 对象进行高级定制

## 🔗 相关资源

- **主文档**：[../README.md](../README.md)
- **API 参考**：查看源代码中的 docstrings
- **问题反馈**：GitHub Issues

## 📝 注意事项

- 所有示例都会在当前目录生成 PNG 图像文件
- 示例会自动将项目根目录添加到 Python 路径，确保能正确导入 `paperplot`
- 某些示例需要额外的依赖（如 seaborn），请根据错误提示安装

---

**最后更新**: 2026-03-25  
**示例总数**: 56+  
**建议 PaperPlot 版本**: >= 0.1.16

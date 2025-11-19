# 06_Annotations - 注释和标注

本目录展示如何为图表添加各种注释和标注元素，提高图表的专业性和可读性。

## 目录结构

### 📝 [text_and_labels/](./text_and_labels/) - 文本和标签
子图编号和图形级文本注释。

- `figure_text.py` - 图形级文本（标题、页脚、边注）
- `subplot_labels_auto.py` - 自动子图标注（a, b, c...）
- `subplot_labels_custom.py` - 自定义子图标注（样式、位置、格式）
- `subplot_labels_grouped.py` - 分组标注（逻辑分组）
- `subplot_labels_nested.py` - 嵌套布局标注（层级标注）

### 🎨 [shapes_and_regions/](./shapes_and_regions/) - 形状和区域
图形元素和区域标注。

- `shapes_and_boxes.py` - 图形级注释（线、框、组标签）
- `highlighting.py` - 高亮数据区域
- `zoom_insets.py` - 缩放插图（局部放大）

### 📊 [statistical/](./statistical/) - 统计注释
统计分析相关的标注。

- `statistical_annotation.py` - 统计检验标注（p-value、显著性）

## 使用场景

### 科学论文
- 子图编号：`subplot_labels_auto.py`, `subplot_labels_grouped.py`
- 统计显著性：`statistical_annotation.py`
- 局部放大：`zoom_insets.py`

### 数据报告
- 高亮重点：`highlighting.py`
- 分组说明：`shapes_and_boxes.py`
- 图例和注释：`figure_text.py`

### 演示文稿
- 简洁标注：`subplot_labels_auto.py`
- 区域高亮：`highlighting.py`

## 学习路径

**基础路径**（推荐新手）：
1. `text_and_labels/subplot_labels_auto.py` - 最简单的自动编号
2. `text_and_labels/figure_text.py` - 添加标题和说明
3. `shapes_and_regions/highlighting.py` - 高亮重要区域

**进阶路径**：
1. `text_and_labels/subplot_labels_custom.py` - 自定义标注样式
2. `text_and_labels/subplot_labels_grouped.py` - 逻辑分组标注
3. `shapes_and_regions/shapes_and_boxes.py` -  图形级注释组合
4. `shapes_and_regions/zoom_insets.py` - 创建缩放插图

**专业路径**（科研用户）：
1. `text_and_labels/subplot_labels_nested.py` - 处理复杂嵌套布局
2. `statistical/statistical_annotation.py` - 添加统计检验结果
3. 结合多种注释方法创建出版级图表

## 快速参考

### 子图标注样式

| 标注风格 | 示例 | 代码参数 |
|---------|------|---------|
| 小写字母 | a, b, c | `label_style='alpha'` |
| 大写字母 | A, B, C | `label_style='alpha', case='upper'` |
| 数字 | 1, 2, 3 | `label_style='numeric'` |
| 罗马数字 | i, ii, iii | `label_style='roman'` |

### 常用位置

| 位置代码 | 说明 |
|---------|------|
| `(0, 1)` | 左上角（默认） |
| `(1, 1)` | 右上角 |
| `(0, 0)` | 左下角 |
| `top_left`, `top_center` 等 | 预定义位置（分组标签） |

## API快速索引

### 子图标注
```python
# 自动标注所有子图
plotter.add_subplot_labels()

# 自定义样式
plotter.add_subplot_labels(
    label_style='alpha',  # 或 'numeric', 'roman'
    case='upper',         # 或 'lower'
    template='({label})', # 自定义模板
    position=(0, 1),      # 位置
    fontsize=14
)

# 分组标注
plotter.add_grouped_labels(
    groups={'(a)': ['ax00', 'ax01'], '(b)': ['ax10']},
    position='top_left'
)
```

### 图形级文本
```python
# 添加文本到图形
plotter.fig_add_text(x=0.5, y=0.96, text='Title', ha='center')

# 添加框和标签
plotter.fig_add_box(tags=['ax00', 'ax01'])
plotter.fig_add_label(tags='ax00', text='Group A', position='top_center')
```

### 高亮和形状
```python
# 高亮数据区域
plotter.add_highlight_box(
    tag='main_plot',
    x_range=(0.5, 2.5),
    y_range=(0.4, 0.8),
    facecolor='orange',
    alpha=0.3
)
```

### 统计标注
```python
# 添加统计检验
plotter.add_pairwise_tests(
    tag='box',
    x='group',
    y='value',
    comparisons=[('A', 'B'), ('B', 'C')],
    test='t-test_ind'
)
```

## 组合示例

### 典型科研图表标注流程
```python
# 1. 创建图表并绘制数据
plotter = pp.Plotter(layout=(2, 2))
# ... 添加各种图表 ...

# 2. 添加子图标注
plotter.add_subplot_labels(label_style='alpha', case='upper')

# 3. 添加分组说明
plotter.add_grouped_labels(
    groups={'实验组': ['ax00', 'ax01'], '对照组': ['ax10', 'ax11']}
)

# 4. 高亮重要区域
plotter.add_highlight_box(tag='ax00', x_range=(2, 5), ...)

# 5. 添加统计检验（如果需要）
plotter.add_pairwise_tests(...)

# 6. 添加图形级标题和说明
plotter.fig_add_text(0.5, 0.96, '实验结果总览', ha='center', fontsize=16)
```

## 下一步

- 定制样式：[../05_Styling_and_Themes/](../05_Styling_and_Themes/)
- 保存高质量图片：查看主 README
- 结合复杂布局：[../03_Layout_Management/](../03_Layout_Management/)

# 元数据导出 (Metadata Export)

PaperPlot 提供了强大的元数据导出功能，用于支持可视化交互和 GUI 工具开发。

## get_layout_metadata()

`get_layout_metadata()` 方法可以导出图表的完整布局信息，包括：

- 图片尺寸（像素）
- 每个子图的位置（bbox）
- 数据坐标范围（xlim/ylim）
- 坐标系类型（linear/log）

这些元数据是实现 **PaperPlot Studio** 等可视化工具的基础，支持：
- 交互式标注
- 坐标系转换
- 所见即所得编辑

## 使用示例

```python
import paperplot as pp
import pandas as pd
import numpy as np
import json

# 创建图表
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100))
})

plotter = pp.Plotter(layout=(1, 1), figsize=(8, 6))
plotter.add_line(data=df, x='x', y='y', tag='ax00')

# 获取元数据
metadata = plotter.get_layout_metadata()

print(f"Image size: {metadata['width']} x {metadata['height']}")
print(f"Subplot bbox: {metadata['subplots']['ax00']['bbox']}")
print(f"Data range: x={metadata['subplots']['ax00']['xlim']}, "
      f"y={metadata['subplots']['ax00']['ylim']}")

# 导出为 JSON
with open('metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

## 元数据结构

```json
{
  "width": 2400,
  "height": 1800,
  "subplots": {
    "ax00": {
      "bbox": [217.58, 150.33, 2387.50, 1713.50],
      "xlim": [-0.5, 10.5],
      "ylim": [-1.099, 1.100],
      "x_scale": "linear",
      "y_scale": "linear"
    }
  }
}
```

### 字段说明

- **width/height**: 图片的像素尺寸
- **subplots**: 所有子图的元数据字典
  - **bbox**: `[left, bottom, right, top]` 像素坐标（原点在左下角）
  - **xlim/ylim**: 数据坐标范围 `[min, max]`
  - **x_scale/y_scale**: 坐标系类型（`linear`, `log`, `symlog` 等）

## 坐标转换示例

利用元数据可以实现像素坐标到数据坐标的转换：

```python
# 用户点击位置（像素）
click_x, click_y = 1200, 900

# 获取子图元数据
subplot = metadata['subplots']['ax00']
bbox = subplot['bbox']
xlim = subplot['xlim']
ylim = subplot['ylim']

# 计算相对位置
ratio_x = (click_x - bbox[0]) / (bbox[2] - bbox[0])
ratio_y = ((metadata['height'] - click_y) - bbox[1]) / (bbox[3] - bbox[1])

# 转换为数据坐标
data_x = xlim[0] + ratio_x * (xlim[1] - xlim[0])
data_y = ylim[0] + ratio_y * (ylim[1] - ylim[0])

print(f"Click at pixel ({click_x}, {click_y})")
print(f"Corresponds to data ({data_x:.2f}, {data_y:.2f})")
```

## 支持的布局类型

`get_layout_metadata()` 支持所有布局类型：

- **Grid 布局**: `layout=(2, 2)`
- **Mosaic 布局**: `layout=[['A', 'A'], ['B', 'C']]`
- **嵌套布局**: 使用字典的声明式布局

嵌套布局示例：
```python
nested_layout = {
    'main': [['main_plot', 'side_group']],
    'subgrids': {
        'side_group': {
            'layout': [['top', 'top'], ['bottom_left', 'bottom_right']],
            'hspace': 0.3
        }
    }
}

plotter = pp.Plotter(layout=nested_layout)
# 标签使用层级结构: 'side_group.top', 'side_group.bottom_left'
```

## 应用场景

### 1. PaperPlot Studio GUI

元数据导出是 PaperPlot Studio 的核心功能，支持：
- 在图片上直接标注
- 像素点击 → 数据坐标转换
- 自动生成可复现的 Python 代码

### 2. 自定义交互工具

利用元数据可以开发自定义的可视化交互工具：
- Jupyter Widget 扩展
- Web 应用集成
- 自动化测试和验证

## 注意事项

1. **必须在渲染后调用**: `get_layout_metadata()` 会自动调用 `fig.canvas.draw()`
2. **坐标系原点**: bbox 坐标原点在左下角（符合 Matplotlib 规范）
3. **孪生轴支持**: 孪生轴的元数据以 `{tag}_twin` 为键导出

## 完整示例

完整的演示脚本请参考：
- [examples/10_Metadata_Export/metadata_demo.py](../../examples/10_Metadata_Export/metadata_demo.py)

# 04_Twin_Axes - 孪生轴（双Y轴）

本目录展示如何创建和定制双Y轴图表，实现在同一个子图中绘制具有不同数值范围的两组数据。

## 文件列表

- **`basic_twin_axes.py`** - 孪生轴基础
  - 创建双Y轴图表
  - 链式调用切换主轴/孪生轴
  - 自动颜色同步
  - 合并图例
  
- **`twin_axes_color_cycle.py`** - 颜色循环管理
  - 孪生轴的颜色循环继承和回绕
  - 多图形元素的颜色协调
  
- **`polar_twin_axes.py`** - 极坐标孪生轴
  - 在极坐标系统中使用双轴
  - 极坐标特定的孪生轴功能

## 核心概念

### 什么是孪生轴？

孪生轴允许在同一个subplot中显示两个不同的Y轴，通常用于：
- 展示具有不同量纲的数据（如温度和降雨量）
- 对比不同数值范围的数据系列
- 节省布局空间，同时保持数据的可读性

### 关键API

```python
plotter = pp.Plotter(layout=(1, 1))

# 在主轴上绘图
plotter.add_line(data=df_temp, x='time', y='temperature', label='Temperature')
       .set_ylabel('Temperature (°C)')
       
# 创建孪生轴（从这里开始命令作用于孪生轴）
       .add_twinx()
       
# 在孪生轴上绘图
       .add_bar(data=df_rain, x='time', y='rainfall', label='Rainfall')
       .set_ylabel('Rainfall (mm)')
       
# 切回主轴
       .target_primary()
       
# 合并图例
       .set_legend()
```

## 学习顺序

1. **`basic_twin_axes.py`** - 从这里开始！
   - 理解孪生轴的创建和使用
   - 学习链式调用在双轴间切换
   
2. **`twin_axes_color_cycle.py`** - 理解颜色管理
   - 孪生轴如何继承主轴的颜色循环
   - 如何自定义双轴的颜色
   
3. **`polar_twin_axes.py`** - 探索高级用法
   - 在非标准坐标系中使用孪生轴

## 常见应用场景

### 气象数据
温度（曲线）+ 降雨量（柱状图）
```python
# 温度在主轴，降雨在孪生轴
plotter.add_line(..., label='Temperature').set_ylabel('Temperature (°C)')
       .add_twinx()
       .add_bar(..., label='Rainfall').set_ylabel('Rainfall (mm)')
```

### 金融数据
股价（曲线）+ 成交量（柱状图）

### 实验数据
浓度变化（曲线）+ pH值（散点图）

## 注意事项

⚠️ **Y轴标签对齐**：使用 `cleanup(align_labels=True)` 可以对齐两个Y轴的标签

⚠️ **颜色区分**：建议为主轴和孪生轴使用不同的颜色，或手动设置Y轴标签颜色与对应数据一致

⚠️ **图例顺序**：`set_legend()` 会自动合并主轴和孪生轴的图例项

⚠️ **避免混淆**：双Y轴可能造成读者误解，确保清晰标注单位和数据含义

## 下一步

- 结合布局：[../03_Layout_Management/](../03_Layout_Management/)
- 添加辅助线和标注：[../06_Annotations/](../06_Annotations/)
- 定制Y轴样式：[../05_Styling_and_Themes/](../05_Styling_and_Themes/)

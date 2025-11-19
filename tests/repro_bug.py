import numpy as np
import pandas as pd
from paperplot import Plotter

# 准备用于统计检验的数据
df_stats = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'value': [10, 12, 11, 20, 22, 21, 15, 14, 16]
})

# 1. 初始化一个 1x1 的网格
p = Plotter(layout=(1, 1), figsize=(6, 5))

# 2. 绘制箱线图
p.add_box(data=df_stats, x='category', y='value')

# 3. 尝试添加统计检验（这步应该会失败）
try:
    p.add_stat_test(
        x='category',
        y='value',
        group1='A',
        group2='B',
        test='t-test_ind'
    )
    p.save('bug2_repro_before_fix.png')
    print("图像已保存，但这不应该发生。")
except ValueError as e:
    print("成功复现 Bug！")
    print(f"捕获到的错误信息: {e}")
import pytest
import matplotlib.pyplot as plt
from paperplot.utils import ColorManager

def test_color_manager_extension():
    """验证 ColorManager 是否能在预设颜色耗尽后生成新颜色。"""
    cm = ColorManager()
    
    # 获取默认颜色数量
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    n_default = len(default_colors)
    
    colors = []
    for i in range(n_default + 10):
        colors.append(cm.get_color(f"series_{i}"))
        
    # 检查是否有重复（在扩展阶段）
    # 如果简单循环，第 n_default 个会和第 0 个相同
    assert colors[0] != colors[n_default], "Color repeated instead of being extended!"
    
    # 检查总数
    assert len(set(colors)) == n_default + 10

if __name__ == "__main__":
    test_color_manager_extension()

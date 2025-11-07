# paperplot/utils.py

import os

def get_style_path(style_name: str) -> str:
    """
    获取预定义样式文件的绝对路径。
    
    Args:
        style_name (str): 样式名称 (例如 'publication').

    Returns:
        str: .mplstyle 文件的路径。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(current_dir, 'styles', f'{style_name}.mplstyle')
    if not os.path.exists(style_path):
        # 如果在当前目录的styles子目录找不到，尝试作为包资源查找
        try:
            import importlib.resources
            with importlib.resources.path('paperplot.styles', f'{style_name}.mplstyle') as path:
                return str(path)
        except (ImportError, FileNotFoundError):
            raise FileNotFoundError(f"Style '{style_name}' not found as a file or package resource.")
    return style_path

def add_stat_annotation(ax, x1, x2, y, p_value):
    """
    在给定的 Axes 对象上绘制统计显著性标记。
    (此函数逻辑可根据需要实现)
    """
    p_text = ''
    if p_value < 0.001:
        p_text = '***'
    elif p_value < 0.01:
        p_text = '**'
    elif p_value < 0.05:
        p_text = '*'
    
    if p_text:
        ax.plot([x1, x1, x2, x2], [y, y + 0.1, y + 0.1, y], lw=1.5, c='black')
        ax.text((x1 + x2) * 0.5, y + 0.1, p_text, ha='center', va='bottom', color='black')

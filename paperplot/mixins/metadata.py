from typing import Dict, Union

class MetadataMixin:
    """为 PaperPlot Studio 提供布局元数据导出功能。
    
    此 Mixin 提供 `get_layout_metadata()` 方法，返回图表的像素级布局信息，
    用于前端实现交互式标注和坐标转换。
    """
    
    def get_layout_metadata(self) -> Dict:
        """获取布局元数据用于前端交互。
        
        必须在 save() 或 canvas.draw() 后调用，以确保布局已计算。
        
        Returns:
            dict: 包含以下结构的元数据:
                - width (int): 图片宽度（像素）
                - height (int): 图片高度（像素）
                - subplots (dict): 每个子图的位置和数据范围信息
                    - bbox (list): [left, bottom, right, top] 像素坐标
                    - xlim (list): [xmin, xmax] 数据范围
                    - ylim (list): [ymin, ymax] 数据范围
                    - x_scale (str): 'linear', 'log', 'symlog' 等
                    - y_scale (str): 'linear', 'log', 'symlog' 等
        
        Example:
            >>> plotter = Plotter(layout=(1, 1))
            >>> plotter.add_line(x=[1, 2, 3], y=[4, 5, 6])
            >>> plotter.fig.canvas.draw()  # 强制渲染
            >>> metadata = plotter.get_layout_metadata()
            >>> print(metadata['width'], metadata['height'])
            800 600
            >>> print(metadata['subplots']['ax00']['bbox'])
            [80.0, 52.8, 576.0, 422.4]
        """
        # 强制渲染以计算布局
        self.fig.canvas.draw()
        
        # 获取画布尺寸
        width, height = self.fig.canvas.get_width_height()
        
        metadata = {
            "width": int(width),
            "height": int(height),
            "subplots": {}
        }
        
        # 遍历所有主轴
        for tag, ax in self.tag_to_ax.items():
            # 获取子图在画布上的像素位置 (Bbox)
            # Matplotlib 的 bbox 原点在左下角
            bbox = ax.get_window_extent()
            
            # 获取当前的数据范围
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            
            metadata["subplots"][str(tag)] = {
                # 转换为 [left, bottom, right, top] 格式
                "bbox": [
                    float(bbox.x0),
                    float(bbox.y0),
                    float(bbox.x1),
                    float(bbox.y1)
                ],
                "xlim": [float(xlim[0]), float(xlim[1])],
                "ylim": [float(ylim[0]), float(ylim[1])],
                "x_scale": ax.get_xscale(),
                "y_scale": ax.get_yscale()
            }
        
        # 如果有孪生轴，也导出其元数据
        if hasattr(self, 'twin_axes'):
            for tag, twin_ax in self.twin_axes.items():
                bbox = twin_ax.get_window_extent()
                xlim = twin_ax.get_xlim()
                ylim = twin_ax.get_ylim()
                
                twin_tag = f"{tag}_twin"
                metadata["subplots"][twin_tag] = {
                    "bbox": [
                        float(bbox.x0),
                        float(bbox.y0),
                        float(bbox.x1),
                        float(bbox.y1)
                    ],
                    "xlim": [float(xlim[0]), float(xlim[1])],
                    "ylim": [float(ylim[0]), float(ylim[1])],
                    "x_scale": twin_ax.get_xscale(),
                    "y_scale": twin_ax.get_yscale()
                }
        
        return metadata

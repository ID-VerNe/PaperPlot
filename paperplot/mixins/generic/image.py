from typing import Optional, Union
import matplotlib.image as mpimg

class ImagePlotsMixin:
    def add_figure(self, image_path: str, fit_mode: str = 'fit', align: str = 'center', padding: float = 0.0, zoom: float = 0.0, **kwargs) -> 'Plotter':
        """将一个图像文件作为子图的全部内容进行绘制。

        此方法用于在子图中展示图片，支持多种适应模式和对齐方式。

        Args:
            image_path (str): 图像文件的路径。
            fit_mode (str, optional): 图像适应模式。
                - 'fit': 保持纵横比，完整显示图像 (可能会留白)。
                - 'cover': 保持纵横比，填满子图 (可能会裁剪)。
                - 'stretch': 拉伸图像以填满子图 (不保持纵横比)。
                默认为 'fit'。
            align (str, optional): 当 `fit_mode='fit'` 且有留白时的对齐方式。
                可选值: 'center', 'top_left', 'top_right', 'bottom_left', 'bottom_right'。
                默认为 'center'。
            padding (float, optional): 图像周围的内边距 (0-0.5)。默认为 0.0。
            zoom (float, optional): 缩放比例 (0-0.5)。正值表示向中心缩小 (zoom in)，实际上裁剪了边缘。默认为 0.0。
            **kwargs:
                核心参数:
                - tag (str or int, optional): 指定绘图的目标子图标签。
                
                样式参数:
                - ... 其他传递给 `ax.imshow` 的参数。

        Returns:
            Plotter: 返回Plotter实例以支持链式调用。

        Raises:
            ValueError: 如果参数值无效或文件未找到。
        """
        _ax, resolved_tag = self._resolve_ax_and_tag(kwargs.pop('tag', None))

        draw_ax = _ax

        if padding > 0:
            if not (0.0 <= padding < 0.5):
                raise ValueError(f"Padding must be between 0.0 and 0.5 (exclusive of 0.5), but got {padding}.")
            draw_ax = _ax.inset_axes([padding, padding, 1 - 2 * padding, 1 - 2 * padding])
            _ax.axis('off')

        if fit_mode not in ['stretch', 'fit', 'cover']:
            raise ValueError(f"Invalid fit_mode '{fit_mode}'. Available modes are 'stretch', 'fit', 'cover'.")
        if align not in ['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']:
            raise ValueError(f"Invalid align '{align}'. Available aligns are 'center', 'top_left', 'top_right', 'bottom_left', 'bottom_right'.")
        if not (0.0 <= zoom < 0.5):
            raise ValueError(f"Zoom must be between 0.0 and 0.5 (exclusive of 0.5), but got {zoom}.")

        try:
            img = mpimg.imread(image_path)
        except FileNotFoundError:
            raise ValueError(f"Image file '{image_path}' not found.")

        draw_ax.axis('off')
        draw_ax.set_xticks([])
        draw_ax.set_yticks([])

        imshow_kwargs = kwargs.copy()
        imshow_kwargs.setdefault('aspect', 'auto')

        draw_ax.imshow(img, **imshow_kwargs)

        img_height, img_width = img.shape[0], img.shape[1]
        img_aspect = img_width / img_height
        
        self.fig.canvas.draw()
        bbox = draw_ax.get_window_extent()
        subplot_aspect = bbox.width / bbox.height if bbox.height > 0 else 1

        draw_ax.set_aspect('auto') 

        xlim, ylim = (0, img_width), (img_height, 0)

        if fit_mode == 'stretch':
            pass

        else:
            if fit_mode == 'fit':
                if img_aspect > subplot_aspect:
                    view_w = img_width
                    view_h = view_w / subplot_aspect
                    pad_y = (view_h - img_height)
                    
                    if align == 'center':
                        ylim = (img_height + pad_y / 2, -pad_y / 2)
                    elif align == 'top_left' or align == 'top_right':
                        ylim = (view_h, 0)
                    elif align == 'bottom_left' or align == 'bottom_right':
                        ylim = (img_height, img_height - view_h)
                    xlim = (0, view_w)

                else:
                    view_h = img_height
                    view_w = view_h * subplot_aspect
                    pad_x = (view_w - img_width)
                    
                    if align == 'center':
                        xlim = (-pad_x / 2, view_w - pad_x / 2)
                    elif align == 'top_left' or align == 'bottom_left':
                        xlim = (0, view_w)
                    elif align == 'top_right' or align == 'bottom_right':
                        xlim = (img_width - view_w, img_width)
                    ylim = (view_h, 0)
            
            elif fit_mode == 'cover':
                if img_aspect > subplot_aspect:
                    view_h = img_height
                    view_w = view_h * subplot_aspect
                    crop_x = (img_width - view_w) / 2
                    xlim, ylim = (crop_x, img_width - crop_x), (img_height, 0)
                else:
                    view_w = img_width
                    view_h = view_w / subplot_aspect
                    crop_y = (img_height - view_h) / 2
                    xlim, ylim = (0, img_width), (img_height - crop_y, crop_y)

        total_w = xlim[1] - xlim[0]
        total_h = ylim[0] - ylim[1]

        xlim = (xlim[0] + total_w * zoom, xlim[1] - total_w * zoom)
        ylim = (ylim[0] - total_h * zoom, ylim[1] + total_h * zoom)

        draw_ax.set_xlim(xlim)
        draw_ax.set_ylim(ylim)

        self.last_active_tag = resolved_tag
        return self

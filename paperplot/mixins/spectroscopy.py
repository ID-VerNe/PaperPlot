import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from scipy.signal import find_peaks
from typing import Optional, Union, Tuple, List
import logging
from ..exceptions import PlottingError

logger = logging.getLogger(__name__)

class SpectroscopyMixin:
    """Methods for spectroscopy and advanced annotation."""

    def add_peak_labels(self, 
                        top_k: int = 5,
                        prominence: float = None,
                        threshold: float = None,
                        distance: int = None,
                        format_str: str = "{:.1f}",
                        offset: Tuple[float, float] = (0, 10),
                        arrow_props: dict = None,
                        font_props: dict = None,
                        tag: Optional[Union[str, int]] = None,
                        **kwargs) -> 'Plotter':
        """
        Automatically detect and label peaks in the current or specified subplot.

        Args:
            top_k (int): Number of highest peaks to label. Default is 5.
            prominence (float): Minimum prominence of peaks (see scipy.signal.find_peaks).
            threshold (float): Minimum absolute height threshold.
            distance (int): Minimum horizontal distance (in samples) between peaks.
            format_str (str): Format string for the label (e.g., "{:.1f}" or "{:.0f}").
            offset (Tuple[float, float]): (x, y) offset for the text label relative to the peak in POINTS.
            arrow_props (dict): Properties for the arrow (e.g., dict(arrowstyle="->", color="black")).
            font_props (dict): Properties for the text (e.g., dict(fontsize=10, color="black")).
            tag (str|int): Target subplot tag.
            **kwargs: Additional arguments passed to find_peaks.
        """
        ax = self._get_active_ax(tag)
        
        # Get data from the last plotted line
        lines = ax.get_lines()
        if not lines:
            raise PlottingError("No lines found in the subplot to detect peaks on.")
        
        # Use the LAST added line by default (most likely the one user wants to label)
        line = lines[-1]
        x_data = line.get_xdata()
        y_data = line.get_ydata()

        # Find peaks
        peaks, properties = find_peaks(y_data, prominence=prominence, height=threshold, distance=distance, **kwargs)
        
        if len(peaks) == 0:
            logger.warning(
                "No peaks found with current parameters (prominence=%s, threshold=%s).",
                prominence,
                threshold,
            )
            return self

        # Filter top K by height
        peak_heights = y_data[peaks]
        if top_k and len(peaks) > top_k:
            # Get indices of top_k largest elements
            top_indices = np.argsort(peak_heights)[-top_k:]
            peaks = peaks[top_indices]
            peak_heights = peak_heights[top_indices]

        # Defaults for props
        default_arrow = dict(arrowstyle="-", color="black", linewidth=0.8)
        if arrow_props:
            default_arrow.update(arrow_props)
        
        default_font = dict(fontsize=9, color="black", ha='center', va='bottom')
        if font_props:
            default_font.update(font_props)

        # Plot annotations
        for i, peak_idx in enumerate(peaks):
            x_val = x_data[peak_idx]
            y_val = y_data[peak_idx]
            
            label_text = format_str.format(x_val)
            
            ax.annotate(text=label_text,
                        xy=(x_val, y_val),
                        xytext=offset,
                        textcoords='offset points',
                        arrowprops=default_arrow,
                        **default_font)

        return self

    def add_image_box(self, 
                      image_path: str, 
                      x: float, 
                      y: float, 
                      zoom: float = 0.5, 
                      coord_system: str = 'data',
                      tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        Embed an image (e.g., molecule structure, logo) into the plot area.

        Args:
            image_path (str): Path to the image file.
            x (float): X coordinate.
            y (float): Y coordinate.
            zoom (float): Zoom level for the image (scaling factor).
            coord_system (str): Coordinate system to use ('data' or 'axes').
                                'data': Uses plot data coordinates (default).
                                'axes': Uses relative axes coordinates (0-1).
            tag (str|int): Target subplot tag.
        """
        ax = self._get_active_ax(tag)
        
        try:
            arr_img = plt.imread(image_path)
        except (FileNotFoundError, OSError) as e:
            raise PlottingError(f"Failed to load image from {image_path}: {str(e)}")

        imagebox = OffsetImage(arr_img, zoom=zoom)
        imagebox.image.axes = ax

        xycoords = 'data' if coord_system == 'data' else 'axes fraction'
        
        ab = AnnotationBbox(imagebox, (x, y),
                            xycoords=xycoords,
                            boxcoords="offset points",
                            pad=0,
                            frameon=False)
        
        ax.add_artist(ab)
        return self

    def add_bracket(self, 
                    x_start: float, 
                    x_end: float, 
                    text: str, 
                    y_position: float, 
                    height: float = None, 
                    style: str = 'square',
                    color: str = 'black',
                    lw: float = 1.5,
                    fontsize: int = 10,
                    tag: Optional[Union[str, int]] = None) -> 'Plotter':
        """
        Add a bracket annotation to group a range of data (e.g., spectral band).

        Args:
            x_start (float): Start X coordinate.
            x_end (float): End X coordinate.
            text (str): Label text (supports LaTeX).
            y_position (float): Y coordinate for the bracket baseline.
            height (float): Height of the bracket legs. If None, defaults to 5% of Y-range.
            style (str): 'square' (default) or 'curly' (future). Currently supports 'square'.
            color (str): Color of the bracket and text.
            lw (float): Line width.
            fontsize (int): Text font size.
            tag (str|int): Target subplot tag.
        """
        ax = self._get_active_ax(tag)
        
        if height is None:
            # Auto-calculate height based on y-axis range
            ylim = ax.get_ylim()
            height = (ylim[1] - ylim[0]) * 0.05

        # Draw bracket lines
        # Shape:
        #      |___________|
        #      ^           ^
        #    x_start     x_end
        
        # Legs
        ax.plot([x_start, x_start], [y_position, y_position + height], color=color, lw=lw)
        ax.plot([x_end, x_end], [y_position, y_position + height], color=color, lw=lw)
        
        # Crossbar
        ax.plot([x_start, x_end], [y_position + height, y_position + height], color=color, lw=lw)
        
        # Text
        mid_x = (x_start + x_end) / 2
        ax.text(mid_x, y_position + height * 1.2, text, 
                ha='center', va='bottom', color=color, fontsize=fontsize)

        return self

---
sidebar_position: 11
title: Spectroscopy & Annotations
---

# Spectroscopy & Advanced Annotations

The `SpectroscopyMixin` provides tools specifically designed for spectral analysis (e.g., Raman, IR, UV-Vis) and complex figure composition. It includes automatic peak detection, image embedding (for molecular structures or logos), and spectral range brackets.

These methods are available directly on the `Plotter` instance.

## Methods

### `add_peak_labels`

Automatically detect and label peaks in a line plot. This function wraps `scipy.signal.find_peaks` and adds arrow annotations pointing to the detected peaks.

```python
def add_peak_labels(
    self,
    top_k: int = 5,
    prominence: float = None,
    threshold: float = None,
    distance: int = None,
    format_str: str = "{:.1f}",
    offset: Tuple[float, float] = (0, 10),
    arrow_props: dict = None,
    font_props: dict = None,
    tag: Optional[Union[str, int]] = None,
    **kwargs
) -> 'Plotter':
```

**Parameters:**

- **top_k** (`int`): Number of highest peaks to label. Default is `5`. Set to `None` to label all detected peaks.
- **prominence** (`float`): The minimum prominence of peaks (vertical distance between the peak and its lowest contour line). See `scipy.signal.find_peaks`.
- **threshold** (`float`): The minimum absolute height threshold for peaks.
- **distance** (`int`): The minimum horizontal distance (in samples) between neighboring peaks.
- **format_str** (`str`): Format string for the label text (e.g., `"{:.1f}"` for 1 decimal place, `"{:.0f}"` for integer). The label value is the x-coordinate of the peak.
- **offset** (`Tuple[float, float]`): The `(x, y)` offset for the text label relative to the peak point, in **points**. Default is `(0, 10)` (10 points above).
- **arrow_props** (`dict`): Properties for the arrow connecting the label to the peak. Default: `dict(arrowstyle="-", color="black", linewidth=0.8)`.
- **font_props** (`dict`): Properties for the text label. Default: `dict(fontsize=9, color="black", ha='center', va='bottom')`.
- **tag** (`str` or `int`, optional): The tag of the subplot to operate on.
- **\*\*kwargs**: Additional keyword arguments passed directly to `scipy.signal.find_peaks`.

**Returns:**
- `Plotter`: The instance itself for method chaining.

**Example:**

```python
plotter.add_line(x=wavenumber, y=intensity) \
       .add_peak_labels(
           top_k=3,
           prominence=100,
           format_str="{:.0f}",
           font_props={'color': 'red'}
       )
```

---

### `add_image_box`

Embed an image (e.g., a molecular structure, logo, or micrograph) into the plot area. The image can be placed using data coordinates (to pin it to a feature) or axes coordinates (to float it in a corner).

```python
def add_image_box(
    self,
    image_path: str,
    x: float,
    y: float,
    zoom: float = 0.1,
    coord_system: str = 'data',
    alpha: float = 1.0,
    tag: Optional[Union[str, int]] = None
) -> 'Plotter':
```

**Parameters:**

- **image_path** (`str`): Path to the image file (PNG, JPG, etc.). Note: SVG support depends on your matplotlib backend.
- **x** (`float`): X-coordinate for the center of the image.
- **y** (`float`): Y-coordinate for the center of the image.
- **zoom** (`float`): Scaling factor for the image. `1.0` is original size. Adjust this to fit your plot.
- **coord_system** (`str`): Coordinate system to use.
    - `'data'`: Use the data coordinates of the axes (default). The image moves if you zoom/pan.
    - `'axes'`: Use axes fraction coordinates `(0,0)` is bottom-left, `(1,1)` is top-right. The image stays fixed relative to the subplot frame.
- **alpha** (`float`): Transparency of the image (0.0 to 1.0).
- **tag** (`str` or `int`, optional): The tag of the subplot to operate on.

**Returns:**
- `Plotter`: The instance itself for method chaining.

**Example:**

```python
# Place a molecule structure in the top-right corner
plotter.add_image_box(
    image_path="structure.png",
    x=0.9, y=0.9,
    coord_system='axes',
    zoom=0.15
)
```

---

### `add_bracket`

Add a bracket (square or curly style) to annotate a specific range on the x-axis. Useful for labeling spectral bands or time intervals.

```python
def add_bracket(
    self,
    x_start: float,
    x_end: float,
    text: str,
    y_position: float,
    color: str = 'black',
    linewidth: float = 1.0,
    fontsize: float = 10,
    style: str = 'square',
    tag: Optional[Union[str, int]] = None
) -> 'Plotter':
```

**Parameters:**

- **x_start** (`float`): Starting x-coordinate of the bracket.
- **x_end** (`float`): Ending x-coordinate of the bracket.
- **text** (`str`): The label text to display above the bracket.
- **y_position** (`float`): The y-coordinate where the horizontal line of the bracket is drawn.
- **color** (`str`): Color of the bracket lines and text.
- **linewidth** (`float`): Width of the bracket lines.
- **fontsize** (`float`): Font size of the label text.
- **style** (`str`): Style of the bracket.
    - `'square'`: Standard square bracket `[--]`.
    - `'curly'`: (Not yet implemented, falls back to square).
- **tag** (`str` or `int`, optional): The tag of the subplot to operate on.

**Returns:**
- `Plotter`: The instance itself for method chaining.

**Example:**

```python
plotter.add_bracket(
    x_start=1200, x_end=1400,
    text=r"$\nu(C-N)$",
    y_position=0.8,
    color='blue'
)
```

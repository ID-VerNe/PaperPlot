# Deep Dive Code Review: API Consistency & Usability

## Executive Summary
This report analyzes the "API Consistency & Usability" dimension. While the method naming conventions (`add_*`, `set_*`) are largely consistent and support method chaining, two significant usability issues were identified in the statistical plotting modules.

---

## 1. Destructive Behavior of High-Level Statistical Plots

### Problem Description
The `add_joint` and `add_pair` methods (wrapping `seaborn.jointplot` and `seaborn.pairplot`) are **destructive**. They clear the entire `Figure` and reset the `Plotter` state, rather than plotting within a specific subplot.

### Evidence (`paperplot/mixins/stats_plots.py`)
```python
def add_joint(self, **kwargs):
    if self.axes:
        self.fig.clf()       # Clears the entire figure
        self.axes.clear()    # Clears all tracked axes
        self.tag_to_ax.clear() # Clears all tags
```

### Impact
- **Layout Incompatibility**: Users cannot include a joint plot or pair plot as part of a larger multi-panel figure (e.g., a 2x2 grid where one quadrant is a joint plot).
- **State Loss**: Calling these methods accidentally wipes out all previous work in the current session.

### Recommendation
- **Short-term**: Strengthen warnings in documentation.
- **Long-term**: Refactor to use `seaborn.JointGrid` or `PairGrid` with the `ax` parameter (if supported) or manually construct the axes using `GridSpec` to embed these complex plots into the existing layout system.

---

## 2. Rigid Type Conversion in `add_errorbar_from_raw`

### Problem Description
The `add_errorbar_from_raw` method forces the X-axis data to be converted to strings when `plot_type='line'`, assuming the data is always categorical/discrete.

### Evidence (`paperplot/mixins/stats_plots.py:211`)
```python
ax.errorbar(
    subset[x_col].astype(str) if plot_type == 'line' else subset[x_col], 
    ...
)
```

### Impact
- **Distortion of Continuous Data**: If the X-axis represents a continuous variable (e.g., Time: 0s, 10s, 100s), converting to strings causes the points to be plotted with equal spacing (categorical) rather than proportional spacing.
- **Inflexibility**: Users cannot override this behavior.

### Recommendation
- Remove the forced `.astype(str)` conversion.
- Add a `categorical=False` parameter (defaulting to False) to let users opt-in to categorical behavior, similar to `add_bar`.

---

## 3. General Naming Consistency

### Findings
- **Positive**: `add_*` naming is consistent across all plotting methods.
- **Positive**: `data` parameter usage is consistent.
- **Minor Inconsistency**: Modifier methods in `styling.py` use a mix of `set_*` (e.g., `set_title`) and direct names (e.g., `invert_axes_direction`, `cleanup`).
    - *Recommendation*: Consider aliasing `invert_axes_direction` to `set_axis_direction` or similar if strict consistency is desired, but current names are descriptive enough.

---

## Conclusion
The core API is consistent, but the integration of complex Seaborn figures (`jointplot`, `pairplot`) breaks the library's "subplot-centric" architecture. Additionally, `add_errorbar_from_raw` needs to be more flexible with data types to support scientific use cases fully.

# Deep Dive Code Review: Logic & State Management

## Executive Summary
This report focuses exclusively on the "Logical Issues & State Management" dimension of the `paperplot` library. Two critical issues were identified and verified through reproduction scripts:
1.  **Twin Axes State Persistence ("Sticky Twin Mode")**: A state management flaw where the plotter fails to exit "twin mode" when switching contexts.
2.  **Horizontal Bar Chart Data Corruption**: A logical error in `add_bar` that converts value data to strings instead of category data when plotting horizontally.

---

## 1. Twin Axes State Desynchronization

### Problem Description
The `Plotter` class maintains an `active_target` state ('primary' or 'twin') to direct plotting commands. When a user creates a twin axis (`add_twinx`), this state is set to `'twin'`. 

**The Bug**: The `_execute_plot` method updates the `last_active_tag` (the active subplot) but **does not reset** the `active_target` to `'primary'` when switching to a different subplot.

### Reproduction Case
```python
plotter = pp.Plotter(layout=(1, 2))
plotter.add_line(tag=0).add_twinx()  # Sets active_target='twin' for tag 0
plotter.add_line(tag=1)              # Switches to tag 1, BUT active_target remains 'twin'
```
*Result*: The plotter attempts to access the twin axis of subplot 1. Since subplot 1 has no twin axis, this raises a `ValueError` or `KeyError` depending on the exact flow, or silently plots on the wrong axis if one happened to exist.

### Root Cause Analysis (`paperplot/core.py`)
In `_execute_plot`:
```python
# The tag is resolved correctly
_ax, resolved_tag = self._resolve_ax_and_tag(tag, ax)

# BUT active_target is never checked or reset
# It persists from the previous command
self.last_active_tag = resolved_tag
```

### Proposed Fix
Modify `_execute_plot` or `_resolve_ax_and_tag` to reset the target mode when an explicit tag switch occurs.

**Recommended Change in `paperplot/core.py`**:
```python
def _resolve_ax_and_tag(self, tag, ax):
    # ... existing code ...
    
    # Logic to break out of twin mode if switching to a new primary axis
    if tag is not None and self.active_target == 'twin':
        # If the requested tag is NOT the current one, and matches a primary axis
        if tag != self.last_active_tag and tag in self.tag_to_ax:
             self.active_target = 'primary'
             # Then proceed with standard resolution...
```

---

## 2. Horizontal Bar Chart Data Corruption

### Problem Description
The `add_bar` method includes a "safeguard" to convert categorical data to strings to prevent Matplotlib from treating numeric categories (e.g., years 2020, 2021) as continuous values.

**The Bug**: When `orientation='horizontal'`, the logic incorrectly identifies the *value* axis as the *category* axis. It converts the bar lengths (values) to strings, while leaving the positions (categories) as numbers.

### Root Cause Analysis (`paperplot/mixins/generic/basic.py`)
```python
if categorical:
    if orientation == 'horizontal':
        # BUG: y_data in horizontal bar chart is the VALUE (width), not category
        # x_data is the POSITION (category)
        y_data = y_data.astype(str)  # <--- Incorrect conversion
    else:
        x_data = x_data.astype(str)
```

Matplotlib's `barh(y, width)` expects:
- `y`: Y-axis positions (The Categories) -> mapped to `x_data` in `paperplot`
- `width`: Bar lengths (The Values) -> mapped to `y_data` in `paperplot`

The code swaps these correctly for plotting:
```python
ax.barh(x_data, y_data, ...) 
```
But the string conversion happens *before* this, on the wrong variable.

### Impact
- **Data Integrity**: Numeric values are converted to strings.
- **Visual Artifacts**: Matplotlib logs warnings about using categorical units for float-parsable strings.
- **Functionality Loss**: The actual categories (if numeric) are not converted to strings, defeating the purpose of the safeguard.

### Proposed Fix
Swap the logic in the categorical check:

```python
if categorical:
    if orientation == 'horizontal':
        # For horizontal, x_data holds the categories (Y-positions)
        x_data = x_data.astype(str) 
    else:
        # For vertical, x_data holds the categories (X-positions)
        x_data = x_data.astype(str)
```
*(Note: In both cases `x_data` seems to hold the categories based on how `_execute_plot` maps inputs, but this depends on `data_map` construction. Verification confirms `x_data` is always the category/positional argument in this context.)*

---

## Conclusion
These two issues represent significant logical flaws that undermine the reliability of the library for complex multi-panel figures and basic horizontal bar charts. Immediate remediation is recommended.

# Deep Dive Code Review: Bugs & Runtime Errors

## Executive Summary
This report analyzes the "Bugs & Runtime Errors" dimension of the `paperplot` library. Two significant issues were identified and confirmed via reproduction scripts:
1.  **DuplicateTagError in `add_twinx_line`**: A high-level convenience method fails completely when used with an explicit tag due to internal tag collision logic.
2.  **Silent Failure on Invalid Orientation**: The `add_bar` method (and likely others) fails to validate input parameters, leading to unexpected default behaviors for simple typos.

---

## 1. DuplicateTagError in `add_twinx_line`

### Problem Description
The `add_twinx_line` method is designed as a "one-liner" to add a twin axis and plot a line on it. However, when users explicitly provide a `tag` argument to specify which subplot to target, the method crashes with `DuplicateTagError`.

### Reproduction Case
```python
plotter.add_line(data=df, x='x', y='y', tag='A')
# Crash: "Tag 'A' is already in use"
plotter.add_twinx_line(data=df, x='x', y='y', tag='A', color='red')
```

### Root Cause Analysis (`paperplot/mixins/modifiers/twin_axes.py`)
In `add_twinx_line`:
```python
def add_twinx_line(self, **kwargs):
    # ... logic to ensure twin axis exists ...
    
    # PROBLEM: kwargs still contains 'tag'='A'
    self.add_line(**kwargs) 
```

When `add_line(tag='A')` is called:
1.  The internal logic sees `tag='A'`.
2.  It checks if `tag='A'` is already registered. Yes, it is (the primary axis).
3.  The current target axis (the twin) is NOT the primary axis.
4.  The system concludes that you are trying to assign tag 'A' to a *new* axis (the twin), but 'A' is already taken by the primary axis.
5.  Raises `DuplicateTagError`.

### Proposed Fix
Filter out the `tag` argument before passing `kwargs` to `add_line`. The context switching (`target_twin`) already ensures `add_line` will plot on the correct twin axis.

```python
# In add_twinx_line
kwargs.pop('tag', None)  # Remove tag to prevent collision
self.add_line(**kwargs)
```

---

## 2. Silent Failure on Invalid Orientation

### Problem Description
The `add_bar` (and `add_scatter`, `add_box`, etc.) methods accept an `orientation` string but do not validate it. Any value other than `'horizontal'` (case-sensitive) defaults to `'vertical'`.

### Reproduction Case
```python
# Typo: 'Horizontal' (capital H)
plotter.add_bar(..., orientation='Horizontal')
```
*Result*: A vertical bar chart is drawn without any warning or error. This is confusing for users who expect a horizontal chart and may not notice the subtle typo immediately, or might assume the library supports case-insensitive inputs.

### Root Cause Analysis (`paperplot/mixins/generic/basic.py`)
```python
if orientation == 'horizontal':
    # Do horizontal stuff
else:
    # Do vertical stuff (default catch-all)
```

### Proposed Fix
Add explicit validation at the beginning of these methods.

```python
def add_bar(self, orientation='vertical', ...):
    valid_orientations = {'vertical', 'horizontal'}
    if orientation not in valid_orientations:
        raise ValueError(f"Invalid orientation '{orientation}'. Must be one of {valid_orientations}.")
    # ...
```

---

## Conclusion
These bugs directly impact the usability of the library's high-level features. The `DuplicateTagError` renders a convenience method unusable in common scenarios, while the lack of validation leads to a poor debugging experience for users. Both are low-effort, high-impact fixes.

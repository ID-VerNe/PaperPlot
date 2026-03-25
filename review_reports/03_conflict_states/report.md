# Deep Dive Code Review: Conflict States

## Executive Summary
This report analyzes the "Conflict States" dimension of the `paperplot` library. A critical architectural vulnerability was identified where the library's manual layout controls can be silently overridden by external or accidental calls to Matplotlib's layout engines, leading to user frustration and lost work.

---

## 1. Silent Layout Engine Override

### Problem Description
`paperplot` offers precise manual layout control via methods like `set_padding()` and `set_spacing()`. These methods correctly disable the default automatic layout engine (`constrained_layout`) to apply user-specified margins.

**The Conflict**: If `fig.tight_layout()` is called subsequently—whether by the user (habitually), by another library function, or by an interactive backend—it re-enables a layout engine and recalculates all subplot parameters, completely discarding the manual settings without warning.

### Reproduction Case
```python
plotter = pp.Plotter(layout=(2, 2))
plotter.set_padding(left=0.2)  # User sets specific left margin
# Result: left=0.2 (Correct)

plotter.fig.tight_layout()     # User calls this thinking it's safe/good practice
# Result: left=0.073 (Manual setting lost!)
```

### Root Cause Analysis (`paperplot/mixins/modifiers/layout.py`)
The `set_padding` method disables the current engine but does not set a persistent "manual mode" flag or protect against re-enablement.

```python
def set_padding(self, ...):
    if self.fig.get_layout_engine() is not None:
        self.fig.set_layout_engine(None)  # Disables engine once
    self.fig.subplots_adjust(...)         # Applies manual settings
```

The `Plotter` class does not intercept or wrap `tight_layout`, leaving the figure vulnerable to standard Matplotlib behaviors that conflict with the library's declarative state.

### Impact
- **Loss of Precision**: Users fine-tuning publication-quality figures will lose their adjustments.
- **Silent Failure**: The override happens without error or warning, making it hard to debug why margins aren't sticking.
- **API Confusion**: Users may not understand why `set_padding` works initially but "breaks" later.

### Proposed Fix
Implement a "Manual Layout Lock" mechanism.

1.  **Add State Flag**: Add `self._manual_layout_active = False` to `Plotter`.
2.  **Set Flag**: In `set_padding/set_spacing`, set `self._manual_layout_active = True`.
3.  **Intercept Conflict**: 
    -   Option A (Aggressive): Monkey-patch `fig.tight_layout` to raise a warning if `_manual_layout_active` is True.
    -   Option B (Passive): Document clearly that `tight_layout` is incompatible with manual padding.
    -   Option C (Robust): Override `tight_layout` in the `Plotter` class (if it exposes it) or wrap the figure object to warn users.

**Recommended Implementation (Option A - Safe Wrapper)**:
```python
# In Plotter.__init__
self._original_tight_layout = self.fig.tight_layout
self.fig.tight_layout = self._safe_tight_layout

def _safe_tight_layout(self, *args, **kwargs):
    if getattr(self, '_manual_layout_active', False):
        import warnings
        warnings.warn(
            "Manual layout settings (set_padding/set_spacing) detected. "
            "Calling tight_layout() will override these settings.",
            UserWarning
        )
    return self._original_tight_layout(*args, **kwargs)
```

---

## Conclusion
This issue represents a significant "gotcha" in the library's design. Implementing a safety mechanism will greatly improve the robustness of the layout system and prevent user errors.

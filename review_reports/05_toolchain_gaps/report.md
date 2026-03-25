# Deep Dive Code Review: Built-in Analysis Toolchain Gaps

## Executive Summary
This report analyzes the "Built-in Utils" dimension. While `StatsPlotsMixin` and `DataAnalysisPlotsMixin` provide some advanced capabilities, the library lacks several standard analytical tools expected in a scientific plotting wrapper, and existing implementations suffer from poor developer experience (DX).

---

## 1. Missing Essential Analytical Tools

### Gaps Identification
Compared to libraries like Seaborn or high-level wrappers like Plotly Express, `paperplot` is missing key "one-liner" analytical visualizations:

1.  **Trend Lines / Regression**: No `add_trendline` or `add_regression` method. Users must calculate fit parameters manually and use `add_line`.
2.  **Confidence Intervals (Shaded)**: `add_errorbar_from_raw` supports vertical error bars but not shaded confidence intervals (bands) for time-series data, which is a standard requirement for scientific publication.
3.  **Polynomial Fit**: No `add_polyfit` to quickly visualize non-linear trends.

### Impact
Users must perform data analysis *outside* the plotting call (e.g., using `scipy.stats` or `numpy.polyfit` manually) and then pass the result to `add_line`. This breaks the "declarative" flow where the plot command handles the visualization logic.

---

## 2. Developer Experience (DX) Issues in Analysis Methods

### Problem Description
Methods in `analysis_plots.py` (e.g., `add_binned_plot`, `add_distribution_fit`) use `**kwargs` to capture core logic parameters (`bins`, `agg_func`, `dist_name`) instead of explicit arguments.

### Evidence
```python
# Current Signature
def add_binned_plot(self, **kwargs) -> 'Plotter': ...

# Implementation
def plot_logic(..., **p_kwargs):
    bins = p_kwargs.pop('bins', 10)
    # ...
```

### Impact
-   **No Autocomplete**: IDEs cannot suggest `bins` or `agg_func` parameters.
-   **No Type Checking**: Static analysis tools cannot validate inputs.
-   **Documentation Disconnect**: Users must read the docstring carefully rather than relying on the function signature.

### Recommendation
Refactor signatures to be explicit:
```python
def add_binned_plot(self, bins: int = 10, agg_func: str = 'mean', ..., **kwargs):
    # Pass explicit args to internal logic or merge into kwargs
```

---

## 3. `add_errorbar_from_raw` Limitations (Revisited)

### Problem
As noted in the API Consistency report, this method forces categorical conversion. In the context of "Analysis Tools", this is a functional gap because it prevents correct analysis of continuous independent variables (e.g., dose-response curves with uneven spacing).

---

## Conclusion
To truly serve as a "High-level wrapper for scientific papers", `paperplot` needs to bridge the gap between "plotting data" and "visualizing analysis". Adding regression lines, confidence bands, and explicit function signatures should be the next priority.

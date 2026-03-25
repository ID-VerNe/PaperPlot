# PaperPlot v0.2.0 Roadmap Proposal: "Data-Driven Intelligence"

Based on the current architecture and common research visualization needs, here are 3 major feature proposals to elevate PaperPlot from a "wrapper" to an "intelligent visualization engine".

## 1. 🧠 Intelligent Statistical Annotation (The "P-Value" Engine)
**Problem**: Researchers frequently need to add significance brackets (e.g., `ns`, `*`, `**`, `****`) to bar/box/violin plots. Currently, this requires manual calculation of coordinates and drawing lines, which is tedious and fragile.
**Proposed Feature**: `add_significance_brackets()`
- **Input**: Raw data or pre-computed p-values + pairs of columns to compare.
- **Mechanism**:
  - Automatically calculate y-positions to avoid overlapping with data points or other brackets.
  - Automatically draw the bracket line and the text.
  - Support "step-up" layout for multiple comparisons.
- **API Example**:
  ```python
  plotter.add_violin(data=df, x='Treatment', y='Response') \
         .add_significance_brackets(
             pairs=[('Control', 'Drug A'), ('Control', 'Drug B')],
             data=df, x='Treatment', y='Response',
             test='t-test_ind'  # or pass p-values directly
         )
  ```

## 2. 🧊 3D Engine & Interactive Export (The "Dimension" Upgrade)
**Problem**: The library currently focuses on 2D static plots. Scientific visualization often requires 3D surfaces or interactive HTML exports for presentations.
**Proposed Feature A**: `add_3d_surface()` / `add_3d_scatter()`
- **Mechanism**: Integrate `mpl_toolkits.mplot3d` into the `Plotter` workflow.
- **Challenge**: 3D axes in Matplotlib require `projection='3d'` at creation time. Need to update `Plotter` initialization to support per-subplot projection types.
**Proposed Feature B**: `save_interactive()`
- **Mechanism**: Export the Matplotlib figure to a standalone HTML file using `mpld3` or `plotly` conversion.
- **Value**: Users can embed zoomable, hoverable plots in their lab websites or digital papers.

## 3. 📄 The "Figure Composer" (The "Adobe Illustrator" Killer)
**Status**: **DEPRIORITIZED / RE-EVALUATED**
**Analysis**: Merging live Matplotlib figures is technically complex due to backend constraints (Axes are tied to specific Figures).
**Revised Approach**:
- **Phase 1 (Easy)**: Enhance `Plotter` to accept `subfigures` (Matplotlib 3.4+) as a backend, allowing multiple independent `Plotter` instances to draw on the same canvas.
- **Phase 2 (Hard)**: A full SVG-based composition engine.
**Recommendation**: Postpone until v0.3.0 or later. Focus on single-figure complexity first.

## 4. 🔬 Domain-Specific Modules (Expansion Pack)
- **Bioinformatics**: `add_volcano()` (Volcano plot for gene expression), `add_heatmap_cluster()` (Clustermap).
- **Control Theory**: `add_bode()` (Bode plot), `add_nyquist()`.
- **Chemistry**: `add_spectrum()` (with peak detection and labeling).

---

### Recommended Priority
1. **Statistical Annotation** (High impact, fits current architecture)
2. **3D Support** (Moderate effort, opens new domains)
3. **Figure Composer** (High effort, but huge value for final submission)

## 5. 🧪 Spectroscopy & Advanced Annotation (The "Complex Plot" Pack)
**Source**: User request based on `复杂图.png` (Raman spectra with molecular structure).
**Problem**: Creating publication-quality spectral plots currently requires manual coordinate hunting for peak labels, manual drawing of brackets for spectral bands, and external tools to paste chemical structures.

**Proposed Feature A**: `add_peak_labels()`
- **Mechanism**: Integrate `scipy.signal.find_peaks`.
- **Functionality**: Automatically detect local maxima in the data and place text labels with arrows pointing to the peaks.
- **API Example**:
  ```python
  plotter.add_line(data=df, x='Raman Shift', y='Intensity') \
         .add_peak_labels(
             data=df, x='Raman Shift', y='Intensity',
             top_k=5,          # Label top 5 peaks
             prominence=100,   # Minimum peak height
             format_str="{:.0f}" # Label format (e.g., '1626')
         )
  ```

**Proposed Feature B**: `add_floating_image()`
- **Mechanism**: Use `OffsetImage` and `AnnotationBbox` from matplotlib.
- **Functionality**: Embed images (molecules, logos, microstructure photos) *inside* the plot area at specific coordinates (data or axes relative).
- **API Example**:
  ```python
  plotter.add_floating_image(
      image_path="molecule_structure.png",
      x=0.5, y=0.8, coord_system='axes', # Top-center
      zoom=0.15
  )
  ```

**Proposed Feature C**: `add_bracket()` (Generalization of Statistical Brackets)
- **Mechanism**: Draw lines and text to group x-axis ranges.
- **Use Case**: Labeling spectral bands (e.g., "v(C-N)") as seen in the right panel of the user's image.
- **API Example**:
  ```python
  plotter.add_bracket(
      x_range=(1200, 1450),
      text=r"$\nu(C-N)$",
      y_position=1000,
      style='square' # or 'curly'
  )
  ```

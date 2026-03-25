import numpy as np
import pandas as pd
import paperplot as pp
import matplotlib.pyplot as plt

def main():
    print("--- Running Example: spectroscopy_complex_demo.py ---")
    
    # 1. Generate Synthetic Raman Data
    x = np.linspace(200, 2000, 1000)
    
    # Background noise
    noise = np.random.normal(0, 50, size=len(x))
    baseline = 700 + noise
    
    # Peaks (Gaussian)
    def gaussian(x, mu, sigma, amp):
        return amp * np.exp(-0.5 * ((x - mu) / sigma)**2)
    
    peaks_signal = (
        gaussian(x, 451, 10, 500) +
        gaussian(x, 601, 15, 200) +
        gaussian(x, 727, 5, 50) +
        gaussian(x, 1189, 20, 150) +
        gaussian(x, 1400, 15, 1200) + # Double peak
        gaussian(x, 1451, 15, 1000) +
        gaussian(x, 1626, 10, 3500)   # Main peak
    )
    
    y_raw = baseline + peaks_signal
    y_clean = peaks_signal
    
    df = pd.DataFrame({'Raman Shift': x, 'Raw Intensity': y_raw, 'Clean Intensity': y_clean})

    # 2. Setup Layout (1x2 Grid)
    plotter = pp.Plotter(layout=(1, 2), style='publication', figsize=(12, 5))
    
    # --- Left Plot: Raw vs Clean with Peak Labels ---
    # We will offset the raw data to match the image style
    
    plotter.add_line(data=df, x='Raman Shift', y='Raw Intensity', label='original curve', 
                     color='#008080', linewidth=1.5, tag=0) \
           .add_line(data=df, x='Raman Shift', y='Clean Intensity', label='peaks of MB', 
                     color='#00FFFF', linewidth=1.5, tag=0) \
           .set_ylabel("Intensity (a.u.)") \
           .set_xlabel("Raman shift (cm$^{-1}$)") \
           .set_legend(loc='upper left') \
           .set_ylim(bottom=-500, top=4000) \
           .add_peak_labels(
               prominence=100, 
               threshold=50, 
               distance=20,
               top_k=5,
               format_str="{:.0f}",
               offset=(0, 15),
               arrow_props=dict(arrowstyle="-", color="black", linewidth=0.8),
               tag=0
           )

    # --- Right Plot: Detailed Spectrum with Structure & Brackets ---
    # We plot the clean spectrum again, maybe filled or just lines
    # For variety, let's make it a filled area plot style using add_line + fill_between (manual for now)
    
    plotter.add_line(data=df, x='Raman Shift', y='Clean Intensity', label='MB Spectrum', 
                     color='#008080', linewidth=1, tag=1)
    
    # Manually fill under curve for effect (access ax directly)
    ax1 = plotter.get_ax(1)
    ax1.fill_between(x, y_clean, color='cyan', alpha=0.3)
    ax1.fill_between(x, gaussian(x, 1626, 10, 3500), color='#008080', alpha=0.6) # Highlight main peak
    
    # Add Molecular Structure (Floating Image)
    # We use an existing PNG file as a placeholder since matplotlib doesn't natively support SVG rasterization
    # without extra dependencies.
    plotter.add_image_box(
        image_path='1_layout_showcase.png', 
        x=0.5, y=0.8, 
        coord_system='axes', 
        zoom=0.15, 
        tag=1
    )
    
    # Add Brackets for Spectral Bands
    plotter.add_bracket(
        x_start=1180, x_end=1480, 
        text=r"$\nu(C-N)$", 
        y_position=1800, 
        height=200,
        color='#0044cc',
        tag=1
    )
    
    plotter.set_xlabel("Raman shift (cm$^{-1}$)") \
           .hide_axes(y_axis=True, tag=1) # Hide Y axis like the example
           
    # Add specific peak labels with custom text (e.g., greek letters)
    # We can use add_text for this, or abuse add_peak_labels if we had custom labels list (future feature)
    # For now, let's use standard annotations for specific chemical bonds
    ax1.annotate(r"$\nu(C-C)_{ring}$", xy=(1626, 3500), xytext=(-30, 20), 
                 textcoords='offset points', arrowprops=dict(arrowstyle="->"))

    plotter.set_padding(wspace=0.05) # Tighten space between plots
    
    output_path = 'complex_spectroscopy_example.png'
    plotter.save(output_path)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    main()

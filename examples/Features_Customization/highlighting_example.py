# examples/Features_Customization/highlighting_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

try:
    # 1. Create a Plotter instance
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 6), style='publication')

    # 2. Add a plot with some interesting features
    x = np.linspace(0, 2 * np.pi, 200)
    y = np.sin(x) * np.exp(-x / 4)
    df = pd.DataFrame({'x': x, 'y': y})

    plotter.add_line(data=df, x='x', y='y', tag='main_plot', label='Damped Sine Wave'
    ).set_title('Highlighting Data Regions and Figure Boundary'
    ).set_xlabel('Time'
    ).set_ylabel('Amplitude'
    ).set_legend()

    # 3. Use add_highlight_box to highlight a specific data region
    # Highlight the first peak of the wave
    plotter.add_highlight_box(
        tag='main_plot',
        x_range=(0.5, 2.5),
        y_range=(0.4, 0.8),
        facecolor='orange',
        alpha=0.3,
        label='First Peak Region' # Note: label won't show by default, but can be used with legends
    ).add_text(1.5, 0.6, 'First Peak', ha='center', va='center', fontsize=10)

    # Highlight the region where the wave decays
    plotter.add_highlight_box(
        tag='main_plot',
        x_range=(4, 6),
        y_range=(-0.2, 0.2),
        facecolor='lightblue',
        alpha=0.4
    ).add_text(5, 0, 'Decay Region', ha='center', va='center', fontsize=10)

    # 4. Use fig_add_boundary_box to draw a border around the axes area

    # plotter.fig_add_text(0.5, 0.98, 'Figure with Smart Boundary Box', ha='center', va='top', fontsize=12)
    plotter.fig_add_boundary_box(padding=0.08, edgecolor='darkgray', linewidth=2)
    # 5. Save the figure
    plotter.save("highlighting_example.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"--- Finished Example: {__file__} ---")
print("A new file 'highlighting_example.png' was generated.")

# examples/Features_Customization/fig_text_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

try:
    # 1. Create a Plotter instance with a 1x2 layout
    plotter = pp.Plotter(layout=(1, 2), figsize=(10, 5), style='publication')

    # 2. Add some plots to the subplots
    df = pd.DataFrame({
        'x': np.linspace(0, 10, 100),
        'y1': np.sin(np.linspace(0, 10, 100)),
        'y2': np.cos(np.linspace(0, 10, 100))
    })

    plotter.add_line(data=df, x='x', y='y1', tag='ax00', label='Sine Wave'
    ).set_title('Left Subplot'
    ).set_xlabel('X-axis'
    ).set_ylabel('Y-axis'
    ).set_legend()

    plotter.add_scatter(data=df, x='x', y='y2', tag='ax01', label='Cosine Points', marker='o', s=20
    ).set_title('Right Subplot'
    ).set_xlabel('X-axis'
    ).set_ylabel('Y-axis'
    ).set_legend()

    # 3. Add figure-level text using fig_text
    plotter.fig_add_text(0.5, 0.96, 'Overall Figure Title (using fig_add_text)', ha='center', va='top', fontsize=14, weight='bold')
    plotter.fig_add_text(0.02, 0.5, 'Left Side Annotation', rotation=90, va='center', ha='left', fontsize=10, color='gray')
    plotter.fig_add_text(0.98, 0.5, 'Right Side Annotation', rotation=-90, va='center', ha='right', fontsize=10, color='gray')
    plotter.fig_add_text(0.5, 0.02, 'Figure Footer - Source: Example Data', ha='center', va='bottom', fontsize=8, style='italic')

    # 4. Apply cleanup and save the figure
    plotter.cleanup(auto_share=True) # Auto-share for demonstration
    plotter.save("fig_text_example.png")

except pp.PaperPlotError as e:
    print(f"\nA PaperPlot error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"--- Finished Example: {__file__} ---")
print("A new file 'fig_text_example.png' was generated.")

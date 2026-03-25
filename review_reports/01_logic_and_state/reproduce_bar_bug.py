import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Setup data
df = pd.DataFrame({
    'category': [1, 2, 3],  # Numeric categories
    'value': [10, 20, 30]
})

print("Testing Horizontal Bar Chart with Categorical=True")
try:
    plotter = pp.Plotter(layout=(1, 1))
    
    # We expect 'category' to be treated as strings (equally spaced)
    # and 'value' to be treated as numbers (length of bars)
    # But due to the bug, 'value' might be converted to strings!
    
    plotter.add_bar(
        data=df, 
        x='category', 
        y='value', 
        orientation='horizontal', 
        categorical=True
    )
    
    # Use 'ax00' or whatever default tag is used if 1 failed
    # Actually, let's just use .get_ax(1) or check tag_to_ax
    ax_tag = list(plotter.tag_to_ax.keys())[0]
    ax = plotter.get_ax(ax_tag)
    
    # Check what was plotted
    # For barh, the patches should have widths equal to the values [10, 20, 30]
    bars = ax.patches
    widths = [p.get_width() for p in bars]
    print(f"Bar widths: {widths}")
    
    # Check Y-axis labels (should be the categories '1', '2', '3')
    yticklabels = [l.get_text() for l in ax.get_yticklabels()]
    print(f"Y-tick labels: {yticklabels}")
    
    # If the bug exists:
    # 1. 'value' (y_data) was converted to string. Matplotlib might handle this gracefully 
    #    if they look like numbers, BUT it might cause issues or warnings.
    # 2. 'category' (x_data) was NOT converted to string. So if categories are 1, 2, 10, 
    #    they will be spaced numerically, not visually equidistant (if that was the intent of categorical=True).
    
    # Let's check if the axis units are categorical
    print(f"Y-axis units: {ax.yaxis.get_units()}")
    
    if widths == [10.0, 20.0, 30.0]:
        print("Widths are correct numbers.")
    else:
        print("Widths are NOT correct.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

# Setup data
df = pd.DataFrame({'cat': ['A', 'B'], 'val': [10, 20]})

print("Testing orientation typo handling...")
try:
    plotter = pp.Plotter(layout=(1, 1))
    
    # Intention: Horizontal bar chart
    # Mistake: Typo 'Horizontal' (capital H) instead of 'horizontal'
    plotter.add_bar(
        data=df, 
        x='cat', 
        y='val', 
        orientation='Horizontal',  # Typo!
        tag='typo_test'
    )
    
    ax = plotter.get_ax('typo_test')
    patches = ax.patches
    
    # Check first bar
    p = patches[0]
    height = p.get_height()
    width = p.get_width()
    
    print(f"Bar 0: height={height}, width={width}")
    
    # Logic check
    if height == 10:
        print("Result: Vertical bar chart (height matches value).")
        print("This confirms the typo was silently ignored and defaulted to vertical.")
    elif width == 10:
        print("Result: Horizontal bar chart (width matches value).")
        print("The library handled the typo correctly (or case-insensitively).")
    else:
        print("Result: Something else happened.")

except Exception as e:
    print(f"Error: {e}")

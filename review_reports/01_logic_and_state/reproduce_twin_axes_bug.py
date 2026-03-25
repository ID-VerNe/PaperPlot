import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

# Setup data
df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

try:
    print("Step 1: Create Plotter with 2 subplots")
    plotter = pp.Plotter(layout=(1, 2))
    
    print("Step 2: Plot on first subplot (tag=0) and add twinx")
    # This sets active_target='twin' and last_active_tag=0
    plotter.add_line(data=df, x='x', y='y', tag=0)
    plotter.add_twinx() 
    plotter.add_line(data=df, x='x', y='y', color='red') # Plots on twin
    
    print(f"Current State after Twin: active_target={plotter.active_target}, last_active_tag={plotter.last_active_tag}")

    print("Step 3: Plot on second subplot (tag=1)")
    # This should switch to tag=1, but if active_target is still 'twin', it might fail
    # or try to find a twin axis for tag=1 (which doesn't exist)
    plotter.add_line(data=df, x='x', y='y', tag=1)
    
    print(f"Current State after Tag Switch: active_target={plotter.active_target}, last_active_tag={plotter.last_active_tag}")
    
    print("Success! No error raised.")

except Exception as e:
    print(f"\nCRITICAL FAILURE: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

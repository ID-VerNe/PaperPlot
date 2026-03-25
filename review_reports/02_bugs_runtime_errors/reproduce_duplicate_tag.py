import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

# Setup data
df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

try:
    print("Step 1: Create Plotter")
    plotter = pp.Plotter(layout=(1, 1))
    
    print("Step 2: Plot primary line")
    plotter.add_line(data=df, x='x', y='y', tag='A', color='blue')
    
    print("Step 3: Try to add twin axis line with explicit tag='A'")
    # This should work seamlessly, but due to the bug it might raise DuplicateTagError
    plotter.add_twinx_line(data=df, x='x', y='y', tag='A', color='red', linestyle='--')
    
    print("Success! Twin line added.")

except Exception as e:
    print(f"\nCRITICAL FAILURE: {type(e).__name__}: {e}")
    # import traceback
    # traceback.print_exc()

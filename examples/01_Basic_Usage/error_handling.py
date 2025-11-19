# examples/error_handling_test.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 测试 DuplicateTagError ---
print("\n--- Test 1: Catching DuplicateTagError ---")
try:
    plotter = pp.Plotter(layout=(2, 1))
    df = pd.DataFrame({'x': [1], 'y': [1]})
    
    plotter.add_bar(data=df, x='x', y='y', tag='my_tag')
    print("First plot with tag 'my_tag' added successfully.")
    
    # 故意再次使用同一个tag
    print("Attempting to add another plot with the same tag...")
    plotter.add_bar(data=df, x='x', y='y', tag='my_tag')

except pp.DuplicateTagError as e:
    print("\nSuccessfully caught expected error!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Message:\n{e}")
except Exception as e:
    print(f"Caught an unexpected error: {e}")
finally:
    plt.close('all')

# --- 2. 测试 TagNotFoundError ---
print("\n--- Test 2: Catching TagNotFoundError ---")
try:
    plotter = pp.Plotter(layout=(1, 1))
    plotter.add_line(data=pd.DataFrame({'t': [0], 'v': [0]}), x='t', y='v', tag='actual_tag')
    print("Plot with tag 'actual_tag' added successfully.")
    
    # 故意使用一个不存在的tag
    print("Attempting to modify a plot with a non-existent tag...")
    plotter.set_title('non_existent_tag', 'My Title')

except pp.TagNotFoundError as e:
    print("\nSuccessfully caught expected error!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Message:\n{e}")
except Exception as e:
    print(f"Caught an unexpected error: {e}")
finally:
    plt.close('all')

# --- 3. 测试 PlottingSpaceError ---
print("\n--- Test 3: Catching PlottingSpaceError ---")
try:
    # 创建一个只能放1个图的画布
    plotter = pp.Plotter(layout=(1, 1))
    df = pd.DataFrame({'x': [1], 'y': [1]})
    
    plotter.add_bar(data=df, x='x', y='y')
    print("First plot added successfully to a 1x1 grid.")

    # 故意添加第二个图
    print("Attempting to add a second plot to the full grid...")
    plotter.add_bar(data=df, x='x', y='y')

except pp.PlottingSpaceError as e:
    print("\nSuccessfully caught expected error!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Message:\n{e}")
except Exception as e:
    print(f"Caught an unexpected error: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")

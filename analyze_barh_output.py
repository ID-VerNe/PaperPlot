"""Analyze what actually happened in the horizontal bar chart"""
import sys
sys.path.insert(0, 'C:\\Users\\VerNe\\Downloads\\Documents\\plotter')

from paperplot import Plotter
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("Analyzing the horizontal bar bug")
print("=" * 70)

df = pd.DataFrame({
    'categories': ['Product A', 'Product B', 'Product C'],
    'values': [25, 40, 35]
})

print("\nExpected:")
print("  Product A: bar of width 25")
print("  Product B: bar of width 40")
print("  Product C: bar of width 35")

# Let's trace what the code actually does
print("\n" + "=" * 70)
print("Tracing the code execution:")
print("=" * 70)

x_data = df['categories'].copy()
y_data = df['values'].copy()

print(f"\nInitial state:")
print(f"  x_data = {list(x_data)} (type: {x_data.dtype})")
print(f"  y_data = {list(y_data)} (type: {y_data.dtype})")

# Line 72: For horizontal, y_data gets converted
y_data_converted = y_data.astype(str)
print(f"\nAfter line 72 (y_data.astype(str)):")
print(f"  x_data = {list(x_data)} (type: {x_data.dtype})")
print(f"  y_data = {list(y_data_converted)} (type: {y_data_converted.dtype})")

print(f"\nLine 79 executes:")
print(f"  ax.barh(x_data, y_data)")
print(f"  = ax.barh(y={list(x_data)}, width={list(y_data_converted)})")

print(f"\nWhat matplotlib does:")
print(f"  - Y positions: {list(x_data)} (categories on Y-axis)")
print(f"  - Bar widths: {list(y_data_converted)} (converted to numbers internally)")

print("\n" + "=" * 70)
print("Creating reference plot with correct implementation:")
print("=" * 70)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# What the current code does
ax1.barh(x_data, y_data_converted)
ax1.set_title("Current implementation\n(with bug)")
ax1.set_xlabel("Value")

# What it SHOULD do
ax2.barh(x_data, y_data)  # Use numeric y_data, not string
ax2.set_title("Correct implementation\n(without string conversion)")
ax2.set_xlabel("Value")

plt.tight_layout()
plt.savefig('C:\\Users\\VerNe\\Downloads\\Documents\\plotter\\barh_comparison.png', dpi=150)
print("Saved barh_comparison.png")

print("\n" + "=" * 70)
print("Checking if there's an actual difference...")
print("=" * 70)

# Test with actual matplotlib to see if string numbers work
fig2, ax3 = plt.subplots(1, 1, figsize=(6, 4))
categories = ['A', 'B', 'C']
values_str = ['25', '40', '35']
values_num = [25, 40, 35]

try:
    ax3.barh(categories, values_str)
    plt.savefig('C:\\Users\\VerNe\\Downloads\\Documents\\plotter\\test_string_values.png')
    print("✓ Matplotlib accepts string numbers for bar widths")
    print("  (It converts them internally)")
except Exception as e:
    print(f"✗ ERROR with string values: {e}")

plt.close('all')

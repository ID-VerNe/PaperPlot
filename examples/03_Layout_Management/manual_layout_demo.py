
import numpy as np
import matplotlib.pyplot as plt
from paperplot import Plotter

def demo_manual_padding():
    print("Generating plot with manual padding...")
    # Create a simple plot
    plotter = Plotter(layout=(1, 1), figsize=(6, 4))
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plotter.add_line(x=x, y=y, label='Sine Wave')
    plotter.set_title('Manual Padding Demo (Large Margins)')
    
    # Apply manual padding: large left and bottom margins
    plotter.set_padding(left=0.2, bottom=0.2, right=0.9, top=0.9)
    
    plotter.save('manual_padding_demo.png')
    print("Saved manual_padding_demo.png")

def demo_manual_spacing():
    print("Generating plot with manual spacing...")
    # Create a 2x2 grid
    plotter = Plotter(layout=(2, 2), figsize=(8, 6))
    
    x = np.linspace(0, 10, 100)
    
    # Plot on all subplots
    plotter.add_line(x=x, y=np.sin(x), tag='ax00', label='Sin')
    plotter.add_line(x=x, y=np.cos(x), tag='ax01', label='Cos')
    plotter.add_line(x=x, y=np.tan(x), tag='ax10', label='Tan')
    plotter.add_line(x=x, y=np.exp(x/10), tag='ax11', label='Exp')
    
    plotter.set_title('Manual Spacing Demo (Large Gaps)', tag='ax00')
    
    # Apply manual spacing: large gaps between subplots
    plotter.set_spacing(wspace=0.5, hspace=0.5)
    
    plotter.save('manual_spacing_demo.png')
    print("Saved manual_spacing_demo.png")

if __name__ == "__main__":
    demo_manual_padding()
    demo_manual_spacing()

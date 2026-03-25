
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ensure paperplot is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paperplot.core import Plotter

def verify_radial_grouped_bar():
    print("Verifying Radial Grouped Bar (Fancy)...")
    # Create proper test data with all groups for all categories
    categories = ['12-hour\nRMSE', '24-hour\nRMSE', '12-hour\nMAE', '24-hour\nMAE', '12-hour\nMAPE', '24-hour\nMAPE']
    groups = ['Proposed', 'SFLV1', 'Fed-S', 'Split', 'Local-S']
    
    data_list = []
    for cat in categories:
        for grp in groups:
            data_list.append({
                'Category': cat,
                'Group': grp,
                'Value': np.random.uniform(5, 15)
            })
    
    data = pd.DataFrame(data_list)
    
    plotter = Plotter(layout=(1, 1), ax_configs={'ax00': {'projection': 'polar'}})
    plotter.add_radial_grouped_bar(
        data=data,
        theta='Category',
        r='Value',
        hue='Group',
        tag='ax00',
        width=0.8, # Relative width
        inner_radius=3.0, # Create a hole
        alpha=0.9,
        show_grid=False # Clean look
    )
    # Add legend manually for now if needed, or rely on default
    plotter.get_ax('ax00').legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    plotter.save('tests/output_radial_grouped_bar_fancy.png')
    print("Saved tests/output_radial_grouped_bar_fancy.png")

def verify_dumbbell():
    print("Verifying Dumbbell Plot...")
    data = pd.DataFrame({
        'Model': ['M1', 'M2', 'M3', 'M4', 'M5'],
        'Score_Old': [0.5, 0.6, 0.55, 0.7, 0.65],
        'Score_New': [0.8, 0.85, 0.75, 0.9, 0.88]
    })
    
    plotter = Plotter(layout=(1, 1))
    plotter.add_dumbbell(
        data=data,
        y='Model',
        x1='Score_Old',
        x2='Score_New',
        tag='ax00',
        color1='gray',
        color2='blue',
        s=100
    )
    plotter.save('tests/output_dumbbell.png')
    print("Saved tests/output_dumbbell.png")

def verify_radar():
    print("Verifying Radar Chart...")
    data = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1', 'AUC'] * 2,
        'Model': ['Model A'] * 5 + ['Model B'] * 5,
        'Value': [0.8, 0.7, 0.9, 0.75, 0.85, 0.6, 0.65, 0.7, 0.6, 0.7]
    })
    
    plotter = Plotter(layout=(1, 1), ax_configs={'ax00': {'projection': 'polar'}})
    plotter.add_radar(
        data=data,
        theta='Metric',
        r='Value',
        hue='Model',
        tag='ax00',
        fill=True,
        alpha=0.3
    )
    plotter.save('tests/output_radar.png')
    print("Saved tests/output_radar.png")

if __name__ == "__main__":
    try:
        verify_radial_grouped_bar()
        verify_dumbbell()
        verify_radar()
        print("All verifications passed!")
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()

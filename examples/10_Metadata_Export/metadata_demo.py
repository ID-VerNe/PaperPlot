"""
Demonstrates MetadataMixin functionality for exporting layout metadata.

This example shows how to get chart layout metadata, which is the foundation
for PaperPlot Studio frontend to implement interactive annotations and 
coordinate transformations.
"""
import paperplot as pp
import pandas as pd
import numpy as np
import json


def demo_basic_metadata():
    """Basic metadata export example"""
    print("=== Basic Metadata Export ===\n")
    
    # Prepare data
    df = pd.DataFrame({
        'x': np.linspace(0, 10, 100),
        'y': np.sin(np.linspace(0, 10, 100))
    })
    
    # Create a simple plot
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 6))
    plotter.add_line(data=df, x='x', y='y', tag='ax00', label='sin(x)')
    plotter.set_title('Sine Function', tag='ax00')
    plotter.set_xlabel('x', tag='ax00')
    plotter.set_ylabel('y', tag='ax00')
    
    # Get metadata
    metadata = plotter.get_layout_metadata()
    
    # Print metadata
    print(f"Image size: {metadata['width']} x {metadata['height']} pixels")
    print(f"\nSubplot 'ax00' metadata:")
    print(f"  Position (bbox): {metadata['subplots']['ax00']['bbox']}")
    print(f"  X-axis range: {metadata['subplots']['ax00']['xlim']}")
    print(f"  Y-axis range: {metadata['subplots']['ax00']['ylim']}")
    print(f"  X-axis scale: {metadata['subplots']['ax00']['x_scale']}")
    print(f"  Y-axis scale: {metadata['subplots']['ax00']['y_scale']}")
    
    # Save plot
    plotter.save('metadata_demo_basic.png')
    print("\nSaved: metadata_demo_basic.png")


def demo_multiple_subplots():
    """Multiple subplots metadata export example"""
    print("\n\n=== Multiple Subplots Metadata Export ===\n")
    
    # Prepare data
    x = np.linspace(0, 10, 50)
    df_sin = pd.DataFrame({'x': x, 'y': np.sin(x)})
    df_cos = pd.DataFrame({'x': x, 'y': np.cos(x)})
    df_bar = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [4, 5, 6]})
    df_hist = pd.DataFrame({'value': np.random.randn(100)})
    
    # Create 2x2 grid
    plotter = pp.Plotter(layout=(2, 2), figsize=(10, 8))
    
    # Plot different chart types
    plotter.add_line(data=df_sin, x='x', y='y', tag='ax00')
    plotter.set_title('sin(x)', tag='ax00')
    
    plotter.add_scatter(data=df_cos, x='x', y='y', tag='ax01')
    plotter.set_title('cos(x)', tag='ax01')
    
    plotter.add_bar(data=df_bar, x='category', y='value', tag='ax10')
    plotter.set_title('Bar Chart', tag='ax10')
    
    plotter.add_hist(data=df_hist, x='value', tag='ax11')
    plotter.set_title('Histogram', tag='ax11')
    
    # Get metadata
    metadata = plotter.get_layout_metadata()
    
    print(f"Number of subplots: {len(metadata['subplots'])}")
    print(f"Subplot tags: {list(metadata['subplots'].keys())}\n")
    
    # Print position info for each subplot
    for tag, subplot_meta in metadata['subplots'].items():
        bbox = subplot_meta['bbox']
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        print(f"{tag}: position={bbox[:2]}, size={width:.1f}x{height:.1f}")
    
    plotter.save('metadata_demo_grid.png')
    print("\nSaved: metadata_demo_grid.png")


def demo_mosaic_layout():
    """Mosaic layout metadata export example"""
    print("\n\n=== Mosaic Layout Metadata Export ===\n")
    
    layout = [
        ['A', 'A', 'B'],
        ['A', 'A', 'C']
    ]
    
    # Prepare data
    x = np.linspace(0, 10, 100)
    df_main = pd.DataFrame({'x': x, 'y': np.sin(x)})
    df_aux1 = pd.DataFrame({'x': x[::10], 'y': np.cos(x[::10])})
    df_aux2 = pd.DataFrame({'category': ['X', 'Y', 'Z'], 'value': [2, 4, 3]})
    
    plotter = pp.Plotter(layout=layout, figsize=(12, 6))
    
    # Main plot (A) - spans multiple cells
    plotter.add_line(data=df_main, x='x', y='y', tag='A', label='Main curve')
    plotter.set_title('Main Plot (Spans 4 Cells)', tag='A')
    
    # Auxiliary plots (B and C)
    plotter.add_scatter(data=df_aux1, x='x', y='y', tag='B')
    plotter.set_title('Auxiliary B', tag='B')
    
    plotter.add_bar(data=df_aux2, x='category', y='value', tag='C')
    plotter.set_title('Auxiliary C', tag='C')
    
    # Get metadata
    metadata = plotter.get_layout_metadata()
    
    # Compare subplot areas
    for tag in ['A', 'B', 'C']:
        bbox = metadata['subplots'][tag]['bbox']
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        print(f"{tag}: area = {area:.0f} square pixels")
    
    plotter.save('metadata_demo_mosaic.png')
    print("\nSaved: metadata_demo_mosaic.png")


def demo_nested_layout():
    """Nested layout metadata export example using declarative syntax"""
    print("\n\n=== Nested Layout Metadata Export ===\n")
    
    # Declarative nested layout using 'main' and 'subgrids'
    nested_layout = {
        'main': [
            ['main_plot', 'side_group']
        ],
        'subgrids': {
            'side_group': {
                'layout': [
                    ['top_plot', 'top_plot'],
                    ['bottom_left', 'bottom_right']
                ],
                'hspace': 0.3
            }
        },
        'col_ratios': [2, 1]
    }
    
    # Prepare data
    x = np.linspace(0, 10, 100)
    df_main = pd.DataFrame({'x': x, 'y': np.sin(x)})
    df_top = pd.DataFrame({'x': x[::10], 'y': np.cos(x[::10])})
    df_bl = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [2, 4, 3]})
    df_br = pd.DataFrame({'value': np.random.randn(100)})
    
    plotter = pp.Plotter(layout=nested_layout, figsize=(14, 6))
    
    # Main plot (left side)
    plotter.add_line(data=df_main, x='x', y='y', label='sin(x)', tag='main_plot')
    plotter.set_title('Main Plot: sin(x)', tag='main_plot')
    plotter.set_xlabel('x', tag='main_plot')
    plotter.set_ylabel('y', tag='main_plot')
    
    # Side group plots (right side)
    plotter.add_scatter(data=df_top, x='x', y='y', label='cos(x)', tag='side_group.top_plot')
    plotter.set_title('Side Top: cos(x)', tag='side_group.top_plot')
    
    plotter.add_bar(data=df_bl, x='category', y='value', tag='side_group.bottom_left')
    plotter.set_title('Side Bottom Left', tag='side_group.bottom_left')
    
    plotter.add_hist(data=df_br, x='value', tag='side_group.bottom_right')
    plotter.set_title('Side Bottom Right', tag='side_group.bottom_right')
    
    # Get metadata
    metadata = plotter.get_layout_metadata()
    
    print(f"Number of subplots: {len(metadata['subplots'])}")
    print(f"Nested subplot tags:")
    for tag in metadata['subplots'].keys():
        print(f"  - {tag}")
    
    plotter.save('metadata_demo_nested.png')
    print("\nSaved: metadata_demo_nested.png")


def demo_coordinate_transformation():
    """Coordinate transformation example: simulate frontend interaction"""
    print("\n\n=== Coordinate Transformation Example ===\n")
    
    # Prepare data
    x = np.linspace(0, 10, 100)
    df = pd.DataFrame({'x': x, 'y': x ** 2})
    
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 6))
    plotter.add_line(data=df, x='x', y='y', tag='ax00')
    plotter.set_title('y = x^2', tag='ax00')
    plotter.set_xlabel('x', tag='ax00')
    plotter.set_ylabel('y', tag='ax00')
    
    # Get metadata
    metadata = plotter.get_layout_metadata()
    
    # Simulate: user clicks somewhere on the image (pixel coordinates)
    # Assume clicking at the center of the image
    click_x_pixel = metadata['width'] / 2
    click_y_pixel = metadata['height'] / 2
    
    print(f"User click position (pixels): ({click_x_pixel:.0f}, {click_y_pixel:.0f})")
    
    # Convert pixel coordinates to data coordinates
    subplot = metadata['subplots']['ax00']
    bbox = subplot['bbox']
    xlim = subplot['xlim']
    ylim = subplot['ylim']
    
    # Calculate relative position (0-1)
    ratio_x = (click_x_pixel - bbox[0]) / (bbox[2] - bbox[0])
    ratio_y = ((metadata['height'] - click_y_pixel) - bbox[1]) / (bbox[3] - bbox[1])
    
    # Map to data range
    data_x = xlim[0] + ratio_x * (xlim[1] - xlim[0])
    data_y = ylim[0] + ratio_y * (ylim[1] - ylim[0])
    
    print(f"Corresponding data coordinates: ({data_x:.2f}, {data_y:.2f})")
    print(f"\nThis is how the frontend converts user clicks to data coordinates!")
    
    plotter.save('metadata_demo_transform.png')
    print("\nSaved: metadata_demo_transform.png")


def demo_export_to_json():
    """Export metadata to JSON (simulating API response)"""
    print("\n\n=== Export JSON Format Metadata ===\n")
    
    # Prepare data
    x = np.linspace(0, 10, 50)
    df_sin = pd.DataFrame({'x': x, 'y': np.sin(x)})
    df_cos = pd.DataFrame({'x': x, 'y': np.cos(x)})
    
    plotter = pp.Plotter(layout=(1, 2), figsize=(12, 5))
    
    plotter.add_line(data=df_sin, x='x', y='y', tag='ax00')
    plotter.set_title('sin(x)', tag='ax00')
    
    plotter.add_scatter(data=df_cos, x='x', y='y', tag='ax01')
    plotter.set_title('cos(x)', tag='ax01')
    
    # Get metadata
    metadata = plotter.get_layout_metadata()
    
    # Convert to JSON string
    json_str = json.dumps(metadata, indent=2)
    
    print("Metadata in JSON format:")
    print(json_str)
    
    # Save to file
    with open('metadata_export.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    print("\nSaved: metadata_export.json")
    plotter.save('metadata_demo_json.png')


if __name__ == '__main__':
    demo_basic_metadata()
    demo_multiple_subplots()
    demo_mosaic_layout()
    demo_nested_layout()
    demo_coordinate_transformation()
    demo_export_to_json()
    
    print("\n\n=== All Demos Completed ===")
    print("Generated files:")
    print("  - metadata_demo_basic.png")
    print("  - metadata_demo_grid.png")
    print("  - metadata_demo_mosaic.png")
    print("  - metadata_demo_nested.png")
    print("  - metadata_demo_transform.png")
    print("  - metadata_demo_json.png")
    print("  - metadata_export.json")

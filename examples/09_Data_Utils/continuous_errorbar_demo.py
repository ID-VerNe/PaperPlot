
import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Create continuous data with uneven spacing
    # Dose response: 0, 10, 100, 1000
    doses = [0, 10, 100, 1000]
    data = []
    for d in doses:
        # Generate 5 replicates per dose
        vals = np.random.normal(loc=np.log1p(d), scale=0.5, size=5)
        for v in vals:
            data.append({'Dose': d, 'Response': v})
    
    df = pd.DataFrame(data)

    print("Generating Continuous ErrorBar Plot...")
    
    (
        pp.Plotter(layout=(1, 2), figsize=(12, 5))
        
        # Left: Default behavior (Categorical=True)
        # This treats 0, 10, 100, 1000 as equal steps
        .add_errorbar_from_raw(
            data=df, 
            x='Dose', 
            y='Response', 
            categorical=True, 
            plot_type='line',
            tag=0
        )
        .set_title("Categorical X-Axis (Equal Spacing)")
        .set_xlabel("Dose (treated as category)")
        
        # Right: New behavior (Categorical=False)
        # This treats X as continuous values
        .add_errorbar_from_raw(
            data=df, 
            x='Dose', 
            y='Response', 
            categorical=False, 
            plot_type='line',
            tag=1
        )
        .set_title("Continuous X-Axis (Proportional Spacing)")
        .set_xlabel("Dose (Numeric)")
        .log_scale(axis='x') # Log scale makes sense for this data
        
        .save("examples/09_Data_Utils/continuous_errorbar_demo.png")
    )
    print("Saved examples/09_Data_Utils/continuous_errorbar_demo.png")

if __name__ == "__main__":
    main()

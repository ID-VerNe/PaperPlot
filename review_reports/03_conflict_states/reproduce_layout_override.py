import paperplot as pp
import matplotlib.pyplot as plt

try:
    print("Step 1: Create Plotter")
    # default layout_engine='constrained'
    plotter = pp.Plotter(layout=(2, 2))
    
    # Check default params (constrained layout uses None params until draw time, but let's see)
    # Actually, let's just use manual padding first.
    
    print("Step 2: Set manual padding")
    # This disables the engine and sets subplot params
    target_left = 0.2
    plotter.set_padding(left=target_left)
    
    # Verify the setting took effect
    current_left = plotter.fig.subplotpars.left
    print(f"Current left padding: {current_left}")
    
    if abs(current_left - target_left) > 0.001:
        print("WARNING: set_padding failed to apply correctly!")
    else:
        print("SUCCESS: set_padding applied correctly.")
        
    print("Step 3: Call tight_layout() (Simulating user action or external library)")
    # This should override the manual padding
    plotter.fig.tight_layout()
    
    new_left = plotter.fig.subplotpars.left
    print(f"New left padding after tight_layout: {new_left}")
    
    if abs(new_left - target_left) > 0.001:
        print("CRITICAL: Manual padding was silently overridden by tight_layout()!")
        print("Expected behavior: Library should warn or prevent this if manual mode is active.")
    else:
        print("SUCCESS: Manual padding persisted (unexpected but good).")

except Exception as e:
    print(f"Error: {e}")

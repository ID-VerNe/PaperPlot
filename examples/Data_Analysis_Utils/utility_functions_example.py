# examples/utility_functions_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---

# SERS 光谱数据
x_spec = np.linspace(400, 1800, 1000)
y_spec = (0.8 * np.exp(-((x_spec - 600)**2) / (2 * 30**2)) + 
          0.6 * np.exp(-((x_spec - 1200)**2) / (2 * 50**2)) +
          np.random.rand(1000) * 0.1)
spectra_df = pd.DataFrame({'wavenumber': x_spec, 'intensity': y_spec})
peaks_to_highlight = [600, 1200]


# 时间序列数据
time = np.linspace(0, 100, 200)
signal = np.sin(time / 10) * np.exp(time / 50) + np.random.randn(200) * 0.1
timeseries_df = pd.DataFrame({'time': time, 'signal': signal})
event_points = [25, 50, 80]
event_labels = ['Fault', 'Clear', 'Load Shed']


# --- 2. 创建一个 1x2 的布局并使用新API绘图 ---
try:
    (
        pp.Plotter(layout=(1, 2), figsize=(12, 5))
        .set_suptitle("Utility Functions Demonstration (New API)", fontsize=16, weight='bold')

        # --- 左侧子图: 高亮光谱峰 ---
        .add_line(data=spectra_df, x='wavenumber', y='intensity', tag='spectra')
        .add_peak_highlights(
            peaks_x=peaks_to_highlight,
            x_col='wavenumber',
            y_col='intensity',
            label_positions={1200: (1250, 0.4)}, # 手动将1200峰的标签移动到右下方
            ha='center' # 水平居中
        )
        .set_title('add_peak_highlights() Example')
        .set_xlabel('Wavenumber (cm⁻¹)')
        .set_ylabel('Intensity (a.u.)')

        # --- 右侧子图: 标记时间序列事件 ---
        .add_line(data=timeseries_df, x='time', y='signal', tag='timeseries', color='navy')
        .add_event_markers(
            event_dates=event_points,
            labels=event_labels,
            label_positions={25: (15, 2.5)} # 手动移动 'Fault' 标签
        )
        .set_title('add_event_markers() Example')
        .set_xlabel('Time (s)')
        .set_ylabel('Signal Value')

        # --- 清理和保存 ---
        .cleanup(align_labels=True)
        .save("utility_functions_example.png")
    )

except (pp.PaperPlotError, ValueError) as e:
    print(f"\nAn error occurred:\n{e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    # import traceback
    # traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'utility_functions_example.png' was generated with the new API.")

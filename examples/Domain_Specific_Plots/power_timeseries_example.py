# examples/power_timeseries_example.py

import paperplot as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# --- 1. 准备数据 ---
# 模拟一个电力系统动态过程
np.random.seed(0)
time = np.linspace(0, 5, 500)
# 基础信号
base_signal = 0.98 + 0.02 * np.sin(time * 5)
# 故障期间的电压跌落
fault_dip = -0.5 * (np.exp(-(time - 1.1)**2 / 0.01))
# 故障切除后的恢复振荡
recovery_oscillation = 0.05 * np.sin((time - 1.2) * 20) * np.exp(-(time - 1.2) / 1.5)

# 信号组合
voltage = base_signal + fault_dip + recovery_oscillation
frequency = 60 - 0.5 * (np.exp(-(time - 1.1)**2 / 0.02)) + 0.1 * np.sin((time - 1.2) * 15) * np.exp(-(time - 1.2))

df = pd.DataFrame({
    'time': time,
    'Voltage (p.u.)': voltage,
    'Frequency (Hz)': frequency
})

# 定义事件
events = {
    'Fault On': 1.0,
    'Fault Cleared': 1.2
}

# --- 2. 创建绘图 (使用新API) ---
try:
    (
        pp.Plotter(layout=(1, 1), figsize=(8, 5))
        # 使用新的 add_power_timeseries 方法
        .add_power_timeseries(
            data=df,
            x='time',
            y_cols=['Voltage (p.u.)', 'Frequency (Hz)'], # 这里我们把两个不同单位的信号画在一起了，仅为演示
            events=events
        )
        # 链式调用修饰器，无需tag
        .set_title('Power System Dynamic Simulation')
        .set_ylabel('Value') # 保持通用标签
        .cleanup()
        .save("power_timeseries_example.png")
    )

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'power_timeseries_example.png' was generated.")

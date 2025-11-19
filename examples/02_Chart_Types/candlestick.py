import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import paperplot as pp
import pandas as pd
import matplotlib.pyplot as plt

print(f"--- Running Example: {__file__} ---")

# 数据准备
df_kline = pd.DataFrame({
    't': ['t1', 't2', 't3', 't4'],
    'open': [10, 12, 11, 13],
    'high': [12, 13, 12, 14],
    'low': [9, 11, 10, 12],
    'close': [11, 11, 12, 12]
})

try:
    # 创建单个子图
    plotter = pp.Plotter(layout=(1, 1), figsize=(8, 5))
    
    plotter.set_suptitle("Candlestick Chart (K-Line)", fontsize=16, weight='bold')
    
    # K线图
    plotter.add_candlestick(
        data=df_kline, time='t', open='open', high='high', low='low', close='close'
    ).set_title('Candlestick Chart'
    ).set_xlabel('Time'
    ).set_ylabel('Price')
    
    # 保存
    plotter.cleanup()
    plotter.save("candlestick_example.png")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    plt.close('all')

print(f"\n--- Finished Example: {__file__} ---")
print("A new file 'candlestick_example.png' was generated.")

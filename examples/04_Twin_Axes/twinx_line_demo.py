import pandas as pd
import numpy as np
import paperplot as pp

def main():
    """演示一键式双轴绘图 (add_twinx_line)。"""
    print("--- Running Example: twinx_line_demo.py ---")
    
    # 准备数据
    time = np.linspace(0, 10, 100)
    temp = 20 + 5 * np.sin(time)
    humidity = 60 + 20 * np.cos(time)
    
    df = pd.DataFrame({'Time': time, 'Temperature': temp, 'Humidity': humidity})
    
    # 1. 创建 Plotter
    plotter = pp.Plotter(layout=(1, 1), style='publication', figsize=(8, 5))
    
    # 2. 链式绘制双 Y 轴
    # .add_line 绘制主轴（Temperature）
    # .add_twinx_line 一步完成：创建孪生轴 -> 切换上下文 -> 绘制湿度（Humidity）
    plotter.add_line(data=df, x='Time', y='Temperature', label='Temperature (°C)') \
           .add_twinx_line(data=df, x='Time', y='Humidity', label='Humidity (%)', color='orange') \
           .set_ylabel("Humidity (%)") \
           .target_primary() \
           .set_xlabel("Time (s)") \
           .set_ylabel("Temperature (°C)") \
           .set_title("Chained Dual-Axis Plotting") \
           .set_legend(loc='upper right')
           
    # 注意：set_legend 能够自动合并主轴和孪生轴的图例项
    
    # 3. 手动调整间距（演示集成的 set_padding）
    plotter.set_padding(left=0.15, right=0.85, top=0.9, bottom=0.15)
    
    output_path = 'twinx_line_example.png'
    plotter.save(output_path)
    
    print(f"A new file '{output_path}' was generated.")
    print("--- Finished Example: twinx_line_demo.py ---")

if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
import paperplot as pp

def generate_mock_data():
    """生成包含重复实验的原始数据。"""
    epochs = np.arange(1, 11)
    models = ['ResNet-18', 'ViT-Tiny', 'MobileNet-V2']
    
    data_list = []
    for model in models:
        # 每个模型有 5 次重复实验
        for run in range(5):
            # 基础精度
            base_acc = 0.7 if model == 'ResNet-18' else 0.65 if model == 'ViT-Tiny' else 0.6
            # 随 epoch 增长，带随机噪声
            acc = base_acc + 0.02 * epochs + np.random.normal(0, 0.03, len(epochs))
            
            run_df = pd.DataFrame({
                'Epoch': epochs,
                'Accuracy': acc,
                'Model': model,
                'Run': run
            })
            data_list.append(run_df)
            
    return pd.concat(data_list, ignore_index=True)

def main():
    df = generate_mock_data()
    
    print("--- Running Example: add_errorbar_from_raw_demo.py ---")
    
    # 1. 创建 Plotter，使用 yelan 主题
    plotter = pp.Plotter(layout=(1, 2), style='yelan', figsize=(12, 5))
    
    # 2. 在左子图绘制线图模式 (默认)
    # 自动计算均值和标准误 (sem)
    plotter.add_errorbar_from_raw(
        data=df, x='Epoch', y='Accuracy', hue='Model',
        error_type='sem', plot_type='line', capsize=3,
        tag='ax00'
    ).set_title("Line Mode (with SEM)")
    
    # 3. 在右子图绘制柱状图模式
    # 自动计算均值和标准差 (std)
    # 我们只取 Epoch 1, 5, 10 进行对比
    df_subset = df[df['Epoch'].isin([1, 5, 10])]
    plotter.add_errorbar_from_raw(
        data=df_subset, x='Epoch', y='Accuracy', hue='Model',
        error_type='std', plot_type='bar', capsize=4,
        tag='ax01'
    ).set_title("Bar Mode (with STD)")
    
    # 4. 收尾
    plotter.add_global_legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=3)
    plotter.cleanup(align_labels=True)
    
    output_path = 'add_errorbar_from_raw_example.png'
    plotter.save(output_path)
    print(f"A new file '{output_path}' was generated.")
    print("--- Finished Example: add_errorbar_from_raw_demo.py ---")

if __name__ == "__main__":
    main()

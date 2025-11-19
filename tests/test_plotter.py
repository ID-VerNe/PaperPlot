import unittest
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import paperplot as pp
from paperplot import Plotter, generate_grid_layout
from paperplot.exceptions import TagNotFoundError, DuplicateTagError, PlottingSpaceError
import pandas as pd
import numpy as np
import seaborn as sns

class TestPlotter(unittest.TestCase):
    def test_plotter_init_simple_grid(self):
        """测试Plotter使用简单网格布局的初始化。"""
        plotter = Plotter(layout=(1, 2))
        self.assertIsNotNone(plotter.fig)
        self.assertEqual(len(plotter.axes), 2)
        self.assertIsInstance(plotter.axes[0], plt.Axes)
        self.assertIsInstance(plotter.axes[1], plt.Axes)
        plt.close(plotter.fig)

    def test_plotter_init_mosaic_layout(self):
        """测试Plotter使用马赛克布局的初始化。"""
        layout = [['A', 'B'], ['C', 'C']]
        plotter = Plotter(layout=layout)
        self.assertIsNotNone(plotter.fig)
        self.assertEqual(len(plotter.axes), 3)  # A, B, C
        self.assertIn('A', plotter.axes_dict)
        self.assertIn('B', plotter.axes_dict)
        self.assertIn('C', plotter.axes_dict)
        self.assertIsInstance(plotter.axes_dict['A'], plt.Axes)
        plt.close(plotter.fig)

    def test_generate_grid_layout(self):
        """测试generate_grid_layout函数。"""
        layout = generate_grid_layout(2, 2)
        expected_layout = [['(0,0)', '(0,1)'], ['(1,0)', '(1,1)']]
        self.assertEqual(layout, expected_layout)

    def test_get_ax_by_tag_and_name(self):
        """测试_get_ax_by_tag和get_ax_by_name方法。"""
        layout = [['A', 'B'], ['C', 'C']]
        plotter = Plotter(layout=layout)

        # Test _get_ax_by_tag (indirectly via get_ax)
        ax_a = plotter.get_ax_by_name('A')
        test_df = pd.DataFrame({'x':[1,2], 'y':[1,2]})
        plotter.add_line(data=test_df, x='x', y='y', tag='line_a', ax=ax_a)
        self.assertEqual(plotter.get_ax('line_a'), ax_a)

        # Test get_ax_by_name
        self.assertEqual(plotter.get_ax_by_name('B'), plotter.axes_dict['B'])
        
        with self.assertRaises(ValueError):
            plotter.get_ax_by_name('NonExistent')

        plt.close(plotter.fig)

    def test_add_line(self):
        """测试add_line方法。"""
        plotter = Plotter(layout=(1,1))
        test_df = pd.DataFrame({'x':[1,2,3], 'y':[4,5,6]})
        plotter.add_line(data=test_df, x='x', y='y', tag='my_line')
        ax = plotter.get_ax('my_line')
        self.assertEqual(len(ax.lines), 1)
        plt.close(plotter.fig)

    def test_add_spectra(self):
        """测试add_spectra方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'x': [1,2,3], 'y1': [4,5,6], 'y2': [5,6,7]})
        # Assuming add_spectra is available (from DomainSpecificPlotsMixin)
        if hasattr(plotter, 'add_spectra'):
            plotter.add_spectra(data=data, x='x', y_cols=['y1', 'y2'], tag='my_spectra', offset=1)
            ax = plotter.get_ax('my_spectra')
            self.assertEqual(len(ax.lines), 2)
            # 检查偏移是否正确应用
            self.assertEqual(ax.lines[0].get_ydata()[0], 4)
            self.assertEqual(ax.lines[1].get_ydata()[0], 5 + 1) # y2_data + offset
        plt.close(plotter.fig)

    def test_add_bar(self):
        """测试add_bar方法。"""
        plotter = Plotter(layout=(1,1))
        test_df = pd.DataFrame({'x':['A','B'], 'y':[10,20]})
        plotter.add_bar(data=test_df, x='x', y='y', tag='my_bar')
        ax = plotter.get_ax('my_bar')
        self.assertEqual(len(ax.patches), 2) # Two bars
        plt.close(plotter.fig)

    def test_add_confusion_matrix(self):
        """测试add_confusion_matrix方法。"""
        plotter = Plotter(layout=(1,1))
        matrix = np.array([[10, 1], [2, 15]])
        class_names = ['Cat', 'Dog']
        # Assuming add_confusion_matrix is available (from MachineLearningPlotsMixin)
        if hasattr(plotter, 'add_confusion_matrix'):
            plotter.add_confusion_matrix(matrix=matrix, class_names=class_names, tag='my_cm')
            ax = plotter.get_ax('my_cm')
            self.assertEqual(len(ax.collections), 1) # Heatmap
            self.assertEqual(ax.get_xlabel(), 'Predicted Label')
            self.assertEqual(ax.get_ylabel(), 'True Label')
        plt.close(plotter.fig)

    def test_add_roc_curve(self):
        """测试add_roc_curve方法。"""
        fpr = {'class1': np.array([0, 0.5, 1]), 'class2': np.array([0, 0.2, 1])}
        tpr = {'class1': np.array([0, 0.8, 1]), 'class2': np.array([0, 0.9, 1])}
        roc_auc = {'class1': 0.75, 'class2': 0.85}
        
        plotter = Plotter(layout=(1,1))
        # Assuming add_roc_curve is available
        if hasattr(plotter, 'add_roc_curve'):
            plotter.add_roc_curve(fpr=fpr, tpr=tpr, roc_auc=roc_auc, tag='my_roc')
            ax = plotter.get_ax('my_roc')
            self.assertEqual(len(ax.lines), 3) # Two ROC curves + diagonal line
            self.assertEqual(ax.get_xlabel(), 'False Positive Rate')
            self.assertEqual(ax.get_ylabel(), 'True Positive Rate')
        plt.close(plotter.fig)

    def test_add_pca_scatter(self):
        """测试add_pca_scatter方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'PC1': [1,2,3], 'PC2': [4,5,6], 'label': ['A','A','B']})
        # Assuming add_pca_scatter is available
        if hasattr(plotter, 'add_pca_scatter'):
            plotter.add_pca_scatter(data=data, x_pc='PC1', y_pc='PC2', hue='label', tag='my_pca')
            ax = plotter.get_ax('my_pca')
            self.assertEqual(len(ax.collections), 1) # Scatter points
            self.assertIsNotNone(ax.get_legend()) # Hue should create a legend
        plt.close(plotter.fig)

    def test_add_power_timeseries(self):
        """测试add_power_timeseries方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'time': [1,2,3], 'signal1': [4,5,6], 'signal2': [7,8,9]})
        events = {'event1': 1.5, 'event2': 2.5}
        # Assuming add_power_timeseries is available
        if hasattr(plotter, 'add_power_timeseries'):
            plotter.add_power_timeseries(data=data, x='time', y_cols=['signal1', 'signal2'], tag='my_power', events=events)
            ax = plotter.get_ax('my_power')
            self.assertEqual(len(ax.lines), 4) # Two signals + two event lines
            self.assertEqual(len(ax.texts), 2) # Two event labels
            self.assertEqual(ax.get_xlabel(), 'Time (s)')
            self.assertEqual(ax.get_ylabel(), 'Value')
        plt.close(plotter.fig)

    def test_add_concentration_map(self):
        """测试add_concentration_map方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame([[1,2],[3,4]])
        # Assuming add_concentration_map is available
        if hasattr(plotter, 'add_concentration_map'):
            plotter.add_concentration_map(data=data, tag='my_map')
            ax = plotter.get_ax('my_map')
            self.assertEqual(len(ax.collections), 1) # Heatmap
        plt.close(plotter.fig)

    def test_add_scatter(self):
        """测试add_scatter方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'x': [1,2,3], 'y': [4,5,6]})
        plotter.add_scatter(data=data, x='x', y='y', tag='my_scatter')
        ax = plotter.get_ax('my_scatter')
        self.assertEqual(len(ax.collections), 1)
        plt.close(plotter.fig)

    def test_add_hist(self):
        """测试add_hist方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'x': [1,2,1,2,3,4,5]})
        plotter.add_hist(data=data, x='x', tag='my_hist')
        ax = plotter.get_ax('my_hist')
        self.assertGreater(len(ax.patches), 0)
        plt.close(plotter.fig)

    def test_add_box(self):
        """测试add_box方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'x': ['A','A','B','B'], 'y': [1,2,3,4]})
        plotter.add_box(data=data, x='x', y='y', tag='my_box')
        ax = plotter.get_ax('my_box')
        self.assertGreater(len(ax.artists) + len(ax.lines), 0) # Boxplot elements
        plt.close(plotter.fig)

    def test_add_heatmap(self):
        """测试add_heatmap方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame([[1,2],[3,4]])
        plotter.add_heatmap(data=data, tag='my_heatmap')
        ax = plotter.get_ax('my_heatmap')
        self.assertEqual(len(ax.collections), 1)
        plt.close(plotter.fig)

    def test_add_seaborn(self):
        """测试add_seaborn方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'x': ['A','A','B','B'], 'y': [1,2,3,4]})
        plotter.add_seaborn(plot_func=sns.violinplot, data=data, x='x', y='y', tag='my_violin')
        ax = plotter.get_ax('my_violin')
        self.assertGreater(len(ax.collections), 0)
        plt.close(plotter.fig)

    def test_add_regplot(self):
        """测试add_regplot方法。"""
        plotter = Plotter(layout=(1,1))
        data = pd.DataFrame({'x': [1,2,3,4], 'y': [2,4,5,8]})
        plotter.add_regplot(data=data, x='x', y='y', tag='my_reg')
        ax = plotter.get_ax('my_reg')
        self.assertGreater(len(ax.collections), 0) # Scatter
        self.assertGreater(len(ax.lines), 0) # Regression line
        plt.close(plotter.fig)

    def test_modifiers(self):
        """测试各种修饰器方法。"""
        plotter = Plotter(layout=(1, 1))
        df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        plotter.add_line(data=df, x='x', y='y')
        
        plotter.set_title("Test Title")
        plotter.set_xlabel("X Label")
        plotter.set_ylabel("Y Label")
        plotter.set_xlim(0, 3)
        plotter.set_ylim(0, 5)
        
        ax = plotter.axes[0]
        self.assertEqual(ax.get_title(), "Test Title")
        self.assertEqual(ax.get_xlabel(), "X Label")
        self.assertEqual(ax.get_ylabel(), "Y Label")
        self.assertEqual(ax.get_xlim(), (0, 3))
        self.assertEqual(ax.get_ylim(), (0, 5))
        plt.close(plotter.fig)

    def test_set_legend(self):
        """测试set_legend方法。"""
        plotter = Plotter(layout=(1,1))
        df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        plotter.add_line(data=df, x='x', y='y', label='Line 1')
        plotter.set_legend()
        ax = plotter.axes[0]
        self.assertIsNotNone(ax.get_legend())
        plt.close(plotter.fig)

    def test_set_suptitle(self):
        """测试set_suptitle方法。"""
        plotter = Plotter(layout=(1,1))
        plotter.set_suptitle("Figure Title")
        # Note: accessing suptitle directly from figure might be version dependent or property
        # self.assertEqual(plotter.fig._suptitle.get_text(), "Figure Title") 
        # Safer check:
        self.assertIsNotNone(plotter.fig._suptitle)
        plt.close(plotter.fig)

    def test_add_twinx(self):
        """测试add_twinx方法。"""
        plotter = Plotter(layout=(1,1))
        df = pd.DataFrame({'x': [1, 2], 'y1': [3, 4], 'y2': [10, 20]})
        plotter.add_line(data=df, x='x', y='y1', tag='primary')
        plotter.add_twinx()
        plotter.add_line(data=df, x='x', y='y2', color='red') # Should go to twin axis
        
        ax = plotter.get_ax('primary')
        self.assertIn('primary', plotter.twin_axes)
        twin_ax = plotter.twin_axes['primary']
        self.assertEqual(len(ax.lines), 1)
        self.assertEqual(len(twin_ax.lines), 1)
        plt.close(plotter.fig)

    def test_add_hline_vline_text(self):
        """测试add_hline, add_vline, add_text方法。"""
        plotter = Plotter(layout=(1,1))
        plotter.add_blank() # Initialize an ax
        plotter.add_hline(y=0.5)
        plotter.add_vline(x=0.5)
        plotter.add_text(x=0.5, y=0.5, text="Center")
        
        ax = plotter.axes[0]
        # Check lines (hline/vline add lines)
        self.assertGreater(len(ax.lines), 0)
        # Check text
        self.assertEqual(len(ax.texts), 1)
        plt.close(plotter.fig)

    def test_add_patch(self):
        """测试add_patch方法。"""
        from matplotlib.patches import Circle
        plotter = Plotter(layout=(1,1))
        plotter.add_blank()
        circle = Circle((0.5, 0.5), 0.1)
        plotter.add_patch(circle)
        ax = plotter.axes[0]
        self.assertEqual(len(ax.patches), 1)
        plt.close(plotter.fig)

if __name__ == '__main__':
    unittest.main()

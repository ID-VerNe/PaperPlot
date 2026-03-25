"""
测试 MetadataMixin 的功能
"""
import unittest
import numpy as np
from paperplot import Plotter


class TestMetadataMixin(unittest.TestCase):
    """测试元数据导出功能"""
    
    def test_get_layout_metadata_basic(self):
        """测试基础元数据导出"""
        plotter = Plotter(layout=(1, 1), figsize=(8, 6))
        plotter.add_line(x=[1, 2, 3], y=[4, 5, 6], tag='ax00')
        
        # 获取元数据
        metadata = plotter.get_layout_metadata()
        
        # 验证基本结构
        self.assertIn('width', metadata)
        self.assertIn('height', metadata)
        self.assertIn('subplots', metadata)
        
        # 验证尺寸
        self.assertIsInstance(metadata['width'], int)
        self.assertIsInstance(metadata['height'], int)
        self.assertGreater(metadata['width'], 0)
        self.assertGreater(metadata['height'], 0)
    
    def test_subplot_metadata_structure(self):
        """测试子图元数据结构"""
        plotter = Plotter(layout=(2, 2))
        plotter.add_scatter(x=[1, 2], y=[3, 4], tag='ax00')
        
        metadata = plotter.get_layout_metadata()
        
        # 验证子图存在
        self.assertIn('ax00', metadata['subplots'])
        
        subplot = metadata['subplots']['ax00']
        
        # 验证必需字段
        self.assertIn('bbox', subplot)
        self.assertIn('xlim', subplot)
        self.assertIn('ylim', subplot)
        self.assertIn('x_scale', subplot)
        self.assertIn('y_scale', subplot)
        
        # 验证 bbox 格式 [left, bottom, right, top]
        bbox = subplot['bbox']
        self.assertEqual(len(bbox), 4)
        self.assertLess(bbox[0], bbox[2])  # left < right
        self.assertLess(bbox[1], bbox[3])  # bottom < top
        
        # 验证数据范围格式
        self.assertEqual(len(subplot['xlim']), 2)
        self.assertEqual(len(subplot['ylim']), 2)
    
    def test_multiple_subplots(self):
        """测试多子图元数据"""
        plotter = Plotter(layout=(2, 2))
        plotter.add_line(x=[1, 2], y=[3, 4], tag='ax00')
        plotter.add_line(x=[1, 2], y=[5, 6], tag='ax01')
        plotter.add_line(x=[1, 2], y=[7, 8], tag='ax10')
        plotter.add_line(x=[1, 2], y=[9, 10], tag='ax11')
        
        metadata = plotter.get_layout_metadata()
        
        # 验证所有子图都存在
        self.assertEqual(len(metadata['subplots']), 4)
        for tag in ['ax00', 'ax01', 'ax10', 'ax11']:
            self.assertIn(tag, metadata['subplots'])
    
    def test_coordinate_scales(self):
        """测试坐标系类型"""
        plotter = Plotter(layout=(1, 2))
        
        # 线性坐标系
        plotter.add_line(x=[1, 10, 100], y=[1, 2, 3], tag='ax00')
        
        # 对数坐标系
        plotter.add_line(x=[1, 10, 100], y=[1, 10, 100], tag='ax01')
        plotter.get_ax('ax01').set_xscale('log')
        plotter.get_ax('ax01').set_yscale('log')
        
        metadata = plotter.get_layout_metadata()
        
        # 验证坐标系类型
        self.assertEqual(metadata['subplots']['ax00']['x_scale'], 'linear')
        self.assertEqual(metadata['subplots']['ax00']['y_scale'], 'linear')
        self.assertEqual(metadata['subplots']['ax01']['x_scale'], 'log')
        self.assertEqual(metadata['subplots']['ax01']['y_scale'], 'log')
    
    def test_data_range_accuracy(self):
        """测试数据范围的准确性"""
        plotter = Plotter(layout=(1, 1))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plotter.add_line(x=x, y=y, tag='ax00')
        
        metadata = plotter.get_layout_metadata()
        xlim = metadata['subplots']['ax00']['xlim']
        ylim = metadata['subplots']['ax00']['ylim']
        
        # 验证范围包含数据
        self.assertLessEqual(xlim[0], 0)
        self.assertGreaterEqual(xlim[1], 10)
        self.assertLessEqual(ylim[0], -1)
        self.assertGreaterEqual(ylim[1], 1)
    
    def test_mosaic_layout(self):
        """测试马赛克布局的元数据"""
        layout = [
            ['A', 'A', 'B'],
            ['A', 'A', 'C']
        ]
        plotter = Plotter(layout=layout)
        plotter.add_line(x=[1, 2], y=[3, 4], tag='A')
        plotter.add_scatter(x=[1, 2], y=[5, 6], tag='B')
        plotter.add_bar(x=[1, 2], y=[7, 8], tag='C')
        
        metadata = plotter.get_layout_metadata()
        
        # 验证所有标签都存在
        self.assertIn('A', metadata['subplots'])
        self.assertIn('B', metadata['subplots'])
        self.assertIn('C', metadata['subplots'])
        
        # 验证 A 的 bbox 应该更大（因为跨越了多个格子）
        bbox_a = metadata['subplots']['A']['bbox']
        bbox_b = metadata['subplots']['B']['bbox']
        
        area_a = (bbox_a[2] - bbox_a[0]) * (bbox_a[3] - bbox_a[1])
        area_b = (bbox_b[2] - bbox_b[0]) * (bbox_b[3] - bbox_b[1])
        
        self.assertGreater(area_a, area_b)


if __name__ == '__main__':
    unittest.main()

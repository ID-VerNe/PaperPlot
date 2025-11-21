import unittest
import matplotlib.pyplot as plt
from paperplot import Plotter

class TestLayoutManual(unittest.TestCase):
    def setUp(self):
        self.plotter = Plotter(layout=(2, 2), layout_engine='constrained')

    def tearDown(self):
        plt.close(self.plotter.fig)

    def test_set_padding_disables_layout_engine(self):
        """Test that set_padding disables the automatic layout engine."""
        self.assertIsNotNone(self.plotter.fig.get_layout_engine())
        self.plotter.set_padding(left=0.1)
        self.assertIsNone(self.plotter.fig.get_layout_engine())

    def test_set_spacing_disables_layout_engine(self):
        """Test that set_spacing disables the automatic layout engine."""
        self.assertIsNotNone(self.plotter.fig.get_layout_engine())
        self.plotter.set_spacing(wspace=0.5)
        self.assertIsNone(self.plotter.fig.get_layout_engine())

    def test_set_padding_values(self):
        """Test that set_padding applies the correct values to subplotpars."""
        self.plotter.set_padding(left=0.15, right=0.85, top=0.9, bottom=0.1)
        
        # Check subplot parameters
        params = self.plotter.fig.subplotpars
        self.assertAlmostEqual(params.left, 0.15)
        self.assertAlmostEqual(params.right, 0.85)
        self.assertAlmostEqual(params.top, 0.9)
        self.assertAlmostEqual(params.bottom, 0.1)

    def test_set_spacing_values(self):
        """Test that set_spacing applies the correct values to subplotpars."""
        self.plotter.set_spacing(wspace=0.4, hspace=0.6)
        
        # Check subplot parameters
        params = self.plotter.fig.subplotpars
        self.assertAlmostEqual(params.wspace, 0.4)
        self.assertAlmostEqual(params.hspace, 0.6)

if __name__ == '__main__':
    unittest.main()

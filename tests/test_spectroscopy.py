import pytest
import numpy as np
import matplotlib.pyplot as plt
from paperplot import Plotter
from unittest.mock import patch, MagicMock

class TestSpectroscopyMixin:

    def setup_method(self):
        self.plotter = Plotter([['plot']])

    def test_add_peak_labels_basic(self):
        # Create dummy data with a clear peak
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        # Create plot
        self.plotter.add_line(x=x, y=y, label='Data')
        
        # Test adding peak labels
        # Mock find_peaks to return known peak indices
        # Since find_peaks is imported in spectroscopy.py, we patch it there
        with patch('paperplot.mixins.spectroscopy.find_peaks') as mock_find_peaks:
            mock_find_peaks.return_value = ([25, 75], {}) # Peaks at indices 25 and 75
            
            self.plotter.add_peak_labels(
                threshold=0.5,
                distance=10,
                font_props={'color': 'red', 'fontsize': 10}
            )
            
            # Verify find_peaks was called
            mock_find_peaks.assert_called_once()
            
            # Verify annotations were added
            # Expecting 2 annotations for the 2 peaks
            annotations = [child for child in self.plotter.axes[0].get_children() if isinstance(child, plt.Annotation)]
            # Note: matplotlib might have other annotations, but we check if count increased
            assert len(annotations) >= 2

    def test_add_bracket(self):
        self.plotter.add_line(x=[0, 1], y=[0, 1])
        
        # Add a bracket
        self.plotter.add_bracket(
            x_start=0.2,
            x_end=0.8,
            text="Region A",
            y_position=0.5,
            color='blue'
        )
        
        # Check for lines and text added to axes
        lines = self.plotter.axes[0].get_lines()
        # The plot has 1 line (data), add_bracket adds lines for the bracket shape
        # verify line count increased. add_bracket uses plot() or Line2D? 
        # Implementation likely uses self.ax.plot for lines.
        assert len(lines) > 1
        
        texts = self.plotter.axes[0].texts
        assert any(t.get_text() == "Region A" for t in texts)

    @patch('matplotlib.pyplot.imread')
    @patch('os.path.exists')
    def test_add_image_box(self, mock_exists, mock_imread):
        mock_exists.return_value = True
        # Mock image data as a simple array
        mock_imread.return_value = np.zeros((10, 10, 3))
        
        self.plotter.add_line(x=[0, 1], y=[0, 1])
        
        self.plotter.add_image_box(
            image_path='dummy.png',
            x=0.5,
            y=0.5,
            zoom=0.1
        )
        
        # Verify image was read
        mock_imread.assert_called_with('dummy.png')
        
        # Verify AnnotationBbox was added
        artists = self.plotter.axes[0].get_children()
        from matplotlib.offsetbox import AnnotationBbox
        assert any(isinstance(a, AnnotationBbox) for a in artists)

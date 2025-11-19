import unittest
import os
import matplotlib.pyplot as plt
from paperplot.styles.manager import list_themes, use_theme, theme_manager

class TestStyles(unittest.TestCase):
    def test_list_themes(self):
        themes = list_themes()
        self.assertIsInstance(themes, list)
        self.assertTrue(len(themes) > 0)
        self.assertIn('publication', themes)
        
    def test_use_theme(self):
        # Test with a known theme
        try:
            use_theme('publication')
        except Exception as e:
            self.fail(f"use_theme raised exception: {e}")
            
        # Test with an invalid theme
        with self.assertRaises(ValueError):
            use_theme('non_existent_theme_12345')
            
    def test_theme_manager_singleton(self):
        self.assertIsNotNone(theme_manager)
        self.assertTrue(os.path.exists(theme_manager.styles_dir))

if __name__ == '__main__':
    unittest.main()

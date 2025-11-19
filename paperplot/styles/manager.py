import os
import matplotlib.pyplot as plt
from typing import List, Optional

class ThemeManager:
    """Helper class to manage and list available PaperPlot styles."""
    
    def __init__(self):
        self.styles_dir = os.path.dirname(__file__)
        
    def list_themes(self) -> List[str]:
        """List all available themes in the styles directory."""
        themes = []
        for filename in os.listdir(self.styles_dir):
            if filename.endswith('.mplstyle'):
                themes.append(filename[:-9]) # Remove .mplstyle extension
        return sorted(themes)
        
    def get_theme_path(self, theme_name: str) -> Optional[str]:
        """Get the absolute path to a specific theme file."""
        theme_filename = f"{theme_name}.mplstyle"
        theme_path = os.path.join(self.styles_dir, theme_filename)
        
        if os.path.exists(theme_path):
            return theme_path
        return None
        
    def apply_theme(self, theme_name: str):
        """Apply a specific theme to matplotlib."""
        theme_path = self.get_theme_path(theme_name)
        if theme_path:
            plt.style.use(theme_path)
        else:
            raise ValueError(f"Theme '{theme_name}' not found.")

# Global instance
theme_manager = ThemeManager()

def list_themes() -> List[str]:
    return theme_manager.list_themes()

def use_theme(theme_name: str):
    theme_manager.apply_theme(theme_name)

"""
Theme management for ghdesk
"""

from ui.themes.dark import DARK_THEME
from ui.themes.light import LIGHT_THEME
from ui.themes.nord import NORD_THEME
from ui.themes.dracula import DRACULA_THEME
from ui.themes.monokai import MONOKAI_THEME

# Available themes with display names
THEMES = {
    "dark": "Dark",
    "light": "Light",
    "nord": "Nord",
    "dracula": "Dracula",
    "monokai": "Monokai"
}

# Theme stylesheet mapping
_THEME_MAP = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
    "nord": NORD_THEME,
    "dracula": DRACULA_THEME,
    "monokai": MONOKAI_THEME
}


def get_theme(name: str) -> str:
    """Get theme stylesheet by name

    Args:
        name: Theme identifier (dark, light, nord, dracula, monokai)

    Returns:
        Theme stylesheet string
    """
    return _THEME_MAP.get(name, DARK_THEME)


__all__ = [
    "THEMES",
    "get_theme",
    "DARK_THEME",
    "LIGHT_THEME",
    "NORD_THEME",
    "DRACULA_THEME",
    "MONOKAI_THEME"
]

"""
Component-specific styling constants for ghdesk
Widget styles and color constants
"""

# =============================================================================
# Color Constants for QColor
# =============================================================================

COLOR_STAGED_FILE = "#28a745"   # Green for staged files
COLOR_MODIFIED_FILE = "#ffa500"  # Orange for modified files

# =============================================================================
# Diff Viewer Colors
# =============================================================================

# Unified diff colors
COLOR_DIFF_ADDED_FG = "#98c379"      # Green text for added lines
COLOR_DIFF_ADDED_BG = "#2d3a2d"      # Dark green background
COLOR_DIFF_REMOVED_FG = "#e06c75"    # Red text for removed lines
COLOR_DIFF_REMOVED_BG = "#3a2d2d"    # Dark red background
COLOR_DIFF_HUNK_FG = "#56b6c2"       # Cyan for hunk headers (@@)
COLOR_DIFF_HEADER_FG = "#e5c07b"     # Yellow for file headers
COLOR_DIFF_META_FG = "#5c6370"       # Gray for metadata lines

# Side-by-side diff colors
COLOR_SBS_ADDED_BG = "#2d4a2d"       # Darker green for side-by-side
COLOR_SBS_REMOVED_BG = "#4a2d2d"     # Darker red for side-by-side
COLOR_SBS_EMPTY_BG = "#2a2a2a"       # Empty line placeholder
COLOR_SBS_EMPTY_FG = "#4a4a4a"       # Empty line text

# =============================================================================
# Diff Viewer Styles
# =============================================================================

STYLE_DIFF_HEADER_OLD = (
    "font-weight: bold; padding: 4px; background: #3a2d2d; color: #e06c75;"
)
STYLE_DIFF_HEADER_NEW = (
    "font-weight: bold; padding: 4px; background: #2d3a2d; color: #98c379;"
)
STYLE_DIFF_FILE_LABEL = "font-weight: bold; padding: 4px;"

# =============================================================================
# Inline Style Constants
# =============================================================================

# Font styles
STYLE_HEADER_LARGE = "font-size: 16px; font-weight: 600;"
STYLE_HEADER_MEDIUM = "font-size: 14px; font-weight: bold;"
STYLE_HEADER_SMALL = "font-size: 12px; font-weight: bold;"
STYLE_LABEL_BOLD = "font-weight: bold; padding: 5px;"
STYLE_LABEL_BOLD_SMALL = "font-weight: bold; font-size: 12px;"
STYLE_HEADER_PANEL = "font-weight: 600; font-size: 14px; padding: 8px;"

# Info/secondary text - use lighter colors for dark themes
STYLE_INFO_TEXT = "font-size: 11px; color: #b8c0cc;"
STYLE_INFO_TEXT_PADDED = "color: #b8c0cc; font-size: 11px; padding: 10px;"
STYLE_INFO_TEXT_MUTED = "color: #888; font-size: 11px;"
STYLE_DESCRIPTION = "font-size: 12px; margin-top: 8px;"
STYLE_NORMAL_TEXT = "font-size: 11px; font-weight: normal;"

# Status text styles
STYLE_SUCCESS_TEXT = "color: #2ea44f; font-weight: bold;"
STYLE_ERROR_TEXT = "color: #cf222e; font-weight: bold;"
STYLE_WARNING_TEXT = "color: #bf8700; font-weight: bold;"

# Empty state / placeholder text
STYLE_EMPTY_STATE = "color: #888; padding: 16px; font-style: italic;"
STYLE_EMPTY_STATE_SMALL = "color: #888; padding: 8px; font-style: italic;"

# Input styles
STYLE_INPUT = "padding: 4px; font-size: 12px;"
STYLE_INPUT_ERROR = "border: 1px solid #c42b1c;"
STYLE_LABEL_PADDING = "padding-right: 8px;"

# Close/hide button
STYLE_CLOSE_BUTTON = """
    QPushButton {
        background: transparent;
        border: none;
        font-size: 18px;
        color: #888;
    }
    QPushButton:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ccc;
    }
"""

# Topic badge styles
STYLE_TOPIC_BADGE = """
    QLabel {
        background: #0969da;
        color: white;
        padding: 4px 8px;
        border-top-left-radius: 12px;
        border-bottom-left-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
"""

STYLE_TOPIC_BADGE_FULL = """
    QLabel {
        background: #0969da;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
"""

STYLE_TOPIC_REMOVE_BTN = """
    QPushButton {
        background: #0550ae;
        color: white;
        border: none;
        border-top-right-radius: 12px;
        border-bottom-right-radius: 12px;
        font-size: 14px;
        font-weight: bold;
        padding: 0;
    }
    QPushButton:hover {
        background: #cf222e;
    }
"""

# Branch header styles
STYLE_BRANCH_CURRENT = """
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: #2ea44f;
        padding: 8px;
        background: rgba(46, 164, 79, 0.15);
        border-left: 4px solid #2ea44f;
    }
"""

STYLE_BRANCH_OTHER = """
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: #58a6ff;
        padding: 8px;
        background: rgba(88, 166, 255, 0.15);
        border-left: 4px solid #58a6ff;
    }
"""

# Auth status styles
STYLE_AUTH_DEFAULT = """
    background-color: transparent;
    padding: 4px 12px;
    border-radius: 4px;
    font-weight: 500;
"""

STYLE_AUTH_SUCCESS = """
    background-color: #4caf50;
    color: #ffffff;
    padding: 6px 16px;
    border-radius: 4px;
    font-weight: 600;
    border: 2px solid #388e3c;
"""

STYLE_AUTH_FAILED = """
    background-color: #f44336;
    color: #ffffff;
    padding: 6px 16px;
    border-radius: 4px;
    font-weight: 600;
    border: 2px solid #d32f2f;
"""


def get_info_box_style(color: str) -> str:
    """Generate info box style with given accent color"""
    return f"""
        QGroupBox {{
            font-weight: bold;
            font-size: 12px;
            border: 1px solid {color};
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
        }}
        QGroupBox::title {{
            color: {color};
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px;
        }}
    """

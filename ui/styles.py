"""
Modern styling for ghdesk
Theme CSS definitions
"""

DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QToolBar {
    background-color: #252526;
    border: none;
    padding: 8px;
    spacing: 8px;
}

QToolBar QToolButton {
    background-color: #2d2d30;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    padding: 8px 16px;
    color: #e0e0e0;
    font-weight: 500;
}

QToolBar QToolButton:hover {
    background-color: #3e3e42;
    border: 1px solid #007acc;
}

QToolBar QToolButton:pressed {
    background-color: #007acc;
}

QToolBar QToolButton:disabled {
    background-color: #2d2d30;
    color: #6e6e6e;
    border: 1px solid #3e3e42;
}

QTabWidget::pane {
    border: 1px solid #3e3e42;
    background-color: #252526;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #2d2d30;
    color: #b0b0b0;
    padding: 12px 24px;
    border: 1px solid #3e3e42;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #252526;
    color: #ffffff;
    border-bottom: 2px solid #007acc;
}

QTabBar::tab:hover:!selected {
    background-color: #3e3e42;
}

QTableWidget {
    background-color: #1e1e1e;
    alternate-background-color: #252526;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    gridline-color: #3e3e42;
    selection-background-color: #094771;
    selection-color: #ffffff;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:hover {
    background-color: #2d2d30;
}

QHeaderView::section {
    background-color: #2d2d30;
    color: #e0e0e0;
    padding: 10px;
    border: none;
    border-right: 1px solid #3e3e42;
    border-bottom: 1px solid #3e3e42;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #3e3e42;
}

QPushButton {
    background-color: #0e639c;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #1177bb;
}

QPushButton:pressed {
    background-color: #0d5a8f;
}

QPushButton:disabled {
    background-color: #3e3e42;
    color: #6e6e6e;
}

QPushButton#dangerButton {
    background-color: #c42b1c;
}

QPushButton#dangerButton:hover {
    background-color: #dc3c2a;
}

QPushButton#secondaryButton {
    background-color: #2d2d30;
    border: 1px solid #3e3e42;
}

QPushButton#secondaryButton:hover {
    background-color: #3e3e42;
}

QLineEdit, QTextEdit {
    background-color: #1e1e1e;
    color: #e0e0e0;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #007acc;
}

QCheckBox {
    spacing: 8px;
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #3e3e42;
    border-radius: 3px;
    background-color: #1e1e1e;
}

QCheckBox::indicator:checked {
    background-color: #007acc;
    border: 1px solid #007acc;
}

QCheckBox::indicator:hover {
    border: 1px solid #007acc;
}

QLabel {
    color: #e0e0e0;
}

QStatusBar {
    background-color: #007acc;
    color: #ffffff;
    border-top: 1px solid #005a9e;
}

QStatusBar QLabel {
    color: #ffffff;
    padding: 4px 8px;
}

QDialog {
    background-color: #1e1e1e;
}

QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 14px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #3e3e42;
    border-radius: 7px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4e4e52;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1e1e1e;
    height: 14px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #3e3e42;
    border-radius: 7px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #4e4e52;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMessageBox {
    background-color: #1e1e1e;
}

QMessageBox QPushButton {
    min-width: 60px;
    padding: 4px 8px;
}

QTreeWidget {
    background-color: #1e1e1e;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px;
    border: none;
    color: #e0e0e0;
}

QTreeWidget::item:hover {
    background-color: #2d2d30;
}

QTreeWidget::item:selected {
    background-color: #094771;
    color: #ffffff;
}

QTreeWidget::branch {
    background-color: #1e1e1e;
}

QSplitter::handle {
    background-color: #3e3e42;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #007acc;
}
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #ffffff;
}

QWidget {
    background-color: #ffffff;
    color: #1e1e1e;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QToolBar {
    background-color: #f3f3f3;
    border: none;
    padding: 8px;
    spacing: 8px;
}

QToolBar QToolButton {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 8px 16px;
    color: #1e1e1e;
    font-weight: 500;
}

QToolBar QToolButton:hover {
    background-color: #e8e8e8;
    border: 1px solid #0078d4;
}

QToolBar QToolButton:pressed {
    background-color: #0078d4;
    color: #ffffff;
}

QToolBar QToolButton:disabled {
    background-color: #f3f3f3;
    color: #a0a0a0;
    border: 1px solid #d0d0d0;
}

QTabWidget::pane {
    border: 1px solid #d0d0d0;
    background-color: #ffffff;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #f3f3f3;
    color: #6e6e6e;
    padding: 12px 24px;
    border: 1px solid #d0d0d0;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1e1e1e;
    border-bottom: 2px solid #0078d4;
}

QTabBar::tab:hover:!selected {
    background-color: #e8e8e8;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f9f9f9;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    gridline-color: #e0e0e0;
    selection-background-color: #cce8ff;
    selection-color: #1e1e1e;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:hover {
    background-color: #f0f0f0;
}

QHeaderView::section {
    background-color: #f3f3f3;
    color: #1e1e1e;
    padding: 10px;
    border: none;
    border-right: 1px solid #d0d0d0;
    border-bottom: 1px solid #d0d0d0;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #e8e8e8;
}

QPushButton {
    background-color: #0078d4;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #1084d8;
}

QPushButton:pressed {
    background-color: #006cbd;
}

QPushButton:disabled {
    background-color: #e0e0e0;
    color: #a0a0a0;
}

QPushButton#dangerButton {
    background-color: #d13438;
}

QPushButton#dangerButton:hover {
    background-color: #e04347;
}

QPushButton#secondaryButton {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    color: #1e1e1e;
}

QPushButton#secondaryButton:hover {
    background-color: #f3f3f3;
}

QLineEdit, QTextEdit {
    background-color: #ffffff;
    color: #1e1e1e;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #0078d4;
}

QCheckBox {
    spacing: 8px;
    color: #1e1e1e;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #d0d0d0;
    border-radius: 3px;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border: 1px solid #0078d4;
}

QCheckBox::indicator:hover {
    border: 1px solid #0078d4;
}

QLabel {
    color: #1e1e1e;
}

QStatusBar {
    background-color: #0078d4;
    color: #ffffff;
    border-top: 1px solid #005a9e;
}

QStatusBar QLabel {
    color: #ffffff;
    padding: 4px 8px;
}

QDialog {
    background-color: #ffffff;
}

QScrollBar:vertical {
    background-color: #f3f3f3;
    width: 14px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #c0c0c0;
    border-radius: 7px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a0a0a0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #f3f3f3;
    height: 14px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #c0c0c0;
    border-radius: 7px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #a0a0a0;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMessageBox {
    background-color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 60px;
    padding: 4px 8px;
}

QTreeWidget {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px;
    border: none;
    color: #1e1e1e;
}

QTreeWidget::item:hover {
    background-color: #f0f0f0;
}

QTreeWidget::item:selected {
    background-color: #cce8ff;
    color: #1e1e1e;
}

QTreeWidget::branch {
    background-color: #ffffff;
}

QSplitter::handle {
    background-color: #d0d0d0;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #0078d4;
}
"""

# =============================================================================
# Color Constants for QColor
# =============================================================================

COLOR_STAGED_FILE = "#28a745"   # Green for staged files
COLOR_MODIFIED_FILE = "#ffa500"  # Orange for modified files

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

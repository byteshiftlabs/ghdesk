"""
Additional themes for ghdesk
"""

THEMES = {
    "dark": "Dark",
    "light": "Light",
    "nord": "Nord",
    "dracula": "Dracula",
    "monokai": "Monokai"
}

NORD_THEME = """
QMainWindow {
    background-color: #2e3440;
}

QWidget {
    background-color: #2e3440;
    color: #eceff4;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QToolBar {
    background-color: #3b4252;
    border: none;
    padding: 8px;
    spacing: 8px;
}

QToolBar QToolButton {
    background-color: #434c5e;
    border: 1px solid #4c566a;
    border-radius: 4px;
    padding: 8px 16px;
    color: #eceff4;
    font-weight: 500;
}

QToolBar QToolButton:hover {
    background-color: #4c566a;
    border: 1px solid #88c0d0;
}

QToolBar QToolButton:pressed {
    background-color: #88c0d0;
}

QToolBar QToolButton:disabled {
    background-color: #434c5e;
    color: #4c566a;
    border: 1px solid #4c566a;
}

QTabWidget::pane {
    border: 1px solid #4c566a;
    background-color: #3b4252;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #434c5e;
    color: #d8dee9;
    padding: 12px 24px;
    border: 1px solid #4c566a;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #3b4252;
    color: #eceff4;
    border-bottom: 2px solid #88c0d0;
}

QTabBar::tab:hover:!selected {
    background-color: #4c566a;
}

QTableWidget {
    background-color: #2e3440;
    alternate-background-color: #3b4252;
    border: 1px solid #4c566a;
    border-radius: 4px;
    gridline-color: #4c566a;
    selection-background-color: #5e81ac;
    selection-color: #eceff4;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:hover {
    background-color: #434c5e;
}

QHeaderView::section {
    background-color: #434c5e;
    color: #eceff4;
    padding: 10px;
    border: none;
    border-right: 1px solid #4c566a;
    border-bottom: 1px solid #4c566a;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #4c566a;
}

QPushButton {
    background-color: #5e81ac;
    color: #eceff4;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #81a1c1;
}

QPushButton:pressed {
    background-color: #4c566a;
}

QPushButton:disabled {
    background-color: #4c566a;
    color: #616e88;
}

QPushButton#dangerButton {
    background-color: #bf616a;
}

QPushButton#dangerButton:hover {
    background-color: #d08770;
}

QPushButton#secondaryButton {
    background-color: #434c5e;
    border: 1px solid #4c566a;
}

QPushButton#secondaryButton:hover {
    background-color: #4c566a;
}

QLineEdit, QTextEdit {
    background-color: #2e3440;
    color: #eceff4;
    border: 1px solid #4c566a;
    border-radius: 4px;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #88c0d0;
}

QCheckBox {
    spacing: 8px;
    color: #eceff4;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #4c566a;
    border-radius: 3px;
    background-color: #2e3440;
}

QCheckBox::indicator:checked {
    background-color: #88c0d0;
    border: 1px solid #88c0d0;
}

QCheckBox::indicator:hover {
    border: 1px solid #88c0d0;
}

QLabel {
    color: #eceff4;
}

QStatusBar {
    background-color: #5e81ac;
    color: #eceff4;
    border-top: 1px solid #4c566a;
}

QStatusBar QLabel {
    color: #eceff4;
    padding: 4px 8px;
}

QDialog {
    background-color: #2e3440;
}

QScrollBar:vertical {
    background-color: #2e3440;
    width: 14px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #4c566a;
    border-radius: 7px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #616e88;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #2e3440;
    height: 14px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #4c566a;
    border-radius: 7px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #616e88;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMessageBox {
    background-color: #2e3440;
}

QMessageBox QPushButton {
    min-width: 60px;
    padding: 4px 8px;
}

QTreeWidget {
    background-color: #2e3440;
    border: 1px solid #4c566a;
    border-radius: 4px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px;
    border: none;
    color: #eceff4;
}

QTreeWidget::item:hover {
    background-color: #434c5e;
}

QTreeWidget::item:selected {
    background-color: #5e81ac;
    color: #eceff4;
}

QTreeWidget::branch {
    background-color: #2e3440;
}

QSplitter::handle {
    background-color: #4c566a;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #88c0d0;
}

QComboBox {
    background-color: #434c5e;
    color: #eceff4;
    border: 1px solid #4c566a;
    border-radius: 4px;
    padding: 6px 12px;
}

QComboBox:hover {
    border: 1px solid #88c0d0;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #434c5e;
    color: #eceff4;
    selection-background-color: #5e81ac;
}
"""

DRACULA_THEME = """
QMainWindow {
    background-color: #282a36;
}

QWidget {
    background-color: #282a36;
    color: #f8f8f2;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QToolBar {
    background-color: #44475a;
    border: none;
    padding: 8px;
    spacing: 8px;
}

QToolBar QToolButton {
    background-color: #44475a;
    border: 1px solid #6272a4;
    border-radius: 4px;
    padding: 8px 16px;
    color: #f8f8f2;
    font-weight: 500;
}

QToolBar QToolButton:hover {
    background-color: #6272a4;
    border: 1px solid #bd93f9;
}

QToolBar QToolButton:pressed {
    background-color: #bd93f9;
}

QToolBar QToolButton:disabled {
    background-color: #44475a;
    color: #6272a4;
    border: 1px solid #6272a4;
}

QTabWidget::pane {
    border: 1px solid #6272a4;
    background-color: #44475a;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #44475a;
    color: #f8f8f2;
    padding: 12px 24px;
    border: 1px solid #6272a4;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #282a36;
    color: #f8f8f2;
    border-bottom: 2px solid #bd93f9;
}

QTabBar::tab:hover:!selected {
    background-color: #6272a4;
}

QTableWidget {
    background-color: #282a36;
    alternate-background-color: #44475a;
    border: 1px solid #6272a4;
    border-radius: 4px;
    gridline-color: #6272a4;
    selection-background-color: #bd93f9;
    selection-color: #282a36;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:hover {
    background-color: #44475a;
}

QHeaderView::section {
    background-color: #44475a;
    color: #f8f8f2;
    padding: 10px;
    border: none;
    border-right: 1px solid #6272a4;
    border-bottom: 1px solid #6272a4;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #6272a4;
}

QPushButton {
    background-color: #bd93f9;
    color: #282a36;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #ff79c6;
}

QPushButton:pressed {
    background-color: #8be9fd;
}

QPushButton:disabled {
    background-color: #6272a4;
    color: #44475a;
}

QPushButton#dangerButton {
    background-color: #ff5555;
}

QPushButton#dangerButton:hover {
    background-color: #ff6e6e;
}

QPushButton#secondaryButton {
    background-color: #44475a;
    border: 1px solid #6272a4;
    color: #f8f8f2;
}

QPushButton#secondaryButton:hover {
    background-color: #6272a4;
}

QLineEdit, QTextEdit {
    background-color: #282a36;
    color: #f8f8f2;
    border: 1px solid #6272a4;
    border-radius: 4px;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #bd93f9;
}

QCheckBox {
    spacing: 8px;
    color: #f8f8f2;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #6272a4;
    border-radius: 3px;
    background-color: #282a36;
}

QCheckBox::indicator:checked {
    background-color: #bd93f9;
    border: 1px solid #bd93f9;
}

QCheckBox::indicator:hover {
    border: 1px solid #bd93f9;
}

QLabel {
    color: #f8f8f2;
}

QStatusBar {
    background-color: #bd93f9;
    color: #282a36;
    border-top: 1px solid #6272a4;
}

QStatusBar QLabel {
    color: #282a36;
    padding: 4px 8px;
}

QDialog {
    background-color: #282a36;
}

QScrollBar:vertical {
    background-color: #282a36;
    width: 14px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #6272a4;
    border-radius: 7px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #bd93f9;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #282a36;
    height: 14px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #6272a4;
    border-radius: 7px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #bd93f9;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMessageBox {
    background-color: #282a36;
}

QMessageBox QPushButton {
    min-width: 60px;
    padding: 4px 8px;
}

QTreeWidget {
    background-color: #282a36;
    border: 1px solid #6272a4;
    border-radius: 4px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px;
    border: none;
    color: #f8f8f2;
}

QTreeWidget::item:hover {
    background-color: #44475a;
}

QTreeWidget::item:selected {
    background-color: #bd93f9;
    color: #282a36;
}

QTreeWidget::branch {
    background-color: #282a36;
}

QSplitter::handle {
    background-color: #6272a4;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #bd93f9;
}

QComboBox {
    background-color: #44475a;
    color: #f8f8f2;
    border: 1px solid #6272a4;
    border-radius: 4px;
    padding: 6px 12px;
}

QComboBox:hover {
    border: 1px solid #bd93f9;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #44475a;
    color: #f8f8f2;
    selection-background-color: #bd93f9;
}
"""

MONOKAI_THEME = """
QMainWindow {
    background-color: #272822;
}

QWidget {
    background-color: #272822;
    color: #f8f8f2;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QToolBar {
    background-color: #3e3d32;
    border: none;
    padding: 8px;
    spacing: 8px;
}

QToolBar QToolButton {
    background-color: #49483e;
    border: 1px solid #75715e;
    border-radius: 4px;
    padding: 8px 16px;
    color: #f8f8f2;
    font-weight: 500;
}

QToolBar QToolButton:hover {
    background-color: #75715e;
    border: 1px solid #66d9ef;
}

QToolBar QToolButton:pressed {
    background-color: #66d9ef;
    color: #272822;
}

QToolBar QToolButton:disabled {
    background-color: #49483e;
    color: #75715e;
    border: 1px solid #75715e;
}

QTabWidget::pane {
    border: 1px solid #75715e;
    background-color: #3e3d32;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #49483e;
    color: #f8f8f2;
    padding: 12px 24px;
    border: 1px solid #75715e;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #272822;
    color: #f8f8f2;
    border-bottom: 2px solid #a6e22e;
}

QTabBar::tab:hover:!selected {
    background-color: #75715e;
}

QTableWidget {
    background-color: #272822;
    alternate-background-color: #3e3d32;
    border: 1px solid #75715e;
    border-radius: 4px;
    gridline-color: #75715e;
    selection-background-color: #49483e;
    selection-color: #a6e22e;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:hover {
    background-color: #49483e;
}

QHeaderView::section {
    background-color: #49483e;
    color: #f8f8f2;
    padding: 10px;
    border: none;
    border-right: 1px solid #75715e;
    border-bottom: 1px solid #75715e;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #75715e;
}

QPushButton {
    background-color: #a6e22e;
    color: #272822;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #b8e447;
}

QPushButton:pressed {
    background-color: #8dc221;
}

QPushButton:disabled {
    background-color: #75715e;
    color: #49483e;
}

QPushButton#dangerButton {
    background-color: #f92672;
}

QPushButton#dangerButton:hover {
    background-color: #ff3d85;
}

QPushButton#secondaryButton {
    background-color: #49483e;
    border: 1px solid #75715e;
    color: #f8f8f2;
}

QPushButton#secondaryButton:hover {
    background-color: #75715e;
}

QLineEdit, QTextEdit {
    background-color: #272822;
    color: #f8f8f2;
    border: 1px solid #75715e;
    border-radius: 4px;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #66d9ef;
}

QCheckBox {
    spacing: 8px;
    color: #f8f8f2;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #75715e;
    border-radius: 3px;
    background-color: #272822;
}

QCheckBox::indicator:checked {
    background-color: #a6e22e;
    border: 1px solid #a6e22e;
}

QCheckBox::indicator:hover {
    border: 1px solid #a6e22e;
}

QLabel {
    color: #f8f8f2;
}

QStatusBar {
    background-color: #a6e22e;
    color: #272822;
    border-top: 1px solid #75715e;
}

QStatusBar QLabel {
    color: #272822;
    padding: 4px 8px;
}

QDialog {
    background-color: #272822;
}

QScrollBar:vertical {
    background-color: #272822;
    width: 14px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #75715e;
    border-radius: 7px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a6e22e;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #272822;
    height: 14px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #75715e;
    border-radius: 7px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #a6e22e;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMessageBox {
    background-color: #272822;
}

QMessageBox QPushButton {
    min-width: 60px;
    padding: 4px 8px;
}

QTreeWidget {
    background-color: #272822;
    border: 1px solid #75715e;
    border-radius: 4px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px;
    border: none;
    color: #f8f8f2;
}

QTreeWidget::item:hover {
    background-color: #49483e;
}

QTreeWidget::item:selected {
    background-color: #49483e;
    color: #a6e22e;
}

QTreeWidget::branch {
    background-color: #272822;
}

QSplitter::handle {
    background-color: #75715e;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #a6e22e;
}

QComboBox {
    background-color: #49483e;
    color: #f8f8f2;
    border: 1px solid #75715e;
    border-radius: 4px;
    padding: 6px 12px;
}

QComboBox:hover {
    border: 1px solid #66d9ef;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #49483e;
    color: #f8f8f2;
    selection-background-color: #75715e;
}
"""

def get_theme(name: str) -> str:
    """Get theme stylesheet by name"""
    from ui.styles import DARK_THEME, LIGHT_THEME
    
    themes_map = {
        "dark": DARK_THEME,
        "light": LIGHT_THEME,
        "nord": NORD_THEME,
        "dracula": DRACULA_THEME,
        "monokai": MONOKAI_THEME
    }
    
    return themes_map.get(name, DARK_THEME)

"""
Nord theme stylesheet for ghdesk
"""

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

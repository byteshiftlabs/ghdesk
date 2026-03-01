"""
Light theme stylesheet for ghdesk
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

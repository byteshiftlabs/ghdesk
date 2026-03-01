"""
Dracula theme stylesheet for ghdesk
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

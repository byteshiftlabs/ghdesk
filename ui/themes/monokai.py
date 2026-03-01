"""
Monokai theme stylesheet for ghdesk
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

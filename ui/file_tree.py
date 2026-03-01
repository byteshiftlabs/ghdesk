"""
Filesystem tree view widget
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles import STYLE_HEADER_PANEL, STYLE_INPUT_ERROR
from ui.constants import MARGIN_NONE


class FileTreeWidget(QWidget):
    """Widget displaying filesystem tree"""

    directory_selected = pyqtSignal(str)  # Emitted when a directory is selected

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.populate_root()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
        self.setLayout(layout)

        # Header
        header = QLabel("Filesystem")
        header.setStyleSheet(STYLE_HEADER_PANEL)
        layout.addWidget(header)

        # Path input
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Enter path to navigate...")
        self.path_input.returnPressed.connect(self.navigate_to_path)
        layout.addWidget(self.path_input)

        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.tree.itemExpanded.connect(self.on_item_expanded)
        layout.addWidget(self.tree)

    def populate_root(self):
        """Populate root directories"""
        self.tree.clear()

        # Add home directory only (don't expose root filesystem)
        home = str(Path.home())
        home_item = self.create_tree_item("Home", home)
        self.tree.addTopLevelItem(home_item)
        self.add_placeholder(home_item)

        # Expand home directory by default
        home_item.setExpanded(True)

    def create_tree_item(self, text: str, path: str) -> QTreeWidgetItem:
        """Create a tree item with stored path"""
        item = QTreeWidgetItem([text])
        item.setData(0, Qt.ItemDataRole.UserRole, path)
        return item

    def add_placeholder(self, parent: QTreeWidgetItem):
        """Add placeholder child to enable expansion arrow"""
        placeholder = QTreeWidgetItem([""])
        parent.addChild(placeholder)

    def on_item_expanded(self, item: QTreeWidgetItem):
        """Handle item expansion"""
        # Remove placeholder and populate real children
        if item.childCount() == 1 and item.child(0).text(0) == "":
            item.removeChild(item.child(0))
            self.populate_children(item)

    def populate_children(self, parent: QTreeWidgetItem):
        """Populate children of a directory"""
        path = parent.data(0, Qt.ItemDataRole.UserRole)

        try:
            path_obj = Path(path)
            if not path_obj.exists() or not path_obj.is_dir():
                return

            # Get directories only, sorted
            directories = []
            try:
                for entry in sorted(path_obj.iterdir()):
                    if entry.is_dir() and not entry.name.startswith('.'):
                        directories.append(entry)
            except PermissionError:
                return

            # Add directories to tree
            for directory in directories:
                icon = "[D]"

                # Check if it's a git repo
                if (directory / ".git").exists():
                    icon = "[R]"

                item = self.create_tree_item(f"{icon} {directory.name}", str(directory))
                parent.addChild(item)

                # Add placeholder to show expansion arrow
                self.add_placeholder(item)

        except Exception as e:
            # Silently handle errors (permission denied, etc.)
            pass

    def on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item click"""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path:
            self.path_input.setText(path)
            self.directory_selected.emit(path)

    def navigate_to_path(self):
        """Navigate to the path entered in the input field"""
        path = self.path_input.text().strip()
        if not path:
            return

        path_obj = Path(path).expanduser().resolve()
        if path_obj.exists() and path_obj.is_dir():
            self.directory_selected.emit(str(path_obj))
            # Could expand the tree to show this path, but that's complex
            # For now, just emit the signal
        else:
            self.path_input.setStyleSheet(STYLE_INPUT_ERROR)
            # Reset style after a delay would be nice, but keep it simple for now

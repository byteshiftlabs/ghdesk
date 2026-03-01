"""
Filesystem tree view widget
"""

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
        self.tree.setRootIsDecorated(True)
        self.tree.setIndentation(20)
        self.tree.setAnimated(True)
        self.tree.setExpandsOnDoubleClick(True)
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.tree.itemExpanded.connect(self.on_item_expanded)
        self.tree.itemCollapsed.connect(self.on_item_collapsed)
        layout.addWidget(self.tree)

    def populate_root(self):
        """Populate root directories starting from project's parent directory"""
        self.tree.clear()

        # Start from the project's parent directory
        project_dir = Path(__file__).resolve().parent.parent  # ui/ -> ghdesk/
        start_dir = project_dir.parent  # ghdesk/ -> parent
        
        # Create root item for the starting directory
        root_item = self.create_tree_item(f"▼ {start_dir.name}", str(start_dir), expandable=True)
        self.tree.addTopLevelItem(root_item)
        
        # Populate children immediately (expanded by default)
        self.populate_children(root_item)
        root_item.setExpanded(True)

    def create_tree_item(self, text: str, path: str, expandable: bool = False) -> QTreeWidgetItem:
        """Create a tree item with stored path"""
        item = QTreeWidgetItem([text])
        item.setData(0, Qt.ItemDataRole.UserRole, path)
        item.setData(0, Qt.ItemDataRole.UserRole + 1, expandable)  # Store if expandable
        return item

    def add_placeholder(self, parent: QTreeWidgetItem):
        """Add placeholder child to enable expansion arrow"""
        placeholder = QTreeWidgetItem([""])
        parent.addChild(placeholder)

    def on_item_expanded(self, item: QTreeWidgetItem):
        """Handle item expansion"""
        # Update arrow indicator
        text = item.text(0)
        if text.startswith("▶"):
            item.setText(0, "▼" + text[1:])
        
        # Remove placeholder and populate real children
        if item.childCount() == 1 and item.child(0).text(0) == "":
            item.removeChild(item.child(0))
            self.populate_children(item)
            
            # If directory is empty, add placeholder back so it can still collapse
            if item.childCount() == 0:
                self.add_placeholder(item)

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

                item = self.create_tree_item(f"▶ {icon} {directory.name}", str(directory), expandable=True)
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
        
        # Toggle expand/collapse on click for expandable items
        expandable = item.data(0, Qt.ItemDataRole.UserRole + 1)
        if expandable:
            item.setExpanded(not item.isExpanded())

    def on_item_collapsed(self, item: QTreeWidgetItem):
        """Handle item collapse - update arrow indicator"""
        text = item.text(0)
        if text.startswith("▼"):
            item.setText(0, "▶" + text[1:])

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

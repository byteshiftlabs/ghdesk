"""
Pull Request list widget
Displays PRs for a repository with filtering options
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QComboBox, QLineEdit, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import Optional, Dict, Any

from core.gh_wrapper import GHWrapper
from ui.constants import (
    PR_LIST_FILTER_SPACING,
    PR_LIST_AUTHOR_FILTER_WIDTH,
    PR_LIST_REFRESH_BUTTON_WIDTH,
)


class PRListWidget(QWidget):
    """Widget for displaying and filtering pull requests"""
    
    pr_selected = pyqtSignal(int)  # Emits PR number when selected
    pr_refresh_requested = pyqtSignal()
    
    def __init__(self, gh: GHWrapper, repo_name: str, parent=None):
        super().__init__(parent)
        
        self.gh = gh
        self.repo_name = repo_name
        self.prs = []
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self.setLayout(layout)
        
        # Filter bar
        filter_bar = self.create_filter_bar()
        layout.addWidget(filter_bar)
        
        # PR list
        self.pr_list = QListWidget()
        self.pr_list.itemClicked.connect(self.on_pr_clicked)
        layout.addWidget(self.pr_list)
        
        # Load PRs
        self.load_prs()
    
    def create_filter_bar(self) -> QFrame:
        """Create the filter bar with state and author filters"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        frame.setLayout(layout)
        
        # State filter
        layout.addWidget(QLabel("State:"))
        self.state_combo = QComboBox()
        self.state_combo.addItems(["Open", "Closed", "Merged", "All"])
        self.state_combo.currentTextChanged.connect(self.on_filter_changed)
        layout.addWidget(self.state_combo)
        
        layout.addSpacing(PR_LIST_FILTER_SPACING)
        
        # Author filter
        layout.addWidget(QLabel("Author:"))
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Filter by username...")
        self.author_edit.setMaximumWidth(PR_LIST_AUTHOR_FILTER_WIDTH)
        self.author_edit.textChanged.connect(self.on_filter_changed)
        layout.addWidget(self.author_edit)
        
        layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("↻ Refresh")
        refresh_btn.setMaximumWidth(PR_LIST_REFRESH_BUTTON_WIDTH)
        refresh_btn.clicked.connect(self.load_prs)
        layout.addWidget(refresh_btn)
        
        return frame
    
    def on_filter_changed(self):
        """Handle filter changes"""
        self.load_prs()
    
    def load_prs(self):
        """Load pull requests from GitHub"""
        self.pr_list.clear()
        self.prs = []
        
        # Get filter values
        state_map = {
            "Open": "open",
            "Closed": "closed",
            "Merged": "merged",
            "All": "all"
        }
        state = state_map[self.state_combo.currentText()]
        author = self.author_edit.text().strip() or None
        
        # Fetch PRs
        result = self.gh.list_prs(self.repo_name, state=state, author=author)
        
        if not result["success"]:
            item = QListWidgetItem("Failed to load pull requests")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.pr_list.addItem(item)
            return
        
        prs = result.get("output", [])
        
        if not prs:
            item = QListWidgetItem("No pull requests found")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.pr_list.addItem(item)
            return
        
        # Add PRs to list
        for pr in prs:
            self.add_pr_item(pr)
            self.prs.append(pr)
    
    def add_pr_item(self, pr: Dict[str, Any]):
        """Add a PR item to the list"""
        number = pr.get("number", 0)
        title = pr.get("title", "Untitled")
        state = pr.get("state", "OPEN")
        author = pr.get("author", {}).get("login", "unknown")
        is_draft = pr.get("isDraft", False)
        head_ref = pr.get("headRefName", "")
        base_ref = pr.get("baseRefName", "")
        
        # Format state indicator
        state_indicators = {
            "OPEN": "🟢",
            "CLOSED": "🔴",
            "MERGED": "🟣"
        }
        indicator = state_indicators.get(state, "⚪")
        
        draft_text = " [DRAFT]" if is_draft else ""
        
        # Create item text
        item_text = f"{indicator} #{number} {title}{draft_text}"
        secondary_text = f"   by {author} • {head_ref} → {base_ref}"
        
        item = QListWidgetItem(item_text + "\n" + secondary_text)
        item.setData(Qt.ItemDataRole.UserRole, number)
        
        # Style based on state
        font = QFont()
        if is_draft:
            font.setItalic(True)
        item.setFont(font)
        
        self.pr_list.addItem(item)
    
    def on_pr_clicked(self, item: QListWidgetItem):
        """Handle PR item click"""
        pr_number = item.data(Qt.ItemDataRole.UserRole)
        if pr_number:
            self.pr_selected.emit(pr_number)
    
    def get_selected_pr_number(self) -> Optional[int]:
        """Get the currently selected PR number"""
        current_item = self.pr_list.currentItem()
        if current_item:
            return current_item.data(Qt.ItemDataRole.UserRole)
        return None

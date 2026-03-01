"""
Pull Request list widget.
Displays PRs for a repository with filtering options.
"""

from typing import List, Dict, Any

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QLabel, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal

from core.logging_config import get_logger
from ui.styles import STYLE_INFO_TEXT_MUTED
from ui.constants import MARGIN_SMALL, SPACING_MEDIUM, BUTTON_MIN_WIDTH_SMALL

logger = get_logger("ui.pr_list_widget")

# Table column indices
COL_NUMBER = 0
COL_TITLE = 1
COL_AUTHOR = 2
COL_BRANCH = 3
COL_STATUS = 4


class PRListWidget(QWidget):
    """Widget for displaying and filtering pull requests."""

    # Emits PR number when selected
    pr_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.prs: List[Dict[str, Any]] = []
        self.repo_name: str = ""
        self.gh = None
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(MARGIN_SMALL, MARGIN_SMALL, MARGIN_SMALL, MARGIN_SMALL)
        layout.setSpacing(SPACING_MEDIUM)
        self.setLayout(layout)

        # Filter bar
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(SPACING_MEDIUM)

        filter_label = QLabel("State:")
        filter_layout.addWidget(filter_label)

        self.state_combo = QComboBox()
        self.state_combo.addItems(["Open", "Closed", "All"])
        self.state_combo.currentIndexChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.state_combo)

        filter_layout.addStretch()

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setMinimumWidth(BUTTON_MIN_WIDTH_SMALL)
        self.refresh_btn.clicked.connect(self._on_refresh)
        filter_layout.addWidget(self.refresh_btn)

        layout.addLayout(filter_layout)

        # PR table
        self.pr_table = QTableWidget()
        self.pr_table.setColumnCount(5)
        self.pr_table.setHorizontalHeaderLabels(["#", "Title", "Author", "Branch", "Status"])
        self.pr_table.horizontalHeader().setStretchLastSection(True)
        self.pr_table.horizontalHeader().setSectionResizeMode(
            COL_TITLE, QHeaderView.ResizeMode.Stretch
        )
        self.pr_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.pr_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.pr_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.pr_table.itemSelectionChanged.connect(self._on_selection_changed)

        # Column widths
        self.pr_table.setColumnWidth(COL_NUMBER, 50)
        self.pr_table.setColumnWidth(COL_AUTHOR, 100)
        self.pr_table.setColumnWidth(COL_BRANCH, 150)
        self.pr_table.setColumnWidth(COL_STATUS, 80)

        layout.addWidget(self.pr_table)

        # Empty state
        self.empty_label = QLabel("No pull requests found")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(STYLE_INFO_TEXT_MUTED)
        self.empty_label.hide()
        layout.addWidget(self.empty_label)

    def set_gh_wrapper(self, gh):
        """Set the GitHub wrapper instance."""
        self.gh = gh

    def set_repo(self, repo_name: str):
        """Set the repository and load PRs."""
        self.repo_name = repo_name
        self.load_prs()

    def load_prs(self):
        """Load pull requests from GitHub."""
        if not self.gh or not self.repo_name:
            return

        state_map = {"Open": "open", "Closed": "closed", "All": "all"}
        state = state_map.get(self.state_combo.currentText(), "open")

        logger.debug("Loading PRs for %s with state=%s", self.repo_name, state)
        self.prs = self.gh.list_prs(repo=self.repo_name, state=state)
        self._update_table()

    def _update_table(self):
        """Update the table with current PR data."""
        self.pr_table.setRowCount(0)

        if not self.prs:
            self.pr_table.hide()
            self.empty_label.show()
            return

        self.empty_label.hide()
        self.pr_table.show()
        self.pr_table.setRowCount(len(self.prs))

        for row, pr in enumerate(self.prs):
            # Number
            number_item = QTableWidgetItem(f"#{pr.get('number', '')}")
            number_item.setData(Qt.ItemDataRole.UserRole, pr.get("number"))
            self.pr_table.setItem(row, COL_NUMBER, number_item)

            # Title (with draft indicator)
            title = pr.get("title", "")
            if pr.get("isDraft"):
                title = f"[Draft] {title}"
            self.pr_table.setItem(row, COL_TITLE, QTableWidgetItem(title))

            # Author
            author = pr.get("author", {})
            author_name = author.get("login", "") if isinstance(author, dict) else str(author)
            self.pr_table.setItem(row, COL_AUTHOR, QTableWidgetItem(author_name))

            # Branch
            head_ref = pr.get("headRefName", "")
            self.pr_table.setItem(row, COL_BRANCH, QTableWidgetItem(head_ref))

            # Status
            state = pr.get("state", "").upper()
            status_item = QTableWidgetItem(state)
            if state == "OPEN":
                status_item.setForeground(Qt.GlobalColor.green)
            elif state == "MERGED":
                status_item.setForeground(Qt.GlobalColor.magenta)
            elif state == "CLOSED":
                status_item.setForeground(Qt.GlobalColor.red)
            self.pr_table.setItem(row, COL_STATUS, status_item)

    def _on_filter_changed(self):
        """Handle filter combo change."""
        self.load_prs()

    def _on_refresh(self):
        """Handle refresh button click."""
        self.load_prs()

    def _on_selection_changed(self):
        """Handle table selection change."""
        selected = self.pr_table.selectedItems()
        if selected:
            row = selected[0].row()
            number_item = self.pr_table.item(row, COL_NUMBER)
            if number_item:
                pr_number = number_item.data(Qt.ItemDataRole.UserRole)
                if pr_number:
                    self.pr_selected.emit(pr_number)

    def clear(self):
        """Clear the widget."""
        self.prs = []
        self.repo_name = ""
        self.pr_table.setRowCount(0)
        self.empty_label.hide()

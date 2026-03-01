"""
Pull Request detail view.
Shows detailed information about a specific pull request.
"""

from typing import Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QFrame, QGroupBox, QFormLayout,
    QMessageBox, QInputDialog, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from core.logging_config import get_logger
from ui.styles import (
    STYLE_HEADER_LARGE, STYLE_INFO_TEXT_MUTED,
    STYLE_SUCCESS_TEXT, STYLE_ERROR_TEXT, STYLE_WARNING_TEXT
)
from ui.constants import (
    MARGIN_MEDIUM, SPACING_SMALL, SPACING_MEDIUM,
    BUTTON_MIN_WIDTH_MEDIUM
)

logger = get_logger("ui.pr_detail_view")


class PRDetailView(QWidget):
    """Widget for displaying pull request details."""

    # Emitted when PR state changes (merged, closed, reopened)
    pr_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gh = None
        self.repo_name: str = ""
        self.pr_number: Optional[int] = None
        self.pr_data: Dict[str, Any] = {}
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM)
        layout.setSpacing(SPACING_MEDIUM)
        self.setLayout(layout)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll)

        # Content widget
        content = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(SPACING_MEDIUM)
        content.setLayout(self.content_layout)
        scroll.setWidget(content)

        # Header section
        self._create_header_section()

        # Info section
        self._create_info_section()

        # Description section
        self._create_description_section()

        # Stats section
        self._create_stats_section()

        # Actions section
        self._create_actions_section()

        # Comments section
        self._create_comments_section()

        self.content_layout.addStretch()

        # Placeholder
        self._show_placeholder()

    def _create_header_section(self):
        """Create the PR header with title and state."""
        self.header_frame = QFrame()
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(SPACING_SMALL)
        self.header_frame.setLayout(header_layout)

        # Title
        self.title_label = QLabel()
        self.title_label.setStyleSheet(STYLE_HEADER_LARGE)
        self.title_label.setWordWrap(True)
        header_layout.addWidget(self.title_label)

        # State and author row
        state_row = QHBoxLayout()
        self.state_label = QLabel()
        state_row.addWidget(self.state_label)

        self.author_label = QLabel()
        self.author_label.setStyleSheet(STYLE_INFO_TEXT_MUTED)
        state_row.addWidget(self.author_label)

        state_row.addStretch()
        header_layout.addLayout(state_row)

        self.content_layout.addWidget(self.header_frame)

    def _create_info_section(self):
        """Create the branch and merge info section."""
        self.info_group = QGroupBox("Branch Info")
        info_layout = QFormLayout()
        self.info_group.setLayout(info_layout)

        self.branch_label = QLabel()
        info_layout.addRow("Branches:", self.branch_label)

        self.mergeable_label = QLabel()
        info_layout.addRow("Mergeable:", self.mergeable_label)

        self.content_layout.addWidget(self.info_group)

    def _create_description_section(self):
        """Create the description section."""
        self.desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout()
        self.desc_group.setLayout(desc_layout)

        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(150)
        desc_layout.addWidget(self.description_text)

        self.content_layout.addWidget(self.desc_group)

    def _create_stats_section(self):
        """Create the stats section."""
        self.stats_group = QGroupBox("Changes")
        stats_layout = QHBoxLayout()
        self.stats_group.setLayout(stats_layout)

        self.additions_label = QLabel()
        self.additions_label.setStyleSheet(STYLE_SUCCESS_TEXT)
        stats_layout.addWidget(self.additions_label)

        self.deletions_label = QLabel()
        self.deletions_label.setStyleSheet(STYLE_ERROR_TEXT)
        stats_layout.addWidget(self.deletions_label)

        self.files_label = QLabel()
        stats_layout.addWidget(self.files_label)

        stats_layout.addStretch()
        self.content_layout.addWidget(self.stats_group)

    def _create_actions_section(self):
        """Create the actions section."""
        self.actions_frame = QFrame()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, SPACING_MEDIUM, 0, 0)
        self.actions_frame.setLayout(actions_layout)

        # Merge button with method selector
        self.merge_method = QComboBox()
        self.merge_method.addItems(["Merge", "Squash", "Rebase"])
        self.merge_method.setMinimumWidth(80)
        actions_layout.addWidget(self.merge_method)

        self.merge_btn = QPushButton("Merge PR")
        self.merge_btn.setMinimumWidth(BUTTON_MIN_WIDTH_MEDIUM)
        self.merge_btn.clicked.connect(self._on_merge)
        actions_layout.addWidget(self.merge_btn)

        # Close/Reopen button
        self.close_btn = QPushButton("Close PR")
        self.close_btn.setMinimumWidth(BUTTON_MIN_WIDTH_MEDIUM)
        self.close_btn.clicked.connect(self._on_close)
        actions_layout.addWidget(self.close_btn)

        # Comment button
        self.comment_btn = QPushButton("Add Comment")
        self.comment_btn.setMinimumWidth(BUTTON_MIN_WIDTH_MEDIUM)
        self.comment_btn.clicked.connect(self._on_add_comment)
        actions_layout.addWidget(self.comment_btn)

        # View diff button
        self.diff_btn = QPushButton("View Diff")
        self.diff_btn.setMinimumWidth(BUTTON_MIN_WIDTH_MEDIUM)
        self.diff_btn.clicked.connect(self._on_view_diff)
        actions_layout.addWidget(self.diff_btn)

        # Side-by-side diff button
        self.sbs_diff_btn = QPushButton("Side-by-Side")
        self.sbs_diff_btn.setMinimumWidth(BUTTON_MIN_WIDTH_MEDIUM)
        self.sbs_diff_btn.clicked.connect(self._on_view_sbs_diff)
        actions_layout.addWidget(self.sbs_diff_btn)

        actions_layout.addStretch()
        self.content_layout.addWidget(self.actions_frame)

    def _create_comments_section(self):
        """Create the comments section."""
        self.comments_group = QGroupBox("Comments")
        comments_layout = QVBoxLayout()
        self.comments_group.setLayout(comments_layout)

        self.comments_text = QTextEdit()
        self.comments_text.setReadOnly(True)
        self.comments_text.setMaximumHeight(200)
        comments_layout.addWidget(self.comments_text)

        self.content_layout.addWidget(self.comments_group)

    def _show_placeholder(self):
        """Show placeholder when no PR is selected."""
        self.header_frame.hide()
        self.info_group.hide()
        self.desc_group.hide()
        self.stats_group.hide()
        self.actions_frame.hide()
        self.comments_group.hide()

    def _show_content(self):
        """Show content sections."""
        self.header_frame.show()
        self.info_group.show()
        self.desc_group.show()
        self.stats_group.show()
        self.actions_frame.show()
        self.comments_group.show()

    def set_gh_wrapper(self, gh):
        """Set the GitHub wrapper instance."""
        self.gh = gh

    def set_repo(self, repo_name: str):
        """Set the repository name."""
        self.repo_name = repo_name

    def load_pr(self, pr_number: int):
        """Load a pull request by number."""
        if not self.gh or not self.repo_name:
            return

        self.pr_number = pr_number
        logger.debug("Loading PR #%d from %s", pr_number, self.repo_name)

        self.pr_data = self.gh.view_pr(pr_number, repo=self.repo_name)
        if not self.pr_data:
            self._show_placeholder()
            return

        self._update_display()
        self._show_content()

    def _update_display(self):
        """Update the display with current PR data."""
        pr = self.pr_data

        # Header
        title = pr.get("title", "Untitled")
        number = pr.get("number", "?")
        self.title_label.setText(f"#{number}: {title}")

        # State
        state = pr.get("state", "UNKNOWN").upper()
        state_style = STYLE_SUCCESS_TEXT
        if state == "MERGED":
            state_style = "color: #a855f7; font-weight: bold;"  # Purple
        elif state == "CLOSED":
            state_style = STYLE_ERROR_TEXT
        elif state == "OPEN":
            state_style = STYLE_SUCCESS_TEXT

        self.state_label.setText(state)
        self.state_label.setStyleSheet(state_style)

        # Author
        author = pr.get("author", {})
        author_name = author.get("login", "unknown") if isinstance(author, dict) else str(author)
        created = pr.get("createdAt", "")[:10]
        self.author_label.setText(f"by {author_name} on {created}")

        # Branch info
        head = pr.get("headRefName", "?")
        base = pr.get("baseRefName", "?")
        self.branch_label.setText(f"{head} → {base}")

        # Mergeable
        mergeable = pr.get("mergeable", "UNKNOWN")
        if mergeable == "MERGEABLE":
            self.mergeable_label.setText("Yes")
            self.mergeable_label.setStyleSheet(STYLE_SUCCESS_TEXT)
        elif mergeable == "CONFLICTING":
            self.mergeable_label.setText("Conflicts")
            self.mergeable_label.setStyleSheet(STYLE_ERROR_TEXT)
        else:
            self.mergeable_label.setText(mergeable)
            self.mergeable_label.setStyleSheet(STYLE_WARNING_TEXT)

        # Description
        body = pr.get("body", "") or "(No description)"
        self.description_text.setPlainText(body)

        # Stats
        additions = pr.get("additions", 0)
        deletions = pr.get("deletions", 0)
        files = pr.get("changedFiles", 0)
        self.additions_label.setText(f"+{additions}")
        self.deletions_label.setText(f"-{deletions}")
        self.files_label.setText(f"{files} files")

        # Update button states based on PR state
        is_open = state == "OPEN"
        self.merge_btn.setEnabled(is_open)
        self.merge_method.setEnabled(is_open)
        self.close_btn.setText("Close PR" if is_open else "Reopen PR")

        # Comments
        comments = pr.get("comments", [])
        if comments:
            comments_text = []
            for comment in comments[:10]:  # Limit to 10 comments
                author = comment.get("author", {})
                author_name = author.get("login", "?") if isinstance(author, dict) else "?"
                body = comment.get("body", "")
                created = comment.get("createdAt", "")[:10]
                comments_text.append(f"[{created}] {author_name}: {body}")
            self.comments_text.setPlainText("\n\n".join(comments_text))
        else:
            self.comments_text.setPlainText("(No comments)")

    def _on_merge(self):
        """Handle merge button click."""
        if not self.gh or not self.pr_number:
            return

        method_map = {"Merge": "merge", "Squash": "squash", "Rebase": "rebase"}
        method = method_map.get(self.merge_method.currentText(), "merge")

        reply = QMessageBox.question(
            self,
            "Merge Pull Request",
            f"Are you sure you want to merge PR #{self.pr_number} using {method}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            result = self.gh.merge_pr(
                self.pr_number,
                repo=self.repo_name,
                merge_method=method
            )
            if result["success"]:
                QMessageBox.information(self, "Success", "Pull request merged successfully!")
                self.pr_updated.emit()
                self.load_pr(self.pr_number)  # Reload to update state
            else:
                QMessageBox.warning(self, "Error", f"Failed to merge: {result.get('error', 'Unknown error')}")

    def _on_close(self):
        """Handle close/reopen button click."""
        if not self.gh or not self.pr_number:
            return

        state = self.pr_data.get("state", "").upper()
        is_open = state == "OPEN"

        if is_open:
            reply = QMessageBox.question(
                self,
                "Close Pull Request",
                f"Are you sure you want to close PR #{self.pr_number}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                result = self.gh.close_pr(self.pr_number, repo=self.repo_name)
                if result["success"]:
                    self.pr_updated.emit()
                    self.load_pr(self.pr_number)
                else:
                    QMessageBox.warning(self, "Error", f"Failed to close: {result.get('error', '')}")
        else:
            result = self.gh.reopen_pr(self.pr_number, repo=self.repo_name)
            if result["success"]:
                self.pr_updated.emit()
                self.load_pr(self.pr_number)
            else:
                QMessageBox.warning(self, "Error", f"Failed to reopen: {result.get('error', '')}")

    def _on_add_comment(self):
        """Handle add comment button click."""
        if not self.gh or not self.pr_number:
            return

        text, ok = QInputDialog.getMultiLineText(
            self,
            "Add Comment",
            "Enter your comment:",
            ""
        )

        if ok and text.strip():
            result = self.gh.add_pr_comment(self.pr_number, text.strip(), repo=self.repo_name)
            if result["success"]:
                self.load_pr(self.pr_number)  # Reload to show new comment
            else:
                QMessageBox.warning(self, "Error", f"Failed to add comment: {result.get('error', '')}")

    def _on_view_diff(self):
        """Handle view diff button click."""
        if not self.gh or not self.pr_number:
            return

        diff = self.gh.get_pr_diff(self.pr_number, repo=self.repo_name)
        if diff:
            # Import here to avoid circular import
            from ui.diff_viewer import DiffViewerDialog
            dialog = DiffViewerDialog(diff, f"PR #{self.pr_number} Diff", self)
            dialog.exec()
        else:
            QMessageBox.information(self, "No Diff", "No diff available for this PR.")

    def _on_view_sbs_diff(self):
        """Handle side-by-side diff button click."""
        if not self.gh or not self.pr_number:
            return

        diff = self.gh.get_pr_diff(self.pr_number, repo=self.repo_name)
        if diff:
            from ui.diff_viewer import SideBySideDiffDialog
            dialog = SideBySideDiffDialog(diff, f"PR #{self.pr_number} - Side-by-Side Diff", self)
            dialog.exec()
        else:
            QMessageBox.information(self, "No Diff", "No diff available for this PR.")

    def clear(self):
        """Clear the display."""
        self.pr_number = None
        self.pr_data = {}
        self._show_placeholder()

"""
Pull Request detail view
Shows detailed information about a specific pull request
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QFrame, QComboBox, QGroupBox, QSplitter,
    QListWidget, QListWidgetItem, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QBrush
from datetime import datetime
from typing import Optional, Dict, Any

from core.gh_wrapper import GHWrapper
from ui.dialogs import show_message_dialog, show_confirmation_dialog


class PRDetailView(QWidget):
    """Widget for displaying pull request details"""
    
    pr_updated = pyqtSignal()  # Emitted when PR is modified
    
    def __init__(self, gh: GHWrapper, repo_name: str, is_local: bool = False, parent=None):
        super().__init__(parent)
        
        self.gh = gh
        self.repo_name = repo_name
        self.is_local = is_local
        self.pr_number = None
        self.pr_data = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        layout.addWidget(scroll)
        
        # Content widget
        content = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(16)
        content.setLayout(self.content_layout)
        scroll.setWidget(content)
        
        # Placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder when no PR is selected"""
        self.clear_content()
        
        label = QLabel("Select a pull request to view details")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #888; font-size: 14px;")
        self.content_layout.addWidget(label)
        self.content_layout.addStretch()
    
    def clear_content(self):
        """Clear all content"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def load_pr(self, pr_number: int):
        """Load and display a pull request"""
        self.pr_number = pr_number
        
        # Fetch PR data
        result = self.gh.get_pr(self.repo_name, pr_number)
        
        if not result["success"]:
            self.clear_content()
            error_label = QLabel(f"Failed to load PR #{pr_number}")
            error_label.setStyleSheet("color: red;")
            self.content_layout.addWidget(error_label)
            return
        
        self.pr_data = result.get("output", {})
        self.display_pr()
    
    def display_pr(self):
        """Display the pull request information"""
        if not self.pr_data:
            return
        
        self.clear_content()
        
        # Header section
        header = self.create_header()
        self.content_layout.addWidget(header)
        
        # Status section
        status = self.create_status_section()
        self.content_layout.addWidget(status)
        
        # Metadata section (assignees and labels)
        metadata = self.create_metadata_section()
        self.content_layout.addWidget(metadata)
        
        # Body section
        body_widget = self.create_body_section()
        self.content_layout.addWidget(body_widget)
        
        # Actions section
        actions = self.create_actions_section()
        self.content_layout.addWidget(actions)
        
        # Comments section
        comments = self.create_comments_section()
        self.content_layout.addWidget(comments)
        
        self.content_layout.addStretch()
    
    def create_header(self) -> QWidget:
        """Create the PR header"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        
        # Title
        title = self.pr_data.get("title", "Untitled")
        number = self.pr_data.get("number", 0)
        
        title_label = QLabel(f"#{number}: {title}")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Meta information
        author = self.pr_data.get("author", {}).get("login", "unknown")
        created_at = self.pr_data.get("createdAt", "")
        state = self.pr_data.get("state", "OPEN")
        is_draft = self.pr_data.get("isDraft", False)
        
        meta_parts = [f"by {author}"]
        if created_at:
            date = self.format_date(created_at)
            meta_parts.append(f"opened {date}")
        if is_draft:
            meta_parts.append("DRAFT")
        
        meta_label = QLabel(" • ".join(meta_parts))
        meta_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(meta_label)
        
        return widget
    
    def create_status_section(self) -> QGroupBox:
        """Create status information section"""
        group = QGroupBox("Status")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        state = self.pr_data.get("state", "OPEN")
        head_ref = self.pr_data.get("headRefName", "")
        base_ref = self.pr_data.get("baseRefName", "")
        additions = self.pr_data.get("additions", 0)
        deletions = self.pr_data.get("deletions", 0)
        changed_files = self.pr_data.get("changedFiles", 0)
        mergeable = self.pr_data.get("mergeable", "UNKNOWN")
        
        # State
        state_colors = {
            "OPEN": "#28a745",
            "CLOSED": "#cb2431",
            "MERGED": "#6f42c1"
        }
        color = state_colors.get(state, "#666")
        state_label = QLabel(f"<b>State:</b> <span style='color: {color};'>{state}</span>")
        state_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(state_label)
        
        # Branches
        branch_label = QLabel(f"<b>Branches:</b> {head_ref} → {base_ref}")
        branch_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(branch_label)
        
        # Changes
        changes_label = QLabel(
            f"<b>Changes:</b> {changed_files} files • "
            f"<span style='color: green;'>+{additions}</span> • "
            f"<span style='color: red;'>-{deletions}</span>"
        )
        changes_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(changes_label)
        
        # Mergeable status
        mergeable_text = "✓ Can be merged" if mergeable == "MERGEABLE" else "⚠ Conflicts detected"
        mergeable_color = "green" if mergeable == "MERGEABLE" else "orange"
        mergeable_label = QLabel(
            f"<span style='color: {mergeable_color};'>{mergeable_text}</span>"
        )
        mergeable_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(mergeable_label)
        
        return group
    
    def create_metadata_section(self) -> QGroupBox:
        """Create metadata section (assignees and labels)"""
        group = QGroupBox("Metadata")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # Assignees section
        assignees_layout = QHBoxLayout()
        layout.addLayout(assignees_layout)
        
        assignees_label = QLabel("<b>Assignees:</b>")
        assignees_label.setTextFormat(Qt.TextFormat.RichText)
        assignees_layout.addWidget(assignees_label)
        
        assignees = self.pr_data.get("assignees", [])
        if isinstance(assignees, dict):
            assignees = assignees.get("nodes", [])
        if assignees:
            assignee_names = ", ".join([a.get("login", "") for a in assignees])
            assignees_text = QLabel(assignee_names)
        else:
            assignees_text = QLabel("<i>No assignees</i>")
            assignees_text.setStyleSheet("color: #888;")
        assignees_text.setTextFormat(Qt.TextFormat.RichText)
        assignees_layout.addWidget(assignees_text)
        assignees_layout.addStretch()
        
        # Only show manage button for local repositories
        if self.is_local:
            manage_assignees_btn = QPushButton("Manage Assignees")
            manage_assignees_btn.clicked.connect(self.manage_assignees)
            assignees_layout.addWidget(manage_assignees_btn)
        
        # Labels section
        labels_layout = QHBoxLayout()
        layout.addLayout(labels_layout)
        
        labels_label = QLabel("<b>Labels:</b>")
        labels_label.setTextFormat(Qt.TextFormat.RichText)
        labels_layout.addWidget(labels_label)
        
        labels = self.pr_data.get("labels", [])
        if isinstance(labels, dict):
            labels = labels.get("nodes", [])
        if labels:
            labels_widget = QWidget()
            labels_inner_layout = QHBoxLayout()
            labels_inner_layout.setContentsMargins(0, 0, 0, 0)
            labels_inner_layout.setSpacing(4)
            labels_widget.setLayout(labels_inner_layout)
            
            for label in labels[:5]:  # Show max 5 labels
                label_name = label.get("name", "")
                label_color = label.get("color", "")
                label_btn = QPushButton(label_name)
                if label_color:
                    # Calculate brightness to determine text color
                    color = QColor(f"#{label_color}")
                    brightness = (color.red() * 299 + color.green() * 587 + color.blue() * 114) / 1000
                    text_color = "white" if brightness < 128 else "black"
                    label_btn.setStyleSheet(
                        f"background-color: #{label_color}; "
                        f"color: {text_color}; "
                        f"border: none; "
                        f"padding: 2px 8px; "
                        f"border-radius: 3px; "
                        f"font-size: 11px;"
                    )
                else:
                    label_btn.setStyleSheet(
                        f"background-color: #e1e4e8; "
                        f"color: black; "
                        f"border: none; "
                        f"padding: 2px 8px; "
                        f"border-radius: 3px; "
                        f"font-size: 11px;"
                    )
                label_btn.setMaximumHeight(20)
                labels_inner_layout.addWidget(label_btn)
            
            labels_layout.addWidget(labels_widget)
        else:
            labels_text = QLabel("<i>No labels</i>")
            labels_text.setTextFormat(Qt.TextFormat.RichText)
            labels_text.setStyleSheet("color: #888;")
            labels_layout.addWidget(labels_text)
        
        labels_layout.addStretch()
        
        # Only show manage button for local repositories
        if self.is_local:
            manage_labels_btn = QPushButton("Manage Labels")
            manage_labels_btn.clicked.connect(self.manage_labels)
            labels_layout.addWidget(manage_labels_btn)
        
        return group
    
    def create_body_section(self) -> QGroupBox:
        """Create PR body section"""
        group = QGroupBox("Description")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        body = self.pr_data.get("body", "")
        if not body:
            body = "<i>No description provided</i>"
        
        body_text = QTextEdit()
        body_text.setReadOnly(True)
        body_text.setPlainText(body)
        body_text.setMaximumHeight(200)
        layout.addWidget(body_text)
        
        return group
    
    def create_actions_section(self) -> QFrame:
        """Create actions section"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout()
        frame.setLayout(layout)
        
        state = self.pr_data.get("state", "OPEN")
        
        if state == "OPEN":
            # Merge options
            layout.addWidget(QLabel("Merge method:"))
            
            self.merge_method_combo = QComboBox()
            self.merge_method_combo.addItems(["Merge", "Squash", "Rebase"])
            layout.addWidget(self.merge_method_combo)
            
            merge_btn = QPushButton("✓ Merge Pull Request")
            merge_btn.clicked.connect(self.merge_pr)
            layout.addWidget(merge_btn)
            
            layout.addSpacing(16)
            
            close_btn = QPushButton("✕ Close")
            close_btn.setObjectName("secondaryButton")
            close_btn.clicked.connect(self.close_pr)
            layout.addWidget(close_btn)
        elif state == "CLOSED":
            reopen_btn = QPushButton("↻ Reopen")
            reopen_btn.clicked.connect(self.reopen_pr)
            layout.addWidget(reopen_btn)
        
        layout.addStretch()
        
        # View diff button
        diff_btn = QPushButton("📄 View Diff")
        diff_btn.clicked.connect(self.view_diff)
        layout.addWidget(diff_btn)
        
        # Comment button
        comment_btn = QPushButton("💬 Add Comment")
        comment_btn.clicked.connect(self.add_comment)
        layout.addWidget(comment_btn)
        
        return frame
    
    def create_comments_section(self) -> QGroupBox:
        """Create comments section"""
        group = QGroupBox("Comments & Reviews")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        comments = self.pr_data.get("comments", [])
        reviews = self.pr_data.get("reviews", [])
        
        total = len(comments) + len(reviews)
        info_label = QLabel(f"{total} comment(s) and review(s)")
        info_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(info_label)
        
        return group
    
    def merge_pr(self):
        """Merge the pull request"""
        method_map = {
            "Merge": "merge",
            "Squash": "squash",
            "Rebase": "rebase"
        }
        method = method_map[self.merge_method_combo.currentText()]
        
        confirmed, delete_branch = show_confirmation_dialog(
            self,
            "Merge Pull Request",
            f"Merge PR #{self.pr_number} using {method}?",
            checkbox_text="Delete branch after merge"
        )
        
        if not confirmed:
            return
        
        result = self.gh.merge_pr(
            self.repo_name,
            self.pr_number,
            method=method,
            delete_branch=delete_branch
        )
        
        if result["success"]:
            show_message_dialog(
                self,
                "Success",
                f"Pull request #{self.pr_number} merged successfully!"
            )
            self.pr_updated.emit()
            self.load_pr(self.pr_number)
        else:
            show_message_dialog(
                self,
                "Merge Failed",
                f"Failed to merge pull request:\n{result['error']}",
                msg_type="error"
            )
    
    def close_pr(self):
        """Close the pull request"""
        confirmed = show_confirmation_dialog(
            self,
            "Close Pull Request",
            f"Close PR #{self.pr_number} without merging?"
        )
        
        if not confirmed:
            return
        
        result = self.gh.close_pr(self.repo_name, self.pr_number)
        
        if result["success"]:
            show_message_dialog(
                self,
                "Success",
                f"Pull request #{self.pr_number} closed."
            )
            self.pr_updated.emit()
            self.load_pr(self.pr_number)
        else:
            show_message_dialog(
                self,
                "Error",
                f"Failed to close pull request:\n{result['error']}",
                msg_type="error"
            )
    
    def reopen_pr(self):
        """Reopen the pull request"""
        result = self.gh.reopen_pr(self.repo_name, self.pr_number)
        
        if result["success"]:
            show_message_dialog(
                self,
                "Success",
                f"Pull request #{self.pr_number} reopened."
            )
            self.pr_updated.emit()
            self.load_pr(self.pr_number)
        else:
            show_message_dialog(
                self,
                "Error",
                f"Failed to reopen pull request:\n{result['error']}",
                msg_type="error"
            )
    
    def view_diff(self):
        """View the PR diff"""
        result = self.gh.get_pr_diff(self.repo_name, self.pr_number)
        
        if result["success"]:
            # TODO: Show diff in a proper viewer
            diff_text = result.get("output", "")
            show_message_dialog(
                self,
                f"Diff for PR #{self.pr_number}",
                f"Diff loaded ({len(diff_text)} characters). Full diff viewer coming soon!"
            )
        else:
            show_message_dialog(
                self,
                "Error",
                f"Failed to load diff:\n{result['error']}",
                msg_type="error"
            )
    
    def add_comment(self):
        """Add a comment to the PR"""
        from PyQt6.QtWidgets import QInputDialog
        
        comment, ok = QInputDialog.getMultiLineText(
            self,
            "Add Comment",
            "Enter your comment:",
        )
        
        if ok and comment.strip():
            result = self.gh.comment_on_pr(
                self.repo_name,
                self.pr_number,
                comment.strip()
            )
            
            if result["success"]:
                show_message_dialog(
                    self,
                    "Success",
                    "Comment added successfully!"
                )
                self.load_pr(self.pr_number)
            else:
                show_message_dialog(
                    self,
                    "Error",
                    f"Failed to add comment:\n{result['error']}",
                    msg_type="error"
                )
    
    @staticmethod
    def format_date(date_str: str) -> str:
        """Format ISO date string to readable format"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%b %d, %Y")
        except:
            return date_str
    
    def manage_assignees(self):
        """Manage assignees for the PR"""
        dialog = AssigneeDialog(
            self.gh,
            self.repo_name,
            self.pr_number,
            self.pr_data,
            self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.pr_updated.emit()
            self.load_pr(self.pr_number)
    
    def manage_labels(self):
        """Manage labels for the PR"""
        dialog = LabelDialog(
            self.gh,
            self.repo_name,
            self.pr_number,
            self.pr_data,
            self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.pr_updated.emit()
            self.load_pr(self.pr_number)


class AssigneeDialog(QDialog):
    """Dialog for managing PR assignees"""
    
    def __init__(self, gh: GHWrapper, repo_name: str, pr_number: int,
                 pr_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.gh = gh
        self.repo_name = repo_name
        self.pr_number = pr_number
        self.pr_data = pr_data
        
        self.setWindowTitle(f"Manage Assignees - PR #{pr_number}")
        self.setModal(True)
        self.resize(450, 400)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Info label
        info = QLabel("Select or deselect assignees for this pull request:")
        layout.addWidget(info)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_assignees)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_data(self):
        """Load collaborators and current assignees"""
        # Get current assignees
        current_assignees = set()
        assignees = self.pr_data.get("assignees", [])
        if isinstance(assignees, dict):
            assignees = assignees.get("nodes", [])
        for assignee in assignees:
            login = assignee.get("login", "")
            if login:
                current_assignees.add(login)
        
        # Get all collaborators
        result = self.gh.get_repo_collaborators(self.repo_name)
        if result["success"] and result.get("output"):
            for collab in result["output"]:
                login = collab.get("login", "")
                if login:
                    item = QListWidgetItem(login)
                    self.list_widget.addItem(item)
                    if login in current_assignees:
                        item.setSelected(True)
    
    def save_assignees(self):
        """Save assignee changes"""
        # Get current and new selections
        current_assignees = set()
        assignees = self.pr_data.get("assignees", [])
        if isinstance(assignees, dict):
            assignees = assignees.get("nodes", [])
        for assignee in assignees:
            login = assignee.get("login", "")
            if login:
                current_assignees.add(login)
        
        selected_assignees = set()
        for item in self.list_widget.selectedItems():
            selected_assignees.add(item.text())
        
        # Calculate additions and removals
        to_add = list(selected_assignees - current_assignees)
        to_remove = list(current_assignees - selected_assignees)
        
        success = True
        
        # Add new assignees
        if to_add:
            result = self.gh.add_pr_assignees(
                self.repo_name,
                self.pr_number,
                to_add
            )
            if not result["success"]:
                show_message_dialog(
                    self,
                    "Error",
                    f"Failed to add assignees:\n{result['error']}",
                    msg_type="error"
                )
                success = False
        
        # Remove assignees
        if to_remove:
            result = self.gh.remove_pr_assignees(
                self.repo_name,
                self.pr_number,
                to_remove
            )
            if not result["success"]:
                show_message_dialog(
                    self,
                    "Error",
                    f"Failed to remove assignees:\n{result['error']}",
                    msg_type="error"
                )
                success = False
        
        if success:
            if to_add or to_remove:
                show_message_dialog(
                    self,
                    "Success",
                    "Assignees updated successfully!"
                )
            self.accept()


class LabelDialog(QDialog):
    """Dialog for managing PR labels"""
    
    def __init__(self, gh: GHWrapper, repo_name: str, pr_number: int,
                 pr_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.gh = gh
        self.repo_name = repo_name
        self.pr_number = pr_number
        self.pr_data = pr_data
        
        self.setWindowTitle(f"Manage Labels - PR #{pr_number}")
        self.setModal(True)
        self.resize(450, 400)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Info label
        info = QLabel("Select or deselect labels for this pull request:")
        layout.addWidget(info)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_labels)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_data(self):
        """Load repo labels and current PR labels"""
        # Get current labels
        current_labels = set()
        labels = self.pr_data.get("labels", [])
        if isinstance(labels, dict):
            labels = labels.get("nodes", [])
        for label in labels:
            name = label.get("name", "")
            if name:
                current_labels.add(name)
        
        # Get all repo labels
        result = self.gh.get_repo_labels(self.repo_name)
        if result["success"] and result.get("output"):
            for label in result["output"]:
                name = label.get("name", "")
                if name:
                    color = label.get("color", "")
                    # Create item with label name and color description
                    display_text = f"{name}"
                    if color:
                        display_text = f"⬤ {name}"  # Add colored circle
                    item = QListWidgetItem(display_text)
                    
                    # Set color using QColor and QBrush
                    if color:
                        bg_color = QColor(f"#{color}")
                        # Calculate brightness to determine text color
                        brightness = (bg_color.red() * 299 + bg_color.green() * 587 + bg_color.blue() * 114) / 1000
                        text_color = QColor("white") if brightness < 128 else QColor("black")
                        item.setForeground(QBrush(text_color))
                        item.setBackground(QBrush(bg_color))
                    
                    self.list_widget.addItem(item)
                    if name in current_labels:
                        item.setSelected(True)
    
    def save_labels(self):
        """Save label changes"""
        # Get current and new selections
        current_labels = set()
        labels = self.pr_data.get("labels", [])
        if isinstance(labels, dict):
            labels = labels.get("nodes", [])
        for label in labels:
            name = label.get("name", "")
            if name:
                current_labels.add(name)
        
        selected_labels = set()
        for item in self.list_widget.selectedItems():
            selected_labels.add(item.text())
        
        # Calculate additions and removals
        to_add = list(selected_labels - current_labels)
        to_remove = list(current_labels - selected_labels)
        
        success = True
        
        # Add new labels
        if to_add:
            result = self.gh.add_pr_labels(
                self.repo_name,
                self.pr_number,
                to_add
            )
            if not result["success"]:
                show_message_dialog(
                    self,
                    "Error",
                    f"Failed to add labels:\n{result['error']}",
                    msg_type="error"
                )
                success = False
        
        # Remove labels
        if to_remove:
            result = self.gh.remove_pr_labels(
                self.repo_name,
                self.pr_number,
                to_remove
            )
            if not result["success"]:
                show_message_dialog(
                    self,
                    "Error",
                    f"Failed to remove labels:\n{result['error']}",
                    msg_type="error"
                )
                success = False
        
        if success:
            if to_add or to_remove:
                show_message_dialog(
                    self,
                    "Success",
                    "Labels updated successfully!"
                )
            self.accept()

"""
Create Pull Request dialog
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QCheckBox, QPushButton,
    QLabel, QComboBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent

from core.gh_wrapper import GHWrapper
from core.git_operations import GitRepository
from ui.dialogs import show_message_dialog, center_dialog_on_parent
from ui.styles import STYLE_INFO_TEXT_PADDED
from ui.constants import (
    PR_CREATE_DIALOG_WIDTH,
    PR_CREATE_DIALOG_HEIGHT,
    PR_CREATE_BODY_MIN_HEIGHT,
    LIST_MAX_HEIGHT_SMALL
)


class CreatePRDialog(QDialog):
    """Dialog for creating a new pull request"""
    
    def __init__(self, repo_path: str, repo_name: str, gh: GHWrapper,
                 parent=None):
        super().__init__(parent)
        
        self.repo_path = repo_path
        self.repo_name = repo_name
        self.gh = gh
        self.repo = None
        self._centered = False
        self.collaborators = []
        self.labels = []
        
        try:
            self.repo = GitRepository(repo_path)
        except Exception as e:
            show_message_dialog(
                self,
                "Error",
                f"Failed to open repository: {str(e)}",
                msg_type="error"
            )
            return
        
        # Load collaborators and labels
        self.load_repo_data()
        
        self.init_ui()
    
    def showEvent(self, event: QShowEvent):
        """Override showEvent to center dialog on parent."""
        super().showEvent(event)
        if not self._centered:
            center_dialog_on_parent(self)
            self._centered = True
    
    def load_repo_data(self):
        """Load collaborators and labels from repository"""
        # Load collaborators
        collab_result = self.gh.get_repo_collaborators(self.repo_name)
        if collab_result["success"] and collab_result.get("output"):
            self.collaborators = collab_result["output"]
        
        # Load labels
        labels_result = self.gh.get_repo_labels(self.repo_name)
        if labels_result["success"] and labels_result.get("output"):
            self.labels = labels_result["output"]
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Create Pull Request")
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(PR_CREATE_DIALOG_WIDTH, PR_CREATE_DIALOG_HEIGHT)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Form layout
        form = QFormLayout()
        layout.addLayout(form)
        
        # Current branch info
        if self.repo:
            current_branch = self.repo.current_branch
            info_label = QLabel(f"Current branch: <b>{current_branch}</b>")
            info_label.setTextFormat(Qt.TextFormat.RichText)
            form.addRow("", info_label)
        
        # Base branch (target)
        self.base_combo = QComboBox()
        if self.repo:
            # Get remote branches
            remote_branches = self.repo.remote_branches
            self.base_combo.addItems(remote_branches)
            # Set main/master as default if available
            if 'main' in remote_branches:
                self.base_combo.setCurrentText('main')
            elif 'master' in remote_branches:
                self.base_combo.setCurrentText('master')
        else:
            self.base_combo.addItems(['main', 'master'])
        
        form.addRow("Base branch:", self.base_combo)
        
        # Head branch (source)
        self.head_combo = QComboBox()
        self.head_combo.setEditable(True)
        if self.repo:
            branches = self.repo.branches
            self.head_combo.addItems(branches)
            # Set current branch as default
            self.head_combo.setCurrentText(self.repo.current_branch)
        form.addRow("Head branch:", self.head_combo)
        
        # PR title
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText(
            "Add descriptive title for your changes"
        )
        form.addRow("Title:", self.title_edit)
        
        # PR body/description
        self.body_edit = QTextEdit()
        self.body_edit.setPlaceholderText(
            "Describe your changes in detail...\n\n"
            "What does this PR do?\n"
            "Why are these changes needed?\n"
            "Any breaking changes?"
        )
        self.body_edit.setMinimumHeight(PR_CREATE_BODY_MIN_HEIGHT)
        form.addRow("Description:", self.body_edit)
        
        # Draft checkbox
        self.draft_check = QCheckBox("Create as draft pull request")
        self.draft_check.setToolTip(
            "Draft PRs cannot be merged until marked as ready"
        )
        form.addRow("", self.draft_check)
        
        # Assignees
        assignees_label = QLabel("Assignees:")
        self.assignees_list = QListWidget()
        self.assignees_list.setMaximumHeight(LIST_MAX_HEIGHT_SMALL)
        self.assignees_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        for collab in self.collaborators:
            login = collab.get("login", "")
            if login:
                item = QListWidgetItem(login)
                self.assignees_list.addItem(item)
        form.addRow(assignees_label, self.assignees_list)
        
        # Labels
        labels_label = QLabel("Labels:")
        self.labels_list = QListWidget()
        self.labels_list.setMaximumHeight(LIST_MAX_HEIGHT_SMALL)
        self.labels_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        for label in self.labels:
            label_name = label.get("name", "")
            if label_name:
                item = QListWidgetItem(label_name)
                # Set color indicator
                color = label.get("color", "")
                if color:
                    item.setForeground(Qt.GlobalColor.white)
                    item.setBackground(Qt.GlobalColor.fromString(f"#{color}"))
                self.labels_list.addItem(item)
        form.addRow(labels_label, self.labels_list)
        
        # Info label
        info_label = QLabel(
            "💡 Select assignees and labels for this pull request. "
            "You can also add reviewers after creation on GitHub."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet(STYLE_INFO_TEXT_PADDED)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.create_btn = QPushButton("Create Pull Request")
        self.create_btn.setDefault(True)
        self.create_btn.clicked.connect(self.create_pr)
        button_layout.addWidget(self.create_btn)
    
    def create_pr(self):
        """Create the pull request"""
        title = self.title_edit.text().strip()
        body = self.body_edit.toPlainText().strip()
        base = self.base_combo.currentText().strip()
        head = self.head_combo.currentText().strip()
        draft = self.draft_check.isChecked()
        
        # Validation
        if not title:
            show_message_dialog(
                self,
                "Validation Error",
                "Please enter a title for the pull request.",
                msg_type="warning"
            )
            return
        
        if not head:
            show_message_dialog(
                self,
                "Validation Error",
                "Please select a head branch.",
                msg_type="warning"
            )
            return
        
        if not base:
            show_message_dialog(
                self,
                "Validation Error",
                "Please select a base branch.",
                msg_type="warning"
            )
            return
        
        if head == base:
            show_message_dialog(
                self,
                "Validation Error",
                "Head and base branches cannot be the same.",
                msg_type="warning"
            )
            return
        
        # Get selected assignees and labels
        selected_assignees = [
            item.text() for item in self.assignees_list.selectedItems()
        ]
        selected_labels = [
            item.text() for item in self.labels_list.selectedItems()
        ]
        
        # Create PR
        self.create_btn.setEnabled(False)
        self.create_btn.setText("Creating...")
        
        result = self.gh.create_pr(
            repo=self.repo_name,
            title=title,
            body=body,
            head=head,
            base=base,
            draft=draft
        )
        
        if result["success"]:
            # Extract PR number from output
            pr_number = None
            output = result.get("output", "")
            # Parse URL like https://github.com/owner/repo/pull/123
            if "/pull/" in output:
                try:
                    pr_number = output.split("/pull/")[-1].split()[0].strip()
                except:
                    pass
            
            # Add assignees if PR created successfully
            if pr_number and selected_assignees:
                assignee_result = self.gh.add_pr_assignees(
                    self.repo_name, pr_number, selected_assignees
                )
                if not assignee_result["success"]:
                    print(f"Warning: Failed to add assignees: {assignee_result['error']}")
            
            # Add labels if PR created successfully
            if pr_number and selected_labels:
                label_result = self.gh.add_pr_labels(
                    self.repo_name, pr_number, selected_labels
                )
                if not label_result["success"]:
                    print(f"Warning: Failed to add labels: {label_result['error']}")
            
            self.create_btn.setEnabled(True)
            self.create_btn.setText("Create Pull Request")
            
            show_message_dialog(
                self,
                "Success",
                f"Pull request created successfully!\n\n{output}"
            )
            self.accept()
        else:
            self.create_btn.setEnabled(True)
            self.create_btn.setText("Create Pull Request")
            
            show_message_dialog(
                self,
                "Creation Failed",
                f"Failed to create pull request:\n\n{result['error']}",
                msg_type="error"
            )

"""
Create Pull Request dialog
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QCheckBox, QPushButton,
    QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
import git

from core.gh_wrapper import GHWrapper
from ui.dialogs import show_message_dialog, center_dialog_on_parent


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
        
        try:
            self.repo = git.Repo(repo_path)
        except Exception as e:
            show_message_dialog(
                self,
                "Error",
                f"Failed to open repository: {str(e)}",
                msg_type="error"
            )
            return
        
        self.init_ui()
    
    def showEvent(self, event: QShowEvent):
        """Override showEvent to center dialog on parent."""
        super().showEvent(event)
        if not self._centered:
            center_dialog_on_parent(self)
            self._centered = True
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Create Pull Request")
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(600, 450)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Form layout
        form = QFormLayout()
        layout.addLayout(form)
        
        # Current branch info
        if self.repo:
            current_branch = self.repo.active_branch.name
            info_label = QLabel(f"Current branch: <b>{current_branch}</b>")
            info_label.setTextFormat(Qt.TextFormat.RichText)
            form.addRow("", info_label)
        
        # Base branch (target)
        self.base_combo = QComboBox()
        if self.repo:
            # Get remote branches
            try:
                remote_branches = [
                    ref.name.split('/')[-1]
                    for ref in self.repo.remote().refs
                    if not ref.name.endswith('/HEAD')
                ]
                self.base_combo.addItems(remote_branches)
                # Set main/master as default if available
                if 'main' in remote_branches:
                    self.base_combo.setCurrentText('main')
                elif 'master' in remote_branches:
                    self.base_combo.setCurrentText('master')
            except:
                self.base_combo.addItems(['main', 'master'])
        else:
            self.base_combo.addItems(['main', 'master'])
        
        form.addRow("Base branch:", self.base_combo)
        
        # Head branch (source)
        self.head_combo = QComboBox()
        self.head_combo.setEditable(True)
        if self.repo:
            branches = [branch.name for branch in self.repo.branches]
            self.head_combo.addItems(branches)
            # Set current branch as default
            try:
                current = self.repo.active_branch.name
                self.head_combo.setCurrentText(current)
            except:
                pass
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
        self.body_edit.setMinimumHeight(150)
        form.addRow("Description:", self.body_edit)
        
        # Draft checkbox
        self.draft_check = QCheckBox("Create as draft pull request")
        self.draft_check.setToolTip(
            "Draft PRs cannot be merged until marked as ready"
        )
        form.addRow("", self.draft_check)
        
        # Info label
        info_label = QLabel(
            "💡 After creation, you can add reviewers, labels, "
            "and assignees on GitHub."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-size: 11px; padding: 10px;")
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
        
        self.create_btn.setEnabled(True)
        self.create_btn.setText("Create Pull Request")
        
        if result["success"]:
            show_message_dialog(
                self,
                "Success",
                f"Pull request created successfully!\n\n{result.get('output', '')}"
            )
            self.accept()
        else:
            show_message_dialog(
                self,
                "Creation Failed",
                f"Failed to create pull request:\n\n{result['error']}",
                msg_type="error"
            )

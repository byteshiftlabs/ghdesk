"""
Create tag dialog
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QCheckBox, QPushButton,
    QLabel, QComboBox
)
from PyQt6.QtCore import Qt
import git

from core.gh_wrapper import GHWrapper
from ui.dialogs import show_message_dialog


class CreateTagDialog(QDialog):
    """Dialog for creating a new Git tag"""
    
    def __init__(self, repo_path: str, gh: GHWrapper, parent=None):
        super().__init__(parent)
        
        self.repo_path = repo_path
        self.gh = gh
        self.repo = None
        
        try:
            self.repo = git.Repo(repo_path)
        except Exception as e:
            show_message_dialog(self, "Error", "Failed to open repository", str(e))
            return
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Create Tag")
        self.setModal(True)
        self.resize(400, 280)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        self.setLayout(layout)
        
        # Form layout
        form = QFormLayout()
        layout.addLayout(form)
        
        # Tag name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("v1.0.0")
        form.addRow("Tag Name:", self.name_edit)
        
        # Target (commit/branch)
        target_layout = QHBoxLayout()
        self.target_combo = QComboBox()
        self.target_combo.setEditable(True)
        
        # Populate with branches and HEAD
        if self.repo:
            self.target_combo.addItem("HEAD")
            for branch in self.repo.branches:
                self.target_combo.addItem(branch.name)
        
        target_layout.addWidget(self.target_combo)
        form.addRow("Target:", target_layout)
        
        # Message (optional)
        self.message_edit = QTextEdit()
        self.message_edit.setPlaceholderText("Optional: Add a message to create an annotated tag...")
        self.message_edit.setMaximumHeight(70)
        form.addRow("Message:", self.message_edit)
        
        # Info label
        info_label = QLabel("The tag will be created locally and pushed to the remote repository.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-size: 11px; padding: 4px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        create_btn = QPushButton("Create Tag")
        create_btn.setDefault(True)
        create_btn.clicked.connect(self.create_tag)
        button_layout.addWidget(create_btn)
    
    def create_tag(self):
        """Create the tag"""
        tag_name = self.name_edit.text().strip()
        target = self.target_combo.currentText().strip()
        message = self.message_edit.toPlainText().strip()
        
        # Validation
        if not tag_name:
            show_message_dialog(self, "Validation Error", "Please enter a tag name.")
            return
        
        if not target:
            target = "HEAD"
        
        # Create tag
        result = self.gh.create_tag(
            repo=self.repo_path,
            tag_name=tag_name,
            target=target,
            message=message if message else None
        )
        
        if result["success"]:
            show_message_dialog(
                self, 
                "Success", 
                f"Tag '{tag_name}' has been created",
                "The tag has been pushed to the remote repository."
            )
            self.accept()
        else:
            show_message_dialog(
                self,
                "Error Creating Tag",
                "Failed to create tag",
                result['error']
            )

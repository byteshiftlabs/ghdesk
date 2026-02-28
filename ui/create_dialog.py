"""
Create repository dialog
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QCheckBox, QPushButton,
    QLabel, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from pathlib import Path

from core.gh_wrapper import GHWrapper
from ui.dialogs import show_message_dialog, center_dialog_on_parent
from ui.constants import CREATE_DIALOG_WIDTH, CREATE_DIALOG_HEIGHT, INPUT_MAX_HEIGHT
from PyQt6.QtGui import QShowEvent


class CreateRepoDialog(QDialog):
    """Dialog for creating a new repository"""
    
    def __init__(self, gh: GHWrapper, parent=None):
        super().__init__(parent)
        
        self.gh = gh
        self._centered = False
        self.init_ui()
    
    def showEvent(self, event: QShowEvent):
        """Override showEvent to center dialog on parent."""
        super().showEvent(event)
        if not self._centered:
            center_dialog_on_parent(self)
            self._centered = True
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Create Repository")
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(CREATE_DIALOG_WIDTH, CREATE_DIALOG_HEIGHT)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Form layout
        form = QFormLayout()
        layout.addLayout(form)
        
        # Repository name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("my-awesome-project")
        form.addRow("Repository Name:", self.name_edit)
        
        # Description
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("A brief description of your project...")
        self.desc_edit.setMaximumHeight(INPUT_MAX_HEIGHT)
        form.addRow("Description:", self.desc_edit)
        
        # Private checkbox
        self.private_check = QCheckBox("Make repository private")
        form.addRow("", self.private_check)
        
        # Clone checkbox
        self.clone_check = QCheckBox("Clone after creation")
        self.clone_check.setChecked(True)
        self.clone_check.stateChanged.connect(self.on_clone_toggled)
        form.addRow("", self.clone_check)
        
        # Clone path
        self.path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setText(str(Path.home()))
        self.path_layout.addWidget(self.path_edit)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_path)
        self.path_layout.addWidget(self.browse_btn)
        
        form.addRow("Clone to:", self.path_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        button_layout.addStretch()
        
        self.create_btn = QPushButton("Create")
        self.create_btn.setDefault(True)
        self.create_btn.clicked.connect(self.create_repository)
        button_layout.addWidget(self.create_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
    
    def on_clone_toggled(self, state):
        """Handle clone checkbox toggle"""
        enabled = state == Qt.CheckState.Checked.value
        self.path_edit.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)
    
    def browse_path(self):
        """Browse for clone destination"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Clone Destination",
            self.path_edit.text()
        )
        
        if directory:
            self.path_edit.setText(directory)
    
    def create_repository(self):
        """Create the repository"""
        name = self.name_edit.text().strip()
        
        if not name:
            show_message_dialog(self, "Invalid Input", "Please enter a repository name", msg_type="warning")
            return
        
        description = self.desc_edit.toPlainText().strip()
        private = self.private_check.isChecked()
        clone = self.clone_check.isChecked()
        
        # Create on GitHub
        self.create_btn.setEnabled(False)
        self.create_btn.setText("Creating...")
        
        result = self.gh.create_repo(
            name=name,
            description=description,
            private=private,
            clone=clone
        )
        
        self.create_btn.setEnabled(True)
        self.create_btn.setText("Create")
        
        if result["success"]:
            show_message_dialog(
                self, "Success",
                f"Repository '{name}' created successfully!"
            )
            self.accept()
        else:
            show_message_dialog(
                self, "Creation Failed",
                f"Failed to create repository:\n{result['error']}",
                msg_type="warning"
            )

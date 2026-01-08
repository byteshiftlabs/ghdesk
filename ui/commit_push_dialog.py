"""
Commit and Push dialog
Shows file diffs, allows staging, committing, and pushing changes
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QPushButton, QLabel, QListWidget, QListWidgetItem,
    QLineEdit, QCheckBox, QGroupBox, QWidget, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
import git
from pathlib import Path

from ui.dialogs import show_message_dialog, center_dialog_on_parent, show_confirmation_dialog


class DiffHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for git diffs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.formats = {}
        
        # Added lines (green)
        add_format = QTextCharFormat()
        add_format.setForeground(QColor("#28a745"))
        self.formats['add'] = add_format
        
        # Removed lines (red)
        remove_format = QTextCharFormat()
        remove_format.setForeground(QColor("#cb2431"))
        self.formats['remove'] = remove_format
        
        # File headers (blue)
        header_format = QTextCharFormat()
        header_format.setForeground(QColor("#0366d6"))
        header_format.setFontWeight(QFont.Weight.Bold)
        self.formats['header'] = header_format
        
        # Hunk headers (cyan)
        hunk_format = QTextCharFormat()
        hunk_format.setForeground(QColor("#0969da"))
        self.formats['hunk'] = hunk_format
    
    def highlightBlock(self, text):
        """Highlight a block of text"""
        if text.startswith('+') and not text.startswith('+++'):
            self.setFormat(0, len(text), self.formats['add'])
        elif text.startswith('-') and not text.startswith('---'):
            self.setFormat(0, len(text), self.formats['remove'])
        elif text.startswith('diff --git') or text.startswith('index ') or text.startswith('+++') or text.startswith('---'):
            self.setFormat(0, len(text), self.formats['header'])
        elif text.startswith('@@'):
            self.setFormat(0, len(text), self.formats['hunk'])


class CommitPushDialog(QDialog):
    """Dialog for viewing diffs, committing, and pushing changes"""
    
    def __init__(self, repo_path: str, parent=None):
        super().__init__(parent)
        
        self.repo_path = repo_path
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
        self.load_changes()
    
    def showEvent(self, event):
        """Override showEvent to center dialog on parent."""
        super().showEvent(event)
        if not self._centered:
            center_dialog_on_parent(self)
            self._centered = True
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Commit and Push Changes")
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(1000, 700)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Info label
        repo_name = Path(self.repo_path).name
        current_branch = self.repo.active_branch.name if not self.repo.head.is_detached else "detached"
        info = QLabel(f"<b>{repo_name}</b> • Branch: <b>{current_branch}</b>")
        info.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(info)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left panel - File list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_panel.setLayout(left_layout)
        
        left_label = QLabel("Modified Files")
        left_label.setStyleSheet("font-weight: bold; padding: 5px;")
        left_layout.addWidget(left_label)
        
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_selected)
        left_layout.addWidget(self.file_list)
        
        splitter.addWidget(left_panel)
        
        # Right panel - Diff viewer
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_panel.setLayout(right_layout)
        
        right_label = QLabel("Diff Preview")
        right_label.setStyleSheet("font-weight: bold; padding: 5px;")
        right_layout.addWidget(right_label)
        
        self.diff_viewer = QTextEdit()
        self.diff_viewer.setReadOnly(True)
        self.diff_viewer.setFont(QFont("Monospace", 9))
        self.highlighter = DiffHighlighter(self.diff_viewer.document())
        right_layout.addWidget(self.diff_viewer)
        
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        # Commit section
        commit_group = QGroupBox("Commit")
        commit_layout = QVBoxLayout()
        commit_group.setLayout(commit_layout)
        
        commit_layout.addWidget(QLabel("Commit message:"))
        self.commit_message = QTextEdit()
        self.commit_message.setMaximumHeight(100)
        self.commit_message.setPlaceholderText("Enter commit message...")
        commit_layout.addWidget(self.commit_message)
        
        # Stage all checkbox
        self.stage_all_check = QCheckBox("Stage all modified files")
        self.stage_all_check.setChecked(True)
        commit_layout.addWidget(self.stage_all_check)
        
        layout.addWidget(commit_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_changes)
        button_layout.addWidget(self.refresh_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.commit_btn = QPushButton("💾 Commit")
        self.commit_btn.clicked.connect(self.commit_changes)
        button_layout.addWidget(self.commit_btn)
        
        self.commit_push_btn = QPushButton("💾 Commit && Push")
        self.commit_push_btn.setDefault(True)
        self.commit_push_btn.clicked.connect(self.commit_and_push)
        button_layout.addWidget(self.commit_push_btn)
    
    def load_changes(self):
        """Load modified files and their diffs"""
        if not self.repo:
            return
        
        self.file_list.clear()
        
        # Get modified files
        modified = [item.a_path for item in self.repo.index.diff(None)]
        staged = [item.a_path for item in self.repo.index.diff("HEAD")] if not self.repo.head.is_detached else []
        untracked = self.repo.untracked_files
        
        # Add modified files
        for file_path in modified:
            item = QListWidgetItem(f"🔸 {file_path} (modified)")
            item.setData(Qt.ItemDataRole.UserRole, {"path": file_path, "type": "modified"})
            self.file_list.addItem(item)
        
        # Add staged files
        for file_path in staged:
            if file_path not in modified:
                item = QListWidgetItem(f"✅ {file_path} (staged)")
                item.setData(Qt.ItemDataRole.UserRole, {"path": file_path, "type": "staged"})
                item.setForeground(QColor("#28a745"))
                self.file_list.addItem(item)
        
        # Add untracked files
        for file_path in untracked:
            item = QListWidgetItem(f"❓ {file_path} (untracked)")
            item.setData(Qt.ItemDataRole.UserRole, {"path": file_path, "type": "untracked"})
            item.setForeground(QColor("#ffa500"))
            self.file_list.addItem(item)
        
        if self.file_list.count() == 0:
            item = QListWidgetItem("No changes detected")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.file_list.addItem(item)
            self.commit_btn.setEnabled(False)
            self.commit_push_btn.setEnabled(False)
        else:
            self.commit_btn.setEnabled(True)
            self.commit_push_btn.setEnabled(True)
    
    def on_file_selected(self, item: QListWidgetItem):
        """Show diff for selected file"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        file_path = data["path"]
        file_type = data["type"]
        
        try:
            if file_type == "untracked":
                # Show file content for untracked files
                full_path = Path(self.repo_path) / file_path
                if full_path.exists() and full_path.is_file():
                    content = full_path.read_text()
                    diff_text = f"New file: {file_path}\n\n{content}"
                else:
                    diff_text = f"Cannot read file: {file_path}"
            else:
                # Show git diff
                diff = self.repo.git.diff(file_path)
                if not diff:
                    diff = f"No diff available for {file_path}"
                diff_text = diff
            
            self.diff_viewer.setPlainText(diff_text)
        except Exception as e:
            self.diff_viewer.setPlainText(f"Error loading diff: {str(e)}")
    
    def commit_changes(self):
        """Commit staged changes"""
        message = self.commit_message.toPlainText().strip()
        
        if not message:
            show_message_dialog(
                self,
                "Validation Error",
                "Please enter a commit message.",
                msg_type="warning"
            )
            return
        
        try:
            # Stage files if needed
            if self.stage_all_check.isChecked():
                self.repo.git.add(A=True)
            
            # Commit
            self.repo.index.commit(message)
            
            show_message_dialog(
                self,
                "Success",
                "Changes committed successfully!"
            )
            
            # Reload changes
            self.load_changes()
            self.commit_message.clear()
            
        except Exception as e:
            show_message_dialog(
                self,
                "Commit Failed",
                f"Failed to commit changes:\n{str(e)}",
                msg_type="error"
            )
    
    def commit_and_push(self):
        """Commit and push changes"""
        message = self.commit_message.toPlainText().strip()
        
        if not message:
            show_message_dialog(
                self,
                "Validation Error",
                "Please enter a commit message.",
                msg_type="warning"
            )
            return
        
        try:
            # Stage files if needed
            if self.stage_all_check.isChecked():
                self.repo.git.add(A=True)
            
            # Check if there are changes to commit
            if not self.repo.is_dirty(untracked_files=True):
                show_message_dialog(
                    self,
                    "No Changes",
                    "No changes to commit.",
                    msg_type="warning"
                )
                return
            
            # Commit
            self.repo.index.commit(message)
            
            # Push
            current_branch = self.repo.active_branch.name
            origin = self.repo.remote('origin')
            
            # Confirm push
            confirmed = show_confirmation_dialog(
                self,
                "Push Changes",
                f"Push changes to remote branch '{current_branch}'?"
            )
            
            if not confirmed:
                show_message_dialog(
                    self,
                    "Committed",
                    "Changes committed locally but not pushed."
                )
                return
            
            origin.push(current_branch)
            
            show_message_dialog(
                self,
                "Success",
                f"Changes committed and pushed to {current_branch}!"
            )
            
            self.accept()
            
        except Exception as e:
            show_message_dialog(
                self,
                "Error",
                f"Failed to commit and push:\n{str(e)}",
                msg_type="error"
            )

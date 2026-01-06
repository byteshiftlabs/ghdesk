"""
Repository view widget
Displays list of repositories with actions
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from core.gh_wrapper import GHWrapper
from core.repo_manager import RepoManager


class LoadReposThread(QThread):
    """Background thread to load repositories"""
    repos_loaded = pyqtSignal(list)
    
    def __init__(self, gh: GHWrapper, is_local: bool, scan_path: str = None):
        super().__init__()
        self.gh = gh
        self.is_local = is_local
        self.scan_path = scan_path
        self.repo_manager = RepoManager()
    
    def run(self):
        if self.is_local:
            if self.scan_path:
                repos = self.repo_manager.scan_directory(self.scan_path)
            else:
                repos = []
        else:
            repos = self.gh.list_repos(limit=200)
        
        self.repos_loaded.emit(repos)


class RepoView(QWidget):
    """Widget for displaying repositories"""
    
    def __init__(self, gh: GHWrapper, repo_manager: RepoManager, is_local: bool = True):
        super().__init__()
        
        self.gh = gh
        self.repo_manager = repo_manager
        self.is_local = is_local
        self.repos = []
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Repository table
        self.table = QTableWidget()
        self.table.setColumnCount(5 if self.is_local else 6)
        
        if self.is_local:
            headers = ["Name", "Path", "Branch", "Status", "Remote"]
        else:
            headers = ["Name", "Owner", "Description", "Private", "Updated", "Actions"]
        
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        if not self.is_local:
            self.delete_btn = QPushButton("🗑️ Delete Selected")
            self.delete_btn.setObjectName("dangerButton")
            self.delete_btn.clicked.connect(self.delete_selected)
            button_layout.addWidget(self.delete_btn)
            
            self.clone_btn = QPushButton("⬇️ Clone Selected")
            self.clone_btn.clicked.connect(self.clone_selected)
            button_layout.addWidget(self.clone_btn)
        
        button_layout.addStretch()
    
    def load_repos(self):
        """Load repositories in background"""
        self.table.setRowCount(0)
        self.table.setSortingEnabled(False)
        
        self.load_thread = LoadReposThread(self.gh, self.is_local)
        self.load_thread.repos_loaded.connect(self.on_repos_loaded)
        self.load_thread.start()
    
    def scan_directory(self, path: str):
        """Scan directory for local repositories"""
        self.table.setRowCount(0)
        self.table.setSortingEnabled(False)
        
        self.load_thread = LoadReposThread(self.gh, True, scan_path=path)
        self.load_thread.repos_loaded.connect(self.on_repos_loaded)
        self.load_thread.start()
    
    def on_repos_loaded(self, repos: list):
        """Handle loaded repositories"""
        self.repos = repos
        self.populate_table(repos)
    
    def populate_table(self, repos: list):
        """Populate table with repository data"""
        self.table.setRowCount(len(repos))
        
        for row, repo in enumerate(repos):
            if self.is_local:
                self.table.setItem(row, 0, QTableWidgetItem(repo.get("name", "")))
                self.table.setItem(row, 1, QTableWidgetItem(repo.get("path", "")))
                self.table.setItem(row, 2, QTableWidgetItem(repo.get("branch", "")))
                self.table.setItem(row, 3, QTableWidgetItem(repo.get("status", "")))
                self.table.setItem(row, 4, QTableWidgetItem(repo.get("remote", "")))
            else:
                owner = repo.get("owner", {}).get("login", "") if isinstance(repo.get("owner"), dict) else ""
                
                self.table.setItem(row, 0, QTableWidgetItem(repo.get("name", "")))
                self.table.setItem(row, 1, QTableWidgetItem(owner))
                self.table.setItem(row, 2, QTableWidgetItem(repo.get("description", "")))
                self.table.setItem(row, 3, QTableWidgetItem("Yes" if repo.get("isPrivate") else "No"))
                self.table.setItem(row, 4, QTableWidgetItem(repo.get("updatedAt", "")[:10]))
        
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()
    
    def delete_selected(self):
        """Delete selected repository"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a repository to delete")
            return
        
        row = selected_rows[0].row()
        repo = self.repos[row]
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        repo_full = f"{owner}/{name}"
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {repo_full}?\nThis cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            result = self.gh.delete_repo(repo_full, confirm=True)
            if result["success"]:
                QMessageBox.information(self, "Success", f"Deleted {repo_full}")
                self.load_repos()
            else:
                QMessageBox.warning(self, "Delete Failed",
                                  f"Failed to delete repository:\n{result['error']}")
    
    def clone_selected(self):
        """Clone selected repository"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a repository to clone")
            return
        
        row = selected_rows[0].row()
        repo = self.repos[row]
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        repo_full = f"{owner}/{name}"
        
        from PyQt6.QtWidgets import QFileDialog
        from pathlib import Path
        
        directory = QFileDialog.getExistingDirectory(
            self, "Select Clone Destination",
            str(Path.home())
        )
        
        if directory:
            target_path = str(Path(directory) / name)
            result = self.gh.clone_repo(repo_full, target_path)
            
            if result["success"]:
                QMessageBox.information(self, "Success", f"Cloned to {target_path}")
            else:
                QMessageBox.warning(self, "Clone Failed",
                                  f"Failed to clone repository:\n{result['error']}")

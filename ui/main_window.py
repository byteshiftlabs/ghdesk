"""
Main application window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QToolBar, QStatusBar, QMessageBox,
    QPushButton, QLabel, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

from core.gh_wrapper import GHWrapper
from core.repo_manager import RepoManager
from ui.repo_view import RepoView
from ui.create_dialog import CreateRepoDialog


class AuthCheckThread(QThread):
    """Background thread to check GitHub authentication"""
    result = pyqtSignal(bool)
    
    def __init__(self, gh: GHWrapper):
        super().__init__()
        self.gh = gh
    
    def run(self):
        authenticated = self.gh.is_authenticated()
        self.result.emit(authenticated)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.gh = GHWrapper()
        self.repo_manager = RepoManager()
        self.authenticated = False
        
        self.init_ui()
        self.check_authentication()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ghdesk - GitHub Desktop Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Local repositories tab
        self.local_view = RepoView(self.gh, self.repo_manager, is_local=True)
        self.tabs.addTab(self.local_view, "Local Repositories")
        
        # GitHub repositories tab
        self.remote_view = RepoView(self.gh, self.repo_manager, is_local=False)
        self.tabs.addTab(self.remote_view, "GitHub Repositories")
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.auth_label = QLabel("Not authenticated")
        self.status_bar.addPermanentWidget(self.auth_label)
    
    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Login action
        self.login_action = QAction("Login", self)
        self.login_action.triggered.connect(self.login)
        toolbar.addAction(self.login_action)
        
        # Logout action
        self.logout_action = QAction("Logout", self)
        self.logout_action.triggered.connect(self.logout)
        self.logout_action.setEnabled(False)
        toolbar.addAction(self.logout_action)
        
        toolbar.addSeparator()
        
        # Scan local repos
        scan_action = QAction("Scan Directory", self)
        scan_action.triggered.connect(self.scan_directory)
        toolbar.addAction(scan_action)
        
        # Create repo
        create_action = QAction("Create Repository", self)
        create_action.triggered.connect(self.create_repository)
        toolbar.addAction(create_action)
        
        toolbar.addSeparator()
        
        # Refresh
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh)
        toolbar.addAction(refresh_action)
    
    def check_authentication(self):
        """Check GitHub authentication status in background"""
        self.status_bar.showMessage("Checking authentication...")
        
        self.auth_thread = AuthCheckThread(self.gh)
        self.auth_thread.result.connect(self.on_auth_checked)
        self.auth_thread.start()
    
    def on_auth_checked(self, authenticated: bool):
        """Handle authentication check result"""
        self.authenticated = authenticated
        
        if authenticated:
            self.auth_label.setText("✓ Authenticated")
            self.login_action.setEnabled(False)
            self.logout_action.setEnabled(True)
            self.status_bar.showMessage("Ready", 3000)
            
            # Load GitHub repos
            self.remote_view.load_repos()
        else:
            self.auth_label.setText("✗ Not authenticated")
            self.login_action.setEnabled(True)
            self.logout_action.setEnabled(False)
            self.status_bar.showMessage("Not authenticated with GitHub", 3000)
    
    def login(self):
        """Login to GitHub"""
        self.status_bar.showMessage("Opening browser for authentication...")
        result = self.gh.login(web=True)
        
        if result["success"]:
            QMessageBox.information(self, "Success", "Successfully authenticated with GitHub!")
            self.check_authentication()
        else:
            QMessageBox.warning(self, "Login Failed", 
                              f"Failed to login:\n{result['error']}")
    
    def logout(self):
        """Logout from GitHub"""
        reply = QMessageBox.question(
            self, "Confirm Logout",
            "Are you sure you want to logout from GitHub?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            result = self.gh.logout()
            if result["success"]:
                QMessageBox.information(self, "Success", "Successfully logged out")
                self.check_authentication()
            else:
                QMessageBox.warning(self, "Logout Failed",
                                  f"Failed to logout:\n{result['error']}")
    
    def scan_directory(self):
        """Scan directory for local repositories"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory to Scan",
            str(Path.home())
        )
        
        if directory:
            self.status_bar.showMessage(f"Scanning {directory}...")
            self.local_view.scan_directory(directory)
            self.status_bar.showMessage(f"Scan complete", 3000)
    
    def create_repository(self):
        """Open create repository dialog"""
        dialog = CreateRepoDialog(self.gh, self)
        if dialog.exec():
            self.refresh()
    
    def refresh(self):
        """Refresh current view"""
        current_widget = self.tabs.currentWidget()
        if current_widget:
            current_widget.load_repos()


# Import Path
from pathlib import Path

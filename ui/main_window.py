"""
Main application window
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QToolBar, QStatusBar, QMessageBox,
    QPushButton, QLabel, QFileDialog, QSplitter, QComboBox, QSizePolicy,
    QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

from core.gh_wrapper import GHWrapper
from core.repo_manager import RepoManager
from ui.repo_view import RepoView
from ui.create_dialog import CreateRepoDialog
from ui.file_tree import FileTreeWidget
from ui.repo_detail_view import RepoDetailView
from ui.themes import get_theme, THEMES


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
        self.setGeometry(100, 100, 1400, 800)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main widget with splitter
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(layout)
        
        # Create main horizontal splitter (file tree | tabs | details)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.main_splitter)
        
        # File tree on the left
        self.file_tree = FileTreeWidget()
        self.file_tree.directory_selected.connect(self.on_directory_selected)
        self.main_splitter.addWidget(self.file_tree)
        
        # Create tab widget in the center
        self.tabs = QTabWidget()
        self.main_splitter.addWidget(self.tabs)
        
        # Repository detail view on the right
        self.repo_detail_view = RepoDetailView(self.gh)
        self.main_splitter.addWidget(self.repo_detail_view)
        
        # Set splitter sizes: 220px for tree, 500px for tabs, 480px for details
        self.main_splitter.setSizes([220, 500, 480])
        
        # Local repositories tab
        self.local_view = RepoView(self.gh, self.repo_manager, is_local=True)
        self.local_view.repo_selected.connect(self.on_local_repo_selected)
        self.tabs.addTab(self.local_view, "💻 Local Repositories")
        
        # GitHub repositories tab
        self.remote_view = RepoView(self.gh, self.repo_manager, is_local=False)
        self.remote_view.repo_selected.connect(self.on_github_repo_selected)
        self.tabs.addTab(self.remote_view, "☁️ GitHub Repositories")
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.auth_label = QLabel("Not authenticated")
        self.auth_label.setStyleSheet("""
            background-color: transparent;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: 500;
        """)
        self.status_bar.addPermanentWidget(self.auth_label)
    
    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Login action
        self.login_action = QAction("🔑 Login", self)
        self.login_action.triggered.connect(self.login)
        toolbar.addAction(self.login_action)
        
        # Logout action
        self.logout_action = QAction("🚪 Logout", self)
        self.logout_action.triggered.connect(self.logout)
        self.logout_action.setEnabled(False)
        toolbar.addAction(self.logout_action)
        
        toolbar.addSeparator()
        
        # Create repo
        create_action = QAction("➕ Create Repository", self)
        create_action.triggered.connect(self.create_repository)
        toolbar.addAction(create_action)
        
        toolbar.addSeparator()
        
        # Refresh
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.triggered.connect(self.refresh)
        toolbar.addAction(refresh_action)
        
        # Add spacer to push theme selector to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)
        
        # Theme selector on the right
        theme_label = QLabel("🎨 Theme:")
        theme_label.setStyleSheet("padding-right: 8px;")
        toolbar.addWidget(theme_label)
        self.theme_combo = QComboBox()
        self.theme_combo.setMinimumWidth(120)
        for theme_id, theme_name in THEMES.items():
            self.theme_combo.addItem(theme_name, theme_id)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        toolbar.addWidget(self.theme_combo)
    
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
            self.auth_label.setStyleSheet("""
                background-color: #4caf50;
                color: #ffffff;
                padding: 6px 16px;
                border-radius: 4px;
                font-weight: 600;
                border: 2px solid #388e3c;
            """)
            self.login_action.setEnabled(False)
            self.logout_action.setEnabled(True)
            self.status_bar.showMessage("Ready", 3000)
            
            # Load GitHub repos
            self.remote_view.load_repos()
        else:
            self.auth_label.setText("✗ Not authenticated")
            self.auth_label.setStyleSheet("""
                background-color: #f44336;
                color: #ffffff;
                padding: 6px 16px;
                border-radius: 4px;
                font-weight: 600;
                border: 2px solid #d32f2f;
            """)
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
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Confirm Logout")
        msg_box.setText("Are you sure you want to logout from GitHub?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.button(QMessageBox.StandardButton.Yes).setText("Yes")
        msg_box.button(QMessageBox.StandardButton.No).setText("No")
        msg_box.setMinimumWidth(400)
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            result = self.gh.logout()
            if result["success"]:
                QMessageBox.information(self, "Success", "Successfully logged out")
                self.check_authentication()
            else:
                QMessageBox.warning(self, "Logout Failed",
                                  f"Failed to logout:\n{result['error']}")
    
    def on_directory_selected(self, path: str):
        """Handle directory selection from file tree"""
        path_obj = Path(path)
        
        # Check if it's a git repository
        if (path_obj / ".git").exists():
            # Load repo details in the right panel
            self.repo_detail_view.load_repo(path)
            self.status_bar.showMessage(f"Loaded repository: {path_obj.name}", 3000)
        else:
            # Scan directory for repositories
            self.status_bar.showMessage(f"Scanning {path}...")
            self.local_view.scan_directory(path)
            # Switch to local repositories tab
            self.tabs.setCurrentIndex(0)
            self.status_bar.showMessage(f"Found repositories in {path}", 3000)
    
    def on_local_repo_selected(self, path: str):
        """Handle click on a local repository"""
        self.repo_detail_view.load_repo(path)
        self.status_bar.showMessage(f"Loaded repository: {Path(path).name}", 3000)
    
    def on_github_repo_selected(self, repo_full_name: str):
        """Handle click on a GitHub repository"""
        self.repo_detail_view.load_github_repo(repo_full_name)
        self.status_bar.showMessage(f"Loaded repository: {repo_full_name}", 3000)
    
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
    
    def change_theme(self, index):
        """Change application theme"""
        theme_id = self.theme_combo.itemData(index)
        stylesheet = get_theme(theme_id)
        self.parent().setStyleSheet(stylesheet) if self.parent() else None
        QApplication.instance().setStyleSheet(stylesheet)


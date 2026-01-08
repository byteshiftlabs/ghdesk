"""
Repository detail view widget
Shows detailed information about a local repository with tabs
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
    QTableWidget, QTableWidgetItem, QTextEdit, QPushButton,
    QHeaderView, QGroupBox, QFormLayout, QFrame, QScrollArea,
    QInputDialog, QLineEdit, QDialog, QDialogButtonBox, QSplitter,
    QListWidget, QListWidgetItem, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QRect, QPoint
from PyQt6.QtGui import QFont, QCursor, QColor
import git

from core.gh_wrapper import GHWrapper
from ui.dialogs import show_message_dialog, show_confirmation_dialog
from ui.pr_list_widget import PRListWidget
from ui.pr_detail_view import PRDetailView
from ui.pr_create_dialog import CreatePRDialog
from ui.commit_push_dialog import CommitPushDialog


class LoadRepoDetailsThread(QThread):
    """Background thread to load repository details"""
    details_loaded = pyqtSignal(dict)
    
    def __init__(self, repo_path: str, gh: GHWrapper):
        super().__init__()
        self.repo_path = repo_path
        self.gh = gh
    
    def run(self):
        details = {
            "local": {},
            "remote": None,
            "commits": [],
            "branches": [],
            "remotes": [],
            "topics": [],
            "status": {},
            "error": None
        }
        
        try:
            repo = git.Repo(self.repo_path)
            
            # Basic info
            details["local"] = {
                "name": Path(self.repo_path).name,
                "path": self.repo_path,
                "branch": repo.active_branch.name if not repo.head.is_detached else f"detached@{repo.head.commit.hexsha[:7]}",
                "is_dirty": repo.is_dirty(untracked_files=True),
            }
            
            # Branches with their commits
            branches_with_commits = []
            for b in repo.branches:
                branch_info = {
                    "name": b.name,
                    "is_current": b == repo.active_branch if not repo.head.is_detached else False,
                    "commits": []
                }
                # Get last 10 commits for each branch
                try:
                    for commit in list(repo.iter_commits(b.name, max_count=10)):
                        branch_info["commits"].append({
                            "sha": commit.hexsha[:7],
                            "message": commit.message.strip().split("\n")[0][:60],
                            "author": commit.author.name,
                            "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M")
                        })
                except Exception:
                    pass
                branches_with_commits.append(branch_info)
            
            details["branches"] = branches_with_commits
            
            # Remotes
            repo_full_name = None
            for remote in repo.remotes:
                remote_info = {
                    "name": remote.name,
                    "url": remote.url
                }
                details["remotes"].append(remote_info)
                
                # Try to get GitHub info if it's a GitHub remote
                url = remote.url
                repo_full = None
                
                # Handle SSH URLs: git@github.com:owner/repo.git
                if url.startswith("git@github.com:"):
                    repo_path = url.replace("git@github.com:", "")
                    if repo_path.endswith(".git"):
                        repo_path = repo_path[:-4]
                    parts = repo_path.split("/")
                    if len(parts) >= 2:
                        repo_full = f"{parts[0]}/{parts[1]}"
                
                # Handle HTTPS URLs: https://github.com/owner/repo.git
                elif "github.com/" in url:
                    if url.endswith(".git"):
                        url = url[:-4]
                    parts = url.split("github.com/")[-1].split("/")
                    if len(parts) >= 2:
                        repo_full = f"{parts[0]}/{parts[1]}"
                
                # Store the first GitHub repo full name we find
                if repo_full and not repo_full_name:
                    repo_full_name = repo_full
                
                # Get remote info from GitHub
                if repo_full and details["remote"] is None:
                    remote_data = self.gh.get_repo(repo_full)
                    if remote_data:
                        details["remote"] = remote_data
            
            # Store repo full name in details
            if repo_full_name:
                details["repo_full_name"] = repo_full_name
            
            # Get topics from GitHub API if remote exists
            if details["remote"]:
                topics_data = details["remote"].get("repositoryTopics", [])
                details["topics"] = topics_data if isinstance(topics_data, list) else []
            
            # Remove commits from top level since they're now per branch
            details["commits"] = []
            
            # Status
            details["status"] = {
                "modified": [item.a_path for item in repo.index.diff(None)],
                "staged": [item.a_path for item in repo.index.diff("HEAD")] if not repo.head.is_detached else [],
                "untracked": repo.untracked_files
            }
            
        except git.InvalidGitRepositoryError:
            details["error"] = "Not a valid Git repository"
        except Exception as e:
            details["error"] = str(e)
        
        self.details_loaded.emit(details)


class RepoDetailView(QWidget):
    """Widget showing detailed repository information"""
    
    # Signal emitted when hide button is clicked
    hide_requested = pyqtSignal()
    
    def __init__(self, gh: GHWrapper):
        super().__init__()
        self.gh = gh
        self.current_path = None
        self.current_repo_full_name = None
        self.current_topics = []
        self.pr_list_widget = None
        self.pr_detail_view = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Header with repo name and hide button
        header_container = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_container.setLayout(header_layout)
        
        self.header = QLabel("Select a repository from the file tree")
        self.header.setStyleSheet("font-size: 16px; font-weight: 600;")
        header_layout.addWidget(self.header)
        
        header_layout.addStretch()
        
        # Hide button (X icon like VS Code)
        hide_btn = QPushButton("✕")
        hide_btn.setFixedSize(24, 24)
        hide_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 18px;
                color: #666;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.1);
                color: #000;
            }
        """)
        hide_btn.setToolTip("Hide panel")
        hide_btn.clicked.connect(self.hide_requested.emit)
        header_layout.addWidget(hide_btn)
        
        layout.addWidget(header_container)
        
        # Loading indicator
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Overview tab
        self.overview_tab = self.create_overview_tab()
        self.tabs.addTab(self.overview_tab, "Overview")
        
        # Status tab
        self.status_tab = self.create_status_tab()
        self.tabs.addTab(self.status_tab, "Status")
        
        # Activity tab (branches & commits)
        self.commits_tab = self.create_commits_tab()
        self.tabs.addTab(self.commits_tab, "Activity")
        
        # Topics tab
        self.tags_tab = self.create_tags_tab()
        self.tabs.addTab(self.tags_tab, "Topics")
        
        # Remotes tab
        self.remotes_tab = self.create_remotes_tab()
        self.tabs.addTab(self.remotes_tab, "Remotes")
        
        # Pull Requests tab
        self.pr_tab = self.create_pr_tab()
        self.tabs.addTab(self.pr_tab, "Pull Requests")
        
        # Hide tabs initially
        self.tabs.hide()
    
    def create_overview_tab(self) -> QWidget:
        """Create the overview tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)
        
        # Local info group
        local_group = QGroupBox("Local Repository")
        local_layout = QFormLayout()
        local_group.setLayout(local_layout)
        
        self.local_name = QLabel("-")
        self.local_path = QLabel("-")
        self.local_path.setWordWrap(True)
        self.local_branch = QLabel("-")
        self.local_status = QLabel("-")
        
        local_layout.addRow("Name:", self.local_name)
        local_layout.addRow("Path:", self.local_path)
        local_layout.addRow("Branch:", self.local_branch)
        local_layout.addRow("Status:", self.local_status)
        
        scroll_layout.addWidget(local_group)
        
        # Remote info group
        remote_group = QGroupBox("GitHub Repository")
        remote_layout = QFormLayout()
        remote_group.setLayout(remote_layout)
        
        self.remote_name = QLabel("-")
        self.remote_visibility = QLabel("-")
        self.remote_description = QLabel("-")
        self.remote_description.setWordWrap(True)
        self.remote_stars = QLabel("-")
        self.remote_forks = QLabel("-")
        self.remote_issues = QLabel("-")
        self.remote_url = QLabel("-")
        self.remote_url.setWordWrap(True)
        self.remote_url.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        remote_layout.addRow("Name:", self.remote_name)
        remote_layout.addRow("Visibility:", self.remote_visibility)
        remote_layout.addRow("Description:", self.remote_description)
        remote_layout.addRow("Stars:", self.remote_stars)
        remote_layout.addRow("Forks:", self.remote_forks)
        remote_layout.addRow("Open Issues:", self.remote_issues)
        remote_layout.addRow("URL:", self.remote_url)
        
        scroll_layout.addWidget(remote_group)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return widget
    
    def create_status_tab(self) -> QWidget:
        """Create the status tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        widget.setLayout(layout)
        
        # Commit message section
        commit_layout = QVBoxLayout()
        
        self.commit_message_input = QTextEdit()
        self.commit_message_input.setMaximumHeight(40)
        self.commit_message_input.setPlaceholderText("Enter commit message...")
        commit_layout.addWidget(self.commit_message_input)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.stage_all_check = QCheckBox("Stage all files")
        self.stage_all_check.setChecked(False)
        self.stage_all_check.setToolTip("Stage all modified files (ignores selection)")
        button_layout.addWidget(self.stage_all_check)
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all_status_files)
        button_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all_status_files)
        button_layout.addWidget(deselect_all_btn)
        
        button_layout.addStretch()
        
        self.refresh_status_btn = QPushButton("🔄 Refresh")
        self.refresh_status_btn.clicked.connect(self.refresh_status)
        button_layout.addWidget(self.refresh_status_btn)
        
        self.commit_btn = QPushButton("💾 Commit")
        self.commit_btn.clicked.connect(self.commit_changes)
        button_layout.addWidget(self.commit_btn)
        
        self.push_btn = QPushButton("⬆️ Push")
        self.push_btn.clicked.connect(self.push_changes)
        button_layout.addWidget(self.push_btn)
        
        commit_layout.addLayout(button_layout)
        layout.addLayout(commit_layout)
        
        # Splitter for files and diff
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left side - File list
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_widget.setLayout(left_layout)
        
        left_label = QLabel("Changed Files")
        left_label.setStyleSheet("font-weight: bold; padding: 5px;")
        left_layout.addWidget(left_label)
        
        self.status_file_list = QListWidget()
        self.status_file_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.status_file_list.itemClicked.connect(self.on_status_file_selected)
        left_layout.addWidget(self.status_file_list)
        
        splitter.addWidget(left_widget)
        
        # Right side - Diff viewer
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_widget.setLayout(right_layout)
        
        right_label = QLabel("Diff Preview")
        right_label.setStyleSheet("font-weight: bold; padding: 5px;")
        right_layout.addWidget(right_label)
        
        self.status_diff_viewer = QTextEdit()
        self.status_diff_viewer.setReadOnly(True)
        self.status_diff_viewer.setFont(QFont("Monospace", 9))
        right_layout.addWidget(self.status_diff_viewer)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 700])
        
        return widget
    
    def create_commits_tab(self) -> QWidget:
        """Create the branches and commits activity view"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Scroll area for branches and their commits
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.activity_container = QWidget()
        self.activity_layout = QVBoxLayout()
        self.activity_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.activity_layout.setSpacing(16)
        self.activity_container.setLayout(self.activity_layout)
        scroll.setWidget(self.activity_container)
        
        layout.addWidget(scroll)
        
        return widget
    

    def create_tags_tab(self) -> QWidget:
        """Create the topics/keywords tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Header with add button
        header_layout = QHBoxLayout()
        info_label = QLabel("GitHub repository topics/keywords")
        info_label.setStyleSheet("color: #888; font-size: 11px;")
        header_layout.addWidget(info_label)
        header_layout.addStretch()
        
        add_topic_btn = QPushButton("Add Topic")
        add_topic_btn.clicked.connect(self.add_topic)
        header_layout.addWidget(add_topic_btn)
        layout.addLayout(header_layout)
        
        # Scrollable area for topics
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(150)
        scroll.setMaximumHeight(400)
        
        # Container for topic badges
        self.topics_container = QWidget()
        self.topics_layout = QVBoxLayout()
        self.topics_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.topics_container.setLayout(self.topics_layout)
        scroll.setWidget(self.topics_container)
        
        layout.addWidget(scroll)
        
        return widget
    
    def create_remotes_tab(self) -> QWidget:
        """Create the remotes tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.remotes_table = QTableWidget()
        self.remotes_table.setColumnCount(2)
        self.remotes_table.setHorizontalHeaderLabels(["Name", "URL"])
        self.remotes_table.horizontalHeader().setStretchLastSection(True)
        self.remotes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.remotes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.remotes_table)
        
        return widget
    
    def create_pr_tab(self) -> QWidget:
        """Create the pull requests tab"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        
        # Left side - PR list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_panel.setLayout(left_layout)
        
        # Create PR button
        create_pr_btn = QPushButton("+ New Pull Request")
        create_pr_btn.clicked.connect(self.create_pr)
        left_layout.addWidget(create_pr_btn)
        
        # PR list widget
        self.pr_list_widget = None  # Will be initialized when repo is loaded
        left_layout.addWidget(QLabel("Loading..."))
        
        layout.addWidget(left_panel, 1)
        
        # Right side - PR details
        self.pr_detail_view = None  # Will be initialized when repo is loaded
        right_placeholder = QLabel("Select a PR to view details")
        right_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_placeholder.setStyleSheet("color: #888;")
        layout.addWidget(right_placeholder, 2)
        
        return widget
    
    def create_pr(self):
        """Open dialog to create a new pull request"""
        if not self.current_path or not self.current_repo_full_name:
            show_message_dialog(
                self,
                "Error",
                "Cannot create PR: Repository information not available",
                msg_type="error"
            )
            return
        
        dialog = CreatePRDialog(
            self.current_path,
            self.current_repo_full_name,
            self.gh,
            self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Refresh PR list
            if self.pr_list_widget:
                self.pr_list_widget.load_prs()
    
    def load_status_files(self):
        """Load modified files into status file list"""
        if not self.current_path:
            return
        
        try:
            repo = git.Repo(self.current_path)
            self.status_file_list.clear()
            
            # Get modified files
            modified = [item.a_path for item in repo.index.diff(None)]
            staged = [item.a_path for item in repo.index.diff("HEAD")] if not repo.head.is_detached else []
            untracked = repo.untracked_files
            
            # Add modified files
            for file_path in modified:
                item = QListWidgetItem(f"🔸 {file_path} (modified)")
                item.setData(Qt.ItemDataRole.UserRole, {"path": file_path, "type": "modified"})
                self.status_file_list.addItem(item)
            
            # Add staged files
            for file_path in staged:
                if file_path not in modified:
                    item = QListWidgetItem(f"✅ {file_path} (staged)")
                    item.setData(Qt.ItemDataRole.UserRole, {"path": file_path, "type": "staged"})
                    item.setForeground(QColor("#28a745"))
                    self.status_file_list.addItem(item)
            
            # Add untracked files
            for file_path in untracked:
                item = QListWidgetItem(f"❓ {file_path} (untracked)")
                item.setData(Qt.ItemDataRole.UserRole, {"path": file_path, "type": "untracked"})
                item.setForeground(QColor("#ffa500"))
                self.status_file_list.addItem(item)
            
            if self.status_file_list.count() == 0:
                item = QListWidgetItem("No changes detected")
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                self.status_file_list.addItem(item)
                self.commit_btn.setEnabled(False)
                self.push_btn.setEnabled(True)  # Can still push
            else:
                self.commit_btn.setEnabled(True)
                self.push_btn.setEnabled(True)
        except Exception as e:
            show_message_dialog(
                self,
                "Error",
                f"Failed to load status: {str(e)}",
                msg_type="error"
            )
    
    def on_status_file_selected(self, item: QListWidgetItem):
        """Show diff for selected file in status tab"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data or not self.current_path:
            return
        
        file_path = data["path"]
        file_type = data["type"]
        
        try:
            repo = git.Repo(self.current_path)
            
            if file_type == "untracked":
                # Show file content for untracked files
                full_path = Path(self.current_path) / file_path
                if full_path.exists() and full_path.is_file():
                    content = full_path.read_text()
                    diff_text = f"New file: {file_path}\n\n{content}"
                else:
                    diff_text = f"Cannot read file: {file_path}"
            else:
                # Show git diff
                diff = repo.git.diff(file_path)
                if not diff:
                    diff = f"No diff available for {file_path}"
                diff_text = diff
            
            self.status_diff_viewer.setPlainText(diff_text)
        except Exception as e:
            self.status_diff_viewer.setPlainText(f"Error loading diff: {str(e)}")
    
    def refresh_status(self):
        """Refresh status tab"""
        self.load_status_files()
        self.status_diff_viewer.clear()
    
    def select_all_status_files(self):
        """Select all files in status list"""
        for i in range(self.status_file_list.count()):
            item = self.status_file_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsSelectable:
                item.setSelected(True)
    
    def deselect_all_status_files(self):
        """Deselect all files in status list"""
        self.status_file_list.clearSelection()
    
    def commit_changes(self):
        """Commit changes"""
        if not self.current_path:
            return
        
        message = self.commit_message_input.toPlainText().strip()
        
        if not message:
            show_message_dialog(
                self,
                "Commit Message Required",
                "Please enter a commit message.",
                msg_type="warning"
            )
            return
        
        try:
            repo = git.Repo(self.current_path)
            
            # Get selected files
            selected_items = self.status_file_list.selectedItems()
            
            # Stage files based on selection or stage all
            if self.stage_all_check.isChecked():
                # Stage all files
                repo.git.add(A=True)
            elif selected_items:
                # Stage only selected files
                for item in selected_items:
                    data = item.data(Qt.ItemDataRole.UserRole)
                    if data:
                        file_path = data["path"]
                        repo.git.add(file_path)
            else:
                show_message_dialog(
                    self,
                    "No Selection",
                    "Please select files to commit or check 'Stage all files'.",
                    msg_type="warning"
                )
                return
            
            # Check if there are changes to commit
            if not repo.is_dirty() and not repo.untracked_files:
                show_message_dialog(
                    self,
                    "No Changes",
                    "No changes to commit.",
                    msg_type="warning"
                )
                return
            
            # Commit
            repo.index.commit(message)
            
            show_message_dialog(
                self,
                "Success",
                "Changes committed successfully!"
            )
            
            # Refresh status
            self.load_status_files()
            self.commit_message_input.clear()
            
        except Exception as e:
            show_message_dialog(
                self,
                "Commit Failed",
                f"Failed to commit changes:\n{str(e)}",
                msg_type="error"
            )
    
    def push_changes(self):
        """Push changes to remote"""
        if not self.current_path:
            return
        
        try:
            repo = git.Repo(self.current_path)
            current_branch = repo.active_branch.name
            origin = repo.remote('origin')
            
            # Check if branch exists on remote
            remote_branches = [ref.name.split('/')[-1] for ref in origin.refs]
            branch_exists = current_branch in remote_branches
            
            # Confirm push
            push_msg = f"Push changes to remote branch '{current_branch}'?"
            if not branch_exists:
                push_msg = f"Branch '{current_branch}' doesn't exist on remote.\nPush and set upstream?"
            
            confirmed = show_confirmation_dialog(
                self,
                "Push Changes",
                push_msg
            )
            
            if not confirmed:
                return
            
            # Push with --set-upstream if branch doesn't exist
            if not branch_exists:
                origin.push(refspec=f"{current_branch}:{current_branch}", set_upstream=True)
            else:
                origin.push(current_branch)
            
            show_message_dialog(
                self,
                "Success",
                f"Changes pushed to {current_branch}!"
            )
            
        except Exception as e:
            show_message_dialog(
                self,
                "Push Failed",
                f"Failed to push changes:\n{str(e)}",
                msg_type="error"
            )
    
    def load_repo(self, path: str):
        """Load repository details"""
        self.current_path = path
        
        # Check if it's a git repo
        git_dir = Path(path) / ".git"
        if not git_dir.exists():
            self.header.setText(f"{Path(path).name} (not a Git repository)")
            self.tabs.hide()
            return
        
        self.header.setText(f"{Path(path).name}")
        self.loading_label.show()
        self.tabs.hide()
        
        # Load details in background
        self.load_thread = LoadRepoDetailsThread(path, self.gh)
        self.load_thread.details_loaded.connect(self.on_details_loaded)
        self.load_thread.start()
    
    def on_details_loaded(self, details: dict):
        """Handle loaded repository details"""
        self.loading_label.hide()
        
        if details.get("error"):
            self.header.setText(f"Error: {details['error']}")
            return
        
        self.tabs.show()
        
        # Check if this is a local repo or GitHub-only repo
        is_local = details.get("local") is not None
        
        # Hide/show tabs based on repo type
        status_index = self.tabs.indexOf(self.status_tab)
        remotes_index = self.tabs.indexOf(self.remotes_tab)
        pr_index = self.tabs.indexOf(self.pr_tab)
        
        if is_local:
            if status_index == -1:
                self.tabs.insertTab(1, self.status_tab, "Status")
            if remotes_index == -1:
                self.tabs.addTab(self.remotes_tab, "Remotes")
            # Show PR tab for local repos
            if pr_index == -1:
                self.tabs.addTab(self.pr_tab, "Pull Requests")
        else:
            # GitHub-only repos: hide Status, Remotes, and PR tabs
            if status_index >= 0:
                self.tabs.removeTab(status_index)
            if remotes_index >= 0:
                self.tabs.removeTab(self.tabs.indexOf(self.remotes_tab))
            if pr_index >= 0:
                self.tabs.removeTab(self.tabs.indexOf(self.pr_tab))
        
        # Extract repo full name from details or remote info
        if details.get("repo_full_name"):
            # Use the repo name extracted from git remote URL
            self.current_repo_full_name = details["repo_full_name"]
        elif details.get("remote"):
            # Fallback: try to extract from GitHub API response
            remote_info = details["remote"]
            owner = remote_info.get("owner", {})
            owner_login = owner.get("login", "") if isinstance(owner, dict) else ""
            repo_name = remote_info.get("name", "")
            if owner_login and repo_name:
                self.current_repo_full_name = f"{owner_login}/{repo_name}"
            else:
                self.current_repo_full_name = None
        else:
            self.current_repo_full_name = None
        
        # Update overview tab - local info
        local = details.get("local", {})
        if is_local:
            self.local_name.setText(local.get("name", "-"))
            self.local_path.setText(local.get("path", "-"))
            self.local_branch.setText(f"{local.get('branch', '-')}")
            status_text = "Clean" if not local.get("is_dirty") else "Modified"
            self.local_status.setText(status_text)
        else:
            # GitHub-only repo, hide/disable local info
            self.local_name.setText("(GitHub repository)")
            self.local_path.setText("-")
            self.local_branch.setText("-")
            self.local_status.setText("-")
        
        # Update overview tab - remote info
        remote = details.get("remote")
        if remote:
            self.remote_name.setText(remote.get("name", "-"))
            visibility = "Private" if remote.get("isPrivate") else "Public"
            self.remote_visibility.setText(visibility)
            self.remote_description.setText(remote.get("description") or "(no description)")
            self.remote_stars.setText(f"{remote.get('stargazerCount', 0)}")
            self.remote_forks.setText(f"{remote.get('forkCount', 0)}")
            self.remote_issues.setText(f"{remote.get('issues', {}).get('totalCount', 0)}")
            self.remote_url.setText(remote.get("url", "-"))
        else:
            self.remote_name.setText("No GitHub remote found")
            self.remote_visibility.setText("-")
            self.remote_description.setText("-")
            self.remote_stars.setText("-")
            self.remote_forks.setText("-")
            self.remote_issues.setText("-")
            self.remote_url.setText("-")
        
        # Update status tab
        if is_local:
            self.load_status_files()
        
        # Update activity tab (branches and commits)
        self.display_activity(details)
        
        # Update topics tab
        self.current_topics = details.get("topics", [])
        self.display_topics()
        
        # Update remotes tab
        remotes = details.get("remotes", [])
        self.remotes_table.setRowCount(len(remotes))
        for row, remote in enumerate(remotes):
            self.remotes_table.setItem(row, 0, QTableWidgetItem(remote.get("name", "")))
            self.remotes_table.setItem(row, 1, QTableWidgetItem(remote.get("url", "")))
        
        # Initialize or update PR tab for local repos with GitHub remote
        if is_local and self.current_repo_full_name:
            # If widgets already exist, update them with new repo
            if self.pr_list_widget:
                self.update_pr_widgets()
            else:
                # First time initialization
                self.init_pr_widgets()
        else:
            # Clear PR widgets if not a local repo or no GitHub remote
            if self.pr_list_widget:
                self.clear_pr_widgets()
    
    def init_pr_widgets(self):
        """Initialize PR list and detail widgets"""
        if not self.current_repo_full_name:
            return
        
        # Get the PR tab layout
        pr_tab_layout = self.pr_tab.layout()
        
        # Clear existing widgets
        while pr_tab_layout.count():
            child = pr_tab_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create left panel with PR list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_panel.setLayout(left_layout)
        
        # Create PR button - only for local repositories
        if self.current_path:
            create_pr_btn = QPushButton("+ New Pull Request")
            create_pr_btn.clicked.connect(self.create_pr)
            left_layout.addWidget(create_pr_btn)
        else:
            # Show info label for GitHub-only repos
            info_label = QLabel("💡 Clone this repository locally to create pull requests")
            info_label.setWordWrap(True)
            info_label.setStyleSheet(
                "color: #666; font-size: 11px; padding: 8px; "
                "background-color: #f6f8fa; border-radius: 4px;"
            )
            left_layout.addWidget(info_label)
        
        # PR list
        self.pr_list_widget = PRListWidget(self.gh, self.current_repo_full_name, self)
        self.pr_list_widget.pr_selected.connect(self.on_pr_selected)
        left_layout.addWidget(self.pr_list_widget)
        
        pr_tab_layout.addWidget(left_panel, 1)
        
        # Create right panel with PR details
        # Pass is_local flag to enable/disable metadata management
        is_local_repo = bool(self.current_path)
        self.pr_detail_view = PRDetailView(
            self.gh, 
            self.current_repo_full_name, 
            is_local=is_local_repo,
            parent=self
        )
        self.pr_detail_view.pr_updated.connect(self.on_pr_updated)
        pr_tab_layout.addWidget(self.pr_detail_view, 2)
    
    def on_pr_selected(self, pr_number: int):
        """Handle PR selection"""
        if self.pr_detail_view:
            self.pr_detail_view.load_pr(pr_number)
    
    def on_pr_updated(self):
        """Handle PR update (merged, closed, etc.)"""
        if self.pr_list_widget:
            self.pr_list_widget.load_prs()
    
    def update_pr_widgets(self):
        """Update PR widgets with new repository"""
        if not self.current_repo_full_name:
            return
        
        # Update the repo name in existing widgets
        if self.pr_list_widget:
            self.pr_list_widget.repo_name = self.current_repo_full_name
            self.pr_list_widget.load_prs()
        
        if self.pr_detail_view:
            self.pr_detail_view.repo_name = self.current_repo_full_name
            self.pr_detail_view.is_local = bool(self.current_path)
            self.pr_detail_view.show_placeholder()
    
    def clear_pr_widgets(self):
        """Clear PR widgets"""
        if self.pr_list_widget:
            self.pr_list_widget.pr_list.clear()
        if self.pr_detail_view:
            self.pr_detail_view.show_placeholder()
    
    def clear(self):
        """Clear the view"""
        self.header.setText("Select a repository from the file tree")
        self.tabs.hide()
        self.current_path = None
    
    def load_github_repo(self, repo_full_name: str):
        """Load repository details from GitHub (for remote repos)"""
        self.current_path = None
        self.current_repo_full_name = repo_full_name
        self.loading_label.show()
        self.header.setText(f"{repo_full_name}")
        self.tabs.show()
        
        # Load GitHub repo info
        gh_info = self.gh.get_repo(repo_full_name)
        if gh_info:
            topics_data = gh_info.get("repositoryTopics", [])
            
            # Fetch commits from main branch only on GitHub
            commits_data = self.gh.get_commits(repo_full_name, branch="main", limit=20)
            commits = []
            for commit in commits_data:
                commits.append({
                    "sha": commit.get("sha", ""),
                    "message": commit.get("message", "").strip().split("\n")[0][:60],
                    "author": commit.get("author", ""),
                    "date": commit.get("date", "")[:16].replace("T", " ")  # Format: YYYY-MM-DD HH:MM
                })
            
            # For GitHub repos, only show main branch
            branches = [{"name": "main", "is_current": False, "commits": commits}]
            
            details = {
                "local": None,
                "remote": gh_info,
                "topics": topics_data if isinstance(topics_data, list) else [],
                "commits": commits,
                "branches": branches,
                "remotes": [],
                "status": {},
                "error": None
            }
            self.on_details_loaded(details)
        else:
            self.loading_label.hide()
            self.header.setText(f"Failed to load {repo_full_name}")
    
    def display_topics(self):
        """Display topics as interactive badges"""
        # Clear existing widgets
        while self.topics_layout.count():
            child = self.topics_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.current_topics:
            no_topics = QLabel("No topics set for this repository")
            no_topics.setStyleSheet("color: #888; padding: 16px; font-style: italic;")
            self.topics_layout.addWidget(no_topics)
            return
        
        # Create a simple vertical list of topics
        for topic in self.current_topics:
            topic_name = topic.get("name", "") if isinstance(topic, dict) else str(topic)
            if not topic_name:
                continue
            
            # Create horizontal container for each topic
            topic_row = QWidget()
            topic_row_layout = QHBoxLayout()
            topic_row_layout.setContentsMargins(4, 4, 4, 4)
            topic_row_layout.setSpacing(8)
            topic_row.setLayout(topic_row_layout)
            
            # Topic badge
            topic_label = QLabel(f" {topic_name} ")
            topic_label.setStyleSheet("""
                QLabel {
                    background: #0969da;
                    color: white;
                    padding: 6px 14px;
                    border-radius: 16px;
                    font-size: 13px;
                    font-weight: 500;
                }
            """)
            topic_row_layout.addWidget(topic_label)
            
            # Delete button (if applicable)
            if self.current_repo_full_name:
                delete_btn = QPushButton("Remove")
                delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        color: #cf222e;
                        border: 1px solid #cf222e;
                        border-radius: 6px;
                        padding: 4px 10px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background: #cf222e;
                        color: white;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, t=topic_name: self.remove_topic(t))
                topic_row_layout.addWidget(delete_btn)
            
            topic_row_layout.addStretch()
            self.topics_layout.addWidget(topic_row)
        
        self.topics_layout.addStretch()
    
    def add_topic(self):
        """Add a new topic to the repository"""
        if not self.current_repo_full_name:
            show_message_dialog(self, "Cannot Add Topic", "Topics can only be added to GitHub repositories.")
            return
        
        # Create custom input dialog
        print("[DIALOG] Creating inline 'Add Topic' dialog")
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Topic")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        dialog.setLayout(layout)
        
        # Main text
        main_label = QLabel("Add a new topic")
        main_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(main_label)
        
        # Info text
        info_label = QLabel("Enter topic name (lowercase, hyphens instead of spaces)")
        info_label.setStyleSheet("font-size: 11px; color: #666;")
        layout.addWidget(info_label)
        
        # Input field
        topic_input = QLineEdit()
        topic_input.setPlaceholderText("e.g., python, machine-learning")
        topic_input.setStyleSheet("padding: 4px; font-size: 12px;")
        layout.addWidget(topic_input)
        
        # Buttons
        button_box = QDialogButtonBox()
        add_btn = QPushButton("Add")
        add_btn.setMinimumWidth(70)
        add_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(70)
        cancel_btn.clicked.connect(dialog.reject)
        button_box.addButton(add_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addWidget(button_box)
        
        dialog.adjustSize()
        print("[DIALOG] Executing inline 'Add Topic' dialog")
        
        # Execute dialog
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        topic = topic_input.text()
        if topic:
            # Validate topic name
            topic = topic.lower().strip().replace(" ", "-")
            if not topic:
                return
            
            # Check if already exists
            existing_names = [t.get("name", "") if isinstance(t, dict) else str(t) 
                            for t in self.current_topics]
            if topic in existing_names:
                show_message_dialog(self, "Topic Exists", f"Topic '{topic}' already exists.")
                return
            
            # Add via GitHub API
            result = self.gh.add_topic(self.current_repo_full_name, topic)
            if result.get("success"):
                show_message_dialog(self, "Success", f"Topic '{topic}' added successfully")
                # Refresh repo details
                self.load_github_repo(self.current_repo_full_name)
            else:
                show_message_dialog(self, "Failed", "Failed to add topic", result.get('error', 'Unknown error'))
    
    def remove_topic(self, topic_name: str):
        """Remove a topic from the repository"""
        if not self.current_repo_full_name:
            return
        
        accepted = show_confirmation_dialog(
            self,
            "Remove Topic",
            f"Remove topic '{topic_name}'?",
            yes_text="Yes",
            no_text="No"
        )
        
        if accepted:
            result = self.gh.remove_topic(self.current_repo_full_name, topic_name)
            if result.get("success"):
                show_message_dialog(self, "Success", f"Topic '{topic_name}' removed successfully")
                # Refresh repo details
                self.load_github_repo(self.current_repo_full_name)
            else:
                show_message_dialog(self, "Failed", "Failed to remove topic", result.get('error', 'Unknown error'))
    
    def display_activity(self, details: dict):
        """Display branches with their commits"""
        # Clear existing widgets
        while self.activity_layout.count():
            child = self.activity_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        branches = details.get("branches", [])
        
        if not branches:
            no_activity = QLabel("No branch activity available")
            no_activity.setStyleSheet("color: #888; padding: 16px; font-style: italic;")
            self.activity_layout.addWidget(no_activity)
            return
        
        # Display each branch with its commits
        for branch_info in branches:
            branch_name = branch_info.get("name", "")
            is_current = branch_info.get("is_current", False)
            commits = branch_info.get("commits", [])
            
            # Branch header
            branch_header = QLabel()
            if is_current:
                branch_header.setText(f"{branch_name} (current)")
                branch_header.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        font-weight: bold;
                        color: #2ea44f;
                        padding: 8px;
                        background: rgba(46, 164, 79, 0.15);
                        border-left: 4px solid #2ea44f;
                    }
                """)
            else:
                branch_header.setText(f"{branch_name}")
                branch_header.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        font-weight: bold;
                        color: #58a6ff;
                        padding: 8px;
                        background: rgba(88, 166, 255, 0.15);
                        border-left: 4px solid #58a6ff;
                    }
                """)
            self.activity_layout.addWidget(branch_header)
            
            # Commits table for this branch
            if commits:
                commits_table = QTableWidget()
                commits_table.setColumnCount(4)
                commits_table.setHorizontalHeaderLabels(["SHA", "Message", "Author", "Date"])
                commits_table.horizontalHeader().setStretchLastSection(True)
                commits_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
                commits_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
                commits_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                commits_table.setMaximumHeight(min(len(commits) * 30 + 35, 300))
                
                commits_table.setRowCount(len(commits))
                for row, commit in enumerate(commits):
                    commits_table.setItem(row, 0, QTableWidgetItem(commit.get("sha", "")))
                    commits_table.setItem(row, 1, QTableWidgetItem(commit.get("message", "")))
                    commits_table.setItem(row, 2, QTableWidgetItem(commit.get("author", "")))
                    commits_table.setItem(row, 3, QTableWidgetItem(commit.get("date", "")))
                
                # Enable sorting AFTER populating the table
                commits_table.setSortingEnabled(True)
                
                self.activity_layout.addWidget(commits_table)
            else:
                no_commits = QLabel("  No commits")
                no_commits.setStyleSheet("color: #888; padding: 8px; font-style: italic;")
                self.activity_layout.addWidget(no_commits)
        
        self.activity_layout.addStretch()

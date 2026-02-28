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
    QInputDialog, QLineEdit, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QRect, QPoint
from PyQt6.QtGui import QFont, QCursor

from core.gh_wrapper import GHWrapper
from core.git_operations import load_repo_details
from ui.dialogs import show_message_dialog, show_confirmation_dialog
from ui.constants import (
    WIDGET_LIST_MAX_HEIGHT_MEDIUM, WIDGET_SCROLL_MAX_HEIGHT,
    WIDGET_BUTTON_MIN_WIDTH_SMALL, WIDGET_COMMITS_MAX_HEIGHT,
    WIDGET_COMMITS_ROW_HEIGHT, WIDGET_COMMITS_HEADER_HEIGHT
)
from ui.styles import (
    STYLE_HEADER_LARGE, STYLE_HIDE_BUTTON, STYLE_LABEL_MUTED,
    STYLE_LABEL_ITALIC_MUTED, STYLE_LABEL_ITALIC_COMPACT, STYLE_TOPIC_LABEL,
    STYLE_TOPIC_DELETE_BUTTON, STYLE_HEADER_SMALL, STYLE_LABEL_INFO,
    STYLE_INPUT_PADDED, STYLE_BRANCH_HEADER_DEFAULT, STYLE_BRANCH_HEADER_ACTIVE
)


class LoadRepoDetailsThread(QThread):
    """Background thread to load repository details"""
    details_loaded = pyqtSignal(dict)
    
    def __init__(self, repo_path: str, gh: GHWrapper):
        super().__init__()
        self.repo_path = repo_path
        self.gh = gh
    
    def run(self):
        """Load repository details using core business logic"""
        details = load_repo_details(self.repo_path, self.gh)
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
        self.header.setStyleSheet(STYLE_HEADER_LARGE)
        header_layout.addWidget(self.header)
        
        header_layout.addStretch()
        
        # Hide button (X icon like VS Code)
        hide_btn = QPushButton("✕")
        hide_btn.setFixedSize(24, 24)
        hide_btn.setStyleSheet(STYLE_HIDE_BUTTON)
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
        widget.setLayout(layout)
        
        # Modified files
        modified_group = QGroupBox("Modified Files")
        modified_layout = QVBoxLayout()
        modified_group.setLayout(modified_layout)
        self.modified_list = QTextEdit()
        self.modified_list.setReadOnly(True)
        self.modified_list.setMaximumHeight(WIDGET_LIST_MAX_HEIGHT_MEDIUM)
        modified_layout.addWidget(self.modified_list)
        layout.addWidget(modified_group)
        
        # Staged files
        staged_group = QGroupBox("Staged Files")
        staged_layout = QVBoxLayout()
        staged_group.setLayout(staged_layout)
        self.staged_list = QTextEdit()
        self.staged_list.setReadOnly(True)
        self.staged_list.setMaximumHeight(WIDGET_LIST_MAX_HEIGHT_MEDIUM)
        staged_layout.addWidget(self.staged_list)
        layout.addWidget(staged_group)
        
        # Untracked files
        untracked_group = QGroupBox("Untracked Files")
        untracked_layout = QVBoxLayout()
        untracked_group.setLayout(untracked_layout)
        self.untracked_list = QTextEdit()
        self.untracked_list.setReadOnly(True)
        self.untracked_list.setMaximumHeight(WIDGET_LIST_MAX_HEIGHT_MEDIUM)
        untracked_layout.addWidget(self.untracked_list)
        layout.addWidget(untracked_group)
        
        layout.addStretch()
        
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
        info_label.setStyleSheet(STYLE_LABEL_MUTED)
        header_layout.addWidget(info_label)
        header_layout.addStretch()
        
        add_topic_btn = QPushButton("Add Topic")
        add_topic_btn.clicked.connect(self.add_topic)
        header_layout.addWidget(add_topic_btn)
        layout.addLayout(header_layout)
        
        # Scrollable area for topics
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(WIDGET_LIST_MAX_HEIGHT_MEDIUM)
        scroll.setMaximumHeight(WIDGET_SCROLL_MAX_HEIGHT)
        
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
        
        if is_local:
            if status_index == -1:
                self.tabs.insertTab(1, self.status_tab, "Status")
            if remotes_index == -1:
                self.tabs.addTab(self.remotes_tab, "Remotes")
        else:
            if status_index >= 0:
                self.tabs.removeTab(status_index)
            if remotes_index >= 0:
                self.tabs.removeTab(self.tabs.indexOf(self.remotes_tab))
        
        # Extract repo full name from remote if available
        if details.get("remote"):
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
        status = details.get("status", {})
        modified = status.get("modified", [])
        self.modified_list.setText("\n".join(modified) if modified else "(no modified files)")
        
        staged = status.get("staged", [])
        self.staged_list.setText("\n".join(staged) if staged else "(no staged files)")
        
        untracked = status.get("untracked", [])
        self.untracked_list.setText("\n".join(untracked) if untracked else "(no untracked files)")
        
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
            no_topics.setStyleSheet(STYLE_LABEL_ITALIC_MUTED)
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
            topic_label.setStyleSheet(STYLE_TOPIC_LABEL)
            topic_row_layout.addWidget(topic_label)
            
            # Delete button (if applicable)
            if self.current_repo_full_name:
                delete_btn = QPushButton("Remove")
                delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                delete_btn.setStyleSheet(STYLE_TOPIC_DELETE_BUTTON)
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
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Topic")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        dialog.setLayout(layout)
        
        # Main text
        main_label = QLabel("Add a new topic")
        main_label.setStyleSheet(STYLE_HEADER_SMALL)
        layout.addWidget(main_label)
        
        # Info text
        info_label = QLabel("Enter topic name (lowercase, hyphens instead of spaces)")
        info_label.setStyleSheet(STYLE_LABEL_INFO)
        layout.addWidget(info_label)
        
        # Input field
        topic_input = QLineEdit()
        topic_input.setPlaceholderText("e.g., python, machine-learning")
        topic_input.setStyleSheet(STYLE_INPUT_PADDED)
        layout.addWidget(topic_input)
        
        # Buttons
        button_box = QDialogButtonBox()
        add_btn = QPushButton("Add")
        add_btn.setMinimumWidth(WIDGET_BUTTON_MIN_WIDTH_SMALL)
        add_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(WIDGET_BUTTON_MIN_WIDTH_SMALL)
        cancel_btn.clicked.connect(dialog.reject)
        button_box.addButton(add_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addWidget(button_box)
        
        dialog.adjustSize()
        
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
            no_activity.setStyleSheet(STYLE_LABEL_ITALIC_MUTED)
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
                branch_header.setStyleSheet(STYLE_BRANCH_HEADER_ACTIVE)
            else:
                branch_header.setText(f"{branch_name}")
                branch_header.setStyleSheet(STYLE_BRANCH_HEADER_DEFAULT)
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
                commits_table.setMaximumHeight(min(len(commits) * WIDGET_COMMITS_ROW_HEIGHT + WIDGET_COMMITS_HEADER_HEIGHT, WIDGET_COMMITS_MAX_HEIGHT))
                
                commits_table.setRowCount(len(commits))
                for row, commit in enumerate(commits):
                    commits_table.setItem(row, 0, QTableWidgetItem(commit.get("sha", "")))
                    commits_table.setItem(row, 1, QTableWidgetItem(commit.get("message", "")))
                    commits_table.setItem(row, 2, QTableWidgetItem(commit.get("author", "")))
                    commits_table.setItem(row, 3, QTableWidgetItem(commit.get("date", "")))
                
                self.activity_layout.addWidget(commits_table)
            else:
                no_commits = QLabel("  No commits")
                no_commits.setStyleSheet(STYLE_LABEL_ITALIC_COMPACT)
                self.activity_layout.addWidget(no_commits)
        
        self.activity_layout.addStretch()

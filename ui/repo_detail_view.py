"""
Repository detail view widget
Shows detailed information about a local repository with tabs
"""

from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView,
    QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from core.gh_wrapper import GHWrapper
from core.git_operations import load_repo_details
from ui.topic_manager import TopicManagerMixin
from ui.tab_builder import TabBuilderMixin
from ui.pr_list_widget import PRListWidget
from ui.pr_detail_view import PRDetailView
from ui.styles import (
    STYLE_HEADER_LARGE, STYLE_CLOSE_BUTTON,
    STYLE_EMPTY_STATE, STYLE_EMPTY_STATE_SMALL,
    STYLE_BRANCH_CURRENT, STYLE_BRANCH_OTHER
)
from ui.constants import (
    MARGIN_NONE, HEADER_PADDING, BUTTON_ICON_SIZE, COMMITS_TABLE_COLUMNS
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


class RepoDetailView(TabBuilderMixin, TopicManagerMixin, QWidget):
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
        layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
        self.setLayout(layout)

        # Header with repo name and hide button
        header_container = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(HEADER_PADDING, HEADER_PADDING, HEADER_PADDING, HEADER_PADDING)
        header_container.setLayout(header_layout)

        self.header = QLabel("Select a repository from the file tree")
        self.header.setStyleSheet(STYLE_HEADER_LARGE)
        header_layout.addWidget(self.header)

        header_layout.addStretch()

        # Hide button (X icon like VS Code)
        hide_btn = QPushButton("✕")
        hide_btn.setFixedSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE)
        hide_btn.setStyleSheet(STYLE_CLOSE_BUTTON)
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

        # Pull Requests tab (only shown for local repos with GitHub remote)
        self.prs_tab = self._create_prs_tab()
        self.tabs.addTab(self.prs_tab, "Pull Requests")

        # Hide tabs initially
        self.tabs.hide()

    def _create_prs_tab(self) -> QWidget:
        """Create the Pull Requests tab with list and detail views."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
        widget.setLayout(layout)

        # Splitter for list and detail
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # PR list (left side)
        self.pr_list_widget = PRListWidget()
        self.pr_list_widget.set_gh_wrapper(self.gh)
        self.pr_list_widget.pr_selected.connect(self._on_pr_selected)
        splitter.addWidget(self.pr_list_widget)

        # PR detail (right side)
        self.pr_detail_widget = PRDetailView()
        self.pr_detail_widget.set_gh_wrapper(self.gh)
        self.pr_detail_widget.pr_updated.connect(self._on_pr_updated)
        splitter.addWidget(self.pr_detail_widget)

        # Set initial sizes (40% list, 60% detail)
        splitter.setSizes([300, 450])

        layout.addWidget(splitter)
        return widget

    def _on_pr_selected(self, pr_number: int):
        """Handle PR selection from list."""
        if self.current_repo_full_name:
            self.pr_detail_widget.set_repo(self.current_repo_full_name)
            self.pr_detail_widget.load_pr(pr_number)

    def _on_pr_updated(self):
        """Handle PR state change (merged, closed, etc.)."""
        self.pr_list_widget.load_prs()

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
        prs_index = self.tabs.indexOf(self.prs_tab)

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

        # Show/hide Pull Requests tab (only for local repos with GitHub remote)
        has_github_remote = self.current_repo_full_name is not None
        if is_local and has_github_remote:
            if prs_index == -1:
                self.tabs.addTab(self.prs_tab, "Pull Requests")
            # Load PRs for this repo
            self.pr_list_widget.set_repo(self.current_repo_full_name)
            self.pr_detail_widget.set_repo(self.current_repo_full_name)
            self.pr_detail_widget.clear()
        else:
            if prs_index >= 0:
                self.tabs.removeTab(prs_index)

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
            no_activity.setStyleSheet(STYLE_EMPTY_STATE)
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
                branch_header.setStyleSheet(STYLE_BRANCH_CURRENT)
            else:
                branch_header.setText(f"{branch_name}")
                branch_header.setStyleSheet(STYLE_BRANCH_OTHER)
            self.activity_layout.addWidget(branch_header)

            # Commits table for this branch
            if commits:
                commits_table = QTableWidget()
                commits_table.setColumnCount(COMMITS_TABLE_COLUMNS)
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

                self.activity_layout.addWidget(commits_table)
            else:
                no_commits = QLabel("  No commits")
                no_commits.setStyleSheet(STYLE_EMPTY_STATE_SMALL)
                self.activity_layout.addWidget(no_commits)

        self.activity_layout.addStretch()

"""
Repository view widget
Displays list of repositories with actions
"""

import shutil
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from core.gh_wrapper import GHWrapper
from core.repo_manager import RepoManager
from ui.dialogs import show_message_dialog, show_confirmation_dialog
from ui.license_dialog import LicenseDialog
from ui.constants import (
    COLUMN_WIDTH_NAME, COLUMN_WIDTH_OWNER, COLUMN_WIDTH_PATH,
    COLUMN_WIDTH_DESCRIPTION, COLUMN_WIDTH_BRANCH, COLUMN_WIDTH_STATUS,
    COLUMN_WIDTH_VISIBILITY, COLUMN_WIDTH_LICENSE, COLUMN_WIDTH_UPDATED,
    COLUMN_WIDTH_REMOTE, LOCAL_REPO_COLUMNS, REMOTE_REPO_COLUMNS
)


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

    # Signal emitted when a repo is selected (double-clicked)
    repo_selected = pyqtSignal(str)  # Emits repo path for local, repo full name for remote

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
        self.table.setColumnCount(LOCAL_REPO_COLUMNS if self.is_local else REMOTE_REPO_COLUMNS)

        if self.is_local:
            headers = ["Name", "Path", "Branch", "Status", "Remote"]
        else:
            headers = ["Name", "Owner", "Description", "Visibility", "License", "Updated"]

        self.table.setHorizontalHeaderLabels(headers)
        # Set uniform column widths - all Interactive so user can resize
        header = self.table.horizontalHeader()
        col_count = LOCAL_REPO_COLUMNS if self.is_local else REMOTE_REPO_COLUMNS

        for i in range(col_count):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        self.table.setColumnWidth(0, COLUMN_WIDTH_NAME)
        self.table.setColumnWidth(1, COLUMN_WIDTH_PATH if self.is_local else COLUMN_WIDTH_OWNER)
        self.table.setColumnWidth(2, COLUMN_WIDTH_BRANCH if self.is_local else COLUMN_WIDTH_DESCRIPTION)
        self.table.setColumnWidth(3, COLUMN_WIDTH_STATUS if self.is_local else COLUMN_WIDTH_VISIBILITY)
        if not self.is_local:
            self.table.setColumnWidth(4, COLUMN_WIDTH_LICENSE)
            self.table.setColumnWidth(5, COLUMN_WIDTH_UPDATED)
        else:
            self.table.setColumnWidth(4, COLUMN_WIDTH_REMOTE)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.clicked.connect(self.on_row_clicked)

        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        if not self.is_local:
            self.license_btn = QPushButton("Change License")
            self.license_btn.clicked.connect(self.change_license)
            button_layout.addWidget(self.license_btn)

            self.visibility_btn = QPushButton("Change Visibility")
            self.visibility_btn.clicked.connect(self.change_visibility)
            button_layout.addWidget(self.visibility_btn)

            self.clone_btn = QPushButton("Clone Selected")
            self.clone_btn.clicked.connect(self.clone_selected)
            button_layout.addWidget(self.clone_btn)

            self.delete_btn = QPushButton("Delete Selected")
            self.delete_btn.setObjectName("dangerButton")
            self.delete_btn.clicked.connect(self.delete_selected)
            button_layout.addWidget(self.delete_btn)

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
                name_item = QTableWidgetItem(repo.get("name", ""))
                name_item.setData(Qt.ItemDataRole.UserRole + 1, row)  # Store original index
                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, QTableWidgetItem(repo.get("path", "")))
                self.table.setItem(row, 2, QTableWidgetItem(repo.get("branch", "")))
                self.table.setItem(row, 3, QTableWidgetItem(repo.get("status", "")))
                self.table.setItem(row, 4, QTableWidgetItem(repo.get("remote", "")))
            else:
                owner = repo.get("owner", {}).get("login", "") if isinstance(repo.get("owner"), dict) else ""
                is_private = repo.get("isPrivate")
                visibility_text = "Private" if is_private else "Public"

                name_item = QTableWidgetItem(repo.get("name", ""))
                # Store the full repo name and original index for later retrieval
                name_item.setData(Qt.ItemDataRole.UserRole, f"{owner}/{repo.get('name', '')}")
                name_item.setData(Qt.ItemDataRole.UserRole + 1, row)  # Store original index
                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, QTableWidgetItem(owner))
                self.table.setItem(row, 2, QTableWidgetItem(repo.get("description", "")))

                visibility_item = QTableWidgetItem(visibility_text)
                # Color code the visibility
                if is_private:
                    visibility_item.setForeground(Qt.GlobalColor.darkYellow)
                else:
                    visibility_item.setForeground(Qt.GlobalColor.darkGreen)
                self.table.setItem(row, 3, visibility_item)

                # License
                license_info = repo.get("licenseInfo", {})
                license_name = ""
                if license_info and isinstance(license_info, dict):
                    license_name = license_info.get("spdxId", "") or license_info.get("name", "")
                    if not license_name:
                        license_name = "-"
                else:
                    license_name = "-"
                self.table.setItem(row, 4, QTableWidgetItem(license_name))

                self.table.setItem(row, 5, QTableWidgetItem(repo.get("updatedAt", "")[:10]))

        self.table.setSortingEnabled(True)

    def _get_repo_for_row(self, visual_row: int):
        """Get repo dict for a visual row, accounting for sorting"""
        name_item = self.table.item(visual_row, 0)
        if name_item:
            original_index = name_item.data(Qt.ItemDataRole.UserRole + 1)
            if original_index is not None and 0 <= original_index < len(self.repos):
                return self.repos[original_index]
        return None

    def on_row_clicked(self, index):
        """Handle click on a row"""
        row = index.row()

        if self.is_local:
            repo = self._get_repo_for_row(row)
            if not repo:
                return
            path = repo.get("path", "")
            if path:
                self.repo_selected.emit(path)
        else:
            # For GitHub repos, get the full name from the table item data
            name_item = self.table.item(row, 0)
            if name_item:
                repo_full_name = name_item.data(Qt.ItemDataRole.UserRole)
                if repo_full_name:
                    self.repo_selected.emit(repo_full_name)

    def delete_selected(self):
        """Delete selected repository"""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            show_message_dialog(self, "No Selection", "Please select a repository to delete")
            return

        row = selected_rows[0].row()
        repo = self._get_repo_for_row(row)
        if not repo:
            show_message_dialog(self, "Error", "Could not find repository data")
            return
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        repo_full = f"{owner}/{name}"

        # Check if there's a local clone
        local_path = self._find_local_clone(name)

        accepted, delete_local = show_confirmation_dialog(
            self,
            "Confirm Delete",
            f"Delete repository '{repo_full}'?",
            f"<span style='color: #f44336;'><b>Warning:</b> This action cannot be undone!</span><br><br>"
            f"The remote repository on GitHub will be permanently deleted.",
            yes_text="Yes, Delete",
            no_text="Cancel",
            checkbox_text="Also delete local clone" if local_path else None
        )

        if accepted:
            result = self.gh.delete_repo(repo_full, confirm=True)
            if result["success"]:
                msg = f"Deleted remote repository: {repo_full}"

                # Delete local clone if checkbox was checked
                if delete_local and local_path:
                    try:
                        shutil.rmtree(local_path)
                        msg += f"\nDeleted local clone: {local_path}"
                    except Exception as e:
                        msg += f"\nFailed to delete local clone: {e}"

                show_message_dialog(self, "Success", msg)
                self.load_repos()
            else:
                show_message_dialog(self, "Delete Failed", "Failed to delete repository",
                                  result['error'])

    def _find_local_clone(self, repo_name: str) -> str:
        """Find local clone of a repository by name"""
        # Common locations to check
        home = Path.home()
        search_paths = [
            home / "Proyectos" / repo_name,
            home / "Projects" / repo_name,
            home / "repos" / repo_name,
            home / "git" / repo_name,
            home / repo_name,
            Path.cwd() / repo_name,
        ]

        for path in search_paths:
            if path.exists() and (path / ".git").exists():
                return str(path)

        return None

    def clone_selected(self):
        """Clone selected repository"""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            show_message_dialog(self, "No Selection", "Please select a repository to clone")
            return

        row = selected_rows[0].row()
        repo = self._get_repo_for_row(row)
        if not repo:
            show_message_dialog(self, "Error", "Could not find repository data")
            return
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        repo_full = f"{owner}/{name}"

        from PyQt6.QtWidgets import QFileDialog

        directory = QFileDialog.getExistingDirectory(
            self, "Select Clone Destination",
            str(Path.home())
        )

        if directory:
            target_path = str(Path(directory) / name)
            result = self.gh.clone_repo(repo_full, target_path)

            if result["success"]:
                show_message_dialog(self, "Success", f"Cloned to {target_path}")
            else:
                show_message_dialog(self, "Clone Failed", "Failed to clone repository",
                                  result['error'])

    def change_visibility(self):
        """Change visibility of selected repository"""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            show_message_dialog(self, "No Selection", "Please select a repository")
            return

        row = selected_rows[0].row()
        repo = self._get_repo_for_row(row)
        if not repo:
            show_message_dialog(self, "Error", "Could not find repository data")
            return
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        repo_full = f"{owner}/{name}"
        is_private = repo.get("isPrivate", False)

        # Ask for new visibility
        new_visibility = "public" if is_private else "private"

        accepted = show_confirmation_dialog(
            self,
            "Change Visibility",
            f"Change visibility of '{repo_full}'?",
            f"Current: <b>{'Private' if is_private else 'Public'}</b><br>"
            f"New: <b>{new_visibility.capitalize()}</b>",
            yes_text=f"Make {new_visibility.capitalize()}",
            no_text="Cancel"
        )

        if accepted:
            result = self.gh.edit_repo(repo_full, visibility=new_visibility)

            if result["success"]:
                show_message_dialog(self, "Success",
                                      f"Repository is now {new_visibility}")
                self.load_repos()
            else:
                show_message_dialog(self, "Failed", "Failed to change visibility",
                                  result['error'])

    def change_license(self):
        """Change license of selected repository"""
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            show_message_dialog(self, "No Selection", "Please select a repository")
            return

        row = selected_rows[0].row()
        repo = self._get_repo_for_row(row)
        if not repo:
            show_message_dialog(self, "Error", "Could not find repository data")
            return
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        repo_full = f"{owner}/{name}"

        # Get current license
        current_license = None
        license_info = repo.get("licenseInfo") or {}
        if license_info:
            current_license = license_info.get("spdxId") or license_info.get("name")

        # Show license dialog
        dialog = LicenseDialog(repo_full, current_license, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_license = dialog.get_selected_license()

            if selected_license:
                # Apply the license
                result = self.gh.change_license(repo_full, selected_license)

                if result.get("success"):
                    show_message_dialog(
                        self, "Success",
                        f"License changed to {selected_license.upper()}",
                        "The LICENSE file has been updated in the repository."
                    )
                    self.load_repos()
                else:
                    show_message_dialog(
                        self, "Failed",
                        "Failed to change license",
                        result.get('error', 'Unknown error')
                    )

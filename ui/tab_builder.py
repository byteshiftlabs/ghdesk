"""
Tab builder mixin for RepoDetailView.
Provides methods to create the various tabs in the detail view.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTextEdit, QPushButton,
    QGroupBox, QFormLayout, QScrollArea
)
from PyQt6.QtCore import Qt

from ui.flow_layout import FlowLayout
from ui.styles import STYLE_INFO_TEXT_MUTED
from ui.constants import (
    MARGIN_MEDIUM, SPACING_MEDIUM, SPACING_XLARGE,
    LIST_MAX_HEIGHT_MEDIUM, SCROLL_MIN_HEIGHT, SCROLL_MAX_HEIGHT,
    REMOTES_TABLE_COLUMNS
)


class TabBuilderMixin:
    """
    Mixin providing tab creation methods for RepoDetailView.

    Requires the host class to:
    - Have an add_topic() method (from TopicManagerMixin)
    - Set widget attributes on self (local_name, remote_name, etc.)
    """

    def create_overview_tab(self) -> QWidget:
        """Create the overview tab with local and remote repository info."""
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
        """Create the status tab showing modified, staged, and untracked files."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Modified files
        modified_group = QGroupBox("Modified Files")
        modified_layout = QVBoxLayout()
        modified_group.setLayout(modified_layout)
        self.modified_list = QTextEdit()
        self.modified_list.setReadOnly(True)
        self.modified_list.setMaximumHeight(LIST_MAX_HEIGHT_MEDIUM)
        modified_layout.addWidget(self.modified_list)
        layout.addWidget(modified_group)

        # Staged files
        staged_group = QGroupBox("Staged Files")
        staged_layout = QVBoxLayout()
        staged_group.setLayout(staged_layout)
        self.staged_list = QTextEdit()
        self.staged_list.setReadOnly(True)
        self.staged_list.setMaximumHeight(LIST_MAX_HEIGHT_MEDIUM)
        staged_layout.addWidget(self.staged_list)
        layout.addWidget(staged_group)

        # Untracked files
        untracked_group = QGroupBox("Untracked Files")
        untracked_layout = QVBoxLayout()
        untracked_group.setLayout(untracked_layout)
        self.untracked_list = QTextEdit()
        self.untracked_list.setReadOnly(True)
        self.untracked_list.setMaximumHeight(LIST_MAX_HEIGHT_MEDIUM)
        untracked_layout.addWidget(self.untracked_list)
        layout.addWidget(untracked_group)

        layout.addStretch()

        return widget

    def create_commits_tab(self) -> QWidget:
        """Create the branches and commits activity view."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Scroll area for branches and their commits
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.activity_container = QWidget()
        self.activity_layout = QVBoxLayout()
        self.activity_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.activity_layout.setSpacing(SPACING_XLARGE)
        self.activity_container.setLayout(self.activity_layout)
        scroll.setWidget(self.activity_container)

        layout.addWidget(scroll)

        return widget

    def create_tags_tab(self) -> QWidget:
        """Create the topics/keywords tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Header with add button
        header_layout = QHBoxLayout()
        info_label = QLabel("GitHub repository topics/keywords")
        info_label.setStyleSheet(STYLE_INFO_TEXT_MUTED)
        header_layout.addWidget(info_label)
        header_layout.addStretch()

        add_topic_btn = QPushButton("Add Topic")
        add_topic_btn.clicked.connect(self.add_topic)
        header_layout.addWidget(add_topic_btn)
        layout.addLayout(header_layout)

        # Scrollable area for topics
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(SCROLL_MIN_HEIGHT)
        scroll.setMaximumHeight(SCROLL_MAX_HEIGHT)

        # Container for topic badges using flow layout
        self.topics_container = QWidget()
        self.topics_layout = FlowLayout(margin=MARGIN_MEDIUM, spacing=SPACING_MEDIUM)
        self.topics_container.setLayout(self.topics_layout)
        scroll.setWidget(self.topics_container)

        layout.addWidget(scroll)
        layout.addStretch()

        return widget

    def create_remotes_tab(self) -> QWidget:
        """Create the remotes tab showing configured git remotes."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.remotes_table = QTableWidget()
        self.remotes_table.setColumnCount(REMOTES_TABLE_COLUMNS)
        self.remotes_table.setHorizontalHeaderLabels(["Name", "URL"])
        self.remotes_table.horizontalHeader().setStretchLastSection(True)
        self.remotes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.remotes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.remotes_table)

        return widget

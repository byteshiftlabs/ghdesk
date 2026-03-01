"""
Topic management mixin for repository views
Handles display and CRUD operations for GitHub repository topics
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

from ui.dialogs import show_message_dialog, show_confirmation_dialog
from ui.styles import (
    STYLE_HEADER_SMALL, STYLE_INFO_TEXT, STYLE_INPUT, STYLE_EMPTY_STATE,
    STYLE_TOPIC_BADGE, STYLE_TOPIC_BADGE_FULL, STYLE_TOPIC_REMOVE_BTN
)
from ui.constants import (
    MARGIN_NONE, MARGIN_LARGE, SPACING_NONE, SPACING_MEDIUM,
    BUTTON_ICON_SIZE, BUTTON_MIN_WIDTH_SMALL
)


class TopicManagerMixin:
    """
    Mixin class for managing GitHub repository topics.

    Requires the following attributes on the class using this mixin:
    - topics_layout: FlowLayout for topic badges
    - current_topics: list of topic dicts
    - current_repo_full_name: str or None
    - gh: GHWrapper instance
    - load_github_repo(name): method to reload repo data
    """

    def display_topics(self):
        """Display topics as compact flowing badges"""
        # Clear existing widgets
        while self.topics_layout.count():
            child = self.topics_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.current_topics:
            no_topics = QLabel("No topics set for this repository")
            no_topics.setStyleSheet(STYLE_EMPTY_STATE)
            self.topics_layout.addWidget(no_topics)
            return

        # Create compact badges that flow horizontally
        for topic in self.current_topics:
            topic_name = topic.get("name", "") if isinstance(topic, dict) else str(topic)
            if not topic_name:
                continue

            # Create compact badge container
            badge = QWidget()
            badge_layout = QHBoxLayout()
            badge_layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
            badge_layout.setSpacing(SPACING_NONE)
            badge.setLayout(badge_layout)

            # Topic text label
            topic_label = QLabel(f" {topic_name} ")
            topic_label.setStyleSheet(STYLE_TOPIC_BADGE)
            badge_layout.addWidget(topic_label)

            # Inline X button for removal
            if self.current_repo_full_name:
                x_btn = QPushButton("×")
                x_btn.setFixedSize(BUTTON_ICON_SIZE, BUTTON_ICON_SIZE)
                x_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                x_btn.setStyleSheet(STYLE_TOPIC_REMOVE_BTN)
                x_btn.clicked.connect(lambda checked, t=topic_name: self.remove_topic(t))
                badge_layout.addWidget(x_btn)
            else:
                # Round right side if no X button
                topic_label.setStyleSheet(STYLE_TOPIC_BADGE_FULL)

            self.topics_layout.addWidget(badge)

    def add_topic(self):
        """Add a new topic to the repository"""
        if not self.current_repo_full_name:
            show_message_dialog(self, "Cannot Add Topic", "Topics can only be added to GitHub repositories.")
            return

        # Create custom input dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Topic")

        layout = QVBoxLayout()
        layout.setContentsMargins(MARGIN_LARGE, MARGIN_LARGE, MARGIN_LARGE, MARGIN_LARGE)
        layout.setSpacing(SPACING_MEDIUM)
        dialog.setLayout(layout)

        # Main text
        main_label = QLabel("Add a new topic")
        main_label.setStyleSheet(STYLE_HEADER_SMALL)
        layout.addWidget(main_label)

        # Info text
        info_label = QLabel("Enter topic name (lowercase, hyphens instead of spaces)")
        info_label.setStyleSheet(STYLE_INFO_TEXT)
        layout.addWidget(info_label)

        # Input field
        topic_input = QLineEdit()
        topic_input.setPlaceholderText("e.g., python, machine-learning")
        topic_input.setStyleSheet(STYLE_INPUT)
        layout.addWidget(topic_input)

        # Buttons
        button_box = QDialogButtonBox()
        add_btn = QPushButton("Add")
        add_btn.setMinimumWidth(BUTTON_MIN_WIDTH_SMALL)
        add_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(BUTTON_MIN_WIDTH_SMALL)
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

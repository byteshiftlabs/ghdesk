"""
License selection dialog
Allows users to view and select licenses for their repositories
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QTextEdit, QSplitter,
    QGroupBox, QScrollArea, QWidget, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QShowEvent

from core.licenses import LICENSES, LICENSE_ORDER, get_license_by_id
from ui.dialogs import center_dialog_on_parent
from ui.styles import (
    STYLE_HEADER_MEDIUM, STYLE_INFO_TEXT_MUTED, STYLE_LABEL_BOLD_SMALL,
    STYLE_HEADER_LARGE, STYLE_DESCRIPTION, STYLE_NORMAL_TEXT, get_info_box_style
)
from ui.constants import (
    LICENSE_DIALOG_WIDTH, LICENSE_DIALOG_HEIGHT, LICENSE_SPLITTER_LEFT,
    LICENSE_SPLITTER_RIGHT, LICENSE_LIST_MIN_WIDTH, MARGIN_NONE, MARGIN_SMALL,
    MARGIN_MEDIUM, MARGIN_XLARGE, SPACING_SMALL, SPACING_MEDIUM, SPACING_LARGE,
    BUTTON_MIN_WIDTH_MEDIUM, BUTTON_MIN_WIDTH_LARGE
)


class LicenseDialog(QDialog):
    """Dialog for selecting and applying a license to a repository"""

    def __init__(self, repo_name: str, current_license: str = None, parent=None):
        super().__init__(parent)

        self.repo_name = repo_name
        self.current_license = current_license
        self.selected_license = None
        self._centered = False

        self.init_ui()

    def showEvent(self, event: QShowEvent):
        """Override showEvent to center dialog on parent."""
        super().showEvent(event)
        if not self._centered:
            center_dialog_on_parent(self)
            self._centered = True

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"Change License - {self.repo_name}")
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(LICENSE_DIALOG_WIDTH, LICENSE_DIALOG_HEIGHT)

        layout = QVBoxLayout()
        layout.setContentsMargins(MARGIN_XLARGE, MARGIN_XLARGE, MARGIN_XLARGE, MARGIN_XLARGE)
        layout.setSpacing(SPACING_LARGE)
        self.setLayout(layout)

        # Header
        header = QLabel("Select a License")
        header.setStyleSheet(STYLE_HEADER_MEDIUM)
        layout.addWidget(header)

        if self.current_license:
            current_label = QLabel(f"Current license: {self.current_license}")
            current_label.setStyleSheet(STYLE_INFO_TEXT_MUTED)
            layout.addWidget(current_label)

        # Main content with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter, 1)

        # Left side - License list
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
        left_widget.setLayout(left_layout)

        list_label = QLabel("Available Licenses")
        list_label.setStyleSheet(STYLE_LABEL_BOLD_SMALL)
        left_layout.addWidget(list_label)

        self.license_list = QListWidget()
        self.license_list.setMinimumWidth(LICENSE_LIST_MIN_WIDTH)
        self.populate_license_list()
        self.license_list.currentItemChanged.connect(self.on_license_selected)
        left_layout.addWidget(self.license_list)

        splitter.addWidget(left_widget)

        # Right side - License details
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
        right_layout.setSpacing(SPACING_MEDIUM)
        right_widget.setLayout(right_layout)

        # Detail scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout()
        self.detail_layout.setContentsMargins(MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM)
        self.detail_layout.setSpacing(SPACING_LARGE)
        self.detail_widget.setLayout(self.detail_layout)

        scroll.setWidget(self.detail_widget)
        right_layout.addWidget(scroll)

        splitter.addWidget(right_widget)
        splitter.setSizes([LICENSE_SPLITTER_LEFT, LICENSE_SPLITTER_RIGHT])

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(BUTTON_MIN_WIDTH_MEDIUM)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        self.apply_btn = QPushButton("Apply License")
        self.apply_btn.setMinimumWidth(BUTTON_MIN_WIDTH_LARGE)
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.apply_btn)

        layout.addLayout(button_layout)

        # Select first item
        if self.license_list.count() > 0:
            self.license_list.setCurrentRow(0)

    def populate_license_list(self):
        """Populate the license list widget"""
        for license_key in LICENSE_ORDER:
            license_info = LICENSES.get(license_key, {})
            item = QListWidgetItem(license_info.get("name", license_key))
            item.setData(Qt.ItemDataRole.UserRole, license_key)

            # Highlight current license
            if self.current_license:
                if (license_key.lower() == self.current_license.lower() or
                    license_info.get("spdx_id", "").lower() == self.current_license.lower()):
                    item.setBackground(Qt.GlobalColor.darkGreen)

            self.license_list.addItem(item)

    def on_license_selected(self, current, previous):
        """Handle license selection change"""
        if not current:
            return

        license_key = current.data(Qt.ItemDataRole.UserRole)
        self.selected_license = license_key
        self.apply_btn.setEnabled(True)

        self.show_license_details(license_key)

    def show_license_details(self, license_key: str):
        """Display details for the selected license"""
        # Clear existing details
        while self.detail_layout.count():
            child = self.detail_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        license_info = LICENSES.get(license_key, {})

        # License name
        name_label = QLabel(license_info.get("name", license_key))
        name_label.setStyleSheet(STYLE_HEADER_LARGE)
        name_label.setWordWrap(True)
        self.detail_layout.addWidget(name_label)

        # SPDX ID
        spdx_label = QLabel(f"SPDX ID: {license_info.get('spdx_id', 'N/A')}")
        spdx_label.setStyleSheet(STYLE_INFO_TEXT_MUTED)
        self.detail_layout.addWidget(spdx_label)

        # Description
        desc_label = QLabel(license_info.get("description", ""))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(STYLE_DESCRIPTION)
        self.detail_layout.addWidget(desc_label)

        # Best for
        if "best_for" in license_info:
            best_box = self.create_info_box("Best For", [license_info["best_for"]], "#2196F3")
            self.detail_layout.addWidget(best_box)

        # Permissions
        if license_info.get("permissions"):
            perm_box = self.create_info_box("Permissions", license_info["permissions"], "#4CAF50")
            self.detail_layout.addWidget(perm_box)

        # Conditions
        if license_info.get("conditions"):
            cond_box = self.create_info_box("Conditions", license_info["conditions"], "#FF9800")
            self.detail_layout.addWidget(cond_box)

        # Limitations
        if license_info.get("limitations"):
            limit_box = self.create_info_box("Limitations", license_info["limitations"], "#f44336")
            self.detail_layout.addWidget(limit_box)

        # Pros
        if license_info.get("pros"):
            pros_box = self.create_info_box("Pros", license_info["pros"], "#4CAF50")
            self.detail_layout.addWidget(pros_box)

        # Cons
        if license_info.get("cons"):
            cons_box = self.create_info_box("Cons", license_info["cons"], "#f44336")
            self.detail_layout.addWidget(cons_box)

        self.detail_layout.addStretch()

    def create_info_box(self, title: str, items: list, color: str) -> QGroupBox:
        """Create a styled info box with a list of items"""
        box = QGroupBox(title)
        box.setStyleSheet(get_info_box_style(color))

        box_layout = QVBoxLayout()
        box_layout.setContentsMargins(MARGIN_MEDIUM, MARGIN_SMALL, MARGIN_MEDIUM, MARGIN_MEDIUM)
        box_layout.setSpacing(SPACING_SMALL)
        box.setLayout(box_layout)

        for item in items:
            item_label = QLabel(f"• {item}")
            item_label.setWordWrap(True)
            item_label.setStyleSheet(STYLE_NORMAL_TEXT)
            box_layout.addWidget(item_label)

        return box

    def get_selected_license(self) -> str:
        """Return the selected license key"""
        return self.selected_license

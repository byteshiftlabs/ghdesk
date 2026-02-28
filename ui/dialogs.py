"""
Custom dialog helpers for consistent styling across the application.
All dialogs follow the same compact design pattern.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, 
    QDialogButtonBox, QCheckBox, QSizePolicy, QApplication, QStyle
)
from PyQt6.QtCore import Qt, QTimer
from ui.styles import STYLE_HEADER_SMALL, STYLE_INFO_TEXT
from ui.constants import MARGIN_LARGE, SPACING_MEDIUM, BUTTON_MIN_WIDTH_SMALL


def center_dialog_on_parent(dialog: QDialog):
    """Center a dialog on its parent window.
    
    Uses frameGeometry() to account for window decorations and ensures
    the dialog is properly sized before positioning.
    """
    # Ensure dialog has been styled and has final size
    dialog.ensurePolished()
    dialog.adjustSize()
    
    if dialog.parent() is None:
        # Center on screen if no parent
        screen = QApplication.primaryScreen().geometry()
        frame_geo = dialog.frameGeometry()
        frame_geo.moveCenter(screen.center())
        dialog.move(frame_geo.topLeft())
    else:
        # Center on parent - use frameGeometry to include decorations
        parent_geometry = dialog.parent().frameGeometry()
        dialog_geometry = dialog.frameGeometry()
        
        # Calculate center position using QRect operations
        dialog_geometry.moveCenter(parent_geometry.center())
        dialog.move(dialog_geometry.topLeft())


def show_message_dialog(parent, title: str, main_text: str, info_text: str = None,
                        msg_type: str = "info") -> None:
    """
    Show a compact message dialog (info, warning, error).
    
    Args:
        parent: Parent widget
        title: Dialog window title
        main_text: Bold main message
        info_text: Optional additional info text
        msg_type: "info", "warning", or "error"
    """
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    
    # Set window modality to force GNOME to respect positioning better
    dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(MARGIN_LARGE, MARGIN_LARGE, MARGIN_LARGE, MARGIN_LARGE)
    layout.setSpacing(SPACING_MEDIUM)
    dialog.setLayout(layout)
    
    # Main text
    main_label = QLabel(main_text)
    main_label.setStyleSheet(STYLE_HEADER_SMALL)
    main_label.setWordWrap(True)
    layout.addWidget(main_label)
    
    # Info text (optional)
    if info_text:
        info_label = QLabel(info_text)
        info_label.setStyleSheet(STYLE_INFO_TEXT)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(info_label)
    
    # OK button
    button_box = QDialogButtonBox()
    ok_btn = QPushButton("OK")
    ok_btn.setMinimumWidth(BUTTON_MIN_WIDTH_SMALL)
    ok_btn.clicked.connect(dialog.accept)
    button_box.addButton(ok_btn, QDialogButtonBox.ButtonRole.AcceptRole)
    layout.addWidget(button_box)
    
    # Center on parent (handles sizing internally)
    center_dialog_on_parent(dialog)
    
    dialog.exec()


def show_confirmation_dialog(parent, title: str, main_text: str, info_text: str = None,
                              yes_text: str = "Yes", no_text: str = "No",
                              checkbox_text: str = None) -> tuple:
    """
    Show a compact confirmation dialog.
    
    Args:
        parent: Parent widget
        title: Dialog window title
        main_text: Bold main message
        info_text: Optional additional info text
        yes_text: Text for the accept button
        no_text: Text for the reject button
        checkbox_text: Optional checkbox text
        
    Returns:
        (accepted: bool, checkbox_checked: bool) if checkbox_text provided
        accepted: bool if no checkbox
    """
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    
    # Set window modality to force GNOME to respect positioning better
    dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(MARGIN_LARGE, MARGIN_LARGE, MARGIN_LARGE, MARGIN_LARGE)
    layout.setSpacing(SPACING_MEDIUM)
    dialog.setLayout(layout)
    
    # Main text
    main_label = QLabel(main_text)
    main_label.setStyleSheet(STYLE_HEADER_SMALL)
    main_label.setWordWrap(True)
    layout.addWidget(main_label)
    
    # Info text (optional)
    if info_text:
        info_label = QLabel(info_text)
        info_label.setStyleSheet(STYLE_INFO_TEXT)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(info_label)
    
    # Optional checkbox
    checkbox = None
    if checkbox_text:
        checkbox = QCheckBox(checkbox_text)
        layout.addWidget(checkbox)
    
    # Buttons
    button_box = QDialogButtonBox()
    yes_btn = QPushButton(yes_text)
    yes_btn.setMinimumWidth(BUTTON_MIN_WIDTH_SMALL)
    yes_btn.clicked.connect(dialog.accept)
    no_btn = QPushButton(no_text)
    no_btn.setMinimumWidth(BUTTON_MIN_WIDTH_SMALL)
    no_btn.clicked.connect(dialog.reject)
    button_box.addButton(yes_btn, QDialogButtonBox.ButtonRole.AcceptRole)
    button_box.addButton(no_btn, QDialogButtonBox.ButtonRole.RejectRole)
    layout.addWidget(button_box)
    
    # Center on parent (handles sizing internally)
    center_dialog_on_parent(dialog)
    
    result = dialog.exec() == QDialog.DialogCode.Accepted
    
    if checkbox_text:
        return result, checkbox.isChecked() if checkbox else False
    return result

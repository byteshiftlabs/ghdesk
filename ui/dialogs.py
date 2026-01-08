"""
Custom dialog helpers for consistent styling across the application.
All dialogs follow the same compact design pattern.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, 
    QDialogButtonBox, QCheckBox, QSizePolicy
)
from PyQt6.QtCore import Qt


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
    
    layout = QVBoxLayout()
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)
    dialog.setLayout(layout)
    
    # Main text
    main_label = QLabel(main_text)
    main_label.setStyleSheet("font-size: 12px; font-weight: bold;")
    main_label.setWordWrap(True)
    layout.addWidget(main_label)
    
    # Info text (optional)
    if info_text:
        info_label = QLabel(info_text)
        info_label.setStyleSheet("font-size: 11px; color: #666;")
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(info_label)
    
    # OK button
    button_box = QDialogButtonBox()
    ok_btn = QPushButton("OK")
    ok_btn.setMinimumWidth(70)
    ok_btn.clicked.connect(dialog.accept)
    button_box.addButton(ok_btn, QDialogButtonBox.ButtonRole.AcceptRole)
    layout.addWidget(button_box)
    
    dialog.adjustSize()
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
    
    layout = QVBoxLayout()
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)
    dialog.setLayout(layout)
    
    # Main text
    main_label = QLabel(main_text)
    main_label.setStyleSheet("font-size: 12px; font-weight: bold;")
    main_label.setWordWrap(True)
    layout.addWidget(main_label)
    
    # Info text (optional)
    if info_text:
        info_label = QLabel(info_text)
        info_label.setStyleSheet("font-size: 11px; color: #666;")
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
    yes_btn.setMinimumWidth(70)
    yes_btn.clicked.connect(dialog.accept)
    no_btn = QPushButton(no_text)
    no_btn.setMinimumWidth(70)
    no_btn.clicked.connect(dialog.reject)
    button_box.addButton(yes_btn, QDialogButtonBox.ButtonRole.AcceptRole)
    button_box.addButton(no_btn, QDialogButtonBox.ButtonRole.RejectRole)
    layout.addWidget(button_box)
    
    dialog.adjustSize()
    result = dialog.exec() == QDialog.DialogCode.Accepted
    
    if checkbox_text:
        return result, checkbox.isChecked() if checkbox else False
    return result

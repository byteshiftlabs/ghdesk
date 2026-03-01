"""
Diff viewer syntax highlighter and dialog for git diffs.
"""

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox


class DiffHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for git diff output."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_formats()

    def _setup_formats(self):
        """Set up text formats for different diff elements."""
        # Added lines (green)
        self.added_format = QTextCharFormat()
        self.added_format.setForeground(QColor("#98c379"))
        self.added_format.setBackground(QColor("#2d3a2d"))

        # Removed lines (red)
        self.removed_format = QTextCharFormat()
        self.removed_format.setForeground(QColor("#e06c75"))
        self.removed_format.setBackground(QColor("#3a2d2d"))

        # Hunk headers (cyan)
        self.hunk_format = QTextCharFormat()
        self.hunk_format.setForeground(QColor("#56b6c2"))
        self.hunk_format.setFontWeight(QFont.Weight.Bold)

        # File headers (yellow)
        self.header_format = QTextCharFormat()
        self.header_format.setForeground(QColor("#e5c07b"))
        self.header_format.setFontWeight(QFont.Weight.Bold)

        # Index/meta lines (gray)
        self.meta_format = QTextCharFormat()
        self.meta_format.setForeground(QColor("#5c6370"))

    def highlightBlock(self, text: str):
        """Apply highlighting to a block of text."""
        if not text:
            return

        # File headers (diff --git, ---, +++)
        if text.startswith("diff --git") or text.startswith("---") or text.startswith("+++"):
            self.setFormat(0, len(text), self.header_format)
        # Hunk headers (@@ ... @@)
        elif text.startswith("@@"):
            self.setFormat(0, len(text), self.hunk_format)
        # Added lines
        elif text.startswith("+") and not text.startswith("+++"):
            self.setFormat(0, len(text), self.added_format)
        # Removed lines
        elif text.startswith("-") and not text.startswith("---"):
            self.setFormat(0, len(text), self.removed_format)
        # Index and other meta lines
        elif text.startswith("index ") or text.startswith("new file") or text.startswith("deleted file"):
            self.setFormat(0, len(text), self.meta_format)


class DiffViewerDialog(QDialog):
    """Dialog for viewing git diffs with syntax highlighting."""

    def __init__(self, diff_text: str, title: str = "Diff Viewer", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)
        self._init_ui(diff_text)

    def _init_ui(self, diff_text: str):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Diff text area
        self.diff_edit = QTextEdit()
        self.diff_edit.setReadOnly(True)
        self.diff_edit.setFontFamily("Monospace")
        self.diff_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        # Apply highlighter
        self.highlighter = DiffHighlighter(self.diff_edit.document())
        self.diff_edit.setPlainText(diff_text)

        layout.addWidget(self.diff_edit)

        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

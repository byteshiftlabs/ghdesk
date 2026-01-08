"""
Diff viewer widget for code reviews
Displays git diffs with syntax highlighting
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter


class DiffHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for git diffs"""
    
    def __init__(self, document):
        super().__init__(document)
        
        # Define formats
        self.formats = {}
        
        # Added lines (green)
        added_format = QTextCharFormat()
        added_format.setBackground(QColor("#e6ffed"))
        added_format.setForeground(QColor("#22863a"))
        self.formats['added'] = added_format
        
        # Removed lines (red)
        removed_format = QTextCharFormat()
        removed_format.setBackground(QColor("#ffeef0"))
        removed_format.setForeground(QColor("#cb2431"))
        self.formats['removed'] = removed_format
        
        # File header (blue)
        header_format = QTextCharFormat()
        header_format.setForeground(QColor("#005cc5"))
        header_format.setFontWeight(QFont.Weight.Bold)
        self.formats['header'] = header_format
        
        # Hunk header (cyan)
        hunk_format = QTextCharFormat()
        hunk_format.setBackground(QColor("#f1f8ff"))
        hunk_format.setForeground(QColor("#0366d6"))
        self.formats['hunk'] = hunk_format
        
        # Context lines (normal)
        context_format = QTextCharFormat()
        self.formats['context'] = context_format
    
    def highlightBlock(self, text):
        """Highlight a block of text"""
        if not text:
            return
        
        first_char = text[0] if text else ''
        
        if text.startswith('diff --git') or text.startswith('index '):
            self.setFormat(0, len(text), self.formats['header'])
        elif text.startswith('+++') or text.startswith('---'):
            self.setFormat(0, len(text), self.formats['header'])
        elif text.startswith('@@'):
            self.setFormat(0, len(text), self.formats['hunk'])
        elif first_char == '+':
            self.setFormat(0, len(text), self.formats['added'])
        elif first_char == '-':
            self.setFormat(0, len(text), self.formats['removed'])
        else:
            self.setFormat(0, len(text), self.formats['context'])


class DiffViewer(QWidget):
    """Widget for displaying git diffs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)
        
        self.title_label = QLabel("Diff Viewer")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        self.title_label.setFont(title_font)
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        close_btn = QPushButton("✕ Close")
        close_btn.clicked.connect(self.clear_diff)
        header_layout.addWidget(close_btn)
        
        # Diff text display
        self.diff_text = QTextEdit()
        self.diff_text.setReadOnly(True)
        self.diff_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        # Use monospace font
        font = QFont("Monospace")
        font.setPointSize(10)
        font.setStyleHint(QFont.StyleHint.TypeWriter)
        self.diff_text.setFont(font)
        
        # Apply syntax highlighting
        self.highlighter = DiffHighlighter(self.diff_text.document())
        
        layout.addWidget(self.diff_text)
        
        # Stats label
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.stats_label)
    
    def set_diff(self, diff_text: str, title: str = "Diff Viewer"):
        """Set and display the diff text"""
        self.title_label.setText(title)
        self.diff_text.setPlainText(diff_text)
        
        # Calculate stats
        lines = diff_text.split('\n')
        added = sum(1 for line in lines if line.startswith('+') and not line.startswith('+++'))
        removed = sum(1 for line in lines if line.startswith('-') and not line.startswith('---'))
        
        self.stats_label.setText(
            f"<span style='color: green;'>+{added}</span> additions, "
            f"<span style='color: red;'>-{removed}</span> deletions"
        )
        self.stats_label.setTextFormat(Qt.TextFormat.RichText)
    
    def clear_diff(self):
        """Clear the diff display"""
        self.diff_text.clear()
        self.stats_label.clear()
        self.title_label.setText("Diff Viewer")

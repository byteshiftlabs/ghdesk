"""
Diff viewer syntax highlighter and dialogs for git diffs.
Supports both unified and side-by-side diff views.
"""

import re
from typing import List, Dict

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QDialogButtonBox,
    QSplitter, QListWidget, QListWidgetItem, QLabel, QFrame, QWidget
)
from PyQt6.QtCore import Qt

from ui.constants import (
    DIFF_DIALOG_MIN_WIDTH, DIFF_DIALOG_MIN_HEIGHT,
    SBS_DIFF_DIALOG_MIN_WIDTH, SBS_DIFF_DIALOG_MIN_HEIGHT,
    SBS_DIFF_FILE_LIST_WIDTH, SBS_DIFF_CONTENT_WIDTH,
    MARGIN_NONE, MARGIN_MEDIUM, FONT_MONOSPACE
)
from ui.styles import (
    COLOR_DIFF_ADDED_FG, COLOR_DIFF_ADDED_BG,
    COLOR_DIFF_REMOVED_FG, COLOR_DIFF_REMOVED_BG,
    COLOR_DIFF_HUNK_FG, COLOR_DIFF_HEADER_FG, COLOR_DIFF_META_FG,
    COLOR_SBS_ADDED_BG, COLOR_SBS_REMOVED_BG,
    COLOR_SBS_EMPTY_BG, COLOR_SBS_EMPTY_FG,
    STYLE_DIFF_HEADER_OLD, STYLE_DIFF_HEADER_NEW, STYLE_DIFF_FILE_LABEL
)


class DiffHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for git diff output."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_formats()

    def _setup_formats(self):
        """Set up text formats for different diff elements."""
        # Added lines (green)
        self.added_format = QTextCharFormat()
        self.added_format.setForeground(QColor(COLOR_DIFF_ADDED_FG))
        self.added_format.setBackground(QColor(COLOR_DIFF_ADDED_BG))

        # Removed lines (red)
        self.removed_format = QTextCharFormat()
        self.removed_format.setForeground(QColor(COLOR_DIFF_REMOVED_FG))
        self.removed_format.setBackground(QColor(COLOR_DIFF_REMOVED_BG))

        # Hunk headers (cyan)
        self.hunk_format = QTextCharFormat()
        self.hunk_format.setForeground(QColor(COLOR_DIFF_HUNK_FG))
        self.hunk_format.setFontWeight(QFont.Weight.Bold)

        # File headers (yellow)
        self.header_format = QTextCharFormat()
        self.header_format.setForeground(QColor(COLOR_DIFF_HEADER_FG))
        self.header_format.setFontWeight(QFont.Weight.Bold)

        # Index/meta lines (gray)
        self.meta_format = QTextCharFormat()
        self.meta_format.setForeground(QColor(COLOR_DIFF_META_FG))

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
        self.setMinimumSize(DIFF_DIALOG_MIN_WIDTH, DIFF_DIALOG_MIN_HEIGHT)
        self._init_ui(diff_text)

    def _init_ui(self, diff_text: str):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Diff text area
        self.diff_edit = QTextEdit()
        self.diff_edit.setReadOnly(True)
        self.diff_edit.setFontFamily(FONT_MONOSPACE)
        self.diff_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        # Apply highlighter
        self.highlighter = DiffHighlighter(self.diff_edit.document())
        self.diff_edit.setPlainText(diff_text)

        layout.addWidget(self.diff_edit)

        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


def parse_unified_diff(diff_text: str) -> List[Dict]:
    """
    Parse a unified diff into a list of file diffs.

    Returns list of dicts with keys:
        - filename: str (new filename or old if deleted)
        - old_filename: str
        - new_filename: str
        - is_new: bool
        - is_deleted: bool
        - hunks: list of hunk dicts
    """
    files = []
    current_file = None
    current_hunk = None

    lines = diff_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        _parse_diff_line(line, files, current_file, current_hunk)
        current_file, current_hunk = _update_state(
            line, files, current_file, current_hunk
        )
        i += 1

    # Don't forget the last file
    if current_file:
        if current_hunk:
            current_file['hunks'].append(current_hunk)
        files.append(current_file)

    return files


def _update_state(line, files, current_file, current_hunk):
    """Update parser state based on line content."""
    if line.startswith('diff --git'):
        if current_file:
            if current_hunk:
                current_file['hunks'].append(current_hunk)
            files.append(current_file)

        match = re.match(r'diff --git a/(.+) b/(.+)', line)
        if match:
            old_name = match.group(1)
            new_name = match.group(2)
        else:
            old_name = new_name = "unknown"

        current_file = {
            'filename': new_name,
            'old_filename': old_name,
            'new_filename': new_name,
            'is_new': False,
            'is_deleted': False,
            'hunks': []
        }
        current_hunk = None

    elif line.startswith('new file'):
        if current_file:
            current_file['is_new'] = True

    elif line.startswith('deleted file'):
        if current_file:
            current_file['is_deleted'] = True
            current_file['filename'] = current_file['old_filename']

    elif line.startswith('@@'):
        if current_file:
            if current_hunk:
                current_file['hunks'].append(current_hunk)

            match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            if match:
                old_start = int(match.group(1))
                new_start = int(match.group(3))
            else:
                old_start = new_start = 1

            current_hunk = {
                'header': line,
                'old_start': old_start,
                'new_start': new_start,
                'old_lines': [],
                'new_lines': []
            }

    elif current_hunk is not None:
        _parse_hunk_line(line, current_hunk)

    return current_file, current_hunk


def _parse_diff_line(line, files, current_file, current_hunk):
    """Parse a single diff line (placeholder for extension)."""
    # Line parsing handled in _update_state
    _ = (line, files, current_file, current_hunk)  # Silence unused warnings


def _parse_hunk_line(line, current_hunk):
    """Parse a line within a hunk."""
    if line.startswith('+') and not line.startswith('+++'):
        current_hunk['new_lines'].append(('add', line[1:]))
        current_hunk['old_lines'].append(('empty', ''))
    elif line.startswith('-') and not line.startswith('---'):
        current_hunk['old_lines'].append(('remove', line[1:]))
        current_hunk['new_lines'].append(('empty', ''))
    elif line.startswith(' ') or line == '':
        content = line[1:] if line.startswith(' ') else line
        current_hunk['old_lines'].append(('context', content))
        current_hunk['new_lines'].append(('context', content))


class SideBySideHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for side-by-side diff panels."""

    def __init__(self, parent=None, is_old: bool = True):
        super().__init__(parent)
        self.is_old = is_old
        self._setup_formats()

    def _setup_formats(self):
        """Set up text formats."""
        # Added line (green background)
        self.added_format = QTextCharFormat()
        self.added_format.setBackground(QColor(COLOR_SBS_ADDED_BG))
        self.added_format.setForeground(QColor(COLOR_DIFF_ADDED_FG))

        # Removed line (red background)
        self.removed_format = QTextCharFormat()
        self.removed_format.setBackground(QColor(COLOR_SBS_REMOVED_BG))
        self.removed_format.setForeground(QColor(COLOR_DIFF_REMOVED_FG))

        # Empty placeholder
        self.empty_format = QTextCharFormat()
        self.empty_format.setBackground(QColor(COLOR_SBS_EMPTY_BG))
        self.empty_format.setForeground(QColor(COLOR_SBS_EMPTY_FG))

    def highlightBlock(self, text: str):
        """Apply highlighting based on line prefix markers."""
        if text.startswith('\x00add\x00'):
            self.setFormat(0, len(text), self.added_format)
        elif text.startswith('\x00remove\x00'):
            self.setFormat(0, len(text), self.removed_format)
        elif text.startswith('\x00empty\x00'):
            self.setFormat(0, len(text), self.empty_format)


class SyncedTextEdit(QTextEdit):
    """Text edit that syncs scrolling with another text edit."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sync_partner = None
        self._syncing = False
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setFontFamily(FONT_MONOSPACE)

    def set_sync_partner(self, partner: 'SyncedTextEdit'):
        """Set the partner to sync scrolling with."""
        self.sync_partner = partner
        self.verticalScrollBar().valueChanged.connect(self._on_scroll)

    def _on_scroll(self, value: int):
        """Sync scroll position with partner."""
        if self._syncing or not self.sync_partner:
            return
        self.sync_partner.set_syncing(True)
        self.sync_partner.verticalScrollBar().setValue(value)
        self.sync_partner.set_syncing(False)

    def set_syncing(self, syncing: bool):
        """Set the syncing flag."""
        self._syncing = syncing


class SideBySideDiffDialog(QDialog):
    """Dialog showing side-by-side diff for all changed files."""

    def __init__(self, diff_text: str, title: str = "Side-by-Side Diff", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(SBS_DIFF_DIALOG_MIN_WIDTH, SBS_DIFF_DIALOG_MIN_HEIGHT)

        self.files = parse_unified_diff(diff_text)
        self._init_ui()

        if self.files:
            self.file_list.setCurrentRow(0)

    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM)
        self.setLayout(layout)

        # Main splitter: file list | diff view
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(main_splitter, 1)

        # File list
        file_frame = QFrame()
        file_layout = QVBoxLayout()
        file_layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
        file_frame.setLayout(file_layout)

        file_label = QLabel("Changed Files")
        file_label.setStyleSheet(STYLE_DIFF_FILE_LABEL)
        file_layout.addWidget(file_label)

        self.file_list = QListWidget()
        self.file_list.currentRowChanged.connect(self._on_file_selected)
        file_layout.addWidget(self.file_list)

        # Populate file list
        for file_info in self.files:
            item = QListWidgetItem()
            filename = file_info['filename']
            if file_info['is_new']:
                item.setText(f"+ {filename}")
                item.setForeground(QColor(COLOR_DIFF_ADDED_FG))
            elif file_info['is_deleted']:
                item.setText(f"- {filename}")
                item.setForeground(QColor(COLOR_DIFF_REMOVED_FG))
            else:
                item.setText(f"  {filename}")
            self.file_list.addItem(item)

        main_splitter.addWidget(file_frame)

        # Diff view container
        diff_container = QWidget()
        diff_layout = QVBoxLayout()
        diff_layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
        diff_container.setLayout(diff_layout)

        # Header labels
        header_layout = QHBoxLayout()
        self.old_header = QLabel("Original")
        self.old_header.setStyleSheet(STYLE_DIFF_HEADER_OLD)
        self.old_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.old_header)

        self.new_header = QLabel("Modified")
        self.new_header.setStyleSheet(STYLE_DIFF_HEADER_NEW)
        self.new_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.new_header)
        diff_layout.addLayout(header_layout)

        # Side-by-side splitter
        diff_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Old (left) side
        self.old_edit = SyncedTextEdit()
        self.old_highlighter = SideBySideHighlighter(self.old_edit.document(), is_old=True)
        diff_splitter.addWidget(self.old_edit)

        # New (right) side
        self.new_edit = SyncedTextEdit()
        self.new_highlighter = SideBySideHighlighter(self.new_edit.document(), is_old=False)
        diff_splitter.addWidget(self.new_edit)

        # Link scrolling
        self.old_edit.set_sync_partner(self.new_edit)
        self.new_edit.set_sync_partner(self.old_edit)

        diff_layout.addWidget(diff_splitter, 1)
        main_splitter.addWidget(diff_container)

        # Set splitter sizes (file list narrower)
        main_splitter.setSizes([SBS_DIFF_FILE_LIST_WIDTH, SBS_DIFF_CONTENT_WIDTH])

        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _on_file_selected(self, index: int):
        """Handle file selection."""
        if index < 0 or index >= len(self.files):
            return

        file_info = self.files[index]

        # Update headers
        self.old_header.setText(f"Original: {file_info['old_filename']}")
        self.new_header.setText(f"Modified: {file_info['new_filename']}")

        # Build side-by-side content
        old_lines, new_lines = self._build_side_by_side(file_info)

        # Set content
        self.old_edit.setPlainText('\n'.join(old_lines))
        self.new_edit.setPlainText('\n'.join(new_lines))

    def _build_side_by_side(self, file_info: Dict) -> tuple:
        """Build side-by-side line content from file info."""
        old_lines = []
        new_lines = []

        for hunk in file_info['hunks']:
            # Add hunk separator
            old_lines.append("\x00context\x00" + hunk['header'])
            new_lines.append("\x00context\x00" + hunk['header'])

            # Process lines - align additions and deletions
            hunk_old = hunk['old_lines']
            hunk_new = hunk['new_lines']

            for line_type, content in hunk_old:
                old_lines.append(self._format_line(line_type, content, 'old'))

            for line_type, content in hunk_new:
                new_lines.append(self._format_line(line_type, content, 'new'))

        return old_lines, new_lines

    @staticmethod
    def _format_line(line_type: str, content: str, side: str) -> str:
        """Format a line with type marker for highlighting."""
        if line_type == 'context':
            return "\x00context\x00" + content
        if line_type == 'remove' and side == 'old':
            return "\x00remove\x00" + content
        if line_type == 'add' and side == 'new':
            return "\x00add\x00" + content
        if line_type == 'empty':
            return "\x00empty\x00"
        return "\x00context\x00" + content

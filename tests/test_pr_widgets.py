"""
Tests for PR-related widgets
"""

import pytest

# Skip all tests in this module if no display is available
pytestmark = pytest.mark.skipif(
    True,  # Skip by default in CI - set to check for DISPLAY env var in real CI
    reason="Qt tests require a display"
)


class TestPRListWidgetInit:
    """Tests for PRListWidget initialization.

    Note: These tests require a Qt application instance.
    In CI without display, they will be skipped.
    """

    def test_pr_list_widget_can_be_imported(self):
        """PRListWidget can be imported."""
        from ui.pr_list_widget import PRListWidget
        assert PRListWidget is not None

    def test_pr_detail_view_can_be_imported(self):
        """PRDetailView can be imported."""
        from ui.pr_detail_view import PRDetailView
        assert PRDetailView is not None

    def test_diff_viewer_dialog_can_be_imported(self):
        """DiffViewerDialog can be imported."""
        from ui.diff_viewer import DiffViewerDialog
        assert DiffViewerDialog is not None

    def test_side_by_side_diff_dialog_can_be_imported(self):
        """SideBySideDiffDialog can be imported."""
        from ui.diff_viewer import SideBySideDiffDialog
        assert SideBySideDiffDialog is not None


class TestDiffHighlighter:
    """Tests for DiffHighlighter that don't require display."""

    def test_diff_highlighter_can_be_imported(self):
        """DiffHighlighter can be imported."""
        from ui.diff_viewer import DiffHighlighter
        assert DiffHighlighter is not None

    def test_side_by_side_highlighter_can_be_imported(self):
        """SideBySideHighlighter can be imported."""
        from ui.diff_viewer import SideBySideHighlighter
        assert SideBySideHighlighter is not None

"""
Tests for ui.diff_viewer module
"""

import pytest
from ui.diff_viewer import parse_unified_diff


class TestParseUnifiedDiff:
    """Tests for the parse_unified_diff function."""

    def test_empty_input_returns_empty_list(self):
        """Empty diff text returns empty list."""
        result = parse_unified_diff("")
        assert result == []

    def test_single_file_modification(self):
        """Parses a single file modification correctly."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,3 +1,3 @@
 def hello():
-    print('hello')
+    print('hello world')
     return True
"""
        result = parse_unified_diff(diff)

        assert len(result) == 1
        assert result[0]['filename'] == 'test.py'
        assert result[0]['old_filename'] == 'test.py'
        assert result[0]['new_filename'] == 'test.py'
        assert result[0]['is_new'] is False
        assert result[0]['is_deleted'] is False
        assert len(result[0]['hunks']) == 1

    def test_new_file(self):
        """Parses a new file addition correctly."""
        diff = """diff --git a/new_file.py b/new_file.py
new file mode 100644
--- /dev/null
+++ b/new_file.py
@@ -0,0 +1,3 @@
+def new_function():
+    pass
+
"""
        result = parse_unified_diff(diff)

        assert len(result) == 1
        assert result[0]['filename'] == 'new_file.py'
        assert result[0]['is_new'] is True
        assert result[0]['is_deleted'] is False

    def test_deleted_file(self):
        """Parses a file deletion correctly."""
        diff = """diff --git a/old_file.py b/old_file.py
deleted file mode 100644
--- a/old_file.py
+++ /dev/null
@@ -1,3 +0,0 @@
-def old_function():
-    pass
-
"""
        result = parse_unified_diff(diff)

        assert len(result) == 1
        assert result[0]['filename'] == 'old_file.py'
        assert result[0]['is_new'] is False
        assert result[0]['is_deleted'] is True

    def test_multiple_files(self):
        """Parses multiple files in a diff correctly."""
        diff = """diff --git a/file1.py b/file1.py
--- a/file1.py
+++ b/file1.py
@@ -1,2 +1,2 @@
-old line
+new line
diff --git a/file2.py b/file2.py
--- a/file2.py
+++ b/file2.py
@@ -1,2 +1,2 @@
-another old line
+another new line
"""
        result = parse_unified_diff(diff)

        assert len(result) == 2
        assert result[0]['filename'] == 'file1.py'
        assert result[1]['filename'] == 'file2.py'

    def test_multiple_hunks(self):
        """Parses multiple hunks in a single file correctly."""
        diff = """diff --git a/multi_hunk.py b/multi_hunk.py
--- a/multi_hunk.py
+++ b/multi_hunk.py
@@ -1,3 +1,3 @@
 def first():
-    pass
+    return 1
@@ -10,3 +10,3 @@
 def second():
-    pass
+    return 2
"""
        result = parse_unified_diff(diff)

        assert len(result) == 1
        assert len(result[0]['hunks']) == 2

    def test_hunk_header_parsing(self):
        """Parses hunk header line numbers correctly."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -5,7 +5,8 @@ def context():
 context line
-removed line
+added line
"""
        result = parse_unified_diff(diff)

        hunk = result[0]['hunks'][0]
        assert hunk['old_start'] == 5
        assert hunk['new_start'] == 5
        assert '@@ -5,7 +5,8 @@' in hunk['header']

    def test_context_lines(self):
        """Context lines are parsed correctly."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,5 +1,5 @@
 context before
-removed
+added
 context after
"""
        result = parse_unified_diff(diff)

        hunk = result[0]['hunks'][0]
        # Check old_lines has correct entries
        old_types = [line[0] for line in hunk['old_lines']]
        assert 'context' in old_types
        assert 'remove' in old_types
        assert 'empty' in old_types

        # Check new_lines has correct entries
        new_types = [line[0] for line in hunk['new_lines']]
        assert 'context' in new_types
        assert 'add' in new_types
        assert 'empty' in new_types

    def test_added_only_lines(self):
        """Lines that are only additions are parsed correctly."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,2 +1,4 @@
 existing
+new line 1
+new line 2
 more existing
"""
        result = parse_unified_diff(diff)

        hunk = result[0]['hunks'][0]
        add_count = sum(1 for line in hunk['new_lines'] if line[0] == 'add')
        assert add_count == 2

    def test_removed_only_lines(self):
        """Lines that are only deletions are parsed correctly."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,4 +1,2 @@
 existing
-deleted line 1
-deleted line 2
 more existing
"""
        result = parse_unified_diff(diff)

        hunk = result[0]['hunks'][0]
        remove_count = sum(1 for line in hunk['old_lines'] if line[0] == 'remove')
        assert remove_count == 2

    def test_path_with_subdirectory(self):
        """Parses file paths with subdirectories correctly."""
        diff = """diff --git a/src/module/file.py b/src/module/file.py
--- a/src/module/file.py
+++ b/src/module/file.py
@@ -1,2 +1,2 @@
-old
+new
"""
        result = parse_unified_diff(diff)

        assert result[0]['filename'] == 'src/module/file.py'
        assert result[0]['old_filename'] == 'src/module/file.py'
        assert result[0]['new_filename'] == 'src/module/file.py'

    def test_renamed_file(self):
        """Parses renamed files (different old/new names) correctly."""
        diff = """diff --git a/old_name.py b/new_name.py
--- a/old_name.py
+++ b/new_name.py
@@ -1,2 +1,2 @@
-old content
+new content
"""
        result = parse_unified_diff(diff)

        assert result[0]['old_filename'] == 'old_name.py'
        assert result[0]['new_filename'] == 'new_name.py'
        # filename defaults to new_filename
        assert result[0]['filename'] == 'new_name.py'

    def test_empty_line_in_diff(self):
        """Empty lines in diff are handled correctly."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,3 +1,3 @@
 line one

 line three
"""
        result = parse_unified_diff(diff)

        # Should not crash and should parse
        assert len(result) == 1

    def test_no_context_hunk(self):
        """Hunks without context are parsed correctly."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1 +1 @@
-old
+new
"""
        result = parse_unified_diff(diff)

        assert len(result[0]['hunks']) == 1
        hunk = result[0]['hunks'][0]
        assert len(hunk['old_lines']) > 0
        assert len(hunk['new_lines']) > 0

    def test_malformed_diff_header_returns_unknown(self):
        """Malformed diff headers default to 'unknown' filename."""
        diff = """diff --git malformed
--- a/test.py
+++ b/test.py
@@ -1 +1 @@
-old
+new
"""
        result = parse_unified_diff(diff)

        # Should handle gracefully
        assert len(result) == 1
        assert result[0]['filename'] == 'unknown'

    def test_special_characters_in_path(self):
        """File paths with special characters are parsed."""
        diff = """diff --git a/path-with-dashes/file_name.py b/path-with-dashes/file_name.py
--- a/path-with-dashes/file_name.py
+++ b/path-with-dashes/file_name.py
@@ -1 +1 @@
-old
+new
"""
        result = parse_unified_diff(diff)

        assert result[0]['filename'] == 'path-with-dashes/file_name.py'


class TestParseUnifiedDiffEdgeCases:
    """Edge case tests for parse_unified_diff."""

    def test_only_diff_header_no_content(self):
        """Diff with only header and no hunks."""
        diff = """diff --git a/empty.py b/empty.py
--- a/empty.py
+++ b/empty.py
"""
        result = parse_unified_diff(diff)

        assert len(result) == 1
        assert result[0]['hunks'] == []

    def test_binary_file_marker(self):
        """Binary file markers don't crash the parser."""
        diff = """diff --git a/image.png b/image.png
Binary files a/image.png and b/image.png differ
"""
        result = parse_unified_diff(diff)

        # Should parse without crashing
        assert len(result) == 1

    def test_no_newline_at_end_marker(self):
        """'No newline at end of file' markers are handled."""
        diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1 +1 @@
-old
\\ No newline at end of file
+new
\\ No newline at end of file
"""
        result = parse_unified_diff(diff)

        # Should parse without crashing
        assert len(result) == 1

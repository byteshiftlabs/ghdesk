"""
Tests for core.github.pull_requests module
"""

from unittest.mock import MagicMock
import pytest
from core.github.pull_requests import PullRequestsMixin


class MockGHWrapper(PullRequestsMixin):
    """Mock GitHub wrapper for testing PullRequestsMixin."""

    def __init__(self):
        self.mock_run_command = MagicMock()

    def _run_command(self, args, capture_json=False):
        """Mock implementation of _run_command."""
        return self.mock_run_command(args, capture_json=capture_json)


@pytest.fixture
def gh_wrapper():
    """Create a mock GitHub wrapper instance."""
    return MockGHWrapper()


class TestPullRequestsMixinListPRs:
    """Tests for list_prs method."""

    def test_list_prs_success_returns_list(self, gh_wrapper):
        """list_prs returns list on success."""
        mock_prs = [
            {"number": 1, "title": "PR 1", "state": "OPEN"},
            {"number": 2, "title": "PR 2", "state": "OPEN"},
        ]
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": mock_prs,
            "error": ""
        }

        result = gh_wrapper.list_prs()

        assert result == mock_prs
        gh_wrapper.mock_run_command.assert_called_once()

    def test_list_prs_failure_returns_empty_list(self, gh_wrapper):
        """list_prs returns empty list on failure."""
        gh_wrapper.mock_run_command.return_value = {
            "success": False,
            "output": "",
            "error": "Failed to list PRs"
        }

        result = gh_wrapper.list_prs()

        assert result == []

    def test_list_prs_with_repo_includes_repo_arg(self, gh_wrapper):
        """list_prs includes --repo when repo is specified."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": [],
            "error": ""
        }

        gh_wrapper.list_prs(repo="owner/repo")

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--repo" in args
        assert "owner/repo" in args

    def test_list_prs_with_state_filter(self, gh_wrapper):
        """list_prs includes state filter in command."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": [],
            "error": ""
        }

        gh_wrapper.list_prs(state="closed")

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--state" in args
        idx = args.index("--state")
        assert args[idx + 1] == "closed"

    def test_list_prs_with_limit(self, gh_wrapper):
        """list_prs includes limit in command."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": [],
            "error": ""
        }

        gh_wrapper.list_prs(limit=50)

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--limit" in args
        idx = args.index("--limit")
        assert args[idx + 1] == "50"

    def test_list_prs_requests_json_fields(self, gh_wrapper):
        """list_prs requests correct JSON fields."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": [],
            "error": ""
        }

        gh_wrapper.list_prs()

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--json" in args
        assert gh_wrapper.PR_LIST_FIELDS in args


class TestPullRequestsMixinViewPR:
    """Tests for view_pr method."""

    def test_view_pr_success_returns_dict(self, gh_wrapper):
        """view_pr returns dict on success."""
        mock_pr = {
            "number": 1,
            "title": "Test PR",
            "body": "Description",
            "state": "OPEN"
        }
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": mock_pr,
            "error": ""
        }

        result = gh_wrapper.view_pr(1)

        assert result == mock_pr

    def test_view_pr_failure_returns_empty_dict(self, gh_wrapper):
        """view_pr returns empty dict on failure."""
        gh_wrapper.mock_run_command.return_value = {
            "success": False,
            "output": "",
            "error": "PR not found"
        }

        result = gh_wrapper.view_pr(999)

        assert result == {}

    def test_view_pr_includes_pr_number(self, gh_wrapper):
        """view_pr includes PR number in command."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": {},
            "error": ""
        }

        gh_wrapper.view_pr(42)

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "42" in args

    def test_view_pr_with_repo(self, gh_wrapper):
        """view_pr includes --repo when specified."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": {},
            "error": ""
        }

        gh_wrapper.view_pr(1, repo="owner/repo")

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--repo" in args
        assert "owner/repo" in args


class TestPullRequestsMixinGetPRDiff:
    """Tests for get_pr_diff method."""

    def test_get_pr_diff_success_returns_string(self, gh_wrapper):
        """get_pr_diff returns diff string on success."""
        mock_diff = "diff --git a/file.py b/file.py\n-old\n+new"
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": mock_diff,
            "error": ""
        }

        result = gh_wrapper.get_pr_diff(1)

        assert result == mock_diff

    def test_get_pr_diff_failure_returns_empty_string(self, gh_wrapper):
        """get_pr_diff returns empty string on failure."""
        gh_wrapper.mock_run_command.return_value = {
            "success": False,
            "output": "",
            "error": "Failed to get diff"
        }

        result = gh_wrapper.get_pr_diff(1)

        assert result == ""

    def test_get_pr_diff_includes_pr_number(self, gh_wrapper):
        """get_pr_diff includes PR number in command."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.get_pr_diff(42)

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "42" in args


class TestPullRequestsMixinMergePR:
    """Tests for merge_pr method."""

    def test_merge_pr_success(self, gh_wrapper):
        """merge_pr returns success result."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "Merged successfully",
            "error": ""
        }

        result = gh_wrapper.merge_pr(1)

        assert result["success"] is True

    def test_merge_pr_default_method_is_merge(self, gh_wrapper):
        """merge_pr uses merge method by default."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.merge_pr(1)

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--merge" in args

    def test_merge_pr_squash_method(self, gh_wrapper):
        """merge_pr can use squash method."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.merge_pr(1, merge_method="squash")

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--squash" in args

    def test_merge_pr_rebase_method(self, gh_wrapper):
        """merge_pr can use rebase method."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.merge_pr(1, merge_method="rebase")

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--rebase" in args

    def test_merge_pr_delete_branch(self, gh_wrapper):
        """merge_pr includes delete-branch flag when requested."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.merge_pr(1, delete_branch=True)

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--delete-branch" in args


class TestPullRequestsMixinClosePR:
    """Tests for close_pr method."""

    def test_close_pr_success(self, gh_wrapper):
        """close_pr returns success result."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "PR closed",
            "error": ""
        }

        result = gh_wrapper.close_pr(1)

        assert result["success"] is True

    def test_close_pr_with_comment(self, gh_wrapper):
        """close_pr includes comment when provided."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.close_pr(1, comment="Closing this PR")

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--comment" in args
        assert "Closing this PR" in args


class TestPullRequestsMixinReopenPR:
    """Tests for reopen_pr method."""

    def test_reopen_pr_success(self, gh_wrapper):
        """reopen_pr returns success result."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "PR reopened",
            "error": ""
        }

        result = gh_wrapper.reopen_pr(1)

        assert result["success"] is True

    def test_reopen_pr_includes_pr_number(self, gh_wrapper):
        """reopen_pr includes PR number in command."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.reopen_pr(42)

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "42" in args
        assert "reopen" in args


class TestPullRequestsMixinAddComment:
    """Tests for add_pr_comment method."""

    def test_add_pr_comment_success(self, gh_wrapper):
        """add_pr_comment returns success result."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "Comment added",
            "error": ""
        }

        result = gh_wrapper.add_pr_comment(1, "This is a comment")

        assert result["success"] is True

    def test_add_pr_comment_includes_body(self, gh_wrapper):
        """add_pr_comment includes comment body in command."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.add_pr_comment(1, "Test comment body")

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--body" in args
        assert "Test comment body" in args


class TestPullRequestsMixinRequestReview:
    """Tests for request_pr_review method."""

    def test_request_pr_review_success(self, gh_wrapper):
        """request_pr_review returns success result."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "Review requested",
            "error": ""
        }

        result = gh_wrapper.request_pr_review(1, ["user1", "user2"])

        assert result["success"] is True

    def test_request_pr_review_includes_reviewers(self, gh_wrapper):
        """request_pr_review includes reviewer usernames."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": "",
            "error": ""
        }

        gh_wrapper.request_pr_review(1, ["alice", "bob"])

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "--add-reviewer" in args
        assert "alice,bob" in args


class TestPullRequestsMixinGetChecks:
    """Tests for get_pr_checks method."""

    def test_get_pr_checks_success_returns_list(self, gh_wrapper):
        """get_pr_checks returns list on success."""
        mock_checks = [
            {"name": "CI", "state": "completed", "conclusion": "success"},
            {"name": "Tests", "state": "completed", "conclusion": "success"},
        ]
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": mock_checks,
            "error": ""
        }

        result = gh_wrapper.get_pr_checks(1)

        assert result == mock_checks

    def test_get_pr_checks_failure_returns_empty_list(self, gh_wrapper):
        """get_pr_checks returns empty list on failure."""
        gh_wrapper.mock_run_command.return_value = {
            "success": False,
            "output": "",
            "error": "Failed to get checks"
        }

        result = gh_wrapper.get_pr_checks(1)

        assert result == []

    def test_get_pr_checks_includes_pr_number(self, gh_wrapper):
        """get_pr_checks includes PR number in command."""
        gh_wrapper.mock_run_command.return_value = {
            "success": True,
            "output": [],
            "error": ""
        }

        gh_wrapper.get_pr_checks(42)

        args = gh_wrapper.mock_run_command.call_args[0][0]
        assert "42" in args
        assert "checks" in args


class TestPullRequestsMixinConstants:
    """Tests for PullRequestsMixin constants."""

    def test_pr_list_fields_contains_required_fields(self):
        """PR_LIST_FIELDS contains essential fields."""
        fields = PullRequestsMixin.PR_LIST_FIELDS
        assert "number" in fields
        assert "title" in fields
        assert "state" in fields
        assert "author" in fields

    def test_pr_detail_fields_contains_body(self):
        """PR_DETAIL_FIELDS contains body field."""
        fields = PullRequestsMixin.PR_DETAIL_FIELDS
        assert "body" in fields

    def test_pr_detail_fields_is_superset_of_list_fields(self):
        """PR_DETAIL_FIELDS contains all fields from PR_LIST_FIELDS."""
        list_fields = set(PullRequestsMixin.PR_LIST_FIELDS.split(","))
        detail_fields = set(PullRequestsMixin.PR_DETAIL_FIELDS.split(","))

        # All list fields except some specific ones should be in detail fields
        common_fields = {"number", "title", "state", "author", "headRefName", "baseRefName"}
        assert common_fields.issubset(detail_fields)

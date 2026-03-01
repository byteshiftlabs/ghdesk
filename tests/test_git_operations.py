"""
Tests for core.git_operations module
"""

import tempfile
from pathlib import Path
from unittest import mock

import pytest
import git

from core.git_operations import GitRepository


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = git.Repo.init(tmpdir)

        # Configure git user for commits
        with repo.config_writer() as cw:
            cw.set_value("user", "email", "test@test.com")
            cw.set_value("user", "name", "Test User")

        # Create a commit so we have a valid HEAD
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("test content")
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")

        yield tmpdir

        # Close repo to avoid ResourceWarnings
        repo.close()


@pytest.fixture
def git_repo(temp_git_repo):
    """Create a GitRepository instance for testing"""
    repo = GitRepository(temp_git_repo)
    yield repo
    # Close the underlying git repo
    repo._repo.close()


class TestGitRepositoryInit:
    """Tests for GitRepository initialization"""

    def test_init_valid_repo(self, temp_git_repo):
        """Can initialize with a valid git repository"""
        repo = GitRepository(temp_git_repo)
        assert repo.path == temp_git_repo

    def test_init_invalid_path_raises(self):
        """Raises error for non-existent path"""
        with pytest.raises(git.exc.NoSuchPathError):
            GitRepository("/nonexistent/path")

    def test_init_non_git_dir_raises(self):
        """Raises error for directory that isn't a git repo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(git.exc.InvalidGitRepositoryError):
                GitRepository(tmpdir)


class TestGitRepositoryProperties:
    """Tests for GitRepository properties"""

    def test_name_returns_directory_name(self, temp_git_repo, git_repo):
        """name property returns the repository directory name"""
        expected_name = Path(temp_git_repo).name
        assert git_repo.name == expected_name

    def test_current_branch(self, git_repo):
        """current_branch returns the active branch name"""
        # Default branch is usually 'master' or 'main'
        branch = git_repo.current_branch
        assert branch in ["master", "main"]

    def test_is_detached_initially_false(self, git_repo):
        """is_detached returns False when on a branch"""
        assert git_repo.is_detached is False

    def test_is_dirty_clean_repo(self, git_repo):
        """is_dirty returns False for clean repository"""
        assert git_repo.is_dirty is False

    def test_is_dirty_with_changes(self, temp_git_repo, git_repo):
        """is_dirty returns True when there are uncommitted changes"""
        # Create an uncommitted file
        new_file = Path(temp_git_repo) / "new_file.txt"
        new_file.write_text("new content")

        assert git_repo.is_dirty is True

    def test_branches_returns_list(self, git_repo):
        """branches property returns a list of branch names"""
        branches = git_repo.branches
        assert isinstance(branches, list)
        assert len(branches) >= 1


class TestGitRepositoryBranches:
    """Tests for GitRepository branch operations"""

    def test_get_branches_returns_list(self, git_repo):
        """get_branches returns a list of branch info dicts"""
        branches = git_repo.get_branches()
        assert isinstance(branches, list)

    def test_get_branches_contains_current(self, git_repo):
        """get_branches includes the current branch"""
        branches = git_repo.get_branches()
        branch_names = [b["name"] for b in branches]
        assert git_repo.current_branch in branch_names

    def test_get_branch_names_returns_list(self, git_repo):
        """get_branch_names returns a list of branch name strings"""
        branch_names = git_repo.get_branch_names()
        assert isinstance(branch_names, list)
        assert git_repo.current_branch in branch_names


class TestGitRepositoryStatus:
    """Tests for GitRepository status operations"""

    def test_get_status_returns_dict(self, git_repo):
        """get_status returns status information dict"""
        status = git_repo.get_status()
        assert isinstance(status, dict)
        assert "modified" in status
        assert "staged" in status
        assert "untracked" in status

    def test_get_status_staged_empty(self, git_repo):
        """get_status returns empty staged list for clean repo"""
        status = git_repo.get_status()
        assert isinstance(status["staged"], list)
        assert len(status["staged"]) == 0

    def test_get_status_modified_empty(self, git_repo):
        """get_status returns empty modified list for clean repo"""
        status = git_repo.get_status()
        assert isinstance(status["modified"], list)
        assert len(status["modified"]) == 0

    def test_get_status_modified_with_changes(self, temp_git_repo, git_repo):
        """get_status returns modified files when files are changed"""
        # Modify an existing file
        test_file = Path(temp_git_repo) / "test.txt"
        test_file.write_text("modified content")

        status = git_repo.get_status()
        assert len(status["modified"]) > 0

    def test_get_status_untracked_with_new_file(self, temp_git_repo, git_repo):
        """get_status returns untracked files when new files exist"""
        # Create a new file
        new_file = Path(temp_git_repo) / "untracked.txt"
        new_file.write_text("new content")

        status = git_repo.get_status()
        assert "untracked.txt" in status["untracked"]


class TestGitRepositoryCommit:
    """Tests for GitRepository commit operations"""

    def test_stage_file(self, temp_git_repo, git_repo):
        """Can stage a file for commit"""
        # Create a new file
        new_file = Path(temp_git_repo) / "to_stage.txt"
        new_file.write_text("content")

        # stage_file returns None
        git_repo.stage_file("to_stage.txt")

        # Verify file is staged
        status = git_repo.get_status()
        assert "to_stage.txt" in status["staged"]

    def test_commit_returns_sha(self, temp_git_repo, git_repo):
        """commit returns a commit SHA string"""
        # Create and stage a file
        new_file = Path(temp_git_repo) / "commit_test.txt"
        new_file.write_text("content")
        git_repo.stage_file("commit_test.txt")

        result = git_repo.commit("Test commit message")

        # Should return a hexadecimal SHA string
        assert isinstance(result, str)
        assert len(result) == 40  # Full SHA is 40 hex chars
        assert all(c in "0123456789abcdef" for c in result)

    def test_get_diff_returns_string(self, temp_git_repo, git_repo):
        """get_diff returns diff as string"""
        # Modify a file
        test_file = Path(temp_git_repo) / "test.txt"
        test_file.write_text("modified content")

        diff = git_repo.get_diff()
        assert isinstance(diff, str)
        assert "modified content" in diff or "-test content" in diff

    def test_get_staged_diff_returns_string(self, temp_git_repo, git_repo):
        """get_staged_diff returns staged diff as string"""
        # Create, modify, and stage a file
        new_file = Path(temp_git_repo) / "staged_file.txt"
        new_file.write_text("staged content")
        git_repo.stage_file("staged_file.txt")

        diff = git_repo.get_staged_diff()
        assert isinstance(diff, str)


class TestGitRepositoryRemotes:
    """Tests for GitRepository remote operations"""

    def test_get_remotes_returns_list(self, git_repo):
        """get_remotes returns a list"""
        remotes = git_repo.get_remotes()
        assert isinstance(remotes, list)

    def test_get_remote_urls_returns_list(self, git_repo):
        """get_remote_urls returns a list"""
        urls = git_repo.get_remote_urls()
        assert isinstance(urls, list)

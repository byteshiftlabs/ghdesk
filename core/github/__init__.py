"""
GitHub CLI wrapper module
Provides a unified interface to GitHub CLI (gh) commands

This module exposes the GHWrapper class which combines all GitHub operations:
- Authentication (login, logout, status)
- Repository management (create, delete, edit, topics)
- Pull requests (list, view)
- Issues (list, view)
- Tags (list, create, delete)

Usage:
    from core.github import GHWrapper
    
    gh = GHWrapper()
    if gh.is_authenticated():
        repos = gh.list_repos()
"""

from core.github.base import GHBase
from core.github.auth import AuthMixin
from core.github.repos import ReposMixin
from core.github.pull_requests import PullRequestsMixin
from core.github.issues import IssuesMixin
from core.github.tags import TagsMixin


class GHWrapper(
    GHBase,
    AuthMixin,
    ReposMixin,
    PullRequestsMixin,
    IssuesMixin,
    TagsMixin
):
    """
    Unified GitHub CLI wrapper combining all operations.
    
    Inherits from:
        GHBase: Core command execution
        AuthMixin: Authentication methods
        ReposMixin: Repository operations
        PullRequestsMixin: Pull request operations
        IssuesMixin: Issue operations
        TagsMixin: Tag/release operations
    """
    pass


__all__ = ["GHWrapper"]

"""
GitHub pull request operations
"""

from typing import Optional, List, Dict, Any

from core.logging_config import get_logger

logger = get_logger("github.pull_requests")


class PullRequestsMixin:
    """Pull request operations for GitHub CLI"""

    # JSON fields to fetch for PR list
    PR_LIST_FIELDS = (
        "number,title,state,author,createdAt,headRefName,baseRefName,"
        "isDraft,mergeable,additions,deletions,changedFiles"
    )

    # JSON fields to fetch for PR details
    PR_DETAIL_FIELDS = (
        "number,title,body,state,author,createdAt,updatedAt,closedAt,mergedAt,"
        "headRefName,baseRefName,isDraft,mergeable,mergeStateStatus,"
        "additions,deletions,changedFiles,commits,comments,reviews,"
        "reviewRequests,labels,url"
    )

    def list_prs(
        self,
        repo: Optional[str] = None,
        state: str = "open",
        limit: int = 30
    ) -> List[Dict[str, Any]]:
        """
        List pull requests for a repository.

        Args:
            repo: Repository name (owner/repo), or None for current
            state: PR state filter ('open', 'closed', 'merged', 'all')
            limit: Maximum number of PRs to return

        Returns:
            List of pull request dicts
        """
        args = [
            "pr", "list",
            "--json", self.PR_LIST_FIELDS,
            "--state", state,
            "--limit", str(limit)
        ]
        if repo:
            args.extend(["--repo", repo])

        logger.debug("Listing PRs for %s with state=%s", repo or "current repo", state)
        result = self._run_command(args, capture_json=True)

        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []

    def view_pr(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get detailed information about a pull request.

        Args:
            pr_number: Pull request number
            repo: Repository name (owner/repo), or None for current

        Returns:
            Dict with PR details, or empty dict on failure
        """
        args = [
            "pr", "view", str(pr_number),
            "--json", self.PR_DETAIL_FIELDS
        ]
        if repo:
            args.extend(["--repo", repo])

        logger.debug("Viewing PR #%d for %s", pr_number, repo or "current repo")
        result = self._run_command(args, capture_json=True)

        if result["success"] and isinstance(result["output"], dict):
            return result["output"]
        return {}

    def get_pr_diff(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> str:
        """
        Get the diff for a pull request.

        Args:
            pr_number: Pull request number
            repo: Repository name (owner/repo), or None for current

        Returns:
            Diff string, or empty string on failure
        """
        args = ["pr", "diff", str(pr_number)]
        if repo:
            args.extend(["--repo", repo])

        logger.debug("Getting diff for PR #%d", pr_number)
        result = self._run_command(args)

        if result["success"]:
            return result["output"]
        return ""

    def merge_pr(
        self,
        pr_number: int,
        repo: Optional[str] = None,
        merge_method: str = "merge",
        delete_branch: bool = False
    ) -> Dict[str, Any]:
        """
        Merge a pull request.

        Args:
            pr_number: Pull request number
            repo: Repository name (owner/repo), or None for current
            merge_method: 'merge', 'squash', or 'rebase'
            delete_branch: Whether to delete the head branch after merge

        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        args = ["pr", "merge", str(pr_number), f"--{merge_method}"]
        if repo:
            args.extend(["--repo", repo])
        if delete_branch:
            args.append("--delete-branch")

        logger.info("Merging PR #%d with method=%s", pr_number, merge_method)
        return self._run_command(args)

    def close_pr(
        self,
        pr_number: int,
        repo: Optional[str] = None,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Close a pull request without merging.

        Args:
            pr_number: Pull request number
            repo: Repository name (owner/repo), or None for current
            comment: Optional closing comment

        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        args = ["pr", "close", str(pr_number)]
        if repo:
            args.extend(["--repo", repo])
        if comment:
            args.extend(["--comment", comment])

        logger.info("Closing PR #%d", pr_number)
        return self._run_command(args)

    def reopen_pr(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Reopen a closed pull request.

        Args:
            pr_number: Pull request number
            repo: Repository name (owner/repo), or None for current

        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        args = ["pr", "reopen", str(pr_number)]
        if repo:
            args.extend(["--repo", repo])

        logger.info("Reopening PR #%d", pr_number)
        return self._run_command(args)

    def add_pr_comment(
        self,
        pr_number: int,
        body: str,
        repo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a comment to a pull request.

        Args:
            pr_number: Pull request number
            body: Comment text
            repo: Repository name (owner/repo), or None for current

        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        args = ["pr", "comment", str(pr_number), "--body", body]
        if repo:
            args.extend(["--repo", repo])

        logger.info("Adding comment to PR #%d", pr_number)
        return self._run_command(args)

    def request_pr_review(
        self,
        pr_number: int,
        reviewers: List[str],
        repo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Request reviewers for a pull request.

        Args:
            pr_number: Pull request number
            reviewers: List of GitHub usernames to request review from
            repo: Repository name (owner/repo), or None for current

        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        args = ["pr", "edit", str(pr_number), "--add-reviewer", ",".join(reviewers)]
        if repo:
            args.extend(["--repo", repo])

        logger.info("Requesting review from %s for PR #%d", reviewers, pr_number)
        return self._run_command(args)

    def get_pr_checks(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get CI/CD check status for a pull request.

        Args:
            pr_number: Pull request number
            repo: Repository name (owner/repo), or None for current

        Returns:
            List of check status dicts
        """
        args = [
            "pr", "checks", str(pr_number),
            "--json", "name,state,conclusion,startedAt,completedAt"
        ]
        if repo:
            args.extend(["--repo", repo])

        logger.debug("Getting checks for PR #%d", pr_number)
        result = self._run_command(args, capture_json=True)

        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []

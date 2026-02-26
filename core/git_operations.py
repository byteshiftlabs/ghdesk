"""
Local Git repository operations
Provides abstraction for git operations used by UI layer

This module isolates git library usage from the UI layer,
following the principle of layer separation.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import git


class GitRepository:
    """
    Wrapper for local Git repository operations.
    
    Provides a clean interface to git operations,
    isolating the git library from UI components.
    """
    
    def __init__(self, repo_path: str):
        """
        Initialize GitRepository wrapper.
        
        Args:
            repo_path: Path to the local git repository
            
        Raises:
            git.InvalidGitRepositoryError: If path is not a valid git repo
            git.GitCommandError: If git operations fail
        """
        self.path = repo_path
        self._repo = git.Repo(repo_path)
    
    @property
    def name(self) -> str:
        """Get repository name from path"""
        return Path(self.path).name
    
    @property
    def is_detached(self) -> bool:
        """Check if HEAD is detached"""
        return self._repo.head.is_detached
    
    @property
    def current_branch(self) -> str:
        """
        Get current branch name.
        
        Returns:
            Branch name, or 'detached@<sha>' if HEAD is detached
        """
        if self._repo.head.is_detached:
            return f"detached@{self._repo.head.commit.hexsha[:7]}"
        return self._repo.active_branch.name
    
    @property
    def is_dirty(self) -> bool:
        """Check if repository has uncommitted changes"""
        return self._repo.is_dirty(untracked_files=True)
    
    @property
    def branches(self) -> List[str]:
        """Get list of local branch names"""
        return [branch.name for branch in self._repo.branches]
    
    @property
    def remote_branches(self) -> List[str]:
        """Get list of remote branch names (without remote prefix)"""
        try:
            return [
                ref.name.split('/')[-1]
                for ref in self._repo.remote().refs
                if not ref.name.endswith('/HEAD')
            ]
        except Exception:
            return ['main', 'master']
    
    def get_branches(self) -> List[Dict[str, Any]]:
        """
        Get list of local branches with commit info.
        
        Returns:
            List of dicts with branch info:
            - name: Branch name
            - is_current: Whether this is the active branch
            - commits: List of recent commits (up to 10)
        """
        branches = []
        for branch in self._repo.branches:
            branch_info = {
                "name": branch.name,
                "is_current": (
                    branch == self._repo.active_branch 
                    if not self.is_detached 
                    else False
                ),
                "commits": []
            }
            
            # Get last 10 commits for this branch
            try:
                for commit in list(self._repo.iter_commits(branch.name, max_count=10)):
                    branch_info["commits"].append({
                        "sha": commit.hexsha[:7],
                        "message": commit.message.strip().split("\n")[0][:60],
                        "author": commit.author.name,
                        "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M")
                    })
            except Exception:
                pass
            
            branches.append(branch_info)
        
        return branches
    
    def get_branch_names(self) -> List[str]:
        """Get list of branch names only"""
        return [branch.name for branch in self._repo.branches]
    
    def get_remotes(self) -> List[Dict[str, str]]:
        """
        Get list of remote repositories.
        
        Returns:
            List of dicts with 'name' and 'url' keys
        """
        return [
            {"name": remote.name, "url": remote.url}
            for remote in self._repo.remotes
        ]
    
    def get_remote_urls(self) -> List[str]:
        """Get list of remote URLs"""
        return [remote.url for remote in self._repo.remotes]
    
    def get_status(self) -> Dict[str, List[str]]:
        """
        Get working tree status.
        
        Returns:
            Dict with:
            - modified: List of modified file paths
            - staged: List of staged file paths
            - untracked: List of untracked file paths
        """
        return {
            "modified": [item.a_path for item in self._repo.index.diff(None)],
            "staged": (
                [item.a_path for item in self._repo.index.diff("HEAD")] 
                if not self.is_detached 
                else []
            ),
            "untracked": self._repo.untracked_files
        }
    
    def get_diff(self, file_path: Optional[str] = None) -> str:
        """
        Get diff of changes.
        
        Args:
            file_path: Optional specific file to diff
            
        Returns:
            Diff string
        """
        if file_path:
            return self._repo.git.diff(file_path)
        return self._repo.git.diff()
    
    def get_staged_diff(self, file_path: Optional[str] = None) -> str:
        """
        Get diff of staged changes.
        
        Args:
            file_path: Optional specific file to diff
            
        Returns:
            Diff string
        """
        if file_path:
            return self._repo.git.diff("--cached", file_path)
        return self._repo.git.diff("--cached")
    
    def stage_file(self, file_path: str) -> None:
        """Stage a file for commit"""
        self._repo.index.add([file_path])
    
    def unstage_file(self, file_path: str) -> None:
        """Unstage a file"""
        self._repo.index.reset(file_path)
    
    def stage_all(self) -> None:
        """Stage all changes"""
        self._repo.git.add("-A")
    
    def commit(self, message: str) -> str:
        """
        Create a commit with staged changes.
        
        Args:
            message: Commit message
            
        Returns:
            Commit SHA
        """
        commit = self._repo.index.commit(message)
        return commit.hexsha
    
    def push(self, remote: str = "origin", branch: Optional[str] = None) -> None:
        """
        Push commits to remote.
        
        Args:
            remote: Remote name (default: origin)
            branch: Branch name (default: current branch)
        """
        if branch is None:
            branch = self.current_branch
        self._repo.git.push(remote, branch)
    
    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> None:
        """
        Pull changes from remote.
        
        Args:
            remote: Remote name (default: origin)
            branch: Branch name (default: current branch)
        """
        if branch is None:
            branch = self.current_branch
        self._repo.git.pull(remote, branch)


def open_repository(repo_path: str) -> Optional[GitRepository]:
    """
    Open a git repository safely.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        GitRepository instance, or None if path is not a valid repo
    """
    try:
        return GitRepository(repo_path)
    except (git.InvalidGitRepositoryError, git.GitCommandError):
        return None


def extract_github_repo_name(url: str) -> Optional[str]:
    """
    Extract owner/repo from a GitHub URL.
    
    Args:
        url: Git remote URL (SSH or HTTPS)
        
    Returns:
        Repository full name (owner/repo), or None if not a GitHub URL
    """
    # Handle SSH URLs: git@github.com:owner/repo.git
    if url.startswith("git@github.com:"):
        repo_path = url.replace("git@github.com:", "")
        if repo_path.endswith(".git"):
            repo_path = repo_path[:-4]
        parts = repo_path.split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
    
    # Handle HTTPS URLs: https://github.com/owner/repo.git
    elif "github.com/" in url:
        clean_url = url
        if clean_url.endswith(".git"):
            clean_url = clean_url[:-4]
        parts = clean_url.split("github.com/")[-1].split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
    
    return None


def load_repo_details(repo_path: str, gh_wrapper=None) -> Dict[str, Any]:
    """
    Load comprehensive repository details.
    
    This function consolidates all the repository info gathering
    that was previously done in UI thread classes.
    
    Args:
        repo_path: Path to the local repository
        gh_wrapper: Optional GHWrapper instance for GitHub API calls
        
    Returns:
        Dict with repository details:
        - local: Basic repo info (name, path, branch, is_dirty)
        - remote: GitHub repo data if available
        - branches: List of branches with commits
        - remotes: List of remotes
        - topics: GitHub topics if available
        - status: Working tree status
        - repo_full_name: GitHub owner/repo if detected
        - error: Error message if failed
    """
    details = {
        "local": {},
        "remote": None,
        "commits": [],
        "branches": [],
        "remotes": [],
        "topics": [],
        "status": {},
        "repo_full_name": None,
        "error": None
    }
    
    try:
        repo = GitRepository(repo_path)
        
        # Basic info
        details["local"] = {
            "name": repo.name,
            "path": repo_path,
            "branch": repo.current_branch,
            "is_dirty": repo.is_dirty,
        }
        
        # Branches with commits
        details["branches"] = repo.get_branches()
        
        # Remotes and GitHub detection
        repo_full_name = None
        for remote_info in repo.get_remotes():
            details["remotes"].append(remote_info)
            
            # Try to extract GitHub repo name
            github_name = extract_github_repo_name(remote_info["url"])
            if github_name and not repo_full_name:
                repo_full_name = github_name
            
            # Get remote info from GitHub if available
            if github_name and gh_wrapper and details["remote"] is None:
                remote_data = gh_wrapper.get_repo(github_name)
                if remote_data:
                    details["remote"] = remote_data
        
        # Store repo full name
        if repo_full_name:
            details["repo_full_name"] = repo_full_name
        
        # Get topics from GitHub API if remote exists
        if details["remote"]:
            topics_data = details["remote"].get("repositoryTopics", [])
            details["topics"] = topics_data if isinstance(topics_data, list) else []
        
        # Status
        details["status"] = repo.get_status()
        
    except git.InvalidGitRepositoryError:
        details["error"] = "Not a valid Git repository"
    except Exception as e:
        details["error"] = str(e)
    
    return details

"""
Local repository management
Scans filesystem for Git repositories
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
import git


class RepoManager:
    """Manages local Git repositories"""
    
    def __init__(self):
        self.repos: List[Dict[str, str]] = []
    
    def scan_directory(self, path: str, max_depth: int = 3) -> List[Dict[str, str]]:
        """
        Scan directory for Git repositories
        
        Args:
            path: Root path to scan
            max_depth: Maximum directory depth to scan
            
        Returns:
            List of repository info dicts
        """
        repos = []
        path_obj = Path(path).expanduser().resolve()
        
        if not path_obj.exists():
            return repos
        
        try:
            for root, dirs, files in os.walk(path_obj):
                # Calculate current depth
                depth = len(Path(root).relative_to(path_obj).parts)
                if depth > max_depth:
                    dirs.clear()  # Don't descend further
                    continue
                
                # Check if this is a git repo
                if '.git' in dirs:
                    try:
                        repo = git.Repo(root)
                        repo_info = self._get_repo_info(repo, root)
                        repos.append(repo_info)
                        
                        # Don't descend into git repos
                        dirs.clear()
                    except (git.InvalidGitRepositoryError, git.GitCommandError):
                        pass
        except PermissionError:
            pass
        
        self.repos = repos
        return repos
    
    def _get_repo_info(self, repo: git.Repo, path: str) -> Dict[str, str]:
        """Extract information from a Git repository"""
        info = {
            "path": path,
            "name": Path(path).name,
            "branch": "",
            "remote": "",
            "status": "clean",
            "ahead": 0,
            "behind": 0,
        }
        
        try:
            # Get current branch
            if repo.head.is_detached:
                info["branch"] = f"detached@{repo.head.commit.hexsha[:7]}"
            else:
                info["branch"] = repo.active_branch.name
            
            # Get remote URL
            if repo.remotes:
                info["remote"] = repo.remotes.origin.url if "origin" in [r.name for r in repo.remotes] else repo.remotes[0].url
            
            # Check if dirty
            if repo.is_dirty(untracked_files=True):
                info["status"] = "modified"
            
            # Check ahead/behind
            if repo.remotes and not repo.head.is_detached:
                try:
                    branch = repo.active_branch
                    tracking = branch.tracking_branch()
                    if tracking:
                        ahead, behind = repo.iter_commits(f'{tracking}..{branch}'), \
                                      repo.iter_commits(f'{branch}..{tracking}')
                        info["ahead"] = sum(1 for _ in ahead)
                        info["behind"] = sum(1 for _ in behind)
                except Exception:
                    pass
                    
        except Exception as e:
            info["status"] = f"error: {str(e)}"
        
        return info
    
    def get_repo_at_path(self, path: str) -> Optional[git.Repo]:
        """Get Git repository at specific path"""
        try:
            return git.Repo(path)
        except (git.InvalidGitRepositoryError, git.GitCommandError):
            return None
    
    def init_repo(self, path: str) -> bool:
        """Initialize a new Git repository"""
        try:
            git.Repo.init(path)
            return True
        except Exception:
            return False

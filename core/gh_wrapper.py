"""
GitHub CLI (gh) wrapper
Provides Python interface to gh commands
"""

import subprocess
import json
from typing import Optional, List, Dict, Any


class GHWrapper:
    """Wrapper for GitHub CLI operations"""
    
    def __init__(self):
        self._check_gh_installed()
    
    def _check_gh_installed(self) -> bool:
        """Check if gh CLI is installed"""
        try:
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("GitHub CLI (gh) is not installed or not in PATH")
    
    def _run_command(self, args: List[str], capture_json: bool = False) -> Dict[str, Any]:
        """
        Run a gh command and return result
        
        Args:
            args: Command arguments (without 'gh' prefix)
            capture_json: If True, parse output as JSON
            
        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        cmd = ["gh"] + args
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            output = result.stdout.strip()
            error = result.stderr.strip()
            success = result.returncode == 0
            
            if capture_json and success and output:
                try:
                    output = json.loads(output)
                except json.JSONDecodeError:
                    pass
            
            return {
                "success": success,
                "output": output,
                "error": error,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }
    
    # =========================================================================
    # Authentication
    # =========================================================================
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated with GitHub"""
        result = self._run_command(["auth", "status"])
        return result["success"]
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Get detailed authentication status"""
        result = self._run_command(["auth", "status"])
        return result
    
    def login(self, web: bool = True) -> Dict[str, Any]:
        """
        Login to GitHub
        
        Args:
            web: If True, use web browser flow; otherwise use token
        """
        args = ["auth", "login"]
        if web:
            args.append("--web")
        return self._run_command(args)
    
    def logout(self, hostname: str = "github.com") -> Dict[str, Any]:
        """Logout from GitHub"""
        return self._run_command(["auth", "logout", "--hostname", hostname])
    
    # =========================================================================
    # Repository Operations
    # =========================================================================
    
    def list_repos(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List user's repositories
        
        Returns:
            List of repository dicts
        """
        result = self._run_command(
            ["repo", "list", "--json", "name,owner,description,url,isPrivate,updatedAt", 
             "--limit", str(limit)],
            capture_json=True
        )
        
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
    def create_repo(self, name: str, description: str = "", 
                   private: bool = False, clone: bool = True) -> Dict[str, Any]:
        """
        Create a new repository
        
        Args:
            name: Repository name
            description: Repository description
            private: Make repository private
            clone: Clone after creation
        """
        args = ["repo", "create", name, "--description", description]
        
        if private:
            args.append("--private")
        else:
            args.append("--public")
        
        if clone:
            args.append("--clone")
        
        return self._run_command(args)
    
    def delete_repo(self, repo: str, confirm: bool = True) -> Dict[str, Any]:
        """
        Delete a repository
        
        Args:
            repo: Repository name (owner/repo)
            confirm: Skip confirmation prompt
        """
        args = ["repo", "delete", repo]
        if confirm:
            args.append("--yes")
        return self._run_command(args)
    
    def view_repo(self, repo: Optional[str] = None) -> Dict[str, Any]:
        """
        View repository details
        
        Args:
            repo: Repository name (owner/repo), or None for current
        """
        args = ["repo", "view", "--json", 
                "name,owner,description,url,isPrivate,createdAt,updatedAt,pushedAt"]
        if repo:
            args.append(repo)
        
        return self._run_command(args, capture_json=True)
    
    def edit_repo(self, repo: str, **kwargs) -> Dict[str, Any]:
        """
        Edit repository settings
        
        Args:
            repo: Repository name (owner/repo)
            **kwargs: Settings to change (description, visibility, homepage, etc.)
        """
        args = ["repo", "edit", repo]
        
        if "description" in kwargs:
            args.extend(["--description", kwargs["description"]])
        if "visibility" in kwargs:
            args.extend(["--visibility", kwargs["visibility"]])
        if "homepage" in kwargs:
            args.extend(["--homepage", kwargs["homepage"]])
        
        return self._run_command(args)
    
    def clone_repo(self, repo: str, directory: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone a repository
        
        Args:
            repo: Repository name (owner/repo)
            directory: Target directory (optional)
        """
        args = ["repo", "clone", repo]
        if directory:
            args.append(directory)
        return self._run_command(args)
    
    # =========================================================================
    # Pull Requests
    # =========================================================================
    
    def list_prs(self, repo: Optional[str] = None, state: str = "open") -> List[Dict[str, Any]]:
        """List pull requests"""
        args = ["pr", "list", "--json", "number,title,state,author,createdAt", 
                "--state", state]
        if repo:
            args.extend(["--repo", repo])
        
        result = self._run_command(args, capture_json=True)
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
    def view_pr(self, pr_number: int, repo: Optional[str] = None) -> Dict[str, Any]:
        """View pull request details"""
        args = ["pr", "view", str(pr_number), "--json", 
                "number,title,body,state,author,createdAt,mergedAt"]
        if repo:
            args.extend(["--repo", repo])
        
        return self._run_command(args, capture_json=True)
    
    # =========================================================================
    # Issues
    # =========================================================================
    
    def list_issues(self, repo: Optional[str] = None, state: str = "open") -> List[Dict[str, Any]]:
        """List issues"""
        args = ["issue", "list", "--json", "number,title,state,author,createdAt",
                "--state", state]
        if repo:
            args.extend(["--repo", repo])
        
        result = self._run_command(args, capture_json=True)
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
    def view_issue(self, issue_number: int, repo: Optional[str] = None) -> Dict[str, Any]:
        """View issue details"""
        args = ["issue", "view", str(issue_number), "--json",
                "number,title,body,state,author,createdAt"]
        if repo:
            args.extend(["--repo", repo])
        
        return self._run_command(args, capture_json=True)

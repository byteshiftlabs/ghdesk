"""
GitHub pull request operations
"""

from typing import Optional, List, Dict, Any


class PullRequestsMixin:
    """Pull request operations for GitHub CLI"""
    
    def list_prs(
        self, 
        repo: Optional[str] = None, 
        state: str = "open"
    ) -> List[Dict[str, Any]]:
        """
        List pull requests
        
        Args:
            repo: Repository name (owner/repo), or None for current
            state: PR state filter ('open', 'closed', 'merged', 'all')
            
        Returns:
            List of pull request dicts
        """
        args = ["pr", "list", "--json", "number,title,state,author,createdAt", 
                "--state", state]
        if repo:
            args.extend(["--repo", repo])
        
        result = self._run_command(args, capture_json=True)
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
    def view_pr(self, pr_number: int, repo: Optional[str] = None) -> Dict[str, Any]:
        """
        View pull request details
        
        Args:
            pr_number: Pull request number
            repo: Repository name (owner/repo), or None for current
            
        Returns:
            Dict with PR details
        """
        args = ["pr", "view", str(pr_number), "--json", 
                "number,title,body,state,author,createdAt,mergedAt"]
        if repo:
            args.extend(["--repo", repo])
        
        return self._run_command(args, capture_json=True)

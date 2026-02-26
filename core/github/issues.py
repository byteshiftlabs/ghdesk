"""
GitHub issues operations
"""

from typing import Optional, List, Dict, Any


class IssuesMixin:
    """Issues operations for GitHub CLI"""
    
    def list_issues(
        self, 
        repo: Optional[str] = None, 
        state: str = "open"
    ) -> List[Dict[str, Any]]:
        """
        List issues
        
        Args:
            repo: Repository name (owner/repo), or None for current
            state: Issue state filter ('open', 'closed', 'all')
            
        Returns:
            List of issue dicts
        """
        args = ["issue", "list", "--json", "number,title,state,author,createdAt",
                "--state", state]
        if repo:
            args.extend(["--repo", repo])
        
        result = self._run_command(args, capture_json=True)
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
    def view_issue(self, issue_number: int, repo: Optional[str] = None) -> Dict[str, Any]:
        """
        View issue details
        
        Args:
            issue_number: Issue number
            repo: Repository name (owner/repo), or None for current
            
        Returns:
            Dict with issue details
        """
        args = ["issue", "view", str(issue_number), "--json",
                "number,title,body,state,author,createdAt"]
        if repo:
            args.extend(["--repo", repo])
        
        return self._run_command(args, capture_json=True)

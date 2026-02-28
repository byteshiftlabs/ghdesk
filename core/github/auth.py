"""
GitHub authentication operations
"""

from typing import Dict, Any

from core.github.base import GHBase


class AuthMixin:
    """Authentication methods for GitHub CLI"""
    
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

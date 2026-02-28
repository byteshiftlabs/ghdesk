"""
GitHub CLI base wrapper
Provides common functionality for gh CLI commands
"""

import subprocess
import json
from typing import Optional, List, Dict, Any

from core.exceptions import GitHubNotInstalledError, GitHubAPIError
from core.logging_config import get_logger

logger = get_logger("github.base")


def make_result(success: bool, output: Any = "", error: str = "", returncode: int = 0) -> Dict[str, Any]:
    """Create a standard result dict"""
    return {"success": success, "output": output, "error": error, "returncode": returncode}


def make_error(error: str, returncode: int = -1) -> Dict[str, Any]:
    """Create an error result dict"""
    return make_result(False, "", error, returncode)


def make_success(output: Any = "", message: str = "") -> Dict[str, Any]:
    """Create a success result dict"""
    return make_result(True, output or message, "", 0)


class GHBase:
    """Base class for GitHub CLI operations"""
    
    def __init__(self):
        self._check_gh_installed()
    
    def _check_gh_installed(self) -> bool:
        """Check if gh CLI is installed"""
        try:
            subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.debug("GitHub CLI found")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("GitHub CLI not found")
            raise GitHubNotInstalledError()
    
    def _run_command(
        self, 
        args: List[str], 
        capture_json: bool = False, 
        input_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a gh CLI command
        
        Args:
            args: Command arguments (without 'gh')
            capture_json: Whether to parse output as JSON
            input_data: Optional stdin data
            
        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        cmd = ["gh"] + args
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                input=input_data
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
            return make_error(str(e))
    
    def _run_git_command(
        self, 
        args: List[str], 
        cwd: str
    ) -> Dict[str, Any]:
        """
        Run a git command in a specific directory
        
        Args:
            args: Command arguments (without 'git')
            cwd: Working directory for the command
            
        Returns:
            Dict with 'success', 'output', 'error', 'returncode' keys
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=False,
                cwd=cwd
            )
            return make_result(
                success=result.returncode == 0,
                output=result.stdout.strip(),
                error=result.stderr.strip(),
                returncode=result.returncode
            )
        except Exception as e:
            return make_error(str(e))

"""
GitHub tags/releases operations
"""

import subprocess
from typing import Optional, List, Dict, Any


class TagsMixin:
    """Tags and releases operations for GitHub CLI"""
    
    def list_tags(
        self, 
        repo: Optional[str] = None, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List repository tags
        
        Args:
            repo: Repository name (owner/repo), or None for current
            limit: Maximum number of tags to return
            
        Returns:
            List of tag dicts with name
        """
        args = ["api", "repos"]
        
        if repo:
            args.append(repo)
        
        args.extend(["/tags", "--jq", ".[].name", "--paginate"])
        
        result = self._run_command(args)
        if result["success"] and result["output"]:
            tags = result["output"].strip().split("\n")
            return [{"name": tag} for tag in tags if tag]
        return []
    
    def create_tag(
        self, 
        repo_path: str, 
        tag_name: str, 
        target: str = "HEAD", 
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new tag via Git (local) and push to remote
        
        Args:
            repo_path: Local repository path (directory)
            tag_name: Name of the tag (e.g., "v1.0.0")
            target: Commit SHA or branch name (default: HEAD)
            message: Optional tag message (creates annotated tag)
            
        Returns:
            Dict with success status and message
        """
        try:
            # Create tag locally
            git_cmd = ["git", "tag"]
            if message:
                git_cmd.extend(["-a", tag_name, "-m", message])
            else:
                git_cmd.append(tag_name)
            git_cmd.append(target)
            
            result = subprocess.run(
                git_cmd, 
                capture_output=True, 
                text=True, 
                check=False,
                cwd=repo_path
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "output": "",
                    "error": f"Failed to create tag: {result.stderr.strip()}",
                    "returncode": result.returncode
                }
            
            # Push tag to remote
            push_result = subprocess.run(
                ["git", "push", "origin", tag_name],
                capture_output=True,
                text=True,
                check=False,
                cwd=repo_path
            )
            
            if push_result.returncode != 0:
                return {
                    "success": False,
                    "output": result.stdout.strip(),
                    "error": f"Tag created locally but push failed: "
                             f"{push_result.stderr.strip()}",
                    "returncode": push_result.returncode
                }
            
            return {
                "success": True,
                "output": f"Tag '{tag_name}' created and pushed successfully",
                "error": "",
                "returncode": 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }
    
    def delete_tag(
        self, 
        repo_path: str, 
        tag_name: str, 
        remote: bool = True
    ) -> Dict[str, Any]:
        """
        Delete a tag locally and optionally from remote
        
        Args:
            repo_path: Local repository path (directory)
            tag_name: Name of the tag to delete
            remote: Also delete from remote (default: True)
            
        Returns:
            Dict with success status and message
        """
        try:
            # Delete local tag
            result = subprocess.run(
                ["git", "tag", "-d", tag_name],
                capture_output=True,
                text=True,
                check=False,
                cwd=repo_path
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "output": "",
                    "error": f"Failed to delete local tag: {result.stderr.strip()}",
                    "returncode": result.returncode
                }
            
            # Delete remote tag if requested
            if remote:
                push_result = subprocess.run(
                    ["git", "push", "origin", f":refs/tags/{tag_name}"],
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=repo_path
                )
                
                if push_result.returncode != 0:
                    return {
                        "success": False,
                        "output": result.stdout.strip(),
                        "error": f"Local tag deleted but remote deletion failed: "
                                 f"{push_result.stderr.strip()}",
                        "returncode": push_result.returncode
                    }
            
            return {
                "success": True,
                "output": f"Tag '{tag_name}' deleted successfully",
                "error": "",
                "returncode": 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }

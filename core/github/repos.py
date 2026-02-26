"""
GitHub repository operations
"""

import base64
import datetime
import json
from typing import Optional, List, Dict, Any


class ReposMixin:
    """Repository operations for GitHub CLI"""
    
    def list_repos(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List user's repositories
        
        Returns:
            List of repository dicts
        """
        result = self._run_command(
            ["repo", "list", "--json", 
             "name,owner,description,url,isPrivate,updatedAt,licenseInfo", 
             "--limit", str(limit)],
            capture_json=True
        )
        
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
    def create_repo(
        self, 
        name: str, 
        description: str = "", 
        private: bool = False, 
        clone: bool = True
    ) -> Dict[str, Any]:
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
    
    def get_repo(self, repo: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed repository information
        
        Args:
            repo: Repository name (owner/repo)
            
        Returns:
            Repository dict or None if not found
        """
        args = ["repo", "view", repo, "--json", 
                "name,owner,description,url,isPrivate,stargazerCount,"
                "forkCount,issues,createdAt,updatedAt,repositoryTopics"]
        result = self._run_command(args, capture_json=True)
        
        if result["success"] and isinstance(result["output"], dict):
            return result["output"]
        return None
    
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
    
    def change_license(self, repo: str, license_key: str) -> Dict[str, Any]:
        """
        Change repository license by creating/updating LICENSE file.
        
        Args:
            repo: Repository name (owner/repo)
            license_key: SPDX license identifier (e.g., 'mit', 'apache-2.0', 'gpl-3.0')
            
        Returns:
            Result dict with success status
        """
        # Get license template from GitHub
        license_result = self._run_command(
            ["api", f"licenses/{license_key}"],
            capture_json=True
        )
        
        if not license_result.get("success"):
            return {
                "success": False, 
                "error": f"Failed to get license template: "
                         f"{license_result.get('error', 'Unknown error')}"
            }
        
        license_data = license_result.get("output", {})
        license_body = license_data.get("body", "")
        
        if not license_body:
            return {"success": False, "error": "License template is empty"}
        
        # Replace placeholders in license template
        current_year = str(datetime.datetime.now().year)
        
        # Get user info for copyright
        user_result = self._run_command(["api", "user"], capture_json=True)
        user_name = "Your Name"
        if user_result.get("success"):
            user_data = user_result.get("output", {})
            user_name = user_data.get("name") or user_data.get("login", "Your Name")
        
        # Replace common placeholders
        license_body = license_body.replace("[year]", current_year)
        license_body = license_body.replace("[yyyy]", current_year)
        license_body = license_body.replace("<year>", current_year)
        license_body = license_body.replace("[fullname]", user_name)
        license_body = license_body.replace("[name of copyright owner]", user_name)
        license_body = license_body.replace("<name of author>", user_name)
        license_body = license_body.replace("[email]", "")
        
        # Check if LICENSE file exists
        check_result = self._run_command(
            ["api", f"repos/{repo}/contents/LICENSE"],
            capture_json=True
        )
        
        license_content_b64 = base64.b64encode(license_body.encode()).decode()
        
        if check_result.get("success"):
            # File exists, update it
            file_sha = check_result.get("output", {}).get("sha", "")
            update_data = json.dumps({
                "message": f"Update LICENSE to {license_key.upper()}",
                "content": license_content_b64,
                "sha": file_sha
            })
            result = self._run_command(
                ["api", f"repos/{repo}/contents/LICENSE", "-X", "PUT", "--input", "-"],
                input_data=update_data
            )
        else:
            # File doesn't exist, create it
            create_data = json.dumps({
                "message": f"Add {license_key.upper()} license",
                "content": license_content_b64
            })
            result = self._run_command(
                ["api", f"repos/{repo}/contents/LICENSE", "-X", "PUT", "--input", "-"],
                input_data=create_data
            )
        
        if result.get("success"):
            return {"success": True, "message": f"License changed to {license_key.upper()}"}
        else:
            return {"success": False, "error": result.get("error", "Failed to update license")}
    
    def add_topic(self, repo: str, topic: str) -> Dict[str, Any]:
        """
        Add a topic to a repository
        
        Args:
            repo: Repository name (owner/repo)
            topic: Topic name to add (e.g., "python", "machine-learning")
            
        Returns:
            Result dict with success status
        """
        # First, get existing topics
        get_result = self.get_repo(repo)
        if not get_result:
            return {"success": False, "error": "Failed to get repository info"}
        
        existing_topics = get_result.get("repositoryTopics") or []
        topic_names = [
            t.get("name") for t in existing_topics 
            if isinstance(t, dict) and t.get("name")
        ]
        
        # Add new topic if not already present
        if topic.lower() not in [t.lower() for t in topic_names]:
            topic_names.append(topic.lower())
        
        # Update topics via API
        topics_json = json.dumps({"names": topic_names})
        result = self._run_command(
            ["api", f"repos/{repo}/topics", "-X", "PUT", "--input", "-"],
            input_data=topics_json
        )
        
        return result
    
    def remove_topic(self, repo: str, topic: str) -> Dict[str, Any]:
        """
        Remove a topic from a repository
        
        Args:
            repo: Repository name (owner/repo)
            topic: Topic name to remove
            
        Returns:
            Result dict with success status
        """
        # Get existing topics
        get_result = self.get_repo(repo)
        if not get_result:
            return {"success": False, "error": "Failed to get repository info"}
        
        existing_topics = get_result.get("repositoryTopics") or []
        topic_names = [
            t.get("name") for t in existing_topics 
            if isinstance(t, dict) and t.get("name")
        ]
        
        # Remove topic (case insensitive)
        topic_names = [t for t in topic_names if t.lower() != topic.lower()]
        
        # Update topics via API
        topics_json = json.dumps({"names": topic_names})
        result = self._run_command(
            ["api", f"repos/{repo}/topics", "-X", "PUT", "--input", "-"],
            input_data=topics_json
        )
        
        return result
    
    def get_commits(
        self, 
        repo: str, 
        branch: Optional[str] = None, 
        limit: int = 20
    ) -> list:
        """
        Get recent commits from a repository
        
        Args:
            repo: Repository name (owner/repo)
            branch: Branch name to get commits from (optional)
            limit: Maximum number of commits to fetch
            
        Returns:
            List of commit dicts with sha, message, author, and date
        """
        jq_query = (
            f".[:{limit}] | map({{sha: .sha[0:7], message: .commit.message, "
            f"author: .commit.author.name, date: .commit.author.date}})"
        )
        
        if branch:
            args = ["api", f"repos/{repo}/commits?sha={branch}", "-q", jq_query]
        else:
            args = ["api", f"repos/{repo}/commits", "-q", jq_query]
        
        result = self._run_command(args, capture_json=True)
        
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
    def get_branches(self, repo: str) -> list:
        """
        Get branches from a repository
        
        Args:
            repo: Repository name (owner/repo)
            
        Returns:
            List of branch dicts with name
        """
        args = ["api", f"repos/{repo}/branches", "-q", "map({name: .name})"]
        result = self._run_command(args, capture_json=True)
        
        if result["success"] and isinstance(result["output"], list):
            return result["output"]
        return []
    
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

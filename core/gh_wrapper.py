"""
GitHub CLI (gh) wrapper
Provides Python interface to gh commands
"""

import subprocess
import json
import os
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
    
    def _run_command(self, args: List[str], capture_json: bool = False, input_data: Optional[str] = None) -> Dict[str, Any]:
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
            ["repo", "list", "--json", "name,owner,description,url,isPrivate,updatedAt,licenseInfo", 
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
    
    def get_repo(self, repo: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed repository information
        
        Args:
            repo: Repository name (owner/repo)
            
        Returns:
            Repository dict or None if not found
        """
        args = ["repo", "view", repo, "--json", 
                "name,owner,description,url,isPrivate,stargazerCount,forkCount,issues,createdAt,updatedAt,repositoryTopics"]
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
            return {"success": False, "error": f"Failed to get license template: {license_result.get('error', 'Unknown error')}"}
        
        license_data = license_result.get("output", {})
        license_body = license_data.get("body", "")
        
        if not license_body:
            return {"success": False, "error": "License template is empty"}
        
        # Replace placeholders in license template
        import datetime
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
        
        import base64
        import json
        
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
        # GitHub CLI doesn't have a direct topic command, use API via gh api
        args = ["api", f"repos/{repo}/topics", "-X", "PUT", "-F", f"names[]=@-"]
        
        # First, get existing topics
        get_result = self.get_repo(repo)
        if not get_result:
            return {"success": False, "error": "Failed to get repository info"}
        
        existing_topics = get_result.get("repositoryTopics") or []
        topic_names = [t.get("name") for t in existing_topics if isinstance(t, dict) and t.get("name")]
        
        # Add new topic if not already present
        if topic.lower() not in [t.lower() for t in topic_names]:
            topic_names.append(topic.lower())
        
        # Update topics via API
        import json
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
        topic_names = [t.get("name") for t in existing_topics if isinstance(t, dict) and t.get("name")]
        
        # Remove topic (case insensitive)
        topic_names = [t for t in topic_names if t.lower() != topic.lower()]
        
        # Update topics via API
        import json
        topics_json = json.dumps({"names": topic_names})
        result = self._run_command(
            ["api", f"repos/{repo}/topics", "-X", "PUT", "--input", "-"],
            input_data=topics_json
        )
        
        return result
    
    def get_commits(self, repo: str, branch: str = None, limit: int = 20) -> list:
        """
        Get recent commits from a repository
        
        Args:
            repo: Repository name (owner/repo)
            branch: Branch name to get commits from (optional, defaults to all branches)
            limit: Maximum number of commits to fetch
            
        Returns:
            List of commit dicts with sha, message, author, and date
        """
        # Use jq to format as array of objects
        if branch:
            args = ["api", f"repos/{repo}/commits?sha={branch}", "-q", f".[:{limit}] | map({{sha: .sha[0:7], message: .commit.message, author: .commit.author.name, date: .commit.author.date}})"]
        else:
            args = ["api", f"repos/{repo}/commits", "-q", f".[:{limit}] | map({{sha: .sha[0:7], message: .commit.message, author: .commit.author.name, date: .commit.author.date}})"]
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
    
    # =========================================================================
    # Tags/Releases
    # =========================================================================
    
    def list_tags(self, repo: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List repository tags
        
        Args:
            repo: Repository name (owner/repo), or None for current
            limit: Maximum number of tags to return
            
        Returns:
            List of tag dicts with name, commit info
        """
        args = ["api", "repos"]
        
        if repo:
            args.append(repo)
        else:
            # Will use current repo
            pass
        
        args.extend(["/tags", "--jq", ".[].name", "--paginate"])
        
        result = self._run_command(args)
        if result["success"] and result["output"]:
            tags = result["output"].strip().split("\n")
            return [{"name": tag} for tag in tags if tag]
        return []
    
    def create_tag(self, repo: str, tag_name: str, target: str = "HEAD", 
                  message: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new tag via Git (local) and push to remote
        
        Args:
            repo: Repository path (local directory)
            tag_name: Name of the tag (e.g., "v1.0.0")
            target: Commit SHA or branch name (default: HEAD)
            message: Optional tag message (creates annotated tag)
            
        Returns:
            Dict with success status and message
        """
        import subprocess
        
        try:
            # Change to repo directory
            original_dir = os.getcwd()
            os.chdir(repo)
            
            # Create tag locally
            git_cmd = ["git", "tag"]
            if message:
                git_cmd.extend(["-a", tag_name, "-m", message])
            else:
                git_cmd.append(tag_name)
            git_cmd.append(target)
            
            result = subprocess.run(git_cmd, capture_output=True, text=True, check=False)
            
            if result.returncode != 0:
                os.chdir(original_dir)
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
                check=False
            )
            
            os.chdir(original_dir)
            
            if push_result.returncode != 0:
                return {
                    "success": False,
                    "output": result.stdout.strip(),
                    "error": f"Tag created locally but push failed: {push_result.stderr.strip()}",
                    "returncode": push_result.returncode
                }
            
            return {
                "success": True,
                "output": f"Tag '{tag_name}' created and pushed successfully",
                "error": "",
                "returncode": 0
            }
            
        except Exception as e:
            try:
                os.chdir(original_dir)
            except:
                pass
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }
    
    def delete_tag(self, repo: str, tag_name: str, remote: bool = True) -> Dict[str, Any]:
        """
        Delete a tag locally and optionally from remote
        
        Args:
            repo: Repository path (local directory)
            tag_name: Name of the tag to delete
            remote: Also delete from remote (default: True)
            
        Returns:
            Dict with success status and message
        """
        import subprocess
        
        try:
            original_dir = os.getcwd()
            os.chdir(repo)
            
            # Delete local tag
            result = subprocess.run(
                ["git", "tag", "-d", tag_name],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                os.chdir(original_dir)
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
                    check=False
                )
                
                os.chdir(original_dir)
                
                if push_result.returncode != 0:
                    return {
                        "success": False,
                        "output": result.stdout.strip(),
                        "error": f"Local tag deleted but remote deletion failed: {push_result.stderr.strip()}",
                        "returncode": push_result.returncode
                    }
            else:
                os.chdir(original_dir)
            
            return {
                "success": True,
                "output": f"Tag '{tag_name}' deleted successfully",
                "error": "",
                "returncode": 0
            }
            
        except Exception as e:
            try:
                os.chdir(original_dir)
            except:
                pass
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }

    # =========================================================================
    # Pull Requests
    # =========================================================================
    
    def list_prs(self, repo: str, state: str = "open", 
                 author: Optional[str] = None, limit: int = 30) -> Dict[str, Any]:
        """
        List pull requests for a repository.
        
        Args:
            repo: Repository name (owner/repo)
            state: PR state - 'open', 'closed', 'merged', or 'all'
            author: Filter by author username
            limit: Maximum number of PRs to return
            
        Returns:
            Dict with 'success' and 'output' (list of PR objects)
        """
        args = ["pr", "list", "--repo", repo, "--state", state, 
                "--limit", str(limit), "--json", 
                "number,title,author,state,createdAt,updatedAt,headRefName,baseRefName,isDraft,mergeable"]
        
        if author:
            args.extend(["--author", author])
        
        result = self._run_command(args, capture_json=True)
        return result
    
    def get_pr(self, repo: str, pr_number: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific pull request.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            
        Returns:
            Dict with PR details
        """
        args = ["pr", "view", str(pr_number), "--repo", repo, "--json",
                "number,title,body,author,state,createdAt,updatedAt,closedAt,"
                "mergedAt,headRefName,baseRefName,isDraft,mergeable,additions,"
                "deletions,changedFiles,comments,reviews,labels,assignees"]
        
        result = self._run_command(args, capture_json=True)
        return result
    
    def create_pr(self, repo: str, title: str, body: str = "",
                  head: Optional[str] = None, base: str = "main",
                  draft: bool = False) -> Dict[str, Any]:
        """
        Create a new pull request.
        
        Args:
            repo: Repository name (owner/repo)
            title: PR title
            body: PR description/body
            head: Source branch (defaults to current branch)
            base: Target branch (default: main)
            draft: Create as draft PR
            
        Returns:
            Dict with created PR details
        """
        args = ["pr", "create", "--repo", repo, "--title", title,
                "--body", body, "--base", base]
        
        if head:
            args.extend(["--head", head])
        
        if draft:
            args.append("--draft")
        
        result = self._run_command(args)
        return result
    
    def merge_pr(self, repo: str, pr_number: int, 
                 method: str = "merge", delete_branch: bool = False) -> Dict[str, Any]:
        """
        Merge a pull request.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            method: Merge method - 'merge', 'squash', or 'rebase'
            delete_branch: Delete branch after merge
            
        Returns:
            Dict with merge result
        """
        args = ["pr", "merge", str(pr_number), "--repo", repo]
        
        if method == "squash":
            args.append("--squash")
        elif method == "rebase":
            args.append("--rebase")
        else:
            args.append("--merge")
        
        if delete_branch:
            args.append("--delete-branch")
        
        result = self._run_command(args)
        return result
    
    def close_pr(self, repo: str, pr_number: int, 
                 comment: Optional[str] = None) -> Dict[str, Any]:
        """
        Close a pull request without merging.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            comment: Optional closing comment
            
        Returns:
            Dict with close result
        """
        args = ["pr", "close", str(pr_number), "--repo", repo]
        
        if comment:
            args.extend(["--comment", comment])
        
        result = self._run_command(args)
        return result
    
    def reopen_pr(self, repo: str, pr_number: int) -> Dict[str, Any]:
        """
        Reopen a closed pull request.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            
        Returns:
            Dict with reopen result
        """
        args = ["pr", "reopen", str(pr_number), "--repo", repo]
        result = self._run_command(args)
        return result
    
    def get_pr_diff(self, repo: str, pr_number: int) -> Dict[str, Any]:
        """
        Get the diff for a pull request.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            
        Returns:
            Dict with diff text
        """
        args = ["pr", "diff", str(pr_number), "--repo", repo]
        result = self._run_command(args)
        return result
    
    def comment_on_pr(self, repo: str, pr_number: int, 
                      comment: str) -> Dict[str, Any]:
        """
        Add a comment to a pull request.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            comment: Comment text
            
        Returns:
            Dict with comment result
        """
        args = ["pr", "comment", str(pr_number), "--repo", repo, 
                "--body", comment]
        result = self._run_command(args)
        return result
    
    def review_pr(self, repo: str, pr_number: int, 
                  action: str = "comment", body: str = "") -> Dict[str, Any]:
        """
        Review a pull request.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            action: Review action - 'approve', 'request-changes', or 'comment'
            body: Review comment
            
        Returns:
            Dict with review result
        """
        args = ["pr", "review", str(pr_number), "--repo", repo]
        
        if action == "approve":
            args.append("--approve")
        elif action == "request-changes":
            args.append("--request-changes")
        else:
            args.append("--comment")
        
        if body:
            args.extend(["--body", body])
        
        result = self._run_command(args)
        return result
    
    def get_pr_checks(self, repo: str, pr_number: int) -> Dict[str, Any]:
        """
        Get CI/CD check status for a pull request.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            
        Returns:
            Dict with check status
        """
        args = ["pr", "checks", str(pr_number), "--repo", repo]
        result = self._run_command(args)
        return result
    
    def get_repo_collaborators(self, repo: str) -> Dict[str, Any]:
        """
        Get list of collaborators for a repository.
        
        Args:
            repo: Repository name (owner/repo)
            
        Returns:
            Dict with list of collaborators
        """
        args = ["api", f"repos/{repo}/collaborators", "--paginate"]
        result = self._run_command(args, capture_json=True)
        return result
    
    def get_repo_labels(self, repo: str) -> Dict[str, Any]:
        """
        Get list of labels defined in a repository.
        
        Args:
            repo: Repository name (owner/repo)
            
        Returns:
            Dict with list of labels
        """
        args = ["api", f"repos/{repo}/labels", "--paginate"]
        result = self._run_command(args, capture_json=True)
        return result
    
    def add_pr_assignees(self, repo: str, pr_number: int, 
                         assignees: List[str]) -> Dict[str, Any]:
        """
        Add assignees to a pull request.
        Uses the Issues API since PRs are issues in GitHub's API.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            assignees: List of usernames to assign
            
        Returns:
            Dict with result
        """
        import json
        # Use the Issues API to add assignees (PRs are issues)
        payload = json.dumps({"assignees": assignees})
        args = ["api", f"repos/{repo}/issues/{pr_number}", 
                "-X", "PATCH",
                "--input", "-"]
        
        result = self._run_command(args, capture_json=True, input_data=payload)
        return result
    
    def add_pr_labels(self, repo: str, pr_number: int, 
                      labels: List[str]) -> Dict[str, Any]:
        """
        Add labels to a pull request.
        Uses the Issues API since PRs are issues in GitHub's API.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            labels: List of label names to add
            
        Returns:
            Dict with result
        """
        import json
        # Use the Issues API to add labels (PRs are issues)
        payload = json.dumps({"labels": labels})
        args = ["api", f"repos/{repo}/issues/{pr_number}/labels",
                "-X", "POST",
                "--input", "-"]
        
        result = self._run_command(args, capture_json=True, input_data=payload)
        return result
    
    def remove_pr_assignees(self, repo: str, pr_number: int, 
                            assignees: List[str]) -> Dict[str, Any]:
        """
        Remove assignees from a pull request.
        Uses the Issues API since PRs are issues in GitHub's API.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            assignees: List of usernames to remove
            
        Returns:
            Dict with result
        """
        import json
        # Use the Issues API to remove assignees (PRs are issues)
        payload = json.dumps({"assignees": assignees})
        args = ["api", f"repos/{repo}/issues/{pr_number}/assignees",
                "-X", "DELETE",
                "--input", "-"]
        
        result = self._run_command(args, capture_json=True, input_data=payload)
        return result
    
    def remove_pr_labels(self, repo: str, pr_number: int, 
                         labels: List[str]) -> Dict[str, Any]:
        """
        Remove labels from a pull request.
        Uses the Issues API since PRs are issues in GitHub's API.
        
        Args:
            repo: Repository name (owner/repo)
            pr_number: Pull request number
            labels: List of label names to remove
            
        Returns:
            Dict with result
        """
        # Use the Issues API to remove labels (PRs are issues)
        # Remove labels one by one
        for label in labels:
            args = ["api", f"repos/{repo}/issues/{pr_number}/labels/{label}",
                    "-X", "DELETE"]
            result = self._run_command(args, capture_json=True)
            if not result["success"]:
                return result
        
        return {"success": True, "output": "Labels removed"}

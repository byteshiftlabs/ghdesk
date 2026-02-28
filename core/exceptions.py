"""
Custom exception classes for ghdesk.
Provides a clear exception hierarchy for domain-specific errors.
"""


class GHDeskError(Exception):
    """Base exception for all ghdesk errors.
    
    All custom exceptions should inherit from this class.
    Provides user-friendly message support separate from technical details.
    """
    
    def __init__(self, message: str, user_message: str = None):
        """
        Args:
            message: Technical error message for logging
            user_message: User-friendly message for display (defaults to message)
        """
        super().__init__(message)
        self.user_message = user_message or message


# ============ GitHub CLI Errors ============

class GitHubCLIError(GHDeskError):
    """Base class for GitHub CLI related errors."""
    pass


class GitHubNotInstalledError(GitHubCLIError):
    """Raised when gh CLI is not installed or not in PATH."""
    
    def __init__(self):
        super().__init__(
            "GitHub CLI (gh) is not installed or not in PATH",
            "GitHub CLI is not installed. Please install it from https://cli.github.com/"
        )


class GitHubAuthError(GitHubCLIError):
    """Raised when GitHub authentication fails or is not configured."""
    
    def __init__(self, message: str = None):
        super().__init__(
            message or "GitHub authentication failed",
            "Please authenticate with GitHub using 'gh auth login'"
        )


class GitHubAPIError(GitHubCLIError):
    """Raised when a GitHub API call fails."""
    
    def __init__(self, operation: str, error: str):
        super().__init__(
            f"GitHub API error during {operation}: {error}",
            f"Failed to {operation}. Please try again."
        )


# ============ Git Errors ============

class GitError(GHDeskError):
    """Base class for Git operation errors."""
    pass


class GitNotRepositoryError(GitError):
    """Raised when a directory is not a Git repository."""
    
    def __init__(self, path: str):
        super().__init__(
            f"Not a git repository: {path}",
            "This directory is not a Git repository."
        )


class GitCommandError(GitError):
    """Raised when a git command fails."""
    
    def __init__(self, command: str, error: str):
        super().__init__(
            f"Git command '{command}' failed: {error}",
            f"Git operation failed: {error}"
        )


class GitTagError(GitError):
    """Raised when tag operations fail."""
    
    def __init__(self, operation: str, tag_name: str, error: str):
        super().__init__(
            f"Tag {operation} failed for '{tag_name}': {error}",
            f"Failed to {operation} tag '{tag_name}'"
        )


class GitPushError(GitError):
    """Raised when push operations fail."""
    
    def __init__(self, error: str):
        super().__init__(
            f"Push failed: {error}",
            "Failed to push changes to remote. Check your connection and permissions."
        )


# ============ Repository Errors ============

class RepositoryError(GHDeskError):
    """Base class for repository-related errors."""
    pass


class RepositoryNotFoundError(RepositoryError):
    """Raised when a repository cannot be found."""
    
    def __init__(self, identifier: str):
        super().__init__(
            f"Repository not found: {identifier}",
            f"Could not find repository '{identifier}'"
        )


class RepositoryScanError(RepositoryError):
    """Raised when scanning for repositories fails."""
    
    def __init__(self, path: str, error: str):
        super().__init__(
            f"Failed to scan directory '{path}': {error}",
            f"Failed to scan for repositories in {path}"
        )


# ============ Configuration Errors ============

class ConfigurationError(GHDeskError):
    """Raised when there's a configuration issue."""
    
    def __init__(self, message: str, user_message: str = None):
        super().__init__(
            message,
            user_message or "Configuration error. Please check your settings."
        )


# ============ Validation Errors ============

class ValidationError(GHDeskError):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, message: str):
        super().__init__(
            f"Validation error for '{field}': {message}",
            message
        )


# ============ Error Message Mapping ============

def get_user_message(error: Exception) -> str:
    """Get a user-friendly message for any exception.
    
    Args:
        error: The exception to get a message for
        
    Returns:
        User-friendly error message
    """
    if isinstance(error, GHDeskError):
        return error.user_message
    
    # Map common exceptions to user-friendly messages
    error_str = str(error).lower()
    
    if "permission denied" in error_str:
        return "Permission denied. Check file or repository permissions."
    if "connection" in error_str or "network" in error_str:
        return "Network error. Please check your internet connection."
    if "not found" in error_str:
        return "The requested resource was not found."
    if "timeout" in error_str:
        return "Operation timed out. Please try again."
    
    # Generic fallback
    return "An unexpected error occurred. Please try again."

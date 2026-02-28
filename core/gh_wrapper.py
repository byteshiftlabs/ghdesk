"""
GitHub CLI (gh) wrapper
Backward compatibility module - re-exports from core.github

For new code, import directly from core.github:
    from core.github import GHWrapper
"""

from core.github import GHWrapper

__all__ = ["GHWrapper"]

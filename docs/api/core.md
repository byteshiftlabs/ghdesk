# Core Modules

API reference for the core business logic layer.

---

## GitHub CLI Wrapper

The `GHWrapper` class provides a unified interface to GitHub CLI operations.

### GHWrapper

::: core.github.GHWrapper
    options:
      show_source: false
      members:
        - is_authenticated
        - login
        - logout
        - get_username
        - list_repos
        - get_repo
        - create_repo
        - delete_repo
        - edit_repo
        - clone_repo
        - get_topics
        - add_topic
        - remove_topic

---

## Base Operations

### GHBase

::: core.github.base.GHBase
    options:
      show_source: true

---

## Authentication

### AuthMixin

::: core.github.auth.AuthMixin
    options:
      show_source: true

---

## Repository Operations

### ReposMixin

::: core.github.repos.ReposMixin
    options:
      show_source: true
      members:
        - list_repos
        - get_repo
        - create_repo
        - delete_repo
        - edit_repo
        - clone_repo
        - get_topics
        - add_topic
        - remove_topic

---

## Git Operations

Local git repository operations using GitPython.

### GitRepository

::: core.git_operations.GitRepository
    options:
      show_source: true
      members:
        - name
        - current_branch
        - is_dirty
        - is_detached
        - branches
        - remote_branches
        - get_modified_files
        - get_staged_files
        - get_untracked_files
        - get_status_summary
        - get_recent_commits
        - get_all_branches_with_commits
        - get_remotes
        - get_remote_url
        - stage_files
        - commit
        - push
        - get_diff
        - get_staged_diff
        - close

### Helper Functions

::: core.git_operations.load_repo_details
    options:
      show_source: true

::: core.git_operations.extract_github_repo_name
    options:
      show_source: true

::: core.git_operations.open_repository
    options:
      show_source: true

---

## Repository Manager

Local filesystem repository discovery.

### RepoManager

::: core.repo_manager.RepoManager
    options:
      show_source: true

---

## Logging

Centralized logging configuration.

### Functions

::: core.logging_config.setup_logging
    options:
      show_source: true

::: core.logging_config.get_logger
    options:
      show_source: true

::: core.logging_config.get_log_dir
    options:
      show_source: true

---

## Licenses

License templates for repository creation.

### Constants

- `LICENSES` — Dict mapping license IDs to license data
- `LICENSE_ORDER` — List of license IDs in display order

### Functions

::: core.licenses.get_license_by_id
    options:
      show_source: true

::: core.licenses.get_license_list
    options:
      show_source: true

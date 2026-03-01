# Repository Management

This guide covers creating, cloning, and managing repositories with ghdesk.

---

## Creating Repositories

ghdesk provides a visual dialog for creating new repositories.

### Creating a New Repository

1. Click **Create** in the toolbar
2. Fill in the repository details:

| Field | Description |
|-------|-------------|
| **Repository Name** | Unique name for your repository (required) |
| **Description** | Brief description of the repository (optional) |
| **Visibility** | Public or Private |
| **License** | Select a license template (MIT, GPL, Apache, etc.) |
| **README** | Initialize with a README file |
| **.gitignore** | Add a .gitignore template for your language |

3. Click **Create** to create the repository on GitHub

!!! tip "Local Repository Creation"
    If you specify a local path, ghdesk will also clone the repository to that location after creation.

---

## Cloning Repositories

### From the Repository List

1. Select a repository from the list
2. Right-click and select **Clone**
3. Choose the destination folder
4. The repository is cloned and appears in your file tree

### Clone Options

When cloning, ghdesk uses the default `gh repo clone` behavior:

- Clones via HTTPS or SSH based on your `gh` configuration
- Sets up remote tracking automatically

---

## Repository Visibility

### Changing Visibility

1. Select a repository
2. Right-click and select **Change Visibility**
3. Choose **Public** or **Private**
4. Confirm the change

!!! warning "Public to Private"
    Making a repository private may affect collaborators and integrations.

---

## Deleting Repositories

### Delete a Repository

1. Select the repository to delete
2. Right-click and select **Delete**
3. Confirm by typing the repository name
4. The repository is permanently deleted from GitHub

!!! danger "Irreversible Action"
    Deleting a repository is permanent. All issues, pull requests, and data are lost.

---

## Local Repository Discovery

### Browsing Local Repositories

The file tree on the left panel allows you to browse your local filesystem:

1. Navigate to folders containing Git repositories
2. Repositories are indicated with a Git icon
3. Click a repository to view its details

### What ghdesk Detects

ghdesk identifies Git repositories by looking for:

- `.git` directory
- Valid Git configuration

It then displays:

- Current branch
- Repository status (clean, modified, ahead/behind)
- Local and remote information

---

## Repository Details

### Overview Tab

Displays combined local and remote repository information:

**Local Repository:**

- Name
- Path
- Current branch
- Status

**GitHub Repository:**

- Full name (owner/repo)
- Visibility
- Description
- Stars, forks, open issues
- Clone URL

### Status Tab

Shows the current working tree status:

- **Modified Files** — Changed files not yet staged
- **Staged Files** — Files staged for commit
- **Untracked Files** — New files not tracked by Git

### Activity Tab

Displays recent commit activity organized by branch:

- Branch name
- Recent commits with messages and dates
- Current branch highlighted

### Topics Tab

Manage GitHub repository topics (keywords):

- View current topics
- Add new topics
- Remove existing topics

### Pull Requests Tab

View and manage pull requests for GitHub repositories:

**PR List View:**

- Filter PRs by state: All, Open, Closed, Merged
- See PR number, title, author, and state at a glance
- Click any PR to view details

**PR Detail View:**

- **Header** — PR number, title, and current state badge
- **Metadata** — Author, creation date, source/target branches
- **Statistics** — Commits, files changed, additions/deletions
- **Description** — Full PR body with markdown rendering
- **Comments** — View and add comments to the discussion

**Actions:**

- **Merge** — Merge the PR (requires appropriate permissions)
- **Close** — Close the PR without merging
- **Reopen** — Reopen a previously closed PR
- **Comment** — Add a comment to the PR discussion
- **Request Review** — Request a review from a GitHub user

**Diff Viewing:**

- **Unified Diff** — Traditional diff format with additions and deletions
- **Side-by-Side** — Compare old and new versions in parallel panels
    - File list on the left for quick navigation
    - Synced scrolling between left and right panels
    - Color-coded additions (green) and removals (red)

### Remotes Tab

View configured Git remotes:

- Remote name
- Remote URL

---

## Next Steps

- [Themes and Customization](themes.md) — Change the application appearance

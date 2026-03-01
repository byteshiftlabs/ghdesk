# Getting Started

This guide walks you through installing and configuring ghdesk for first-time use.

---

## Prerequisites

Before installing ghdesk, ensure you have the following:

### Required

- **Python 3.8 or higher** — ghdesk is built with Python
- **GitHub CLI (`gh`)** — The underlying tool that ghdesk wraps

### Installing GitHub CLI

```bash
sudo apt install gh
```

After installation, verify:
```bash
gh --version
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/cmelnulabs/ghdesk.git
cd ghdesk
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Authentication

ghdesk requires GitHub authentication to access your repositories.

### First-Time Authentication

1. Launch ghdesk: `python main.py`
2. Click the **Login** button in the toolbar
3. Follow the browser prompts to authenticate with GitHub
4. Once authenticated, the status indicator turns green

Alternatively, authenticate via terminal before launching:
```bash
gh auth login
```

### Verifying Authentication

The toolbar displays your authentication status:

- **Green indicator** — Authenticated successfully
- **Red indicator** — Not authenticated or session expired

---

## Launching ghdesk

### Standard Launch

```bash
cd /path/to/ghdesk
source venv/bin/activate
python main.py
```

### Using the Launch Script

On Linux, use the provided script that handles Wayland/X11 compatibility:

```bash
./run.sh
```

---

## Interface Overview

The main window consists of three panels:

| File Tree | Repository List | Repository Details |
|-----------|-----------------|--------------------|
| Browse local filesystem | View GitHub repos | View selected repo info |
| Navigate folders | My Repos / Starred tabs | Overview, Status, Activity, Topics, Remotes |

### File Tree (Left Panel)

Browse your local filesystem to discover Git repositories. Click a folder to navigate, and select a repository to view its details.

### Repository List (Center Panel)

View your GitHub repositories. Use the tabs to switch between:

- **My Repos** — Your personal repositories
- **Starred** — Repositories you've starred

### Repository Details (Right Panel)

Displays detailed information about the selected repository:

- **Overview** — Local and remote repository info
- **Status** — Modified, staged, and untracked files
- **Activity** — Recent commits by branch
- **Topics** — GitHub repository topics/keywords
- **Remotes** — Configured Git remotes

---

## Next Steps

- [Repository Management](repository-management.md) — Create, clone, and manage repositories
- [Themes and Customization](themes.md) — Change the application appearance

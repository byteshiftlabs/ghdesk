# ghdesk

A powerful GUI wrapper for GitHub CLI (`gh`) with enhanced repository management capabilities.

## Features

- 🗂️ **Filesystem Navigation** - Browse and discover local Git repositories
- 🆕 **Repository Creation** - Create repos locally and push to GitHub
- 🔐 **Authentication** - Login/logout from GitHub account
- 🔧 **Full gh Operations** - All `gh` CLI capabilities with a visual interface
- 📊 **Repository Dashboard** - View repo status, branches, PRs, issues
- ⚙️ **Settings Management** - Change visibility, description, topics, etc.
- 🗑️ **Repository Management** - Delete, archive, transfer repositories

## Installation

```bash
# Clone the repository
git clone https://github.com/cmelnulabs/ghdesk.git
cd ghdesk

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## Requirements

- Python >= 3.8
- GitHub CLI (`gh`) installed and in PATH
- PyQt6 (6.6.1)
- GitPython (3.1.46)

See `requirements.txt` for exact pinned versions.

## Usage

1. Launch ghdesk: `python main.py`
2. Login to GitHub via the toolbar or settings
3. Browse your local repositories or search GitHub
4. Create, manage, and delete repositories with visual controls

## Architecture

```
ghdesk/
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies (pinned versions)
├── pytest.ini               # Test configuration
├── .pylintrc                # Linting configuration
├── core/                    # Core functionality
│   ├── gh_wrapper.py        # GitHub CLI wrapper (compatibility)
│   ├── git_operations.py    # Local Git operations
│   ├── licenses.py          # License templates
│   ├── logging_config.py    # Centralized logging
│   ├── repo_manager.py      # Local repository management
│   └── github/              # GitHub API modules
│       ├── __init__.py      # GHWrapper class
│       ├── auth.py          # Authentication handling
│       ├── base.py          # Base CLI wrapper
│       ├── issues.py        # Issue operations
│       ├── pull_requests.py # PR operations
│       ├── repos.py         # Repository operations
│       └── tags.py          # Tag/release operations
├── ui/                      # UI components
│   ├── main_window.py       # Main application window
│   ├── repo_view.py         # Repository list view
│   ├── repo_detail_view.py  # Repository details panel
│   ├── create_dialog.py     # Create repository dialog
│   ├── pr_create_dialog.py  # Create pull request dialog
│   ├── commit_push_dialog.py# Commit and push dialog
│   ├── license_dialog.py    # License selector dialog
│   ├── tag_dialog.py        # Tag/release dialog
│   ├── diff_viewer.py       # Diff syntax highlighter
│   ├── dialogs.py           # Common dialog utilities
│   ├── file_tree.py         # File tree widget
│   ├── flow_layout.py       # Horizontal flow layout
│   ├── topic_manager.py     # Topic management mixin
│   ├── constants.py         # UI constants
│   ├── styles.py            # Component styles
│   └── themes/              # Theme stylesheets
│       ├── __init__.py      # Theme loader
│       ├── dark.py          # Dark theme
│       ├── light.py         # Light theme
│       ├── nord.py          # Nord theme
│       ├── dracula.py       # Dracula theme
│       └── monokai.py       # Monokai theme
└── tests/                   # Test suite
    ├── test_git_operations.py
    └── test_logging_config.py
```

## License

MIT License - see [LICENSE](LICENSE) for details.

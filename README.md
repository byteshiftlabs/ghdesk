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
- PyQt6

## Usage

1. Launch ghdesk: `python main.py`
2. Login to GitHub via the toolbar or settings
3. Browse your local repositories or search GitHub
4. Create, manage, and delete repositories with visual controls

## Architecture

```
ghdesk/
├── main.py              # Application entry point
├── ui/                  # UI components
│   ├── main_window.py   # Main application window
│   ├── repo_view.py     # Repository list/details view
│   ├── create_dialog.py # Create repository dialog
│   └── settings.py      # Settings panel
├── core/                # Core functionality
│   ├── gh_wrapper.py    # GitHub CLI wrapper
│   ├── repo_manager.py  # Local repository management
│   └── auth.py          # Authentication handling
└── utils/               # Utilities
    └── scanner.py       # Filesystem scanning
```

## License

MIT License - see [LICENSE](LICENSE) for details.

# ghdesk

A powerful GUI wrapper for GitHub CLI (`gh`) with enhanced repository management capabilities.

---

## Overview

ghdesk provides a visual interface for managing GitHub repositories, combining the power of the GitHub CLI with an intuitive desktop application. It bridges the gap between command-line efficiency and visual accessibility.

### Key Features

- **Filesystem Navigation** — Browse and discover local Git repositories
- **Repository Creation** — Create repos locally and push to GitHub
- **Authentication** — Login/logout from GitHub account
- **Full gh Operations** — All `gh` CLI capabilities with a visual interface
- **Repository Dashboard** — View repo status, branches, PRs, issues
- **Settings Management** — Change visibility, description, topics
- **Multiple Themes** — Dark, Light, Nord, Dracula, Monokai

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/cmelnulabs/ghdesk.git
cd ghdesk

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

!!! note "Prerequisites"
    - Python >= 3.8
    - GitHub CLI (`gh`) installed and authenticated
    - PyQt6 (6.6.1)
    - GitPython (3.1.46)

---

## Documentation Structure

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **User Guide**

    ---

    Learn how to use ghdesk for day-to-day repository management.

    [:octicons-arrow-right-24: Getting Started](user-guide/getting-started.md)

-   :material-code-braces:{ .lg .middle } **Development**

    ---

    Architecture, contributing guidelines, and code style.

    [:octicons-arrow-right-24: Architecture](development/architecture.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Auto-generated documentation from source code docstrings.

    [:octicons-arrow-right-24: Core Modules](api/core.md)

</div>

---

## License

ghdesk is released under the [MIT License](https://opensource.org/licenses/MIT).

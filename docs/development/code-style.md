# Code Style

ghdesk follows consistent code style guidelines to maintain readability and quality.

---

## Python Style

### PEP 8 Compliance

Follow [PEP 8](https://peps.python.org/pep-0008/) with these specifics:

- **Line length**: 100 characters (relaxed from 79)
- **Indentation**: 4 spaces (no tabs)
- **Blank lines**: 2 between top-level definitions, 1 within classes

### Import Organization

Imports at the top of each file, organized in groups:

```python
# 1. Standard library
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 2. Third-party packages
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
import git

# 3. Local imports
from core.gh_wrapper import GHWrapper
from core.git_operations import GitRepository
from ui.constants import WINDOW_WIDTH
```

**Rules:**

- Alphabetical order within each group
- One blank line between groups
- Prefer `from x import y` over `import x` when using few items
- Never use `from x import *`

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `MainWindow`, `GitRepository` |
| Functions/Methods | snake_case | `load_repo_details`, `get_modified_files` |
| Variables | snake_case | `repo_path`, `is_authenticated` |
| Constants | UPPER_SNAKE | `WINDOW_WIDTH`, `MARGIN_MEDIUM` |
| Private | Leading underscore | `_run_command`, `_repo` |

### Type Hints

Use type hints for public APIs:

```python
def load_repo_details(repo_path: str, gh: GHWrapper) -> Dict[str, Any]:
    """Load repository details."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def get_repo(self, repo_full_name: str) -> Dict[str, Any]:
    """
    Get repository information from GitHub.

    Args:
        repo_full_name: Repository in "owner/repo" format

    Returns:
        Dict containing repository metadata or error info

    Raises:
        ValueError: If repo_full_name is invalid format
    """
```

---

## Constants and Magic Numbers

### No Magic Numbers

Bad:
```python
self.setGeometry(100, 100, 1200, 800)  # What are these?
```

Good:
```python
from ui.constants import WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT
self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
```

### Centralized Constants

All constants go in `ui/constants.py`:

```python
# ui/constants.py

# Application
APP_NAME = "ghdesk"
APP_TITLE = "ghdesk - GitHub Desktop"

# Window dimensions
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Margins and spacing
MARGIN_NONE = 0
MARGIN_SMALL = 5
MARGIN_MEDIUM = 10
```

---

## PyQt6 Specific

### Signal/Slot Naming

- Signals: noun or past tense verb (`details_loaded`, `result`)
- Slots: verb or `on_` prefix (`load_repo`, `on_details_loaded`)

### Widget Creation Pattern

```python
def init_ui(self):
    """Initialize the user interface"""
    layout = QVBoxLayout()
    layout.setContentsMargins(MARGIN_NONE, MARGIN_NONE, MARGIN_NONE, MARGIN_NONE)
    self.setLayout(layout)

    # Create widgets
    self.header = QLabel("Title")
    self.header.setStyleSheet(STYLE_HEADER_LARGE)
    layout.addWidget(self.header)
```

### Stylesheet Strings

Keep styles in `ui/styles.py`:

```python
# ui/styles.py

STYLE_HEADER_LARGE = """
    font-size: 18px;
    font-weight: bold;
    padding: 10px;
"""

STYLE_CLOSE_BUTTON = """
    QPushButton {
        border: none;
        background: transparent;
    }
    QPushButton:hover {
        background: rgba(255, 255, 255, 0.1);
    }
"""
```

---

## Module Size

### 500 Line Limit

Keep modules under 500 lines. If a module grows too large:

1. Identify cohesive groups of functionality
2. Extract into mixins or separate modules
3. Use composition over inheritance when possible

**Example**: `RepoDetailView` was split into:

- `repo_detail_view.py` — Main widget and logic
- `tab_builder.py` — Tab creation methods (mixin)
- `topic_manager.py` — Topic management (mixin)

---

## Linting

### Pylint Configuration

ghdesk uses a custom `.pylintrc`:

```ini
[MAIN]
extension-pkg-allow-list=PyQt6

[MESSAGES CONTROL]
disable=
    R0902,  # too-many-instance-attributes
    R0915,  # too-many-statements
```

### Running Pylint

```bash
python -m pylint **/*.py
```

**Minimum score**: 9.0/10

### Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| `W0611: Unused import` | Remove the import |
| `C0301: Line too long` | Break into multiple lines |
| `W0612: Unused variable` | Remove or use `_` prefix |
| `R0913: Too many arguments` | Consider a config object |

---

## Pre-Commit Checklist

Before committing:

- [ ] `pytest tests/ -v -W default` passes with zero warnings
- [ ] `pylint **/*.py` scores ≥ 9.0
- [ ] No unused imports
- [ ] No magic numbers
- [ ] Docstrings for public APIs
- [ ] Type hints where practical

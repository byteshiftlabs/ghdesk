# UI Components

API reference for the user interface layer.

---

## Main Window

### MainWindow

::: ui.main_window.MainWindow
    options:
      show_source: false
      members:
        - __init__
        - init_ui
        - create_toolbar
        - check_authentication

---

## Repository Views

### RepoView

::: ui.repo_view.RepoView
    options:
      show_source: false
      members:
        - __init__
        - load_repos
        - refresh
        - refresh_current_tab

### RepoDetailView

::: ui.repo_detail_view.RepoDetailView
    options:
      show_source: false
      members:
        - __init__
        - load_repo
        - load_github_repo

---

## Dialogs

### CreateRepoDialog

::: ui.create_dialog.CreateRepoDialog
    options:
      show_source: false

### CommitPushDialog

::: ui.commit_push_dialog.CommitPushDialog
    options:
      show_source: false

### CreatePRDialog

::: ui.pr_create_dialog.CreatePRDialog
    options:
      show_source: false

### CreateTagDialog

::: ui.tag_dialog.CreateTagDialog
    options:
      show_source: false

### LicenseDialog

::: ui.license_dialog.LicenseDialog
    options:
      show_source: false

---

## Widgets

### FileTreeWidget

::: ui.file_tree.FileTreeWidget
    options:
      show_source: false

### FlowLayout

::: ui.flow_layout.FlowLayout
    options:
      show_source: false

### DiffHighlighter

::: ui.diff_viewer.DiffHighlighter
    options:
      show_source: false

---

## Mixins

### TopicManagerMixin

::: ui.topic_manager.TopicManagerMixin
    options:
      show_source: false

### TabBuilderMixin

::: ui.tab_builder.TabBuilderMixin
    options:
      show_source: false

---

## Themes

### Theme Functions

::: ui.themes.get_theme
    options:
      show_source: true

### Available Themes

```python
from ui.themes import THEMES

# THEMES = {
#     "dark": "Dark",
#     "light": "Light", 
#     "nord": "Nord",
#     "dracula": "Dracula",
#     "monokai": "Monokai"
# }
```

---

## Constants

### Application

| Constant | Value | Description |
|----------|-------|-------------|
| `APP_NAME` | `"ghdesk"` | Application identifier |
| `APP_TITLE` | `"ghdesk - GitHub Desktop"` | Window title |
| `ORGANIZATION_NAME` | `"cmelnulabs"` | Organization identifier |

### Window Dimensions

| Constant | Value | Description |
|----------|-------|-------------|
| `WINDOW_X` | `100` | Initial X position |
| `WINDOW_Y` | `100` | Initial Y position |
| `WINDOW_WIDTH` | `1200` | Window width |
| `WINDOW_HEIGHT` | `800` | Window height |

### Margins and Spacing

| Constant | Value | Description |
|----------|-------|-------------|
| `MARGIN_NONE` | `0` | No margin |
| `MARGIN_SMALL` | `5` | Small margin |
| `MARGIN_MEDIUM` | `10` | Medium margin |
| `SPACING_MEDIUM` | `10` | Medium spacing |
| `SPACING_LARGE` | `15` | Large spacing |

---

## Styles

Style strings are defined in `ui/styles.py`:

| Constant | Purpose |
|----------|---------|
| `STYLE_HEADER_LARGE` | Large header text |
| `STYLE_CLOSE_BUTTON` | Close/hide buttons |
| `STYLE_EMPTY_STATE` | Empty state messages |
| `STYLE_BRANCH_CURRENT` | Current branch highlight |
| `STYLE_BRANCH_OTHER` | Other branch styling |
| `STYLE_AUTH_SUCCESS` | Authenticated indicator |
| `STYLE_AUTH_FAILED` | Not authenticated indicator |

---

## Signals

### MainWindow Signals

| Signal | Emitted When |
|--------|--------------|
| (none) | MainWindow uses slots, not signals |

### RepoDetailView Signals

| Signal | Emitted When |
|--------|--------------|
| `hide_requested` | User clicks hide button |

### RepoView Signals

| Signal | Parameters | Emitted When |
|--------|------------|--------------|
| `repo_selected` | `repo_full_name: str` | User selects a repo |

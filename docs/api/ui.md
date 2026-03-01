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

### PRListView

::: ui.pr_list_view.PRListView
    options:
      show_source: false
      members:
        - __init__
        - set_prs
        - filter_prs
        - get_selected_pr

### PRDetailView

::: ui.pr_detail_view.PRDetailView
    options:
      show_source: false
      members:
        - __init__
        - show_pr
        - clear

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

### DiffViewerDialog

::: ui.diff_viewer.DiffViewerDialog
    options:
      show_source: false
      members:
        - __init__
        - set_diff

### SideBySideDiffDialog

::: ui.diff_viewer.SideBySideDiffDialog
    options:
      show_source: false
      members:
        - __init__
        - set_diff

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

### SideBySideHighlighter

::: ui.diff_viewer.SideBySideHighlighter
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

### PullRequestsMixin

::: ui.pull_requests.PullRequestsMixin
    options:
      show_source: false
      members:
        - list_prs
        - view_pr
        - get_pr_diff
        - merge_pr
        - close_pr
        - reopen_pr
        - add_pr_comment
        - request_pr_review
        - get_pr_checks

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

### Diff Dialog Dimensions

| Constant | Value | Description |
|----------|-------|-------------|
| `DIFF_DIALOG_MIN_WIDTH` | `800` | Minimum width for unified diff dialog |
| `DIFF_DIALOG_MIN_HEIGHT` | `600` | Minimum height for unified diff dialog |
| `SBS_DIFF_DIALOG_MIN_WIDTH` | `1200` | Minimum width for side-by-side diff dialog |
| `SBS_DIFF_DIALOG_MIN_HEIGHT` | `700` | Minimum height for side-by-side diff dialog |
| `SBS_DIFF_FILE_LIST_WIDTH` | `200` | Width of file list panel |
| `SBS_DIFF_CONTENT_WIDTH` | `1000` | Width of diff content panels |

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
| `STYLE_DIFF_HEADER_OLD` | Old file header in side-by-side diff |
| `STYLE_DIFF_HEADER_NEW` | New file header in side-by-side diff |
| `STYLE_DIFF_FILE_LABEL` | File name label styling |

### Diff Colors

| Constant | Purpose |
|----------|---------|
| `COLOR_DIFF_ADDED_FG` | Foreground for added lines |
| `COLOR_DIFF_ADDED_BG` | Background for added lines |
| `COLOR_DIFF_REMOVED_FG` | Foreground for removed lines |
| `COLOR_DIFF_REMOVED_BG` | Background for removed lines |
| `COLOR_DIFF_HUNK_FG` | Hunk header foreground |
| `COLOR_DIFF_HEADER_FG` | Diff header foreground |
| `COLOR_DIFF_META_FG` | Meta line foreground |
| `COLOR_SBS_ADDED_BG` | Side-by-side added background |
| `COLOR_SBS_REMOVED_BG` | Side-by-side removed background |
| `COLOR_SBS_CONTEXT_BG` | Side-by-side context background |
| `COLOR_SBS_EMPTY_BG` | Side-by-side empty line background |

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

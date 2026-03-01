"""
UI Constants for ghdesk
Centralized configuration for layout dimensions and settings
"""

# Application metadata
APP_NAME = "ghdesk"
APP_TITLE = "ghdesk - GitHub Desktop Manager"
ORGANIZATION_NAME = "byteshiftlabs"

# Main window geometry
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

# Splitter panel sizes (pixels)
SPLITTER_FILE_TREE_WIDTH = 220
SPLITTER_TABS_WIDTH = 500
SPLITTER_DETAILS_WIDTH = 480

# Repository table column widths
COLUMN_WIDTH_NAME = 180
COLUMN_WIDTH_OWNER = 120
COLUMN_WIDTH_PATH = 120
COLUMN_WIDTH_DESCRIPTION = 150
COLUMN_WIDTH_BRANCH = 150
COLUMN_WIDTH_STATUS = 100
COLUMN_WIDTH_VISIBILITY = 100
COLUMN_WIDTH_LICENSE = 120
COLUMN_WIDTH_UPDATED = 100
COLUMN_WIDTH_REMOTE = 200

# =============================================================================
# Layout Constants
# =============================================================================

# Margins and spacing
MARGIN_NONE = 0
MARGIN_SMALL = 4
MARGIN_MEDIUM = 8
MARGIN_LARGE = 12
MARGIN_XLARGE = 16

SPACING_NONE = 0
SPACING_SMALL = 4
SPACING_MEDIUM = 8
SPACING_LARGE = 12
SPACING_XLARGE = 16

# Button sizes
BUTTON_MIN_WIDTH_SMALL = 70
BUTTON_MIN_WIDTH_MEDIUM = 80
BUTTON_MIN_WIDTH_LARGE = 100
BUTTON_ICON_SIZE = 24

# Input/list heights
INPUT_MAX_HEIGHT = 100
LIST_MAX_HEIGHT_SMALL = 100
LIST_MAX_HEIGHT_MEDIUM = 150
LIST_MAX_HEIGHT_LARGE = 300

# Scroll area dimensions
SCROLL_MIN_HEIGHT = 100
SCROLL_MAX_HEIGHT = 300

# Theme combo width
THEME_COMBO_MIN_WIDTH = 120

# Message box width
MESSAGE_BOX_MIN_WIDTH = 400

# =============================================================================
# Dialog Dimensions
# =============================================================================

# License dialog
LICENSE_DIALOG_WIDTH = 800
LICENSE_DIALOG_HEIGHT = 550
LICENSE_SPLITTER_LEFT = 250
LICENSE_SPLITTER_RIGHT = 550
LICENSE_LIST_MIN_WIDTH = 200

# Tag dialog
TAG_DIALOG_WIDTH = 500
TAG_DIALOG_HEIGHT = 350

# Create repo dialog
CREATE_DIALOG_WIDTH = 500
CREATE_DIALOG_HEIGHT = 400

# Commit/Push dialog (already defined elsewhere, kept for compatibility)
COMMIT_PUSH_DIALOG_WIDTH = 900
COMMIT_PUSH_DIALOG_HEIGHT = 700
COMMIT_PUSH_SPLITTER_LEFT = 300
COMMIT_PUSH_SPLITTER_RIGHT = 600

# PR Create dialog (already defined elsewhere, kept for compatibility)
PR_CREATE_DIALOG_WIDTH = 600
PR_CREATE_DIALOG_HEIGHT = 650
PR_CREATE_BODY_MIN_HEIGHT = 150

# Diff viewer dialog
DIFF_DIALOG_MIN_WIDTH = 800
DIFF_DIALOG_MIN_HEIGHT = 600
SBS_DIFF_DIALOG_MIN_WIDTH = 1200
SBS_DIFF_DIALOG_MIN_HEIGHT = 700
SBS_DIFF_FILE_LIST_WIDTH = 200
SBS_DIFF_CONTENT_WIDTH = 1000

# =============================================================================
# Fonts
# =============================================================================

FONT_MONOSPACE = "Monospace"
FONT_SIZE_MONOSPACE = 9

# =============================================================================
# Table/List dimensions
# =============================================================================

COMMITS_TABLE_COLUMNS = 4
REMOTES_TABLE_COLUMNS = 2
HEADER_PADDING = 10

# Repository table columns
LOCAL_REPO_COLUMNS = 5   # Name, Path, Branch, Status, Remote
REMOTE_REPO_COLUMNS = 6  # Name, Owner, Description, Visibility, License, Updated

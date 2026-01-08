#!/bin/bash
# Launch ghdesk with optimal backend for dialog centering

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Detect if running on GNOME with Wayland
if [[ "$XDG_CURRENT_DESKTOP" == *"GNOME"* ]] && [[ -n "$WAYLAND_DISPLAY" || "$XDG_SESSION_TYPE" == "wayland" ]]; then
    echo "Detected GNOME on Wayland - using X11 backend for proper dialog centering"
    export QT_QPA_PLATFORM=xcb
else
    echo "Running with native backend"
fi

# Run the application
python main.py

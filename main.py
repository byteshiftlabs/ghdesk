#!/usr/bin/env python3
"""
ghdesk - GUI wrapper for GitHub CLI
Entry point for the application
"""

import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.main_window import MainWindow
from ui.themes import get_theme
from ui.constants import APP_NAME, ORGANIZATION_NAME


def main():
    """Main entry point"""
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORGANIZATION_NAME)
    
    # Apply default dark theme
    app.setStyleSheet(get_theme("dark"))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

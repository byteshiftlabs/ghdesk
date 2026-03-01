"""
Logging configuration for ghdesk.

Provides a centralized logging setup with both file and console handlers.
Logs are stored in the user's config directory alongside app settings.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


# Default log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log file location
def get_log_dir() -> Path:
    """Get the log directory, creating it if necessary."""
    config_dir = Path.home() / ".config" / "ghdesk"
    log_dir = config_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def setup_logging(
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True,
    max_files: int = 5
) -> logging.Logger:
    """
    Configure application-wide logging.

    Args:
        level: Logging level (default: INFO)
        log_to_file: Whether to log to a file (default: True)
        log_to_console: Whether to log to console (default: True)
        max_files: Maximum number of log files to keep (default: 5)

    Returns:
        The root logger for ghdesk
    """
    # Create root logger for ghdesk
    logger = logging.getLogger("ghdesk")
    logger.setLevel(level)

    # Close and remove any existing handlers
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_to_file:
        log_dir = get_log_dir()

        # Clean up old log files
        _cleanup_old_logs(log_dir, max_files)

        # Create new log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"ghdesk_{timestamp}.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info("Logging to file: %s", log_file)

    return logger


def _cleanup_old_logs(log_dir: Path, max_files: int) -> None:
    """Remove old log files, keeping only the most recent ones."""
    log_files = sorted(log_dir.glob("ghdesk_*.log"), key=lambda p: p.stat().st_mtime)

    # Remove oldest files if we have too many
    while len(log_files) >= max_files:
        oldest = log_files.pop(0)
        try:
            oldest.unlink()
        except OSError:
            pass  # Ignore errors when deleting old logs


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Module name (e.g., "gh", "git_operations", "ui.main_window")

    Returns:
        A logger instance with the specified name under ghdesk namespace
    """
    return logging.getLogger(f"ghdesk.{name}")

"""
Logging configuration for ghdesk.
Provides consistent logging across all modules.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Default format: timestamp, level, module, message
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log levels by environment
LOG_LEVEL_DEBUG = logging.DEBUG
LOG_LEVEL_DEFAULT = logging.INFO
LOG_LEVEL_QUIET = logging.WARNING


def setup_logging(
    level: int = LOG_LEVEL_DEFAULT,
    log_file: Optional[Path] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configure logging for ghdesk.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional path to log file
        console: Whether to output to console
        
    Returns:
        Root logger for ghdesk
    """
    # Get the root logger for ghdesk
    logger = logging.getLogger("ghdesk")
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Module name (will be prefixed with 'ghdesk.')
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"ghdesk.{name}")


# Convenience function for quick debug logging
def log_exception(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log an exception with full traceback at ERROR level.
    
    Args:
        logger: Logger instance
        error: The exception to log
        context: Optional context about what was happening
    """
    if context:
        logger.error(f"{context}: {error}", exc_info=True)
    else:
        logger.error(str(error), exc_info=True)

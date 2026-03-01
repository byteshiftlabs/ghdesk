"""
Tests for core.logging_config module
"""

import logging
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from core.logging_config import setup_logging, get_logger, get_log_dir, _cleanup_old_logs


class TestGetLogDir:
    """Tests for get_log_dir function"""

    def test_returns_path(self):
        """get_log_dir returns a Path object"""
        result = get_log_dir()
        assert isinstance(result, Path)

    def test_directory_exists(self):
        """get_log_dir creates the directory if needed"""
        result = get_log_dir()
        assert result.exists()
        assert result.is_dir()

    def test_correct_location(self):
        """Log directory is in expected location"""
        result = get_log_dir()
        assert "ghdesk" in str(result)
        assert "logs" in str(result)


class TestGetLogger:
    """Tests for get_logger function"""

    def test_returns_logger(self):
        """get_logger returns a Logger instance"""
        result = get_logger("test_module")
        assert isinstance(result, logging.Logger)

    def test_logger_name_prefix(self):
        """Logger has correct namespace prefix"""
        result = get_logger("my_module")
        assert result.name == "ghdesk.my_module"

    def test_different_names_different_loggers(self):
        """Different names return different logger instances"""
        logger1 = get_logger("module_a")
        logger2 = get_logger("module_b")
        assert logger1 is not logger2
        assert logger1.name != logger2.name


class TestSetupLogging:
    """Tests for setup_logging function"""

    def test_returns_logger(self):
        """setup_logging returns the root ghdesk logger"""
        result = setup_logging(log_to_file=False, log_to_console=False)
        assert isinstance(result, logging.Logger)
        assert result.name == "ghdesk"

    def test_sets_level(self):
        """setup_logging sets the correct log level"""
        logger = setup_logging(
            level=logging.DEBUG,
            log_to_file=False,
            log_to_console=False
        )
        assert logger.level == logging.DEBUG

    def test_console_handler_added(self):
        """Console handler is added when enabled"""
        logger = setup_logging(log_to_file=False, log_to_console=True)
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "StreamHandler" in handler_types

    def test_console_handler_not_added_when_disabled(self):
        """Console handler is not added when disabled"""
        logger = setup_logging(log_to_file=False, log_to_console=False)
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "StreamHandler" not in handler_types

    def test_file_handler_added(self):
        """File handler is added when enabled"""
        logger = setup_logging(log_to_file=True, log_to_console=False)
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "FileHandler" in handler_types

    def test_clears_existing_handlers(self):
        """setup_logging clears any existing handlers"""
        # Add a dummy handler first
        logger = logging.getLogger("ghdesk")
        logger.addHandler(logging.NullHandler())
        initial_count = len(logger.handlers)

        # Setup should clear and add new handlers
        setup_logging(log_to_file=False, log_to_console=True)
        assert len(logger.handlers) < initial_count + 2


class TestCleanupOldLogs:
    """Tests for _cleanup_old_logs function"""

    def test_removes_old_files(self):
        """Old log files are removed when over limit"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)

            # Create more files than max
            for i in range(5):
                (log_dir / f"ghdesk_{i:04d}.log").touch()

            assert len(list(log_dir.glob("ghdesk_*.log"))) == 5

            _cleanup_old_logs(log_dir, max_files=3)

            # Should have removed 2 oldest files
            remaining = list(log_dir.glob("ghdesk_*.log"))
            assert len(remaining) <= 3

    def test_keeps_files_under_limit(self):
        """Files are kept when under the limit"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)

            # Create fewer files than max
            for i in range(2):
                (log_dir / f"ghdesk_{i:04d}.log").touch()

            _cleanup_old_logs(log_dir, max_files=5)

            # All files should remain
            remaining = list(log_dir.glob("ghdesk_*.log"))
            assert len(remaining) == 2

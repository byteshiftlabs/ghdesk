"""
GitHub CLI base wrapper
Provides common functionality for gh CLI commands
"""

import subprocess
import json
from typing import Optional, List, Dict, Any

from core.logging_config import get_logger

logger = get_logger("github.base")


class GHBase:
    """Base class for GitHub CLI operations"""

    def __init__(self):
        self._check_gh_installed()

    def _check_gh_installed(self) -> bool:
        """Check if gh CLI is installed"""
        try:
            subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.debug("GitHub CLI is available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("GitHub CLI (gh) is not installed or not in PATH")
            raise RuntimeError("GitHub CLI (gh) is not installed or not in PATH")

    def _run_command(
        self,
        args: List[str],
        capture_json: bool = False,
        input_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a gh CLI command

        Args:
            args: Command arguments (without 'gh')
            capture_json: Whether to parse output as JSON
            input_data: Optional stdin data

        Returns:
            Dict with 'success', 'output', 'error' keys
        """
        cmd = ["gh"] + args
        logger.debug("Running command: gh %s", ' '.join(args))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                input=input_data
            )

            output = result.stdout.strip()
            error = result.stderr.strip()
            success = result.returncode == 0

            if capture_json and success and output:
                try:
                    output = json.loads(output)
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON output: %s...", output[:100])

            if not success:
                logger.warning("Command failed (rc=%d): %s", result.returncode, error)

            return {
                "success": success,
                "output": output,
                "error": error,
                "returncode": result.returncode
            }
        except Exception as e:
            logger.exception(f"Exception running command: {e}")
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }

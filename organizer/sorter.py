# organizer/sorter.py

from datetime import datetime
from pathlib import Path
from organizer.logger import setup_logger


class FileCategorizer:
    """Categorizes files based on different strategies."""

    def __init__(self, logger=None):
        self.logger = logger or setup_logger()

    def by_extension(self, file_path: Path) -> str:
        """Categorize file by its extension.

        Args:
            file_path (Path): The path to the file.

        Returns:
            str: The file extension (e.g., 'pdf', 'jpg'), or 'no_extension' if missing.
        """
        return file_path.suffix[1:].lower() if file_path.suffix else "no_extension"

    def by_modification_date(self, file_path: Path) -> str:
        """Categorize file by its last modified date, formatted as 'YYYY-MM'.

        Args:
            file_path (Path): The path to the file.

        Returns:
            str: A string representing the file's last modified month, e.g. '2024-04'.
        """
        timestamp = file_path.stat().st_mtime
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m")

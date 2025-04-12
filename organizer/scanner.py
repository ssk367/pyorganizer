# organizer/scanner.py

from pathlib import Path
from typing import List
from organizer.logger import setup_logger


class FileScanner:
    """Scans a given directory and returns a list of files."""

    def __init__(self, directory: str, logger=None):
        self.directory = Path(directory)
        self.logger = logger or setup_logger()

        if not self.directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory.")

    def get_all_files(self) -> List[Path]:
        return [item for item in self.directory.iterdir() if item.is_file()]

    def get_all_files_recursive(self) -> List[Path]:
        return [item for item in self.directory.rglob("*") if item.is_file()]

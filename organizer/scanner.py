# organizer/scanner.py

from pathlib import Path
from typing import List


class FileScanner:
    """Scans a given directory and returns a list of files."""

    def __init__(self, directory: str):
        self.directory = Path(directory)
        if not self.directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory.")

    def get_all_files(self) -> List[Path]:
        """
        Returns:
            List[Path]: Returns a list of all files in the directory (non-recursive)
        """
        return [item for item in self.directory.iterdir() if item.is_file()]

    def get_all_files_recursive(self) -> List[Path]:
        """
        Returns:
            List[Path]: Returns a list of all files in the directory and subdirectories.
        """
        return [item for item in self.directory.rglob("*") if item.is_file()]

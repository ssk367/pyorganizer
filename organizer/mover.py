# organizer/mover.py

from pathlib import Path
import shutil
from organizer.logger import setup_logger


class FileMover:
    """Moves files to target directories based on categorization."""

    def __init__(self, logger=None):
        self.logger = logger or setup_logger()

    def move_to_folder(self, file_path: Path, target_root: Path, category: str) -> None:
        """Move a file into a subfolder under the target root based on the category.

        Args:
            file_path (Path): The path to the file to move.
            target_root (Path): The root directory where categorized folders will be created.
            category (str): The folder name to move the file into.

        Returns:
            None
        """
        destination_folder = target_root / category
        destination_folder.mkdir(parents=True, exist_ok=True)

        destination_path = destination_folder / file_path.name

        try:
            shutil.move(str(file_path), str(destination_path))
        except Exception as e:
            self.logger.error(
                f"Error moving file {file_path} -> {destination_path}: {e}"
            )

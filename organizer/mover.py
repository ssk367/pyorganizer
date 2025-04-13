# organizer/mover.py

from pathlib import Path
import shutil
from organizer.logger import setup_logger


class FileMover:
    def __init__(self, logger=None):
        self.logger = logger or setup_logger()

    def move_to_folder(self, file_path: Path, target_root: Path, category: str) -> None:
        """Move a file into a subfolder under the target root based on the category.
        Automatically renames the file if a collision occurs.

        Args:
            file_path (Path): The path to the file to move.
            target_root (Path): The root directory where categorized folders will be created.
            category (str): The folder name to move the file into.
        """
        destination_folder = target_root / category
        destination_folder.mkdir(parents=True, exist_ok=True)

        destination_path = destination_folder / file_path.name

        # 🔁 Handle filename collisions by adding suffixes
        if destination_path.exists():
            base = file_path.stem
            ext = file_path.suffix
            counter = 1

            while (destination_folder / f"{base}_{counter}{ext}").exists():
                counter += 1

            destination_path = destination_folder / f"{base}_{counter}{ext}"
            self.logger.debug(f"Renaming to avoid collision: {destination_path.name}")

        try:
            shutil.move(str(file_path), str(destination_path))
        except Exception as e:
            self.logger.error(
                f"Error moving file {file_path} -> {destination_path}: {e}"
            )

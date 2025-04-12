import argparse
from pathlib import Path

from organizer.scanner import FileScanner
from organizer.sorter import FileCategorizer
from organizer.mover import FileMover
from organizer.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(
        description="PyOrganizer - A utility to organize files by extension or date."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the folder you want to organize.",
    )
    parser.add_argument(
        "--by",
        choices=["extension", "date"],
        default="extension",
        help="Organize files by 'extension' or 'date'. Default is 'extension'.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview file moves without actually performing them.",
    )

    args = parser.parse_args()

    logger = setup_logger()
    logger.info(f"Organizing folder: {args.path} by {args.by}")

    target_dir = Path(args.path)
    if not target_dir.is_dir():
        logger.info(f"Error: '{args.path}' is not a valid directory.")
        return

    logger = setup_logger()
    logger.info(f"Organizing folder: {args.path} by {args.by}")

    # Initialize components
    scanner = FileScanner(target_dir)
    categorizer = FileCategorizer()
    mover = FileMover()

    files = scanner.get_all_files()

    logger.info(f"\nFound {len(files)} file(s) in '{args.path}'\n")

    for file_path in files:
        if args.by == "extension":
            category = categorizer.by_extension(file_path)
        else:
            category = categorizer.by_modification_date(file_path)

        if args.dry_run:
            logger.info(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
        else:
            mover.move_to_folder(file_path, target_dir, category)
            logger.info(f"Moved: {file_path.name} -> {category}/")


if __name__ == "__main__":
    main()

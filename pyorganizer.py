import argparse
from pathlib import Path
from organizer.logger import setup_logger
from organizer.scanner import FileScanner
from organizer.sorter import FileCategorizer
from organizer.mover import FileMover


def get_parser():
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
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO).",
    )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    logger = setup_logger(level=args.log_level)
    logger.info(f"Organizing folder: {args.path} by {args.by}")

    target_dir = Path(args.path)
    if not target_dir.is_dir():
        logger.error(f"Error: '{args.path}' is not a valid directory.")
        return

    scanner = FileScanner(target_dir, logger=logger)
    categorizer = FileCategorizer(logger=logger)
    mover = FileMover(logger=logger)

    files = scanner.get_all_files()
    logger.info(f"\nFound {len(files)} file(s) in '{args.path}'\n")

    moved_count = 0
    error_count = 0
    categories_created = set()

    for file_path in files:
        category = (
            categorizer.by_extension(file_path)
            if args.by == "extension"
            else categorizer.by_modification_date(file_path)
        )

        categories_created.add(category)

        if args.dry_run:
            logger.info(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
        else:
            try:
                mover.move_to_folder(file_path, target_dir, category)
                moved_count += 1
                logger.info(f"Moved: {file_path.name} -> {category}/")
            except Exception as e:
                logger.error(f"Error moving file {file_path.name}: {e}")
                error_count += 1

    logger.info("==== Summary ====")
    logger.info(f"Scanned: {len(files)} file(s)")
    logger.info(f"Categories created: {len(categories_created)}")
    logger.info(f"Moved: {moved_count} file(s)")
    logger.info(f"Errors: {error_count}")

    if args.dry_run:
        logger.info("Note: No files were actually moved due to dry run mode.")


if __name__ == "__main__":
    main()

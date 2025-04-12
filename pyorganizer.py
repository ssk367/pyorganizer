import argparse
from pathlib import Path

from organizer.scanner import FileScanner
from organizer.sorter import FileCategorizer
from organizer.mover import FileMover


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

    target_dir = Path(args.path)
    if not target_dir.is_dir():
        print(f"Error: '{args.path}' is not a valid directory.")
        return

    # Initialize components
    scanner = FileScanner(target_dir)
    categorizer = FileCategorizer()
    mover = FileMover()

    files = scanner.get_all_files()

    print(f"\nFound {len(files)} file(s) in '{args.path}'\n")

    for file_path in files:
        if args.by == "extension":
            category = categorizer.by_extension(file_path)
        else:
            category = categorizer.by_modification_date(file_path)

        if args.dry_run:
            print(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
        else:
            mover.move_to_folder(file_path, target_dir, category)
            print(f"Moved: {file_path.name} -> {category}/")


if __name__ == "__main__":
    main()

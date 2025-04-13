import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path

from organizer.logger import setup_logger
from organizer.scanner import FileScanner
from organizer.sorter import FileCategorizer
from organizer.mover import FileMover


class PyOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyOrganizer")
        self.root.geometry("400x250")

        self.logger = setup_logger(level="INFO")

        self.selected_path = tk.StringVar()
        self.organize_by = tk.StringVar(value="extension")
        self.dry_run = tk.BooleanVar()

        self._build_interface()

    def _build_interface(self):
        tk.Label(self.root, text="Select Folder to Organize:").pack(pady=(10, 0))

        path_frame = tk.Frame(self.root)
        path_frame.pack(fill="x", padx=10)

        tk.Entry(path_frame, textvariable=self.selected_path, width=30).pack(
            side="left", expand=True, fill="x"
        )
        tk.Button(path_frame, text="Browse", command=self._browse_folder).pack(
            side="right", padx=(5, 0)
        )

        tk.Label(self.root, text="Organize By:").pack(pady=(10, 0))
        ttk.Combobox(
            self.root,
            textvariable=self.organize_by,
            values=["extension", "date"],
            state="readonly",
        ).pack(padx=10, fill="x")

        tk.Checkbutton(
            self.root, text="Dry Run (preview only)", variable=self.dry_run
        ).pack(pady=5)

        tk.Button(self.root, text="Organize Files", command=self._organize_files).pack(
            pady=10
        )

        self.status_label = tk.Label(self.root, text="Ready", anchor="w")
        self.status_label.pack(side="bottom", fill="x", padx=5, pady=5)

    def _browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_path.set(folder)

    def _organize_files(self):
        path = Path(self.selected_path.get())
        if not path.is_dir():
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        scanner = FileScanner(path, logger=self.logger)
        categorizer = FileCategorizer(logger=self.logger)
        mover = FileMover(logger=self.logger)

        files = scanner.get_all_files()
        moved_count = 0
        error_count = 0
        categories_created = set()

        for file_path in files:
            category = (
                categorizer.by_extension(file_path)
                if self.organize_by.get() == "extension"
                else categorizer.by_modification_date(file_path)
            )

            categories_created.add(category)

            if self.dry_run.get():
                self.logger.info(
                    f"[DRY RUN] Would move: {file_path.name} -> {category}/"
                )
            else:
                try:
                    mover.move_to_folder(file_path, path, category)
                    moved_count += 1
                    self.logger.info(f"Moved: {file_path.name} -> {category}/")
                except Exception as e:
                    self.logger.error(f"Error moving file {file_path.name}: {e}")
                    error_count += 1

        summary = f"Scanned: {len(files)} | Moved: {moved_count} | Errors: {error_count} | Categories: {len(categories_created)}"
        self.status_label.config(text=summary)
        messagebox.showinfo("Done", "File organization complete.\n" + summary)


if __name__ == "__main__":
    root = tk.Tk()
    app = PyOrganizerGUI(root)
    root.mainloop()

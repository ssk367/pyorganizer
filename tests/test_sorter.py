import unittest
from pathlib import Path
from datetime import datetime
import os

from organizer.sorter import FileCategorizer


class TestFileCategorizer(unittest.TestCase):
    def setUp(self):
        self.categorizer = FileCategorizer()
        self.temp_dir = Path("tests/temp_sorter")
        self.temp_dir.mkdir(exist_ok=True)

        # Create files with extensions
        (self.temp_dir / "document.pdf").write_text("PDF content")
        (self.temp_dir / "image.JPG").write_text("JPG content")
        (self.temp_dir / "no_extension").write_text("No ext")

        # Create a file with a known mod time
        self.timestamp_file = self.temp_dir / "old_file.txt"
        self.timestamp_file.write_text("Old content")

        # Set fixed modification time (e.g., Jan 1, 2023)
        fixed_time = datetime(2023, 1, 1).timestamp()
        os.utime(self.timestamp_file, (fixed_time, fixed_time))

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_by_extension(self):
        self.assertEqual(
            self.categorizer.by_extension(self.temp_dir / "document.pdf"), "pdf"
        )
        self.assertEqual(
            self.categorizer.by_extension(self.temp_dir / "image.JPG"), "jpg"
        )
        self.assertEqual(
            self.categorizer.by_extension(self.temp_dir / "no_extension"),
            "no_extension",
        )

    def test_by_modification_date(self):
        category = self.categorizer.by_modification_date(self.timestamp_file)
        self.assertEqual(category, "2023-01")


if __name__ == "__main__":
    unittest.main()

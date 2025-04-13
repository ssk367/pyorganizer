import unittest
from pathlib import Path
import shutil

from organizer.scanner import FileScanner


class TestFileScanner(unittest.TestCase):
    def setUp(self):
        # Create a temporary folder with files
        self.test_dir = Path("tests/temp_test_dir")
        self.test_dir.mkdir(exist_ok=True)
        (self.test_dir / "file1.txt").write_text("Hello")
        (self.test_dir / "file2.jpg").write_text("Image")
        (self.test_dir / "nested").mkdir(exist_ok=True)
        (self.test_dir / "nested" / "file3.doc").write_text("Doc")

    def tearDown(self):
        # Recursively delete the entire test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_get_all_files(self):
        scanner = FileScanner(str(self.test_dir))
        files = scanner.get_all_files()
        self.assertEqual(len(files), 2)
        self.assertTrue(all(file.name in {"file1.txt", "file2.jpg"} for file in files))

    def test_get_all_files_recursive(self):
        scanner = FileScanner(str(self.test_dir))
        files = scanner.get_all_files_recursive()
        self.assertEqual(len(files), 3)
        self.assertTrue(any(file.name == "file3.doc" for file in files))


if __name__ == "__main__":
    unittest.main()

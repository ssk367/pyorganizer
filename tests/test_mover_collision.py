import unittest
import tempfile
import shutil
from pathlib import Path

from organizer.mover import FileMover


class TestFileMoverCollision(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.temp_dir.name) / "source"
        self.target_dir = Path(self.temp_dir.name) / "target"
        self.source_dir.mkdir(parents=True)
        self.target_dir.mkdir(parents=True)

        # Create two files with the same name in the source
        self.file1 = self.source_dir / "duplicate.txt"
        self.file2 = self.source_dir / "duplicate_copy.txt"

        self.file1.write_text("First file")
        self.file2.write_text("Second file")

        # Rename the second file to 'duplicate.txt' to simulate same name
        self.file2_renamed = self.source_dir / "duplicate.txt"
        shutil.copy(str(self.file2), str(self.file2_renamed))

        self.mover = FileMover()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_filename_collision_is_handled(self):
        category = "text"
        dest_path = self.target_dir / category
        dest_path.mkdir(parents=True, exist_ok=True)

        # Create first duplicate.txt and move
        file1 = self.source_dir / "duplicate.txt"
        file1.write_text("First file")
        self.mover.move_to_folder(file1, self.target_dir, category)

        # Create second duplicate.txt (with same name) and move
        file2 = self.source_dir / "duplicate.txt"
        file2.write_text("Second file")
        self.mover.move_to_folder(file2, self.target_dir, category)

        # Check both files exist with different names
        files_moved = sorted(p.name for p in dest_path.glob("*.txt"))
        self.assertIn("duplicate.txt", files_moved)
        self.assertIn("duplicate_1.txt", files_moved)
        self.assertEqual(len(files_moved), 2)


if __name__ == "__main__":
    unittest.main()

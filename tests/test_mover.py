import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import shutil

from organizer.mover import FileMover


class TestFileMover(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/temp_mover")
        self.test_dir.mkdir(exist_ok=True)

        self.test_file = self.test_dir / "testfile.txt"
        self.test_file.write_text("Test content")

        self.target_root = self.test_dir / "organized"
        self.category = "text_files"

        self.mover = FileMover()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("shutil.move")
    def test_move_to_folder_calls_shutil_move(self, mock_move):
        """Test that shutil.move is called with correct arguments."""
        self.mover.move_to_folder(self.test_file, self.target_root, self.category)

        expected_dest = self.target_root / self.category / self.test_file.name
        mock_move.assert_called_once_with(str(self.test_file), str(expected_dest))

        # Confirm the destination directory was created
        self.assertTrue((self.target_root / self.category).exists())

    @patch("shutil.move", side_effect=OSError("Permission denied"))
    def test_move_to_folder_logs_error_on_exception(self, mock_move):
        """Test that errors are logged when shutil.move fails."""
        with self.assertLogs("PyOrganizer", level="ERROR") as log:
            self.mover.move_to_folder(self.test_file, self.target_root, self.category)

            self.assertIn("Error moving file", log.output[0])
            self.assertIn("Permission denied", log.output[0])


if __name__ == "__main__":
    unittest.main()

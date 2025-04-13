import unittest
import subprocess
import tempfile
from pathlib import Path


class TestPyOrganizerCLI(unittest.TestCase):
    def setUp(self):
        # Create a temp directory with test files
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

        # Create sample files
        (self.test_path / "test1.pdf").write_text("PDF content")
        (self.test_path / "test2.jpg").write_text("Image content")
        (self.test_path / "test3").write_text("No extension")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_cli_organizes_by_extension(self):
        # Run the CLI tool using subprocess
        result = subprocess.run(
            [
                "python",
                "pyorganizer.py",
                "--path",
                str(self.test_path),
                "--by",
                "extension",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr into stdout
            text=True,
        )

        # ✅ CLI exited cleanly
        self.assertEqual(result.returncode, 0)

        # ✅ Output contains expected logs
        self.assertIn("Moved: test1.pdf", result.stdout)
        self.assertIn("Moved: test2.jpg", result.stdout)

        # ✅ Files have been moved
        self.assertTrue((self.test_path / "pdf" / "test1.pdf").exists())
        self.assertTrue((self.test_path / "jpg" / "test2.jpg").exists())
        self.assertTrue((self.test_path / "no_extension" / "test3").exists())


if __name__ == "__main__":
    unittest.main()

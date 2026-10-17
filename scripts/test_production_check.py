import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from pathlib import Path

import production_check as pc


class ScanTests(unittest.TestCase):
    def test_detects_lorem_ipsum(self):
        self.assertTrue(pc.scan_text("<h1>Lorem ipsum dolor</h1>"))

    def test_detects_todo(self):
        self.assertEqual(pc.scan_text("// TODO fix timing")[0]["issue"], "developer note")

    def test_detects_your_text_here(self):
        self.assertTrue(pc.scan_text("Your text here"))

    def test_clean_text_passes(self):
        self.assertEqual(pc.scan_text("Solar power grew 24% in 2025."), [])

    def test_lowercase_todo_word_not_flagged(self):
        self.assertEqual(pc.scan_text("a list of things to do today"), [])

    def test_missing_asset_and_exit_code(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "scene.tsx"
            f.write_text('<img src="./logo.png" />', encoding="utf-8")
            self.assertEqual(pc.main(["scan", d]), 1)
            (Path(d) / "logo.png").write_bytes(b"x")
            self.assertEqual(pc.main(["scan", d]), 0)

    def test_parse_blackdetect(self):
        s = "[blackdetect @ 0x1] black_start:0 black_end:0.5 black_duration:0.5"
        self.assertEqual(pc.parse_blackdetect(s)[0]["duration"], 0.5)

    def test_missing_scan_path_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(pc.main(["scan", str(Path(d) / "missing.html")]), 2)

    def test_mixed_valid_and_missing_scan_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "scene.html"
            p.write_text("Hello")
            self.assertEqual(pc.main(["scan", str(p), str(Path(d) / "missing")]), 2)

    def test_empty_scan_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(pc.main(["scan", d]), 2)

    def test_unreadable_scan_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "scene.html"
            p.write_text("Hello")
            with patch.object(Path, "read_text", side_effect=OSError("unreadable")):
                self.assertEqual(pc.main(["scan", str(p)]), 2)

    def test_missing_video_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(pc.main(["blackframes", str(Path(d) / "missing.mp4")]), 2)

    def test_failed_decode_is_error(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with patch.object(pc.shutil, "which", return_value="ffmpeg"), patch.object(
                pc.subprocess, "run", return_value=SimpleNamespace(returncode=1, stderr="invalid video")
            ):
                self.assertEqual(pc.main(["blackframes", f.name]), 2)

    def test_invalid_duration_is_error(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            for value in ["0", "-1", "nan", "inf"]:
                with self.subTest(value=value):
                    self.assertEqual(pc.main(["blackframes", f.name, "--min-duration", value]), 2)

    def test_decode_launch_error_is_error(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with patch.object(pc.shutil, "which", return_value="ffmpeg"), patch.object(
                pc.subprocess, "run", side_effect=OSError("launch failed")
            ):
                self.assertEqual(pc.main(["blackframes", f.name]), 2)

    def test_successful_decode_exit_codes(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            for stderr, expected in [("", 0), ("black_start:0 black_end:0.5 black_duration:0.5", 1)]:
                with self.subTest(expected=expected), patch.object(pc.shutil, "which", return_value="ffmpeg"), patch.object(
                    pc.subprocess, "run", return_value=SimpleNamespace(returncode=0, stderr=stderr)
                ):
                    self.assertEqual(pc.main(["blackframes", f.name]), expected)


if __name__ == "__main__":
    unittest.main()

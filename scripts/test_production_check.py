import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()

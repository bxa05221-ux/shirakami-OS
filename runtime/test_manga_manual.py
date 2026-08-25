import re
import unittest
from pathlib import Path

from manga_manual import render_manual


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "protocols" / "manual" / "manga-user-manual.yaml"


class MangaManualRendererTests(unittest.TestCase):
    def test_japanese_manual_contains_all_pages(self):
        svg = render_manual(SOURCE, "ja")
        self.assertEqual(svg.count("<g transform="), 4)
        self.assertIn("AIが変わっても、景色を残したい", svg)
        self.assertIn("同じ構造を、別の言語へ", svg)

    def test_english_manual_uses_same_page_structure(self):
        svg = render_manual(SOURCE, "en")
        self.assertEqual(svg.count("<g transform="), 4)
        self.assertRegex(svg, r"Keep the landscape, even when AI\s*changes")
        self.assertRegex(svg, r"Render the same structure in another\s*language")


if __name__ == "__main__":
    unittest.main()

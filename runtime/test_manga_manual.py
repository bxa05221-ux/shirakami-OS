import re
import unittest
from pathlib import Path

from manga_manual import render_manual


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "protocols" / "manual" / "manga-user-manual.yaml"


def rendered_text(svg: str) -> str:
    """Return rendered text with SVG tags removed so wrapping is irrelevant."""
    return re.sub(r"<[^>]+>", "", svg)


class MangaManualRendererTests(unittest.TestCase):
    def test_japanese_manual_contains_all_pages(self):
        svg = render_manual(SOURCE, "ja")
        text = rendered_text(svg)
        self.assertEqual(svg.count("<g transform="), 4)
        self.assertIn("AIが変わっても、景色を残したい", text)
        self.assertIn("同じ構造を、別の言語へ", text)

    def test_english_manual_uses_same_page_structure(self):
        svg = render_manual(SOURCE, "en")
        text = rendered_text(svg)
        self.assertEqual(svg.count("<g transform="), 4)
        self.assertIn("Keep the landscape, even when AI changes", text)
        self.assertIn("Render the same structure in another language", text)


if __name__ == "__main__":
    unittest.main()

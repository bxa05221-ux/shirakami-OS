from pathlib import Path

from manga_manual import render_manual


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "protocols" / "manual" / "manga-user-manual.yaml"


def test_japanese_manual_contains_all_pages():
    svg = render_manual(SOURCE, "ja")
    assert svg.count("<g transform=") == 4
    assert "AIが変わっても、景色を残したい" in svg
    assert "同じ構造を、別の言語へ" in svg


def test_english_manual_uses_same_page_structure():
    svg = render_manual(SOURCE, "en")
    assert svg.count("<g transform=") == 4
    assert "Keep the landscape, even when AI changes" in svg
    assert "Render the same structure in another language" in svg

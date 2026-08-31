"""Minimal multilingual manga-manual renderer for the Public Alpha.

This renderer intentionally supports only the small manual protocol subset
used by protocols/manual/manga-user-manual.yaml. It is a documentation/UI
adapter experiment, not a general YAML parser or image-generation engine.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


class ManualRenderError(ValueError):
    """Raised when the manual source cannot be rendered."""


def render_manual(source: str | Path, language: str = "ja") -> str:
    text = Path(source).read_text(encoding="utf-8") if isinstance(source, (str, Path)) else source
    pages = _parse_pages(text, language)
    if not pages:
        raise ManualRenderError("manual must contain at least one page")

    width, height = 1200, 900
    panels = [_panel(index, page) for index, page in enumerate(pages, start=1)]
    body = "\n".join(panels)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height * len(panels)}" viewBox="0 0 {width} {height * len(panels)}">
  <title>Shirakami OS User Manual Manga ({html.escape(language)})</title>
  <desc>Generated from a Matome YAML manual source.</desc>
  {body}
</svg>
'''


def _parse_pages(text: str, language: str) -> list[dict[str, str]]:
    if not re.search(r"^\s+manual:\s*$", text, re.MULTILINE):
        raise ManualRenderError("matome.manual is required")

    chunks = re.split(r"^\s{6}- id:\s*", text, flags=re.MULTILINE)
    pages: list[dict[str, str]] = []
    for chunk in chunks[1:]:
        page_id, _, rest = chunk.partition("\n")
        page = {"id": page_id.strip()}
        for field in ("title", "narration", "dialogue"):
            value = _localized_value(rest, field, language)
            if value:
                page[field] = value
        required = ("id", "title", "narration", "dialogue")
        if not all(page.get(key) for key in required):
            raise ManualRenderError(f"page '{page_id.strip()}' is incomplete")
        pages.append(page)
    return pages


def _localized_value(text: str, field: str, language: str) -> str | None:
    pattern = rf"^\s{{8}}{re.escape(field)}:\s*$\n(.*?)(?=^\s{{8}}(?:title|narration|dialogue):\s*$|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        return None
    locale_match = re.search(
        rf"^\s{{10}}{re.escape(language)}:\s*[\"']?(.*?)[\"']?\s*$",
        match.group(1),
        re.MULTILINE,
    )
    if not locale_match:
        return None
    return locale_match.group(1).strip().strip('"\'')


def _panel(index: int, page: dict[str, str]) -> str:
    width, height = 1200, 900
    y = (index - 1) * height
    title = _wrap(page["title"], 38)
    narration = _wrap(page["narration"], 46)
    dialogue = _wrap(page["dialogue"], 38)
    full_title = html.escape(page["title"])

    def text_lines(lines: list[str], x: int, start_y: int, line_height: int, size: int, weight: str = "normal") -> str:
        return "\n".join(
            f'<text x="{x}" y="{start_y + i * line_height}" font-size="{size}px" font-weight="{weight}" font-family="sans-serif">{html.escape(line)}</text>'
            for i, line in enumerate(lines)
        )

    return f'''<g transform="translate(0,{y})">
  <title>{full_title}</title>
  <rect x="40" y="40" width="1120" height="820" rx="24" fill="white" stroke="black" stroke-width="4"/>
  <text x="80" y="100" font-size="28px" font-family="sans-serif">PAGE {index} · {html.escape(page["id"])}</text>
  {text_lines(title, 100, 190, 48, 40, "bold")}
  <rect x="90" y="310" width="1020" height="210" rx="18" fill="none" stroke="black" stroke-width="3"/>
  {text_lines(narration, 125, 370, 42, 28)}
  <rect x="250" y="570" width="760" height="170" rx="85" fill="white" stroke="black" stroke-width="3"/>
  {text_lines(dialogue, 320, 640, 42, 30)}
</g>'''


def _wrap(value: str, width: int) -> list[str]:
    """Wrap Latin text at whitespace; preserve character wrapping for CJK."""
    if len(value) <= width:
        return [value]
    if re.search(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", value):
        return [value[index:index + width] for index in range(0, len(value), width)]

    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a Shirakami manga manual from Matome YAML")
    parser.add_argument("source")
    parser.add_argument("--lang", default="ja")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    svg = render_manual(args.source, args.lang)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    print(f"Rendered {args.lang}: {output}")


if __name__ == "__main__":
    main()

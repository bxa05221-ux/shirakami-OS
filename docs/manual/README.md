# User Manual — Manga Renderer α0.1

This directory contains the Public Alpha demonstration of a multilingual manga-style user manual generated from a Matome YAML source.

## Source

- [`protocols/manual/manga-user-manual.yaml`](../../protocols/manual/manga-user-manual.yaml)
- [`spec/manual-rendering.md`](../../spec/manual-rendering.md)
- [`runtime/manga_manual.py`](../../runtime/manga_manual.py)

## Generated manuals

- [日本語版 — SVG](manga-user-manual.ja.svg)
- [English — SVG](manga-user-manual.en.svg)

## Re-render

```bash
python runtime/manga_manual.py \
  protocols/manual/manga-user-manual.yaml \
  --lang ja \
  --output docs/manual/manga-user-manual.ja.svg

python runtime/manga_manual.py \
  protocols/manual/manga-user-manual.yaml \
  --lang en \
  --output docs/manual/manga-user-manual.en.svg
```

The renderer is intentionally minimal. It demonstrates the separation between manual structure, language, and presentation. It is not a general manga-generation engine.

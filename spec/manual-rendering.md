# Manual Rendering Contract α0.1

## Purpose

This document defines the smallest rendering boundary for the Public Alpha user-manual experiment.

The goal is not to define a general manga-generation system. The goal is to demonstrate that a structured Matome Protocol can be rendered into a human-facing manual while keeping content structure separate from language and presentation.

## Flow

```text
Matome YAML
    ↓
Manual Source
    ↓
Language Selection
    ↓
Manga Renderer
    ↓
SVG Manual
```

## Contract

- The source protocol is the canonical content structure.
- Language is selected at render time.
- Page order and semantic page IDs remain language-independent.
- Dialogue, narration, and titles may vary by locale.
- The renderer does not invent protocol meaning.
- SVG is the current Public Alpha output format because it is text-based and repository-friendly.
- PNG generation, speech output, image-model integration, and advanced panel layout are out of scope for α0.1.

## Multilingual principle

A locale changes presentation language, not the underlying manual structure.

For example:

```text
page id: landscape
  ja → Japanese text
  en → English text
```

The same page ID remains observable across languages.

## Current status

This is an experimental UI/documentation adapter for Public Alpha. It is not yet part of the core Runtime Contract and must not be treated as a finalized architectural specification.

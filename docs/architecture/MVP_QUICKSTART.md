# MVP Quickstart

> This document is the shortest path to running the current Shirakami Runtime MVP.

## Requirements

- Python 3.11+
- Git

## Run

```bash
python shirakami_os.py
```

## Test

```bash
pytest runtime tests -q
```

## Current Boundary

The current MVP verifies the Runtime-side execution boundary and intentionally stops before provider-specific AI invocation.

The Runtime is responsible for executing Protocol-side semantics and producing observable execution results. External AI providers remain replaceable adapters and are not required for this quickstart.

## Repository Structure

```text
Landscape → Evidence → Protocol → Runtime → Adapter → Backend
```

## Notes

This quickstart is an implementation entry point, not a complete specification of the Shirakami Model. Consult the architecture and protocol documents for the relevant boundaries and limitations.

# Shirakami OS Documentation Architecture α0.1

The project separates documentation responsibilities so that one document class cannot silently redefine another.

| Layer | Question | Allowed content | Explicitly excluded |
|---|---|---|---|
| Vision | Why? | purpose, vision, landscape-level intent | API, directories, classes, implementation |
| Constitution | What must be protected? | principles, invariants, boundaries | implementation details, data structures, class design |
| Blueprint | What structure? | components, responsibilities, boundaries | algorithms, API contracts, concrete code |
| Design | How is it specified? | API, state machine, IR format, workspace layout | changing constitutional principles |
| Implementation | What runs? | code, tests, configuration, executable behavior | silently redefining Vision/Constitution |

## Rule

If content crosses a boundary, it must be moved to the document layer that owns that responsibility rather than extending the current document opportunistically.

## Protocol Registry Position

The Protocol Registry is a catalog/metadata artifact. It is not a sixth architectural layer.

```text
Vision
  ↓
Constitution
  ↓
Blueprint
  ↓
Design
  ↓
Implementation

Protocol Registry = index across the implementation boundary
Matome YAML       = source protocol asset
```

The registry records protocol identity, classification, source status, and verification tier. It does not redefine protocol semantics.

## Source Basis

The project information explicitly establishes the five-level documentation architecture: Vision → Constitution → Blueprint → Design → Implementation, with API, State Machine, IR Format, and Workspace Layout belonging to Design rather than Blueprint. fileciteturn168file15

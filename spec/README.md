# Implementation-Side Specification Index

This directory contains implementation-side specifications and transition material that remains useful to the `shirakami-OS` reference implementation.

## Canonical Normative Specifications

Stable normative contracts now live in the separate `shirakami-specification` repository.

- [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification)
- Protocol Specification α0.1
- Adapter Contract α0.1
- Plugin Contract
- Plugin Lifecycle Contract
- Runtime Lifecycle Contract
- Contract Layer Overview

## Boundary

Files kept here should explain implementation boundaries, compatibility notes, migration context, or experimental behavior. They should not silently become the canonical normative definition of Shirakami OS.

## Current Transition

The former `spec/protocol.md` and `spec/adapter-contract.md` have been promoted to the normative specification repository. They remain in this repository temporarily so implementation history and local references can be migrated without losing context.

## Experimental Material

`spec/manual-rendering.md` remains implementation-side and experimental. It is not part of the core Runtime Contract.

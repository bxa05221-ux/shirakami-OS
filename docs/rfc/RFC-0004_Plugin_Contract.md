# RFC-0004 Plugin Contract

## Purpose

This RFC defines the minimum architectural contract that every Shirakami OS plugin must satisfy. The contract exists to set clear, implementation-agnostic expectations about what a plugin declares and how it behaves within the Runtime.

## Required Metadata

Every plugin MUST provide, at a minimum, the following conceptual metadata:

- Name
- Version
- Description
- Capability
- Provider

These elements describe the plugin’s identity, the capability it offers, its provenance, and a human-readable summary. This section describes conceptual requirements only; it does not mandate file layouts, syntax, or formats.

## Responsibilities

- Provides one capability.
- Extends Runtime.
- Never modifies Foundation.
- Operates independently.

Plugins are expected to be focused, to contribute a single, well-scoped capability, and to interact with the Runtime without altering Foundation artifacts or other plugins' operation.

## Principles

- Single Responsibility
- Loose Coupling
- Runtime Managed
- Foundation Protected

These principles guide plugin authors and Runtime designers to keep plugins simple, decoupled, and safely governed by the Runtime.

## Out of Scope

This RFC does not define or prescribe:

- APIs
- Loaders
- Registration
- Dependency Injection
- Configuration
- Security
- Implementation
- Programming Language

A contract defines expectations, not implementation.

# OPPAI Pipeline Selection Contract v0.1

Status: proposal / contract draft

## Purpose

The current repository already contains OPPAI normalization, ProtocolRegistry, ProtocolRequest, RouteMap, and a canonical Protocol → Runtime path. The missing boundary is the connection from OPPAI observation to selection/request of the Protocol Pipeline.

The working hypothesis is that OPPAI is not merely a prompt-normalization layer. Its basic operational task is to identify candidate Protocol Pipelines for the current interaction, while preserving the Human Decision Boundary.

## Conceptual position

Human / Landscape
→ Natural Language
→ OPPAI
→ Protocol Pipeline Candidates
→ Human Gate
→ Protocol Selection / Request
→ ProtocolRegistry
→ ProtocolRequest
→ Runtime
→ Adapter
→ Generation AI / Backend
→ Evidence
→ Human Judgment

## Core responsibility

OPPAI MAY:
- observe explicit properties of human interaction;
- normalize input without erasing conversational history;
- preserve corrections and unresolved items;
- identify candidate Protocol Pipelines from observable input and context;
- consider explicitly represented Landscape conditions such as timing, availability, permission, and backend availability;
- emit a Protocol Selection Request.

OPPAI MUST NOT:
- silently make the final human judgment;
- redefine Protocol semantics;
- promote AI-generated interpretation into semantic authority;
- silently activate an unapproved Protocol where Human Gate is required;
- own Runtime execution;
- equate OPPAI normalization confidence with Evidence confidence;
- use hidden psychological inference as routing authority.

## Pipeline model

A Pipeline is an execution path associated with a Protocol:

Protocol
→ Pipeline
→ Adapter
→ Generation AI / Backend

The backend may vary according to Protocol, Landscape, execution context, time/availability, permission, and operational constraints. The semantic Protocol therefore remains separate from the replaceable generation backend.

## Candidate versus selection

OPPAI produces candidates; it does not silently turn a candidate into authority.

Conceptual candidate:

    protocol_candidates:
      - protocol_id: example.protocol
        pipeline_id: example.pipeline
        basis:
          - observable_signal
          - context_match
        status: candidate

Conceptual selected request:

    protocol_selection:
      status: selected
      protocol_id: example.protocol
      pipeline_id: example.pipeline
      authority: human

If selection is unresolved, it remains unresolved. No implicit fallback to an arbitrary Protocol is defined by this contract.

## Minimal handoff

    oppai_protocol_handoff:
      observation:
        raw_input: "..."
        canonical_prompt: "..."
        context: {}
        unresolved: []

      protocol_candidates:
        - protocol_id: "..."
          pipeline_id: "..."
          basis: []
          status: candidate

      human_gate:
        required: true
        status: unresolved
        selected_protocol: null
        selected_pipeline: null

      protocol_request:
        status: pending
        protocol_id: null
        version: null
        input: {}

This is a conceptual contract, not yet the Runtime schema.

## Boundary ownership

| Function | Owner |
|---|---|
| Natural-language observation | OPPAI |
| Prompt normalization | OPPAI |
| Candidate Protocol discovery | OPPAI / authorized routing mechanism |
| Final Protocol selection | Human Gate or explicitly authorized policy |
| Protocol artifact resolution | ProtocolRegistry |
| ProtocolRequest construction | Protocol API |
| Protocol execution | Runtime |
| AI/backend selection inside execution constraints | Adapter/Pipeline |
| Execution observation | Runtime/Evidence |
| Final real-world judgment | Human |

## Relationship to RouteMap

RouteMap already represents explicit Protocol-to-Protocol reachability. OPPAI should not infer arbitrary routes merely because an input appears compatible with them.

The intended relationship is:

OPPAI candidate discovery
→ route / permission constraints
→ Human Gate
→ ProtocolRequest

Routing remains observable rather than becoming hidden semantic authority.

## Relationship to generation AI

The selected Protocol does not imply one permanent model vendor.

Protocol
→ Pipeline Selection
→ Adapter
→ Generation AI

The same Protocol can therefore operate through different generation backends when the Landscape and authorized execution conditions differ.

## Evidence boundary

OPPAI observation and Runtime Evidence remain separate.

OPPAI may record what it observed about the input and routing candidates. Runtime Evidence records what execution actually occurred.

No automatic mapping is defined between OPPAI confidence and Evidence confidence; they are different axes until a future contract proves otherwise.

## Required verification

Before implementation changes, verify:

1. Multiple Protocols can be represented as selectable candidates.
2. Pipeline identity can be represented independently from Protocol identity.
3. A selected Protocol can be resolved through the existing ProtocolRegistry.
4. The selected Protocol can be converted into the existing ProtocolRequest.
5. The resulting request reaches the existing Runtime path without bypassing contracts.
6. Adapter/backend selection can vary without changing Protocol meaning.
7. Unresolved selection remains unresolved.
8. Routing decisions are observable in route history and/or Evidence.

## Non-goals

This contract does not:
- change Protocol semantics;
- change ProtocolRegistry behavior;
- change Evidence schema;
- define an autonomous Protocol selector;
- define a model-ranking system;
- claim that one generation AI is better than another;
- require a specific AI vendor;
- replace the Human Decision Boundary.

## Status

This is a hypothesis-driven contract draft derived from the existing implementation and the observed OPPAI → Protocol → Runtime gap.

Implementation should follow verification of these boundaries rather than precede it.

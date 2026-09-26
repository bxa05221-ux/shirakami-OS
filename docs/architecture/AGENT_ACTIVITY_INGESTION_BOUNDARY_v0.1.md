# Agent Activity Ingestion Boundary v0.1

## Status

- Status: specification draft
- Scope: external Agent activity ingestion
- Boundary: Agent → Shirakami Runtime
- Authority: non-granting
- Evidence status: unverified until verification
- Human Gate: required for promotion/adoption decisions

## 1. Purpose

The Agent Activity Ingestion Boundary provides a provider-neutral entry point for activity that has already occurred outside the Shirakami Runtime.

It does not execute the activity, authorize the Agent, or declare the activity to be Evidence merely because an Agent reported it.

The boundary exists to make external Agent activity observable, traceable, and verifiable.

## 2. Architectural Position

    External Agent
          |
          | Activity
          v
    Agent Activity Ingestion Boundary
          |
          v
      Observation
          |
          v
    Evidence Candidate
          |
          v
      Verification
       /        \
      v          v
  Evidence    Unverified / Rejected
      |
      v
 ExecutionTrace
      |
      v
   AIwitness

The existing Provider Boundary remains separate:

    Shirakami Runtime
          |
          v
    RealModelAdapter
          |
          v
    ProviderTransport
          |
          v
       Model

Provider output and Agent activity are different classes of external information.

## 3. Boundary Principle

The boundary MUST distinguish:

1. what the external Agent claims to have done;
2. what Shirakami observed receiving;
3. what can be independently verified;
4. what is promoted to Evidence.

Receiving an Agent Activity record MUST NOT by itself establish that the underlying external operation actually occurred.

## 4. Agent Activity Record

Minimum conceptual fields:

    activity_id
    agent_id
    session_id
    source
    timestamp
    operation.type
    operation.target
    operation.input
    operation.result
    provenance
    self_reported
    verification_status

The initial contract SHOULD permit opaque provider-specific metadata without allowing provider metadata to modify Shirakami authority state.

## 5. Activity Types

The initial boundary SHOULD support the following conceptual operation types:

- file_read
- file_write
- search
- shell_command
- git_operation
- tool_call
- mcp_call
- http_request
- model_call
- other

Implementations MAY introduce additional types, but MUST preserve the distinction between the activity itself and Shirakami's verification of that activity.

## 6. Identity and Provenance

The boundary SHOULD preserve:

- agent identity, where available;
- agent session identity, where available;
- source/provider;
- originating environment;
- timestamp;
- target/resource;
- operation type;
- reported result;
- provenance metadata;
- verification status.

Missing identity information MUST be represented as unknown rather than inferred.

## 7. ID Lifecycle

The boundary MUST NOT require the external Agent to manufacture Shirakami Evidence IDs.

Conceptual lifecycle:

    activity_id
        |
        v
    handoff_id
        |
        v
    execution_id / trace_id
        |
        v
    evidence_id

These identifiers represent progressively stronger Shirakami-side linkage.

An external Agent MAY provide correlation identifiers, but Shirakami MUST distinguish external correlation identifiers from Shirakami-generated identifiers.

## 8. Observation Boundary

An accepted Activity record first becomes an Observation Candidate.

Example:

    Agent Activity
      "read runtime/trace.py"
             |
             v
    Observation
      source = external_agent
      operation = file_read
      target = runtime/trace.py
      verification_status = unverified

Observation does not imply Evidence.

## 9. Evidence Promotion

Evidence promotion MUST preserve provenance and uncertainty.

A promoted Evidence record SHOULD identify:

- source Activity;
- source Agent/session;
- originating repository/environment;
- relevant commit or resource version;
- verification method;
- verification result;
- uncertainty;
- evidence_id.

The original Activity and Candidate records MUST remain distinguishable from the promoted Evidence.

## 10. ExecutionTrace Integration

External Agent activity MAY be linked to ExecutionTrace after Shirakami assigns the necessary execution context.

ExecutionTrace MUST describe the linkage rather than falsely implying that Shirakami Runtime itself performed the external operation.

Example:

    transition_kind:
      external_agent_activity

    execution_subject:
      actor: external_agent
      operation: file_read

    verification_status:
      pending

The trace SHOULD retain the fact that the activity originated outside the Runtime.

## 11. AIwitness Integration

AIwitness records SHOULD reference the same verified Evidence IDs used by ExecutionTrace.

AIwitness MUST NOT convert:

    Agent claim → verified fact

without an explicit verification boundary.

The witness layer records traceability and provenance; it does not grant execution, publication, merge, or other authority.

## 12. Authority Boundary

The Agent Activity Ingestion Boundary MUST NOT set or infer:

    execution_authorized
    publish_authorized
    merge_authorized

These remain Shirakami authority-state fields.

The default boundary state is:

    execution_authorized: false
    publish_authorized: false
    merge_authorized: false
    human_gate_required: true

An Activity record cannot bypass Human Gate.

## 13. Self-Reported vs Independently Observed

The boundary SHOULD distinguish at minimum:

    self_reported
    observed_by_runtime
    independently_verified

These are provenance/verification states, not authority states.

For example:

    Copilot says:
      "I read runtime/trace.py"

is initially:

    self_reported: true
    independently_verified: false

A later verification mechanism may establish stronger provenance without mutating the original claim.

## 14. Initial Copilot Validation

The first validation target is the existing Copilot review operation.

Candidate activities include:

- repository file reads;
- repository searches;
- git status inspection;
- git HEAD inspection;
- review synthesis.

The first implementation SHOULD NOT attempt to capture every Copilot internal event.

The minimum validation goal is:

    Copilot Activity
        ↓
    Activity Boundary
        ↓
    Observation
        ↓
    Evidence Candidate
        ↓
    verification metadata

without granting authority or modifying existing Runtime semantics.

## 15. Provider Boundary Separation

Copilot may appear in two distinct roles.

### Provider role

    Shirakami Runtime
        ↓
    RealModelAdapter
        ↓
    ProviderTransport
        ↓
    Copilot SDK
        ↓
    Model

### Agent role

    Copilot Agent
        ↓
    Agent Activity Ingestion Boundary
        ↓
    Observation
        ↓
    Evidence Candidate
        ↓
    Verification
        ↓
    Evidence / Trace / AIwitness

The two paths MUST NOT be conflated.

## 16. MCP

MCP is a potential future source of Agent Activity.

An MCP tool call SHOULD enter the same Agent Activity Boundary rather than receiving a separate Evidence semantics.

Conceptually:

    Agent
      ↓
    MCP Tool Call
      ↓
    Agent Activity
      ↓
    common ingestion boundary

This avoids creating provider-specific traceability models.

## 17. Security and Trust

The boundary MUST treat external Agent input as untrusted activity metadata until verified.

In particular:

- external Agent claims MUST NOT become authority;
- external Evidence IDs MUST NOT overwrite Shirakami Evidence IDs;
- provider credentials MUST NOT be copied into Evidence;
- secrets SHOULD be redacted before persistence;
- activity results SHOULD preserve uncertainty when verification is unavailable;
- provenance loss MUST be explicit.

## 18. Non-Goals

This boundary does NOT:

- execute Agent commands;
- approve Agent actions;
- replace Human Gate;
- authenticate a human decision merely from an Agent claim;
- prove external activity solely by receiving a report;
- replace the ProviderTransport boundary;
- require a specific model vendor;
- require a specific Agent framework.

## 19. Verification Gate

A future implementation is considered boundary-valid only when the following chain can be demonstrated:

    external Agent activity
        ↓
    Activity Boundary
        ↓
    Observation
        ↓
    Evidence Candidate
        ↓
    Verification
        ↓
    Evidence
        ↓
    ExecutionTrace
        ↓
    AIwitness

with all of the following remaining true:

    execution_authorized = false
    publish_authorized = false
    merge_authorized = false
    human_gate_required = true

The verification must also demonstrate that the original external activity remains identifiable as external activity.

## 20. Open Questions

The following MUST remain explicit before implementation is considered complete:

1. How is external activity authenticated?
2. Which activity facts can be independently verified?
3. Which local tools can provide independent provenance?
4. How are timestamps normalized?
5. How are file/resource versions bound to activity?
6. How are secrets and sensitive inputs redacted?
7. When should an Activity receive a handoff_id?
8. When should execution_id/trace_id be created?
9. Which verification results are sufficient for Evidence promotion?
10. How should partial or failed Agent activity be represented?

## 21. Design Rule

The central rule of this boundary is:

> An Agent may report what it did. Shirakami records that report as an observation. Verification determines what can become Evidence. Human authority remains outside the Agent.

This preserves the existing Shirakami principle:

> AIが動いても、決定権は動かない。

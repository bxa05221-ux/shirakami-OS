# GitHub Copilot SDK Async Boundary v0.1

## Status

Boundary specification only. No provider credentials are required and no external model execution is claimed.

## Rationale

The current GitHub Copilot Python SDK exposes native async session APIs. Shirakami's existing `ProviderTransport` contract is synchronous.

Rather than hiding an event loop inside the synchronous Runtime, Shirakami defines an explicit `AsyncProviderTransport` boundary.

## Flow

External HTTP → Shirakami API → Runtime → RealModelAdapter → AsyncProviderTransport → GitHub Copilot SDK → model → opaque output → RuntimeResult → Evidence → Trace → AIwitness

## Boundary rules

The async provider transport:

- receives only `ProviderRequest`;
- returns opaque provider output;
- does not create or rewrite Evidence;
- does not modify Trace or AIwitness state;
- does not authorize execution, publication, or merge;
- does not bypass Human Gate;
- does not carry provider credentials in `ProviderRequest`;
- remains replaceable by another provider transport.

Authentication and provider credentials remain deployment/provider concerns.

## Verification gate

Actual completion of the real-provider boundary still requires an external provider execution that proves:

1. model output reaches `RuntimeResult`;
2. exact output is bound to Evidence;
3. Evidence ID changes when output changes;
4. Trace and AIwitness reference the same Evidence ID;
5. `execution_authorized` remains false;
6. `human_gate_required` remains true;
7. credentials do not enter source-controlled code or Evidence.

This document does not mark API MVP items 9 or 10 complete.

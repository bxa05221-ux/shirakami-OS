# Shirakami Licensing Boundary Matrix

## Status

Draft architecture aid for review. This document does not grant, revoke, or interpret legal rights.

## Purpose

This matrix separates the four layers of Shirakami so that a future licensing transition does not accidentally change rights, conformance claims, or authority boundaries.

| Layer | Typical material | Intended treatment | Key boundary |
|---|---|---|---|
| Implementation / research | Python source, tests, utilities | Existing file/directory license | Code rights are not protocol-conformance rights |
| Protocol | Normative specifications, schemas, boundary contracts | Future Shirakami Protocol License | Protocol rights do not grant AI authority |
| Commercial integration | API, hosted service, SDK, adapters, managed integration | Vendor License / Integration Agreement | Eligibility must be vendor-neutral |
| Name / conformance | Shirakami name, marks, badges, conformance claims | Separate branding/conformance policy | Passing tests does not automatically grant certification |

## Cross-layer rules

1. A repository contribution or implementation right does not automatically grant permission to use the Shirakami name as a conformance claim.
2. A protocol license does not automatically replace the license of implementation code.
3. A commercial agreement must not silently weaken normative protocol invariants.
4. Conformance requirements must be observable and versioned.
5. Human Gate remains an architectural boundary and is not transferred by any license, API credential, or integration agreement.
6. Equivalent vendors should receive materially equivalent published eligibility conditions.
7. Third-party copyright, attribution, dependency, and notice obligations remain applicable.
8. Any final certification or trademark program must be defined separately from ordinary copyright licensing.

## Transition gate

Before changing the top-level LICENSE or publishing binding commercial terms, verify:

- affected files and directories are inventoried;
- copyright and third-party notices are preserved;
- compatibility with existing licenses is reviewed;
- protocol and implementation scopes are explicitly separated;
- conformance and branding rules are separately defined;
- legal review is complete;
- Human Gate explicitly authorizes adoption.

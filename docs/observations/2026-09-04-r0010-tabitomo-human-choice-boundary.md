# R0010 旅とも Human Choice Boundary Observation

- Status: implementation-side observation
- Runtime change: none
- Theory change: none
- Protocol change: none

## 1. Existing Boundary

R0010 has already established that Runtime must not autonomously infer necessity, truth, correctness, or replace Human judgment.

This observation applies that settled boundary to the `旅とも` use case.

## 2. Observed Application Flow

```text
Traveler observation
    ↓
Character response
    ↓
Options / possibilities
    ↓
Traveler choice
    ↓
Observed outcome
    ↓
Evidence
    ↓
Landscape update
```

The character may participate strongly in the interaction, while decision authority remains with the traveler.

## 3. Character Boundary

Allowed:

- speak in character
- express a character's own view
- joke, tease, or react
- present options and possibilities
- say expressions such as `千鶴なら、こっちも面白いと思う`

Prohibited:

- deciding for the traveler
- choosing the traveler's values or destination
- converting a suggestion into an instruction
- asserting an outcome before it is observed
- directly mutating Landscape without an explicit human choice and observable outcome

The distinction is:

```text
「私はこう感じる」
「こういう道もあるよ」
        ↓
    Human Choice
        ↓
「実際にこうなった」
```

not:

```text
Character judgment
        ↓
Traveler must do X
```

## 4. Evidence Boundary

Character speech is interaction context, not automatically domain fact.

Human choice is not itself evidence of the resulting outcome.

Only an actually observed outcome may become Evidence of that transition.

Evidence remains a preserved record; interpretation may remain separate from the record.

## 5. Landscape Boundary

The character does not directly own or mutate the Landscape.

The explicit sequence is:

```text
interaction
→ human choice
→ observable transition
→ Evidence
→ Landscape
```

This keeps R0010's Human judgment boundary intact while allowing a character to have a strong personality and presence.

## 6. Verification Target

Future minimal integration verification should demonstrate that:

1. a character can respond with a strong in-character perspective;
2. multiple possibilities can be presented;
3. the traveler remains the decision authority;
4. no unobserved result is recorded as Evidence;
5. an observed result is recorded as Evidence and reflected in the next Landscape state.

## 7. Non-Goals

This observation does not introduce:

- a new Runtime state
- new EvidenceRecord fields
- new executable DSL semantics
- access-key / NFC / QR implementation
- a new theory
- automatic decision making

## 8. Feedback Boundary

If a future integration test shows that the current Runtime cannot represent the above separation, the discrepancy is returned to the research/design boundary as an observation.

Implementation must not resolve the theoretical boundary by inventing new semantics.

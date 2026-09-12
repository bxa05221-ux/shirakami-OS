# Shirakami β1.0 — Launch Model

## 概要

Shirakami β1.0は、シェイクダウンを完了した実装基盤として、**Launch Model / Operational Rollout**へ移行する。

この文書は、理論完成や最終製品完成を宣言するものではない。これまでの実装・検証によって確認された基盤を実運用へ投入し、そこで発生するEvidenceを観測する段階への移行を宣言する。

> **β1.0は完成品ではない。走らせることのできる、検証済みのローンチモデルである。**

## 確認済みの実装境界

- Landscape → Evidence → Protocol → Runtime → Adapter → Backend
- Runtime / Evidence / Protocol / Adapter / Renderer continuity
- Evidence identity continuity
- State Machine continuity
- Adapter / Renderer exchange continuity
- Operation execution loop
- Operation ID / Execution ID separation
- Operation Result boundary
- Protected PR / Protected Merge path
- canonical verification: `test-runtime`

### Operation execution path

```text
Operation Definition
        ↓
Operation Plan
        ↓
Baseline
        ↓
Dedicated Branch
        ↓
Artifact
        ↓
Canonical Verification
        ↓
Protected PR
        ↓
Protected Merge
        ↓
Main Verification
        ↓
Operation Result
```

Operationと個々のExecutionは分離し、再実行によって過去のExecutionやArtifactを上書きしない。

## OperationResult境界

`OperationResult`は、**Executionの観測結果を保持するための薄い境界**である。

保持するもの:

- Operation ID
- Execution ID
- observed outcome

保持しないもの:

- 世界の最終結果
- Semantic Truth
- Domain Authority
- Humanの最終判断
- Evidenceの意味解釈

AutomationによってRuntimeの実行能力が増えても、意味解釈や判断権まで自動的に拡張しない。

## 安全境界

- **AI is simulator, not authority**
- 人間の最終判断はRuntimeの外側に残す
- LandscapeをRuntimeのSemantic Ownershipに置かない
- Runtimeは交換可能とする
- Adapterは交換可能とする
- Evidenceを保存する
- RuntimeがProtocol semanticsを勝手に発明しない
- Artifact mismatchを推測で修復しない
- 未確認・未解決の状態を推測によって確定状態へ変換しない

## i-field

i-fieldは現時点では**provisional**として扱う。

```text
i
 ↓
Observable Evidence
 ↓
resolved state
 ↓
next state / next i
```

`i`は回答そのものではない。resolveにはObservable Evidenceを要求し、Runtime自身が意味を推論して解決することはしない。

i-fieldの理論的性質は研究課題として保持し、本Launch Modelでは完成を宣言しない。

## このLaunch Modelで宣言しないもの

- 理論完成
- 最終製品完成
- Universal AI Control
- Autonomous Authority
- i-field theory completion
- 無制限の自動化
- 人間の判断の代替

また、実装上の都合によって既存理論やProtocol semanticsを勝手に変更・拡張しない。

## Operational Rollout

ローンチ後の問いは、

```text
「これを作れるか？」
```

から、

```text
「実装された境界は、実運用でも宣言どおりに振る舞うか？」
```

へ移る。

実運用で発生したEvidenceを観測・保存し、理論的な問題が発見された場合は研究側へ返す。

実装側では引き続きAPI、State Machine、Plugin、Memory Manager、UI/UX、Verification、Real Operationを優先する。

## Launchの定義

Launchは完成を意味しない。

> **検証された実装境界を、実運用へ投入できる状態になったこと。**

強いシステムとは、どこまでも壊れないシステムではない。

**壊れる場所と、判断を止める場所を設計できるシステムである。**

## Declaration

> **Shirakami β1.0は、シェイクダウンを完了した実装基盤として、Launch Modelへ移行する。**

ここからは、

**作る。  
走らせる。  
観測する。  
壊れる。  
検証する。**

そして、実運用から本当に生まれた問いだけを研究側へ返す。

---

# English

## Summary

Shirakami β1.0 has completed its shakedown phase and is moving into **Launch Model / Operational Rollout**.

This does **not** declare theory completion or final product completion. It declares that the verified implementation baseline is ready to be operated, observed, and iteratively improved while preserving its established boundaries.

> **β1.0 is not a finished product. It is a verified launch model that is ready to run.**

## Verified boundaries

- Landscape → Evidence → Protocol → Runtime → Adapter → Backend
- Runtime / Evidence / Protocol / Adapter / Renderer continuity
- Evidence identity continuity
- State Machine continuity
- Adapter / Renderer exchange continuity
- Operation execution loop
- Operation ID / Execution ID separation
- Operation Result boundary
- Protected PR / Protected Merge path
- canonical verification: `test-runtime`

## OperationResult boundary

`OperationResult` is intentionally a thin **execution-observation boundary**. It records execution identity and observed outcome, but does not represent semantic truth, world finality, domain authority, or human judgment.

Automation must not expand the semantic authority of the Runtime.

## Safety boundaries

- AI is simulator, not authority.
- Human final judgment remains outside the Runtime.
- Landscape remains outside Runtime semantic ownership.
- Runtime remains replaceable.
- Adapters remain exchangeable.
- Evidence is preserved.
- Protocol semantics are not invented by Runtime.
- Artifact mismatch is not silently repaired.
- Unknown or unresolved states are not converted into fabricated certainty.

## i-field

The i-field remains **provisional**. Resolution requires Observable Evidence and does not permit the Runtime to invent semantic meaning. Its theoretical status remains a research question.

## What this launch does NOT declare

- theory completion
- final product completion
- universal AI control
- autonomous authority
- i-field theory completion
- unrestricted automation
- replacement of human judgment

## Operational rollout

After launch, the development question changes from **"Can we build it?"** to **"Does the implemented boundary continue to behave as declared under real operation?"**

Operational Evidence will be observed and preserved. The implementation will prioritize API, State Machine, Plugin, Memory Manager, UI/UX, Verification, and Real Operation. The underlying theory will not be silently expanded to accommodate implementation convenience.

## Launch definition

Launch means:

> **The verified implementation boundary is ready to be operated in the real world while failures, unknowns, and decision boundaries remain observable.**

A strong system is not one that never breaks. It is one that can define where it may break and where human judgment must remain.

## Declaration

> **Shirakami β1.0 has completed shakedown and is moving into Launch Model / Operational Rollout.**

**Build. Run. Observe. Break. Verify.**

Return only the questions that actually emerge from operation to the research side.
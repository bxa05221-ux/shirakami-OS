# Shirakami Verification Protocol v1.0

## Purpose

本書は、白神モデル／Shirakami OSの主張・実装・運用上の境界を、印象ではなく再現可能な検証によって確認するための基準文書である。PASSだけでなく、PARTIAL、FAIL、NOT_RUNも記録する。

## Principles

- 一変更一検証（局所検証）
- 俯瞰検証（周辺構造・契約・CIへの影響確認）
- 主張よりEvidenceを先に置く
- Green CIを設計目的や安全性の証明とみなさない
- 人間が最終判断を行う
- 不成立・未検証・再現不能も結果として保存する

## Verification Scope

### V-01 Reproducibility

Quickstart、依存関係、対応Python、期待出力、失敗時の切り分けが第三者環境で再現できるか。

### V-02 Protocol Loading and IR

Matome YAMLの正常入力、必須項目欠落、型不一致、未知フィールド、空入力、不正YAML/JSONを検証し、入力からProtocol IRへの変換とエラー情報を記録する。

### V-03 Runtime State Transition

初期状態、実行前後の差分、成功・失敗時のTransition、再実行、同一入力に対する決定性を確認する。状態が変化したことと、変化が正しいことは別々に判定する。

### V-04 Evidence Integrity

Evidenceの識別子、発生元Transition、順序、immutable性、改変時の新規Evidence生成、事実・解釈・推定の区別を確認する。LLM出力をそのまま事実として登録しない。

### V-05 Landscape Continuity

Runtime／Backendの差し替えを想定し、Landscape Stateの意味、識別性、Evidenceとの参照関係、Backend固有情報の分離、欠損・重複・競合時の挙動を確認する。設計検証と実装検証を分離して記録する。

### V-06 Adapter Boundary

Adapterの責務、Runtimeとの契約、Backendエラーの伝播、Backend未接続時の挙動、モックAdapterによる独立テストを確認する。

### V-07 Safety and Adversarial Inputs

巨大入力、深いネスト、不正型、予期しない命令、Evidence改変、権限外操作、失敗時の情報漏えいを確認する。PASSしても全面的な安全性は保証しない。

## Test Record Format

```yaml
verification_id: V-XX
subject: "検証対象"
version: "PV1.0"
date: "YYYY-MM-DD"
environment:
  os: ""
  python: ""
  commit: ""
input:
  fixture: ""
expected:
  - "期待結果"
observed:
  - "観測結果"
status: PASS | PARTIAL | FAIL | NOT_RUN
limitations:
  - "未検証範囲"
evidence:
  - "ログ・テスト・差分等"
reviewer: ""
```

## Release Gate

完了条件は全項目PASSではなく、対象範囲、実行結果または未実行理由、FAIL/PARTIAL/NOT_RUN、環境とcommit、未検証領域、検証結果と解釈の分離、人間による最終レビューが記録されていることである。

## Non-Goals

本書は、世界初、既存技術より優れていること、ハルシネーションの完全防止、全面的な安全性、新規性・特許性、市場性・収益性を証明しない。必要に応じて別個の比較研究・安全性評価・市場検証・知財調査として扱う。

## Initial Execution Order

1. V-01 Reproducibility
2. V-02 Protocol Loading and IR
3. V-03 Runtime State Transition
4. V-04 Evidence Integrity
5. V-06 Adapter Boundary
6. V-05 Landscape Continuity
7. V-07 Safety and Adversarial Inputs
8. 全体の俯瞰検証

## Status

- Document: Verification Protocol v1.0
- Scope: PV1.0 / β1.0 Operational Rollout
- Current status: Protocol defined; execution records pending
- 本書は、列挙した検証が既にPASSしたことを主張しない。

# Shirakami 検証スコープ・プロトコル v0.1

Status: operational

## 中核原則

局所を確かめ、全体を俯瞰する。

- 一変更一検証
- 節目ごとに俯瞰検証

## 二層検証

### Local Change Verification

変更単位で、目的・既存機能・意味付与・該当テスト・必要なCIを確認する。

### Whole-System Consistency

節目ごとに、全体の構造、責務境界、検証体系、状態境界を確認する。

## 構造

Landscape → Evidence → Protocol → Runtime → Adapter → Backend

必要に応じて Landscape → Runtime → Renderer も確認する。

## 境界

- 観測 ≠ 解釈
- 候補 ≠ 確定
- Evidence ≠ 意味
- Runtime ≠ Authority

## 判定

- Local Verified: 個別変更の検証成功
- Whole-System Consistent: 全体構造・責務・検証体系との整合確認
- Verified: 必要な局所検証と、必要な場合の俯瞰検証が完了

局所テスト成功だけでは、全体についてVerifiedとは宣言しない。

## 主要トリガー

複数変更の一区切り、Protocol統合、CI/Workflow変更、Model existence control等の検証体系変更、新しいRuntime境界追加、ブランチ統合、リリース/Launch Model等の節目、責務境界の不整合が疑われた場合。

## 禁止事項

- 局所テスト成功だけで全体整合を推測しない
- 俯瞰検証を理由に既存理論を勝手に変更しない
- 不整合を推測で修正しない
- 検証されていない状態をVerifiedと呼ばない
- 新しい理論的意味を実装側で追加しない

## 運用フロー

変更 → 局所検証 → 成功確認 → 節目判定 → 俯瞰検証 → 全体整合確認 → Verified

節目でない場合は次の変更へ進む。

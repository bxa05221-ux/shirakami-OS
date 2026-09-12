# 開発者向け

ここから先は、白神を実装・検証する人向けです。

## 主な構成

- `Landscape` — 文脈
- `Evidence` — 観測・実行の記録
- `Protocol` — ルール
- `Runtime` — 実行
- `Adapter` — 外部システムとの接続境界
- `Renderer` — 表示境界

## 実装を見るときの原則

### 1. 境界を確認する

どの処理がどの層に属するのかを確認します。

### 2. 実装と検証を分ける

コードが存在しても、Canonical Verificationで確認されているとは限りません。

### 3. 現在と過去を分ける

現在の実装と、過去の実験・記録を同一視しません。

### 4. 不一致を勝手に修正しない

Artifact mismatchなどの観測結果は、原因を確認せずに「正しい状態」へ書き換えません。

## さらに詳しく

- [MVP Quickstart](../architecture/MVP_QUICKSTART.md)
- [Reviewer Entry Point](../architecture/REVIEWER_ENTRY_POINT.md)
- [Launch Model Protocol](../protocols/SHIRAKAMI_MODEL_LAUNCH_PROTOCOL_v1.0.yaml)

このページは実装案内です。理論そのものを変更・拡張する場所ではありません。

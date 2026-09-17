# Input Boundary Contract v0.1

- Status: Architecture proposal
- Scope: Input boundary and semantic preservation
- Applies to: OPPAI / Protocol selection boundary

## 1. Purpose

この文書は、ユーザー入力を受け取る境界において、原文の意味・順序・不確実性を保持し、入力の観察と実行制御を混同しないための設計制約を定める。

## 2. Core principles

1. `raw_input` はユーザーが記述した入力の原形として保持する。
2. 分割・分類・検査・警告は観察情報であり、原文の代替物ではない。
3. 観察処理は `raw_input`、Evidence、Runtime state を暗黙に書き換えてはならない。
4. OPPAI は明示的に観察できる情報を整理するが、隠れた意図・事実の確実性・心理診断を生成してはならない。
5. 実行可能な意味は Protocol と Runtime の明示的な契約によって決定する。
6. 未解決事項と不確実性は、解消されたものとして扱わず明示的に保持する。

## 3. Input flow

```text
Human Input
    ├── raw_input (preserved source)
    ├── observational analysis
    └── interaction / inspection signals
                ↓
              OPPAI
                ↓
             Protocol
                ↓
             Runtime
                ↓
       Observable Result / Evidence
```

## 4. Explicit exclusions

- 文字列統計や n-gram 分析を、白神モデルの必須中核機能とはしない。
- 入力を自動的に再構成・置換・削除して実行用プロンプトを生成しない。
- 観察結果だけを根拠として、入力を攻撃または危険と確定しない。
- 警告信号を、明示的な Protocol の命令と同一視しない。
- 入力境界で、ユーザーの判断や Runtime の実行権限を暗黙に代行しない。

## 5. Current OPPAI constraint

現行の OPPAI 実装では、分割や補助的な観察は観測目的に限定し、canonical prompt はユーザー入力の完全な系列を保持する。将来の変更でも、この原文保持の制約を破らないこと。

## 6. Verification checklist

- [ ] `raw_input` が保持される
- [ ] 観察処理が原文を変更しない
- [ ] 警告信号が Protocol 命令へ自動昇格しない
- [ ] 入力データと制御情報が境界で区別される
- [ ] 空入力・不正形式の扱いが明示される
- [ ] 日本語・Unicode・日本語句読点を検証する
- [ ] Evidence に観察結果と実行結果の区別が残る

## 7. Non-goal

この文書は、入力理解の性能向上やプロンプトインジェクション検出性能を証明するものではない。境界で守るべき不変条件を明確化するための設計文書である。

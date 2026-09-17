# Shirakami OS Repository Map

**白神OSを初めて訪れる人のためのRepository案内**

この文書は、Repositoryの内部構造を説明するだけではなく、**「何を見たい人が、どこから入ればよいか」**を示すためのNavigation Layerです。

---

## 1. まず、何をしたいですか？

### 白神OSが何なのか知りたい

→ [`README.ja.md`](../../README.ja.md)

白神OSの目的、基本原則、現在の状態を確認してください。

### Architectureを理解したい

→ [`REVIEWER_ENTRY_POINT.md`](REVIEWER_ENTRY_POINT.md)

Landscape / Evidence / Protocol / Runtime / Adapter / Backend の関係を、レビュー向けの読み順で確認できます。

### とにかく動かしたい

→ [`MVP_QUICKSTART.md`](MVP_QUICKSTART.md)

最小Runtimeを実行し、テストによって現在のPrototypeを確認します。

### Protocolがどう動くのか知りたい

→ `docs/architecture/` → Protocol関連文書

ProtocolはPromptそのものではなく、Runtimeが扱う外部化された処理定義として整理されています。

### Runtimeの実装を見たい

→ [`runtime/`](../../runtime/)

Protocol Loader、Runtime、Evidence、Stateなど、実装側の構造を確認してください。

### APIを見たい

→ [`api/`](../../api/)

公開・実験中のAPI関連実装を確認してください。

### 個別アプリケーションを見たい

→ [`apps/`](../../apps/)

Shirakami Runtimeを利用するアプリケーション領域です。

### CI・検証の仕組みを見たい

→ [`ci/`](../../ci/) と [`.github/`](../../.github/)

自動テスト、CI、Repository運用に関する設定があります。

### コントリビューション方法を知りたい

→ [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

変更を加える前に確認してください。

---

## 2. Repository全体の見取り図

```text
shirakami-OS/
│
├─ README.md / README.ja.md       ← 最初の入口
│
├─ docs/
│  └─ architecture/               ← Architecture / Reviewer / Quickstart
│
├─ runtime/                       ← Runtime実装
├─ api/                            ← API
├─ apps/                           ← Applications
├─ ci/                             ← 検証・CI関連
├─ .github/                       ← GitHub運用・CI設定
├─ community/                     ← Community関連
│
├─ tests / runtime tests          ← 実装検証
├─ CHECKLIST.md                   ← 検証・確認項目
├─ CONTRIBUTING.md                ← 開発参加方法
└─ Glossary.md                    ← 用語
```

※ Repositoryのディレクトリ構造は実装の履歴と進行に伴って変化します。このMapは「現在の構造を固定する仕様」ではなく、**訪問者が現在地を把握するための案内**です。

---

## 3. 白神OSを読む基本順序

初めての場合は、次の順番を推奨します。

```text
01  README
     ↓
02  Reviewer Entry Point
     ↓
03  Architecture
     ↓
04  MVP Quickstart
     ↓
05  Runtime
     ↓
06  Tests / CI
     ↓
07  API / Applications
```

### なぜこの順番なのか

白神OSでは、実装だけを先に読むと個々のコードの意味を取り違える可能性があります。

先にArchitecture上の境界を確認し、その後にRuntimeと検証を見ることで、

> **「このコードは白神OSのどの境界を実装しているのか」**

を追跡できます。

---

## 4. 三つの入口

| 目的 | 入口 | 所要時間の目安 |
|---|---|---:|
| 概要を知る | README | 2–5分 |
| 構造をレビューする | Reviewer Entry Point | 5–15分 |
| 実際に動かす | MVP Quickstart | 約5分 |

この3つを用意することで、**「読む」「理解する」「動かす」**の3つの訪問経路を分離します。

---

## 5. 重要な境界

白神OSでは、次の境界を意識してRepositoryを読んでください。

```text
Research / Meaning
        │
        │  semantic handoff
        ▼
    Protocol
        │
        ▼
     Runtime
        │
        ▼
    Evidence
        │
        ▼
 Adapter / Backend
```

Repository内のすべてのディレクトリが同じ意味を持つわけではありません。

- **意味・理論**を読む → Architecture / Protocol / Specification
- **実装**を見る → Runtime / API
- **利用例**を見る → Applications
- **検証**を見る → Tests / CI / Evidence関連
- **開発ルール**を見る → CONTRIBUTING / CHECKLIST / `.github/`

---

## 6. 迷ったら

迷った場合は、コードを適当に探し始める前に、次の3つへ戻ってください。

1. [`README.ja.md`](../../README.ja.md)
2. [`REVIEWER_ENTRY_POINT.md`](REVIEWER_ENTRY_POINT.md)
3. [`MVP_QUICKSTART.md`](MVP_QUICKSTART.md)

白神OSは、**RepositoryそのものをLandscapeの一部として扱います。**

したがって、Repositoryを訪れた人が「今どこにいて、次に何を見ればよいか」を把握できることも、Architectureの可観測性の一部です。

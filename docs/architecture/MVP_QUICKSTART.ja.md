# Shirakami OS — MVP クイックスタート

初めてRepositoryを見る人が、現在のRuntime境界を実際に実行・確認するための最短ルートです。

> **現在のQuickstartは、外部AIプロバイダを必要としません。**
> Matome YAMLからProtocol IRを生成し、Runtime、Evidence、Landscape Stateまでをローカルで確認します。

## 1. 前提

- Python 3.11+
- Git

```bash
git clone https://github.com/bxa05221-ux/shirakami-OS.git
cd shirakami-OS
```

## 2. Quickstartを実行

```bash
python examples/quickstart/run.py
```

このスクリプトは、Quickstart用のProtocol YAMLを読み込み、Runtimeを実行します。

```text
Matome YAML
    ↓
Protocol IR
    ↓
Protocol Bridge
    ↓
Runtime
    ↓
Transition
    ↓
Evidence
    ↓
Landscape State
```

最後に `SUCCESS` が表示されれば、現在のMVP実行経路が完了しています。

## 3. 何を確認できるか

Quickstartでは、外部AIを呼び出す前の白神OSの最小実行境界を確認できます。

1. **Protocol** — 的目YAMLを読み込む
2. **Runtime** — Protocolを実行する
3. **Evidence** — 実行結果から状態変化を観測する
4. **Landscape State** — Evidenceを適用した状態を確認する

現在のQuickstartは、AIそのものを実行するデモではありません。Backend固有のAI処理をRuntime Coreから切り離し、まずRuntime境界そのものを検証可能にしています。

## 4. テストを実行

```bash
python -m pytest runtime tests -q
```

テストが成功すれば、Runtime経路とその回帰テストを確認できます。

## 5. 次に見る場所

- `examples/quickstart/run.py` — 実際に実行するQuickstart
- `examples/quickstart/protocol.yaml` — Quickstartで読み込むProtocol
- `runtime/` — Runtime実装
- `tests/` — 実行可能な契約・回帰テスト
- `protocols/` — Protocolのソースアーティファクト
- `docs/architecture/REVIEWER_ENTRY_POINT.md` — ArchitectureとEvidenceのレビュー入口

## 6. 現在のMVPの境界

```text
Landscape / Context
        ↓
     Protocol
        ↓
      Runtime
        ↓
     Evidence
        ↓
  Landscape State
```

外部AIプロバイダの呼び出しは、このMVPの必須条件ではありません。AI Backendとの接続はAdapter境界の外側に置き、Runtime Coreが特定のAIベンダーへ依存しない構造を維持します。

## MVP status

MVPは**完成した製品ではなく、実装可能性を検証するための最小実装**です。

現在確認できる範囲と未完成部分を分けてレビューできるようにすることを、このQuickstartの目的としています。

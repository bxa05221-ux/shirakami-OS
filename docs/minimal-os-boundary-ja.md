# 白神OS 最小実行境界 α0.1

## 目的

「白神OSはどこにあるのか？」という問いに対して、概念や設計資料ではなく、実際に起動できる最小実体を示す。

現在の最小入口はリポジトリ直下の `shirakami_os.py` である。

## 最小実行経路

```text
Landscape
  ↓
Protocol
  ↓
Runtime
  ↓
Transition
  ↓
Evidence
  ↓
Landscape
  ↓
Result
```

`ShirakamiOS.boot()` が初期Landscapeを受け取り、`ShirakamiOS.execute()` がProtocolをRuntimeで実行する。実行結果からEvidenceを生成し、観測可能なTransitionをLandscapeへ反映した上で、人間が確認できる `OSResult` を返す。

## Workspace 境界

OS の共有実行基盤と、ユーザー固有の Landscape は同一の所有物として扱わない。

```text
Shirakami OS
│
├── Runtime
├── Protocol Registry
├── Adapter Registry
│
└── Workspace
    ├── User A → Landscape A / Context A / Memory A
    ├── User B → Landscape B / Context B / Memory B
    └── User C → Landscape C / Context C / Memory C
```

Workspace 単位で Landscape を分離することを次段階の実装境界とする。詳細は `docs/workspace-landscape-boundary-ja.md` を参照する。

## これは何を意味するか

このファイルは新しい理論を定義しない。

また、白神OS全体が完成したことを主張するものでもない。

ここで固定するのは、**「OSとして実際に触れる最小の境界」**と、その次に検証する**「OSとUser Landscapeの所有境界」**だけである。

## 対象外

- 外部LLM Provider
- AWS / Supabase
- 認証・認可
- 永続DB
- 新しいProtocol理論
- 大規模なArchitecture変更

## レビュー対象

1. `shirakami_os.py` を最小OS入口として扱えるか。
2. 上記の実行経路をOSの最小Vertical Sliceとして扱えるか。
3. Workspace単位のLandscape分離を次の実装境界として扱えるか。

## 原則

> OSを説明するのではなく、起動できるものをOSの境界とする。

> Evidenceを集めること自体をOSの存在証明とせず、実行可能な境界から観測を開始する。

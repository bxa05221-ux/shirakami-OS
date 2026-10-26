# Workspace / User Landscape Boundary

## 目的

Shirakami OS は、OS と個々のユーザーの Landscape を同一の状態として扱わない。

OS は共有可能な実行基盤であり、Landscape は Workspace 単位で分離される人間側の状態である。

## 最小構造

```text
Shirakami OS
│
├── Runtime
├── Protocol Registry
├── Adapter Registry
│
└── Workspace
    ├── User A
    │   ├── Landscape A
    │   ├── Context A
    │   └── Memory A
    ├── User B
    │   ├── Landscape B
    │   ├── Context B
    │   └── Memory B
    └── User C
        ├── Landscape C
        ├── Context C
        └── Memory C
```

## 境界

- Runtime は実行機構であり、ユーザー固有の Landscape そのものではない。
- Landscape は Workspace に所属し、ユーザー間で暗黙に共有しない。
- Protocol は Runtime 上で実行されるが、入力される Context / Landscape は Workspace 境界を越えない。
- Adapter は外部サービスとの接続を担当し、ユーザー固有状態の所有者にはならない。
- Model は Landscape の所有者ではない。Model を交換しても Workspace の Landscape を失わない構造を目標とする。

## 現段階での扱い

これはマルチユーザー機能を完成させる仕様ではない。

PR #14 で確立した最小 OS 実行境界の次に、OS と User Landscape の所有境界を検証するための設計基準として置く。

## 対象外

- 認証・認可の実装
- 永続 DB の選定
- クラウド基盤の導入
- Model Provider の追加
- 新しい Protocol の設計

## Review Question

> Shirakami OS を共有基盤として動かしながら、各ユーザーの Landscape / Context / Memory を Workspace 単位で分離する境界として、この構造を採用できるか。

## English Summary

Shirakami OS separates the shared execution substrate from user-owned Landscape state.

Runtime, Protocol Registry, and Adapter Registry belong to the OS boundary, while Landscape, Context, and Memory belong to an isolated Workspace.

This document is a design boundary for the next implementation step; it does not claim complete multi-user, authentication, persistence, or cloud support.

# Matome API

Status: experimental / contract draft

このディレクトリは、白神モデル v3.2 の的目YAML循環を外部APIとして扱うための契約検討場所です。

## 重要な位置づけ

このAPIはShirakami OSそのものではありません。

```text
Landscape
  ↓
Protocol
  ↓
Runtime
  ↓
Matome API
  ↓
External Client / Adapter
```

APIはRuntimeの外部境界です。

現時点ではFastAPIなどのサーバー実装を含めず、OpenAPIを契約案として先に固定します。

## v3.2との対応

概念上は次の循環を扱います。

```text
Observe
  ↓
Compress
  ↓
Conference
  ↓
Optimize
  ↓
Return
  ↓
Observe again
```

ただし、`OSアーキテクト`、`教育者`、`研究者`などのThreadはv3.2の固定人格仕様ではありません。実装例で使用する観測視点にすぎません。

## 現在のRuntimeとの関係

Repositoryの最小実行境界は、現在次の形です。

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
Landscape State
  ↓
Result
```

API実装は、この境界を壊さずに外部から呼び出せるようにすることを目的とします。

## 次の検証

1. OpenAPI Contractと現在のRuntime境界を照合する
2. Protocol Registry / Protocol IDの扱いを確定する
3. Workspace境界をAPIに入れるか検証する
4. Evidenceの返却形式を確定する
5. その後にサーバー実装を検討する

**Contract first. Server later.**

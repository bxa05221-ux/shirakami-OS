# Shirakami Runtime（白神ランタイム）

**人間のLandscapeを中心に据えた、Protocol-driven Runtime基盤**

[English](README.md) | **日本語**

---

## 👋 初めて来た人へ

GitHubの構造を理解していなくても、白神を試せます。

まずは次の順番だけ見てください。

1. **[Shirakami Model Launch Protocol](docs/protocols/SHIRAKAMI_MODEL_LAUNCH_PROTOCOL_v1.0.yaml)** — 何をローンチするのか
2. **[白神ラジオ Language UI](examples/shirakami_radio_ui/)** — 人間向けの一番簡単な入口
3. **[MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)** — 実装を動かす
4. **[Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)** — 構造とEvidence境界を見る
5. **[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)** — 既存の公開サービスアーティファクト

### 一言でいうと

**白神は、AIが変わっても、人間が自分の文脈と判断を保てるかを試すプロジェクトです。**

AIは、Simulator・Observer・Hypothesis Generatorとして使います。
**最終的な決定権は人間に残します。**

---

## 現在の状態

**β1.0 → Launch Model → Operational Rollout**

β1.0のシェイクダウンで検証してきた境界を、実運用の観測へ移していく段階です。

ここでいうLaunchは「完成品になった」という意味ではありません。

**検証された境界を現実の運用へ投入し、観測し、Evidenceを蓄積し、必要に応じて更新すること**を意味します。

→ **[Shirakami Model Launch Protocol v1.0](docs/protocols/SHIRAKAMI_MODEL_LAUNCH_PROTOCOL_v1.0.yaml)**

---

## 白神とは

白神は、AIそのものを作るためのOSではありません。

人間のLandscape、Protocol、Evidence、判断を明示的に扱い、AIやBackendが変わっても文脈を引き継げるようにするRuntime / Interface architectureです。

```text
Landscape
    ↓
Evidence
    ↓
Protocol
    ↓
Runtime
    ↓
Adapter
    ↓
External AI / Backend
```

RuntimeはDomain Truthを所有せず、Adapterによって外部AIやBackendから分離されます。

---

## 人間向けの入口：白神ラジオ

### **[白神ラジオ Language UIを開く](examples/shirakami_radio_ui/)**

白神ラジオは、白神を「読む」のではなく、まず会話として体験するための最小UIです。

現在のMVPは意図的に小さくしています。

- ブラウザベース
- 日本語会話UI
- Demo mode
- 任意のRuntime endpoint
- 静的UI自体にはアカウント不要
- 外部AIがデフォルトで接続されているとは宣言しない

**UIはRuntimeそのものではありません。**

最初のローンチでは音声を必須にしません。音声UIは別Versionで追加できる境界として残します。

---

## アーキテクチャ

```text
Human
  ↓
Shirakami Radio / UI
  ↓
Language UI Adapter
  ↓
Protocol
  ↓
Runtime
  ↓
AI / Backend Adapter
  ↓
External AI / Service
  ↓
Response
  ↓
Renderer / UI
  ↓
Human
```

AIが交換されても、人間のLandscapeと、その周囲の境界を持ち運べることを目指します。

---

## 基本原則

- **Human final authority** — AIに最終決定権を移さない
- **Landscape First** — 人間の文脈をAIより上位の中心資産として扱う
- **Hypotheses remain provisional** — 意図・感情・人格などの推測を事実化しない
- **Uncertainty is preserved** — 未理解を勝手に埋めない
- **Contradictions are signals** — 否定や修正を更新信号として扱う
- **Evidence is preserved** — 観測された履歴を勝手に書き換えない
- **Runtime is replaceable** — 特定AIベンダーへの固定を避ける
- **One change, one verification** — 変更は小さく入れて検証する

---

## ローンチ後も観測する

白神の認知サイクルは次のように置きます。

```text
Observe
  ↓
Hypothesis
  ↓
Dialogue
  ↓
Echo
  ↓
Update
  ↓
Consistency Check
  ↓
Observe
```

評価するのはAIの回答精度だけではありません。

- 認知エコー
- 矛盾
- 誤解
- 未理解
- プロトコル逸脱
- Runtime依存
- 人間による修正

を観測対象にします。

**Launch → Observe → Evidence → Refine → Verify → Next Version**

---

## 実装を動かす

最小Runtimeは次で実行できます。

```bash
git clone https://github.com/bxa05221-ux/shirakami-OS.git
cd shirakami-OS
python examples/quickstart/run.py
```

→ **[MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)**

---

## 公開サービスアーティファクト

現在の公開サービスアーティファクトは **[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)** です。

その他の実験的アーティファクトは、明示的に公開サービスとして指定されない限り、開発・研究用として扱います。

→ **[Service Artifact Index](products/)**

---

## レビューする人へ

実装やArchitectureを評価したい場合は、まずこちらから。

**[Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)**

このRepositoryでは、次のものを意図的に分離しています。

- 現在の実装
- Normative Specification
- Observation / Evidence
- Experiment
- Historical Artifact
- Research Question

**ファイルが存在すること自体は、その実験が成功したことや、Canonical Runtime pathに実装されたことを意味しません。**

---

## Repositoryの構成

- `spec/` — 実装側Specification
- `docs/` — Architecture、Protocol、Observation、参考文書
- `examples/` — 実行可能な例とUI Prototype
- `protocols/` — Protocol source artifacts
- `runtime/` — Runtime implementation
- `plugins/` — Plugin / Adapter
- `products/` — 公開サービスアーティファクト

---

## 関連Repository

- [shirakami-model](https://github.com/bxa05221-ux/shirakami-model) — Model / Vision
- [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification) — Specification
- [shirakami-research](https://github.com/bxa05221-ux/shirakami-research) — Research / 理論
- **shirakami-OS** — Runtime / Implementation

---

## License

Repositoryのライセンスについては、ルートの `LICENSE` および `LICENSE-SPECIFICATION.md` を参照してください。

---

## Contributing

質問、批判、実験、別アプローチを歓迎します。

修正やドキュメント変更は `fix/...` または `feat/...` ブランチからPRを作成してください。

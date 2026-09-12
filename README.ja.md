# Shirakami Runtime（白神ランタイム）

**人間のLandscape（文脈・景色）を中心に据えた、Protocol駆動のRuntime基盤**

[English](README.md) | **日本語**

---

## 👋 初めて来た人へ

GitHubの構造を理解していなくても、白神を試せます。

まずは次の順番だけ見てください。

1. **[白神モデル ローンチ・プロトコル](docs/protocols/SHIRAKAMI_MODEL_LAUNCH_PROTOCOL_v1.0.yaml)** — 白神は今、どこまでできている？
2. **[白神ラジオ 言語UI](examples/shirakami_radio_ui/)** — まず触ってみる
3. **[最小実装の導入・実行（MVPクイックスタート）](docs/architecture/MVP_QUICKSTART.md)** — 自分のパソコンで動かしてみる
4. **[白神を詳しく知る（Wiki）](docs/wiki/Home.ja.md)** — 白神の仕組みや考え方を読む
5. **[仕組みを詳しく見る（レビュー入口）](docs/architecture/REVIEWER_ENTRY_POINT.md)** — ArchitectureとEvidenceの境界を確認する
6. **[スレッドRPG v1.2.1](products/thread-rpg-v1.2.1/)** — 既存の公開サービスを見る

### AIで試す場合

**GPTでの確認を推奨しています。**

現在の白神の実装確認を行う場合は、まずGPTを使って試してください。

そして、**他のAIモデルで試した結果のレポートも歓迎します。**

モデルによって、同じProtocolや同じ入力からどのような違いが生じるのかを比較すること自体が、白神の観測になります。

- GPTで試した結果
- 他AIモデルで試した結果
- うまく動かなかった場合の結果
- GPTと他モデルで違った点
- 「白神の意図が伝わらなかった」と感じた点

などを、できるだけ元の状態を残したまま共有してください。

**外部AIの回答そのものを「正解」とは扱いません。**

AIによる観測は観測として記録し、必要に応じて白神側の実装・テスト・Evidenceで確認します。

### 一言でいうと

**白神は、AIが変わっても、人間が自分の文脈と判断を保てるかを試すプロジェクトです。**

AIは、シミュレーター・観測者・仮説生成器として使います。
**最終的な決定権は人間に残します。**

---

## 現在の状態

**β1.0 → ローンチモデル → 実運用展開**

β1.0のシェイクダウンで検証してきた境界を、実運用の観測へ移していく段階です。

ここでいうローンチは「完成品になった」という意味ではありません。

**検証された境界を現実の運用へ投入し、観測し、Evidence（観測記録）を蓄積し、必要に応じて更新すること**を意味します。

→ **[白神モデル ローンチ・プロトコル v1.0](docs/protocols/SHIRAKAMI_MODEL_LAUNCH_PROTOCOL_v1.0.yaml)**

---

## 白神とは

白神は、AIそのものを作るためのOSではありません。

人間のLandscape（文脈・景色）、Protocol（手順・規約）、Evidence（観測記録）、判断を明示的に扱い、AIやBackend（外部処理系）が変わっても文脈を引き継げるようにするRuntime / Interface基盤です。

```text
Landscape（人間の文脈）
    ↓
Evidence（観測記録）
    ↓
Protocol（手順・規約）
    ↓
Runtime（実行層）
    ↓
Adapter（接続境界）
    ↓
外部AI / Backend（外部処理系）
```

RuntimeはDomain Truth（領域上の真実）を所有せず、Adapterによって外部AIやBackendから分離されます。

---

## 人間向けの入口：白神ラジオ

### **[白神ラジオ 言語UIを開く](examples/shirakami_radio_ui/)**

白神ラジオは、白神を「読む」のではなく、まず会話として体験するための最小UIです。

現在のMVP（最小実装）は意図的に小さくしています。

- ブラウザで動作
- 日本語の会話UI
- デモモード
- 任意のRuntime接続先を指定可能
- 静的UI自体にはアカウント不要
- 外部AIが標準で接続されているとは宣言しない

**UIはRuntimeそのものではありません。**

最初のローンチでは音声を必須にしません。音声UIは別Version（次の版）で追加できる境界として残します。

---

## 白神を詳しく知る

GitHubや技術用語に慣れていない人は、ここから読めます。

→ **[白神を詳しく知る（Wiki）](docs/wiki/Home.ja.md)**

Wikiでは、白神とは何か、まず何を試せばよいか、どんな仕組みなのか、開発・検証がどう行われているかを、READMEより詳しく説明しています。

---

## 全体の流れ

```text
人間
  ↓
白神ラジオ / UI
  ↓
言語UI Adapter（接続層）
  ↓
Protocol（手順・規約）
  ↓
Runtime（実行層）
  ↓
AI / Backend Adapter（外部接続層）
  ↓
外部AI / サービス
  ↓
応答
  ↓
Renderer / UI（表示層）
  ↓
人間
```

AIが交換されても、人間のLandscapeと、その周囲の境界を持ち運べることを目指します。

---

## 基本原則

- **人間が最終決定者** — AIに最終決定権を移さない
- **Landscape First（文脈を第一に）** — 人間の文脈をAIより上位の中心資産として扱う
- **仮説は暫定のまま** — 意図・感情・人格などの推測を事実化しない
- **不確実性を保存する** — 未理解を勝手に埋めない
- **矛盾を更新信号として扱う** — 否定や修正を更新の手がかりにする
- **Evidenceを保存する** — 観測された履歴を勝手に書き換えない
- **Runtimeを交換可能にする** — 特定AIベンダーへの固定を避ける
- **一つ変更したら一つ検証する** — 変更は小さく入れて検証する

---

## ローンチ後も観測する

白神の認知サイクルは次のように置きます。

```text
観測
  ↓
仮説
  ↓
対話
  ↓
反響
  ↓
更新
  ↓
整合性確認
  ↓
観測
```

評価するのはAIの回答精度だけではありません。

- 認知エコー
- 矛盾
- 誤解
- 未理解
- Protocolからの逸脱
- Runtimeへの依存
- 人間による修正

を観測対象にします。

**ローンチ → 観測 → Evidence → 改良 → 検証 → 次の版**

---

## 最小実装を導入して動かす

白神を実際に動かしてみたい場合は、以下が最小手順です。

### 1. リポジトリを取得する

```bash
git clone https://github.com/bxa05221-ux/shirakami-OS.git
cd shirakami-OS
```

### 2. 最小実装を起動する

```bash
python examples/quickstart/run.py
```

### 3. 詳しい導入手順を見る

→ **[まず動かす：最小実装の導入・実行ガイド](docs/architecture/MVP_QUICKSTART.md)**

ここでいう「MVP」は、完成した製品版ではなく、白神のRuntimeを最小構成で試すための実装を指します。

---

## 公開サービス・アーティファクト

現在の公開サービス・アーティファクトは **[スレッドRPG v1.2.1](products/thread-rpg-v1.2.1/)** です。

その他の実験的アーティファクトは、明示的に公開サービスとして指定されない限り、開発・研究用として扱います。

→ **[公開サービス・アーティファクト一覧](products/)**

---

## 仕組みを詳しく見たい人へ

実装やArchitecture（構造）を評価したい場合は、こちらから。

→ **[仕組みを詳しく見る（レビュー入口）](docs/architecture/REVIEWER_ENTRY_POINT.md)**

このRepositoryでは、次のものを意図的に分離しています。

- 現在の実装
- 規範仕様
- Observation / Evidence（観測・証拠記録）
- Experiment（実験）
- Historical Artifact（過去のアーティファクト）
- Research Question（研究上の問い）

**ファイルが存在すること自体は、その実験が成功したことや、正規のRuntime経路に実装されたことを意味しません。**

---

## リポジトリの構成

- `spec/` — 実装側の仕様
- `docs/` — 構造、Protocol、観測、参考文書
- `examples/` — 実行可能な例とUI試作
- `protocols/` — Protocolの原資料
- `runtime/` — Runtime実装
- `plugins/` — Plugin / Adapter
- `products/` — 公開サービス・アーティファクト

---

## 関連リポジトリ

- [shirakami-model](https://github.com/bxa05221-ux/shirakami-model) — 白神モデル／ビジョン
- [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification) — 仕様
- [shirakami-research](https://github.com/bxa05221-ux/shirakami-research) — 研究／理論
- **shirakami-OS** — Runtime／実装

---

## ライセンス

リポジトリのライセンスについては、ルートの `LICENSE` および `LICENSE-SPECIFICATION.md` を参照してください。

---

## 参加・提案について

質問、批判、実験、別アプローチを歓迎します。

修正やドキュメント変更は `fix/...` または `feat/...` ブランチからPRを作成してください。

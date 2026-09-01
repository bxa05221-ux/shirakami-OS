# Shirakami OS（白神OS）

**人間のLandscapeを中心に据えた、Protocol-driven Runtime基盤**

[English](README.md) | **日本語**

---

## 白神OSとは

白神OSは、AIそのものを作るためのOSではありません。

AIが変わっても、人間がAIとともに積み上げてきた文脈、知識、判断、履歴などの**Landscape（景色）**を維持し、再利用できるようにするためのRuntime基盤です。

白神OSでは、AIを中心に置きません。

```text
Landscape
    ↓
Protocol
    ↓
Runtime
    ↓
Evidence
    ↓
Adapter
    ↓
Backend
```

Landscapeが中心であり、RuntimeはLandscapeを扱うための交換可能な実行層です。

---

## 外部レビューの入口

初めて見る場合は、まず以下から入ってください。

- **[Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)** — ArchitectureとEvidenceを確認するための読み順
- **[MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)** — 最短で実装を実行・検証する入口

最短ルート：

**Landscape → Evidence → Protocol → Runtime → Adapter → Execution → Observation**

---

## 誤解を防ぐために

白神OSは、次のものを目的としていません。

- ChatGPTなど特定AIの代替
- 新しいLLMそのものの開発
- 特定AIベンダーに固定されたアプリケーション
- 研究ノートを保存するだけのRepository

白神OSは、AIを人間のようにすることも目的としません。

むしろ、AIを使っていく中で人間側から明確になってきた、AIの「使える部分」と「使えない部分」の両方を前提にします。

AIには、圧倒的な計算・生成・情報処理能力があります。一方で、人間が当然のように扱う時間・空間・身体・経験・関係・文脈などを、そのまま人間と同じ形で持っているわけではありません。

白神モデルは、この能力差をAI自身に人間化させて埋めるのではなく、UI・Protocol・Landscape・Runtimeによって接続し、人間にとって利用可能な形へ変換することを目指します。

---

## 出発点

白神の出発点は「AI用OSを作る」ことではありませんでした。

もともとは、AIを「サーバールームに引きこもった中二病」と捉え、そのAIが人間の世界に参加できるようにするためのUIを作る、という発想から始まっています。

認知観測をテーマとしたプロトコルを積み上げ、的目YAMLによってThread、Matagi AI、Matagi Sessionなどを扱えるようになった時点で、すでにAIそのものではなく、AIを取り巻く状態・文脈・Protocol・UI・Sessionを扱うためのOS的な必要条件が形成されていました。

そこからボトムアップに構造が拡張され、Landscape、Evidence、Runtime、Adapterへと接続されて現在のShirakami OSに至っています。

---

## 基本原則

- **Landscape First** — Landscapeを恒久的な中心資産として扱う
- **Protocol First** — 振る舞いをProtocolとして定義する
- **Human Context First** — AIではなく人間側の文脈を中心に置く
- **Backend Independence** — 特定のBackendにRuntimeを依存させない
- **Observable Evidence** — 状態変化をEvidenceとして記録する
- **Runtime Replaceability** — Runtime自体を交換可能なものとして扱う

白神OSのFoundationでは、LLMは交換可能であり、Landscapeが残ることを基本的な設計原則としています。

---

## 認知観測

白神OSの重要な研究系譜には、次の認知観測系があります。

- **天球モデル** — Cognitive Space
- **3D位相回転アイゼンハワーマトリクス** — Cognitive Position / Phase Rotation
- **認知エコーロケーション** — Cognitive Observation
- **暗問層** — Unresolved Questions
- **AASS** — Operational Connection

これらは、Landscapeを単にMemoryとして保存するのではなく、認知位置の変化と観測可能性の変化を扱うための研究・実験系です。

---

## 開発の系譜

```text
AIのためのUI
      ↓
認知観測プロトコル
      ↓
的目YAML
      ↓
Thread / Matagi AI / Matagi Session
      ↓
AA Thread Simulator Lite
      ↓
Thread RPG
      ↓
認知観測
      ↓
Landscape / Evidence / Protocol
      ↓
Runtime / Adapter
      ↓
Shirakami OS
```

この系譜は、最初にOSを設計して後から機能を追加したものではありません。小さなUI・Protocol・観測実験をボトムアップに積み上げた結果として、Runtime architectureが明確になってきたものです。

---

## Protocolとは

白神OSでは、AIへの指示や処理手順を、その場限りのPromptだけで管理するのではなく、**Protocol**として外部化します。

Protocolは現在、主に**的目YAML（Matome YAML）**を実行可能な入力形式として扱う方向で実装しています。

現在のRuntime Prototypeでは、

```text
Matome YAML
    ↓
Protocol Loader
    ↓
Protocol IR
    ↓
Runtime
    ↓
Evidence
    ↓
Landscape State
```

という最小の実行経路を検証しています。

> 注意：現在のProtocol Loaderはβ0.1の最小Matome YAML subsetを対象としています。完全なProtocol仕様・完全なYAML実行系ではありません。

---

## Runtime

RuntimeはAIそのものではありません。

Protocolを受け取り、実行し、Observableな状態変化をTransitionとして扱い、その結果からEvidenceを記録し、Landscape Stateを更新します。

Backend固有の処理はAdapter境界の外側に置くことを目指しています。

現在はGitHubを最初のBackend / Landscapeとして実装・検証しています。

---

## Evidence

白神OSでは、AIやRuntimeの出力を直接Landscapeの事実として扱うのではなく、実行時のTransitionからEvidenceを生成する境界を設けています。

Evidenceは、何が起きたかを後から追跡できるようにするための記録です。

現在のPrototypeではEvidence Recordをimmutableな構造として扱っています。

---

## 現在の状態

**Public Alpha / Runtime β0.1 preparation**

現在確認できている範囲：

- Foundation Architecture
- Runtime Prototype
- Evidence境界
- Landscape State
- Matome YAML Loaderの最小実装
- Protocol IR
- GitHub Adapter / Backend境界
- Quickstart
- 自動テスト / CI

現在進行中：

- Protocol仕様の正式化
- Protocol semanticsの実装
- Quickstartの入力経路強化
- CI対象の拡張
- Runtime API α0.1
- Adapter Contractの整理

まだ完成した製品ではありません。

このRepositoryは、Architectureを実装で検証しながら公開している開発段階のプロジェクトです。

---

## 5分Quickstart

Repositoryを取得して、最小Runtimeを実行できます。

```bash
git clone https://github.com/bxa05221-ux/shirakami-OS.git
cd shirakami-OS
python examples/quickstart/run.py
```

Quickstartでは、Protocol YAMLを読み込み、Protocol IRを生成し、Runtimeを実行してEvidenceとLandscape Stateを確認します。

→ **[MVP Quickstart](docs/architecture/MVP_QUICKSTART.md)**

---

## ユーザーズマニュアル（漫画版）

Public Alphaでは、**的目YAML → 漫画Renderer → SVG**という最小の文書生成経路を試しています。

- [漫画マニュアルの入口](docs/manual/)
- [日本語版SVG](docs/manual/manga-user-manual.ja.svg)
- [English版SVG](docs/manual/manga-user-manual.en.svg)
- [生成元の的目YAML](protocols/manual/manga-user-manual.yaml)
- [Rendering Contract α0.1](spec/manual-rendering.md)
- [漫画Renderer](runtime/manga_manual.py)

日本語と英語で言語を差し替えても、ページIDや説明構造は共通です。

これは現時点では、**漫画生成AIそのものを作るものではなく、Protocolで定義した説明構造を人間向けUIへRenderする実験的なAdapter**です。

---

## Repositoryの構成

白神OS単体だけでは、白神プロジェクト全体を説明しません。

現在、役割を分けてRepositoryを構成しています。

| Repository | 役割 |
|---|---|
| [shirakami-model](https://github.com/bxa05221-ux/shirakami-model) | 白神モデル全体のVision / Model |
| [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification) | 仕様・Specification |
| [shirakami-research](https://github.com/bxa05221-ux/shirakami-research) | Research / 理論・研究 |
| **shirakami-OS** | Foundation / Runtime / Implementation |

つまり、概念・研究・仕様・実装を一つのRepositoryに混ぜるのではなく、それぞれのLandscapeを分離しています。

---

## 開発方針

白神OSでは、Foundationを先に定義し、その後にRuntimeを実装します。

また、実装中にFoundationそのものを勝手に変更するのではなく、実装から見つかった問題をObservationとして記録し、必要に応じて研究・仕様側へフィードバックすることを重視します。

そのため、現在のコードには意図的にPrototype段階の部分があります。

---

## レビュー・参加

白神OSは、第三者によるレビューを歓迎します。

特に以下の観点からの意見を歓迎します。

- Architecture
- Runtime設計
- Protocol設計
- Adapter境界
- Evidence / Landscapeモデル
- API設計
- セキュリティ
- 実際に使ったときの分かりやすさ

「これは本当に必要なのか？」という批判も含め、実装とArchitectureの両方をレビューしてもらうことを想定しています。

---

## License

Repositoryのライセンスについては、ルートの `LICENSE` を参照してください。

---

## 関連リンク

- [Shirakami Model](https://github.com/bxa05221-ux/shirakami-model)
- [Shirakami Specification](https://github.com/bxa05221-ux/shirakami-specification)
- [Shirakami Research](https://github.com/bxa05221-ux/shirakami-research)
- [Shirakami OS](https://github.com/bxa05221-ux/shirakami-OS)

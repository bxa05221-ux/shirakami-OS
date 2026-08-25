# Shirakami OS（白神OS）

> **白神OSは、AIそのものを作るOSではありません。**
> 人間のLandscapeを保持し、ProtocolをRuntimeで実行・観測し、AIやBackendが変わっても文脈を引き継ぐための基盤です。

[English](README.md) | **日本語**

---

## 30秒でわかる：何ができる？

白神OSは、人間の **Landscape（景色）** と交換可能なAI / Backendの間に入る、Protocol-driven Runtime基盤です。

現在の実装で扱っている主な機能は次のとおりです。

- **ProtocolをRuntime / API境界から実行する**
- **的目YAML（Matome YAML）**をProtocolや圧縮文脈の中間表現として扱う
- Observableな状態変化を**Evidence**として記録する
- AIモデルとLandscape Stateを分離する
- **Adapter / Plugin**を介して外部システムと接続する
- GitHub Actionsによる自動テスト / CIで実行境界を検証する

### 実際に通った例

公開されている**白神モデル v3.2**の的目YAMLをAPI実行テストのFixtureとして投入し、`/v1/execute` を通してGitHub Actionsで検証しています。

```text
白神モデル v3.2
       ↓
  /v1/execute
       ↓
 白神 Runtime
       ↓
  API Result
       ↓
 GitHub Actions
       ↓
     PASS
```

これはv3.2が完全な実行可能Protocol仕様であることを意味するものではなく、**実装境界を実物のProtocol資産で検証した例**です。

---

## Architecture

```text
Landscape
    ↓
Evidence
    ↓
Protocol / Specification
    ↓
Runtime
    ↓
API / Adapter
    ↓
External System / AI
```

中心原則は **Landscape First**。

RuntimeはLandscapeの主人ではなく、Landscapeを扱うための交換可能な実行層です。

最小の実行ループは次のようになります。

```text
Landscape
   ↓
Protocol
   ↓
Runtime
   ↓
Observable Transition
   ↓
Evidence
   ↓
Landscape State
   ↓
Inspectable Result
```

---

## 白神OSとは

AIモデルは変わります。
AIプロバイダも変わります。
インターフェースも変わります。

白神OSが問うのは別の問題です。

> **AIモデルそのものではなく、人間がAIとともに積み上げてきたLandscapeを、AIが変わっても引き継げるようにできないか。**

そのため、FoundationではLLMを交換可能なものとして扱い、Landscapeを持続的なアーキテクチャ資産として扱います。

---

## Repository Landscape

白神プロジェクトは役割ごとにRepositoryを分離しています。

| Repository | 役割 |
|---|---|
| [shirakami-model](https://github.com/bxa05221-ux/shirakami-model) | 白神モデルのVision / Model / 的目YAML |
| [shirakami-research](https://github.com/bxa05221-ux/shirakami-research) | Research / 理論・観測・実験 |
| [shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification) | Stable Specification / Protocol Contract |
| **shirakami-OS** | Foundation / Runtime / API / Implementation |

このRepositoryは**実装・Runtime層**です。安定した規範仕様を、実装が存在するという理由だけでここへ重複させない方針です。

---

## 現在の実装状態

現在、Repositoryには次の実装・検証要素があります。

- Foundation Architecture
- Runtime Prototype
- Runtime API α0.1 work
- Evidence境界
- Landscape State
- Matome YAML / Protocol Loaderの実験
- Protocol IR
- GitHub Adapter / Backend境界
- 実行可能なExamples
- 自動テスト / GitHub Actions CI

まだ完成した製品ではありません。
特に現在のAPIやProtocol Loaderは、すべての白神Protocolを完全実装したものではありません。

---

## まず動かす

最小Runtime：

```bash
python shirakami_os.py
```

Quickstart：

```bash
git clone https://github.com/bxa05221-ux/shirakami-OS.git
cd shirakami-OS
python examples/quickstart/run.py
```

Architectureをレビューする場合は、次の順番を推奨します。

**Landscape → Evidence → Specification / Protocol → Runtime → Adapter → Execution → Observation**

→ [Reviewer Entry Point](docs/architecture/REVIEWER_ENTRY_POINT.md)

---

## Public Service Artifact

現在の公開サービスArtifactは、**[Thread RPG v1.2.1](products/thread-rpg-v1.2.1/)**です。

UI-for-AI dialogue protocol / multi-voice conversation systemとして、Protocol-driven interactionを具体的に体験できる入口になっています。

→ [Service Artifact Index](products/)

その他の実験的Artifactは開発・研究成果として扱い、完成した公開サービスとは区別しています。

---

## Repository構成

```text
spec/       実装側のFoundation / transition specification
docs/       Architecture / reference notes
examples/   最小実行例
protocols/  実装で使用するProtocol source artifacts
runtime/    Runtime実装
plugins/    Adapter / Plugin
products/   公開サービスArtifact / reference implementation
tests/      自動テスト
```

---

## ユーザーズマニュアル（漫画版）

Public Alphaでは、的目YAML → 漫画Renderer → SVGという最小の文書生成経路を試しています。

- [漫画マニュアルの入口](docs/manual/)
- [日本語版SVG](docs/manual/manga-user-manual.ja.svg)
- [English版SVG](docs/manual/manga-user-manual.en.svg)
- [生成元の的目YAML](protocols/manual/manga-user-manual.yaml)
- [Rendering Contract α0.1](spec/manual-rendering.md)
- [漫画Renderer](runtime/manga_manual.py)

これは現時点では**漫画生成AIそのものではなく、Protocolで定義した説明構造を人間向けUIへRenderする実験的Adapter**です。

---

## 白神OSは何ではないか

白神OSは、次のものを目的としていません。

- ChatGPTなど特定AIの代替
- 新しいLLMそのものの開発
- 特定AIベンダーに固定されたアプリケーション
- 研究ノートを保存するだけのRepository

白神OSが目指しているのは、**AIが交換されても人間のLandscapeを引き継げるRuntime基盤**です。

---

## 開発方針

Foundationを先に定義し、その後にRuntimeを実装します。

実装中にFoundationそのものを勝手に変更するのではなく、実装から見つかった問題をObservationとして記録し、必要に応じて研究・仕様側へフィードバックすることを重視します。

そのため、現在のコードには意図的にPrototype段階の部分があります。

---

## レビュー・参加

第三者によるレビューを歓迎します。

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

## 関連リンク

- [Shirakami Model](https://github.com/bxa05221-ux/shirakami-model)
- [Shirakami Specification](https://github.com/bxa05221-ux/shirakami-specification)
- [Shirakami Research](https://github.com/bxa05221-ux/shirakami-research)
- [Shirakami OS](https://github.com/bxa05221-ux/shirakami-OS)

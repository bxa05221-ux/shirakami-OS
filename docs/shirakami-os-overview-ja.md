# Shirakami OS 公開概要

## 1. Shirakami OSとは

**Shirakami OSは、AIモデルそのものではない。**

人間が持つLandscapeを、AIやAIサービスが変わっても保持・観測・受け渡しできるようにするためのRuntime / reference implementationです。

AIモデルは変わります。
AIプロバイダーも変わります。
インターフェースも変わります。

しかし、人間が積み重ねてきたContextまで、そのたびに失われる必要はありません。

Shirakami OSは、AIモデルの性能競争の中ではなく、**モデルの外側にある人間のLandscapeを扱う層**を実装対象とします。

> **Landscape First.**
> RuntimeはLandscapeのためのサービスであり、その逆ではない。

---

## 2. 白神モデルとの関係

Shirakami OSは白神モデルそのものではありません。

現在のRepository構成では、役割を分けています。

- **shirakami-model** — 認知モデル、原則、概念的基盤
- **shirakami-research** — 観測、実験、仮説、探索的成果物
- **shirakami-specification** — 安定した仕様、Schema、規範的Protocol Contract
- **shirakami-OS** — Runtime、reference implementation、Adapter、Plugin、実行可能成果物

したがって、白神モデルが「何を目指すのか」を示すのに対して、Shirakami OSは「その考えを実行可能な境界としてどう扱うか」を担当します。

---

## 3. 白神OSの基本構造

Shirakami OSでは、次の流れを基本的なArchitectureとして扱います。

```text
Landscape
    ↓
Evidence
    ↓
Protocol / Specification
    ↓
Runtime
    ↓
Adapter
    ↓
External System / AI
```

Landscapeを出発点とし、観測可能な状態とEvidenceを保持し、Protocol / Specificationによって境界を定義し、Runtimeが実行し、Adapterを通じて外部システムやAIと接続します。

重要なのは、AIモデルをLandscapeの所有者にしないことです。

> **LLMs are replaceable. Landscape remains.**

---

## 4. 最小実行可能OS

Shirakami OSには、現在のRuntimeを実際に起動して確認できる最小のVertical Sliceがあります。

```text
boot Landscape
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

入口は `shirakami_os.py` です。

```bash
python shirakami_os.py
```

これは完成されたOS全体を意味するものではありません。

**「白神OSはどこにあるのか」**という問いに対して、現在確認可能な最小の実行境界を示すものです。

つまり、概念だけではなく、Landscapeを読み込み、Protocolを実行し、Observable TransitionをEvidenceとして扱い、Landscape StateとInspectable Resultへ戻すところまでを一つの実行経路として確認できます。

---

## 5. WorkspaceとUser Landscape

Shirakami OSは、OSそのものと個々のユーザーのLandscapeを同一視しません。

基本的な境界は次のように考えます。

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

ここでの原則は、Runtimeを共有可能な実行機構として扱いながら、ユーザー固有のLandscape / Context / MemoryをWorkspace境界の内側に保持することです。

現段階では、これは完成したマルチユーザー機能や認証仕様を意味しません。OSとUser Landscapeの所有境界を実装・検証するための設計基準です。

---

## 6. Protocolの役割

Protocolは、AIへの単純なプロンプトとしてではなく、**LandscapeとRuntimeの間の境界を定義するもの**として扱います。

Protocolが実行されることで、観測や状態変化をRuntimeが扱えるようになります。

そのため、白神OSではProtocolをRuntimeに埋め込んで一体化するのではなく、可能な限り独立した成果物として扱います。

安定した規範的仕様は `shirakami-specification` を正規の場所とし、このRepositoryでは実装に必要なProtocol source artifactsを扱います。

---

## 7. Evidenceの役割

Evidenceは「OSが存在することを証明するために集める記録」ではありません。

Runtime上で観測可能なTransitionが起きたとき、その状態変化を次の観測へ引き渡せるように記録するためのものです。

したがって、基本的には、

```text
Observable Transition
        ↓
      Evidence
        ↓
   Landscape State
        ↓
  Next Observation
```

という循環を作ります。

Evidenceは、Runtimeの都合で過去の状態を書き換えるためのものではなく、観測可能だった変化を保持するための境界です。

---

## 8. Adapterの役割

Adapterは、Shirakami OSの外部世界との接続点です。

例えばGitHubのような外部サービスをLandscapeとして観測する場合、GitHub固有のAPIやRepository構造をRuntime本体に直接埋め込むのではなく、Adapterとして接続します。

この構造により、外部サービスが変わってもRuntimeの中心的な責務を維持できます。

```text
Shirakami Runtime
       │
       ├── GitHub Adapter
       ├── Other Adapter
       └── Model Adapter
```

AdapterはLandscapeそのものの所有者ではありません。

---

## 9. Modelは交換可能

Shirakami OSが扱う中心的な資産は、特定のAIモデルではありません。

同じLandscapeを保持したまま、異なるAIモデルやAIサービスをRuntimeの外側で交換できることを目標とします。

```text
        Human Landscape
               │
          Shirakami OS
               │
        Model Adapter
          /    |    \
        AI-A  AI-B  AI-C
```

これにより、「AIが変わったから、これまでのContextも最初からやり直す」という状態を避けることを目指します。

---

## 10. このRepositoryが担当するもの

`shirakami-OS` は実装 / Runtime層です。

### 含むもの

- Runtime implementation
- Reference architecture implementation
- Adapter / Plugin implementations
- Executable examples
- Evidence / observation mechanisms
- 実装に使用するProtocol source artifacts

### 含まないもの

- Research Notes
- Historical Discussions
- Stable normative specifications
- Private user Landscape

---

## 11. 今のShirakami OSはどこまで来ているか

現在は、完成した商用OSを宣言している段階ではありません。

一方で、OSという名前だけを先行させている段階でもありません。

現在確認できる最小実体は、

1. Landscapeを起動時に受け取る
2. ProtocolをRuntimeで実行する
3. Observable Transitionを生成する
4. Evidenceとして扱う
5. Landscape Stateへ反映する
6. Inspectable Resultを返す

という一連の実行境界です。

今後の実装では、この最小境界を基礎にWorkspace、複数Landscape、Model交換、Adapterなどの境界を一つずつ検証していきます。

**機能を増やすことよりも、境界が本当に機能しているかを確認することを優先します。**

---

## 12. 公開入口

### 白神モデル

[shirakami-model](https://github.com/bxa05221-ux/shirakami-model)

### 白神モデル v3.2 — 的目YAML

[matome_yaml/shirakami-model-v3.2.yaml](https://github.com/bxa05221-ux/shirakami-model/blob/main/matome_yaml/shirakami-model-v3.2.yaml)

### 白神OS

[shirakami-OS](https://github.com/bxa05221-ux/shirakami-OS)

### 正規仕様

[shirakami-specification](https://github.com/bxa05221-ux/shirakami-specification)

### 研究・観測

[shirakami-research](https://github.com/bxa05221-ux/shirakami-research)

---

## 13. 最後に

Shirakami OSが目指すのは、AIそのものを人間の代わりにすることではありません。

人間が持っているLandscapeを中心に置き、AIやProtocolや外部サービスを交換可能な構成要素として扱いながら、観測と状態変化を次の思考へ引き渡せる環境を作ることです。

> **AIを中心にOSを作るのではなく、Landscapeを中心にRuntimeを置く。**

これが、現在のShirakami OSの出発点です。

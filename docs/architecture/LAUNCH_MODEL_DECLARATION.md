# Shirakami β1.0 Launch Model Declaration

## 白神モデル β1.0 — Launch Model / Operational Rollout

白神モデルは、研究・設計・実装の蓄積を経て、**Operational Rollout（運用展開）へ移行する段階**に入ったことを宣言します。

これは「完成品」や「理論完成」を意味しません。

β1.0の意味は、白神の構造を実装として動かし、検証し、観測しながら運用へ投入できる基盤が成立した、ということです。

---

## 1. Rolloutの対象

白神は特定のAIそのものではありません。

人間側の **Landscape** を中心に、Protocol、Runtime、Evidence、Adapter、Backendを分離して扱う基盤です。

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

RuntimeやBackendは交換可能な実装層として扱い、AIそのものを白神の中心資産とはしません。

---

## 2. Protocol First

β1.0の公開導線は **Protocol First** とします。

白神を理解・検証する入口は、特定AIのAPI利用ではなく、Protocolとその実行構造です。

最小経路は次の通りです。

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

現在のLoaderおよびRuntimeにはβ段階の制約があります。完全なProtocol仕様・完全なYAML実行系を意味するものではありません。

---

## 3. β1.0で確認するもの

β1.0では、以下を運用しながら継続的に検証します。

- Landscapeを中心に置けること
- ProtocolをRuntimeから分離できること
- Matome YAMLを意味の引継ぎ単位として扱えること
- RuntimeでProtocolを実行できること
- 状態変化をEvidenceとして観測できること
- AdapterによってBackend境界を分離できること
- 実装上のFindingをResearch / Specificationへ返せること
- 一変更一検証を維持できること

---

## 4. Matome YAMLと再生

白神の研究過程で、Matome YAMLは単なる要約ではなく、構造・意味を別の作業空間へ引き渡すための媒体として扱える可能性が確認されました。

ある的目YAMLから、観測・状態推定・状態遷移・シミュレーション・選択肢生成・再観測という構造を再構成できるかを検証する実験を行っています。

これは**完全な決定論的再現性を保証するものではありません**。

現段階では、意味の圧縮・引継ぎによって構造的対応を再生成できることを示す研究上の観測として扱います。

---

## 5. Human Agency

白神はAIに決定権を移すための仕組みではありません。

AIは観測、状態推定、予測、選択肢生成、シミュレーションなどを担い得ますが、人間の判断主体を置き換えることを目的としません。

> **AIは決めない。**

白神は、AIを権威化するのではなく、人間がAIを利用するための境界と観測可能性を構造化します。

---

## 6. Rollout後の運用

Rollout後は、実装を固定して終わるのではなく、OperationとEvidenceを通じて継続的に観測します。

```text
Operation
    ↓
Evidence
    ↓
Finding
    ↓
Research / Specification
    ↓
Protocol
    ↓
Runtime
```

理論上の未解決事項をRuntimeが勝手に埋めることはしません。

実装上の問題はFindingとして記録し、必要に応じてResearch / Specificationへ返します。

---

## 7. β1.0の位置づけ

β1.0は、次の状態を意味します。

**Shakedown → Launch Model → Operational Rollout**

つまり、白神は「完成したから運用する」のではなく、**検証可能な基盤が成立したので、運用そのものを次の検証環境とする**段階へ移行します。

未完成の仕様、未確認の境界、Prototype段階の実装については、その状態を明示したまま運用します。

---

## 8. 基本原則

- 分ける。しかし意味は切断しない。
- 作業はLocalで行う。
- 実装はGitHubで確定する。
- 意味は的目YAMLで引き継ぐ。
- 全体LandscapeはMotherで保持する。
- 未検証変更を確定扱いしない。
- 観測できたものを、系の全体だと決めつけない。

---

**Status: β1.0 Launch Model / Operational Rollout**

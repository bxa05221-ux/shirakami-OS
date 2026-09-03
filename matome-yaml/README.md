# 的目YAML集

白神OSの開発過程で得られた観測、発見、設計判断、到達経緯を、再利用可能なLandscapeとして保存するための記録群。

## 位置づけ

的目YAMLは完成した仕様書そのものではない。

- **Landscape** — 何が起きているか
- **的目YAML** — そこから何が見えてきたか／なぜ設計が変化したか
- **Protocol** — どう振る舞わせるか
- **Evidence** — 実行・検証によって何が確認されたか
- **Git History** — 実際に何を変更したか

を分離しつつ接続する。

## 原則

1. 観測を先に置く。
2. 発見と仕様を混同しない。
3. 設計変更の理由を残す。
4. 後からReplayできる粒度で記録する。
5. 的目YAML自体も更新履歴を持つ。
6. ブラックボックス化を避け、Landscape → Observation → Decision → Change → Verification の連鎖を追えるようにする。

## 初期カテゴリ

- `genesis/` — 白神OSの発生・発見経緯
- `architecture/` — アーキテクチャ上の転換点
- `verification/` — 検証方式・Evidence・Replay
- `applications/` — 個別適用から得られた知見
- `observations/` — 個別の観測記録

## 命名

`<topic>.yaml` を基本とする。仕様書ではなく「到達点とその理由」を記録する場合に使用する。

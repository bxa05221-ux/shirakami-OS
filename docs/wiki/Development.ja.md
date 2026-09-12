# 開発・検証

白神では、「ファイルがある」ことと「実験が成功した」ことを同じ意味にはしません。

## 現在の段階

β1.0は、理論完成や最終製品完成ではありません。

現在は、シェイクダウンから実運用へ移していく段階です。

## 開発の基本ループ

```text
Operation Definition
→ OperationPlan
→ Baseline
→ Dedicated Branch
→ Artifact
→ Canonical Verification
→ Protected PR
→ Protected Merge
→ Main Verification
→ Operation Result
```

## 検証

現在の標準的な実行確認は `test-runtime` です。

検証では、何が確認できたかと、何がまだ確認できていないかを分けます。

## Evidence

Evidenceは、実際の実行や観測の記録です。

「こうだったはず」という推測を、実際に起きたこととして置き換えません。

## 未解決のもの

分からないものは、分からないまま扱えるようにします。

理論上の未解決事項を、実装上の都合だけで勝手に確定しません。

## 外部AIによる観測

GPTでの確認を推奨していますが、GPTだけを正解の基準にはしません。

他AIモデルで試した場合は、結果をレポートしてください。

異なるモデルで何が起きたかを観測し、白神側で検証できる形にすることを目的とします。

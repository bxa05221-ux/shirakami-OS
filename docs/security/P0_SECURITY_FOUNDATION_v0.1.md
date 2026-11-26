# 第三者評価支援システム α版 v0.1 — P0セキュリティ基盤

Status: implementation candidate / human approval required

## 実装した境界

- `AIwitnessPolicyGate` は外部送信を default deny とする。policy、分類、送信先(provider/model)、データクラスの全てが明示許可されない限り送信しない。
- `OpenAIBackend` と `CopilotSDKProviderTransport` は policy gate なしでは送信できない。承認済みpayloadのfingerprintを再確認し、承認後改変を拒否する。
- 監査ログは判定、送信先、分類、payload fingerprintだけを保持し、本文は保持しない。
- `EncryptedEvaluationStore` は評価案件と評価者を分離し、本人の非共有記録を明示共有まで他評価者に返さない。保存値はFernetで暗号化し、鍵versionを記録する。

## 意図的な限界

この実装はP0の参照境界であり、本番保管サービスではない。現在のEncryptedEvaluationStoreはプロセス内メモリで、KMS/HSM、永続バックアップ、削除証跡、鍵の実運用ローテーション、端末保護、ネットワークegressのOS/クラウド強制は未実装である。

外部LLM APIに許可済みの入力を送信する場合も、その入力が提供者へ開示されないとは保証しない。実データの利用には、別途の法務・制度・組織承認と、管理下推論環境又は明示的な送信最小化方針が必要である。

## P0完了候補の条件

この変更だけでP0完了とはしない。少なくとも、全外部通信経路の棚卸し、永続暗号化基盤、鍵管理、評価専用APIへの組込み、実行環境のegress制御、CI成功記録、独立したセキュリティレビューを人間が確認すること。

# Supabase Adapter α0.1

## 目的

Supabase Adapterは、ShirakamiのLandscape / Evidence / Context / Relationを外部Backendへ保存・観測するための実験的な境界です。

Supabase自体はRuntime Coreではありません。

## 水脈としてのRelation

SNSでは、表面的な発言だけを見ると「管理者への反発」に見える発言でも、過去の発言や他者との関係を辿ることで、同じ場所を守ろうとしている文脈が見える場合があります。

このAdapterでは、その接続を `relation` として保存できます。

ただし、Relationは本人の真意を判定するものではありません。

```text
発言
 ↓
Context
 ↓
Relation
 ↓
水脈候補
 ↓
追加観測
```

AIは「あなたの本当の気持ちはこれだ」と決めません。

「ここに接続が観測されています」と提示するための基盤です。

## 日本語Context

日本語テキストはUTF-8の原文として保存します。Adapter側で翻訳や意味の書き換えは行いません。

## α0.1で試すこと

1. 日本語のLandscapeを保存する
2. Contextを原文のまま保存する
3. Evidenceを保存する
4. Context間のRelationを保存する
5. 保存後に読み戻し、元のLandscapeと比較する

## 現段階ではやらないこと

- 自動BAN
- 人物の意図判定
- 自動的な人格分類
- Relationを真実として確定すること
- Supabase固有仕様をRuntime Coreへ持ち込むこと

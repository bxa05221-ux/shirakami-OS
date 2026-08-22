# 最小実行可能白神OS

白神OSの最小実行境界を、実装として確認するための記録です。

## 実行経路

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

## 起動

```bash
python shirakami_os.py
```

この入口は最終Architectureを定義するものではありません。
既存Runtime β0.1の最小Vertical Sliceを、実際に起動・観測できるOS境界として提示します。

## レビュー対象

今回のレビュー対象は、機能追加の量ではなく、次の問いです。

> 「これを起動すれば白神OSが動く」と言える最小境界になっているか。

## English Summary

This document records the minimal executable boundary of Shirakami OS.

The entry point exposes one concrete path:

`Landscape → Protocol → Runtime → Observable Transition → Evidence → Landscape State → Inspectable Result`

It is intentionally not a final architecture. It makes the existing Runtime β0.1 vertical slice directly executable and reviewable.

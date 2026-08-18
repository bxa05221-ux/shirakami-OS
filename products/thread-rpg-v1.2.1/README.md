# Thread RPG v1.2.1

## A Shirakami OS service artifact

**Thread RPG** is a UI-for-AI dialogue protocol that turns AI reasoning and conversation into a multi-voice thread.

Version: **1.2.1**

## What it is

Thread RPG explores a simple idea:

> Instead of presenting an AI response as one monolithic voice, represent the conversation as a thread of distinct participants and perspectives.

The protocol is designed to support:

- multi-voice dialogue
- perspective separation
- conversational state
- thread-based interaction
- human-readable AI behavior
- later integration with Shirakami Runtime

## Relationship to Shirakami OS

Thread RPG is an application-level protocol artifact.

It is not the Shirakami OS kernel and does not define the Foundation by itself.

Its role is to provide a concrete service through which Shirakami concepts can be observed and tested.

```text
Shirakami OS
     ↓
Protocol Runtime
     ↓
Thread RPG
     ↓
Multi-voice conversation
```

## Version note

v1.2.1 is published here as a service artifact / reference implementation entry point.

Experimental extensions should remain separate from the stable protocol definition.

## Copyright / character use

Thread RPG itself is designed to be character-agnostic.

Examples using copyrighted characters or fictional settings are demonstrations only and must be handled separately from the core protocol and repository distribution.

## Japanese

Thread RPGは、AIとの対話を複数の視点・発言者によるスレッドとして表現する、UI-for-AI型の対話プロトコルです。

Shirakami OSそのものではなく、Shirakami Runtime上で扱うことのできる具体的なサービス／プロトコル成果物として位置づけます。

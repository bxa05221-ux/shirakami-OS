# External Landscape Observation — 9-Model Comparative Map

Status: observational working document
Scope: public GitHub repository observation
Purpose: compare externally observable software structures against the Shirakami nine-model overlay without inferring reference, influence, or causality.

## 1. Purpose

This document records a comparative observation of public GitHub repositories encountered through the Shirakami project's follower/repository observation work.

The objective is not to rank developers, identify competitors, or infer why an account follows Shirakami.

The objective is narrower:

> When contemporary AI, agent, RAG, security, infrastructure, and data systems are observed from the outside, which structural concerns recur, and where does Shirakami place its own boundaries?

This is a Landscape observation. It is not evidence of influence or authorship.

## 2. Shirakami nine-model overlay

The comparison uses nine structural dimensions:

1. Landscape Model — external environment, human/project context, or observable world outside the model.
2. Language Protocol Model — structured transfer of meaning, state, constraints, or intent.
3. Context Model — retention and management of state, history, memory, and premises.
4. Evidence Model — observation, evidence, verification, provenance, and separation of inference from fact.
5. Human Judgment Model — human authority, approval, rejection, stopping, or acceptance boundaries.
6. AI Runtime Model — separation and interchangeability of AI models, runtimes, adapters, or backends.
7. FSM Model — explicit states, transitions, guards, checkpoints, and boundary conditions.
8. DAG / Agent Runtime Model — multi-agent roles, dependencies, orchestration, and handoffs.
9. Durable Execution Model — persistence, restart, replay, execution history, and lineage.

### Observation rule

Structural similarity is recorded as high, medium, low, or UNKNOWN.

A name, profile description, repository title, or follower relationship is not by itself evidence of structural similarity.

## 3. Authorship and causality rule

The following are kept separate:

- repository ownership;
- original authorship;
- upstream/fork relationship;
- structural similarity;
- direct reference;
- influence;
- causal relationship.

In particular:

> A repository existing under an account does not establish that the account originated its architecture.

Forks, templates, copied projects, educational repositories, and repositories containing external references require additional caution.

Unless concrete evidence establishes otherwise:

- direct reference to Shirakami = UNKNOWN
- influence = UNKNOWN
- causal relationship = UNKNOWN

## 4. Initial external observations

The following are representative observations from the current public-repository survey. They are not rankings.

| Observed account | Primary observed area | Strongest structural overlap | Shirakami-specific boundary observed? |
|---|---|---|---|
| MaxCode917 | Full-stack AI Agent infrastructure | Context, AI Runtime, FSM, Agent Runtime, Durable Execution | Partial Human interaction; Shirakami Evidence/Provenance boundary not confirmed |
| mcdev7777 | GitRAG, RAG, Agent, MCP, feedback processing | Landscape, Context, Evidence, Agent Runtime | Structured AI processing observed; Human Gate / Provenance not confirmed |
| sungeer | Agent framework / Context Engineering / Protocol / Evaluation | Language Protocol, Context, AI Runtime, FSM, Agent Runtime | Comparable concepts observed; Shirakami authority boundary not confirmed |
| kh0kamoni | AI security automation / bug bounty | Evidence, Human Review, AI Runtime, FSM, Agent Runtime | Validation and human review observed; general Evidence/authority contract not confirmed |
| codewithQasimAli | DevSecOps / CI / security / observability | Landscape, Evidence, FSM, execution controls | Verification gates observed; AI authority boundary not observed |
| IDouble | AI usage / ChatGPT / ML | Evidence awareness, Human Judgment | AI output limitations documented; no Shirakami Evidence Contract observed |
| seehiong | Multi-model / local AI / multi-agent | AI Runtime, Context, Agent Runtime | Model choice and agent orchestration observed; Human Gate not confirmed |
| gaqx | Exchange APIs / realtime data | Landscape, Evidence, deterministic processing | Non-AI observation pipeline; Shirakami-specific boundary not observed |
| altyebv | Software / AI-ML adjacent applications | Context, semantic application design | AI-control architecture not confirmed |
| rahuloraj | AI applications / security / identity / robotics | Landscape, AI Runtime, security | Direct Shirakami boundary not confirmed |
| polystrategist | Discord AI bot / application integration | Language Protocol, Context, AI Runtime, FSM | User interaction and backend separation observed |
| coda-coda-23 | PHP / web / framework repositories | General software structure | AI-control structure not confirmed |
| takumi-sato0209 | Broad software / AI-named repositories | Landscape / general runtime | AI implementation not confirmed from the inspected material |

This table is deliberately descriptive. It does not score or rank the accounts.

## 5. Emerging structural pattern

The observations suggest several recurring layers in contemporary AI software:

AI Application
      ↓
RAG / Memory / MCP
      ↓
Agent Runtime / Orchestration
      ↓
Execution / Infrastructure / Security
      ↓
External systems and data

Across these layers, recurring engineering concerns include:

- model and backend separation;
- context and memory management;
- structured tool calls;
- agent orchestration;
- validation;
- observability;
- security gates;
- human interaction;
- durable execution.

These concerns occur independently across different projects. Their occurrence does not establish that those projects share an architecture or that any project references Shirakami.

## 6. Shirakami's observed boundary

The current Shirakami implementation places particular emphasis on a boundary that is not reducible to ordinary Agent orchestration:

Landscape
   ↓
Observation
   ↓
Evidence
   ↓
Context
   ↓
Protocol
   ↓
Runtime
   ↓
Verification
   ↓
Human Gate

The important architectural proposition is:

> AI execution may proceed, but authority does not move with the execution.

In the current implementation, candidate generation does not itself authorize execution. Human approval remains an explicit boundary, and verification returns observed results to the Evidence side.

This distinction should be evaluated from implementation evidence rather than from terminology.

## 7. What this observation does and does not show

### It does show

- AI Agent infrastructure is developing across multiple implementation styles.
- Context, protocol, runtime, verification, and human interaction are recurring engineering concerns.
- Several observed projects contain partial structures that can be meaningfully compared with Shirakami's nine-model overlay.
- Shirakami can be used as an observation lens across systems that were not designed as Shirakami systems.

### It does not show

- that any observed developer copied Shirakami;
- that any observed project was influenced by Shirakami;
- that similar structures have a common origin;
- that Shirakami is technically superior to any observed project;
- that a follower relationship indicates technical interest or intent.

## 8. Next experimental step

The next step is to turn this manual observation process into a reproducible GitHub Context Bridge / Repository Chat Explorer workflow:

Public GitHub repository
        ↓
Observation
        ↓
Context Bridge
        ↓
Nine-model structural analysis
        ↓
Evidence / UNKNOWN separation
        ↓
Human review
        ↓
Recorded observation

The system should preserve:

- source repository;
- observed file/path;
- observation timestamp;
- extracted evidence;
- structural interpretation;
- uncertainty;
- authorship status;
- reference/influence/causal status;
- human review state.

The output should remain an observation artifact rather than an autonomous verdict.

## 9. Design principle

The comparative survey reinforces a central Shirakami constraint:

> Observe broadly. Infer narrowly. Keep unknowns unknown.

The purpose of the Context Bridge is therefore not to make an AI decide what another repository really is.

It is to make the path from repository → observation → evidence → interpretation → human judgment inspectable.

## Verification status

This document records the current observational synthesis. It should not be treated as a normative specification.

Normative protocol material remains under shirakami-specification.

Implementation evidence remains under shirakami-OS.

Unverified hypotheses remain explicitly marked as UNKNOWN.

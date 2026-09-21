# Pipeline Execution Trace v0.1

## Purpose

`PipelineExecutionTrace` records the observable results of an explicitly selected
Protocol Pipeline run.

## Boundary

```text
Selected ProtocolRequest + PipelinePlan
    -> PipelineAdapter
    -> PipelineExecutionTrace
```

The trace preserves:

- Protocol ID and version
- Execution context
- Ordered per-step adapter results
- Backend identity for each step
- A conservative completion observation

## Deliberate non-goals

The trace does not:

- select a Protocol or Pipeline;
- select an AI vendor silently;
- determine truth or epistemic category;
- promote output to verified Evidence;
- replace the existing EvidenceStore contract.

This is an execution-observation boundary. Semantic verification and Human Gate
remain outside it.

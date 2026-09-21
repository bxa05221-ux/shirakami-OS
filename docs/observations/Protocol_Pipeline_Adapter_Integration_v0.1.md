# Protocol → Pipeline → Adapter → Backend

This integration boundary verifies the β development architecture without
calling an external AI service.

```
Selected Protocol
      ↓
PipelinePlan
      ↓
PipelineAdapterRequest
      ↓
PipelineAdapter
      ↓
Backend
```

The integration test uses a deterministic in-memory backend. Its purpose is
boundary verification, not model evaluation.

## Contract

1. Protocol supplies the Pipeline steps.
2. PipelinePlan preserves the selected Protocol identity and execution context.
3. Each Pipeline step becomes one Adapter request.
4. Adapter forwards the request to a replaceable Backend.
5. Backend selection is represented by the Adapter instance, not inferred by
   the Protocol or Pipeline.
6. The result can carry backend identity as execution evidence.

No external model invocation is required for this contract test.

## Next boundary

After this contract is stable, the next experiment is to run two different
Adapters against the same Protocol and compare only their observable execution
records.

That experiment will test the original Shirakami hypothesis:

> one Protocol can remain semantically stable while its execution backend
> changes with explicitly supplied context or operational conditions.

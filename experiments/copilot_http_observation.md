# Copilot → Shirakami HTTP Observation

This is the live-provider observation boundary for API MVP.

## Flow

Copilot SDK → provider output → `/v1/execute` → Runtime → Evidence → Trace → AIwitness → Human Gate

## Success conditions

- a real Copilot response is received
- the response crosses `/v1/execute`
- an Evidence ID is created and retrievable
- the Trace references that Evidence ID
- AIwitness references the same trace/evidence chain
- execution/publish/merge authority remains false
- Human Gate remains required

Provider credentials are runtime configuration only. They are not persisted as Evidence, Trace, or AIwitness data.

OpenAI API credentials are not required for this observation path.

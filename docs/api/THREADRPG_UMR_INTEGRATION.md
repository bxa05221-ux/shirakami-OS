# ThreadRPG through UMR

This integrates the existing implementation from `997a4fb` and `84d3ca7`
onto main `35ee22e`, using the preserved Windows HTTP changes. It does not
claim conformance to a newer ThreadRPG v0.2 specification or the old v3.2.2.

## Composition and local startup

Run UMR in its own process and checkout to avoid the two `api` packages
shadowing each other. For example, from the UMR checkout:

```bash
python -m uvicorn api.routes:app --host 127.0.0.1 --port 8010
```

From the Shirakami checkout, after securely configuring `SHIRAKAMI_API_KEY`,
start the mock-only ThreadRPG HTTP application:

```bash
python - <<'PY'
import os
import uvicorn
from api.http import create_app
from runtime.thread_rpg_umr_adapter import create_thread_rpg_umr_adapter

adapter = create_thread_rpg_umr_adapter(
    base_url="http://127.0.0.1:8010", engine="mock", timeout=30.0,
)
app = create_app(
    api_key=os.environ["SHIRAKAMI_API_KEY"], thread_rpg_adapter=adapter,
)
uvicorn.run(app, host="127.0.0.1", port=8012)
PY
```

The backend retains the original default UMR port 8766 for compatibility;
specify `base_url` explicitly when using the cloud environment's port 8010.
Configure a provider engine only when real model execution is authorized.
No provider is selected or called by the mock-only examples/tests.

## HTTP contract

`POST /v1/thread-rpg/execute`, with the configured `X-API-Key`, accepts:

```json
{
  "task": {"question": "Compare interpretations without deciding"},
  "perspectives": [{"id": "A"}, {"id": "B"}],
  "context": {"source": "explicitly supplied context"},
  "protocol_id": "thread_rpg",
  "version": "0.1"
}
```

Each perspective receives a separate independent-observation request with no
previous output. Conference receives both observations; Matome receives the
observations and conference. Context is explicitly supplied by the caller;
this endpoint does not implement automatic context selection or evidence acceptance.

The response contains `observations`, `conference`, `matome`, and `trace`.
`trace_kind="thread_rpg.phase_results"` identifies the legacy phase-result
sequence. It is **not** a canonical `ExecutionTrace` or AIwitness record.
The `evidence` field inside a PipelineAdapterResult describes adapter invocation
metadata; it is not an accepted EvidenceRecord or a provenance proof for model claims.

`record_status="generated"` and `evidence_ids=[]` are intentional. Unlike the
earlier Windows endpoint, generation does not append its contents to the Runtime
EvidenceStore. It does not create an execution ID, canonical trace ID, witness,
or approval; change the Runtime loop state; or update Landscape. All execution,
publication, merge, and decision authority flags remain false.

The observation-only generation route does not imply Human Gate approval.
The existing `/v1/execute` async execution and explicit Human Gate behavior remain
unchanged. Applications must retain generated output separately until a distinct,
authorized acceptance operation exists. This integration adds no such operation.

HTTP failures: unauthenticated requests are rejected when an API key is configured;
missing ThreadRPG adapter returns 503; invalid inputs return 422; backend failures
return 502 without exposing provider exception messages. Failed partial generation
does not create accepted Evidence.

## Validation

The normal unit/HTTP tests use deterministic providers or injected mock transport.
For the real two-process UMR HTTP test, set the local UMR checkout explicitly:

```bash
SHIRAKAMI_UMR_CHECKOUT=/path/to/universal-model-runtime \
python -m pytest -q tests/test_thread_rpg_umr_http_integration.py
```

This test starts and stops its own UMR process on a temporary loopback port.
It exercises the production factory, real UMR mock execution, four-stage payloads,
previous-output isolation, error handling, and non-promotion of generated output.
Without the checkout setting it is skipped, not passed. It never uses a real LLM.

Main's provider regression fixtures prepare the Runtime state before execution.
The async Human Gate test explicitly creates a candidate requiring review, and
asserts that the provider is not invoked before approval. Existing Evidence,
ExecutionTrace, witness verification/revisions and traceability remain covered.

Run AIwitness endpoint files in separate pytest processes: several existing tests
replace `sys.modules['api']`, which breaks combined collection independently of
this integration. The known ten earlier failures across repositories are separate
baseline issues and were not fixed here.

## Remaining design boundaries

- Persistence and explicit human acceptance/promotion of generated observations.
- A separately specified link from phase results to canonical execution lineage
  and AIwitness, without rerunning the same generation or asserting truth.
- A formal ThreadRPG v0.2 contract and migration from the inherited `version=0.1`.
- Real-model behavior, semantic quality and authorized provider configuration.

# Generated Route Candidate Pipeline Boundary

## Alpha 0.2

The one-stroke route pipeline now accepts the output of
`tools.protocol_route_candidates.generate_candidates()` through an explicit
`select_candidate()` boundary.

The implemented flow is:

`Protocol artifacts → structural n-gram candidates → Human Gate → One-Stroke Runtime → Verify → Evidence`

### Boundary rules

- Candidate generation remains structural only.
- `select_candidate()` does not infer semantic compatibility.
- Human approval remains explicit and fail-closed.
- Only the selected candidate is composed and executed.
- Execution remains one Runtime operation.
- Verification and Evidence capture remain mandatory parts of the pipeline.
- Missing Protocol implementations stop execution.

This boundary connects the existing n-gram candidate generator to the existing
human-gated one-stroke Runtime without making candidate generation an
authorization mechanism.

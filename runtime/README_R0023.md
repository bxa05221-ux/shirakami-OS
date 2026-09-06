# R0023 operational read

Run the read-only GitHub Landscape probe with an externally supplied credential:

```bash
SHIRAKAMI_LIVE_GITHUB_TEST=1 SHIRAKAMI_GITHUB_TOKEN="$TOKEN" python -m runtime.operational_github_read
```

Optional variables: `SHIRAKAMI_GITHUB_OWNER`, `SHIRAKAMI_GITHUB_REPO`, `SHIRAKAMI_GITHUB_BRANCH`.

The command performs a repository-root read and emits the observation as JSON. It performs no GitHub write and does not persist credentials.

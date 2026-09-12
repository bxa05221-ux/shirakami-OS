# β1.0 Reference Application

This is the smallest user-facing example for Shirakami OS β1.0.

It deliberately contains **no AI integration**.

The application demonstrates the public boundary as an ordinary state/history service:

```text
Browser UI
   |
   | POST /v1/execute
   v
Shirakami OS β1.0
   |
   +--> Protocol
   +--> Landscape
   +--> Evidence
   |
   v
Browser observes the resulting state
```

## Run

Start the β1.0 API with the repository's FastAPI application, then serve this directory from the same origin (or configure the API URL in `index.html`).

For example, from the repository root:

```bash
uvicorn api.runtime_api:create_app --factory --reload
```

Then serve `examples/beta1-reference-app/` with a static HTTP server and open `index.html`.

## What to observe

1. The page reads the current Landscape.
2. Enter a message and choose **Record change**.
3. The application sends a Protocol execution request.
4. Shirakami OS returns the Transition, Evidence, and Landscape.
5. The page refreshes and shows the accumulated Evidence.

The demo is intentionally in-memory. Restarting the API resets the Landscape and Evidence.

## Design boundary

AI may be connected later as an optional adapter or application component, but it is not part of this public-facing reference flow. The API remains meaningful when no AI is present.

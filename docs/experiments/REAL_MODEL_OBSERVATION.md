# Real model observation

This workflow exposes the experiment-only real-model observation boundary from the default branch so GitHub Actions can present it for manual dispatch.

The workflow checks out `experiment/real-model-adapter-001`, where the observation implementation currently lives. It requires repository secrets `OPENAI_API_KEY` and `OPENAI_MODEL` and performs one opaque model request.

No semantic interpretation, model-quality judgment, automatic protocol selection, or new theory is introduced by this workflow.

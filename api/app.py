"""Runnable HTTP entrypoint for Shirakami OS API alpha 0.1.

Run locally with:
    uvicorn api.app:app --reload
"""

from api.runtime_api import create_app

app = create_app()

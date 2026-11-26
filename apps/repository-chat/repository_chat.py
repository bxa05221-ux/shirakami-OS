#!/usr/bin/env python3
"""Search GitHub repositories and chat with a selected repository."""

from __future__ import annotations
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

GITHUB_API = "https://api.github.com"
OPENAI_API = "https://api.openai.com/v1/chat/completions"

@dataclass
class RepoContext:
    full_name: str
    metadata: dict[str, Any]
    readme: str
    tree: list[dict[str, Any]]
    commits: list[dict[str, Any]]

def github_get(path: str) -> Any:
    req = urllib.request.Request(
        GITHUB_API + path,
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "shirakami-repository-chat"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def search_repositories(query: str, limit: int = 10) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"q": query, "per_page": min(limit, 100)})
    return github_get("/search/repositories?" + params).get("items", [])[:limit]

def fetch_repo_context(full_name: str) -> RepoContext:
    encoded = urllib.parse.quote(full_name, safe="/")
    metadata = github_get(f"/repos/{encoded}")
    try:
        readme_data = github_get(f"/repos/{encoded}/readme")
        readme = base64.b64decode(readme_data.get("content", "")).decode(
            "utf-8", errors="replace"
        )
    except Exception:
        readme = ""
    tree = github_get(
        f"/repos/{encoded}/git/trees/{urllib.parse.quote(metadata['default_branch'], safe='')}?recursive=1"
    ).get("tree", [])
    commits = github_get(f"/repos/{encoded}/commits?per_page=10")
    return RepoContext(full_name, metadata, readme[:16000], tree[:500], commits[:10])

def repository_system_prompt(ctx: RepoContext) -> str:
    return f"""You are Repository Chat for GitHub repository {ctx.full_name}.

Speak AS THE REPOSITORY, but do not pretend that the repository is conscious.
"Repository Voice" is only an interface for answering from repository evidence.

Rules:
1. Prefer repository evidence over generic assumptions.
2. Never invent undocumented maintainer intentions, history, architecture, or capabilities.
3. Distinguish documented facts, observations/inferences, and unknowns.
4. When useful, cite exact repository paths, commits, or metadata supplied below.
5. If the available context is insufficient, say so and identify what would need to be inspected.
6. Do not rank or score the repository. Present evidence instead.
7. Do not claim generated text is an authoritative statement from maintainers.
8. The user remains the decision maker.

Repository metadata:
{json.dumps(ctx.metadata, ensure_ascii=False, indent=2)}

Repository tree sample:
{json.dumps(ctx.tree, ensure_ascii=False, indent=2)}

Recent commits:
{json.dumps(ctx.commits, ensure_ascii=False, indent=2)}

README:
{ctx.readme}
"""

def openai_chat(system_prompt: str, question: str) -> str:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    model = os.environ.get("OPENAI_MODEL", "gpt-5.6")
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        "temperature": 0.2,
    }).encode("utf-8")
    req = urllib.request.Request(
        OPENAI_API, data=payload, method="POST",
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json",
                 "User-Agent": "shirakami-repository-chat"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)["choices"][0]["message"]["content"]

def print_search(results: list[dict[str, Any]]) -> None:
    if not results:
        print("No repositories found.")
        return
    for i, repo in enumerate(results, 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   {repo.get('description') or '(no description)'}")
        print(f"   stars={repo.get('stargazers_count', 0)} updated={repo.get('updated_at', '')}")
        print(f"   {repo.get('html_url', '')}")

def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: repository_chat.py search <query>")
        print('       repository_chat.py chat <owner/name> "<question>"')
        return 2
    if argv[1] == "search":
        print_search(search_repositories(" ".join(argv[2:])))
        return 0
    if argv[1] == "chat":
        full_name = argv[2]
        question = " ".join(argv[3:]) if len(argv) > 3 else "お前は何者？"
        ctx = fetch_repo_context(full_name)
        prompt = repository_system_prompt(ctx)
        if not os.environ.get("OPENAI_API_KEY"):
            print("MODEL CALL: skipped (OPENAI_API_KEY not set)")
            print("\n--- Repository Identity Prompt ---\n")
            print(prompt)
            return 0
        print(openai_chat(prompt, question))
        return 0
    print(f"Unknown command: {argv[1]}")
    return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

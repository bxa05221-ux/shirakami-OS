#!/usr/bin/env python3
from __future__ import annotations
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "repository-chat"))
import repository_chat as core

ROOT = Path(__file__).parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def evidence_for(ctx: core.RepoContext) -> list[dict[str, str]]:
    meta_url = ctx.metadata.get("html_url", "")
    items = [
        {"label": "repository metadata", "url": meta_url},
        {"label": "README.md", "url": f"{meta_url}/blob/{ctx.metadata.get('default_branch', 'main')}/README.md"},
        {"label": "repository tree", "url": f"{meta_url}/tree/{ctx.metadata.get('default_branch', 'main')}"},
    ]
    for commit in ctx.commits[:10]:
        url = commit.get("html_url")
        message = (commit.get("commit", {}).get("message", "") or "").splitlines()[0]
        if url:
            items.append({"label": f"commit: {message[:80]}", "url": url})
    return [x for x in items if x["url"]]


class Handler(BaseHTTPRequestHandler):
    def send_json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            data = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if u.path == "/api/search":
            q = parse_qs(u.query).get("q", [""])[0]
            self.send_json({"items": core.search_repositories(q)})
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(n))
            ctx = core.fetch_repo_context(body["repo"])
            prompt = core.repository_system_prompt(ctx)
            evidence = evidence_for(ctx)
            if not os.environ.get("OPENAI_API_KEY"):
                self.send_json({
                    "error": "OPENAI_API_KEY が未設定です",
                    "evidence": evidence,
                }, 503)
                return
            self.send_json({
                "answer": core.openai_chat(prompt, body["question"]),
                "evidence": evidence,
            })
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8787"))
    print(f"Repository Chat Explorer: http://localhost:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()

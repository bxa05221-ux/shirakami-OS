#!/usr/bin/env python3
from __future__ import annotations
import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs,urlparse
import sys
sys.path.insert(0,str(Path(__file__).parent.parent/"repository-chat"))
import repository_chat as core
ROOT=Path(__file__).parent
HTML=(ROOT/"index.html").read_text(encoding="utf-8")
class Handler(BaseHTTPRequestHandler):
 def send_json(self,obj,status=200):
  d=json.dumps(obj,ensure_ascii=False).encode();self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Content-Length",str(len(d)));self.end_headers();self.wfile.write(d)
 def do_GET(self):
  u=urlparse(self.path)
  if u.path=="/":
   d=HTML.encode();self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Content-Length",str(len(d)));self.end_headers();self.wfile.write(d);return
  if u.path=="/api/search":self.send_json({"items":core.search_repositories(parse_qs(u.query).get("q",[""])[0])});return
  self.send_error(404)
 def do_POST(self):
  if self.path!="/api/chat":self.send_error(404);return
  try:
   n=int(self.headers.get("Content-Length","0"));b=json.loads(self.rfile.read(n));ctx=core.fetch_repo_context(b["repo"]);prompt=core.repository_system_prompt(ctx)
   if not os.environ.get("OPENAI_API_KEY"):self.send_json({"error":"OPENAI_API_KEY が未設定です","evidence":["metadata","README.md","repository tree","recent commits"]},503);return
   self.send_json({"answer":core.openai_chat(prompt,b["question"]),"evidence":["repository metadata","README.md","repository tree","recent commits"]})
  except Exception as e:self.send_json({"error":str(e)},500)
 def log_message(self,*a):pass
if __name__=="__main__":
 p=int(os.environ.get("PORT","8787"));print(f"Repository Chat Explorer: http://localhost:{p}");ThreadingHTTPServer(("127.0.0.1",p),Handler).serve_forever()

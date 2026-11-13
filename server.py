"""golden/env-names: answers which of the asked environment variable names it started with.

GET /                         -> a line naming this fixture
GET /env-names?names=A,B,C    -> {"present": [...], "missing": [...]} for the asked names only

Names only: never a value, a length or a hash, and never a name it wasn't asked about, so the
service's public URL shows nothing about the environment beyond what the caller already named.
"""
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

# fullmatch, not match with $: in Python, $ also matches before a trailing newline.
NAME = re.compile(r"[A-Z_][A-Z0-9_]{0,63}")
MAX_NAMES = 10


def check(raw, environ):
    """(status, body) for the query value of `names`, against the mapping `environ`."""
    names = [n for n in (raw or "").split(",") if n]
    if not names or len(names) > MAX_NAMES or not all(NAME.fullmatch(n) for n in names):
        # A fixed sentence: the refusal never repeats what was sent.
        return 400, {"error": f"names: 1 to {MAX_NAMES} comma-separated names like DATABASE_URL"}
    asked = sorted(set(names))
    return 200, {
        "present": [n for n in asked if n in environ],
        "missing": [n for n in asked if n not in environ],
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/env-names":
            raw = parse_qs(url.query).get("names", [""])
            status, body = check(raw[0] if len(raw) == 1 else "", os.environ)
            self.reply(status, "application/json", json.dumps(body) + "\n")
        elif url.path == "/":
            self.reply(200, "text/plain", "golden/env-names fixture\n")
        else:
            self.reply(404, "text/plain", "not found\n")

    def reply(self, status, kind, text):
        data = text.encode()
        self.send_response(status)
        self.send_header("content-type", kind)
        self.send_header("x-content-type-options", "nosniff")
        self.send_header("cache-control", "no-store")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # Method and path only: the query holds names, never values, but logs needn't carry it.
        print(f"{self.command} {urlsplit(self.path).path}", flush=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT") or 3000)
    print(f"Server is running on port {port}", flush=True)
    ThreadingHTTPServer(("", port), Handler).serve_forever()

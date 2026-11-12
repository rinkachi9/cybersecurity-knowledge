#!/usr/bin/env python3
"""Deliberately vulnerable XSS lab: reflected, stored and DOM-based XSS, each with a fixed twin.

For local study only. Binds to 127.0.0.1. Never expose it to a network.
Python 3.10 or later, standard library only.

Run:   python3 run-xss-lab.py            (listens on http://127.0.0.1:8088)
Pages:
  /search?q=...          reflected XSS (vulnerable)     /search-safe?q=...   output encoded
  /search-csp?q=...      same bug, blocked by a strict Content-Security-Policy
  /comments              stored XSS (vulnerable)        /comments-safe       output encoded
  POST /comment  body=... stores a comment in memory
  /dom#...               DOM-based XSS (vulnerable)     /dom-safe#...        textContent sink
  /dom-tt#...            same vulnerable code, but Trusted Types are enforced by CSP
"""
import html
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

COMMENTS: list[str] = []   # in-memory "database"

PAGE = "<!doctype html><html><head><meta charset='utf-8'><title>{title}</title></head><body>{body}</body></html>"

DOM_VULN = """<h1>Welcome</h1><div id="greeting"></div>
<script>
  // Vulnerable: attacker-controlled fragment flows into an HTML sink.
  const name = decodeURIComponent(location.hash.slice(1));
  document.getElementById("greeting").innerHTML = "Hello, " + name;
</script>"""

DOM_SAFE = """<h1>Welcome</h1><div id="greeting"></div>
<script>
  // Fixed: same source, but a text sink. The browser never parses it as HTML.
  const name = decodeURIComponent(location.hash.slice(1));
  document.getElementById("greeting").textContent = "Hello, " + name;
</script>"""


class Lab(BaseHTTPRequestHandler):
    def send_page(self, title, body, headers=None):
        data = PAGE.format(title=title, body=body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query).get("q", [""])[0]
        if url.path == "/search":
            # Vulnerable: q is inserted into HTML without encoding.
            self.send_page("Search", f"<p>Results for: {q}</p>")
        elif url.path == "/search-safe":
            self.send_page("Search", f"<p>Results for: {html.escape(q)}</p>")
        elif url.path == "/search-csp":
            csp = "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'"
            self.send_page("Search", f"<p>Results for: {q}</p>", {"Content-Security-Policy": csp})
        elif url.path == "/comments":
            items = "".join(f"<li>{c}</li>" for c in COMMENTS)
            self.send_page("Comments", f"<ul>{items}</ul>")
        elif url.path == "/comments-safe":
            items = "".join(f"<li>{html.escape(c)}</li>" for c in COMMENTS)
            self.send_page("Comments", f"<ul>{items}</ul>")
        elif url.path == "/dom":
            self.send_page("DOM", DOM_VULN)
        elif url.path == "/dom-safe":
            self.send_page("DOM", DOM_SAFE)
        elif url.path == "/dom-tt":
            # Same vulnerable script. The browser now refuses plain strings in HTML sinks.
            self.send_page("DOM", DOM_VULN, {"Content-Security-Policy": "require-trusted-types-for 'script'"})
        else:
            self.send_error(404)

    def do_POST(self):
        if urlparse(self.path).path != "/comment":
            return self.send_error(404)
        length = int(self.headers.get("Content-Length", 0))
        body = parse_qs(self.rfile.read(length).decode()).get("body", [""])[0]
        COMMENTS.append(body)          # stored as-is: encoding belongs at output time
        self.send_response(303)
        self.send_header("Location", "/comments")
        self.end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8088
    print(f"XSS lab on http://127.0.0.1:{port} (local only)")
    ThreadingHTTPServer(("127.0.0.1", port), Lab).serve_forever()

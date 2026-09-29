#!/usr/bin/env python3
import json
import os
import re
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "dist"
LEADS_FILE = Path(os.environ.get("LEADS_FILE", "/tmp/korda-leads.jsonl"))
REQUESTS = defaultdict(deque)


class KordaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/lead":
            self.send_json(404, {"error": "not_found"})
            return

        client = self.client_address[0]
        now = time.time()
        window = REQUESTS[client]
        while window and window[0] < now - 60:
            window.popleft()
        if len(window) >= 6:
            self.send_json(429, {"error": "too_many_requests"})
            return
        window.append(now)

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16_384:
                raise ValueError
            data = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "invalid_request"})
            return

        name = str(data.get("name", "")).strip()[:100]
        phone = str(data.get("phone", "")).strip()[:40]
        message = str(data.get("message", "")).strip()[:1500]
        request_type = str(data.get("requestType", "Заявка с сайта")).strip()[:120]
        if not name or len(re.sub(r"\D", "", phone)) < 7 or data.get("consent") != "on":
            self.send_json(422, {"error": "validation_failed"})
            return

        lead = {
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "requestType": request_type,
            "name": name,
            "phone": phone,
            "message": message,
            "ip": client,
        }
        LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LEADS_FILE.open("a", encoding="utf-8") as output:
            output.write(json.dumps(lead, ensure_ascii=False) + "\n")
        print("NEW_LEAD " + json.dumps(lead, ensure_ascii=False), flush=True)
        self.send_json(201, {"status": "accepted"})

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), KordaHandler)
    print(f"KORDA web service listening on port {port}", flush=True)
    server.serve_forever()

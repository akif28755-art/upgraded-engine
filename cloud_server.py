#!/usr/bin/env python3
"""TJK FormLab cloud-compatible static/API server. No API keys required."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path
import json, os, threading, time

ROOT = Path(__file__).resolve().parent
STATE = {
    "updatedAt": None, "forecastUpdatedAt": None, "sources": [],
    "programRows": [], "forecastRows": [], "forecastCoverage": [],
    "trainingRows": [], "statsRows": [], "resultRows": [],
    "refreshState": {"running": False, "status": "not_configured",
                     "message": "Bulut sunucusu çalışıyor; canlı TJK veri sağlayıcısı bu dağıtımda henüz etkinleştirilmedi."}
}
LOCK = threading.Lock()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, code, obj):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            return self.send_json(200, {"ok": True, "service": "TJK FormLab", "mode": "cloud-no-api-key"})
        if parsed.path == "/api/data":
            with LOCK:
                return self.send_json(200, STATE)
        if parsed.path == "/api/network":
            return self.send_json(200, {"addresses": [], "port": int(os.environ.get("PORT", "10000")), "mode": "cloud"})
        if parsed.path == "/api/refresh":
            # Deliberately do not pretend live refresh succeeded.
            return self.send_json(200, {"ok": False, "refreshState": STATE["refreshState"],
                                        "message": STATE["refreshState"]["message"]})
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/refresh":
            return self.send_json(503, {"ok": False, "error": "live_source_not_configured",
                "message": "Canlı TJK veri çekimi henüz bulut sunucusuna taşınmadı; sahte veri üretilmedi."})
        return self.send_json(404, {"error": "not_found"})

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    print(f"TJK FormLab cloud server listening on 0.0.0.0:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()

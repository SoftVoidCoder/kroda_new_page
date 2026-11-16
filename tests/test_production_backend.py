"""Smoke-test the PHP handlers used on Timeweb without sending e-mail."""
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import unittest
from urllib import error, parse, request


DIST = Path(__file__).resolve().parents[1] / "dist"


class ProductionBackendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        cls.port = sock.getsockname()[1]
        sock.close()
        cls.tmp = tempfile.TemporaryDirectory()
        env = os.environ | {"KORDA_MAIL_DRY_RUN": "1", "TMPDIR": cls.tmp.name}
        cls.server = subprocess.Popen(
            ["php", "-S", f"127.0.0.1:{cls.port}", "-t", str(DIST)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        time.sleep(0.25)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.wait(timeout=3)
        cls.tmp.cleanup()

    def call(self, path, data=None, headers=None):
        req = request.Request(f"http://127.0.0.1:{self.port}{path}", data=data, headers=headers or {})
        try:
            response = request.urlopen(req)
        except error.HTTPError as exc:
            response = exc
        return response.status, response.headers, response.read()

    def test_lead_validation_and_success(self):
        status, _, _ = self.call("/api/lead.php")
        self.assertEqual(status, 405)
        payload = json.dumps({"name": "Тест", "phone": "+7 900 000-00-00", "consent": "on"}).encode()
        status, _, body = self.call("/api/lead.php", payload, {"Content-Type": "application/json"})
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(body)["ok"])

    def test_questionnaire_redirects_after_acceptance(self):
        fields = parse.urlencode({
            "questionnaire_type": "pipelines",
            "object_name": "Тестовый объект",
            "contacts[0][name]": "Тест",
            "contacts[0][phone]": "+7 900 000-00-00",
            "consent": "on",
        }).encode()
        opener = request.build_opener(request.HTTPHandler())
        req = request.Request(f"http://127.0.0.1:{self.port}/api/questionnaire.php", data=fields)
        response = opener.open(req)
        self.assertTrue(response.url.endswith("/spasibo.html?source=questionnaire"))


if __name__ == "__main__":
    unittest.main()

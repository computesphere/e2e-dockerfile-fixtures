import contextlib
import io
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from server import MAX_NAMES, Handler, check

FAKE = {"DB_URL": "a-value-never-shown", "PORT": "3000"}


class Check(unittest.TestCase):
    def test_asked_names_only(self):
        self.assertEqual(check("REDIS_URL,DB_URL", FAKE), (200, {"present": ["DB_URL"], "missing": ["REDIS_URL"]}))

    def test_never_a_value_or_an_unasked_name(self):
        _, body = check("DB_URL", FAKE)
        text = str(body)
        self.assertNotIn("a-value-never-shown", text)
        self.assertNotIn("PORT", text)

    def test_refuses_bad_or_too_many_names_without_echoing_them(self):
        for raw in ["", ",", "db_url", "A B", "A;B", "<script>", "DB_URL\n", "\nDB_URL", "X" * 65, ",".join(f"N{i}" for i in range(MAX_NAMES + 1))]:
            status, body = check(raw, FAKE)
            self.assertEqual(status, 400, raw)
            for part in filter(None, raw.split(",")):
                self.assertNotIn(part, json.dumps(body), raw)


class Served(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def get(self, path):
        try:
            r = urllib.request.urlopen(self.base + path, timeout=5)
        except urllib.error.HTTPError as e:
            r = e
        return r.status, r.headers, r.read().decode()

    def test_json_nosniff_no_store(self):
        self.assertEqual(self.get("/env-names?names=DB_URL%0A")[0], 400)
        for path in ["/env-names?names=NOT_SET_HERE", "/env-names?names=%3Cscript%3E"]:
            status, headers, body = self.get(path)
            self.assertEqual(headers["content-type"], "application/json", path)
            self.assertEqual(headers["x-content-type-options"], "nosniff", path)
            self.assertEqual(headers["cache-control"], "no-store", path)
            self.assertNotIn("<script>", body, path)
        self.assertEqual(self.get("/env-names?names=NOT_SET_HERE")[0], 200)
        self.assertEqual(self.get("/env-names?names=%3Cscript%3E")[0], 400)

    def test_root_and_unknown(self):
        self.assertEqual(self.get("/")[2], "golden/env-names fixture\n")
        self.assertEqual(self.get("/nope")[0], 404)

    def test_log_line_is_method_and_path_only(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.get("/env-names?names=LOGGED_NAME_PROBE")
        self.assertIn("GET /env-names", out.getvalue())
        self.assertNotIn("LOGGED_NAME_PROBE", out.getvalue())
        self.assertNotIn("?", out.getvalue())


if __name__ == "__main__":
    unittest.main()

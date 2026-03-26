import time
import concurrent.futures
import json
import os
import socket
import subprocess
import sys
import urllib.request
from django.test import SimpleTestCase


class SleepApiTests(SimpleTestCase):
    def test_sleep_endpoint_waits_and_returns_timing_fields(self):
        started_at = time.time()
        response = self.client.get("/api/sleep")
        ended_at = time.time()
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(payload.keys()), {"start", "end", "duration"})
        self.assertGreaterEqual(payload["duration"], 1.0)
        self.assertGreaterEqual(payload["end"] - payload["start"], 1.0)
        self.assertGreaterEqual(ended_at - started_at, 1.0)
    
    def test_sleep_endpoint_concurrent_requests(self):
        start = time.time()

        request_count = 5

        def fetch_api():
            return self.client.get("/api/sleep")

        responses = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=request_count) as executor:
            futures = [executor.submit(fetch_api) for _ in range(request_count)]

            for future in concurrent.futures.as_completed(futures):
                responses.append(future.result())

        self.assertEqual(len(responses), request_count)
        for response in responses:
            self.assertEqual(response.status_code, 200)

        end = time.time()
        elapsed_time = end - start
        print(f"Total elapsed time for {request_count} requests: {elapsed_time:.2f} seconds")

    def test_sleep_endpoint_concurrent_requests_via_uvicorn(self):
        request_count = 5
        port = self._find_free_port()
        process = self._start_uvicorn(port)

        try:
            self._wait_for_server_ready(port)

            start = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=request_count) as executor:
                responses = list(
                    executor.map(
                        lambda _: self._fetch_json_from_uvicorn("api/sleep", port),
                        range(request_count),
                    )
                )
            elapsed_time = time.time() - start

            self.assertEqual(len(responses), request_count)
            for payload in responses:
                self.assertEqual(set(payload.keys()), {"start", "end", "duration"})
                self.assertGreaterEqual(payload["duration"], 1.0)

            print(
                f"Total elapsed time for {request_count} uvicorn requests: {elapsed_time:.2f} seconds"
            )
        finally:
            process.terminate()
            process.wait(timeout=10)

    def _fetch_json_from_uvicorn(self, path, port):
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/{path}", timeout=30) as response:
            self.assertEqual(response.status, 200)
            return json.loads(response.read())

    def _find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    def _start_uvicorn(self, port):
        env = os.environ.copy()
        env.setdefault("PYTHONUNBUFFERED", "1")
        return subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "apidemo.asgi:application",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            env=env,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    def _wait_for_server_ready(self, port):
        deadline = time.time() + 10
        while time.time() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                    return
            except Exception:
                time.sleep(0.1)

        self.fail("uvicorn server did not become ready within 10 seconds")

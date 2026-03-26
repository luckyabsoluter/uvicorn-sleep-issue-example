import time

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

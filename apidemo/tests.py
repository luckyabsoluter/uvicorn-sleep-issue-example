import time

import concurrent
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

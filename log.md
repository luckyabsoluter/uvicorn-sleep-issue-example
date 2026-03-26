# Log
`PRINT` is in `apidemo.router.api`.

## PRINT = False
```
$ python ./manage.py test
Found 6 test(s).
System check identified no issues (0 silenced).
Total elapsed time for 5 async requests: 1.03 seconds
.Total elapsed time for 5 uvicorn async-sleep requests: 5.18 seconds
..Total elapsed time for 5 requests: 1.00 seconds
.Total elapsed time for 5 uvicorn sleep requests: 1.15 seconds
..
----------------------------------------------------------------------
Ran 6 tests in 11.612s
```

## PRINT = True
```
$ python ./manage.py test
Found 6 test(s).
System check identified no issues (0 silenced).
Received request, sleeping... thread: ThreadPoolExecutor-3_0
Received request, sleeping... thread: ThreadPoolExecutor-5_0
Received request, sleeping... thread: ThreadPoolExecutor-2_0
Received request, sleeping... thread: ThreadPoolExecutor-4_0
Received request, sleeping... thread: ThreadPoolExecutor-6_0
Finished sleeping. thread: ThreadPoolExecutor-3_0
Finished sleeping. thread: ThreadPoolExecutor-2_0
Finished sleeping. thread: ThreadPoolExecutor-4_0
Finished sleeping. thread: ThreadPoolExecutor-5_0
Finished sleeping. thread: ThreadPoolExecutor-6_0
Total elapsed time for 5 async requests: 1.01 seconds
.INFO:     Started server process [41524]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:63087 (Press CTRL+C to quit)
Received request, sleeping... thread: MainThread
Finished sleeping. thread: MainThread
INFO:     127.0.0.1:63093 - "GET /api/async-sleep HTTP/1.1" 200 OK
Received request, sleeping... thread: MainThread
Finished sleeping. thread: MainThread
Received request, sleeping... thread: MainThread
Finished sleeping. thread: MainThread
Received request, sleeping... thread: MainThread
Finished sleeping. thread: MainThread
Received request, sleeping... thread: MainThread
Finished sleeping. thread: MainThread
INFO:     127.0.0.1:63094 - "GET /api/async-sleep HTTP/1.1" 200 OK
INFO:     127.0.0.1:63095 - "GET /api/async-sleep HTTP/1.1" 200 OK
INFO:     127.0.0.1:63096 - "GET /api/async-sleep HTTP/1.1" 200 OK
INFO:     127.0.0.1:63097 - "GET /api/async-sleep HTTP/1.1" 200 OK
Total elapsed time for 5 uvicorn async-sleep requests: 5.16 seconds
.Received request, sleeping... thread: ThreadPoolExecutor-8_0
Finished sleeping. thread: ThreadPoolExecutor-8_0
.Received request, sleeping... thread: ThreadPoolExecutor-9_0
Received request, sleeping... thread: ThreadPoolExecutor-9_1
Received request, sleeping... thread: ThreadPoolExecutor-9_2
Received request, sleeping... thread: ThreadPoolExecutor-9_3
Received request, sleeping... thread: ThreadPoolExecutor-9_4
Finished sleeping. thread: ThreadPoolExecutor-9_0
Finished sleeping. thread: ThreadPoolExecutor-9_1
Finished sleeping. thread: ThreadPoolExecutor-9_2
Finished sleeping. thread: ThreadPoolExecutor-9_4Finished sleeping. thread: ThreadPoolExecutor-9_3

Total elapsed time for 5 requests: 1.00 seconds
.INFO:     Started server process [10984]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:63101 (Press CTRL+C to quit)
Received request, sleeping... thread: ThreadPoolExecutor-1_0
Received request, sleeping... thread: ThreadPoolExecutor-2_0Received request, sleeping... thread: ThreadPoolExecutor-3_0

Received request, sleeping... thread: ThreadPoolExecutor-4_0
Received request, sleeping... thread: ThreadPoolExecutor-5_0
Finished sleeping. thread: ThreadPoolExecutor-1_0
Finished sleeping. thread: ThreadPoolExecutor-4_0Finished sleeping. thread: ThreadPoolExecutor-3_0Finished sleeping. thread: ThreadPoolExecutor-2_0


Finished sleeping. thread: ThreadPoolExecutor-5_0
INFO:     127.0.0.1:63106 - "GET /api/sleep HTTP/1.1" 200 OK
INFO:     127.0.0.1:63108 - "GET /api/sleep HTTP/1.1" 200 OK
INFO:     127.0.0.1:63110 - "GET /api/sleep HTTP/1.1" 200 OK
INFO:     127.0.0.1:63107 - "GET /api/sleep HTTP/1.1" 200 OK
INFO:     127.0.0.1:63109 - "GET /api/sleep HTTP/1.1" 200 OK
Total elapsed time for 5 uvicorn sleep requests: 1.13 seconds
.Received request, sleeping... thread: MainThread
Finished sleeping. thread: MainThread
.
----------------------------------------------------------------------
Ran 6 tests in 11.546s
```

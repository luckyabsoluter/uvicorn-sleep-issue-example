# Uvicorn Sleep Issue Example

This project demonstrates and reproduces the Event Loop blocking problem (Sleep Issue) that can occur when writing asynchronous (`async`) routes in `django-ninja` with `uvicorn`. It simulates a critical server failure where invoking synchronous, blocking functions like `time.sleep()` within an `async def` router prevents the server from processing any other requests. This highlights the dangers of using blocking I/O or heavy, non-time-sliced computations in asynchronous environments.

## Results Summary (Based on 5 Concurrent Requests)

> Detailed execution logs (including thread information and elapsed time) can be found in [`log.md`](log.md).

### 1. Uvicorn Environment (ASGI, Production Environment)
A fatal problem occurs when executing blocking I/O within asynchronous code in Uvicorn, simulating a real production environment.

| API Endpoint | Function Type | Server Status | Execution Thread | Time (5 Requests) | Evaluation |
| --- | --- | --- | --- | --- | --- |
| `GET /api/sleep` | Synchronous (`def`) | Normal | `ThreadPoolExecutor` | 1.13 | Immediatley processed in parallel, distributed across the thread pool |
| `GET /api/async-sleep` | Asynchronous (`async def`) | **Failure Occurred** | `MainThread` | **5.16 sec** | Event loop is blocked; requests are processed sequentially (Bottleneck) |

* **Uvicorn Caveat**: If synchronous blocking code like `time.sleep()` is used inside an `async def` endpoint, Uvicorn's entire `MainThread` is locked. Since each request enforces a 1-second delay, serious latency escalates.

### 2. Django WSGI Environment (Built-in Server and Test Client)
Conversely, in development or testing environments using the built-in Django server (`manage.py runserver`, WSGI) or test clients, this flaw remains hidden. The server naturally delegates these requests to a thread pool, masking the async limitation.

| API Endpoint | Function Type | Server Status | Execution Thread | Time (5 Requests) | Evaluation |
| --- | --- | --- | --- | --- | --- |
| `GET /api/sleep` | Synchronous (`def`) | Normal | `ThreadPoolExecutor` | 1.00 sec | Processed in parallel successfully |
| `GET /api/async-sleep` | Asynchronous (`async def`) | Normal | `ThreadPoolExecutor` | 1.01 sec | Bottlenecks are completely hidden due to WSGI thread-pool behavior |

* **The Development Environment Trap**: Built-in development servers will often fall back to thread pools, completely masking the fact that your `async` route is blocking the overarching server loop. To detect potential bottlenecks, you must test identical asynchronous configurations in your production ASGI server (e.g., Uvicorn).

## Key Points

This project targets the severe response delay triggered when synchronous blocking I/O functions (e.g., `time.sleep()`) are evaluated inside an `async def` endpoint within an ASGI server like Uvicorn.

> **Note**: Uvicorn fundamentally operates on a **single-thread-per-worker (1 Thread)** basis. The asynchronous Event Loop executing on this single thread manages all incoming requests. Therefore, if the main thread gets blocked, the entire worker falls into a deadlock state, unable to accept or process any concurrent traffic.

### API Endpoints (`apidemo/router/api.py`)

1. **`GET /api/sleep`** 
   - Implemented as a standard synchronous function (`def`).
   - Internally executes `time.sleep()`.
   - By leveraging Django/Ninja's synchronous process flow, it delegates the execution to an isolated thread (Thread Pool), safely avoiding blocking the main event loop.
   
2. **`GET /api/async-sleep`**
   - Implemented as an asynchronous function (`async def`).
   - Specifically invokes the synchronous `time.sleep()` inside.
   - The blocking synchronous code acts directly within a coroutine, **intercepting and blocking Uvicorn's main event loop**. Consequently, the server goes offline for any concurrent requests until the process releases the lock.

## How to Run

### Requirements
- Environment setup and package dependencies are managed via `uv`.
- Review `mise.toml` for targeting specific Python versions and deep dependency details.

### Install Dependencies
```bash
uv venv
uv pip install -r requirements.txt
```

### Start the Server
Launch the application asynchronously via ASGI using Uvicorn:

```bash
uvicorn apidemo.asgi:application --reload
```

## Solutions

When executing blocking I/O inside asynchronous frameworks such as FastAPI or Django Ninja, opt for one of the following methods to ensure non-blocking execution:
1. Swap synchronous methods with genuine asynchronous awaitable functions (e.g., replace `time.sleep()` with `asyncio.sleep()`).
2. Utilize native thread-wrapping functions such as `sync_to_async` to explicitly delegate blocking segments to a standard thread pool.
3. Simply keep the endpoint fully synchronous (`def`) so the native framework automatically offloads it to a background thread block.


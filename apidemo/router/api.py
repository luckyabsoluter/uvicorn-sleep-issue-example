import threading
import time
from ninja import NinjaAPI

api = NinjaAPI()

PRINT = True
SLEEP_TIME = 1

def log(message):
    if PRINT:
        print(message)

@api.get("/sleep")
def sleep(request):
    log(f"Received request, sleeping... thread: {threading.current_thread().name}")
    start = time.time()
    time.sleep(SLEEP_TIME)
    end = time.time()
    log(f"Finished sleeping. thread: {threading.current_thread().name}")
    return {"start": start, "end": end, "duration": end - start}

@api.get("/async-sleep")
async def async_sleep(request):
    return sleep(request)

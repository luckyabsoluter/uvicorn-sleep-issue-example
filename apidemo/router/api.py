import threading
import time
from ninja import NinjaAPI

api = NinjaAPI()

SLEEP_TIME = 1

@api.get("/sleep")
def sleep(request):
    print(f"Received request, sleeping... thread: {threading.current_thread().name}")
    start = time.time()
    time.sleep(SLEEP_TIME)
    end = time.time()
    print(f"Finished sleeping. thread: {threading.current_thread().name}")
    return {"start": start, "end": end, "duration": end - start}

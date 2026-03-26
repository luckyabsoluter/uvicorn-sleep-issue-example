import time
from ninja import NinjaAPI

api = NinjaAPI()

SLEEP_TIME = 1

@api.get("/sleep")
def sleep(request):
    start = time.time()
    time.sleep(SLEEP_TIME)
    end = time.time()
    return {"start": start, "end": end, "duration": end - start}

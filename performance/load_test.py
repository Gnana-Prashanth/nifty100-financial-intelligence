import threading
import requests
import time

URL = "http://127.0.0.1:8000/api/v1/screener"

response_times = []
errors = []


def worker(thread_id):
    start = time.perf_counter()

    try:
        response = requests.get(URL)

        elapsed = time.perf_counter() - start

        response_times.append(elapsed)

        print(
            f"Thread {thread_id}: "
            f"{response.status_code} "
            f"{elapsed:.3f} sec"
        )

    except Exception as e:
        errors.append(str(e))


threads = []

overall_start = time.perf_counter()

for i in range(10):
    t = threading.Thread(
        target=worker,
        args=(i + 1,)
    )

    threads.append(t)
    t.start()

for t in threads:
    t.join()

overall_end = time.perf_counter()

print("\n==========================")
print("LOAD TEST SUMMARY")
print("==========================")

print(f"Total Requests : {len(response_times)}")
print(f"Failures       : {len(errors)}")
print(f"Total Time     : {overall_end - overall_start:.3f} sec")

if response_times:
    print(
        f"Average        : "
        f"{sum(response_times)/len(response_times):.3f} sec"
    )
    print(f"Fastest        : {min(response_times):.3f} sec")
    print(f"Slowest        : {max(response_times):.3f} sec")

if errors:
    print("\nErrors:")
    for e in errors:
        print(e)

#uvicorn src.api.main:app --reload --port 8000
#python performance/load_test.py
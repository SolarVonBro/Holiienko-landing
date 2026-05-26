import time
import random
import sys

DATA_SIZE = 100
REQUEST_COUNT = 1000
DELAY = 0.001
RUNS = 5

database = {
    i: f"data_value_{i}"
    for i in range(1, DATA_SIZE + 1)
}

def load_from_database(key):
    time.sleep(DELAY)
    return database.get(key)

def process_without_cache(requests):
    results = []
    db_calls = 0

    start = time.perf_counter()

    for key in requests:
        result = load_from_database(key)
        db_calls += 1
        results.append(result)

    end = time.perf_counter()

    return {
        "results": results,
        "time_ms": (end - start) * 1000,
        "db_calls": db_calls
    }

def process_with_cache(requests):
    results = []
    cache = {}
    cache_hits = 0
    db_calls = 0

    start = time.perf_counter()

    for key in requests:
        if key in cache:
            result = cache[key]
            cache_hits += 1
        else:
            result = load_from_database(key)
            cache[key] = result
            db_calls += 1

        results.append(result)

    end = time.perf_counter()

    cache_memory = sys.getsizeof(cache)

    return {
        "results": results,
        "time_ms": (end - start) * 1000,
        "cache_hits": cache_hits,
        "db_calls": db_calls,
        "cache_size": len(cache),
        "cache_memory_bytes": cache_memory
    }

random.seed(42)

requests = [
    random.randint(1, DATA_SIZE)
    for _ in range(REQUEST_COUNT)
]

summary = []

for run in range(1, RUNS + 1):
    no_cache = process_without_cache(requests)
    with_cache = process_with_cache(requests)

    is_correct = no_cache["results"] == with_cache["results"]

    speedup = no_cache["time_ms"] / with_cache["time_ms"]
    hit_rate = with_cache["cache_hits"] / REQUEST_COUNT * 100

    summary.append({
        "run": run,
        "time_no_cache": round(no_cache["time_ms"], 2),
        "time_cache": round(with_cache["time_ms"], 2),
        "speedup": round(speedup, 2),
        "hit_rate": round(hit_rate, 2),
        "db_calls_no_cache": no_cache["db_calls"],
        "db_calls_cache": with_cache["db_calls"],
        "cache_size": with_cache["cache_size"],
        "cache_memory_bytes": with_cache["cache_memory_bytes"],
        "correct": is_correct
    })

print("Результаты эксперимента:")
for item in summary:
    print(item)

avg_no_cache = sum(item["time_no_cache"] for item in summary) / RUNS
avg_cache = sum(item["time_cache"] for item in summary) / RUNS
avg_speedup = sum(item["speedup"] for item in summary) / RUNS
avg_hit_rate = sum(item["hit_rate"] for item in summary) / RUNS

print("\nСредние значения:")
print(f"Среднее время без кэша: {avg_no_cache:.2f} мс")
print(f"Среднее время с кэшем: {avg_cache:.2f} мс")
print(f"Среднее ускорение: {avg_speedup:.2f} раз")
print(f"Средний Hit Rate: {avg_hit_rate:.2f}%")
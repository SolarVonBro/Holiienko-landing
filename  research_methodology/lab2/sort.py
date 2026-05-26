import random
import time
import sys

sys.setrecursionlimit(1000000)


def bubble_sort(arr):
    a = arr.copy()
    n = len(a)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True

        if not swapped:
            break

    return a


def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def measure_time(sort_function, arr, repeats=3):
    results = []

    for _ in range(repeats):
        start = time.perf_counter()
        sort_function(arr)
        end = time.perf_counter()
        results.append(end - start)

    return sum(results) / len(results)


sizes = [1000, 5000, 10000, 20000]

print("Размер массива | Bubble Sort | Quick Sort")

for size in sizes:
    data = [random.randint(0, 100000) for _ in range(size)]

    bubble_time = measure_time(bubble_sort, data)
    quick_time = measure_time(quick_sort, data)

    print(f"{size:14d} | {bubble_time:11.5f} | {quick_time:10.5f}")
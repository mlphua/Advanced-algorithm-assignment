"""Question 3: Fibonacci with and without multithreading.

Time_Elapsed = (end time of the thread that finished last)
             - (start time of the thread that started first)
All times are in nanoseconds from time.perf_counter_ns().
"""
import threading
import time

NUMBERS = [35, 38, 40]
ROUNDS = 10


def fibonacci(n):
    """Naive recursive Fibonacci: T(n) = T(n-1) + T(n-2) + c  ->  O(2^n)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def worker(n, results, index):
    """Thread body: compute fib(n) and record its own start/end times."""
    start = time.perf_counter_ns()
    value = fibonacci(n)
    end = time.perf_counter_ns()
    results[index] = (value, start, end)


def run_multithreaded():
    results = [None] * len(NUMBERS)
    threads = [threading.Thread(target=worker, args=(n, results, i))
               for i, n in enumerate(NUMBERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t1 = min(r[1] for r in results)    # start of the thread that started first
    t2 = max(r[2] for r in results)    # end of the thread that finished last
    return t2 - t1, [r[0] for r in results]


def run_sequential():
    start = time.perf_counter_ns()
    values = [fibonacci(n) for n in NUMBERS]
    return time.perf_counter_ns() - start, values


def experiment(title, runner):
    print(f"\n=== {title} ===")
    times = []
    for rnd in range(1, ROUNDS + 1):
        elapsed, values = runner()
        times.append(elapsed)
        print(f"Round {rnd:>2}: T = {elapsed:>16,} ns  ({elapsed / 1e9:.3f} s)")
    total = sum(times)
    average = total / ROUNDS
    print(f"Total time   : {total:>16,} ns")
    print(f"Average of T : {average:>16,.0f} ns  ({average / 1e9:.3f} s)")
    print("Results      : " + ", ".join(f"fib({n}) = {v:,}" for n, v in zip(NUMBERS, values)))
    return average


def main():
    multi = experiment("WITH multithreading (3 threads)", run_multithreaded)
    single = experiment("WITHOUT multithreading (sequential)", run_sequential)
    print("\n=== Comparison ===")
    print(f"Multithreaded average : {multi:>16,.0f} ns")
    print(f"Sequential average    : {single:>16,.0f} ns")
    print(f"Sequential / Multithreaded = {single / multi:.2f}x")


if __name__ == "__main__":
    main()

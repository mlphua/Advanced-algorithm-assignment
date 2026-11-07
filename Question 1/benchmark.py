"""Q1 experiment: search performance of Hash Table vs one-dimensional array.

For each data size N the SAME N products are put in both structures and the
SAME search keys are used on both. Hits (keys that exist) and misses (keys that
do not) are timed separately.
"""
import random
import time
from hash_table import HashTable
from product import Product
from inventory import linear_search


def next_prime(n):
    def is_prime(x):
        if x < 2:
            return False
        i = 2
        while i * i <= x:
            if x % i == 0:
                return False
            i += 1
        return True
    while not is_prime(n):
        n += 1
    return n


def time_searches(func, keys, repeats=3):
    """Average nanoseconds per search over several repeats."""
    best = []
    for _ in range(repeats):
        t0 = time.perf_counter_ns()
        for k in keys:
            func(k)
        best.append((time.perf_counter_ns() - t0) / len(keys))
    return sum(best) / len(best)


def run(n, queries, rng):
    queries = min(queries, n)
    ids = rng.sample(range(10_000, 10_000_000), n + queries)
    stored, missing = ids[:n], ids[n:]
    table = HashTable(next_prime(n * 2))            # load factor ~0.5
    array = []
    for pid in stored:
        p = Product(pid, f"Item {pid}", 1.0, 1)
        table.insert(pid, p)
        array.append(p)

    hits = rng.sample(stored, queries)
    hash_hit = time_searches(table.search, hits)
    arr_hit = time_searches(lambda k: linear_search(array, k), hits)
    hash_miss = time_searches(table.search, missing)
    arr_miss = time_searches(lambda k: linear_search(array, k), missing)

    probes = 0
    for k in hits:
        table.search(k)
        probes += table.last_probes
    return hash_hit, arr_hit, hash_miss, arr_miss, probes / len(hits)


def main():
    rng = random.Random(42)  # fixed seed -> repeatable data
    print(f"{'N':>7} | {'Hash hit':>10} {'Array hit':>11} {'Speed-up':>9} | "
          f"{'Hash miss':>10} {'Array miss':>11} {'Speed-up':>9} | {'Avg probes':>10}")
    print("-" * 98)
    for n, q in [(100, 500), (1000, 500), (10000, 300), (50000, 100)]:
        hh, ah, hm, am, pr = run(n, q, rng)
        print(f"{n:>7} | {hh:>8.0f}ns {ah:>9.0f}ns {ah / hh:>8.0f}x | "
              f"{hm:>8.0f}ns {am:>9.0f}ns {am / hm:>8.0f}x | {pr:>10.2f}")
    print("\n(times are the average nanoseconds per single search)")


if __name__ == "__main__":
    main()
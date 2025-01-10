import os
import timeit

# Constants for benchmarking
ITERATIONS = 10
ROUNDS = 1000000

# Import cache implementations
from algos import sieve_cache, lru_cache, fifo_cache

# Cached functions for benchmarking
@sieve_cache(maxsize=128)
def func_sieve(obj):
    return obj

@lru_cache(maxsize=128)
def func_lru(obj):
    return obj

@fifo_cache(maxsize=128)
def func_fifo(obj):
    return obj

# Baseline Benchmark (No-op Function)
def no_op():
    pass

def run_timeit_benchmarks():
    print("\nTimeit Benchmarks:")

    print(f"\nBaseline Test ({ROUNDS} rounds):")
    baseline = timeit.timeit('no_op()', setup="from __main__ import no_op", number=ROUNDS)
    print(f"No-op Baseline: {baseline:.6f} seconds")
    print(f"Average time per round: {baseline/ROUNDS:.9f} seconds")

    print(f"\nCache Hit Tests ({ROUNDS} rounds, {ITERATIONS} iterations each):")
    hit_setup = """
from __main__ import func_sieve, func_lru, func_fifo, ITERATIONS
# Warm up the cache
func_sieve(1)
func_lru(1)
func_fifo(1)

def hit_test(func):
    for _ in range(ITERATIONS):
        func(1)
"""

    sieve_hit = timeit.timeit('hit_test(func_sieve)', setup=hit_setup, number=ROUNDS)
    lru_hit = timeit.timeit('hit_test(func_lru)', setup=hit_setup, number=ROUNDS)
    fifo_hit = timeit.timeit('hit_test(func_fifo)', setup=hit_setup, number=ROUNDS)

    print("\nTotal time for all rounds:")
    print(f"Sieve Cache Hit: {sieve_hit:.6f} seconds")
    print(f"LRU Cache Hit: {lru_hit:.6f} seconds")
    print(f"FIFO Cache Hit: {fifo_hit:.6f} seconds")

    print("\nAverage time per round:")
    print(f"Sieve Cache Hit: {sieve_hit/ROUNDS:.9f} seconds")
    print(f"LRU Cache Hit: {lru_hit/ROUNDS:.9f} seconds")
    print(f"FIFO Cache Hit: {fifo_hit/ROUNDS:.9f} seconds")

    print(f"\nCache Miss Tests ({ROUNDS} rounds, {ITERATIONS} iterations each):")
    miss_setup = """
from __main__ import func_sieve, func_lru, func_fifo, ITERATIONS

def miss_test(func):
    for i in range(ITERATIONS):
        func(i)
"""

    sieve_miss = timeit.timeit('miss_test(func_sieve)', setup=miss_setup, number=ROUNDS)
    lru_miss = timeit.timeit('miss_test(func_lru)', setup=miss_setup, number=ROUNDS)
    fifo_miss = timeit.timeit('miss_test(func_fifo)', setup=miss_setup, number=ROUNDS)

    print("\nTotal time for all rounds:")
    print(f"Sieve Cache Miss: {sieve_miss:.6f} seconds")
    print(f"LRU Cache Miss: {lru_miss:.6f} seconds")
    print(f"FIFO Cache Miss: {fifo_miss:.6f} seconds")

    print("\nAverage time per round:")
    print(f"Sieve Cache Miss: {sieve_miss/ROUNDS:.9f} seconds")
    print(f"LRU Cache Miss: {lru_miss/ROUNDS:.9f} seconds")
    print(f"FIFO Cache Miss: {fifo_miss/ROUNDS:.9f} seconds")

if __name__ == "__main__":
    run_timeit_benchmarks()

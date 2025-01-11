import os
import timeit
import statistics

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

    # Baseline Benchmark
    print(f"\nBaseline Test ({ROUNDS} rounds):")
    baseline_times = [timeit.timeit('no_op()', setup="from __main__ import no_op", number=ROUNDS) for _ in range(ITERATIONS)]
    baseline_avg = statistics.mean(baseline_times)
    baseline_std = statistics.stdev(baseline_times) if len(baseline_times) > 1 else 0
    
    print(f"No-op Baseline: Avg = {baseline_avg:.6f} seconds, Std Dev = {baseline_std:.6f} seconds")
    print(f"Average time per round: {baseline_avg/ROUNDS:.9f} seconds")

    # Hit Tests
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

    # Benchmark hit tests for each cache type
    def benchmark_hits(func_name):
        times = [
            timeit.timeit(f'hit_test({func_name})', setup=hit_setup, number=ROUNDS) 
            for _ in range(ITERATIONS)
        ]
        avg_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        return avg_time, std_dev

    sieve_hit_avg, sieve_hit_std = benchmark_hits('func_sieve')
    lru_hit_avg, lru_hit_std = benchmark_hits('func_lru')
    fifo_hit_avg, fifo_hit_std = benchmark_hits('func_fifo')

    print("\nCache Hit Results:")
    print(f"Sieve Cache Hit: Avg = {sieve_hit_avg:.6f} s, Std Dev = {sieve_hit_std:.6f} s")
    print(f"LRU Cache Hit: Avg = {lru_hit_avg:.6f} s, Std Dev = {lru_hit_std:.6f} s")
    print(f"FIFO Cache Hit: Avg = {fifo_hit_avg:.6f} s, Std Dev = {fifo_hit_std:.6f} s")

    print("\nAverage time per round:")
    print(f"Sieve Cache Hit: {sieve_hit_avg/ROUNDS:.9f} s")
    print(f"LRU Cache Hit: {lru_hit_avg/ROUNDS:.9f} s")
    print(f"FIFO Cache Hit: {fifo_hit_avg/ROUNDS:.9f} s")

    # Miss Tests
    print(f"\nCache Miss Tests ({ROUNDS} rounds, {ITERATIONS} iterations each):")
    miss_setup = """
from __main__ import func_sieve, func_lru, func_fifo, ITERATIONS

def miss_test(func):
    for i in range(ITERATIONS):
        func(i)
"""

    # Benchmark miss tests for each cache type
    def benchmark_misses(func_name):
        times = [
            timeit.timeit(f'miss_test({func_name})', setup=miss_setup, number=ROUNDS) 
            for _ in range(ITERATIONS)
        ]
        avg_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        return avg_time, std_dev

    sieve_miss_avg, sieve_miss_std = benchmark_misses('func_sieve')
    lru_miss_avg, lru_miss_std = benchmark_misses('func_lru')
    fifo_miss_avg, fifo_miss_std = benchmark_misses('func_fifo')

    print("\nCache Miss Results:")
    print(f"Sieve Cache Miss: Avg = {sieve_miss_avg:.6f} s, Std Dev = {sieve_miss_std:.6f} s")
    print(f"LRU Cache Miss: Avg = {lru_miss_avg:.6f} s, Std Dev = {lru_miss_std:.6f} s")
    print(f"FIFO Cache Miss: Avg = {fifo_miss_avg:.6f} s, Std Dev = {fifo_miss_std:.6f} s")

    print("\nAverage time per round:")
    print(f"Sieve Cache Miss: {sieve_miss_avg/ROUNDS:.9f} s")
    print(f"LRU Cache Miss: {lru_miss_avg/ROUNDS:.9f} s")
    print(f"FIFO Cache Miss: {fifo_miss_avg/ROUNDS:.9f} s")

if __name__ == "__main__":
    run_timeit_benchmarks()

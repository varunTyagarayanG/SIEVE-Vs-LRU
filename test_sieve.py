import os
from algos import sieve_cache, lru_cache, fifo_cache

# Constants for benchmarking
ITERATIONS = 10
ROUNDS = 1000000

# Test Functions
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

# Pytest Benchmarking Functions
def sieve_cache_test_hit():
    for _ in range(ITERATIONS):
        func_sieve(1)

def test_sieve_hit(benchmark):
    # Warm up cache
    func_sieve(1)
    benchmark.pedantic(sieve_cache_test_hit, iterations=ITERATIONS, rounds=ROUNDS)

def lru_cache_test_hit():
    for _ in range(ITERATIONS):
        func_lru(1)

def test_lru_hit(benchmark):
    # Warm up cache
    func_lru(1)
    benchmark.pedantic(lru_cache_test_hit, iterations=ITERATIONS, rounds=ROUNDS)

def fifo_cache_test_hit():
    for _ in range(ITERATIONS):
        func_fifo(1)

def test_fifo_hit(benchmark):
    # Warm up cache
    func_fifo(1)
    benchmark.pedantic(fifo_cache_test_hit, iterations=ITERATIONS, rounds=ROUNDS)

def sieve_cache_test_miss():
    for i in range(ITERATIONS):
        func_sieve(i)

def test_sieve_miss(benchmark):
    benchmark.pedantic(sieve_cache_test_miss, iterations=ITERATIONS, rounds=ROUNDS)

def lru_cache_test_miss():
    for i in range(ITERATIONS):
        func_lru(i)

def test_lru_miss(benchmark):
    benchmark.pedantic(lru_cache_test_miss, iterations=ITERATIONS, rounds=ROUNDS)

def fifo_cache_test_miss():
    for i in range(ITERATIONS):
        func_fifo(i)

def test_fifo_miss(benchmark):
    benchmark.pedantic(fifo_cache_test_miss, iterations=ITERATIONS, rounds=ROUNDS)

if __name__ == "__main__":
    # Run pytest benchmarks
    print("\nRunning Pytest Benchmarks...")
    os.system("pytest --benchmark-only --benchmark-save=benchmark_results")

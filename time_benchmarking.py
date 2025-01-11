import time
import statistics
import timeit
from algos import sieve_cache, lru_cache, fifo_cache

# Constants for benchmarking
ITERATIONS = 10
ROUNDS = 1000000

# Test function to be cached
def sample_function(obj):
    return obj

# Decorate functions with different cache mechanisms
@sieve_cache(maxsize=128)
def func_sieve(obj):
    return sample_function(obj)

@lru_cache(maxsize=128)
def func_lru(obj):
    return sample_function(obj)

@fifo_cache(maxsize=128)
def func_fifo(obj):
    return sample_function(obj)

def no_op():
    pass

def benchmark(func, test_type, iterations, rounds):
    """
    Benchmark a function with either hit or miss test type.
    
    Args:
        func (callable): Function to benchmark
        test_type (str): 'hit' or 'miss' test
        iterations (int): Number of iterations
        rounds (int): Number of rounds per iteration
    
    Returns:
        tuple: Average time and standard deviation
    """
    timings = []
    
    # Warm up cache for hit tests
    if test_type == "hit":
        func(1)
    
    for _ in range(iterations):
        start_time = time.perf_counter()
        
        if test_type == "hit":
            for _ in range(rounds):
                func(1)
        elif test_type == "miss":
            for i in range(rounds):
                func(i)
        
        end_time = time.perf_counter()
        timings.append(end_time - start_time)
    
    # Calculate statistics
    avg_time = statistics.mean(timings)
    std_dev = statistics.stdev(timings) if len(timings) > 1 else 0
    
    return avg_time, std_dev

def run_benchmarks():
    """Run comprehensive benchmarks for different cache mechanisms."""
    print("\nBenchmarking Results:")
    
    # Baseline (No-op) Benchmark
    baseline = timeit.timeit('no_op()', setup="from __main__ import no_op", number=ROUNDS)
    print(f"\nBaseline Test ({ROUNDS} rounds):")
    print(f"No-op Baseline: {baseline:.6f} seconds")
    print(f"Average time per round: {baseline/ROUNDS:.9f} seconds")
    
    # Cache Hit Benchmarks
    print(f"\nCache Hit Tests ({ROUNDS} rounds, {ITERATIONS} iterations each):")
    sieve_hit_avg, sieve_hit_std = benchmark(func_sieve, "hit", ITERATIONS, ROUNDS)
    lru_hit_avg, lru_hit_std = benchmark(func_lru, "hit", ITERATIONS, ROUNDS)
    fifo_hit_avg, fifo_hit_std = benchmark(func_fifo, "hit", ITERATIONS, ROUNDS)
    
    print(f"Sieve Cache Hit: Avg = {sieve_hit_avg:.6f}s, Std Dev = {sieve_hit_std:.6f}s")
    print(f"LRU Cache Hit: Avg = {lru_hit_avg:.6f}s, Std Dev = {lru_hit_std:.6f}s")
    print(f"FIFO Cache Hit: Avg = {fifo_hit_avg:.6f}s, Std Dev = {fifo_hit_std:.6f}s")
    
    # Cache Miss Benchmarks
    print(f"\nCache Miss Tests ({ROUNDS} rounds, {ITERATIONS} iterations each):")
    sieve_miss_avg, sieve_miss_std = benchmark(func_sieve, "miss", ITERATIONS, ROUNDS)
    lru_miss_avg, lru_miss_std = benchmark(func_lru, "miss", ITERATIONS, ROUNDS)
    fifo_miss_avg, fifo_miss_std = benchmark(func_fifo, "miss", ITERATIONS, ROUNDS)
    
    print(f"Sieve Cache Miss: Avg = {sieve_miss_avg:.6f}s, Std Dev = {sieve_miss_std:.6f}s")
    print(f"LRU Cache Miss: Avg = {lru_miss_avg:.6f}s, Std Dev = {lru_miss_std:.6f}s")
    print(f"FIFO Cache Miss: Avg = {fifo_miss_avg:.6f}s, Std Dev = {fifo_miss_std:.6f}s")

if __name__ == "__main__":
    run_benchmarks()

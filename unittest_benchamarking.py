import unittest
import time
from algos import sieve_cache, lru_cache, fifo_cache

# Constants for benchmarking
ITERATIONS = 10
ROUNDS = 1000000

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

class TestCachePerformance(unittest.TestCase):
    def measure_time(self, func, test_type):
        timings = []
        for _ in range(ITERATIONS):
            start_time = time.time()
            if test_type == "hit":
                for _ in range(ROUNDS):
                    func(1)
            elif test_type == "miss":
                for i in range(ROUNDS):
                    func(i)
            end_time = time.time()
            timings.append(end_time - start_time)
        avg_time = sum(timings) / len(timings)
        std_dev = (sum((x - avg_time) ** 2 for x in timings) / len(timings)) ** 0.5
        return avg_time, std_dev

    def test_sieve_cache_hit(self):
        # Warm up the cache
        func_sieve(1)
        avg_time, std_dev = self.measure_time(func_sieve, "hit")
        print(f"\n* Sieve Cache Hit: Avg = {avg_time:.6f}s, Std Dev = {std_dev:.6f}s")

    def test_lru_cache_hit(self):
        # Warm up the cache
        func_lru(1)
        avg_time, std_dev = self.measure_time(func_lru, "hit")
        print(f"* LRU Cache Hit: Avg = {avg_time:.6f}s, Std Dev = {std_dev:.6f}s")

    def test_fifo_cache_hit(self):
        # Warm up the cache
        func_fifo(1)
        avg_time, std_dev = self.measure_time(func_fifo, "hit")
        print(f"* FIFO Cache Hit: Avg = {avg_time:.6f}s, Std Dev = {std_dev:.6f}s")

    def test_sieve_cache_miss(self):
        avg_time, std_dev = self.measure_time(func_sieve, "miss")
        print(f"\n* Sieve Cache Miss: Avg = {avg_time:.6f}s, Std Dev = {std_dev:.6f}s")

    def test_lru_cache_miss(self):
        avg_time, std_dev = self.measure_time(func_lru, "miss")
        print(f"* LRU Cache Miss: Avg = {avg_time:.6f}s, Std Dev = {std_dev:.6f}s")

    def test_fifo_cache_miss(self):
        avg_time, std_dev = self.measure_time(func_fifo, "miss")
        print(f"* FIFO Cache Miss: Avg = {avg_time:.6f}s, Std Dev = {std_dev:.6f}s")

if __name__ == "__main__":
    unittest.main()

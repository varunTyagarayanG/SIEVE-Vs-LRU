# SIEVE Cache Eviction Algorithm with Benchmarking

## Overview

This implementation introduces the SIEVE cache eviction algorithm alongside a custom implementation of the LRU (Least Recently Used) cache eviction policy. Both caching mechanisms have been benchmarked using Python's `pytest-benchmark` library.

### Key Features of SIEVE
1. **Lazy Promotion:** Items in the cache are not promoted unnecessarily, optimizing performance.
2. **Quick Demotion:** Items can be efficiently evicted when needed.
3. **Thread-Safety:** SIEVE does not require locks for cache hits, unlike LRU, resulting in increased throughput.

### Benchmark Output
![Benchmark Results](Images/image.png)

### Analysis of Benchmark Results

The benchmark results provide insights into the performance of the SIEVE and LRU cache eviction algorithms:

1. **Cache Hits**
   - **SIEVE**: The SIEVE algorithm shows a lower mean time (0.0004 ms) compared to LRU (0.0006 ms) for cache hits. This indicates that SIEVE is slightly faster in retrieving items from the cache, likely due to its lazy promotion feature, which reduces unnecessary operations.
   - **LRU**: While slightly slower, LRU's performance is still competitive. However, the higher standard deviation (0.0003 ms) suggests more variability in response time compared to SIEVE (0.0001 ms).

2. **Cache Misses**
   - **SIEVE**: For cache misses, SIEVE has a mean time of 0.6657 ms, which is slightly better than LRU's 0.6837 ms. This efficiency is attributed to SIEVE's quick demotion strategy that efficiently identifies and evicts unvisited items.
   - **LRU**: The LRU algorithm, while slightly slower, is still a robust choice for scenarios where cache misses are less frequent.

3. **Operations Per Second (OPS)**
   - The OPS metric further highlights SIEVE's advantage in both cache hits and misses, with higher operations per second compared to LRU.

### Conclusion

The SIEVE algorithm demonstrates superior performance in both cache hits and misses, making it a more efficient choice for scenarios requiring high throughput and low latency. Its design optimizes cache operations by minimizing unnecessary promotions and efficiently handling evictions. LRU, while slightly less performant, remains a viable option, especially in environments where its simplicity and predictability are preferred.

---

## Code Details

### SIEVE Cache Implementation
The `sieve_cache` decorator uses the SIEVE algorithm to optimize cache performance. The cache maintains a doubly linked list to track access patterns and efficiently evict entries.

#### Key Highlights
- **Lazy Promotion:** Items are marked as visited without altering their positions.
- **Quick Demotion:** A traversal identifies unvisited items for eviction.
- **Thread-Safe:** Ensures safe concurrent access with `_thread.RLock`.

### LRU Cache Implementation
The custom `lru_cache` decorator uses a circular doubly linked list to implement the traditional LRU cache eviction policy.

#### Key Highlights
- **Promotion on Access:** Recently accessed items are moved to the front.
- **Eviction Policy:** Oldest items are evicted when the cache reaches capacity.

---

## Functions

### SIEVE Cache Functions
1. **`sieve_cache(maxsize=128):`**
   - A decorator for caching functions with the SIEVE eviction policy.
   - **Arguments:** `maxsize` (default=128) determines the maximum cache size.

2. **`_sieve_wrapper(user_func, maxsize):`**
   - Core function implementing the SIEVE cache logic.

### LRU Cache Functions
1. **`lru_cache(maxsize=128):`**
   - A decorator for caching functions with the LRU eviction policy.
   - **Arguments:** `maxsize` (default=128) determines the maximum cache size.

2. **`_my_lru_wrapper(user_func, maxsize):`**
   - Core function implementing the LRU cache logic.

---

## Benchmarking
The benchmarking tests measure the performance of cache hits and misses for both SIEVE and LRU implementations. `pytest-benchmark` is used for this purpose.


### Benchmarking Functions
1. **SIEVE Tests**
   - **`sieve_cache_test_hit:`** Tests cache hits for SIEVE.
   - **`sieve_cache_test_miss:`** Tests cache misses for SIEVE.

2. **LRU Tests**
   - **`lru_cache_test_hit:`** Tests cache hits for LRU.
   - **`lru_cache_test_miss:`** Tests cache misses for LRU.

### Installation
Before running the benchmarks, ensure you have the necessary dependencies installed:

```bash
pip install pytest pytest-benchmark
```

### Command to Run Benchmarks
Run the following command to execute benchmarks and save results:
```bash
pytest --benchmark-save=benchmark_results
```

---

# SIEVE Cache Eviction Algorithm with Benchmarking

## Overview

This implementation introduces the SIEVE cache eviction algorithm alongside a custom implementation of the LRU (Least Recently Used) cache eviction policy. Both caching mechanisms have been benchmarked using Python's `pytest-benchmark` library.

### Key Features of SIEVE
1. **Lazy Promotion:** Items in the cache are not promoted unnecessarily, optimizing performance.
2. **Quick Demotion:** Items can be efficiently evicted when needed.
3. **Thread-Safety:** SIEVE does not require locks for cache hits, unlike LRU, resulting in increased throughput.

# Benchmarking Observations

## **Pytest Benchmark Results**
![Benchmark Results](./Images/pytest-benchmakring-results.png)

### Cache Hits:
1. **Sieve Cache Hit**:
   - Min: **0.0023 ms**
   - Max: **0.3640 ms**
   - Mean: **0.0025 ms** (fastest among all hits, with a relative speed of **1.0**).
   - Operations per second (OPS): **393.170 Kops/s**

2. **FIFO Cache Hit**:
   - Min: **0.0030 ms**
   - Max: **0.4003 ms**
   - Mean: **0.0041 ms** (relative speed of **1.63**).
   - OPS: **241.477 Kops/s**

3. **LRU Cache Hit**:
   - Min: **0.0058 ms**
   - Max: **0.6672 ms**
   - Mean: **0.0085 ms** (relative speed of **2.27**, slowest among hits).
   - OPS: **173.0866 Kops/s**

### Cache Misses:
1. **Sieve Cache Miss**:
   - Min: **0.0023 ms**
   - Max: **0.0231 ms**
   - Mean: **0.0023 ms** (relative speed of **1.0**, tied with the fastest miss).
   - OPS: **353.069 Kops/s**

2. **FIFO Cache Miss**:
   - Min: **0.0030 ms**
   - Max: **0.0643 ms**
   - Mean: **0.0041 ms** (relative speed of **1.63**).
   - OPS: **255.556 Kops/s**

3. **LRU Cache Miss**:
   - Min: **0.0039 ms**
   - Max: **0.1729 ms**
   - Mean: **0.0051 ms** (relative speed of **2.01**, slowest among misses).
   - OPS: **195.3724 Kops/s**

### Summary:
- **Sieve Cache** is the fastest for both hits and misses, with the highest OPS.
- **LRU Cache** is the slowest in all cases, with the lowest OPS.

---

## **TimeIt Benchmark Results**
![Benchmark Results](./Images/TimeIt-benchmarking-results.png)

### Baseline:
- **No-op Baseline**:
  - Total Time: **0.026296 seconds**
  - Average Time Per Round: **0.000000026 seconds**

### Cache Hits:
1. **Sieve Cache Hit**:
   - Total Time: **2.779958 seconds**
   - Average Time Per Round: **0.00002780 seconds**

2. **FIFO Cache Hit**:
   - Total Time: **3.820931 seconds**
   - Average Time Per Round: **0.00003821 seconds**

3. **LRU Cache Hit**:
   - Total Time: **4.940739 seconds**
   - Average Time Per Round: **0.00004941 seconds**

### Cache Misses:
1. **Sieve Cache Miss**:
   - Total Time: **2.780835 seconds**
   - Average Time Per Round: **0.00002780 seconds**

2. **FIFO Cache Miss**:
   - Total Time: **3.860705 seconds**
   - Average Time Per Round: **0.00003861 seconds**

3. **LRU Cache Miss**:
   - Total Time: **4.899257 seconds**
   - Average Time Per Round: **0.00004899 seconds**

### Summary:
- **Sieve Cache** consistently performs the best for both hits and misses, with the shortest total and average times.
- **LRU Cache** is the slowest across all categories.

---

## **Overall Best Cache**
- From both **Pytest** and **TimeIt** results, the **Sieve Cache** is clearly the best performer for hits and misses, showcasing the fastest execution times and highest operations per second.



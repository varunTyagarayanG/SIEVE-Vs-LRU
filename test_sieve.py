from functools import _make_key
from _thread import RLock

def _sieve_wrapper(user_func, maxsize):
    cache = {}
    tail = []
    full = None
    tail[:] = [
        tail, # PREV
        tail, # NEXT
        None, # KEY
        None, # RESULT
        None, # VISITED
    ]
    PREV, NEXT, KEY, RESULT, VISITED = 0, 1, 2, 3, 4

    make_key = _make_key
    cache_get = cache.get
    cache_len = cache.__len__
    lock = RLock()

    hand = tail

    def wrapper(*args, **kwargs):
        nonlocal tail, full, hand
        key = make_key(args, kwargs, typed=False)
        link = cache_get(key)
        if link is not None:
            link[VISITED] = True
            return link[RESULT]

        result = user_func(*args, **kwargs)
        with lock:
            # Cache miss
            if key in cache:
                # another thread might have already computed the value
                pass
            elif full:
                o = hand
                if o[KEY] is None:
                    o = tail[PREV]
                    
                while o[VISITED]:
                    o[VISITED] = False
                    o = o[PREV]
                    if o[KEY] is None:
                        o = tail[PREV]
                        
                # Evict o
                hand = o[PREV]
                oldkey = o[KEY]
                hand[NEXT] = o[NEXT]
                o[NEXT][PREV] = hand
                del cache[oldkey]

                # Insert at head of linked list
                head = tail[NEXT]
                new_head = [tail, head, key, result, True]
                head[PREV] = tail[NEXT] = cache[key] = new_head
            else:
                # Insert at head of linked list
                head = tail[NEXT]
                new_head = [tail, head, key, result, True]
                head[PREV] = tail[NEXT] = cache[key] = new_head
                full = (cache_len() >= maxsize)


        return result
    return wrapper

def sieve_cache(maxsize=128):
    def wrapper(user_func):
        w = _sieve_wrapper(user_func, maxsize)
        return w
    return wrapper

from functools import _make_key
from _thread import RLock

def _my_lru_wrapper(user_func, maxsize):
    cache = {}
    root = []
    full = None
    root[:] = [
        root, # PREV
        root, # NEXT
        None, # KEY
        None, # RESULT
    ]
    PREV, NEXT, KEY, RESULT = 0, 1, 2, 3

    make_key = _make_key
    cache_get = cache.get
    cache_len = cache.__len__ 
    lock = RLock()

    def wrapper(*args, **kwargs):
        nonlocal root, full
        key = make_key(args, kwargs, typed=False)
        with lock:
            link = cache_get(key) 
            if link is not None:
                # Move link to front of circular doubly linked list
                link_prev, link_next, key, result = link
                link_prev[NEXT] = link_next
                link_next[PREV] = link_prev
                last = root[PREV]
                last[NEXT] = root[PREV] = link
                link[PREV] = last
                link[NEXT] = root
                return result

        result = user_func(*args, **kwargs)
        with lock:
            # Cache miss
            if key in cache:
                # another thread might have already computed the value
                pass
            elif full:
                # Insert new key at root (which turns from a root node
                # into a regular one) and convert an existing node into
                # a root node (and "evict" it).
                #
                # All this dance is required to limit updates to just the
                # KEY and RESULT fields and avoid updating PREV/NEXT links.
                oldroot = root
                oldroot[KEY] = key
                oldroot[RESULT] = result
                root = oldroot[NEXT]
                oldkey = root[KEY]
                oldresult = root[RESULT]
                root[KEY] = root[RESULT] = None
                del cache[oldkey]
                cache[key] = oldroot
            else:
                # Insert at end head of linked list
                last = root[PREV]
                new_last = [last, root, key, result]
                last[NEXT] = root[PREV] = cache[key] = new_last
                full = (cache_len() >= maxsize)

        return result
    return wrapper

def lru_cache(maxsize=128):
    def wrapper(user_func):
        w = _my_lru_wrapper(user_func, maxsize)
        return w
    return wrapper

import os

@sieve_cache(maxsize=128)
def func_sieve(obj):
    return obj

@lru_cache(maxsize=128)
def func_lru(obj):
    return obj

def sieve_cache_test_hit():
    func_sieve(1)

def test_sieve_hit(benchmark):
    benchmark(sieve_cache_test_hit)

def lru_cache_test_hit():
    func_lru(1)

def test_lru_hit(benchmark):
    benchmark(lru_cache_test_hit)

def sieve_cache_test_miss():
    for i in range(1000):
        func_sieve(i)

def test_sieve_miss(benchmark):
    benchmark(sieve_cache_test_miss)

def lru_cache_test_hit():
    func_lru(1)

def lru_cache_test_miss():
    for i in range(1000):
        func_lru(i)

def test_lru_miss(benchmark):
    benchmark(lru_cache_test_miss)

if __name__ == "__main__":
    os.system("pytest --benchmark-save=benchmark_results")

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

def _fifo_wrapper(user_func, maxsize):
    cache = {}
    queue = []
    cache_get = cache.get
    cache_len = cache.__len__ 
    lock = RLock()

    def wrapper(*args, **kwargs):
        key = _make_key(args, kwargs, typed=False)
        with lock:
            link = cache_get(key)
            if link is not None:
                return link

        result = user_func(*args, **kwargs)
        with lock:
            # Cache miss
            if key in cache:
                pass
            elif cache_len() >= maxsize:
                # Evict the first inserted item (FIFO)
                oldest_key = queue.pop(0)
                del cache[oldest_key]

            # Add new item to the cache
            cache[key] = result
            queue.append(key)

        return result
    return wrapper

def fifo_cache(maxsize=128):
    def wrapper(user_func):
        w = _fifo_wrapper(user_func, maxsize)
        return w
    return wrapper

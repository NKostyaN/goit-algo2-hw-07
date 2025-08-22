import random
import time
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right, cache):
    key = (left, right)
    cached_result = cache.get(key)
    if cached_result != -1:
        return cached_result
    result = sum(array[left : right + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value, cache):
    array[index] = value
    keys_to_delete = [
        key for key in list(cache.cache.keys()) if key[0] <= index <= key[1]
    ]
    for key in keys_to_delete:
        del cache.cache[key]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% запитів — Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% — Range
            if random.random() < p_hot:  # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:  # 5% — випадкові діапазони
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


if __name__ == "__main__":
    array = [random.randint(1, 100) for _ in range(100000)]
    queries = make_queries(100000, 50000)

    array_no_cache = array.copy()
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array_no_cache, query[1], query[2])
        else:
            update_no_cache(array_no_cache, query[1], query[2])
    time_no_cache = time.time() - start

    array_cached = array.copy()
    cache = LRUCache(capacity=1000)
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array_cached, query[1], query[2], cache)
        else:
            update_with_cache(array_cached, query[1], query[2], cache)
    time_cached = time.time() - start

    mult = round(time_no_cache / time_cached, 2)

    print(f"Без кешу :  {time_no_cache:.2f} c")
    print(f"LRU-кеш  :  {time_cached:.2f} c  (прискорення ×{mult})")

import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from splay_tree import SplayTree


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    result = tree.search(n)
    if result is not None:
        return result
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


if __name__ == "__main__":
    n_values = list(range(0, 951, 50))

    lru_times = []
    for n in n_values:
        time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        lru_times.append(time)

    splay_times = []
    for n in n_values:
        tree = SplayTree()
        time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
        splay_times.append(time)

    print(f"{'n':<10}{'LRU Cache Time (s)':<24}{'Splay Tree Time (s)':<24}")
    print("-" * 53)
    for n, lru, splay in zip(n_values, lru_times, splay_times):
        print(f"{n:<10}{lru:<24.8f}{splay:<24.8f}")

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, marker=".", label="LRU Cache")
    plt.plot(n_values, splay_times, marker="o", label="Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(
        "\nМетод із використанням LRU-кешу показав низький час виконання навіть при чисельних ітераціях."
    )
    print(
        "Метод із використанням Splay Tree має вищу складність тож показав більший час виконання."
    )
    print("Отже для обчислення чисел Фібоначчі LRU-кеш буде ефективнішим.")

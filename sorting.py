# TODO: Quick, Merge, Shell, Heap

from typing import Any, Callable, TypeVar

# used for generics
T = TypeVar("T")

def bubble_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> list[T]:
    # Avg.: O(n^2), Best: O(n), Worst: O(n^2)

    sorted_list = sorting_list.copy()

    swapped = False
    for i in range(len(sorted_list) - 1):
        for j in range(len(sorted_list) - 1 - i):
            if not comparison_function(sorted_list[j], sorted_list[j + 1]):
                swapped = True
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
        
        if not swapped:
            break

    return sorted_list

def heap_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> list[T]:
    # Avg.: O(n*log(n)), Best: O(n*log(n)), Worst: O(n*log(n))

    def heapify(array: list[T], n: int, i: int) -> None:
        largest = i
        l = (2 * i) + 1
        r = (2 * i) + 2

        if (l < n) and comparison_function(array[largest], array[l]):
            largest = l

        if (r < n) and comparison_function(array[largest], array[r]):
            largest = r

        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            heapify(array, n, largest)

    sorted_list = sorting_list.copy()
    n = len(sorted_list)

    for i in range((n // 2) - 1, -1, -1):
        heapify(sorted_list, n, i)

    for i in range(n - 1, 0, -1):
        sorted_list[i], sorted_list[0] = sorted_list[0], sorted_list[i]
        heapify(sorted_list, i, 0)

    return sorted_list

def insertion_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> list[T]:
    # Avg.: O(n^2), Best: O(n), Worst: O(n^2)

    sorted_list = sorting_list.copy()
    for i in range(1, len(sorted_list)):
        key = sorted_list[i]

        j = i - 1
        while (j >= 0) and (not comparison_function(sorted_list[j], key)):
            sorted_list[j + 1] = sorted_list[j]
            j -= 1

        sorted_list[j + 1] = key

    return sorted_list

def selection_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> list[T]:
    # Avg.: O(n^2), Best: O(n^2), Worst: O(n^2)

    sorted_list = sorting_list.copy()
    for idx in range(len(sorted_list)):
        min_idx = idx
        for i in range(idx + 1, len(sorted_list)):
            if not comparison_function(sorted_list[i], sorted_list[min_idx]):
                min_idx = i

        sorted_list[idx], sorted_list[min_idx] = sorted_list[min_idx], sorted_list[idx]

    return sorted_list
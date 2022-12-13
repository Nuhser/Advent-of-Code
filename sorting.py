from typing import Any, Callable, TypeVar

# used for generics
T = TypeVar("T")

def bubble_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> None:
    # Avg.: O(n^2), Best: O(n), Worst: O(n^2)

    swapped = False
    for i in range(len(sorting_list) - 1):
        for j in range(len(sorting_list) - 1 - i):
            if not comparison_function(sorting_list[j], sorting_list[j + 1]):
                swapped = True
                sorting_list[j], sorting_list[j + 1] = sorting_list[j + 1], sorting_list[j]
        
        if not swapped:
            break


def heap_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> None:
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

    n = len(sorting_list)

    for i in range((n // 2) - 1, -1, -1):
        heapify(sorting_list, n, i)

    for i in range(n - 1, 0, -1):
        sorting_list[i], sorting_list[0] = sorting_list[0], sorting_list[i]
        heapify(sorting_list, i, 0)


def insertion_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> None:
    # Avg.: O(n^2), Best: O(n), Worst: O(n^2)

    for i in range(1, len(sorting_list)):
        key = sorting_list[i]

        j = i - 1
        while (j >= 0) and (not comparison_function(sorting_list[j], key)):
            sorting_list[j + 1] = sorting_list[j]
            j -= 1

        sorting_list[j + 1] = key


def merge_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> None:
    # Avg.: O(n*log(n)), Best: O(n*log(n)), Worst: O(n*log(n))

    if len(sorting_list) > 1:
        middle = len(sorting_list) // 2
        L = sorting_list[:middle]
        R = sorting_list[middle:]

        merge_sort(L, comparison_function)
        merge_sort(R, comparison_function)

        i = j = k = 0
        while (i < len(L)) and (j < len(R)):
            if not comparison_function(R[j], L[i]):
                sorting_list[k] = L[i]
                i += 1
            else:
                sorting_list[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            sorting_list[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            sorting_list[k] = R[j]
            j += 1
            k += 1

def quick_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)], low: int=0, high: (int | None)=None) -> None:
    # Avg.: O(n*log(n)), Best: O(n*log(n)), Worst: O(n^2)

    def partition(sorting_list: list[T], low: int, high: int) -> int:
        pivot = sorting_list[high]
        i = low - 1

        for j in range(low, high):
            if not comparison_function(pivot, sorting_list[j]):
                i += 1
                sorting_list[i], sorting_list[j] = sorting_list[j], sorting_list[i]

        sorting_list[i+1], sorting_list[high] = sorting_list[high], sorting_list[i+1]

        return i + 1

    if high == None:
        high = len(sorting_list) - 1

    if low < high:
        pivot_idx = partition(sorting_list, low, high)
        quick_sort(sorting_list, comparison_function, low, pivot_idx - 1)
        quick_sort(sorting_list, comparison_function, pivot_idx + 1, high)


def selection_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> None:
    # Avg.: O(n^2), Best: O(n^2), Worst: O(n^2)

    for idx in range(len(sorting_list)):
        min_idx = idx
        for i in range(idx + 1, len(sorting_list)):
            if not comparison_function(sorting_list[i], sorting_list[min_idx]):
                min_idx = i

        sorting_list[idx], sorting_list[min_idx] = sorting_list[min_idx], sorting_list[idx]
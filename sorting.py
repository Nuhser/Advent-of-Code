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
from typing import Any, Callable, TypeVar

# used for generics
T = TypeVar("T")

def bubble_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> list[T]:
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
from typing import TypeVar


T = TypeVar("T")


def flip_2d_list(original_list: list[list[T]]) -> list[list[T]]:
    if (len(set(len(row) for row in original_list)) > 1):
        raise ValueError("ERROR: All rows of 'original_list' need to have the same number of elements.")

    flipped_list: list[list[T]] = []

    for row in original_list:
        for i, element in enumerate(row):
            if (i >= len(flipped_list)):
                flipped_list.append([])

            flipped_list[i].append(element)

    return flipped_list

def flip_list_of_string(original_list: list[str]) -> list[str]:
    flipped_list = flip_2d_list([[c for c in s] for s in original_list])

    return ["".join(l) for l in flipped_list]
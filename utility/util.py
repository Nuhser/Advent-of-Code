from typing import Any


def convert_hex_to_bin(hex_string: str) -> str:
    return str(bin(int(hex_string, base=16)))[2:].zfill(4)


def count_elements_in_list(list: list[Any]) -> dict[Any, int]:
    return {key: list.count(key) for key in list}


def flip_2d_list[T](original_list: list[list[T]]) -> list[list[T]]:
    if len(set(len(row) for row in original_list)) > 1:
        raise ValueError(
            "ERROR: All rows of 'original_list' need to have the same number of elements."
        )

    flipped_list: list[list[T]] = []

    for row in original_list:
        for i, element in enumerate(row):
            if i >= len(flipped_list):
                flipped_list.append([])

            flipped_list[i].append(element)

    return flipped_list


def flip_list_of_string(original_list: list[str]) -> list[str]:
    flipped_list = flip_2d_list([[c for c in s] for s in original_list])

    return ["".join(l) for l in flipped_list]


def get_diff_between_strings(string1: str, string2: str) -> int:
    diff: int = abs(len(string1) - len(string2))

    for i in range(min(len(string1), len(string2))):
        if string1[i] != string2[i]:
            diff += 1

    return diff

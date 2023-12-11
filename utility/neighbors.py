from typing import Any, Callable, TypeVar


T = TypeVar("T")


def get_neighbor_coords_with_specific_directions(
        map: dict[tuple[int, int], Any],
        current_coords: tuple[int, int],
        left: bool=True,
        right: bool=True,
        up: bool=True,
        down: bool=True,
        up_left: bool=True,
        up_right: bool=True,
        down_left: bool=True,
        down_right: bool=True
) -> list[tuple[int, int]]:

    neighbor_coords: list[tuple[int, int]] = []

    if left:
        neighbor_coords += [(current_coords[0] - 1, current_coords[1])] if (current_coords[0] - 1, current_coords[1]) in map else []

    if right:
        neighbor_coords += [(current_coords[0] + 1, current_coords[1])] if (current_coords[0] + 1, current_coords[1]) in map else []

    if up:
        neighbor_coords += [(current_coords[0], current_coords[1] - 1)] if (current_coords[0], current_coords[1] - 1) in map else []

    if down:
        neighbor_coords += [(current_coords[0], current_coords[1] + 1)] if (current_coords[0], current_coords[1] + 1) in map else []

    if up_left:
        neighbor_coords += [(current_coords[0] - 1, current_coords[1] - 1)] if (current_coords[0] - 1, current_coords[1] - 1) in map else []

    if up_right:
        neighbor_coords += [(current_coords[0] + 1, current_coords[1] - 1)] if (current_coords[0] + 1, current_coords[1] - 1) in map else []

    if down_left:
        neighbor_coords += [(current_coords[0] - 1, current_coords[1] + 1)] if (current_coords[0] - 1, current_coords[1] + 1) in map else []

    if down_right:
        neighbor_coords += [(current_coords[0] + 1, current_coords[1] + 1)] if (current_coords[0] + 1, current_coords[1] + 1) in map else []

    return neighbor_coords


def get_neighbors(
        map: dict[tuple[int, int], T],
        current_coords: tuple[int, int],
        horizontal: bool=True,
        vertical: bool=True,
        diagonal: bool=True
) -> list[tuple[tuple[int, int], T]]:

    return get_neighbors_with_specific_directions(map, current_coords, horizontal, horizontal, vertical, vertical, diagonal, diagonal, diagonal, diagonal)


def get_neighbors_with_specific_directions(
        map: dict[tuple[int, int], T],
        current_coords: tuple[int, int],
        left: bool,
        right: bool,
        up: bool,
        down: bool,
        up_left: bool,
        up_right: bool,
        down_left: bool,
        down_right: bool
) -> list[tuple[tuple[int, int], T]]:
    
    neighbor_coords = get_neighbor_coords_with_specific_directions(map, current_coords, left, right, up, down, up_left, up_right, down_left, down_right)

    return [(coords, map[coords]) for coords in neighbor_coords]


def get_matching_neighbors(
        map: dict[tuple[int, int], T],
        current_coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        horizontal: bool=True,
        vertical: bool=True,
        diagonal: bool=True
) -> list[tuple[tuple[int, int], T]]:
    
    neighbors = get_neighbors(map, current_coords, horizontal, vertical, diagonal)
    return [neighbor for neighbor in neighbors if matching_function(current_coords, neighbor)]


def has_matching_neighbors(
        map: dict[tuple[int, int], T],
        current_coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        horizontal: bool=True,
        vertical: bool=True,
        diagonal: bool=True
) -> bool:
    
    return len(get_matching_neighbors(map, current_coords, matching_function, horizontal, vertical, diagonal)) > 0
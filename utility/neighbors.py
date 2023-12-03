from typing import Any, Callable, TypeVar


T = TypeVar("T")


def get_neighbor_coords(
        map: dict[tuple[int, int], Any],
        current_coords: tuple[int, int],
        horizontal: bool=True,
        vertical: bool=True,
        diagonal: bool=True
) -> list[tuple[int, int]]:

    neighbor_coords = list()

    if (horizontal):
        neighbor_coords += [(x, current_coords[1]) for x in range(current_coords[0]-1, current_coords[0]+2, 2) if (x, current_coords[1]) in map]

    if (vertical):
        neighbor_coords += [(current_coords[0], y) for y in range(current_coords[1]-1, current_coords[1]+2, 2) if (current_coords[0], y) in map]

    if (diagonal):
        neighbor_coords += [(x, y) for x in range(current_coords[0]-1, current_coords[0]+2, 2) for y in range(current_coords[1]-1, current_coords[1]+2, 2) if (x, y) in map]

    return neighbor_coords


def get_neighbors(
        map: dict[tuple[int, int], T],
        current_coords: tuple[int, int],
        horizontal: bool=True,
        vertical: bool=True,
        diagonal: bool=True
) -> list[tuple[tuple[int, int], T]]:

    neighbor_coords = get_neighbor_coords(map, current_coords, horizontal, vertical, diagonal)

    return [(coords, map[coords]) for coords in neighbor_coords]


def get_matching_neighbors(
        map: dict[tuple[int, int], T],
        current_coords: tuple[int, int],
        matching_function: Callable[[T], bool],
        horizontal: bool=True,
        vertical: bool=True,
        diagonal: bool=True
) -> list[tuple[tuple[int, int], T]]:
    
    neighbors = get_neighbors(map, current_coords, horizontal, vertical, diagonal)
    return [neighbor for neighbor in neighbors if matching_function(neighbor[1])]

def has_matching_neighbors(
        map: dict[tuple[int, int], T],
        current_coords: tuple[int, int],
        matching_function: Callable[[T], bool],
        horizontal: bool=True,
        vertical: bool=True,
        diagonal: bool=True
) -> bool:
    
    return len(get_matching_neighbors(map, current_coords, matching_function, horizontal, vertical, diagonal)) > 0
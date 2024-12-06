from typing import Any, Callable, Type


def generate_map_with_coordinates[T](map_list: list[list[Any] | str], cast_to: Type[T]=str) -> dict[tuple[int, int], T]:
    """
    Takes a list of lists or strings and generates a map which uses coordinates as the keys and the inner list elements or the strings individual characters as the values.

    Parameters
    ----------
    map_list: list[list[Any] | str]
        The list that should be converted into a map with coordinates. The indices of the list elements will be the y-coordinates. If the list elements are lists themselves, their indices will be the x-coordinates. If the list elements are strings, then the indices of the chars in the string will become the x-coordinates.
    cast_to: Type[T] = str
        The type to which the final map's elements should be casted (e.g. to convert a list of strings to a map with coords containing integers).

    Returns
    -------
    dict[tuple[int, int], T]
        A dictionary which keys are tuple containing the x- and y-coords of the map and which values are the corresponding values at those coords. The values have the type of the `cast_to`-parameter.
    """

    map: dict[tuple[int, int], T] = {}

    for y, row in enumerate(map_list):
        for x, element in enumerate(row):
            map[x, y] = cast_to(element)

    return map


def get_map_dimensions(map: dict[tuple[int, int], Any]) -> tuple[int, int]:
    x_coords: set[int] = set()
    y_coords: set[int] = set()

    for x, y in map.keys():
        x_coords.add(x)
        y_coords.add(y)

    return max(x_coords) + 1, max(y_coords) + 1


def get_map_row(map: dict[tuple[int, int], T], row: int) -> list[tuple[tuple[int, int], T]]:
    return [((x, y), element) for (x, y), element in map.items() if (y == row)]


def get_map_column(map: dict[tuple[int, int], T], column: int) -> list[tuple[tuple[int, int], T]]:
    return [((x, y), element) for (x, y), element in map.items() if (x == column)]


def print_map(map: dict[tuple[int, int], Any], end: str="") -> None:
    for y in range(get_map_dimensions(map)[1]):
        row: str = ""
        for _, element in sorted([element for element in get_map_row(map, y)], key=lambda element: element[0][0]):
            row += str(element)

        print(row)

    print(end=end)


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


def flood_fill_area(
        map: dict[tuple[int, int], T],
        start_coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        diagonal: bool=False
) -> list[tuple[int, int]]:
    
    if not matching_function(start_coords, (start_coords, map[start_coords])):
        return []
    
    filled_area: list[tuple[int, int]] = []
    queue: set[tuple[int, int]] = {start_coords}

    while (len(queue) > 0):
        current_coords = queue.pop()
        filled_area.append(current_coords)

        matching_neighbors = get_matching_neighbors(map, current_coords, matching_function, diagonal=diagonal)

        for coords in [coords for coords, _ in matching_neighbors if coords not in filled_area]:
            queue.add(coords)

    return filled_area


def flood_fill_area_recursively(
        map: dict[tuple[int, int], T],
        start_coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        filled_area: list[tuple[int, int]],
        diagonal: bool=False
) -> None:
    
    if start_coords in filled_area:
        return
    
    filled_area.append(start_coords)

    matching_neighbors = get_matching_neighbors(map, start_coords, matching_function, diagonal=diagonal)

    for coords in [coords for coords, _ in matching_neighbors if coords not in filled_area]:
        flood_fill_area_recursively(map, coords, matching_function, filled_area, diagonal)
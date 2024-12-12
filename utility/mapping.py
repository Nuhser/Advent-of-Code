from typing import Any, Callable


class Map[T]:
    def __init__(
        self,
        map_list: list[list[Any] | str],
        cast_to: type[T] = str,
        filter: None | Callable[[tuple[int, int], Any], bool] = None,
    ):
        self.map: dict[tuple[int, int], T] = {}

        for y, row in enumerate(map_list):
            for x, element in enumerate(row):
                if (filter == None) or filter((x, y), element):
                    self.map[x, y] = cast_to(element)  # type: ignore

    def __add__(self, other: "Map[T]") -> "Map[T]":
        new_map: dict[tuple[int, int], T] = self.map.copy()
        for coords, value in other.map.items():
            if coords in new_map:
                if value != new_map[coords]:
                    raise KeyError(
                        f"Both maps contain different values at coords {coords}. The values need to be the same or at least one of the maps can't contain a value for the coords."
                    )
            else:
                new_map[coords] = value

        return Map.from_dict(new_map)

    def __eq__(self, other) -> bool:
        return self.map == other.map

    def __len__(self) -> int:
        return len(self.map)

    def __str__(self) -> str:
        rows: list[str] = []

        dim_x, dim_y = self.get_dimensions()
        for y in range(dim_y):
            rows.append("")
            for x in range(dim_x):
                rows[-1] += str(self.map[x, y]) if (x, y) in self.map else " "

        return "\n".join(rows)

    @classmethod
    def from_dict(cls, dictionary: dict[tuple[int, int], T]) -> "Map[T]":
        obj = cls.__new__(cls)
        obj.map = dictionary.copy()
        return obj

    def get(self, coords: tuple[int, int]) -> T | None:
        if not coords in self.map:
            return None

        return self.map[coords]

    def set(self, coords: tuple[int, int], value: T) -> T | None:
        old_value: T | None = self.get(coords)
        self.map[coords] = value
        return old_value

    def get_row(self, row_number: int) -> list[tuple[tuple[int, int], T]]:
        return [
            ((x, y), value) for (x, y), value in self.map.items() if (y == row_number)
        ]

    def get_column(self, column_number: int) -> list[tuple[tuple[int, int], T]]:
        return [
            ((x, y), value)
            for (x, y), value in self.map.items()
            if (x == column_number)
        ]

    def get_all_coords(self) -> list[tuple[int, int]]:
        return [coords for coords, _ in self.map.items()]

    def get_all_values(self) -> list[T]:
        return [value for _, value in self.map.items()]

    def get_dimensions(self) -> tuple[int, int]:
        x_coords: set[int] = set()
        y_coords: set[int] = set()

        for x, y in self.map.keys():
            x_coords.add(x)
            y_coords.add(y)

        return max(x_coords) + 1, max(y_coords) + 1

    def get_inverted_map(self) -> dict[T, list[tuple[int, int]]]:
        inverted_map: dict[T, list[tuple[int, int]]] = dict()

        for key, value in self.map.items():
            if value not in inverted_map:
                inverted_map[value] = []

            inverted_map[value].append(key)

        return inverted_map

    def contains_coords(self, coords: tuple[int, int]) -> bool:
        if (coords[0] < 0) or (coords[1] < 0):
            return False

        dimensions = self.get_dimensions()

        if (coords[0] >= dimensions[0]) or (coords[1] >= dimensions[1]):
            return False

        return True

    def get_neighbor_coords_for_specific_directions(
        self,
        coords: tuple[int, int],
        left: bool = True,
        right: bool = True,
        up: bool = True,
        down: bool = True,
        up_left: bool = True,
        up_right: bool = True,
        down_left: bool = True,
        down_right: bool = True,
    ) -> list[tuple[int, int]]:

        if coords not in self.map:
            raise KeyError(f"Coords {coords} are not in map.")

        neighbor_coords: list[tuple[int, int]] = []

        if left:
            neighbor_coords += (
                [(coords[0] - 1, coords[1])]
                if (coords[0] - 1, coords[1]) in self.map
                else []
            )

        if right:
            neighbor_coords += (
                [(coords[0] + 1, coords[1])]
                if (coords[0] + 1, coords[1]) in self.map
                else []
            )

        if up:
            neighbor_coords += (
                [(coords[0], coords[1] - 1)]
                if (coords[0], coords[1] - 1) in self.map
                else []
            )

        if down:
            neighbor_coords += (
                [(coords[0], coords[1] + 1)]
                if (coords[0], coords[1] + 1) in self.map
                else []
            )

        if up_left:
            neighbor_coords += (
                [(coords[0] - 1, coords[1] - 1)]
                if (coords[0] - 1, coords[1] - 1) in self.map
                else []
            )

        if up_right:
            neighbor_coords += (
                [(coords[0] + 1, coords[1] - 1)]
                if (coords[0] + 1, coords[1] - 1) in self.map
                else []
            )

        if down_left:
            neighbor_coords += (
                [(coords[0] - 1, coords[1] + 1)]
                if (coords[0] - 1, coords[1] + 1) in self.map
                else []
            )

        if down_right:
            neighbor_coords += (
                [(coords[0] + 1, coords[1] + 1)]
                if (coords[0] + 1, coords[1] + 1) in self.map
                else []
            )

        return neighbor_coords

    def get_neighbors(
        self,
        coords: tuple[int, int],
        horizontal: bool = True,
        vertical: bool = True,
        diagonal: bool = True,
    ) -> list[tuple[tuple[int, int], T]]:

        return self.get_neighbors_with_specific_directions(
            coords,
            horizontal,
            horizontal,
            vertical,
            vertical,
            diagonal,
            diagonal,
            diagonal,
            diagonal,
        )

    def get_neighbors_with_specific_directions(
        self,
        coords: tuple[int, int],
        left: bool,
        right: bool,
        up: bool,
        down: bool,
        up_left: bool,
        up_right: bool,
        down_left: bool,
        down_right: bool,
    ) -> list[tuple[tuple[int, int], T]]:

        neighbor_coords = self.get_neighbor_coords_for_specific_directions(
            coords,
            left,
            right,
            up,
            down,
            up_left,
            up_right,
            down_left,
            down_right,
        )

        return [(coords, self.map[coords]) for coords in neighbor_coords]

    def get_matching_neighbors(
        self,
        coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        horizontal: bool = True,
        vertical: bool = True,
        diagonal: bool = True,
    ) -> list[tuple[tuple[int, int], T]]:

        neighbors = self.get_neighbors(coords, horizontal, vertical, diagonal)
        return [
            neighbor for neighbor in neighbors if matching_function(coords, neighbor)
        ]

    def has_matching_neighbors(
        self,
        coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        horizontal: bool = True,
        vertical: bool = True,
        diagonal: bool = True,
    ) -> bool:

        return (
            len(
                self.get_matching_neighbors(
                    coords, matching_function, horizontal, vertical, diagonal
                )
            )
            > 0
        )


def generate_map_with_coordinates[
    T
](map_list: list[list[Any] | str], cast_to: type[T] = str) -> dict[tuple[int, int], T]:
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
            map[x, y] = cast_to(element)  # type: ignore

    return map


def invert_map[T](map: dict[tuple[int, int], T]) -> dict[T, list[tuple[int, int]]]:
    inverted_map: dict[T, list[tuple[int, int]]] = dict()

    for coords, frequency in map.items():
        if frequency not in inverted_map:
            inverted_map[frequency] = []

        inverted_map[frequency].append(coords)

    return inverted_map


def get_map_dimensions[T](map: dict[tuple[int, int], T]) -> tuple[int, int]:
    x_coords: set[int] = set()
    y_coords: set[int] = set()

    for x, y in map.keys():
        x_coords.add(x)
        y_coords.add(y)

    return max(x_coords) + 1, max(y_coords) + 1


def is_coord_in_map[T](map: dict[tuple[int, int], T], coord: tuple[int, int]) -> bool:
    if (coord[0] < 0) or (coord[1] < 0):
        return False

    dimensions = get_map_dimensions(map)

    if (coord[0] >= dimensions[0]) or (coord[1] >= dimensions[1]):
        return False

    return True


def get_map_row[
    T
](map: dict[tuple[int, int], T], row: int) -> list[tuple[tuple[int, int], T]]:
    return [((x, y), element) for (x, y), element in map.items() if (y == row)]


def get_map_column[
    T
](map: dict[tuple[int, int], T], column: int) -> list[tuple[tuple[int, int], T]]:
    return [((x, y), element) for (x, y), element in map.items() if (x == column)]


def print_map(map: dict[tuple[int, int], Any], end: str = "") -> None:
    for y in range(get_map_dimensions(map)[1]):
        row: str = ""
        for _, element in sorted(
            [element for element in get_map_row(map, y)],
            key=lambda element: element[0][0],
        ):
            row += str(element)

        print(row)

    print(end=end)


def get_neighbor_coords_with_specific_directions(
    map: dict[tuple[int, int], Any],
    current_coords: tuple[int, int],
    left: bool = True,
    right: bool = True,
    up: bool = True,
    down: bool = True,
    up_left: bool = True,
    up_right: bool = True,
    down_left: bool = True,
    down_right: bool = True,
) -> list[tuple[int, int]]:

    neighbor_coords: list[tuple[int, int]] = []

    if left:
        neighbor_coords += (
            [(current_coords[0] - 1, current_coords[1])]
            if (current_coords[0] - 1, current_coords[1]) in map
            else []
        )

    if right:
        neighbor_coords += (
            [(current_coords[0] + 1, current_coords[1])]
            if (current_coords[0] + 1, current_coords[1]) in map
            else []
        )

    if up:
        neighbor_coords += (
            [(current_coords[0], current_coords[1] - 1)]
            if (current_coords[0], current_coords[1] - 1) in map
            else []
        )

    if down:
        neighbor_coords += (
            [(current_coords[0], current_coords[1] + 1)]
            if (current_coords[0], current_coords[1] + 1) in map
            else []
        )

    if up_left:
        neighbor_coords += (
            [(current_coords[0] - 1, current_coords[1] - 1)]
            if (current_coords[0] - 1, current_coords[1] - 1) in map
            else []
        )

    if up_right:
        neighbor_coords += (
            [(current_coords[0] + 1, current_coords[1] - 1)]
            if (current_coords[0] + 1, current_coords[1] - 1) in map
            else []
        )

    if down_left:
        neighbor_coords += (
            [(current_coords[0] - 1, current_coords[1] + 1)]
            if (current_coords[0] - 1, current_coords[1] + 1) in map
            else []
        )

    if down_right:
        neighbor_coords += (
            [(current_coords[0] + 1, current_coords[1] + 1)]
            if (current_coords[0] + 1, current_coords[1] + 1) in map
            else []
        )

    return neighbor_coords


def get_neighbors[
    T
](
    map: dict[tuple[int, int], T],
    current_coords: tuple[int, int],
    horizontal: bool = True,
    vertical: bool = True,
    diagonal: bool = True,
) -> list[tuple[tuple[int, int], T]]:

    return get_neighbors_with_specific_directions(
        map,
        current_coords,
        horizontal,
        horizontal,
        vertical,
        vertical,
        diagonal,
        diagonal,
        diagonal,
        diagonal,
    )


def get_neighbors_with_specific_directions[
    T
](
    map: dict[tuple[int, int], T],
    current_coords: tuple[int, int],
    left: bool,
    right: bool,
    up: bool,
    down: bool,
    up_left: bool,
    up_right: bool,
    down_left: bool,
    down_right: bool,
) -> list[tuple[tuple[int, int], T]]:

    neighbor_coords = get_neighbor_coords_with_specific_directions(
        map,
        current_coords,
        left,
        right,
        up,
        down,
        up_left,
        up_right,
        down_left,
        down_right,
    )

    return [(coords, map[coords]) for coords in neighbor_coords]


def get_matching_neighbors[
    T
](
    map: dict[tuple[int, int], T],
    current_coords: tuple[int, int],
    matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
    horizontal: bool = True,
    vertical: bool = True,
    diagonal: bool = True,
) -> list[tuple[tuple[int, int], T]]:

    neighbors = get_neighbors(map, current_coords, horizontal, vertical, diagonal)
    return [
        neighbor
        for neighbor in neighbors
        if matching_function(current_coords, neighbor)
    ]


def has_matching_neighbors[
    T
](
    map: dict[tuple[int, int], T],
    current_coords: tuple[int, int],
    matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
    horizontal: bool = True,
    vertical: bool = True,
    diagonal: bool = True,
) -> bool:

    return (
        len(
            get_matching_neighbors(
                map, current_coords, matching_function, horizontal, vertical, diagonal
            )
        )
        > 0
    )


def flood_fill_area[
    T
](
    map: dict[tuple[int, int], T],
    start_coords: tuple[int, int],
    matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
    diagonal: bool = False,
) -> list[tuple[int, int]]:

    if not matching_function(start_coords, (start_coords, map[start_coords])):
        return []

    filled_area: list[tuple[int, int]] = []
    queue: set[tuple[int, int]] = {start_coords}

    while len(queue) > 0:
        current_coords = queue.pop()
        filled_area.append(current_coords)

        matching_neighbors = get_matching_neighbors(
            map, current_coords, matching_function, diagonal=diagonal
        )

        for coords in [
            coords for coords, _ in matching_neighbors if coords not in filled_area
        ]:
            queue.add(coords)

    return filled_area


def flood_fill_area_recursively[
    T
](
    map: dict[tuple[int, int], T],
    start_coords: tuple[int, int],
    matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
    filled_area: list[tuple[int, int]],
    diagonal: bool = False,
) -> None:

    if start_coords in filled_area:
        return

    filled_area.append(start_coords)

    matching_neighbors = get_matching_neighbors(
        map, start_coords, matching_function, diagonal=diagonal
    )

    for coords in [
        coords for coords, _ in matching_neighbors if coords not in filled_area
    ]:
        flood_fill_area_recursively(
            map, coords, matching_function, filled_area, diagonal
        )
